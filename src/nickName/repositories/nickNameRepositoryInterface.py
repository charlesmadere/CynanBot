from abc import ABC, abstractmethod

from ..models.nickNameData import NickNameData
from ...misc.clearable import Clearable


class NickNameRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> NickNameData | None:
        pass

    @abstractmethod
    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> NickNameData | None:
        pass

    @abstractmethod
    async def set(
        self,
        chatterUserId: str,
        nickName: str | None,
        twitchChannelId: str,
    ) -> NickNameData | None:
        pass
