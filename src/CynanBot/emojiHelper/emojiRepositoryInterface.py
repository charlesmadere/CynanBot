from abc import ABC, abstractmethod

from CynanBot.emojiHelper.emojiInfo import EmojiInfo


class EmojiRepositoryInterface(ABC):

    @abstractmethod
    async def fetchEmojiInfo(self, emoji: str | None) -> EmojiInfo | None:
        pass
