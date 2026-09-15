from abc import ABC, abstractmethod

from .crowdMicrophoneStatusProviderInterface import CrowdMicrophoneStatusProviderInterface
from ..models.crowdMicrophoneStatus import CrowdMicrophoneStatus


class CrowdMicrophoneHelperInterface(CrowdMicrophoneStatusProviderInterface, ABC):

    @abstractmethod
    async def start(
        self,
        durationSeconds: int,
        twitchChannelId: str,
    ) -> CrowdMicrophoneStatus:
        pass
