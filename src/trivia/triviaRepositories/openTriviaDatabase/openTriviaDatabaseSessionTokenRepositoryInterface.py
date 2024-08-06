from abc import ABC, abstractmethod


class OpenTriviaDatabaseSessionTokenRepositoryInterface(ABC):

    @abstractmethod
    async def get(
        self,
        twitchChannelId: str
    ) -> str | None:
        pass

    @abstractmethod
    async def set(
        self,
        sessionToken: str | None,
        twitchChannelId: str
    ):
        pass
