from enum import Enum, auto

from frozenlist import FrozenList

from ..misc import utils as utils


class LanguageEntry(Enum):

    AFRIKAANS = auto()
    ARABIC = auto()
    BASQUE = auto()
    BENGALI = auto()
    BULGARIAN = auto()
    CATALAN = auto()
    CHINESE = auto()
    CZECH = auto()
    DANISH = auto()
    DUTCH = auto()
    ENGLISH = auto()
    ENGLISH_FOR_PORTUGUESE_SPEAKERS = auto()
    ENGLISH_FOR_SPANISH_SPEAKERS = auto()
    FILIPINO = auto()
    FINNISH = auto()
    FRENCH = auto()
    GALICIAN = auto()
    GERMAN = auto()
    GREEK = auto()
    GUJARATI = auto()
    HEBREW = auto()
    HINDI = auto()
    HUNGARIAN = auto()
    ICELANDIC = auto()
    INDONESIAN = auto()
    ITALIAN = auto()
    JAPANESE = auto()
    KANNADA = auto()
    KOREAN = auto()
    LATIN = auto()
    LATVIAN = auto()
    LITHUANIAN = auto()
    MALAY = auto()
    MALAYALAM = auto()
    MARATHI = auto()
    NORWEGIAN = auto()
    POLISH = auto()
    PORTUGUESE = auto()
    PUNJABI = auto()
    ROMANIAN = auto()
    RUSSIAN = auto()
    SERBIAN = auto()
    SLOVAK = auto()
    SPANISH = auto()
    SWEDISH = auto()
    TAMIL = auto()
    TELUGU = auto()
    THAI = auto()
    TURKISH = auto()
    UKRANIAN = auto()
    URDU = auto()
    VIETNAMESE = auto()

    @property
    def commandNames(self) -> FrozenList[str]:
        commandNames: list[str]

        match self:
            case LanguageEntry.AFRIKAANS:
                commandNames = [ 'af', 'za', 'afrikaans' ]

            case LanguageEntry.ARABIC:
                commandNames = [ 'ar', 'arabic', 'عَرَبِيّ', 'اَلْعَرَبِيَّةُ' ]

            case LanguageEntry.BASQUE:
                commandNames = [ 'ba', 'basque', 'euskara' ]

            case LanguageEntry.BENGALI:
                commandNames = [ 'bn', 'bengali', 'bangla', 'বাংলা' ]

            case LanguageEntry.BULGARIAN:
                commandNames = [ 'bg', 'bulgarian', 'bŭlgarski', 'български' ]

            case LanguageEntry.CATALAN:
                commandNames = [ 'ca', 'catalan', 'català' ]

            case LanguageEntry.CHINESE:
                commandNames = [ 'zh', 'chinese', 'china', '中文' ]

            case LanguageEntry.CZECH:
                commandNames = [ 'cs', 'czech', 'čeština' ]

            case LanguageEntry.DANISH:
                commandNames = [ 'da', 'danish', 'dansk', 'denmark' ]

            case LanguageEntry.DUTCH:
                commandNames = [ 'nl', 'dutch', 'nederlands', 'netherlands', 'vlaams' ]

            case LanguageEntry.ENGLISH:
                commandNames = [ 'en', 'eng', 'english', '英語' ]

            case LanguageEntry.ENGLISH_FOR_PORTUGUESE_SPEAKERS:
                commandNames = [ 'en-pt' ]

            case LanguageEntry.ENGLISH_FOR_SPANISH_SPEAKERS:
                commandNames = [ 'en-es' ]

            case LanguageEntry.FILIPINO:
                commandNames = [ 'fil', 'filipino', 'tagalog' ]

            case LanguageEntry.FINNISH:
                commandNames = [ 'fi', 'finnish', 'suomi', 'suomeksi' ]

            case LanguageEntry.FRENCH:
                commandNames = [ 'fr', 'français', 'france', 'french' ]

            case LanguageEntry.GALICIAN:
                commandNames = [ 'gl', 'galician', 'galegos', 'gallegos' ]

            case LanguageEntry.GERMAN:
                commandNames = [ 'de', 'deutsche', 'german', 'germany' ]

            case LanguageEntry.GREEK:
                commandNames = [ 'el', 'greek' ]

            case LanguageEntry.GUJARATI:
                commandNames = [ 'gu', 'gujarati', 'ગુજરાતી' ]

            case LanguageEntry.HEBREW:
                commandNames = [ 'he', 'hebrew', 'ࠏࠨࠁࠬࠓࠪࠉࠕ', 'עִבְרִית' ]

            case LanguageEntry.HINDI:
                commandNames = [ 'hi', 'hin', 'hindi' ]

            case LanguageEntry.HUNGARIAN:
                commandNames = [ 'hu', 'hungarian', 'magyar', 'hungary' ]

            case LanguageEntry.ICELANDIC:
                commandNames = [ 'is', 'icelandic', 'íslenska', 'iceland' ]

            case LanguageEntry.INDONESIAN:
                commandNames = [ 'id', 'indonesian', 'indonesia' ]

            case LanguageEntry.ITALIAN:
                commandNames = [ 'it', 'italian', 'italiano', 'italy' ]

            case LanguageEntry.JAPANESE:
                commandNames = [ 'ja', 'japan', 'japanese', 'jp', '日本', '日本語', 'にほんご' ]

            case LanguageEntry.KANNADA:
                commandNames = [ 'kn', 'kannada', 'ಕನ್ನಡ' ]

            case LanguageEntry.KOREAN:
                commandNames = [ 'ko', 'korea', 'korean', '한국어' ]

            case LanguageEntry.LATIN:
                commandNames = [ 'la', 'latin' ]

            case LanguageEntry.LATVIAN:
                commandNames = [ 'lv', 'latvian', 'lettish', 'latvia' ]

            case LanguageEntry.LITHUANIAN:
                commandNames = [ 'lt', 'lithuanian', 'lietuvių', 'lithuania' ]

            case LanguageEntry.MALAY:
                commandNames = [ 'ms', 'malay' ]

            case LanguageEntry.MALAYALAM:
                commandNames = [ 'ml', 'malayalam', 'മലയാളം' ]

            case LanguageEntry.MARATHI:
                commandNames = [ 'mr', 'marathi', 'मराठी' ]

            case LanguageEntry.NORWEGIAN:
                commandNames = [ 'no', 'norsk', 'norway', 'norwegian' ]

            case LanguageEntry.POLISH:
                commandNames = [ 'po', 'poland', 'polish' ]

            case LanguageEntry.PORTUGUESE:
                commandNames = [ 'pt', 'portuguese', 'português' ]

            case LanguageEntry.PUNJABI:
                commandNames = [ 'pa', 'punjabi', 'ਪੰਜਾਬੀ', 'پنجابی' ]

            case LanguageEntry.ROMANIAN:
                commandNames = [ 'ro', 'romanian', 'română' ]

            case LanguageEntry.RUSSIAN:
                commandNames = [ 'ru', 'russia', 'russian', 'русский' ]

            case LanguageEntry.SERBIAN:
                commandNames = [ 'sr', 'serbian', 'serbia', 'srpski' ]

            case LanguageEntry.SLOVAK:
                commandNames = [ 'sk', 'slovak', 'slovenčina', 'slovakia' ]

            case LanguageEntry.SPANISH:
                commandNames = [ 'es', 'español', 'sp', 'spanish' ]

            case LanguageEntry.SWEDISH:
                commandNames = [ 'se', 'sv', 'svenska', 'sw', 'sweden', 'swedish' ]

            case LanguageEntry.TAMIL:
                commandNames = [ 'ta', 'tamil', 'தமிழ்' ]

            case LanguageEntry.TELUGU:
                commandNames = [ 'te', 'telugu', 'తెలుగు' ]

            case LanguageEntry.THAI:
                commandNames = [ 'th', 'thai', 'thailand', 'ภาษาไทย' ]

            case LanguageEntry.TURKISH:
                commandNames = [ 'tr', 'turkish', 'türkçe' ]

            case LanguageEntry.UKRANIAN:
                commandNames = [ 'uk', 'ua', 'ukrainian', 'ukraine', 'українська' ]

            case LanguageEntry.URDU:
                commandNames = [ 'ur', 'urd', 'urdu', 'اُردُو' ]

            case LanguageEntry.VIETNAMESE:
                commandNames = [ 'vi', 'vn', 'vietnamese', 'vietnam', 'viet']

            case _:
                raise RuntimeError(f'Unknown LanguageEntry value: \"{self}\"')

        frozenCommandNames: FrozenList[str] = FrozenList(commandNames)
        frozenCommandNames.freeze()

        return frozenCommandNames

    @property
    def flag(self) -> str | None:
        match self:
            case LanguageEntry.AFRIKAANS: return '🇿🇦'
            case LanguageEntry.ARABIC: return None
            case LanguageEntry.BASQUE: return None
            case LanguageEntry.BENGALI: return None
            case LanguageEntry.BULGARIAN: return '🇧🇬'
            case LanguageEntry.CATALAN: return None
            case LanguageEntry.CHINESE: return '🇨🇳'
            case LanguageEntry.CZECH: return '🇨🇿'
            case LanguageEntry.DANISH: return '🇩🇰'
            case LanguageEntry.DUTCH: return '🇳🇱'
            case LanguageEntry.ENGLISH: return '🇬🇧'
            case LanguageEntry.ENGLISH_FOR_PORTUGUESE_SPEAKERS: return None
            case LanguageEntry.ENGLISH_FOR_SPANISH_SPEAKERS: return None
            case LanguageEntry.FILIPINO: return '🇵🇭'
            case LanguageEntry.FINNISH: return '🇫🇮'
            case LanguageEntry.FRENCH: return '🇫🇷'
            case LanguageEntry.GALICIAN: return None
            case LanguageEntry.GERMAN: return '🇩🇪'
            case LanguageEntry.GREEK: return '🇬🇷'
            case LanguageEntry.GUJARATI: return '🇮🇳'
            case LanguageEntry.HEBREW: return '🇮🇱'
            case LanguageEntry.HINDI: return '🇮🇳'
            case LanguageEntry.HUNGARIAN: return '🇭🇺'
            case LanguageEntry.ICELANDIC: return '🇮🇸'
            case LanguageEntry.INDONESIAN: return '🇮🇩'
            case LanguageEntry.ITALIAN: return '🇮🇹'
            case LanguageEntry.JAPANESE: return '🇯🇵'
            case LanguageEntry.KANNADA: return '🇮🇳'
            case LanguageEntry.KOREAN: return '🇰🇷'
            case LanguageEntry.LATIN: return None
            case LanguageEntry.LATVIAN: return '🇱🇻'
            case LanguageEntry.LITHUANIAN: return '🇱🇹'
            case LanguageEntry.MALAY: return '🇲🇾'
            case LanguageEntry.MALAYALAM: return '🇮🇳'
            case LanguageEntry.MARATHI: return '🇮🇳'
            case LanguageEntry.NORWEGIAN: return '🇳🇴'
            case LanguageEntry.POLISH: return '🇵🇱'
            case LanguageEntry.PORTUGUESE: return None
            case LanguageEntry.PUNJABI: return None
            case LanguageEntry.ROMANIAN: return '🇷🇴'
            case LanguageEntry.RUSSIAN: return '🇷🇺'
            case LanguageEntry.SERBIAN: return '🇷🇸'
            case LanguageEntry.SLOVAK: return '🇸🇰'
            case LanguageEntry.SPANISH: return None
            case LanguageEntry.SWEDISH: return '🇸🇪'
            case LanguageEntry.TAMIL: return None
            case LanguageEntry.TELUGU: return '🇮🇳'
            case LanguageEntry.THAI: return '🇹🇭'
            case LanguageEntry.TURKISH: return '🇹🇷'
            case LanguageEntry.UKRANIAN: return '🇺🇦'
            case LanguageEntry.URDU: return '🇵🇰'
            case LanguageEntry.VIETNAMESE: return '🇻🇳'
            case _: raise RuntimeError(f'Unknown LanguageEntry value: \"{self}\"')

    @property
    def humanName(self) -> str:
        match self:
            case LanguageEntry.AFRIKAANS: return 'Afrikaans'
            case LanguageEntry.ARABIC: return 'Arabic'
            case LanguageEntry.BASQUE: return 'Basque'
            case LanguageEntry.BENGALI: return 'Bengali'
            case LanguageEntry.BULGARIAN: return 'Bulgarian'
            case LanguageEntry.CATALAN: return 'Catalan'
            case LanguageEntry.CHINESE: return 'Chinese'
            case LanguageEntry.CZECH: return 'Czech'
            case LanguageEntry.DANISH: return 'Danish'
            case LanguageEntry.DUTCH: return 'Dutch'
            case LanguageEntry.ENGLISH: return 'English'
            case LanguageEntry.ENGLISH_FOR_PORTUGUESE_SPEAKERS: return 'English for Portuguese speakers'
            case LanguageEntry.ENGLISH_FOR_SPANISH_SPEAKERS: return 'English for Spanish speakers'
            case LanguageEntry.FILIPINO: return 'Filipino'
            case LanguageEntry.FINNISH: return 'Finnish'
            case LanguageEntry.FRENCH: return 'French'
            case LanguageEntry.GALICIAN: return'Galician'
            case LanguageEntry.GERMAN: return 'German'
            case LanguageEntry.GREEK: return 'Greek'
            case LanguageEntry.GUJARATI: return 'Gujarati'
            case LanguageEntry.HEBREW: return 'Hebrew'
            case LanguageEntry.HINDI: return 'Hindi'
            case LanguageEntry.HUNGARIAN: return 'Hungarian'
            case LanguageEntry.ICELANDIC: return 'Icelandic'
            case LanguageEntry.INDONESIAN: return 'Indonesian'
            case LanguageEntry.ITALIAN: return 'Italian'
            case LanguageEntry.JAPANESE: return 'Japanese'
            case LanguageEntry.KANNADA: return 'Kannada'
            case LanguageEntry.KOREAN: return 'Korean'
            case LanguageEntry.LATIN: return'Latin'
            case LanguageEntry.LATVIAN: return 'Latvian'
            case LanguageEntry.LITHUANIAN: return 'Lithuanian'
            case LanguageEntry.MALAY: return 'Malay'
            case LanguageEntry.MALAYALAM: return 'Malayalam'
            case LanguageEntry.MARATHI: return 'Marathi'
            case LanguageEntry.NORWEGIAN: return 'Norwegian'
            case LanguageEntry.POLISH: return 'Polish'
            case LanguageEntry.PORTUGUESE: return'Portuguese'
            case LanguageEntry.PUNJABI: return'Punjabi'
            case LanguageEntry.ROMANIAN: return 'Romanian'
            case LanguageEntry.RUSSIAN: return 'Russian'
            case LanguageEntry.SERBIAN: return 'Serbian'
            case LanguageEntry.SLOVAK: return 'Slovak'
            case LanguageEntry.SPANISH: return'Spanish'
            case LanguageEntry.SWEDISH: return 'Swedish'
            case LanguageEntry.TAMIL: return'Tamil'
            case LanguageEntry.TELUGU: return 'Telugu'
            case LanguageEntry.THAI: return 'Thai'
            case LanguageEntry.TURKISH: return 'Turkish'
            case LanguageEntry.UKRANIAN: return 'Ukranian'
            case LanguageEntry.URDU: return 'Urdu'
            case LanguageEntry.VIETNAMESE: return 'Vietnamese'
            case _: raise RuntimeError(f'Unknown LanguageEntry value: \"{self}\"')

    @property
    def iso6391Code(self) -> str | None:
        match self:
            case LanguageEntry.AFRIKAANS: return 'af'
            case LanguageEntry.ARABIC: return 'ar'
            case LanguageEntry.BASQUE: return 'eu'
            case LanguageEntry.BENGALI: return 'bn'
            case LanguageEntry.BULGARIAN: return 'bg'
            case LanguageEntry.CATALAN: return 'ca'
            case LanguageEntry.CHINESE: return 'zh'
            case LanguageEntry.CZECH: return 'cs'
            case LanguageEntry.DANISH: return 'da'
            case LanguageEntry.DUTCH: return 'nl'
            case LanguageEntry.ENGLISH: return 'en'
            case LanguageEntry.ENGLISH_FOR_PORTUGUESE_SPEAKERS: return 'en-pt'
            case LanguageEntry.ENGLISH_FOR_SPANISH_SPEAKERS: return 'en-es'
            case LanguageEntry.FILIPINO: return 'fil'
            case LanguageEntry.FINNISH: return 'fi'
            case LanguageEntry.FRENCH: return 'fr'
            case LanguageEntry.GALICIAN: return 'gl'
            case LanguageEntry.GERMAN: return 'de'
            case LanguageEntry.GREEK: return 'el'
            case LanguageEntry.GUJARATI: return 'gu'
            case LanguageEntry.HEBREW: return 'he'
            case LanguageEntry.HINDI: return 'hi'
            case LanguageEntry.HUNGARIAN: return 'hu'
            case LanguageEntry.ICELANDIC: return 'is'
            case LanguageEntry.INDONESIAN: return 'id'
            case LanguageEntry.ITALIAN: return 'it'
            case LanguageEntry.JAPANESE: return 'ja'
            case LanguageEntry.KANNADA: return 'kn'
            case LanguageEntry.KOREAN: return 'ko'
            case LanguageEntry.LATIN: return 'la'
            case LanguageEntry.LATVIAN: return 'lv'
            case LanguageEntry.LITHUANIAN: return 'lt'
            case LanguageEntry.MALAY: return 'ms'
            case LanguageEntry.MALAYALAM: return 'ml'
            case LanguageEntry.MARATHI: return 'mr'
            case LanguageEntry.NORWEGIAN: return 'no'
            case LanguageEntry.POLISH: return 'pl'
            case LanguageEntry.PORTUGUESE: return 'pt'
            case LanguageEntry.PUNJABI: return 'pa'
            case LanguageEntry.ROMANIAN: return 'ro'
            case LanguageEntry.RUSSIAN: return 'ru'
            case LanguageEntry.SERBIAN: return 'sr'
            case LanguageEntry.SLOVAK: return 'sk'
            case LanguageEntry.SPANISH: return 'es'
            case LanguageEntry.SWEDISH: return 'sv'
            case LanguageEntry.TAMIL: return 'ta'
            case LanguageEntry.TELUGU: return 'te'
            case LanguageEntry.THAI: return 'th'
            case LanguageEntry.TURKISH: return 'tr'
            case LanguageEntry.UKRANIAN: return 'uk'
            case LanguageEntry.URDU: return 'ur'
            case LanguageEntry.VIETNAMESE: return 'vi'
            case _: raise RuntimeError(f'Unknown LanguageEntry value: \"{self}\"')

    @property
    def primaryCommandName(self) -> str:
        return self.commandNames[0]

    def requireIso6391Code(self) -> str:
        iso6391Code = self.iso6391Code

        if not utils.isValidStr(iso6391Code):
            raise RuntimeError(f'LanguageEntry has no iso6391Code value: ({self}) ({iso6391Code=})')

        return iso6391Code

    def requireWotdApiCode(self) -> str:
        wotdApiCode = self.wotdApiCode

        if not utils.isValidStr(wotdApiCode):
            raise RuntimeError(f'LanguageEntry has no wotdApiCode value: ({self}) ({wotdApiCode=})')

        return wotdApiCode

    @property
    def wotdApiCode(self) -> str | None:
        ########################################################################################
        ## The below strings directly correspond to the different available "Word of the Day" ##
        ## from this website: https://www.transparent.com/word-of-the-day                     ##
        ##                                                                                    ##
        ## Not all languages are available, and there is not really a predictable consistency ##
        ## either. So I built up this list manually, by using my browser's network inspection ##
        ## feature, and checking all the featured languages.                                  ##
        ########################################################################################

        match self:
            case LanguageEntry.AFRIKAANS: return None
            case LanguageEntry.ARABIC: return 'ar'
            case LanguageEntry.BASQUE: return None
            case LanguageEntry.BENGALI: return None
            case LanguageEntry.BULGARIAN: return None
            case LanguageEntry.CATALAN: return None
            case LanguageEntry.CHINESE: return 'zh'
            case LanguageEntry.CZECH: return None
            case LanguageEntry.DANISH: return None
            case LanguageEntry.DUTCH: return 'nl'
            case LanguageEntry.ENGLISH: return None
            case LanguageEntry.ENGLISH_FOR_PORTUGUESE_SPEAKERS: return 'en-pt'
            case LanguageEntry.ENGLISH_FOR_SPANISH_SPEAKERS: return 'en-es'
            case LanguageEntry.FILIPINO: return None
            case LanguageEntry.FINNISH: return None
            case LanguageEntry.FRENCH: return 'fr'
            case LanguageEntry.GALICIAN: return None
            case LanguageEntry.GERMAN: return 'de'
            case LanguageEntry.GREEK: return None
            case LanguageEntry.GUJARATI: return None
            case LanguageEntry.HEBREW: return 'hebrew'
            case LanguageEntry.HINDI: return 'hindi'
            case LanguageEntry.HUNGARIAN: return None
            case LanguageEntry.ICELANDIC: return None
            case LanguageEntry.INDONESIAN: return 'indonesian'
            case LanguageEntry.ITALIAN: return 'it'
            case LanguageEntry.JAPANESE: return 'ja'
            case LanguageEntry.KANNADA: return None
            case LanguageEntry.KOREAN: return 'korean'
            case LanguageEntry.LATIN: return 'la'
            case LanguageEntry.LATVIAN: return None
            case LanguageEntry.LITHUANIAN: return None
            case LanguageEntry.MALAY: return None
            case LanguageEntry.MALAYALAM: return None
            case LanguageEntry.MARATHI: return None
            case LanguageEntry.NORWEGIAN: return 'norwegian'
            case LanguageEntry.POLISH: return 'polish'
            case LanguageEntry.PORTUGUESE: return 'pt'
            case LanguageEntry.PUNJABI: return None
            case LanguageEntry.ROMANIAN: return None
            case LanguageEntry.RUSSIAN: return 'ru'
            case LanguageEntry.SERBIAN: return None
            case LanguageEntry.SLOVAK: return None
            case LanguageEntry.SPANISH: return 'es'
            case LanguageEntry.SWEDISH: return 'swedish'
            case LanguageEntry.TAMIL: return None
            case LanguageEntry.TELUGU: return None
            case LanguageEntry.THAI: return None
            case LanguageEntry.TURKISH: return 'turkish'
            case LanguageEntry.UKRANIAN: return None
            case LanguageEntry.URDU: return 'urdu'
            case LanguageEntry.VIETNAMESE: return None
            case _: raise RuntimeError(f'Unknown LanguageEntry value: \"{self}\"')
