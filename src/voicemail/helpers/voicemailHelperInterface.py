from abc import ABC, abstractmethod

from frozenlist import FrozenList

from ..models.addVoicemailResult import AddVoicemailResult
from ..models.preparedVoicemailData import PreparedVoicemailData


class VoicemailHelperInterface(ABC):

    @abstractmethod
    async def addVoicemail(
        self,
        message: str | None,
        originatingUserId: str,
        targetUserId: str,
        twitchChannelId: str,
    ) -> AddVoicemailResult:
        pass

    @abstractmethod
    async def getAllForOriginatingUser(
        self,
        originatingUserId: str,
        twitchChannelId: str,
    ) -> FrozenList[PreparedVoicemailData]:
        pass

    @abstractmethod
    async def getAllForTargetUser(
        self,
        targetUserId: str,
        twitchChannelId: str,
    ) -> FrozenList[PreparedVoicemailData]:
        pass

    @abstractmethod
    async def popForTargetUser(
        self,
        targetUserId: str,
        twitchChannelId: str,
    ) -> PreparedVoicemailData | None:
        pass
