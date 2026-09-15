from abc import ABC, abstractmethod

from ..models.crowdMicrophoneStatus import CrowdMicrophoneStatus
from ...tts.compositeTtsManagerInterface import CompositeTtsManagerInterface


class CrowdMicrophoneProviderInterface(ABC):

    @abstractmethod
    async def addAssociatedTtsManager(
        self,
        compositeTtsManager: CompositeTtsManagerInterface,
        twitchChannelId: str,
    ):
        pass

    @abstractmethod
    async def getMicrophone(
        self,
        twitchChannelId: str,
    ) -> CrowdMicrophoneStatus | None:
        pass
