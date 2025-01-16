from abc import ABC, abstractmethod


class TwitchConnectionReadinessProvider(ABC):

    @abstractmethod
    async def waitForReady(self):
        pass
