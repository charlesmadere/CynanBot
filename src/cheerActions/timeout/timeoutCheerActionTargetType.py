from enum import Enum, auto


class TimeoutCheerActionTargetType(Enum):

    ANY = auto()
    RANDOM_ONLY = auto()
    SPECIFIC_TARGET_ONLY = auto()

    @property
    def humanName(self) -> str:
        match self:
            case TimeoutCheerActionTargetType.ANY: return 'any'
            case TimeoutCheerActionTargetType.RANDOM_ONLY: return 'random only'
            case TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY: return 'specific target only'
            case _: raise ValueError(f'Unknown TimeoutCheerActionTargetType value: \"{self}\"')
