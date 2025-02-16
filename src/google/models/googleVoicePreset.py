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
    KOREAN_KOREA_STANDARD_A = auto()
    KOREAN_KOREA_STANDARD_B = auto()
    KOREAN_KOREA_STANDARD_C = auto()
    KOREAN_KOREA_STANDARD_D = auto()
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
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_A: return 'ko-KR-Standard-A'
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_B: return 'ko-KR-Standard-B'
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_C: return 'ko-KR-Standard-C'
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_D: return 'ko-KR-Standard-D'
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
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_A: return 'ko-KR'
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_B: return 'ko-KR'
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_C: return 'ko-KR'
            case GoogleVoicePreset.KOREAN_KOREA_STANDARD_D: return 'ko-KR'
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_A: return 'sv-SE'
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_B: return 'sv-SE'
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_C: return 'sv-SE'
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_D: return 'sv-SE'
            case _: raise ValueError(f'Unknown GoogleVoicePreset value: \"{self}\"')
