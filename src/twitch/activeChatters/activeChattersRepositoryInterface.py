from abc import ABC, abstractmethod
from typing import Collection

from .activeChatter import ActiveChatter
from ...misc.clearable import Clearable


class ActiveChattersRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def add(
        self,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannelId: str
    ):
        pass

    @abstractmethod
    async def get(
        self,
        twitchChannelId: str
    ) -> Collection[ActiveChatter]:
        pass

    @abstractmethod
    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ):
        pass
