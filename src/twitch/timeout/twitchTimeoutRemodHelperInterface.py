from abc import ABC, abstractmethod

from ...misc.startable import Startable


class TwitchTimeoutRemodHelperInterface(Startable, ABC):

    @abstractmethod
    async def submitRemodData(
        self,
        timeoutDurationSeconds: int,
        broadcasterUserId: str,
        userId: str,
    ):
        pass
