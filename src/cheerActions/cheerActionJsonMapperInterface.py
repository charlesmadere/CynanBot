from abc import ABC, abstractmethod

from .absCheerAction import AbsCheerAction
from .beanChanceCheerAction import BeanChanceCheerAction
from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from .crowdControl.crowdControlCheerAction import CrowdControlCheerAction
from .crowdControl.crowdControlCheerActionType import CrowdControlCheerActionType
from .soundAlertCheerAction import SoundAlertCheerAction
from .timeoutCheerAction import TimeoutCheerAction


class CheerActionJsonMapperInterface(ABC):

    @abstractmethod
    async def parseBeanChanceCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> BeanChanceCheerAction | None:
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
    async def parseCrowdControlCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> CrowdControlCheerAction | None:
        pass

    @abstractmethod
    async def parseCrowdControlCheerActionType(
        self,
        jsonString: str | None
    ) -> CrowdControlCheerActionType | None:
        pass

    @abstractmethod
    async def parseSoundAlertCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> SoundAlertCheerAction | None:
        pass

    @abstractmethod
    async def parseTimeoutCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> TimeoutCheerAction | None:
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
    async def requireCrowdControlCheerActionType(
        self,
        jsonString: str | None
    ) -> CrowdControlCheerActionType:
        pass

    @abstractmethod
    async def serializeAbsCheerAction(
        self,
        cheerAction: AbsCheerAction
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

    @abstractmethod
    async def serializeCrowdControlCheerActionType(
        self,
        actionType: CrowdControlCheerActionType
    ) -> str:
        pass
