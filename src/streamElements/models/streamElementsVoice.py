from enum import Enum, auto


class StreamElementsVoice(Enum):

    AMY = auto()
    BRIAN = auto()
    JOEY = auto()

    @property
    def humanName(self) -> str:
        match self:
            case StreamElementsVoice.AMY: return 'Amy'
            case StreamElementsVoice.BRIAN: return 'Brian'
            case StreamElementsVoice.JOEY: return 'Joey'
            case _: raise RuntimeError(f'unknown StreamElementsVoice: \"{self}\"')

    @property
    def urlValue(self) -> str:
        match self:
            case StreamElementsVoice.AMY: return 'Amy'
            case StreamElementsVoice.BRIAN: return 'Brian'
            case StreamElementsVoice.JOEY: return 'Joey'
            case _: raise RuntimeError(f'unknown StreamElementsVoice: \"{self}\"')
