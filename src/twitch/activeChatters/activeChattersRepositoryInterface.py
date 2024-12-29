from abc import ABC, abstractmethod
from typing import Collection

from .activeChatter import ActiveChatter


class ActiveChattersRepositoryInterface(ABC):

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
        twitchChannelId: str,
        count: int | None = None
    ) -> Collection[ActiveChatter]:
        pass

    @abstractmethod
    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ):
        pass
