from enum import Enum, auto


class GoogleVoicePreset(Enum):

    ENGLISH_AUSTRALIAN_CHIRP_D = auto()
    ENGLISH_AUSTRALIAN_CHIRP_F = auto()
    ENGLISH_AUSTRALIAN_CHIRP_O = auto()
    ENGLISH_GREAT_BRITAIN_CHIRP_D = auto()
    ENGLISH_GREAT_BRITAIN_CHIRP_F = auto()
    ENGLISH_GREAT_BRITAIN_CHIRP_O = auto()
    FRENCH_CANADA_CHIRP_D = auto()
    FRENCH_CANADA_CHIRP_F = auto()
    FRENCH_CANADA_CHIRP_O = auto()
    GERMAN_GERMANY_CHIRP_D = auto()
    GERMAN_GERMANY_CHIRP_F = auto()
    GERMAN_GERMANY_CHIRP_O = auto()
    ITALIAN_ITALY_CHIRP_D = auto()
    ITALIAN_ITALY_CHIRP_F = auto()
    ITALIAN_ITALY_CHIRP_O = auto()
    JAPANESE_JAPAN_STANDARD_A = auto()
    JAPANESE_JAPAN_STANDARD_B = auto()
    JAPANESE_JAPAN_STANDARD_C = auto()
    JAPANESE_JAPAN_STANDARD_D = auto()
    KOREAN_KOREA_STANDARD_A = auto()
    KOREAN_KOREA_STANDARD_B = auto()
    KOREAN_KOREA_STANDARD_C = auto()
    KOREAN_KOREA_STANDARD_D = auto()
    NORWEGIAN_NORWAY_STANDARD_A = auto()
    NORWEGIAN_NORWAY_STANDARD_B = auto()
    NORWEGIAN_NORWAY_STANDARD_C = auto()
    NORWEGIAN_NORWAY_STANDARD_D = auto()
    NORWEGIAN_NORWAY_STANDARD_E = auto()
    NORWEGIAN_NORWAY_STANDARD_F = auto()
    NORWEGIAN_NORWAY_STANDARD_G = auto()
    PORTUGUESE_BRAZIL_STANDARD_A = auto()
    PORTUGUESE_BRAZIL_STANDARD_B = auto()
    PORTUGUESE_BRAZIL_STANDARD_C = auto()
    PORTUGUESE_BRAZIL_STANDARD_D = auto()
    PORTUGUESE_BRAZIL_STANDARD_E = auto()
    SPANISH_US_CHIRP_D = auto()
    SPANISH_US_CHIRP_F = auto()
    SPANISH_US_CHIRP_O = auto()
    SWEDISH_SWEDEN_STANDARD_A = auto()
    SWEDISH_SWEDEN_STANDARD_B = auto()
    SWEDISH_SWEDEN_STANDARD_C = auto()
    SWEDISH_SWEDEN_STANDARD_D = auto()

    @property
    def fullName(self) -> str:
        match self:
            case GoogleVoicePreset.ENGLISH_AUSTRALIAN_CHIRP_D: return 'en-AU-Chirp-HD-D'
            case GoogleVoicePreset.ENGLISH_AUSTRALIAN_CHIRP_F: return 'en-AU-Chirp-HD-F'
            case GoogleVoicePreset.ENGLISH_AUSTRALIAN_CHIRP_O: return 'en-AU-Chirp-HD-O'
            case GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_D: return 'en-GB-Chirp-HD-D'
            case GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_F: return 'en-GB-Chirp-HD-F'
            case GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_O: return 'en-GB-Chirp-HD-O'
            case GoogleVoicePreset.FRENCH_CANADA_CHIRP_D: return 'fr-CA-Chirp-HD-D'
            case GoogleVoicePreset.FRENCH_CANADA_CHIRP_F: return 'fr-CA-Chirp-HD-F'
            case GoogleVoicePreset.FRENCH_CANADA_CHIRP_O: return 'fr-CA-Chirp-HD-O'
            case GoogleVoicePreset.GERMAN_GERMANY_CHIRP_D: return 'de-DE-Chirp-HD-D'
            case GoogleVoicePreset.GERMAN_GERMANY_CHIRP_F: return 'de-DE-Chirp-HD-F'
            case GoogleVoicePreset.GERMAN_GERMANY_CHIRP_O: return 'de-DE-Chirp-HD-O'
            case GoogleVoicePreset.ITALIAN_ITALY_CHIRP_D: return 'it-IT-Chirp-HD-D'
            case GoogleVoicePreset.ITALIAN_ITALY_CHIRP_F: return 'it-IT-Chirp-HD-F'
            case GoogleVoicePreset.ITALIAN_ITALY_CHIRP_O: return 'it-IT-Chirp-HD-O'
            case GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_A: return 'ja-JP-Standard-A'
            case GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_B: return 'ja-JP-Standard-B'
            case GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_C: return 'ja-JP-Standard-C'
            case GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_D: return 'ja-JP-Standard-D'
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_A: return 'ko-KR-Standard-A'
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_B: return 'ko-KR-Standard-B'
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_C: return 'ko-KR-Standard-C'
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_D: return 'ko-KR-Standard-D'
            case GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_A: return 'nb-NO-Standard-A'
            case GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_B: return 'nb-NO-Standard-B'
            case GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_C: return 'nb-NO-Standard-C'
            case GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_D: return 'nb-NO-Standard-D'
            case GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_E: return 'nb-NO-Standard-E'
            case GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_F: return 'nb-NO-Standard-F'
            case GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_G: return 'nb-NO-Standard-G'
            case GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_A: return 'pt-BR-Standard-A'
            case GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_B: return 'pt-BR-Standard-B'
            case GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_C: return 'pt-BR-Standard-C'
            case GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_D: return 'pt-BR-Standard-D'
            case GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_E: return 'pt-BR-Standard-E'
            case GoogleVoicePreset.SPANISH_US_CHIRP_D: return 'es-US-Chirp-HD-D'
            case GoogleVoicePreset.SPANISH_US_CHIRP_F: return 'es-US-Chirp-HD-F'
            case GoogleVoicePreset.SPANISH_US_CHIRP_O: return 'es-US-Chirp-HD-O'
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_A: return 'sv-SE-Standard-A'
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_B: return 'sv-SE-Standard-B'
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_C: return 'sv-SE-Standard-C'
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_D: return 'sv-SE-Standard-D'
            case _: raise ValueError(f'Unknown GoogleVoicePreset value: \"{self}\"')

    @property
    def languageCode(self) -> str:
        match self:
            case GoogleVoicePreset.ENGLISH_AUSTRALIAN_CHIRP_D: return 'en-AU'
            case GoogleVoicePreset.ENGLISH_AUSTRALIAN_CHIRP_F: return 'en-AU'
            case GoogleVoicePreset.ENGLISH_AUSTRALIAN_CHIRP_O: return 'en-AU'
            case GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_D: return 'en-GB'
            case GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_F: return 'en-GB'
            case GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_O: return 'en-GB'
            case GoogleVoicePreset.FRENCH_CANADA_CHIRP_D: return 'fr-CA'
            case GoogleVoicePreset.FRENCH_CANADA_CHIRP_F: return 'fr-CA'
            case GoogleVoicePreset.FRENCH_CANADA_CHIRP_O: return 'fr-CA'
            case GoogleVoicePreset.GERMAN_GERMANY_CHIRP_D: return 'de-DE'
            case GoogleVoicePreset.GERMAN_GERMANY_CHIRP_F: return 'de-DE'
            case GoogleVoicePreset.GERMAN_GERMANY_CHIRP_O: return 'de-DE'
            case GoogleVoicePreset.ITALIAN_ITALY_CHIRP_D: return 'it-IT'
            case GoogleVoicePreset.ITALIAN_ITALY_CHIRP_F: return 'it-IT'
            case GoogleVoicePreset.ITALIAN_ITALY_CHIRP_O: return 'it-IT'
            case GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_A: return 'ja-JP'
            case GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_B: return 'ja-JP'
            case GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_C: return 'ja-JP'
            case GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_D: return 'ja-JP'
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_A: return 'ko-KR'
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_B: return 'ko-KR'
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_C: return 'ko-KR'
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_D: return 'ko-KR'
            case GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_A: return 'nb-NO'
            case GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_B: return 'nb-NO'
            case GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_C: return 'nb-NO'
            case GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_D: return 'nb-NO'
            case GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_E: return 'nb-NO'
            case GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_F: return 'nb-NO'
            case GoogleVoicePreset.NORWEGIAN_NORWAY_STANDARD_G: return 'nb-NO'
            case GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_A: return 'pt-BR'
            case GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_B: return 'pt-BR'
            case GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_C: return 'pt-BR'
            case GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_D: return 'pt-BR'
            case GoogleVoicePreset.PORTUGUESE_BRAZIL_STANDARD_E: return 'pt-BR'
            case GoogleVoicePreset.SPANISH_US_CHIRP_D: return 'es-US'
            case GoogleVoicePreset.SPANISH_US_CHIRP_F: return 'es-US'
            case GoogleVoicePreset.SPANISH_US_CHIRP_O: return 'es-US'
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_A: return 'sv-SE'
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_B: return 'sv-SE'
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_C: return 'sv-SE'
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_D: return 'sv-SE'
            case _: raise ValueError(f'Unknown GoogleVoicePreset value: \"{self}\"')
