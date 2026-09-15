from abc import ABC, abstractmethod

from .crowdMicrophoneStatusProviderInterface import CrowdMicrophoneStatusProviderInterface
from ..models.crowdMicrophoneStatus import CrowdMicrophoneStatus
from ..models.useChatterItemAction import UseChatterItemAction


class CrowdMicrophoneHelperInterface(CrowdMicrophoneStatusProviderInterface, ABC):

    @abstractmethod
    async def getAllDeadMicrophones(self) -> frozenset[CrowdMicrophoneStatus]:
        pass

    @abstractmethod
    async def removeMicrophone(
        self,
        twitchChannelId: str,
    ) -> CrowdMicrophoneStatus | None:
        pass

    @abstractmethod
    async def startMicrophone(
        self,
        durationSeconds: int,
        originatingAction: UseChatterItemAction,
    ) -> CrowdMicrophoneStatus:
        pass
