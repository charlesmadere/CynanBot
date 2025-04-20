from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class TtsChatterRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def add(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ):
        pass

    @abstractmethod
    async def isTtsChatter(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> bool:
        pass

    @abstractmethod
    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> bool:
        pass
