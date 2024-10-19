from abc import abstractmethod

from ..misc.clearable import Clearable


class TrollmojiSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getGottemEmote(self) -> str | None:
        pass

    @abstractmethod
    async def getHypeEmote(self) -> str | None:
        pass
