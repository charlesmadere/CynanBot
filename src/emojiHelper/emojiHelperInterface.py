from abc import ABC, abstractmethod

from .emojiData import EmojiData


class EmojiHelperInterface(ABC):

    @abstractmethod
    async def getHumanNameForEmoji(self, emoji: str | None) -> str | None:
        pass

    @abstractmethod
    async def getRandomFoodAndDrinkEmoji(self) -> EmojiData:
        pass

    @abstractmethod
    async def replaceEmojisWithHumanNames(self, text: str) -> str:
        pass
