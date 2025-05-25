from abc import ABC, abstractmethod

from frozenlist import FrozenList

from ..models.addVoicemailResult import AddVoicemailResult
from ..models.voicemailData import VoicemailData


class VoicemailHelperInterface(ABC):

    @abstractmethod
    async def addVoicemail(
        self,
        message: str | None,
        originatingUserId: str,
        targetUserId: str,
        twitchChannelId: str
    ) -> AddVoicemailResult:
        pass

    @abstractmethod
    async def getAllForOriginatingUser(
        self,
        originatingUserId: str,
        twitchChannelId: str
    ) -> FrozenList[VoicemailData]:
        pass

    @abstractmethod
    async def getAllForTargetUser(
        self,
        targetUserId: str,
        twitchChannelId: str
    ) -> FrozenList[VoicemailData]:
        pass

    @abstractmethod
    async def getAndRemoveForTargetUser(
        self,
        targetUserId: str,
        twitchChannelId: str
    ) -> VoicemailData | None:
        pass
