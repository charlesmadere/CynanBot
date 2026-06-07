import random
from typing import Final

import emoji
from frozenlist import FrozenList

from .emojiData import EmojiData
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

        emojiData = await self.__emojiRepository.fetchEmojiData(
            emoji = emoji,
        )

        if emojiData is None:
            return None
        else:
            return emojiData.name

    async def getRandomFoodAndDrinkEmoji(self) -> EmojiData:
        allFoodAndDrinkEmoji = await self.__emojiRepository.fetchEmojiCategory(
            category = 'Food & Drink',
        )

        frozenFoodAndDrinkEmoji: FrozenList[EmojiData] = FrozenList(allFoodAndDrinkEmoji)
        frozenFoodAndDrinkEmoji.freeze()

        if len(frozenFoodAndDrinkEmoji) == 0:
            raise RuntimeError(f'Failed to find any \"Food & Drink\" emoji: ({frozenFoodAndDrinkEmoji=})')

        return random.choice(frozenFoodAndDrinkEmoji)

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
                humanName = await self.getHumanNameForEmoji(
                    emoji = distinctEmoji,
                )

                if humanName is not None:
                    replacementString = f'{replacementString} {humanName}'

            splits[index] = replacementString
            replacementMade = True

        if replacementMade:
            return ' '.join(splits).strip()
        else:
            return text
