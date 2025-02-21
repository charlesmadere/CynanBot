import random

from frozenlist import FrozenList

from .googleTtsVoicesHelperInterface import GoogleTtsVoicesHelperInterface
from ..models.googleVoicePreset import GoogleVoicePreset
from ...language.languageEntry import LanguageEntry


class GoogleTtsVoicesHelper(GoogleTtsVoicesHelperInterface):

    async def chooseEnglishVoice(self) -> GoogleVoicePreset:
        voice = await self.getVoiceForLanguage(LanguageEntry.ENGLISH)

        if voice is None:
            raise RuntimeError(f'Failed to choose an english voice! ({voice=})')

        return voice

    async def getVoiceForLanguage(
        self,
        languageEntry: LanguageEntry
    ) -> GoogleVoicePreset | None:
        if not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')

        voices = await self.getVoicesForLanguage(languageEntry)

        if len(voices) == 0:
            return None

        voicesList: FrozenList[GoogleVoicePreset] = FrozenList(voices)
        voicesList.freeze()

        return random.choice(voicesList)

    async def getVoicesForLanguage(
        self,
        languageEntry: LanguageEntry
    ) -> frozenset[GoogleVoicePreset]:
        if not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')

        voicePresets: set[GoogleVoicePreset]

        match languageEntry:
            case LanguageEntry.DUTCH:
                voicePresets = {
                    GoogleVoicePreset.DUTCH_BELGIUM_STANDARD_A,
                    GoogleVoicePreset.DUTCH_BELGIUM_STANDARD_B,
                    GoogleVoicePreset.DUTCH_BELGIUM_STANDARD_C,
                    GoogleVoicePreset.DUTCH_BELGIUM_STANDARD_D
                }

            case LanguageEntry.ENGLISH:
                voicePresets = {
                    GoogleVoicePreset.ENGLISH_AUSTRALIAN_CHIRP_D,
                    GoogleVoicePreset.ENGLISH_AUSTRALIAN_CHIRP_F,
                    GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_D,
                    GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_F,
                    GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_O
                }

            case LanguageEntry.FRENCH:
                voicePresets = {
                    GoogleVoicePreset.FRENCH_CANADA_CHIRP_D,
                    GoogleVoicePreset.FRENCH_CANADA_CHIRP_F,
                    GoogleVoicePreset.FRENCH_CANADA_CHIRP_O
                }

            case LanguageEntry.GERMAN:
                voicePresets = {
                    GoogleVoicePreset.GERMAN_GERMANY_CHIRP_D,
                    GoogleVoicePreset.GERMAN_GERMANY_CHIRP_F,
                    GoogleVoicePreset.GERMAN_GERMANY_CHIRP_O
                }

            case LanguageEntry.ITALIAN:
                voicePresets = {
                    GoogleVoicePreset.ITALIAN_ITALY_CHIRP_D,
                    GoogleVoicePreset.ITALIAN_ITALY_CHIRP_F,
                    GoogleVoicePreset.ITALIAN_ITALY_CHIRP_O
                }

            case LanguageEntry.JAPANESE:
                voicePresets = {
                    GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_A,
                    GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_B,
                    GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_C,
                    GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_D
                }

            case LanguageEntry.KOREAN:
                voicePresets = {
                    GoogleVoicePreset.KOREAN_KOREA_STANDARD_A,
                    GoogleVoicePreset.KOREAN_KOREA_STANDARD_B,
                    GoogleVoicePreset.KOREAN_KOREA_STANDARD_C,
                    GoogleVoicePreset.KOREAN_KOREA_STANDARD_D
                }

            case LanguageEntry.NORWEGIAN:
                voicePresets = {
                    GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_A,
                    GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_B,
                    GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_C,
                    GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_D,
                    GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_E,
                    GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_F,
                    GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_G
                }

            case LanguageEntry.PORTUGUESE:
                voicePresets = {
                    GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_A,
                    GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_B,
                    GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_C,
                    GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_D,
                    GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_E,
                    GoogleVoicePreset.PORTUGUESE_PORTUGAL_STANDARD_A,
                    GoogleVoicePreset.PORTUGUESE_PORTUGAL_STANDARD_B,
                    GoogleVoicePreset.PORTUGUESE_PORTUGAL_STANDARD_C,
                    GoogleVoicePreset.PORTUGUESE_PORTUGAL_STANDARD_D,
                    GoogleVoicePreset.PORTUGUESE_PORTUGAL_STANDARD_E,
                    GoogleVoicePreset.PORTUGUESE_PORTUGAL_STANDARD_F
                }

            case LanguageEntry.SPANISH:
                voicePresets = {
                    GoogleVoicePreset.SPANISH_US_CHIRP_D,
                    GoogleVoicePreset.SPANISH_US_CHIRP_F,
                    GoogleVoicePreset.SPANISH_US_CHIRP_O
                }

            case LanguageEntry.SWEDISH:
                voicePresets = {
                    GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_A,
                    GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_B,
                    GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_C,
                    GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_D
                }

            case LanguageEntry.FINNISH:
                voicePresets = {
                    GoogleVoicePreset.FINNISH_FINLAND_STANDARD_A,
                    GoogleVoicePreset.FINNISH_FINLAND_STANDARD_B,
                }

            case _:
                voicePresets = set()

        return frozenset(voicePresets)
