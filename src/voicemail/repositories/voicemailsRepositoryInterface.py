from abc import ABC, abstractmethod

from frozenlist import FrozenList

from ..models.addVoicemailResult import AddVoicemailResult
from ..models.removeVoicemailResult import RemoveVoicemailResult
from ..models.voicemailData import VoicemailData
from ...misc.clearable import Clearable
from ...tts.models.ttsProvider import TtsProvider


class VoicemailsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def addVoicemail(
        self,
        message: str,
        originatingUserId: str,
        targetUserId: str,
        twitchChannelId: str,
        ttsProvider: TtsProvider | None
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
    async def getForTargetUser(
        self,
        targetUserId: str,
        twitchChannelId: str
    ) -> VoicemailData | None:
        pass

    @abstractmethod
    async def removeVoicemail(
        self,
        twitchChannelId: str,
        voicemailId: str
    ) -> RemoveVoicemailResult:
        pass
