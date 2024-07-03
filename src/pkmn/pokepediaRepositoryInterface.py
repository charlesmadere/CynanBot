from abc import ABC, abstractmethod

from .pokepediaGeneration import PokepediaGeneration
from .pokepediaMachine import PokepediaMachine
from .pokepediaMove import PokepediaMove
from .pokepediaNature import PokepediaNature
from .pokepediaPokemon import PokepediaPokemon
from .pokepediaStat import PokepediaStat


class PokepediaRepositoryInterface(ABC):

    @abstractmethod
    async def fetchMachine(self, machineId: int) -> PokepediaMachine:
        pass

    @abstractmethod
    async def fetchMove(self, moveId: int) -> PokepediaMove:
        pass

    @abstractmethod
    async def fetchNature(self, natureId: int) -> PokepediaNature:
        pass

    @abstractmethod
    async def fetchRandomMove(self, maxGeneration: PokepediaGeneration) -> PokepediaMove:
        pass

    @abstractmethod
    async def fetchRandomNature(self) -> PokepediaNature:
        pass

    @abstractmethod
    async def fetchRandomPokemon(self, maxGeneration: PokepediaGeneration) -> PokepediaPokemon:
        pass

    @abstractmethod
    async def fetchRandomStat(self) -> PokepediaStat:
        pass

    @abstractmethod
    async def fetchStat(self, statId: int) -> PokepediaStat:
        pass

    @abstractmethod
    async def searchMoves(self, name: str) -> PokepediaMove:
        pass

    @abstractmethod
    async def searchPokemon(self, name: str) -> PokepediaPokemon:
        pass
