from abc import ABC, abstractmethod
from typing import Collection

from .emojiData import EmojiData


class EmojiRepositoryInterface(ABC):

    @abstractmethod
    async def fetchEmojiCategory(self, category: str) -> Collection[EmojiData]:
        pass

    @abstractmethod
    async def fetchEmojiData(self, emoji: str | None) -> EmojiData | None:
        pass
