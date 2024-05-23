from abc import ABC, abstractmethod

from CynanBot.funtoon.funtoonPkmnCatchType import FuntoonPkmnCatchType


class FuntoonJsonMapperInterface(ABC):

    @abstractmethod
    async def serializePkmnCatchType(
        self,
        pkmnCatchType: FuntoonPkmnCatchType
    ) -> str:
        pass
