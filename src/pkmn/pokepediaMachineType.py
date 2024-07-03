from enum import Enum, auto


class PokepediaMachineType(Enum):

    HM = auto()
    TM = auto()
    TR = auto()

    def getMaxMachineNumber(self) -> int:
        match self:
            case PokepediaMachineType.HM: return 12
            case PokepediaMachineType.TM: return 112
            case PokepediaMachineType.TR: return 90
            case _: raise RuntimeError(f'unknown PokepediaMachineType: \"{self}\"')

    def toStr(self) -> str:
        match self:
            case PokepediaMachineType.HM: return 'HM'
            case PokepediaMachineType.TM: return 'TM'
            case PokepediaMachineType.TR: return 'TR'
            case _: raise RuntimeError(f'unknown PokepediaMachineType: \"{self}\"')
