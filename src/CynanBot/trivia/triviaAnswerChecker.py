import math
import re
import traceback
from typing import Any, Dict, Generator, List, Optional, Pattern, Set

import polyleven

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.compilers.triviaAnswerCompilerInterface import \
    TriviaAnswerCompilerInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from CynanBot.trivia.questions.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.trueFalseTriviaQuestion import \
    TrueFalseTriviaQuestion
from CynanBot.trivia.triviaAnswerCheckerInterface import \
    TriviaAnswerCheckerInterface
from CynanBot.trivia.triviaAnswerCheckResult import TriviaAnswerCheckResult
from CynanBot.trivia.triviaExceptions import (BadTriviaAnswerException,
                                              UnsupportedTriviaTypeException)
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class TriviaAnswerChecker(TriviaAnswerCheckerInterface):

    def __init__(
        self,
        timber: TimberInterface,
        triviaAnswerCompiler: TriviaAnswerCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
    ):
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaAnswerCompiler, TriviaAnswerCompilerInterface), f"malformed {triviaAnswerCompiler=}"
        assert isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface), f"malformed {triviaSettingsRepository=}"

        self.__timber: TimberInterface = timber
        self.__triviaAnswerCompiler: TriviaAnswerCompilerInterface = triviaAnswerCompiler
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository

        self.__whitespacePattern: Pattern = re.compile(r'\s\s+', re.IGNORECASE)

        self.__irregularNouns: Dict[str, Set[str]] = {
            'addendum': { 'addenda', 'addendums' },
            'alumna': { 'alumnae' },
            'bacterium': { 'bacteria' },
            'child': { 'children' },
            'deer': { 'deer', 'deers' },
            'die': { 'dice' },
            'fish': { 'fish', 'fishes' },
            'foot': { 'feet' },
            'goose': { 'geese' },
            'index': { 'indexes', 'indices' },
            'loaf': { 'loaves' },
            'man': { 'men' },
            'moose': { 'moose' },
            'mouse': { 'mice' },
            'person': { 'people' },
            'ox': { 'ox', 'oxen' },
            'scarf': { 'scarfs', 'scarves' },
            'self': { 'selves' },
            'tooth': { 'teeth' },
            'vertebra': { 'vertebrae', 'vertebras' },
            'wife': { 'wives' },
            'wolf': { 'wolves' },
            'woman': { 'women' }
        }

        self.__stopWords: Set[str] = {
            'i', 'me', 'my', 'myself', 'we', 'ourselves', 'you', 'he', 'him', 'his', 'she', 'they', 'them',  'what',
            'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
            'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
            'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
            'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
            'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'some', 'such', 'nor', 'not', 'only',
            'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'dont', 'should', 'now',
        }

    async def checkAnswer(
        self,
        answer: Optional[str],
        triviaQuestion: AbsTriviaQuestion,
        extras: Optional[Dict[str, Any]] = None
    ) -> TriviaAnswerCheckResult:
        assert isinstance(triviaQuestion, AbsTriviaQuestion), f"malformed {triviaQuestion=}"

        if not utils.isValidStr(answer):
            return TriviaAnswerCheckResult.INVALID_INPUT

        if triviaQuestion.getTriviaType() is TriviaQuestionType.MULTIPLE_CHOICE:
            return await self.__checkAnswerMultipleChoice(answer, triviaQuestion)
        elif triviaQuestion.getTriviaType() is TriviaQuestionType.QUESTION_ANSWER:
            return await self.__checkAnswerQuestionAnswer(answer, triviaQuestion, extras)
        elif triviaQuestion.getTriviaType() is TriviaQuestionType.TRUE_FALSE:
            return await self.__checkAnswerTrueFalse(answer, triviaQuestion)
        else:
            raise UnsupportedTriviaTypeException(f'Unsupported TriviaType: \"{triviaQuestion.getTriviaType()}\"')

    async def __checkAnswerMultipleChoice(
        self,
        answer: Optional[str],
        triviaQuestion: MultipleChoiceTriviaQuestion
    ) -> TriviaAnswerCheckResult:
        assert isinstance(triviaQuestion, MultipleChoiceTriviaQuestion), f"malformed {triviaQuestion=}"
        if triviaQuestion.getTriviaType() is not TriviaQuestionType.MULTIPLE_CHOICE:
            raise RuntimeError(f'TriviaType is not {TriviaQuestionType.MULTIPLE_CHOICE}: \"{triviaQuestion.getTriviaType()}\"')

        answerOrdinal: Optional[int] = None
        try:
            answerOrdinal = await self.__triviaAnswerCompiler.compileMultipleChoiceAnswer(answer)
        except BadTriviaAnswerException as e:
            self.__timber.log('TriviaAnswerChecker', f'Unable to convert multiple choice answer to ordinal: \"{answer}\": {e}', e, traceback.format_exc())
            return TriviaAnswerCheckResult.INVALID_INPUT

        if not utils.isValidInt(answerOrdinal):
            # this should be impossible, but let's just check anyway
            self.__timber.log('TriviaAnswerChecker', f'Unable to convert multiple choice answer to ordinal: (answer=\"{answer}\", answerOrdinal={answerOrdinal})')
            return TriviaAnswerCheckResult.INVALID_INPUT

        answerOrdinals = triviaQuestion.getAnswerOrdinals()

        if answerOrdinal < 0 or answerOrdinal >= len(answerOrdinals):
            # Checks for a scenario where the user guessed an answer outside the range
            # of actual responses. For example, the user might have guessed F, but the
            # question only had up to D.
            self.__timber.log('TriviaAnswerChecker', f'Multiple choice answer ordinal ({answerOrdinal}) is outside the range of actual answer ordinals: {answerOrdinals}')
            return TriviaAnswerCheckResult.INVALID_INPUT

        if answerOrdinal in triviaQuestion.getCorrectAnswerOrdinals():
            return TriviaAnswerCheckResult.CORRECT
        else:
            return TriviaAnswerCheckResult.INCORRECT

    async def __checkAnswerQuestionAnswer(
        self,
        answer: Optional[str],
        triviaQuestion: QuestionAnswerTriviaQuestion,
        extras: Optional[Dict[str, Any]] = None
    ) -> TriviaAnswerCheckResult:
        assert isinstance(triviaQuestion, QuestionAnswerTriviaQuestion), f"malformed {triviaQuestion=}"
        if triviaQuestion.getTriviaType() is not TriviaQuestionType.QUESTION_ANSWER:
            raise RuntimeError(f'TriviaType is not {TriviaQuestionType.QUESTION_ANSWER}: \"{triviaQuestion.getTriviaType()}\"')

        # prevent potential for insane answer lengths
        maxPhraseGuessLength = await self.__triviaSettingsRepository.getMaxPhraseGuessLength()
        if utils.isValidStr(answer) and len(answer) > maxPhraseGuessLength:
            answer = answer[0:maxPhraseGuessLength]

        cleanedAnswers = await self.__triviaAnswerCompiler.compileTextAnswersList([ answer ], False)
        if not all(utils.isValidStr(cleanedAnswer) for cleanedAnswer in cleanedAnswers):
            return TriviaAnswerCheckResult.INCORRECT

        cleanedCorrectAnswers = triviaQuestion.getCleanedCorrectAnswers()
        self.__timber.log('TriviaAnswerChecker', f'In depth question/answer debug information — (answer=\"{answer}\") (cleanedAnswers=\"{cleanedAnswers}\") (correctAnswers=\"{triviaQuestion.getCorrectAnswers()}\") (cleanedCorrectAnswers=\"{cleanedCorrectAnswers}\") (extras=\"{extras}\")')

        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            for cleanedAnswer in cleanedAnswers:
                expandedGuesses = await self.__triviaAnswerCompiler.expandNumerals(cleanedAnswer)

                for guess in expandedGuesses:
                    if guess == cleanedCorrectAnswer:
                        return TriviaAnswerCheckResult.CORRECT

                    guessWords = self.__whitespacePattern.sub(' ', guess).split(' ')
                    answerWords = self.__whitespacePattern.sub(' ', cleanedCorrectAnswer).split(' ')
                    minWords = min(len(guessWords), len(answerWords))

                    for gWords in self.__mergeWords(guessWords, minWords):
                        for aWords in self.__mergeWords(answerWords, minWords):
                            # This expansion of all() is required because you can't perform list comprehension on async
                            #   generators yet. :(
                            valid = True
                            for i in range(len(gWords)):
                                if not await self.__compareWords(gWords[i], aWords[i]):
                                    valid = False
                                    break
                            if valid:
                                return TriviaAnswerCheckResult.CORRECT

        return TriviaAnswerCheckResult.INCORRECT

    async def __checkAnswerTrueFalse(
        self,
        answer: Optional[str],
        triviaQuestion: TrueFalseTriviaQuestion
    ) -> TriviaAnswerCheckResult:
        assert isinstance(triviaQuestion, TrueFalseTriviaQuestion), f"malformed {triviaQuestion=}"
        if triviaQuestion.getTriviaType() is not TriviaQuestionType.TRUE_FALSE:
            raise RuntimeError(f'TriviaType is not {TriviaQuestionType.TRUE_FALSE}: \"{triviaQuestion.getTriviaType()}\"')

        answerBool: Optional[bool] = None
        try:
            answerBool = await self.__triviaAnswerCompiler.compileBoolAnswer(answer)
        except BadTriviaAnswerException as e:
            self.__timber.log('TriviaAnswerChecker', f'Unable to convert true false answer to bool: \"{answer}\": {e}', e, traceback.format_exc())
            return TriviaAnswerCheckResult.INVALID_INPUT

        if answerBool in triviaQuestion.getCorrectAnswerBools():
            return TriviaAnswerCheckResult.CORRECT
        else:
            return TriviaAnswerCheckResult.INCORRECT

    # generates all possible groupings of the given words such that the resulting word count is target_length
    # example: words = ["a", "b", "c", "d"], target_length = 2
    #          generates ["abc", "d"], ["ab", "cd"], ["a", "bcd"]
    def __mergeWords(self, wordList: List[str], target_length: int) -> Generator[List[str], None, None]:
        if target_length == 1:
            yield [''.join(wordList)]
        elif len(wordList) <= target_length:
            yield wordList
        else:
            for i in range(len(wordList) - target_length + 1):
                for w in self.__mergeWords(wordList[i+1:], target_length - 1):
                    yield [''.join(wordList[0:i+1])] + w

    # compare two individual words, returns true if any valid variants match between the two words
    async def __compareWords(self, word1: str, word2: str) -> bool:
        thresholdGrowthRate = await self.__triviaSettingsRepository.getLevenshteinThresholdGrowthRate()
        for w1 in self.__genVariantPossibilities(word1):
            for w2 in self.__genVariantPossibilities(word2):
                # calculate threshold based on shorter word length
                threshold = math.floor(min(len(w1), len(w2)) / thresholdGrowthRate)
                dist = polyleven.levenshtein(w1, w2, threshold + 1)
                if dist <= threshold:
                    return True
        return False

    def __genVariantPossibilities(self, word: str) -> Generator[str, None, None]:
        yield word

        # don't preprocess stopwords
        if word in self.__stopWords:
            return

        # pluralizations
        if any(word.endswith(s) for s in ('ss', 'sh', 'ch', 'x', 'z', 's', 'o')):
            yield word + 'es'
        if word[-1] in 'sz':
            yield word + word[-1] + 'es'
        elif word.endswith('f'):
            yield word[:-1] + 'ves'
        elif word.endswith('fe'):
            yield word[:-2] + 'ves'
        elif word[-1] == 'y' and len(word) > 1 and word[-2] not in 'aeiou':
            yield word[:-1] + 'ies'
        elif word.endswith('us'):
            yield word[:-2] + 'i'
        elif word.endswith('is'):
            yield word[:-2] + 'es'
        elif word.endswith('on') or word.endswith('um'):
            yield word[:-2] + 'a'
        if word[-1] != 's':
            yield word + 's'

        if word in self.__irregularNouns:
            for irregularNoun in self.__irregularNouns[word]:
                yield irregularNoun

        # titles
        if word == 'atty':
            yield 'attorney'
        if word == 'do':
            yield 'doctor of osteopathy'
        if word == 'dr':
            yield 'doctor'
        if word == 'esq':
            yield 'esquire'
        if word == 'jr':
            yield 'junior'
        if word == 'md':
            yield 'doctor of medicine'
        if word == 'mr':
            yield 'mister'
        if word == 'mrs':
            yield 'missus'
        if word == 'ms':
            yield 'miss'
        if word == 'np':
            yield 'nurse practitioner'
        if word == 'pa':
            yield 'physician assistant'
        if word == 'phd':
            yield 'philosophiae doctor'
        if word == 'sr':
            yield 'senior'
        if word == 'st':
            yield 'saint'

        # common names
        if word == 'al':
            yield 'alan'
        if word in ('alberta', 'bert', 'bertie'):
            yield 'albert'
        if word in ('aron', 'aaron', 'aaryn', 'eryn'):
            yield 'erin'
        if word in ('billie', 'billy'):
            yield 'bill'
        if word == 'bob':
            yield 'bobby'
        if word in ('cathleen', 'katherine', 'kathleen', 'kathy'):
            yield 'catherine'
        if word in ('charlie', 'charly', 'chuck', 'chucky'):
            yield 'charles'
        if word in ('chris', 'christ', 'cris', 'kris'):
            yield 'christopher'
        if word == 'delanor':
            yield 'delano'
        if word in ('dick', 'rick'):
            yield 'richard'
        if word in ('ed', 'eddie', 'eddy'):
            yield 'edward'
        if word == 'fdr':
            yield 'franklin roosevelt'
            yield 'franklin delano roosevelt'
        if word == 'goerge':
            yield 'george'
        if word == 'gw':
            yield 'george washington'
        if word == 'jakob':
            yield 'jacob'
        if word in ('jo', 'joey', 'joseph'):
            yield 'joe'
        if word in ('jon', 'jhon'):
            yield 'john'
        if word == 'joshua':
            yield 'josh'
        if word == 'marty':
            yield 'martin'
        if word in ('micheal', 'mike'):
            yield 'michael'
        if word in ('rob', 'robbie'):
            yield 'robert'
        if word in ('ron', 'ronnie'):
            yield 'ronald'
        if word in ('sadie', 'sally', 'sara'):
            yield 'sarah'
        if word in ('tom', 'tony'):
            yield 'thomas'
        if word == 'toni':
            yield 'tony'
        if word in ('william', 'willie', 'willy'):
            yield 'will'

        # geographical features/streets
        if word in ('aly', 'ally'):
            yield 'alley'
        if word in ('anx', 'annx'):
            yield 'anex'
        if word == 'arc':
            yield 'arcade'
        if word in ('av', 'ave', 'avn'):
            yield 'avenue'
        if word == 'bch':
            yield 'beach'
        if word in ('blvd', 'boul'):
            yield 'boulevard'
        if word in ('br', 'brnch'):
            yield 'branch'
        if word == 'brg':
            yield 'bridge'
        if word == 'brk':
            yield 'brook'
        if word == 'byu':
            yield 'bayou'
        if word in ('canyn', 'cnyn'):
            yield 'canyon'
        if word == 'cswy':
            yield 'causeway'
        if word in ('cen', 'cntr', 'ctr'):
            yield 'center'
        if word in ('cir', 'cir', 'circl', 'crcl'):
            yield 'circle'
        if word == 'clb':
            yield 'club'
        if word == 'cty':
            yield 'city'
        if word in ('ct', 'crt'):
            yield 'court'
        if word in ('cts', 'crts'):
            yield 'courts'
        if word == 'cv':
            yield 'cove'
        if word == 'crk':
            yield 'creek'
        if word == 'dr':
            yield 'drive'
        if word == 'est':
            yield 'estate'
        if word == 'fld':
            yield 'field'
        if word == 'frd':
            yield 'ford'
        if word in ('frt', 'ft'):
            yield 'fort'
        if word == 'gdn':
            yield 'garden'
        if word == 'glf':
            yield 'gulf'
        if word == 'grn':
            yield 'green'
        if word == 'grv':
            yield 'grove'
        if word == 'hvn':
            yield 'haven'
        if word in ('ht', 'hgt', 'hts'):
            yield 'height'
        if word in ('hiwy', 'hiway', 'hway', 'hwy'):
            yield 'highway'
        if word in ('is', 'isl', 'isle'):
            yield 'island'
        if word in ('ldg', 'ldge'):
            yield 'lodge'
        if word == 'lk':
            yield 'lake'
        if word == 'ln':
            yield 'lane'
        if word == 'mdw':
            yield 'meadow'
        if word == 'mnr':
            yield 'manor'
        if word == 'mt':
            yield 'mount'
            yield 'mountain'
        if word == 'mtwy':
            yield 'motorway'
        if word == 'orch':
            yield 'orchard'
        if word in ('pkwy', 'pkway', 'pky'):
            yield 'parkway'
        if word == 'pl':
            yield 'place'
        if word == 'px':
            yield 'post exchange'
        if word == 'rd':
            yield 'road'
        if word in ('riv', 'rvr', 'rivr'):
            yield 'river'
        if word == 'rd':
            yield 'road'
        if word == 'sq':
            yield 'square'
        if word in ('st', 'str', 'strt'):
            yield 'street'
        if word == 'stn':
            yield 'station'
        if word == 'vlg':
            yield 'village'
        if word == 'vw':
            yield 'view'
        if word in ('crssng', 'xing'):
            yield 'crossing'

        # countries, languages, and specific places
        if word == 'asl':
            yield 'american sign language'
        if word == 'antigua':
            yield 'antigua and barbuda'
        if word == 'arctic':
            yield 'arctic ocean'
        if word == 'atlantic':
            yield 'atlantic ocean'
        if word == 'bosnia':
            yield 'bosnia and herzegovina'
        if word == 'burma':
            yield 'myanmar'
        if word == 'cape verde':
            yield 'cabo verde'
        if word == 'car':
            yield 'central african republic'
        if word in ('czechia republic', 'czech republic'):
            yield 'czechia'
        if word == 'dr':
            yield 'dominican republic'
        if word == 'drc':
            yield 'democratic republic of congo'
            yield 'democratic republic of the congo'
        if word in ('en', 'eng'):
            yield 'english'
        if word == 'eu':
            yield 'europe'
            yield 'european union'
        if word == 'gb':
            yield 'great britain'
        if word == 'holland':
            yield 'netherlands'
        if word == 'indian':
            yield 'indian ocean'
        if word == 'ivory coast':
            yield 'cote d ivoire'
            yield 'cote divoire'
        if word in ('ja', 'jp', 'jpn'):
            yield 'japan'
        if word == 'kr':
            yield 'korea'
        if word in ('macedonia', 'n macedonia'):
            yield 'macedonia'
            yield 'north macedonia'
        if word == 'mx':
            yield 'mexico'
        if word == 'myanmar':
            yield 'burma'
        if word == 'new guinea':
            yield 'papua new guinea'
        if word in ('ny', 'new york city', 'nyc'):
            yield 'new york'
        if word == 'pacific':
            yield 'pacific ocean'
        if word in ('palestine state', 'palestinian', 'palestinian state', 'west bank'):
            yield 'palestine'
        if word == 'pr':
            yield 'puerto rico'
        if word in ('rep', 'repr'):
            yield 'representative'
        if word == 'sen':
            yield 'senator'
        if word == 'swaziland':
            yield 'eswatini'
        if word in ('timor', 'east timor'):
            yield 'timor leste'
        if word == 'turkiye':
            yield 'turkey'
        if word == 'uae':
            yield 'united arab emirates'
        if word == 'uk':
            yield 'united kingdom'
        if word == 'un':
            yield 'united nations'
        if word in ('us', 'usa'):
            yield 'united states'
            yield 'united states of america'

        # government organizations
        if word == 'cia':
            yield 'central intelligence agency'
        if word in ('dem', 'democratic', 'democratic party', 'dnc', 'democratic national convention', 'liberal'):
            yield 'democrat'
        if word == 'fbi':
            yield 'federal bureau of investigation'
        if word in ('fedex', 'fed ex'):
            yield 'federal express'
        if word in ('conservative', 'gop', 'grand old party', 'republican party', 'rnc', 'republican national convention'):
            yield 'republican'
        if word == 'irs':
            yield 'internal revenue service'
        if word == 'mi6':
            yield 'secret intelligence service'
        if word == 'nsa':
            yield 'natural security agency'
        if word in ('post', 'usps'):
            yield 'mail'
            yield 'post'
            yield 'post office'
            yield 'postal service'
            yield 'united states postal service'
        if word == 'sec':
            yield 'securities and exchange commission'
        if word == 'tsa':
            yield 'transportation security administration'
        if word == 'ups':
            yield 'united parcel service'

        # currencies
        if word == 'eur':
            yield 'euro'
        if word == 'jpy':
            yield 'japanese yen'
            yield 'yen'
        if word == 'sek':
            yield 'krona'
            yield 'swedish krona'
        if word == 'usd':
            yield 'dollar'
            yield 'united states dollar'

        # sports
        if word == 'asl':
            yield 'american soccer league'
        if word == 'cfl':
            yield 'canadian football league'
        if word == 'fifa':
            yield 'federation internationale de football association'
        if word == 'mlb':
            yield 'major league baseball'
        if word == 'mls':
            yield 'major league soccer'
        if word == 'nba':
            yield 'national basketball association'
        if word == 'nfl':
            yield 'national football league'
        if word in ('nhl', 'wnhl'):
            yield 'national hockey league'

        # directions
        if word in ('n', 'north', 'northerly', 'northern'):
            yield 'north'
        if word in ('s', 'south', 'southerly', 'southern'):
            yield 'south'
        if word in ('e', 'east', 'easterly', 'eastern'):
            yield 'east'
        if word in ('w', 'west', 'westerly', 'western'):
            yield 'west'
        if word in ('nw', 'northwest', 'northwestern'):
            yield 'northwest'
        if word in ('ne', 'northeast', 'northeastern'):
            yield 'northeast'
        if word in ('sw', 'southwest', 'southwestern'):
            yield 'southwest'
        if word in ('se', 'southeast', 'southeastern'):
            yield 'southeast'
        if word in ('l', 'left'):
            yield 'left'
        if word in ('r', 'right'):
            yield 'right'

        # corporation things
        if word == 'asst':
            yield 'assistant'
        if word == 'corp':
            yield 'corporation'
        if word == 'inc':
            yield 'incorporated'
        if word == 'llc':
            yield 'limited liability company'
        if word == 'ltd':
            yield 'limited'
        if word == 'vp':
            yield 'vice president'

        # weird latin things
        if word == 'cv':
            yield 'curriculum vitae'
        if word == 'et al':
            yield 'et alia'
        if word == 'etc':
            yield 'et cetera'
        if word == 'eg':
            yield 'example gratia'
            yield 'exempli gratia'
        if word == 'ie':
            yield 'id est'
            yield 'in other words'
        if word == 'ps':
            yield 'postscript'
            yield 'postscriptum'
        if word == 'sic':
            yield 'sic erat scriptum'

        # technology
        if word == 'cmyk':
            yield 'cyan magenta yellow black'
        if word == 'cpu':
            yield 'central processing unit'
            yield 'processor'
        if word == 'ddr':
            yield 'data delivery rate'
        if word == 'dns':
            yield 'domain name system'
        if word in ('dp', 'dip'):
            yield 'density independent pixel'
        if word == 'dpi':
            yield 'dots per inch'
        if word == 'ff':
            yield 'firefox'
        if word == 'fps':
            yield 'frames per second'
        if word == 'ftp':
            yield 'file transfer protocol'
        if word == 'goog':
            yield 'google'
        if word == 'gps':
            yield 'global positioning system'
        if word == 'gpu':
            yield 'graphics processing unit'
        if word in ('hd', 'hdd'):
            yield 'hard disk drive'
            yield 'hard drive'
        if word == 'http':
            yield 'hypertext transfer protocol'
        if word == 'https':
            yield 'hypertext transfer protocol secure'
        if word == 'ie':
            yield 'internet explorer'
        if word == 'int':
            yield 'integer'
        if word == 'ip':
            yield 'internet protocol'
        if word in ('ms', 'msft'):
            yield 'microsoft'
        if word == 'ppi':
            yield 'pixels per inch'
        if word == 'pt':
            yield 'point'
        if word in ('px', 'pxl'):
            yield 'pixel'
            yield 'pixels'
        if word == 'ram':
            yield 'random access memory'
        if word == 'rgb':
            yield 'red green blue'
        if word == 'sftp':
            yield 'secure file transfer protocol'
        if word == 'sp':
            yield 'scaleable pixels'
            yield 'scale independent pixels'
        if word == 'ssd':
            yield 'solid state drive'
        if word == 'uri':
            yield 'uniform resource identifier'
        if word == 'url':
            yield 'uniform resource locator'
        if word == 'www':
            yield 'world wide web'

        # measurements (imperial and metric)
        if word == 'atm':
            yield 'atmospheres'
        if word == 'bin':
            yield 'binary'
        if word == 'bps':
            yield 'bits per second'
        if word == 'c':
            yield 'celsius'
        if word == 'cg':
            yield 'centigram'
        if word == 'cl':
            yield 'centiliter'
        if word == 'cm':
            yield 'centimeter'
        if word == 'dl':
            yield 'deciliter'
        if word == 'dm':
            yield 'decimeter'
        if word == 'eb':
            yield 'exabyte'
        if word == 'f':
            yield 'fahrenheit'
        if word == 'fps':
            yield 'feet per second'
        if word == 'ft':
            yield 'feet'
            yield 'foot'
        if word == 'g':
            yield 'gallon'
            yield 'gram'
        if word == 'gb':
            yield 'gigabyte'
        if word == 'gph':
            yield 'gallons per hour'
        if word == 'gw':
            yield 'gigawatt'
        if word == 'hg':
            yield 'hectogram'
        if word == 'hm':
            yield 'hectometer'
        if word == 'hr':
            yield 'hour'
        if word == 'in':
            yield 'inch'
            yield 'inches'
        if word == 'k':
            yield 'kelvin'
        if word == 'kb':
            yield 'kilobyte'
        if word == 'kg':
            yield 'kilogram'
        if word == 'kl':
            yield 'kiloliter'
            yield 'kiloliters'
        if word == 'km':
            yield 'kilometer'
            yield 'kilometers'
        if word == 'kph':
            yield 'kilometers per hour'
        if word == 'kw':
            yield 'kilowatt'
        if word == 'kwh':
            yield 'kilowatt hours'
        if word == 'l':
            yield 'liter'
            yield 'liters'
        if word in ('lb', 'lbs'):
            yield 'pound'
            yield 'pounds'
        if word == 'm':
            yield 'meter'
            yield 'minute'
        if word == 'mb':
            yield 'megabyte'
            yield 'megabytes'
        if word == 'mg':
            yield 'milligram'
            yield 'milligrams'
        if word == 'mi':
            yield 'mile'
            yield 'miles'
        if word == 'min':
            yield 'minute'
            yield 'minutes'
        if word == 'ml':
            yield 'milliliter'
        if word == 'mm':
            yield 'millimeter'
        if word == 'mpg':
            yield 'miles per gallon'
        if word == 'mph':
            yield 'miles per hour'
        if word == 'mps':
            yield 'meters per second'
        if word == 'nmi':
            yield 'nautical miles'
        if word == 'oz':
            yield 'ounce'
            yield 'ounces'
        if word == 'pb':
            yield 'petabyte'
            yield 'petabytes'
        if word == 's':
            yield 'second'
        if word == 'tb':
            yield 'terabyte'
            yield 'terabytes'
        if word in ('tbs', 'tbsp'):
            yield 'tablespoon'
            yield 'tablespoons'
        if word == 'tsp':
            yield 'teaspoon'
            yield 'teaspoons'
        if word == 'w':
            yield 'watt'
            yield 'wattage'
        if word in ('yd', 'yds', 'yrd', 'yrds'):
            yield 'yard'

        # british english vs american english spellings
        if word == 'aluminium':
            yield 'aluminum'
        if word == 'analogue':
            yield 'analog'
        if word == 'analyse':
            yield 'analyze'
        if word == 'armour':
            yield 'armor'
        if word == 'catalogue':
            yield 'catalog'
        if word == 'colour':
            yield 'color'
        if word == 'defence':
            yield 'defense'
        if word == 'dialogue':
            yield 'dialog'
        if word == 'flavour':
            yield 'flavor'
        if word == 'labour':
            yield 'labor'
        if word == 'licence':
            yield 'license'
        if word == 'neighbour':
            yield 'neighbor'
        if word == 'offence':
            yield 'offense'
        if word == 'travelled':
            yield 'traveled'
        if word == 'traveller':
            yield 'traveler'
        if word == 'travelling':
            yield 'traveling'

        # other
        if word == 'ac':
            yield 'air conditioner'
            yield 'air conditioning'
            yield 'alternating current'
        if word == 'alright':
            yield 'all right'
        if word == 'bday':
            yield 'birthday'
        if word == 'bunny':
            yield 'rabbit'
        if word == 'dad':
            yield 'father'
        if word == 'cnn':
            yield 'cable news network'
        if word == 'est':
            yield 'establish'
            yield 'established'
            yield 'estimate'
        if word == 'capital':
            yield 'capitol'
        if word == 'dc':
            yield 'direct current'
        if word in ('dpt', 'dept'):
            yield 'department'
        if word == 'espn':
            yield 'entertainment and sports programming network'
        if word == 'est':
            yield 'estimate'
            yield 'estimated'
            yield 'established'
        if word == 'eta':
            yield 'estimated time of arrival'
        if word == 'fridge':
            yield 'refrigerator'
        if word == 'ft':
            yield 'feature'
            yield 'featuring'
        if word == 'fyi':
            yield 'for your information'
        if word == 'grey':
            yield 'gray'
        if word == 'mom':
            yield 'mother'
        if word == 'no':
            yield 'number'
        if word == 'ocd':
            yield 'obsessive compulsive disorder'
        if word == 'parcel':
            yield 'mail'
            yield 'package'
        if word in ('phone', 'tel'):
            yield 'telephone'
        if word == 'precedent':
            yield 'president'
        if word in ('temp', 'tmp'):
            yield 'temporary'
        if word == 'tv':
            yield 'television'
        if word == 'vs':
            yield 'versus'
        if word == 'wr':
            yield 'world record'
        if word == 'ww':
            yield 'world war'
        if word in ('wwi', 'ww1', 'first world war'):
            yield 'world war 1'
        if word in ('wwii', 'ww2', 'second world war'):
            yield 'world war 2'
        if word == 'xmas':
            yield 'christmas'
