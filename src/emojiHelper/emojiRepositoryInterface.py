from abc import ABC, abstractmethod
from typing import Collection

from .emojiData import EmojiData


class EmojiRepositoryInterface(ABC):

    @abstractmethod
    async def fetchEmojiCategory(
        self,
        category: str,
        subCategory: str | None = None,
    ) -> Collection[EmojiData]:
        pass

    @abstractmethod
    async def fetchEmojiData(
        self,
        emoji: str | None,
    ) -> EmojiData | None:
        pass
