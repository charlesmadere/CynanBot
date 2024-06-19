from abc import ABC, abstractmethod

from CynanBot.cheerActions.cheerActionType import CheerActionType


class CheerActionJsonMapperInterface(ABC):

    @abstractmethod
    async def parseCheerActionType(
        self,
        jsonString: str | None
    ) -> CheerActionType | None:
        pass

    @abstractmethod
    async def requireCheerActionType(
        self,
        jsonString: str | None
    ) -> CheerActionType:
        pass

    @abstractmethod
    async def serializeCheerActionType(
        self,
        actionType: CheerActionType
    ) -> str:
        pass
