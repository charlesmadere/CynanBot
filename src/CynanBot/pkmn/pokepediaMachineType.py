from enum import auto

from typing_extensions import override

from CynanBot.misc.enumWithToFromStr import EnumWithToFromStr


class PokepediaMachineType(EnumWithToFromStr):

    HM = auto()
    TM = auto()
    TR = auto()

    def getMaxMachineNumber(self) -> int:
        if self is PokepediaMachineType.HM:
            return 12
        elif self is PokepediaMachineType.TM:
            return 112
        elif self is PokepediaMachineType.TR:
            return 90
        else:
            raise RuntimeError(f'unknown PokepediaMachineType: \"{self}\"')

    @override
    def toStr(self) -> str:
        return super().toStr().upper()
