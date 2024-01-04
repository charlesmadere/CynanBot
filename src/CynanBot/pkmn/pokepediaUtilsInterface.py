from abc import ABC, abstractmethod


class PokepediaUtilsInterface(ABC):

    @abstractmethod
    async def getMachineNumber(self, machineName: str) -> int:
        pass
