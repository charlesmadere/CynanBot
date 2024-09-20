from abc import abstractmethod

from ...misc.clearable import Clearable


class StreamElementsUserKeyRepositoryInterface(Clearable):

    @abstractmethod
    async def get(self, twitchChannelId: str) -> str | None:
        pass

    @abstractmethod
    async def set(self, userKey: str | None, twitchChannelId: str):
        pass
