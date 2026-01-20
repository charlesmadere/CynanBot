from dataclasses import dataclass

from .pokepediaGeneration import PokepediaGeneration
from .pokepediaMachineType import PokepediaMachineType


@dataclass(frozen = True, slots = True)
class PokepediaMachine:
    machineId: int
    machineNumber: int
    generation: PokepediaGeneration
    machineType: PokepediaMachineType
    machineName: str
    moveName: str
