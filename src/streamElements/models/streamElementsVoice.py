from enum import Enum, auto


class StreamElementsVoice(Enum):

    BRIAN = auto()
    JOEY = auto()

    @property
    def urlValue(self) -> str:
        match self:
            case StreamElementsVoice.BRIAN: return 'Brian'
            case StreamElementsVoice.JOEY: return 'Joey'
            case _: raise RuntimeError(f'unknown StreamElementsVoice: \"{self}\"')
