from abc import abstractmethod

from .trollmojiDetails import TrollmojiDetails
from ..misc.clearable import Clearable


class TrollmojiSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getGottemEmote(self) -> TrollmojiDetails | None:
        pass

    @abstractmethod
    async def getHypeEmote(self) -> TrollmojiDetails | None:
        pass
