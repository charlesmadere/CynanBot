from abc import ABC, abstractmethod

from ..models.crowdMicrophoneStatus import CrowdMicrophoneStatus


class CrowdMicrophoneStatusProviderInterface(ABC):

    @abstractmethod
    async def getMicrophone(
        self,
        twitchChannelId: str,
    ) -> CrowdMicrophoneStatus | None:
        pass
