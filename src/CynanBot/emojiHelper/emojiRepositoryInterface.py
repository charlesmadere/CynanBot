from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.emojiHelper.emojiInfo import EmojiInfo


class EmojiRepositoryInterface(ABC):

    @abstractmethod
    async def fetchEmojiInfo(self, emoji: Optional[str]) -> Optional[EmojiInfo]:
        pass
