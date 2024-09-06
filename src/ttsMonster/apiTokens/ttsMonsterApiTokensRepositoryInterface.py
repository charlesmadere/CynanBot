from abc import abstractmethod

from ...misc.clearable import Clearable


class TtsMonsterApiTokensRepositoryInterface(Clearable):

    @abstractmethod
    async def get(self, twitchChannelId: str) -> str | None:
        pass

    @abstractmethod
    async def set(self, apiToken: str | None, twitchChannelId: str):
        pass
