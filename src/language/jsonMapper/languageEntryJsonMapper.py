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
            case 'chinese': return LanguageEntry.CHINESE
            case 'dutch': return LanguageEntry.DUTCH
            case 'english': return LanguageEntry.ENGLISH
            case 'french': return LanguageEntry.FRENCH
            case 'german': return LanguageEntry.GERMAN
            case 'greek': return LanguageEntry.GREEK
            case 'hindi': return LanguageEntry.HINDI
            case 'italian': return LanguageEntry.ITALIAN
            case 'japanese': return LanguageEntry.JAPANESE
            case 'korean': return LanguageEntry.KOREAN
            case 'latin': return LanguageEntry.LATIN
            case 'norwegian': return LanguageEntry.NORWEGIAN
            case 'polish': return LanguageEntry.POLISH
            case 'portuguese': return LanguageEntry.PORTUGUESE
            case 'russian': return LanguageEntry.RUSSIAN
            case 'spanish': return LanguageEntry.SPANISH
            case 'swedish': return LanguageEntry.SWEDISH
            case 'thai': return LanguageEntry.THAI
            case 'urdu': return LanguageEntry.URDU
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
            case LanguageEntry.CHINESE: return 'chinese'
            case LanguageEntry.DUTCH: return 'dutch'
            case LanguageEntry.ENGLISH: return 'english'
            case LanguageEntry.FRENCH: return 'french'
            case LanguageEntry.GERMAN: return 'german'
            case LanguageEntry.GREEK: return 'greek'
            case LanguageEntry.HINDI: return 'hindi'
            case LanguageEntry.ITALIAN: return 'italian'
            case LanguageEntry.JAPANESE: return 'japanese'
            case LanguageEntry.KOREAN: return 'korean'
            case LanguageEntry.LATIN: return 'latin'
            case LanguageEntry.NORWEGIAN: return 'norwegian'
            case LanguageEntry.POLISH: return 'polish'
            case LanguageEntry.RUSSIAN: return 'russian'
            case LanguageEntry.SPANISH: return 'spanish'
            case LanguageEntry.SWEDISH: return 'swedish'
            case LanguageEntry.THAI: return 'thai'
            case LanguageEntry.URDU: return 'urdu'
            case _: raise ValueError(f'Unknown languageEntry value: \"{languageEntry}\"')
