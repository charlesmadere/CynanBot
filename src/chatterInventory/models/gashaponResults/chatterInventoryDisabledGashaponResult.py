from dataclasses import dataclass

from .absGashaponResult import AbsGashaponResult


@dataclass(frozen = True, slots = True)
class ChatterInventoryDisabledGashaponResult(AbsGashaponResult):
    pass
