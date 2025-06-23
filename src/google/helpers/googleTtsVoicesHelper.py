import random

from .googleTtsVoicesHelperInterface import GoogleTtsVoicesHelperInterface
from ..models.googleVoicePreset import GoogleVoicePreset
from ...language.languageEntry import LanguageEntry


class GoogleTtsVoicesHelper(GoogleTtsVoicesHelperInterface):

    async def getEnglishVoice(self) -> GoogleVoicePreset:
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
        else:
            return random.choice(list(voices))

    async def getVoicesForLanguage(
        self,
        languageEntry: LanguageEntry
    ) -> frozenset[GoogleVoicePreset]:
        if not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')

        voicePresets: set[GoogleVoicePreset]

        match languageEntry:
            case LanguageEntry.AFRIKAANS:
                voicePresets = {
                    GoogleVoicePreset.AFRIKAANS_SOUTH_AFRICA_STANDARD_A,
                }

            case LanguageEntry.ARABIC:
                voicePresets = {
                    GoogleVoicePreset.ARABIC_STANDARD_A,
                    GoogleVoicePreset.ARABIC_STANDARD_B,
                    GoogleVoicePreset.ARABIC_STANDARD_C,
                    GoogleVoicePreset.ARABIC_STANDARD_D,
                }

            case LanguageEntry.BASQUE:
                voicePresets = {
                    GoogleVoicePreset.BASQUE_SPAIN_STANDARD_A,
                    GoogleVoicePreset.BASQUE_SPAIN_STANDARD_B,
                }

            case LanguageEntry.BENGALI:
                voicePresets = {
                    GoogleVoicePreset.BENGALI_INDIA_STANDARD_A,
                    GoogleVoicePreset.BENGALI_INDIA_STANDARD_B,
                    GoogleVoicePreset.BENGALI_INDIA_STANDARD_C,
                    GoogleVoicePreset.BENGALI_INDIA_STANDARD_D,
                }

            case LanguageEntry.BULGARIAN:
                voicePresets = {
                    GoogleVoicePreset.BULGARIAN_BULGARIA_STANDARD_A,
                    GoogleVoicePreset.BULGARIAN_BULGARIA_STANDARD_B,
                }

            case LanguageEntry.CATALAN:
                voicePresets = {
                    GoogleVoicePreset.CATALAN_SPAIN_STANDARD_A,
                    GoogleVoicePreset.CATALAN_SPAIN_STANDARD_B,
                }

            case LanguageEntry.CHINESE:
                voicePresets = {
                    GoogleVoicePreset.CHINESE_CHINA_STANDARD_A,
                    GoogleVoicePreset.CHINESE_CHINA_STANDARD_B,
                    GoogleVoicePreset.CHINESE_CHINA_STANDARD_C,
                    GoogleVoicePreset.CHINESE_CHINA_STANDARD_D,
                    GoogleVoicePreset.CHINESE_HONG_KONG_STANDARD_A,
                    GoogleVoicePreset.CHINESE_HONG_KONG_STANDARD_B,
                    GoogleVoicePreset.CHINESE_HONG_KONG_STANDARD_C,
                    GoogleVoicePreset.CHINESE_HONG_KONG_STANDARD_D,
                    GoogleVoicePreset.CHINESE_TAIWAN_STANDARD_A,
                    GoogleVoicePreset.CHINESE_TAIWAN_STANDARD_B,
                    GoogleVoicePreset.CHINESE_TAIWAN_STANDARD_C,
                }

            case LanguageEntry.CZECH:
                voicePresets = {
                    GoogleVoicePreset.CZECH_CZECH_REPUBLIC_STANDARD_A,
                    GoogleVoicePreset.CZECH_CZECH_REPUBLIC_STANDARD_B,
                }

            case LanguageEntry.DANISH:
                voicePresets = {
                    GoogleVoicePreset.DANISH_DENMARK_STANDARD_A,
                    GoogleVoicePreset.DANISH_DENMARK_STANDARD_C,
                    GoogleVoicePreset.DANISH_DENMARK_STANDARD_D,
                    GoogleVoicePreset.DANISH_DENMARK_STANDARD_E,
                    GoogleVoicePreset.DANISH_DENMARK_STANDARD_F,
                    GoogleVoicePreset.DANISH_DENMARK_STANDARD_G,
                }

            case LanguageEntry.DUTCH:
                voicePresets = {
                    GoogleVoicePreset.DUTCH_BELGIUM_STANDARD_A,
                    GoogleVoicePreset.DUTCH_BELGIUM_STANDARD_B,
                    GoogleVoicePreset.DUTCH_BELGIUM_STANDARD_C,
                    GoogleVoicePreset.DUTCH_BELGIUM_STANDARD_D,
                    GoogleVoicePreset.DUTCH_NETHERLANDS_STANDARD_A,
                    GoogleVoicePreset.DUTCH_NETHERLANDS_STANDARD_B,
                    GoogleVoicePreset.DUTCH_NETHERLANDS_STANDARD_C,
                    GoogleVoicePreset.DUTCH_NETHERLANDS_STANDARD_D,
                    GoogleVoicePreset.DUTCH_NETHERLANDS_STANDARD_E,
                    GoogleVoicePreset.DUTCH_NETHERLANDS_STANDARD_F,
                    GoogleVoicePreset.DUTCH_NETHERLANDS_STANDARD_G,
                }

            case LanguageEntry.ENGLISH:
                voicePresets = {
                    GoogleVoicePreset.ENGLISH_AUSTRALIAN_CHIRP_D,
                    GoogleVoicePreset.ENGLISH_AUSTRALIAN_CHIRP_F,
                    GoogleVoicePreset.ENGLISH_AUSTRALIAN_CHIRP_O,
                    GoogleVoicePreset.ENGLISH_AUSTRALIAN_STANDARD_A,
                    GoogleVoicePreset.ENGLISH_AUSTRALIAN_STANDARD_B,
                    GoogleVoicePreset.ENGLISH_AUSTRALIAN_STANDARD_C,
                    GoogleVoicePreset.ENGLISH_AUSTRALIAN_STANDARD_D,
                    GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_D,
                    GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_F,
                    GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_O,
                }

            case LanguageEntry.FILIPINO:
                voicePresets = {
                    GoogleVoicePreset.FILIPINO_PHILIPPINES_STANDARD_A,
                    GoogleVoicePreset.FILIPINO_PHILIPPINES_STANDARD_B,
                    GoogleVoicePreset.FILIPINO_PHILIPPINES_STANDARD_C,
                    GoogleVoicePreset.FILIPINO_PHILIPPINES_STANDARD_D,
                }

            case LanguageEntry.FINNISH:
                voicePresets = {
                    GoogleVoicePreset.FINNISH_FINLAND_STANDARD_A,
                    GoogleVoicePreset.FINNISH_FINLAND_STANDARD_B,
                }

            case LanguageEntry.FRENCH:
                voicePresets = {
                    GoogleVoicePreset.FRENCH_CANADA_CHIRP_D,
                    GoogleVoicePreset.FRENCH_CANADA_CHIRP_F,
                    GoogleVoicePreset.FRENCH_CANADA_CHIRP_O,
                    GoogleVoicePreset.FRENCH_CANADA_STANDARD_A,
                    GoogleVoicePreset.FRENCH_CANADA_STANDARD_B,
                    GoogleVoicePreset.FRENCH_CANADA_STANDARD_C,
                    GoogleVoicePreset.FRENCH_CANADA_STANDARD_D,
                    GoogleVoicePreset.FRENCH_FRANCE_STANDARD_A,
                    GoogleVoicePreset.FRENCH_FRANCE_STANDARD_B,
                    GoogleVoicePreset.FRENCH_FRANCE_STANDARD_C,
                    GoogleVoicePreset.FRENCH_FRANCE_STANDARD_D,
                    GoogleVoicePreset.FRENCH_FRANCE_STANDARD_E,
                    GoogleVoicePreset.FRENCH_FRANCE_STANDARD_F,
                    GoogleVoicePreset.FRENCH_FRANCE_STANDARD_G,
                }

            case LanguageEntry.GALICIAN:
                voicePresets = {
                    GoogleVoicePreset.GALICIAN_SPAIN_STANDARD_A,
                    GoogleVoicePreset.GALICIAN_SPAIN_STANDARD_B,
                }

            case LanguageEntry.GERMAN:
                voicePresets = {
                    GoogleVoicePreset.GERMAN_GERMANY_CHIRP_D,
                    GoogleVoicePreset.GERMAN_GERMANY_CHIRP_F,
                    GoogleVoicePreset.GERMAN_GERMANY_CHIRP_O,
                    GoogleVoicePreset.GERMAN_GERMANY_STANDARD_A,
                    GoogleVoicePreset.GERMAN_GERMANY_STANDARD_B,
                    GoogleVoicePreset.GERMAN_GERMANY_STANDARD_C,
                    GoogleVoicePreset.GERMAN_GERMANY_STANDARD_D,
                    GoogleVoicePreset.GERMAN_GERMANY_STANDARD_E,
                    GoogleVoicePreset.GERMAN_GERMANY_STANDARD_F,
                    GoogleVoicePreset.GERMAN_GERMANY_STANDARD_G,
                    GoogleVoicePreset.GERMAN_GERMANY_STANDARD_H,
                }

            case LanguageEntry.GREEK:
                voicePresets = {
                    GoogleVoicePreset.GREEK_GREECE_STANDARD_A,
                    GoogleVoicePreset.GREEK_GREECE_STANDARD_B,
                }

            case LanguageEntry.GUJARATI:
                voicePresets = {
                    GoogleVoicePreset.GUJARATI_INDIA_STANDARD_A,
                    GoogleVoicePreset.GUJARATI_INDIA_STANDARD_B,
                    GoogleVoicePreset.GUJARATI_INDIA_STANDARD_C,
                    GoogleVoicePreset.GUJARATI_INDIA_STANDARD_D,
                }

            case LanguageEntry.HEBREW:
                voicePresets = {
                    GoogleVoicePreset.HEBREW_ISRAEL_STANDARD_A,
                    GoogleVoicePreset.HEBREW_ISRAEL_STANDARD_B,
                    GoogleVoicePreset.HEBREW_ISRAEL_STANDARD_C,
                    GoogleVoicePreset.HEBREW_ISRAEL_STANDARD_D,
                }

            case LanguageEntry.HINDI:
                voicePresets = {
                    GoogleVoicePreset.HINDI_INDIA_STANDARD_A,
                    GoogleVoicePreset.HINDI_INDIA_STANDARD_B,
                    GoogleVoicePreset.HINDI_INDIA_STANDARD_C,
                    GoogleVoicePreset.HINDI_INDIA_STANDARD_D,
                    GoogleVoicePreset.HINDI_INDIA_STANDARD_E,
                    GoogleVoicePreset.HINDI_INDIA_STANDARD_F,
                }

            case LanguageEntry.HUNGARIAN:
                voicePresets = {
                    GoogleVoicePreset.HUNGARIAN_HUNGARY_STANDARD_A,
                    GoogleVoicePreset.HUNGARIAN_HUNGARY_STANDARD_B,
                }

            case LanguageEntry.ICELANDIC:
                voicePresets = {
                    GoogleVoicePreset.ICELANDIC_ICELAND_STANDARD_A,
                    GoogleVoicePreset.ICELANDIC_ICELAND_STANDARD_B,
                }

            case LanguageEntry.INDONESIAN:
                voicePresets = {
                    GoogleVoicePreset.INDONESIAN_INDONESIA_STANDARD_A,
                    GoogleVoicePreset.INDONESIAN_INDONESIA_STANDARD_B,
                    GoogleVoicePreset.INDONESIAN_INDONESIA_STANDARD_C,
                    GoogleVoicePreset.INDONESIAN_INDONESIA_STANDARD_D,
                }

            case LanguageEntry.ITALIAN:
                voicePresets = {
                    GoogleVoicePreset.ITALIAN_ITALY_CHIRP_D,
                    GoogleVoicePreset.ITALIAN_ITALY_CHIRP_F,
                    GoogleVoicePreset.ITALIAN_ITALY_CHIRP_O,
                    GoogleVoicePreset.ITALIAN_ITALY_STANDARD_A,
                    GoogleVoicePreset.ITALIAN_ITALY_STANDARD_B,
                    GoogleVoicePreset.ITALIAN_ITALY_STANDARD_C,
                    GoogleVoicePreset.ITALIAN_ITALY_STANDARD_D,
                    GoogleVoicePreset.ITALIAN_ITALY_STANDARD_E,
                    GoogleVoicePreset.ITALIAN_ITALY_STANDARD_F,
                }

            case LanguageEntry.JAPANESE:
                voicePresets = {
                    GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_A,
                    GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_B,
                    GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_C,
                    GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_D,
                }

            case LanguageEntry.KANNADA:
                voicePresets = {
                    GoogleVoicePreset.KANNADA_INDIA_STANDARD_A,
                    GoogleVoicePreset.KANNADA_INDIA_STANDARD_B,
                    GoogleVoicePreset.KANNADA_INDIA_STANDARD_C,
                    GoogleVoicePreset.KANNADA_INDIA_STANDARD_D,
                }

            case LanguageEntry.KOREAN:
                voicePresets = {
                    GoogleVoicePreset.KOREAN_KOREA_STANDARD_A,
                    GoogleVoicePreset.KOREAN_KOREA_STANDARD_B,
                    GoogleVoicePreset.KOREAN_KOREA_STANDARD_C,
                    GoogleVoicePreset.KOREAN_KOREA_STANDARD_D,
                }

            case LanguageEntry.LATVIAN:
                voicePresets = {
                    GoogleVoicePreset.LATVIAN_LATVIA_STANDARD_A,
                    GoogleVoicePreset.LATVIAN_LATVIA_STANDARD_B,
                }

            case LanguageEntry.LITHUANIAN:
                voicePresets = {
                    GoogleVoicePreset.LITHUANIAN_LITHUANIA_STANDARD_A,
                    GoogleVoicePreset.LITHUANIAN_LITHUANIA_STANDARD_B,
                }

            case LanguageEntry.MALAY:
                voicePresets = {
                    GoogleVoicePreset.MALAY_MALAYSIA_STANDARD_A,
                    GoogleVoicePreset.MALAY_MALAYSIA_STANDARD_B,
                    GoogleVoicePreset.MALAY_MALAYSIA_STANDARD_C,
                    GoogleVoicePreset.MALAY_MALAYSIA_STANDARD_D,
                }

            case LanguageEntry.MALAYALAM:
                voicePresets = {
                    GoogleVoicePreset.MALAYALAM_INDIA_STANDARD_A,
                    GoogleVoicePreset.MALAYALAM_INDIA_STANDARD_B,
                    GoogleVoicePreset.MALAYALAM_INDIA_STANDARD_C,
                    GoogleVoicePreset.MALAYALAM_INDIA_STANDARD_D,
                }

            case LanguageEntry.MARATHI:
                voicePresets = {
                    GoogleVoicePreset.MARATHI_INDIA_STANDARD_A,
                    GoogleVoicePreset.MARATHI_INDIA_STANDARD_B,
                    GoogleVoicePreset.MARATHI_INDIA_STANDARD_C,
                }

            case LanguageEntry.NORWEGIAN:
                voicePresets = {
                    GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_A,
                    GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_B,
                    GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_C,
                    GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_D,
                    GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_E,
                    GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_F,
                    GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_G,
                }

            case LanguageEntry.POLISH:
                voicePresets = {
                    GoogleVoicePreset.POLISH_POLAND_STANDARD_A,
                    GoogleVoicePreset.POLISH_POLAND_STANDARD_B,
                    GoogleVoicePreset.POLISH_POLAND_STANDARD_C,
                    GoogleVoicePreset.POLISH_POLAND_STANDARD_D,
                    GoogleVoicePreset.POLISH_POLAND_STANDARD_E,
                    GoogleVoicePreset.POLISH_POLAND_STANDARD_F,
                    GoogleVoicePreset.POLISH_POLAND_STANDARD_G,
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
                    GoogleVoicePreset.PORTUGUESE_PORTUGAL_STANDARD_F,
                }

            case LanguageEntry.PUNJABI:
                voicePresets = {
                    GoogleVoicePreset.PUNJABI_INDIA_STANDARD_A,
                    GoogleVoicePreset.PUNJABI_INDIA_STANDARD_B,
                    GoogleVoicePreset.PUNJABI_INDIA_STANDARD_C,
                    GoogleVoicePreset.PUNJABI_INDIA_STANDARD_D,
                }

            case LanguageEntry.ROMANIAN:
                voicePresets = {
                    GoogleVoicePreset.ROMANIAN_ROMANIA_STANDARD_A,
                    GoogleVoicePreset.ROMANIAN_ROMANIA_STANDARD_B,
                }

            case LanguageEntry.RUSSIAN:
                voicePresets = {
                    GoogleVoicePreset.RUSSIAN_RUSSIA_STANDARD_A,
                    GoogleVoicePreset.RUSSIAN_RUSSIA_STANDARD_B,
                    GoogleVoicePreset.RUSSIAN_RUSSIA_STANDARD_C,
                    GoogleVoicePreset.RUSSIAN_RUSSIA_STANDARD_D,
                    GoogleVoicePreset.RUSSIAN_RUSSIA_STANDARD_E,
                }

            case LanguageEntry.SERBIAN:
                voicePresets = {
                    GoogleVoicePreset.SERBIAN_CYRILLIC_STANDARD_A,
                }

            case LanguageEntry.SLOVAK:
                voicePresets = {
                    GoogleVoicePreset.SLOVAK_SLOVAKIA_STANDARD_A,
                    GoogleVoicePreset.SLOVAK_SLOVAKIA_STANDARD_B,
                }

            case LanguageEntry.SPANISH:
                voicePresets = {
                    GoogleVoicePreset.SPANISH_US_CHIRP_D,
                    GoogleVoicePreset.SPANISH_US_CHIRP_F,
                    GoogleVoicePreset.SPANISH_US_CHIRP_O,
                    GoogleVoicePreset.SPANISH_SPAIN_STANDARD_A,
                    GoogleVoicePreset.SPANISH_SPAIN_STANDARD_B,
                    GoogleVoicePreset.SPANISH_SPAIN_STANDARD_C,
                    GoogleVoicePreset.SPANISH_SPAIN_STANDARD_D,
                    GoogleVoicePreset.SPANISH_SPAIN_STANDARD_E,
                    GoogleVoicePreset.SPANISH_SPAIN_STANDARD_F,
                    GoogleVoicePreset.SPANISH_SPAIN_STANDARD_G,
                    GoogleVoicePreset.SPANISH_SPAIN_STANDARD_H,
                    GoogleVoicePreset.SPANISH_US_STANDARD_A,
                    GoogleVoicePreset.SPANISH_US_STANDARD_B,
                    GoogleVoicePreset.SPANISH_US_STANDARD_C,
                }

            case LanguageEntry.SWEDISH:
                voicePresets = {
                    GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_A,
                    GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_B,
                    GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_C,
                    GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_D,
                    GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_E,
                    GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_F,
                    GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_G,
                }

            case LanguageEntry.TAMIL:
                voicePresets = {
                    GoogleVoicePreset.TAMIL_INDIA_STANDARD_A,
                    GoogleVoicePreset.TAMIL_INDIA_STANDARD_B,
                    GoogleVoicePreset.TAMIL_INDIA_STANDARD_C,
                    GoogleVoicePreset.TAMIL_INDIA_STANDARD_D,
                }

            case LanguageEntry.TELUGU:
                voicePresets = {
                    GoogleVoicePreset.TELUGU_INDIA_STANDARD_A,
                    GoogleVoicePreset.TELUGU_INDIA_STANDARD_B,
                    GoogleVoicePreset.TELUGU_INDIA_STANDARD_C,
                    GoogleVoicePreset.TELUGU_INDIA_STANDARD_D,
                }

            case LanguageEntry.THAI:
                voicePresets = {
                    GoogleVoicePreset.THAI_THAILAND_STANDARD_A,
                }

            case LanguageEntry.TURKISH:
                voicePresets = {
                    GoogleVoicePreset.TURKISH_TURKEY_STANDARD_A,
                    GoogleVoicePreset.TURKISH_TURKEY_STANDARD_B,
                    GoogleVoicePreset.TURKISH_TURKEY_STANDARD_C,
                    GoogleVoicePreset.TURKISH_TURKEY_STANDARD_D,
                    GoogleVoicePreset.TURKISH_TURKEY_STANDARD_E,
                }

            case LanguageEntry.UKRANIAN:
                voicePresets = {
                    GoogleVoicePreset.UKRANIAN_UKRAINE_STANDARD_A,
                }

            case LanguageEntry.VIETNAMESE:
                voicePresets = {
                    GoogleVoicePreset.VIETNAMESE_VIETNAM_STANDARD_A,
                    GoogleVoicePreset.VIETNAMESE_VIETNAM_STANDARD_B,
                    GoogleVoicePreset.VIETNAMESE_VIETNAM_STANDARD_C,
                    GoogleVoicePreset.VIETNAMESE_VIETNAM_STANDARD_D,
                }

            case _:
                voicePresets = set()

        return frozenset(voicePresets)
