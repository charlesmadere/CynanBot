from enum import Enum, auto


class TransparentLanguageEntry(Enum):

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
    def apiCode(self) -> str | None:
        match self:
            case TransparentLanguageEntry.CHINESE: return 'zh'
            case TransparentLanguageEntry.DUTCH: return 'nl'
            case TransparentLanguageEntry.ENGLISH: return None
            case TransparentLanguageEntry.ENGLISH_FOR_PORTUGUESE_SPEAKERS: return 'en-pt'
            case TransparentLanguageEntry.ENGLISH_FOR_SPANISH_SPEAKERS: return 'en-es'
            case TransparentLanguageEntry.FRENCH: return 'fr'
            case TransparentLanguageEntry.GERMAN: return 'de'
            case TransparentLanguageEntry.GREEK: return None
            case TransparentLanguageEntry.HINDI: return 'hindi'
            case TransparentLanguageEntry.ITALIAN: return 'it'
            case TransparentLanguageEntry.JAPANESE: return 'ja'
            case TransparentLanguageEntry.KOREAN: return 'korean'
            case TransparentLanguageEntry.LATIN: return None
            case TransparentLanguageEntry.NORWEGIAN: return 'norwegian'
            case TransparentLanguageEntry.POLISH: return 'polish'
            case TransparentLanguageEntry.PORTUGUESE: return 'pt'
            case TransparentLanguageEntry.RUSSIAN: return 'ru'
            case TransparentLanguageEntry.SPANISH: return 'es'
            case TransparentLanguageEntry.SWEDISH: return 'swedish'
            case TransparentLanguageEntry.THAI: return None
            case TransparentLanguageEntry.URDU: return 'urdu'
            case _: raise RuntimeError(f'Unknown TransparentLanguageEntry value: \"{self}\"')
