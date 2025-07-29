from abc import ABC, abstractmethod


class TwitchTimeoutRemodHelperInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    async def submitRemodData(
        self,
        timeoutDurationSeconds: int,
        broadcasterUserId: str,
        broadcasterUserName: str,
        userId: str,
    ):
        pass
