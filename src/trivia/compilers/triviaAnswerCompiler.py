import re
import traceback
from typing import Collection, Final, Pattern

import roman
import unicodedata
from frozenlist import FrozenList
from num2words import num2words
from roman import RomanError

from .triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from ..triviaExceptions import BadTriviaAnswerException
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TriviaAnswerCompiler(TriviaAnswerCompilerInterface):

    """_summary_

    This class is used for improving answer handling. Trivia answers often take an assortment of
    different common forms, many of which can be parsed/interpreted to remove unnecessary chunks,
    or to improve answer handling.

    For example, the answer "to run" has a pretty important word at the beginning (to). This class
    will scan for that string, and convert it into just "run". Another example, if an answer is
    "President George Washington", this class will convert it into "(President) George Washington".

    There are many other simple conversions that this class performs, but those are some key examples.
    """

    def __init__(
        self,
        timber: TimberInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: Final[TimberInterface] = timber

        self.__ampersandRegEx: Final[Pattern] = re.compile(r'(^&\s+)|(\s+&\s+)|(\s+&$)', re.IGNORECASE)
        self.__decadeRegEx: Final[Pattern] = re.compile(r'^((in\s+)?the\s+)?(\d{4})\'?s$', re.IGNORECASE)
        self.__equationRegEx: Final[Pattern] = re.compile(r'([a-z])\s*=\s*(-?(?:\d*\.)?\d+)', re.IGNORECASE)
        self.__firstMiddleLastNameRegEx: Final[Pattern] = re.compile(r'^\w+\s+(\w\.?)\s+\w+(\s+(i{0,3}|iv|vi{0,3}|i?x|jr\.?|junior|senior|sr\.?)\.?)?$', re.IGNORECASE)
        self.__firstNameAndMiddleInitialGroupedMatchRegEx: Final[Pattern] = re.compile(r'^\(\w+\s+(\w\.?)\)\s+\w+(\s+(i{0,3}|iv|vi{0,3}|i?x|jr\.?|junior|senior|sr\.?)\.?)?$', re.IGNORECASE)
        self.__hashRegEx: Final[Pattern] = re.compile(r'(#)')
        self.__honoraryPrefixRegEx: Final[Pattern] = re.compile(r'^(bishop|brother|captain|chancellor|chief|colonel|corporal|csar|czar|dean|director|doctor|dr\.?|duke|earl|esq|esquire|executive|father|general|judge|king|lady|lieutenant|lord|madam|madame|master|minister|miss|missus|mister|mistress|mother|mr\.?|mrs\.?|ms\.?|mx\.?|officer|president|priest|prime minister|principal|private|professor|queen|rabbi|representative|reverend|saint|secretary|senator|senior|sister|sir|sire|teacher|tsar|tzar|warden)\s+', re.IGNORECASE)
        self.__japaneseHonorarySuffixRegEx: Final[Pattern] = re.compile(r'(\s|-)(chan|kohai|kouhai|kun|sama|san|senpai|sensei|tan)$', re.IGNORECASE)
        self.__multipleChoiceBasicAnswerRegEx: Final[Pattern] = re.compile(r'^\s*([a-z])\s*$', re.IGNORECASE)
        self.__multipleChoiceBracedAnswerRegEx: Final[Pattern] = re.compile(r'^\s*\[([a-z])\]\s*$', re.IGNORECASE)
        self.__multipleChoiceCleanAnswerRegEx: Final[Pattern] = re.compile(r'^\s*[a-z]\s*$', re.IGNORECASE)
        self.__newLineRegEx: Final[Pattern] = re.compile(r'(\n)+', re.IGNORECASE)
        self.__parenGroupRegEx: Final[Pattern] = re.compile(r'(\(.*?\))', re.IGNORECASE)
        self.__phraseAnswerRegEx: Final[Pattern] = re.compile(r'[^A-Za-z0-9\-_ ]|(?<=\s)\s+', re.IGNORECASE)
        self.__phraseDigitAnswerRegEx: Final[Pattern] = re.compile(r'[^A-Za-z0-9\-_/ ]|(?<=\s)\s+', re.IGNORECASE)
        self.__possessivePronounPrefixRegEx: Final[Pattern] = re.compile(r'^(her|his|my|our|their|your)\s+', re.IGNORECASE)
        self.__prefixRegEx: Final[Pattern] = re.compile(r'^(a|an|and|at|as|by|for|in|of|on|that|the|these|this|those|to|with((\s+that)|(\s+the)|(\s+these)|(\s+this)|(\s+those))?)\s+', re.IGNORECASE)
        self.__simpleTimeDurationRegEx: Final[Pattern] = re.compile(r'^((\d+)\s+(second|minute|hour|day|month|year)s?)(\s+old)?$', re.IGNORECASE)
        self.__tagRemovalRegEx: Final[Pattern] = re.compile(r'[<\[]\/?\w+[>\]]', re.IGNORECASE)
        self.__thingIsPhraseRegEx: Final[Pattern] = re.compile(r'^(he\'?s?|it\'?s?|she\'?s?|they\'?(re)?|we\'?(re)?)\s+((are|is|was|were)\s+)?((a|an|are)\s+)?(\w+\s*\w*)$', re.IGNORECASE)
        self.__thingsThatArePhraseRegEx: Final[Pattern] = re.compile(r'^(things\s+that\s+are)\s+(\w+(\s+)?(\w+)?)$', re.IGNORECASE)
        self.__usDollarRegEx: Final[Pattern] = re.compile(r'^\$?((?!,$)[\d,.]+)(\s+\(?USD?\)?)?$', re.IGNORECASE)
        self.__whiteSpaceRegEx: Final[Pattern] = re.compile(r'\s{2,}', re.IGNORECASE)
        self.__wordDashWordRegEx: Final[Pattern] = re.compile(r'[\-_]', re.IGNORECASE)
        self.__wordSlashWordRegEx: Final[Pattern] = re.compile(r'^([a-z]+)/([a-z]+)(/([a-z]+))?$', re.IGNORECASE)
        self.__wordTheWordRegEx: Final[Pattern] = re.compile(r'^(\w+)\s+(a|an|the)\s+(\w+)$', re.IGNORECASE)

        # RegEx pattern for arabic and roman numerals, returning only one capturing group
        self.__numeralRegEx: Final[Pattern] = re.compile(r'\b(\d+(?:st|nd|rd|th)?|[IVXLCDM]+(?:st|nd|rd|th)?)\b', re.IGNORECASE)

        # RegEx patterns for arabic and roman numerals, returning separate capturing groups for digits and ordinals
        self.__groupedNumeralRegEx: Final[Pattern] = re.compile(r'\b(?:(\d+)|([IVXLCDM]+))(st|nd|rd|th)?\b', re.IGNORECASE)

        # RegEx pattern for finding every individual word in an answer, along with its parens if it has them
        self.__findAllWordsWithOrWithoutParensRegEx: Final[Pattern] = re.compile(r'\(?\b[\w-]+\)?', re.IGNORECASE)

        # RegEx pattern for verifying if a word in an answer has parens
        self.__wordIsFullySurroundedByParensRegEx: Final[Pattern] = re.compile(r'^\([\w-]+\)$', re.IGNORECASE)

        # RegEx pattern for finding all words in an answer that are surrounded by parens
        self.__findAllWordsWithParensRegEx: Final[Pattern] = re.compile(r'\([\w-]+\)', re.IGNORECASE)

        # RegEx pattern for finding all words in an answer, regardless of their parens
        self.__findAllWordsRegEx: Final[Pattern] = re.compile(r'\b[\w-]+', re.IGNORECASE)

        self.__combiningDiacriticsRegEx: Final[Pattern] = re.compile(r'[\u0300-\u036f\u1ab0-\u1aff\u1dc0-\u1dff\u20d0-\u20ff\ufe20-\ufe2f]')

        self.__specialCharsRegEx: Final[Pattern] = re.compile(
            r"""
                (?P<a>[ÅåǺǻḀḁẚĂăẶặẮắẰằẲẳẴẵȂȃâẬậẤấẦầẪẫẨẩẢảǍǎȺⱥȦȧǠǡẠạÄäǞǟÀàȀȁÁáĀāÃãĄąᶏɑᶐⱯɐɒᴀᴬᵃᵄᶛₐªÅ∀@₳ΑαАаⲀⲁⒶⓐ⒜🅰𝔄𝔞𝕬𝖆𝓐𝓪𝒜𝒶𝔸𝕒Ａａ🄰ค𝐀𝐚𝗔𝗮𝘈𝘢𝘼𝙖𝙰𝚊Λ卂ﾑȺᗩΔልДдꚈꚉꚀꚁꙢꙣꭿꋫλ🅐🅰️ꙢꙣꙘѦԬꙙѧԭӒӓҨҩ])|
                (?P<b>[ΒβⲂⲃВвБб𐌁ᛒ𐌱ɓʙɃƀḂḃḄḅḆḇƁᵬᶀꞖꞗᴃᴯᴮᵇƂƃ␢฿₿♭𝐁𝐛𝔹𝕓𝕭𝖇𝑩𝒃🄱🅱️Ⓑⓑ🅑ᙠᗷҍ𝔅𝔟𝓑𝓫𝗕𝗯𝘽𝙗𝘉𝘣Ｂｂ⒝𝙱𝚋𝖡𝖻🇧๖乃𝑏ƄЬᏏᖯᑲ𝒷𝚩ꓐ𝜝𝛣𝝗𐊂𝞑ℬᏴ𐊡𝐵])|
                (?P<c>[СсɕʗᶜᶝᴄꟄꞔĆćĈĉČčĊċḈḉƇƈȻȼÇçꞒꞓↃↄ©℃¢₡₢₵₠ℂℭꜾꜿ𝑐𝗰ｃ𝕔ⲥ𐐽𝖈𝓬𝚌ꮯ𝔠ϲ𝒄𝘤𝒸𝙘𝐜𝖼ⅽ𝕮𝙲𝑪𝒞𝖢𐌂𝗖ꓚᏟＣⲤ𝓒Ⅽ𝘊𐐕𝘾🝌𝐂Ϲ𐊢𝐶])|
                (?P<d>[ԀԁƊɗ𝓭𝚍ⅆ𝑑𝗱Ꮷ𝒅𝘥𝖉ᑯꓒ𝐝𝖽𝔡𝕕ⅾ𝒹𝙙Ꭰ𝕯ⅅ𝓓𝙳𝔇ᗪ𝑫𝘋Ⅾ𝒟𝘿ꓓ𝐃𝖣𝐷𝗗𝔻ᗞ])|
                (?P<e>[ẹėéèеẸĖÉÈЕ𝓮𝚎ｅ𝑒𝗲ⅇ𝒆𝘦℮𝖊ℯ𝐞𝖾ꬲ𝔢𝕖ҽ𝙚𝙴𝛦𝑬𝚬𝜠𝖤Ε𝗘𐊆𝝚𝓔𝞔Ｅ𝔈𝘌Ꭼℰ𝙀ꓰⴹ])|
                (?P<f>[f𝓯𝚏𝑓𝗳𝒇𝘧𝖋𝐟𝖿𝔣ꬵ𝕗ꞙ𝒻𝙛ẝ𝕱Ꞙ𝓕Ϝ𐊇ꓝ𝗙ℱᖴ𝙁𝙵𐊥𝐹])|
                (?P<g>[ġĠ𝓰𝚐ɡցᶃ𝑔𝗴ｇ𝒈𝘨ℊ𝖌𝐠𝗀𝔤𝕘𝙜Ꮐ𝑮𝘎𝕲𝐆𝖦Ԍ𝔊𝔾Ᏻ𝒢𝙂ꓖ𝓖𝙶𝐺𝗚])|
                (?P<h>[һҺᏂ𝖍𝓱𝚑ｈ𝔥ℎ𝒉𝘩հ𝒽𝙝𝐡𝗁𝗵𝕙𝑯𝚮𝕳𝛨𝖧ℋℌℍⲎ𐋏𝜢Η𝓗𝞖𝝜𝗛Н𝘏ꓧＨ𝐇𝙃𝙷Ꮋᕼ𝐻])|
                (?P<i>[іíïІÍÏ𝓲𝞲ꙇⅈｉ𝔦𝘪ӏ𝙞𝚤𝐢𝑖𝕚𝖎Ꭵ𝚒ɩɪ𝒊𝛊ⅰı𝒾𝜾⍳𝜄ꭵ𝗂𝝸ℹι𝗶𝚰𝘭𝖨𝐥ﺍﺎ𝔩ℐℑ𐊊Ⲓ𐌉ℓ𝜤Ɩ𝞘Ι𝚕𝟏∣اＩ𝗅𝕀𝙄𝓁𐌠𝐼𝑰ǀӀᛁ𝟭𝕴ߊｌ𝛪ⵏ𝝞𝕝𝟣𝙡𝓘𝗜𝟙𝑙ןⅠ𝘐١𝒍𝖑￨𝐈۱ꓲ|ⅼ])|
                (?P<j>[јʝЈꞲ𝖏𝓳𝚓ⅉ𝔧ｊ𝒋𝘫𝒿𝙟ϳ𝐣𝗃𝑗𝗷𝕛𝔍𝑱𝘑Ｊ𝒥𝙅Ꭻᒍ𝐉𝖩𝐽𝗝𝕁ꓙ𝕵𝓙𝙹Ϳ])|
                (?P<k>[κΚ𝖐𝓴𝚔𝔨𝒌𝘬𝓀𝙠𝐤𝗄𝑘𝗸𝕜𝑲𝚱𝒦𝜥𝛫𝖪𝝟𝗞ⲔᛕꓗК𝓚𝞙𝔎𝘒Ꮶ𝙆Ｋ])|
                (?P<l>[ӏḷӀḶ𝚰𝘭І𝖨𝐥ﺍﺎ𝔩ℐℑ𐊊Ⲓ𐌉ℓ𝜤Ɩ𝞘Ι𝚕𝟏∣ا𝗅𝕀𝙄𝓁𐌠𝐼𝑰ǀᛁ𝟭𝕴ߊｌ𝛪ⵏ𝝞𝕝𝟣ו𞣇𝙡𝓘𝗜𝟙𝑙ןⅠ𝘐١𝒍𝖑𝐈۱|ⅼ𝖫Ⳑ𝗟ℒ𝓛Ꮮꓡ𐐛𝘓𝙇ᒪⅬ])|
                (?P<m>[m𝔪𝕞𝓂𝙢𝓶𝚖𝑚𝗺ⅿ𝛭𝑴𝚳𝜧𐌑𝖬𝗠ᛖ𝝡Ⲙ𝓜ΜМ𝞛ꓟ𝔐𝘔𝙈𐊰𝐌ＭⅯ𝑀ᗰℳ𝕄Ꮇ𝕸Ϻ𝙼])|
                (?P<n>[ոՈΝれり𝒏𝘯𝖓𝐧𝗇𝔫𝕟𝓃𝙣𝓷𝚗ռ𝑛𝗻ꓠ𝛮𝐍𝖭𝚴𝔑𝜨Ｎ𝒩𝙉𝓝𝙽ℕ𝝢𝑁𝗡Ⲛ𝑵𝘕𝞜𝕹])|
                (?P<o>[оᴏοօØøǾǿÖöȪȫÓóÒòÔôỐốỒồỔổỖỗỘộǑǒŐőŎŏȎȏȮȯȰȱỌọƟɵƠơỚớỜờỠỡỢợỞởỎỏŌōṒṓṐṑÕõȬȭṌṍṎṏǪǫȌȍǬǭꝌꝍⱺᴏᴼᵒᴑᴓꬽꬾꬿꭃꭄₒꝊꝋ∅ºΟοⲞⲟОо𐌏ՕօＯｏ◎Ⓞ⒪⓪⓿⍟Ꜿꜿ𝘰ంಂംං𝐨𐓪𝚘ဝ𝛐ഠ𝛔𝗈𝝈𝝄𝞸𝞼၀σ๐໐𝕠𐐬𝙤ە𝑜𝒐ס𝜎𝖔٥०੦૦௦౦೦൦𝜊𝝾۵𝞂𝓸𝗼ჿ߀𝛰〇𐊒𝟬𝒪𝜪ዐ𝓞𝞞𝝤ⵔ𝟢𝗢𝟘𝘖ଠ𝟎𝐎০୦𝔒𝕆𝙊𐊫𝙾ꓳ𐐄𝟶𝑶𝚶𐓂𝕺])|
                (?P<p>[рРρ𝔭𝘱𝙥𝐩ｐ𝛠𝑝𝕡𝖕𝜚𝚙𝞎ⲣ𝝔𝛒𝒑𝟈𝝆𝓅𝜌𝗉𝞀ϱ𝗽⍴𝞺𝓹𝖯𝛲𝝦𝜬𝒫𐊕𝞠𝓟ꓑ𝗣ℙ𝘗𝐏ΡⲢᏢ𝙋ᑭＰ𝙿𝑃𝚸𝑷])|
                (?P<q>[զԶ𝔮գ𝒒𝘲𝓆𝙦𝐪𝗊𝑞𝗾𝕢𝖖ԛ𝓺𝚚𝐐𝖰𝔔𝒬𝙌𝓠𝚀𝑄𝗤ⵕ𝑸𝘘ℚ𝕼])|
                (?P<r>[r𝔯ꮁ𝒓𝘳ⲅᴦꭇꭈ𝓇𝙧𝐫𝗋𝑟𝗿г𝕣𝖗𝓻𝚛ᎡꓣƦ𝐑𝖱ᖇ𐒴𝑅𝗥Ꮢ𝕽𝓡𝚁ℛℜℝ])|
                (?P<s>[ʂꟅꮪ𝐬𝗌𝑠𝘀ꜱｓ𝕤ѕ𝖘𝓼𝚜𐑈ƽ𝒮𝙎ꓢ𐐠Ѕ𝐒𝖲𝑆𝗦𐊖𝕊Տ𝕾ＳᏕ𝓢𝚂𝔖Ꮪ𝑺𝘚])|
                (?P<t>[𝐭𝗍𝔱𝕥𝓉𝙩𝓽𝚝𝑡𝘁𝒕𝘵𝖙𝒯𝜯𝖳𝗧𐊗𐌕𝝩🝨ꓔТᎢ⊤Τ𝐓Ⲧ𝑇𐊱𝕋Ｔ𝚃𝛵𝑻𝚻])|
                (?P<u>[υսüúùՍÜÚÙ𝐮𝔲ʋ𝙪ꭎ𐓶𝚞ꭒ𝑢𝒖𝛖ᴜ𝖚ꞟ𝜐𝗎𝓊𝝊𝓾𝞾𝞄𝘂𝘶𝒰𝙐ሀ⋃𝐔𝖴𝑈𝗨ᑌ𝖀𝓤𝚄ꓴ𐓎𝔘𝑼𝘜])|
                (?P<v>[νѵѴⱯ∀⋁𝐯𝔳𝕧𝙫𝚟𝑣ｖט𝒗𝖛ᴠ𝗏ꮩ𝓋𝓿ⅴ𝘃𝝂𝘷𝞶Ꮩ𝐕Ⅴꓦ٧𝙑ᐯ𝑽۷𝖁ⴸ𝖵])|
                (?P<w>[w𝐰𝗐ᴡѡաꮃ𝔴𝕨𝓌𝙬ɯ𝔀𝚠𝒘𝘸𝖜ԝ𝕎𝒲𝙒𝓦𝚆ꓪ𝑊𝗪ᎳᏔ𝖂𝐖𝖶Ԝ𝔚])|
                (?P<x>[хҳХҲᕁ𝓍𝙭𝐱𝗑⤫𝑥𝘅⤬᙮⨯𝕩𝖝×𝔁𝚡ｘⅹ𝔵ᕽ𝒙𝘹𝒳𝜲𝓧𝞦𐊐𝝬𐌗𝗫𝘟𝐗𝔛ⵝΧⅩ𝚇ꓫⲬ᙭𝑋𐊴𝑿𝚾╳Ꭓ𝖃ᚷＸ𝛸𐌢𝖷])|
                (?P<y>[уýУÝΥ𝙮𝐲𝝲𝑦ᶌ𝞬ʏ𝖞𝚢ｙꭚ𝒚𝓎ɣ𝗒ყ𝘆ү𝛾γ𝛄𝔂𝜸𝔶ℽ𝘺ỿϒ𝔜𝕐𝙔𝚈ⲨᎩ𐊲𝑌ꓬҮ𝒀𝖄𝖸Ｙ𝛶𝚼Ꮍ])|
                (?P<z>[ʐżŻ𝓏𝙯ᴢ𝐳𝗓ꮓ𝔃𝚣𝔷𝒛𝘻𝗭𝚭ᏃΖ𝘡𝜡𝙕𝞕ꓜ𝝛𝐙𝑍ℤℨ𝖅Ｚ𝒵𝖹])
            """,
            re.VERBOSE | re.IGNORECASE,
        )

        self.__globalOptionalWords: Final[frozenset[str]] = frozenset({
            'a', 'an' ,'city', 'continent', 'county', 'island', 'islands', 'isle', 'lake',
            'mountain', 'mountains', 'ocean', 'park', 'pond', 'river', 'road', 'sea', 'street',
            'the', 'town',
        })

    async def compileBoolAnswer(self, answer: str | None) -> bool:
        if answer is not None and not isinstance(answer, str):
            raise BadTriviaAnswerException(f'answer can\'t be compiled to bool ({answer=})')

        cleanedAnswer = utils.cleanStr(answer)

        try:
            return utils.strictStrToBool(cleanedAnswer)
        except Exception as e:
            raise BadTriviaAnswerException(f'answer can\'t be compiled to bool ({answer=}) ({cleanedAnswer=}): {e}')

    async def compileMultipleChoiceAnswer(self, answer: str | None) -> int:
        if not utils.isValidStr(answer):
            raise BadTriviaAnswerException(f'answer can\'t be compiled to multiple choice ordinal ({answer=})')

        answer = utils.cleanStr(answer)
        cleanedAnswer: str | None = None

        # check if the answer is just an alphabetical character from A to Z
        basicAnswerMatch = self.__multipleChoiceBasicAnswerRegEx.fullmatch(answer)
        if basicAnswerMatch is not None and utils.isValidStr(basicAnswerMatch.group(1)):
            cleanedAnswer = basicAnswerMatch.group(1)

        if not utils.isValidStr(cleanedAnswer):
            # check if the answer is an alphabetical character that is surrounded by braces, like "[A]" or "[B]"
            bracedAnswerMatch = self.__multipleChoiceBracedAnswerRegEx.fullmatch(answer)

            if bracedAnswerMatch is not None and utils.isValidStr(bracedAnswerMatch.group(1)):
                cleanedAnswer = bracedAnswerMatch.group(1)

        if not utils.isValidStr(cleanedAnswer) or len(cleanedAnswer) != 1 or self.__multipleChoiceCleanAnswerRegEx.fullmatch(cleanedAnswer) is None:
            raise BadTriviaAnswerException(f'answer can\'t be compiled to multiple choice ordinal ({answer=}) ({cleanedAnswer=})')

        # this converts the answer 'A' into 0, 'B' into 1, 'C' into 2, and so on...
        return ord(cleanedAnswer.upper()) % 65

    async def compileTextAnswer(self, answer: str | None) -> str:
        if answer is not None and not isinstance(answer, str):
            raise TypeError(f'answer argument is malformed: \"{answer}\"')

        if not utils.isValidStr(answer):
            return ''

        answer = answer.lower().strip()

        # removes HTML tag-like junk
        answer = self.__tagRemovalRegEx.sub('', answer).strip()

        # replaces all new line characters with just a space
        answer = self.__newLineRegEx.sub(' ', answer).strip()

        # replaces the '&' character, when used like the word "and", with the word "and"
        answer = self.__ampersandRegEx.sub(' and ', answer).strip()

        # convert special characters to latin where possible
        answer = await self.__fancyToLatin(answer)

        if any(character.isdigit() for character in answer):
            # only remove some special characters (if there are digits in the answer)
            answer = self.__phraseDigitAnswerRegEx.sub('', answer).strip()
        else:
            # completely remove most special characters (if there are no digits in the answer)
            answer = self.__phraseAnswerRegEx.sub('', answer).strip()

        # removes common prefix words that shouldn't be necessary to an answer's comprehensibility
        answer = self.__prefixRegEx.sub('', answer).strip()

        return answer

    async def compileTextAnswersList(
        self,
        answers: Collection[str | None] | None,
        allWords: frozenset[str] | None = None,
        expandParentheses: bool = True,
    ) -> list[str]:
        if answers is not None and not isinstance(answers, Collection):
            raise TypeError(f'answers argument is malformed: \"{answers}\"')
        elif allWords is not None and not isinstance(allWords, frozenset):
            raise TypeError(f'allWords argument is malformed: \"{allWords}\"')
        elif not utils.isValidBool(expandParentheses):
            raise TypeError(f'expandParentheses argument is malformed: \"{expandParentheses}\"')

        frozenAnswers: FrozenList[str | None] = FrozenList(answers)
        frozenAnswers.freeze()

        if frozenAnswers is None or len(frozenAnswers) == 0:
            return list()

        compiledAnswers: set[str] = set()

        for answer in frozenAnswers:
            if not utils.isValidStr(answer):
                continue

            cases = await self.__expandSpecialCases(
                answer = answer,
            )

            for case in cases:
                if expandParentheses:
                    possibilities = await self.__getParentheticalPossibilities(
                        allWords = allWords,
                        answer = case,
                    )
                else:
                    possibilities = [ case ]

                for possibility in possibilities:
                    compiledAnswer = await self.compileTextAnswer(
                        answer = possibility,
                    )

                    compiledAnswers.add(self.__whiteSpaceRegEx.sub(' ', compiledAnswer).strip())

        return list(answer for answer in compiledAnswers if utils.isValidStr(answer))

    # returns text answers with all arabic and roman numerals expanded into possible full-word forms
    async def expandNumerals(self, answer: str) -> list[str]:
        if answer is not None and not isinstance(answer, str):
            raise TypeError(f'answer argument is malformed: \"{answer}\"')

        split = self.__numeralRegEx.split(answer)

        for i in range(1, len(split), 2):
            match = self.__groupedNumeralRegEx.fullmatch(split[i])

            if not match:
                raise BadTriviaAnswerException(f'numbers cannot be expanded properly in trivia answer ({answer=})')

            if not match.group(1):
                # roman numerals
                split[i] = await self.__getRomanNumeralSubstitutes(match.group(2))
            else:
                # arabic numerals
                split[i] = await self.__getArabicNumeralSubstitutes(match.group(1))

        return list(set(''.join(item) for item in utils.permuteSubArrays(split)))

    async def __expandSpecialCases(
        self,
        answer: str,
    ) -> list[str]:
        specialCases = await self.__expandSpecialCasesDecade(answer)
        if specialCases is not None and len(specialCases) >= 1:
            return specialCases

        specialCases = await self.__expandSpecialCasesThingIsPhrase(answer)
        if specialCases is not None and len(specialCases) >= 1:
            return specialCases

        specialCases = await self.__expandSpecialCasesUsDollar(answer)
        if specialCases is not None and len(specialCases) >= 1:
            return specialCases

        specialCases = await self.__expandSpecialCasesWordSlashWord(answer)
        if specialCases is not None and len(specialCases) >= 1:
            return specialCases

        specialCases = await self.__expandSpecialCasesSimpleTimeDuration(answer)
        if specialCases is not None and len(specialCases) >= 1:
            return specialCases

        specialCases = await self.__expandSpecialCasesEquation(answer)
        if specialCases is not None and len(specialCases) >= 1:
            return specialCases

        specialCases = await self.__expandSpecialCasesWordDashWord(answer)
        if specialCases is not None and len(specialCases) >= 1:
            return specialCases

        # this special case is intentionally at the end of the list
        specialCases = await self.__expandSpecialCasesWordThenNumber(answer)
        if specialCases is not None and len(specialCases) >= 1:
            return specialCases

        return list()

    # Transforms "in the 1990's", "the 1990's", or just "1990's" to ['1990']
    async def __expandSpecialCasesDecade(self, answer: str) -> list[str] | None:
        match = self.__decadeRegEx.fullmatch(answer)
        if match is None:
            return None

        yearString = match.group(3)
        if not utils.isValidStr(yearString):
            return None

        return [ yearString ]

    # Expands 'X=5' to ['5', 'X = 5', 'X is 5', 'X equals 5']
    async def __expandSpecialCasesEquation(self, answer: str) -> list[str] | None:
        match = self.__equationRegEx.search(answer)
        if match is None:
            return None

        return [
            match.group(2),
            f'{match.group(1)} = {match.group(2)}',
            f'{match.group(1)} is {match.group(2)}',
            f'{match.group(1)} equals {match.group(2)}',
        ]

    # Expands 'he is a vampire' to ['he is a vampire', 'vampire']
    async def __expandSpecialCasesThingIsPhrase(self, answer: str) -> list[str] | None:
        match = self.__thingIsPhraseRegEx.fullmatch(answer)
        if match is None:
            return None

        thingIsPhrase = match.group()
        if not utils.isValidStr(thingIsPhrase):
            return None

        phraseAnswer = match.group(8)
        if not utils.isValidStr(phraseAnswer):
            return None

        return [ thingIsPhrase, phraseAnswer ]

    # Expands '$50,000.00 USD' to ['$50,000,000 (USD)', '50000000']
    async def __expandSpecialCasesUsDollar(self, answer: str) -> list[str] | None:
        match = self.__usDollarRegEx.fullmatch(answer)
        if match is None:
            return None

        usDollarAmount = match.group(1)
        if not utils.isValidStr(usDollarAmount):
            return None

        # strip any comma characters from the dollar amount
        usDollarAmount = usDollarAmount.replace(',', '')

        usDollarFloat: float | None = None

        try:
            usDollarFloat = float(usDollarAmount)
        except Exception as e:
            self.__timber.log('TriviaAnswerChecker', f'Unable to convert either usDollarAmount (\"{usDollarAmount}\") into float (raw match group: \"{match.group()}\")', e, traceback.format_exc())
            return None

        cleanedUsDollarAmount: str

        if usDollarFloat.is_integer():
            cleanedUsDollarAmount = str(int(usDollarFloat))
        else:
            cleanedUsDollarAmount = '{:.2f}'.format(usDollarFloat)

        return [
            f'{match.group(1)} usd',
            cleanedUsDollarAmount,
        ]

    async def __expandSpecialCasesWordDashWord(self, answer: str) -> list[str] | None:
        splits = self.__wordDashWordRegEx.split(answer)
        if splits is None or len(splits) <= 1:
            return None

        specialCases: set[str] = set()
        specialCases.add(''.join(splits))
        specialCases.add(' '.join(splits))

        return list(specialCases)

    # Expands 'groan/grown' into ['groan/grown', 'groan', 'grown'], or 'hello/world/123' into
    # ['hello/world/123', 'hello', 'world', '123']
    async def __expandSpecialCasesWordSlashWord(self, answer: str) -> list[str] | None:
        match = self.__wordSlashWordRegEx.fullmatch(answer)
        if match is None:
            return None

        allWords = match.group()
        firstWord = match.group(1)
        secondWord = match.group(2)

        if not utils.isValidStr(allWords) or not utils.isValidStr(firstWord) or not utils.isValidStr(secondWord):
            return None

        thirdWord: str | None = match.group(3)

        specialCases: list[str] = [
            match.group(),
            match.group(1),
            match.group(2),
        ]

        if utils.isValidStr(thirdWord):
            specialCases.append(thirdWord)

        return specialCases

    # Expands 'mambo #5' to ['mambo #5', 'mambo number 5']
    async def __expandSpecialCasesWordThenNumber(self, answer: str) -> list[str] | None:
        split = self.__hashRegEx.split(answer)
        for i in range(1, len(split), 2):
            split[i] = [ 'number ', '#' ]

        return [ ''.join(item) for item in utils.permuteSubArrays(split) ]

    # Expands '1 day old' into [ '1 day old', '1' ], '3 months old' into [ '3 months old', '3' ],
    # and '50 years old' into [ '50 years old', '50' ].
    async def __expandSpecialCasesSimpleTimeDuration(self, answer: str) -> list[str] | None:
        match = self.__simpleTimeDurationRegEx.fullmatch(answer)
        if match is None:
            return None

        fullAnswer: str | None = match.group()
        timeOnly: str | None = match.group(2)
        timeAndUnit: str | None = match.group(1)

        if not utils.isValidStr(fullAnswer) or not utils.isValidStr(timeOnly) or not utils.isValidStr(timeAndUnit):
            return None

        specialCases: list[str] = [ timeOnly, timeAndUnit ]

        if fullAnswer not in specialCases:
            specialCases.append(fullAnswer)

        return specialCases

    async def __fancyToLatin(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        text = unicodedata.normalize("NFKD", text)

        text = ''.join(
            self.__specialCharsRegEx.sub(
                lambda m: {k: v for k, v in m.groupdict().items() if v}.popitem()[0],
                char,
            ) for char in text
        )

        return self.__combiningDiacriticsRegEx.sub('', text).strip()

    async def __getArabicNumeralSubstitutes(self, arabicNumerals: str) -> list[str]:
        individualDigits = ' '.join([num2words(int(digit)) for digit in arabicNumerals])
        n = int(arabicNumerals)

        return [
                num2words(n, to = 'ordinal').replace('-', ' ').replace(',', ''),
                'the ' + num2words(n, to = 'ordinal').replace('-', ' ').replace(',', ''),
                num2words(n).replace('-', ' ').replace(',', ''),
                num2words(n, to = 'year').replace('-', ' ').replace(',', ''),
                individualDigits,
            ]

    async def __getRomanNumeralSubstitutes(self, romanNumerals: str) -> list[str]:
        n: int | None = None

        try:
            n = roman.fromRoman(romanNumerals.upper())
        except RomanError as e:
            self.__timber.log('TriviaAnswerCompiler', f'Failed to convert roman numerals \"{romanNumerals}\" into an integer: {e}', e)

        if not utils.isValidInt(n):
            return [ romanNumerals ]

        return [
            romanNumerals.lower(),
            num2words(n, to = 'ordinal').replace('-', ' ').replace(',', ''),
            'the ' + num2words(n, to = 'ordinal').replace('-', ' ').replace(',', ''),
            num2words(n).replace('-', ' ').replace(',', ''),
            num2words(n, to = 'year').replace('-', ' ').replace(',', ''),
        ]

    # Returns all possibilities with parenthesized phrases both included and excluded
    async def __getParentheticalPossibilities(
        self,
        allWords: frozenset[str] | None,
        answer: str,
    ) -> list[str]:
        if allWords is not None and len(allWords) >= 1:
            answer = await self.__patchWordsAppearingInQuestionAsOptional(
                allWords = allWords,
                answer = answer,
            )

        answer = await self.__patchAnswerFirstMiddleLastName(answer)
        answer = await self.__patchAnswerFirstNameAndMiddleInitialGroupedAndThenLastName(answer)
        answer = await self.__patchAnswerHonoraryPrefixes(answer)
        answer = await self.__patchAnswerJapaneseHonorarySuffixes(answer)
        answer = await self.__patchAnswerPossessivePronounPrefixes(answer)
        answer = await self.__patchAnswerThingsThatArePhrase(answer)
        answer = await self.__patchAnswerWordTheWord(answer)

        # Split the uncleaned answer with this regex to find all parentheticals
        splitPossibilities = self.__parenGroupRegEx.split(answer)

        # join the split possibilities back to strings and substitute multiple whitespaces back to a single space.
        return [ self.__whiteSpaceRegEx.sub(' ', ''.join(p).strip()) for p in await self.__getSubPossibilities(splitPossibilities) ]

    # Recursively resolves the possibilities for each word in the answer.
    async def __getSubPossibilities(
        self,
        splitAnswer: list[str]
    ) -> list[list[str] | str]:
        # early exit on trivial cases
        if len(splitAnswer) == 0:
            return list()
        if len(splitAnswer) == 1:
            return [ splitAnswer ]

        # get all "future" possible variants starting with the next word
        futurePossible = await self.__getSubPossibilities(splitAnswer[1:])

        # switch on open paren
        if splitAnswer[0].startswith('('):
            res: list[list[str] | str] = list()

            for possible in futurePossible:
                # add a version including this word but without the parentheses
                res.append([ splitAnswer[0][1:-1], *possible ])
                # also keep the version not including this word at all
                res.append(possible)

            # return all possibilities, with and without this word
            return res
        else:
            # return all future possibilities with this current word mapped onto it as well.
            return [ [ splitAnswer[0], *possible ] for possible in futurePossible ]

    # This method checks to see if an answer appears to be a first name, middle initial, and last
    # name (with optional suffix), such as "George H. Richard III". This method would then transform
    # that full name into "George (H.) Richard (III)".
    async def __patchAnswerFirstMiddleLastName(self, answer: str) -> str:
        firstMiddleLastNameMatch = self.__firstMiddleLastNameRegEx.fullmatch(answer)

        if firstMiddleLastNameMatch is None or not utils.isValidStr(firstMiddleLastNameMatch.group()):
            # return the unmodified answer
            return answer

        indexOfFirstSpace = answer.find(' ') + 1
        indexOfSecondSpace = answer.find(' ', indexOfFirstSpace)
        answer = answer[:indexOfFirstSpace] + '(' + firstMiddleLastNameMatch.group(1) + ')' + answer[indexOfSecondSpace:]

        if not utils.isValidStr(firstMiddleLastNameMatch.group(3)):
            # this name does not have a suffix like "Jr" or "Sr"
            return answer

        indexOfThirdSpace = answer.rfind(' ') + 1
        answer = answer[:indexOfThirdSpace] + '(' + answer[indexOfThirdSpace:len(answer)] + ')'

        return answer

    # This method checks to see if an answer matches this pattern: "(First name Middle initial) Last name", such as
    # "(George H.) Richard III". This method would then transform that full name into "(George) (H.) Richard (III)".
    async def __patchAnswerFirstNameAndMiddleInitialGroupedAndThenLastName(self, answer: str) -> str:
        firstNameAndMiddleInitialGroupedMatch = self.__firstNameAndMiddleInitialGroupedMatchRegEx.fullmatch(answer)

        if firstNameAndMiddleInitialGroupedMatch is None or not utils.isValidStr(firstNameAndMiddleInitialGroupedMatch.group()):
            # return the unmodified answer
            return answer

        indexOfFirstSpace = answer.find(' ')
        indexOfSecondSpace = answer.find(' ', indexOfFirstSpace + 1)
        answer = answer[:indexOfFirstSpace] + ') (' + firstNameAndMiddleInitialGroupedMatch.group(1) + ')' + answer[indexOfSecondSpace:]

        if not utils.isValidStr(firstNameAndMiddleInitialGroupedMatch.group(3)):
            # this name does not have a suffix like "Jr" or "Sr"
            return answer

        indexOfThirdSpace = answer.rfind(' ') + 1
        answer = answer[:indexOfThirdSpace] + '(' + answer[indexOfThirdSpace:len(answer)] + ')'

        return answer

    # This method checks to see if an answer starts with an honorary prefix, like "Mr.", "Mrs.",
    # etc. If it does, we patch this answer so that it will play nicely with our paren-checking logic.
    # For example, this method will transform the string "Mr. Potato Head" into "(Mr) Potato Head".
    async def __patchAnswerHonoraryPrefixes(self, answer: str) -> str:
        honoraryMatch = self.__honoraryPrefixRegEx.match(answer)

        if honoraryMatch is None or not utils.isValidStr(honoraryMatch.group()):
            # return the unmodified answer
            return answer

        oldHonoraryString = honoraryMatch.group()

        # make sure to remove the '.' character so that "Mr." becomes "(Mr)" rather than "(Mr.)"
        newHonoraryString = f'({oldHonoraryString.strip()}) '.replace('.', '')

        return answer.replace(oldHonoraryString, newHonoraryString)

    # This method checks to see if an answer ends with a Japanese honorary suffix, like "chan", "sama",
    # etc. If it does, we patch this answer so that it will play nicely with our paren-checking logic.
    # For example, this method will transform the string "Miyamoto-sama" into "Miyamoto (sama)".
    async def __patchAnswerJapaneseHonorarySuffixes(self, answer: str) -> str:
        honoraryMatch = self.__japaneseHonorarySuffixRegEx.search(answer)

        if honoraryMatch is None or not utils.isValidStr(honoraryMatch.group()):
            # return the unmodified answer
            return answer

        oldHonoraryString = honoraryMatch.group()
        newHonoraryString = f' ({oldHonoraryString[1:len(oldHonoraryString)].strip()})'
        return answer.replace(oldHonoraryString, newHonoraryString)

    # This method checks to see if an answer starts with a possessive pronoun prefix, such as "her"
    # or "his". If it does, we patch this answer so that it will play nicely with our paren-checking
    # logic. For example, this method will transform the string "his car" into "(his) car".
    async def __patchAnswerPossessivePronounPrefixes(self, answer: str) -> str:
        possessivePronounMatch = self.__possessivePronounPrefixRegEx.match(answer)

        if possessivePronounMatch is None or not utils.isValidStr(possessivePronounMatch.group()):
            # return the unmodified answer
            return answer

        oldPossessivePronounString = possessivePronounMatch.group()
        newPossessivePronounString = f'({oldPossessivePronounString.strip()}) '
        return answer.replace(oldPossessivePronounString, newPossessivePronounString)

    # This method checks to see if an answer starts with the exact phrase "things that are", and
    # if so, wraps that portion of the question in parenthesis. For example, this method will
    # transform the string "things that are pinched" into "(things that are) pinched".
    async def __patchAnswerThingsThatArePhrase(self, answer: str) -> str:
        match = self.__thingsThatArePhraseRegEx.fullmatch(answer)

        if match is None or not utils.isValidStr(match.group()) or not utils.isValidStr(match.group(1)) or not utils.isValidStr(match.group(2)):
            # return the unmodified answer
            return answer

        return f'({match.group(1)}) {match.group(2)}'

    # This method checks to see if an answer has a word pattern such as "Eric the Great", and if
    # so, wraps the middle word in parenthesis. For example, this method will transform the string
    # "Garfield the cat" into "Garfield (the) cat".
    async def __patchAnswerWordTheWord(self, answer: str) -> str:
        match = self.__wordTheWordRegEx.fullmatch(answer)

        if match is None or not utils.isValidStr(match.group()) or not utils.isValidStr(match.group(1)) or not utils.isValidStr(match.group(2)) or not utils.isValidStr(match.group(3)):
            # return the unmodified answer
            return answer

        return f'{match.group(1)} ({match.group(2)}) {match.group(3)}'

    async def __patchWordsAppearingInQuestionAsOptional(
        self,
        allWords: frozenset[str],
        answer: str
    ) -> str:
        matches = self.__findAllWordsWithOrWithoutParensRegEx.finditer(answer)

        if matches is None:
            return answer

        allOptionalWords: set[str] = set()
        allOptionalWords.update(allWords)
        allOptionalWords.update(self.__globalOptionalWords)

        patchedWords: list[str] = list()
        patchedAnswer = answer
        totalOffset = 0

        for match in matches:
            if self.__wordIsFullySurroundedByParensRegEx.fullmatch(match.string):
                continue

            word = match.group().casefold()

            if word not in allOptionalWords:
                continue

            patchedWords.append(word)

            openParenIndex = match.start() + totalOffset
            totalOffset += 1

            closeParenIndex = match.end() + totalOffset
            totalOffset += 1

            # place parens around the word in the answer
            patchedAnswer = patchedAnswer[:openParenIndex] + '(' + patchedAnswer[openParenIndex:]
            patchedAnswer = patchedAnswer[:closeParenIndex] + ')' + patchedAnswer[closeParenIndex:]

        modificationCount = len(patchedWords)

        if modificationCount == 0:
            self.__timber.log('TriviaAnswerCompiler', f'Abandoned patching words appearing in question as optional ({answer=}) ({patchedAnswer=}) ({patchedWords=}) ({modificationCount=}) ({allWords=}) ({allOptionalWords=})')
            return answer

        # The below logic checks to see if every single word in the answer now has parens. This
        # might not truly be 100% absolutely necessary, but I think it's better to not treat every
        # word answer as optional. This could have weird unforeseen ramifications down the road.
        allWordsInAnswer = self.__findAllWordsRegEx.findall(patchedAnswer)
        allWordsInAnswerWithParens = self.__findAllWordsWithParensRegEx.findall(patchedAnswer)

        allWordsInAnswerCount = 0
        if allWordsInAnswer is not None:
            allWordsInAnswerCount = len(allWordsInAnswer)

        allWordsInAnswerWithParensCount = 0
        if allWordsInAnswerWithParens is not None:
            allWordsInAnswerWithParensCount = len(allWordsInAnswerWithParens)

        if allWordsInAnswerCount != 0 and allWordsInAnswerWithParensCount != 0 and allWordsInAnswerCount == allWordsInAnswerWithParensCount:
            self.__timber.log('TriviaAnswerCompiler', f'Abandoned patching words appearing in question as optional ({answer=}) ({patchedAnswer=}) ({patchedWords=}) ({modificationCount=}) ({allWordsInAnswerWithParensCount=}) ({allWordsInAnswerWithParensCount=}) ({allWords=}) ({allOptionalWords=})')
            return answer
        else:
            self.__timber.log('TriviaAnswerCompiler', f'Patched words appearing in question as optional ({answer=}) ({patchedAnswer=}) ({patchedWords=}) ({modificationCount=}) ({allWordsInAnswerWithParensCount=}) ({allWordsInAnswerWithParensCount=}) ({allWords=}) ({allOptionalWords=})')
            return patchedAnswer
