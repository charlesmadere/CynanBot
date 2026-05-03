from abc import ABC, abstractmethod

from .emojiData import EmojiData


class EmojiRepositoryInterface(ABC):

    @abstractmethod
    async def fetchEmojiData(self, emoji: str | None) -> EmojiData | None:
        pass
