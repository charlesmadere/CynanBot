from abc import ABC, abstractmethod

from CynanBot.pkmn.pokepediaBerryFlavor import PokepediaBerryFlavor


class PokepediaJsonMapperInterface(ABC):

    @abstractmethod
    async def parseBerryFlavor(
        self,
        jsonNumber: int | None
    ) -> PokepediaBerryFlavor | None:
        pass

    @abstractmethod
    async def requireBerryFlavor(
        self,
        jsonNumber: int | None
    ) -> PokepediaBerryFlavor:
        pass
