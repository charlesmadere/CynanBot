from abc import ABC, abstractmethod


class CrowdMicrophoneHelperInterface(ABC):

    @abstractmethod
    async def isCurrentlyEnabled(self, twitchChannelId: str) -> bool:
        pass
