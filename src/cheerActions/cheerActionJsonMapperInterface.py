from abc import ABC, abstractmethod
from typing import Any

from .absCheerAction import AbsCheerAction
from .adge.adgeCheerAction import AdgeCheerAction
from .airStrike.airStrikeCheerAction import AirStrikeCheerAction
from .beanChance.beanChanceCheerAction import BeanChanceCheerAction
from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from .crowdControl.crowdControlButtonPressCheerAction import CrowdControlButtonPressCheerAction
from .crowdControl.crowdControlGameShuffleCheerAction import CrowdControlGameShuffleCheerAction
from .soundAlert.soundAlertCheerAction import SoundAlertCheerAction
from .timeout.timeoutCheerAction import TimeoutCheerAction
from .timeout.timeoutCheerActionTargetType import TimeoutCheerActionTargetType
from .voicemail.voicemailCheerAction import VoicemailCheerAction


class CheerActionJsonMapperInterface(ABC):

    @abstractmethod
    async def parseAdgeCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> AdgeCheerAction | None:
        pass

    @abstractmethod
    async def parseAirStrikeCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> AirStrikeCheerAction | None:
        pass

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
        jsonString: str | Any | None
    ) -> CheerActionType | None:
        pass

    @abstractmethod
    async def parseCheerActionStreamStatusRequirement(
        self,
        jsonString: str | Any | None
    ) -> CheerActionStreamStatusRequirement | None:
        pass

    @abstractmethod
    async def parseCrowdControlButtonPressCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> CrowdControlButtonPressCheerAction | None:
        pass

    @abstractmethod
    async def parseCrowdControlGameShuffleCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> CrowdControlGameShuffleCheerAction | None:
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
    async def parseTimeoutCheerActionTargetType(
        self,
        string: str | Any | None
    ) -> TimeoutCheerActionTargetType | None:
        pass

    @abstractmethod
    async def parseVoicemailCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> VoicemailCheerAction | None:
        pass

    @abstractmethod
    async def requireAdgeCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> AdgeCheerAction:
        pass

    @abstractmethod
    async def requireAirStrikeCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> AirStrikeCheerAction:
        pass

    @abstractmethod
    async def requireBeanChanceCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> BeanChanceCheerAction:
        pass

    @abstractmethod
    async def requireCheerActionStreamStatusRequirement(
        self,
        jsonString: str | Any | None
    ) -> CheerActionStreamStatusRequirement:
        pass

    @abstractmethod
    async def requireCheerActionType(
        self,
        jsonString: str | Any | None
    ) -> CheerActionType:
        pass

    @abstractmethod
    async def requireCrowdControlButtonPressCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> CrowdControlButtonPressCheerAction:
        pass

    @abstractmethod
    async def requireCrowdControlGameShuffleCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> CrowdControlGameShuffleCheerAction:
        pass

    @abstractmethod
    async def requireSoundAlertCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> SoundAlertCheerAction:
        pass

    @abstractmethod
    async def requireTimeoutCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> TimeoutCheerAction:
        pass

    @abstractmethod
    async def requireTimeoutCheerActionTargetType(
        self,
        string: str | Any | None
    ) -> TimeoutCheerActionTargetType:
        pass

    @abstractmethod
    async def requireVoicemailCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> VoicemailCheerAction:
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
    async def serializeTimeoutCheerActionTargetType(
        self,
        targetType: TimeoutCheerActionTargetType
    ) -> str:
        pass
