from typing import Final

import emoji

from .emojiHelperInterface import EmojiHelperInterface
from .emojiRepositoryInterface import EmojiRepositoryInterface
from ..misc import utils as utils


class EmojiHelper(EmojiHelperInterface):

    def __init__(
        self,
        emojiRepository: EmojiRepositoryInterface,
    ):
        if not isinstance(emojiRepository, EmojiRepositoryInterface):
            raise TypeError(f'emojiRepository argument is malformed: \"{emojiRepository}\"')

        self.__emojiRepository: Final[EmojiRepositoryInterface] = emojiRepository

    async def getHumanNameForEmoji(self, emoji: str | None) -> str | None:
        if not utils.isValidStr(emoji):
            return None

        emojiInfo = await self.__emojiRepository.fetchEmojiInfo(emoji)

        if emojiInfo is None:
            return None
        else:
            return emojiInfo.name

    async def replaceEmojisWithHumanNames(self, text: str) -> str:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        splits = utils.getCleanedSplits(text)

        if len(splits) == 0:
            return text

        replacementMade = False

        for index, split in enumerate(splits):
            distinctEmojis = emoji.distinct_emoji_list(split)

            if distinctEmojis is None or len(distinctEmojis) == 0:
                continue

            replacementString = ''

            for distinctEmoji in distinctEmojis:
                humanName = await self.getHumanNameForEmoji(distinctEmoji)

                if humanName is not None:
                    replacementString = f'{replacementString} {humanName}'

            splits[index] = replacementString
            replacementMade = True

        if replacementMade:
            return ' '.join(splits).strip()
        else:
            return text
