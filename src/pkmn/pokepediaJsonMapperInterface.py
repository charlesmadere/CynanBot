from abc import ABC, abstractmethod

from .pokepediaBerryFlavor import PokepediaBerryFlavor
from .pokepediaMachineType import PokepediaMachineType


class PokepediaJsonMapperInterface(ABC):

    @abstractmethod
    async def parseBerryFlavor(
        self,
        jsonNumber: int | None
    ) -> PokepediaBerryFlavor | None:
        pass

    @abstractmethod
    async def parseMachineNumber(
        self,
        machineNumberString: str | None
    ) -> int | None:
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
    async def requireMachineNumber(
        self,
        machineNumberString: str | None
    ) -> int:
        pass

    @abstractmethod
    async def requireMachineType(
        self,
        machineTypeString: str | None
    ) -> PokepediaMachineType:
        pass
