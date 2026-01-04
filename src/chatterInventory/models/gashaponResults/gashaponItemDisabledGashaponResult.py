from dataclasses import dataclass

from .absGashaponResult import AbsGashaponResult


@dataclass(frozen = True)
class GashaponItemDisabledGashaponResult(AbsGashaponResult):
    pass
