from abc import ABC, abstractmethod

from .crowdMicrophoneProviderInterface import CrowdMicrophoneProviderInterface
from ..models.crowdMicrophoneStatus import CrowdMicrophoneStatus
from ..models.useChatterItemAction import UseChatterItemAction


class CrowdMicrophoneHelperInterface(CrowdMicrophoneProviderInterface, ABC):

    @abstractmethod
    async def getAllDeadMicrophones(self) -> frozenset[CrowdMicrophoneStatus]:
        pass

    @abstractmethod
    async def startMicrophone(
        self,
        durationSeconds: int,
        originatingAction: UseChatterItemAction,
    ) -> CrowdMicrophoneStatus:
        pass

    @abstractmethod
    async def stopMicrophone(
        self,
        twitchChannelId: str,
    ) -> CrowdMicrophoneStatus | None:
        pass
