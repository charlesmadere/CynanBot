from typing import Any

from .languageEntryJsonMapperInterface import LanguageEntryJsonMapperInterface
from ..languageEntry import LanguageEntry
from ...misc import utils as utils


class LanguageEntryJsonMapper(LanguageEntryJsonMapperInterface):

    def parseLanguageEntry(
        self,
        jsonString: str | Any | None
    ) -> LanguageEntry | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonString = jsonString.lower()

        # Note that there are missing case statements for two LanguageEntry values:
        #  * ENGLISH_FOR_PORTUGUESE_SPEAKERS
        #  * ENGLISH_FOR_SPANISH_SPEAKERS
        #
        # These are intentionally left out. This is because those two values probably
        # don't really belong here, and should be refactored to be somewhere else. They
        # primarily exist to help facilitate some Word Of The Day functionality and so
        # shouldn't really be here.

        match jsonString:
            case 'afrikaans': return LanguageEntry.AFRIKAANS
            case 'arabic': return LanguageEntry.ARABIC
            case 'basque': return LanguageEntry.BASQUE
            case 'bengali': return LanguageEntry.BENGALI
            case 'bulgarian': return LanguageEntry.BULGARIAN
            case 'catalan': return LanguageEntry.CATALAN
            case 'chinese': return LanguageEntry.CHINESE
            case 'czech': return LanguageEntry.CZECH
            case 'danish': return LanguageEntry.DANISH
            case 'dutch': return LanguageEntry.DUTCH
            case 'english': return LanguageEntry.ENGLISH
            case 'filipino': return LanguageEntry.FILIPINO
            case 'finnish': return LanguageEntry.FINNISH
            case 'french': return LanguageEntry.FRENCH
            case 'galician': return LanguageEntry.GALICIAN
            case 'german': return LanguageEntry.GERMAN
            case 'greek': return LanguageEntry.GREEK
            case 'gujarati': return LanguageEntry.GUJARATI
            case 'hebrew': return LanguageEntry.HEBREW
            case 'hindi': return LanguageEntry.HINDI
            case 'hungarian': return LanguageEntry.HUNGARIAN
            case 'icelandic': return LanguageEntry.ICELANDIC
            case 'indonesian': return LanguageEntry.INDONESIAN
            case 'italian': return LanguageEntry.ITALIAN
            case 'japanese': return LanguageEntry.JAPANESE
            case 'kannada': return LanguageEntry.KANNADA
            case 'korean': return LanguageEntry.KOREAN
            case 'latin': return LanguageEntry.LATIN
            case 'latvian': return LanguageEntry.LATVIAN
            case 'lithuanian': return LanguageEntry.LITHUANIAN
            case 'malay': return LanguageEntry.MALAY
            case 'malayalam': return LanguageEntry.MALAYALAM
            case 'marathi': return LanguageEntry.MARATHI
            case 'norwegian': return LanguageEntry.NORWEGIAN
            case 'polish': return LanguageEntry.POLISH
            case 'portuguese': return LanguageEntry.PORTUGUESE
            case 'punjabi': return LanguageEntry.PUNJABI
            case 'romanian': return LanguageEntry.ROMANIAN
            case 'russian': return LanguageEntry.RUSSIAN
            case 'serbian': return LanguageEntry.SERBIAN
            case 'slovak': return LanguageEntry.SLOVAK
            case 'spanish': return LanguageEntry.SPANISH
            case 'swedish': return LanguageEntry.SWEDISH
            case 'tamil': return LanguageEntry.TAMIL
            case 'telugu': return LanguageEntry.TELUGU
            case 'thai': return LanguageEntry.THAI
            case 'turkish': return LanguageEntry.TURKISH
            case 'ukranian': return LanguageEntry.UKRANIAN
            case 'urdu': return LanguageEntry.URDU
            case 'vietnamese': return LanguageEntry.VIETNAMESE
            case _: return None

    def requireLanguageEntry(
        self,
        jsonString: str | Any | None
    ) -> LanguageEntry:
        result = self.parseLanguageEntry(jsonString)

        if result is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into a LanguageEntry')

        return result

    def serializeLanguageEntry(
        self,
        languageEntry: LanguageEntry
    ) -> str:
        if not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')

        match languageEntry:
            case LanguageEntry.AFRIKAANS: return 'afrikaans'
            case LanguageEntry.ARABIC: return 'arabic'
            case LanguageEntry.BASQUE: return 'basque'
            case LanguageEntry.BENGALI: return 'bengali'
            case LanguageEntry.BULGARIAN: return 'bulgarian'
            case LanguageEntry.CATALAN: return 'catalan'
            case LanguageEntry.CHINESE: return 'chinese'
            case LanguageEntry.CZECH: return 'czech'
            case LanguageEntry.DANISH: return 'danish'
            case LanguageEntry.DUTCH: return 'dutch'
            case LanguageEntry.ENGLISH: return 'english'
            case LanguageEntry.FILIPINO: return 'filipino'
            case LanguageEntry.FINNISH: return 'finnish'
            case LanguageEntry.FRENCH: return 'french'
            case LanguageEntry.GALICIAN: return 'galician'
            case LanguageEntry.GERMAN: return 'german'
            case LanguageEntry.GREEK: return 'greek'
            case LanguageEntry.GUJARATI: return 'gujarati'
            case LanguageEntry.HEBREW: return 'hebrew'
            case LanguageEntry.HINDI: return 'hindi'
            case LanguageEntry.HUNGARIAN: return 'hungarian'
            case LanguageEntry.ICELANDIC: return 'icelandic'
            case LanguageEntry.INDONESIAN: return 'indonesian'
            case LanguageEntry.ITALIAN: return 'italian'
            case LanguageEntry.JAPANESE: return 'japanese'
            case LanguageEntry.KANNADA: return 'kannada'
            case LanguageEntry.KOREAN: return 'korean'
            case LanguageEntry.LATIN: return 'latin'
            case LanguageEntry.LATVIAN: return 'latvian'
            case LanguageEntry.LITHUANIAN: return 'lithuanian'
            case LanguageEntry.MALAY: return 'malay'
            case LanguageEntry.MALAYALAM: return 'malayalam'
            case LanguageEntry.MARATHI: return 'marathi'
            case LanguageEntry.NORWEGIAN: return 'norwegian'
            case LanguageEntry.POLISH: return 'polish'
            case LanguageEntry.PORTUGUESE: return 'portuguese'
            case LanguageEntry.PUNJABI: return 'punjabi'
            case LanguageEntry.ROMANIAN: return 'romanian'
            case LanguageEntry.RUSSIAN: return 'russian'
            case LanguageEntry.SERBIAN: return 'serbian'
            case LanguageEntry.SLOVAK: return 'slovak'
            case LanguageEntry.SPANISH: return 'spanish'
            case LanguageEntry.SWEDISH: return 'swedish'
            case LanguageEntry.TAMIL: return 'tamil'
            case LanguageEntry.TELUGU: return 'telugu'
            case LanguageEntry.THAI: return 'thai'
            case LanguageEntry.TURKISH: return 'turkish'
            case LanguageEntry.UKRANIAN: return 'ukranian'
            case LanguageEntry.URDU: return 'urdu'
            case LanguageEntry.VIETNAMESE: return 'vietnamese'
            case _: raise ValueError(f'Unknown languageEntry value: \"{languageEntry}\"')
