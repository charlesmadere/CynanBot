from enum import Enum, auto


class TtsMonsterWebsiteVoice(Enum):

    BRIAN = auto()
    GERALT = auto()
    HAL_9000 = auto()
    JAZZ = auto()
    JOHNNY = auto()
    KKONA = auto()
    MEGAN = auto()
    MORGAN = auto()
    NARRATOR = auto()
    OBI_WAN = auto()
    SHADOW = auto()
    SPONGEBOB = auto()
    SQUIDWARD = auto()
    ZERO_TWO = auto()

    @property
    def voiceId(self) -> str:
        match self:
            case TtsMonsterWebsiteVoice.BRIAN: return '0993f688-6719-4cf6-9769-fee7b77b1df5'
            case TtsMonsterWebsiteVoice.GERALT: return 'c5d9224a-60d1-48db-9dfd-3146842a931c'
            case TtsMonsterWebsiteVoice.HAL_9000: return '105e3e7d-ec3e-47a3-a3d3-86345feed23d'
            case TtsMonsterWebsiteVoice.JAZZ: return '1faab65c-c489-45ba-b302-b22d9e491d9f'
            case TtsMonsterWebsiteVoice.JOHNNY: return '24e1a8ff-e5c7-464f-a708-c4fe92c59b28'
            case TtsMonsterWebsiteVoice.KKONA: return '50570964-9672-4927-ac7d-40575e9112d3'
            case TtsMonsterWebsiteVoice.MEGAN: return '1364bd06-f252-433e-9eac-f9a9a964a77b'
            case TtsMonsterWebsiteVoice.MORGAN: return 'e0f1c6e2-fbb2-4df4-9ec2-f1109371ab1e'
            case TtsMonsterWebsiteVoice.NARRATOR: return '7dfab21a-da07-4474-b7df-dcbbd7c7c69c'
            case TtsMonsterWebsiteVoice.OBI_WAN: return '5dbb63c3-1179-4704-90cf-8dbe0d9b33ab'
            case TtsMonsterWebsiteVoice.SHADOW: return '67dbd94d-a097-4676-af2f-1db67c1eb8dd'
            case TtsMonsterWebsiteVoice.SPONGEBOB: return 'faa92dd8-0517-49da-8f01-1fb03f0e0096'
            case TtsMonsterWebsiteVoice.SQUIDWARD: return '7cbd44df-08ac-4234-bc95-836e0ae6b22c'
            case TtsMonsterWebsiteVoice.ZERO_TWO: return '32a369aa-5485-4039-beb6-4c757e93a197'
            case _: raise RuntimeError(f'unknown TtsMonsterWebsiteVoice: \"{self}\"')

    @property
    def websiteName(self) -> str:
        match self:
            case TtsMonsterWebsiteVoice.BRIAN: return 'brian'
            case TtsMonsterWebsiteVoice.GERALT: return 'geralt'
            case TtsMonsterWebsiteVoice.HAL_9000: return 'hal9000'
            case TtsMonsterWebsiteVoice.JAZZ: return 'jazz'
            case TtsMonsterWebsiteVoice.JOHNNY: return 'johnny'
            case TtsMonsterWebsiteVoice.KKONA: return 'kkona'
            case TtsMonsterWebsiteVoice.MEGAN: return 'megan'
            case TtsMonsterWebsiteVoice.MORGAN: return 'morgan'
            case TtsMonsterWebsiteVoice.NARRATOR: return 'narrator'
            case TtsMonsterWebsiteVoice.OBI_WAN: return 'obiwan'
            case TtsMonsterWebsiteVoice.SHADOW: return 'shadow'
            case TtsMonsterWebsiteVoice.SPONGEBOB: return 'spongebob'
            case TtsMonsterWebsiteVoice.SQUIDWARD: return 'squidward'
            case TtsMonsterWebsiteVoice.ZERO_TWO: return 'zerotwo'
            case _: raise RuntimeError(f'unknown TtsMonsterWebsiteVoice: \"{self}\"')
