from enum import Enum, auto


class TtsMonsterWebsiteVoice(Enum):

    BRIAN = auto()
    GERALT = auto()
    HAL_9000 = auto()
    JOHNNY = auto()
    KKONA = auto()
    MEGAN = auto()
    NARRATOR = auto()
    SHADOW = auto()
    ZERO_TWO = auto()

    @property
    def isEnabled(self):
        match self:
            case TtsMonsterWebsiteVoice.BRIAN: return True
            case TtsMonsterWebsiteVoice.GERALT: return False
            case TtsMonsterWebsiteVoice.HAL_9000: return False
            case TtsMonsterWebsiteVoice.JOHNNY: return False
            case TtsMonsterWebsiteVoice.KKONA: return True
            case TtsMonsterWebsiteVoice.MEGAN: return True
            case TtsMonsterWebsiteVoice.NARRATOR: return False
            case TtsMonsterWebsiteVoice.SHADOW: return True
            case TtsMonsterWebsiteVoice.ZERO_TWO: return True
            case _: raise RuntimeError(f'unknown TtsMonsterWebsiteVoice: \"{self}\"')

    @property
    def voiceId(self) -> str:
        match self:
            case TtsMonsterWebsiteVoice.BRIAN: return '0993f688-6719-4cf6-9769-fee7b77b1df5'
            case TtsMonsterWebsiteVoice.GERALT: return 'c5d9224a-60d1-48db-9dfd-3146842a931c'
            case TtsMonsterWebsiteVoice.HAL_9000: return '105e3e7d-ec3e-47a3-a3d3-86345feed23d'
            case TtsMonsterWebsiteVoice.JOHNNY: return '24e1a8ff-e5c7-464f-a708-c4fe92c59b28'
            case TtsMonsterWebsiteVoice.KKONA: return '50570964-9672-4927-ac7d-40575e9112d3'
            case TtsMonsterWebsiteVoice.MEGAN: return '1364bd06-f252-433e-9eac-f9a9a964a77b'
            case TtsMonsterWebsiteVoice.NARRATOR: return '7dfab21a-da07-4474-b7df-dcbbd7c7c69c'
            case TtsMonsterWebsiteVoice.SHADOW: return '67dbd94d-a097-4676-af2f-1db67c1eb8dd'
            case TtsMonsterWebsiteVoice.ZERO_TWO: return '32a369aa-5485-4039-beb6-4c757e93a197'
            case _: raise RuntimeError(f'unknown TtsMonsterWebsiteVoice: \"{self}\"')

    @property
    def websiteName(self) -> str:
        match self:
            case TtsMonsterWebsiteVoice.BRIAN: return 'brian'
            case TtsMonsterWebsiteVoice.GERALT: return 'geralt'
            case TtsMonsterWebsiteVoice.HAL_9000: return 'hal9000'
            case TtsMonsterWebsiteVoice.JOHNNY: return 'johnny'
            case TtsMonsterWebsiteVoice.KKONA: return 'kkona'
            case TtsMonsterWebsiteVoice.MEGAN: return 'megan'
            case TtsMonsterWebsiteVoice.NARRATOR: return 'narrator'
            case TtsMonsterWebsiteVoice.SHADOW: return 'shadow'
            case TtsMonsterWebsiteVoice.ZERO_TWO: return 'zerotwo'
            case _: raise RuntimeError(f'unknown TtsMonsterWebsiteVoice: \"{self}\"')
