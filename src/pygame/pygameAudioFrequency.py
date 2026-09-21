from enum import Enum, auto


class PygameAudioFrequency(Enum):

    FORTY_FOUR_KHZ = auto()
    FORTY_EIGHT_KHZ = auto()

    @property
    def hzValue(self) -> int:
        match self:
            case PygameAudioFrequency.FORTY_FOUR_KHZ: return 44100
            case PygameAudioFrequency.FORTY_EIGHT_KHZ: return 48000
