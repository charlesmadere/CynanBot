from abc import abstractmethod

from ....misc.clearable import Clearable


class OpenTriviaDatabaseSessionTokenRepositoryInterface(Clearable):

    @abstractmethod
    async def get(self, twitchChannelId: str) -> str | None:
        pass

    @abstractmethod
    async def remove(self, twitchChannelId: str):
        pass

    @abstractmethod
    async def update(self, sessionToken: str | None, twitchChannelId: str):
        pass
