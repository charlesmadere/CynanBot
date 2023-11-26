from abc import ABC, abstractmethod
from typing import Optional


class EmojiHelperInterface(ABC):

    @abstractmethod
    async def getHumanNameForEmoji(self, emoji: Optional[str]) -> Optional[str]:
        pass

    @abstractmethod
    async def replaceEmojisWithHumanNames(self, text: str) -> str:
        pass
