from abc import ABC, abstractmethod

from CynanBot.cheerActions.cheerActionBitRequirement import CheerActionBitRequirement
from CynanBot.cheerActions.cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from CynanBot.cheerActions.cheerActionType import CheerActionType


class CheerActionJsonMapperInterface(ABC):

    @abstractmethod
    async def parseCheerActionBitRequirement(
        self,
        jsonString: str | None
    ) -> CheerActionBitRequirement | None:
        pass

    @abstractmethod
    async def parseCheerActionType(
        self,
        jsonString: str | None
    ) -> CheerActionType | None:
        pass

    @abstractmethod
    async def parseCheerActionStreamStatusRequirement(
        self,
        jsonString: str | None
    ) -> CheerActionStreamStatusRequirement | None:
        pass

    @abstractmethod
    async def requireCheerActionBitRequirement(
        self,
        jsonString: str | None
    ) -> CheerActionBitRequirement:
        pass

    @abstractmethod
    async def requireCheerActionStreamStatusRequirement(
        self,
        jsonString: str | None
    ) -> CheerActionStreamStatusRequirement:
        pass

    @abstractmethod
    async def requireCheerActionType(
        self,
        jsonString: str | None
    ) -> CheerActionType:
        pass

    @abstractmethod
    async def serializeCheerActionBitRequirement(
        self,
        bitRequirement: CheerActionBitRequirement
    ) -> str:
        pass

    @abstractmethod
    async def serializeCheerActionStreamStatusRequirement(
        self,
        streamStatusRequirement: CheerActionStreamStatusRequirement
    ) -> str:
        pass

    @abstractmethod
    async def serializeCheerActionType(
        self,
        actionType: CheerActionType
    ) -> str:
        pass
