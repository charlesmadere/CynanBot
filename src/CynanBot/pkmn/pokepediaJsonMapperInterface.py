from abc import ABC, abstractmethod

from CynanBot.pkmn.pokepediaBerryFlavor import PokepediaBerryFlavor
from CynanBot.pkmn.pokepediaMachineType import PokepediaMachineType


class PokepediaJsonMapperInterface(ABC):

    @abstractmethod
    async def parseBerryFlavor(
        self,
        jsonNumber: int | None
    ) -> PokepediaBerryFlavor | None:
        pass

    @abstractmethod
    async def parseMachineType(
        self,
        machineTypeString: str | None
    ) -> PokepediaMachineType | None:
        pass

    @abstractmethod
    async def requireBerryFlavor(
        self,
        jsonNumber: int | None
    ) -> PokepediaBerryFlavor:
        pass

    @abstractmethod
    async def requireMachineType(
        self,
        machineTypeString: str | None
    ) -> PokepediaMachineType:
        pass
