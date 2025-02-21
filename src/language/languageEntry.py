from enum import Enum, auto

from frozenlist import FrozenList

from ..misc import utils as utils


class LanguageEntry(Enum):

    CHINESE = auto()
    DUTCH = auto()
    ENGLISH = auto()
    ENGLISH_FOR_PORTUGUESE_SPEAKERS = auto()
    ENGLISH_FOR_SPANISH_SPEAKERS = auto()
    FRENCH = auto()
    GERMAN = auto()
    GREEK = auto()
    HINDI = auto()
    ITALIAN = auto()
    JAPANESE = auto()
    KOREAN = auto()
    LATIN = auto()
    NORWEGIAN = auto()
    POLISH = auto()
    PORTUGUESE = auto()
    RUSSIAN = auto()
    SPANISH = auto()
    SWEDISH = auto()
    THAI = auto()
    URDU = auto()

    @property
    def commandNames(self) -> FrozenList[str]:
        commandNames: list[str]

        match self:
            case LanguageEntry.CHINESE:
                commandNames = [ 'zh', 'chinese', 'china', '中文' ]

            case LanguageEntry.DUTCH:
                commandNames = [ 'nl', 'dutch', 'nederlands', 'netherlands', 'vlaams' ]

            case LanguageEntry.ENGLISH:
                commandNames = [ 'en', 'eng', 'english', '英語' ]

            case LanguageEntry.ENGLISH_FOR_PORTUGUESE_SPEAKERS:
                commandNames = [ 'en-pt' ]

            case LanguageEntry.ENGLISH_FOR_SPANISH_SPEAKERS:
                commandNames = [ 'en-es' ]

            case LanguageEntry.FRENCH:
                commandNames = [ 'fr', 'français', 'france', 'french' ]

            case LanguageEntry.GERMAN:
                commandNames = [ 'de', 'deutsche', 'german', 'germany' ]

            case LanguageEntry.GREEK:
                commandNames = [ 'el', 'greek' ]

            case LanguageEntry.HINDI:
                commandNames = [ 'hi', 'hin', 'hindi' ]

            case LanguageEntry.ITALIAN:
                commandNames = [ 'it', 'italian', 'italiano', 'italy' ]

            case LanguageEntry.JAPANESE:
                commandNames = [ 'ja', 'japan', 'japanese', 'jp', '日本語', 'にほんご' ]

            case LanguageEntry.KOREAN:
                commandNames = [ 'ko', 'korea', 'korean', '한국어' ]

            case LanguageEntry.LATIN:
                commandNames = [ 'la', 'latin' ]

            case LanguageEntry.NORWEGIAN:
                commandNames = [ 'no', 'norsk', 'norway', 'norwegian' ]

            case LanguageEntry.POLISH:
                commandNames = [ 'po', 'poland', 'polish' ]

            case LanguageEntry.PORTUGUESE:
                commandNames = [ 'pt', 'portuguese', 'português' ]

            case LanguageEntry.RUSSIAN:
                commandNames = [ 'ru', 'russia', 'russian', 'русский' ]

            case LanguageEntry.SPANISH:
                commandNames = [ 'es', 'español', 'sp', 'spanish' ]

            case LanguageEntry.SWEDISH:
                commandNames = [ 'se', 'sv', 'svenska', 'sw', 'sweden', 'swedish' ]

            case LanguageEntry.THAI:
                commandNames = [ 'th', 'thai' ]

            case LanguageEntry.URDU:
                commandNames = [ 'ur', 'urd', 'urdu' ]

            case _:
                raise RuntimeError(f'Unknown LanguageEntry value: \"{self}\"')

        frozenCommandNames: FrozenList[str] = FrozenList(commandNames)
        frozenCommandNames.freeze()

        return frozenCommandNames

    @property
    def flag(self) -> str | None:
        match self:
            case LanguageEntry.CHINESE: return '🇨🇳'
            case LanguageEntry.DUTCH: return '🇳🇱'
            case LanguageEntry.ENGLISH: return '🇬🇧'
            case LanguageEntry.ENGLISH_FOR_PORTUGUESE_SPEAKERS: return None
            case LanguageEntry.ENGLISH_FOR_SPANISH_SPEAKERS: return None
            case LanguageEntry.FRENCH: return '🇫🇷'
            case LanguageEntry.GERMAN: return '🇩🇪'
            case LanguageEntry.GREEK: return '🇬🇷'
            case LanguageEntry.HINDI: return '🇮🇳'
            case LanguageEntry.ITALIAN: return '🇮🇹'
            case LanguageEntry.JAPANESE: return '🇯🇵'
            case LanguageEntry.KOREAN: return '🇰🇷'
            case LanguageEntry.LATIN: return None
            case LanguageEntry.NORWEGIAN: return '🇳🇴'
            case LanguageEntry.POLISH: return '🇵🇱'
            case LanguageEntry.PORTUGUESE: return None
            case LanguageEntry.RUSSIAN: return '🇷🇺'
            case LanguageEntry.SPANISH: return None
            case LanguageEntry.SWEDISH: return '🇸🇪'
            case LanguageEntry.THAI: return '🇹🇭'
            case LanguageEntry.URDU: return '🇵🇰'
            case _: raise RuntimeError(f'Unknown LanguageEntry value: \"{self}\"')

    @property
    def iso6391Code(self) -> str | None:
        match self:
            case LanguageEntry.CHINESE: return 'zh'
            case LanguageEntry.DUTCH: return 'nl'
            case LanguageEntry.ENGLISH: return None
            case LanguageEntry.ENGLISH_FOR_PORTUGUESE_SPEAKERS: return 'en-pt'
            case LanguageEntry.ENGLISH_FOR_SPANISH_SPEAKERS: return 'en-es'
            case LanguageEntry.FRENCH: return 'fr'
            case LanguageEntry.GERMAN: return 'de'
            case LanguageEntry.GREEK: return 'el'
            case LanguageEntry.HINDI: return 'hi'
            case LanguageEntry.ITALIAN: return 'it'
            case LanguageEntry.JAPANESE: return 'ja'
            case LanguageEntry.KOREAN: return 'ko'
            case LanguageEntry.LATIN: return 'la'
            case LanguageEntry.NORWEGIAN: return 'no'
            case LanguageEntry.POLISH: return 'pl'
            case LanguageEntry.PORTUGUESE: return 'pt'
            case LanguageEntry.RUSSIAN: return 'ru'
            case LanguageEntry.SPANISH: return 'es'
            case LanguageEntry.SWEDISH: return 'sv'
            case LanguageEntry.THAI: return 'th'
            case LanguageEntry.URDU: return 'ur'
            case _: raise RuntimeError(f'Unknown LanguageEntry value: \"{self}\"')

    @property
    def name(self) -> str:
        match self:
            case LanguageEntry.CHINESE: return 'Chinese'
            case LanguageEntry.DUTCH: return 'Dutch'
            case LanguageEntry.ENGLISH: return 'English'
            case LanguageEntry.ENGLISH_FOR_PORTUGUESE_SPEAKERS: return 'English for Portuguese speakers'
            case LanguageEntry.ENGLISH_FOR_SPANISH_SPEAKERS: return 'English for Spanish speakers'
            case LanguageEntry.FRENCH: return 'French'
            case LanguageEntry.GERMAN: return 'German'
            case LanguageEntry.GREEK: return 'Greek'
            case LanguageEntry.HINDI: return 'Hindi'
            case LanguageEntry.ITALIAN: return 'Italian'
            case LanguageEntry.JAPANESE: return 'Japanese'
            case LanguageEntry.KOREAN: return 'Korean'
            case LanguageEntry.LATIN: return 'Latin'
            case LanguageEntry.NORWEGIAN: return 'Norwegian'
            case LanguageEntry.POLISH: return 'Polish'
            case LanguageEntry.PORTUGUESE: return 'Portuguese'
            case LanguageEntry.RUSSIAN: return 'Russian'
            case LanguageEntry.SPANISH: return 'Spanish'
            case LanguageEntry.SWEDISH: return 'Swedish'
            case LanguageEntry.THAI: return 'Thai'
            case LanguageEntry.URDU: return 'Urdu'
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
        match self:
            case LanguageEntry.CHINESE: return 'zh'
            case LanguageEntry.DUTCH: return 'nl'
            case LanguageEntry.ENGLISH: return None
            case LanguageEntry.ENGLISH_FOR_PORTUGUESE_SPEAKERS: return 'en-pt'
            case LanguageEntry.ENGLISH_FOR_SPANISH_SPEAKERS: return 'en-es'
            case LanguageEntry.FRENCH: return 'fr'
            case LanguageEntry.GERMAN: return 'de'
            case LanguageEntry.GREEK: return None
            case LanguageEntry.HINDI: return 'hindi'
            case LanguageEntry.ITALIAN: return 'it'
            case LanguageEntry.JAPANESE: return 'ja'
            case LanguageEntry.KOREAN: return 'korean'
            case LanguageEntry.LATIN: return None
            case LanguageEntry.NORWEGIAN: return 'norwegian'
            case LanguageEntry.POLISH: return 'polish'
            case LanguageEntry.PORTUGUESE: return 'pt'
            case LanguageEntry.RUSSIAN: return 'ru'
            case LanguageEntry.SPANISH: return 'es'
            case LanguageEntry.SWEDISH: return 'swedish'
            case LanguageEntry.THAI: return None
            case LanguageEntry.URDU: return 'urdu'
            case _: raise RuntimeError(f'Unknown LanguageEntry value: \"{self}\"')
