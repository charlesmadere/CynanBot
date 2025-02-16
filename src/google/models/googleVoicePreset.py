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
    SWEDISH_SWEDEN_STANDARD_A = auto()
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
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_A: return 'sv-SE-Standard-A'
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
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_A: return 'sv-SE'
            case GoogleVoicePreset.SWEDISH_SWEDEN_STANDARD_D: return 'sv-SE'
            case _: raise ValueError(f'Unknown GoogleVoicePreset value: \"{self}\"')
