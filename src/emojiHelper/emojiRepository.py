import traceback
from typing import Any, Collection, Final

from frozenlist import FrozenList

from .emojiData import EmojiData
from .emojiRepositoryInterface import EmojiRepositoryInterface
from ..misc import utils as utils
from ..storage.jsonReaderInterface import JsonReaderInterface
from ..timber.timberInterface import TimberInterface


class EmojiRepository(EmojiRepositoryInterface):

    def __init__(
        self,
        emojiJsonReader: JsonReaderInterface,
        timber: TimberInterface,
    ):
        if not isinstance(emojiJsonReader, JsonReaderInterface):
            raise TypeError(f'emojiJsonReader argument is malformed: \"{emojiJsonReader}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__emojiJsonReader: Final[JsonReaderInterface] = emojiJsonReader
        self.__timber: Final[TimberInterface] = timber

        self.__isLoaded: bool = False
        self.__emojiData: Final[dict[str, EmojiData | None]] = dict()

    async def fetchEmojiCategory(self, category: str) -> Collection[EmojiData]:
        if not utils.isValidStr(category):
            raise TypeError(f'category argument is malformed: \"{category}\"')

        await self.__readJson()
        matchingEmoji: list[EmojiData] = list()

        for emojiData in self.__emojiData.values():
            if emojiData is None or not utils.isValidStr(emojiData.category):
                continue
            elif emojiData.category == category:
                matchingEmoji.append(emojiData)

        matchingEmoji.sort(key = lambda emojiData: emojiData.name.casefold())
        frozenMatchingEmoji: FrozenList[EmojiData] = FrozenList(matchingEmoji)
        frozenMatchingEmoji.freeze()
        return frozenMatchingEmoji

    async def fetchEmojiData(self, emoji: str | None) -> EmojiData | None:
        if emoji is None:
            return None
        elif not isinstance(emoji, str):
            raise TypeError(f'emoji argument is malformed: \"{emoji}\"')
        elif not utils.isValidStr(emoji):
            return None

        await self.__readJson()
        return self.__emojiData.get(emoji, None)

    async def __parseJsonToEmojiData(
        self,
        emojiJson: dict[str, Any],
    ) -> EmojiData:
        codes: set[str] = set()
        codeArray: list[str] | Any | None = emojiJson.get('code')
        if isinstance(codeArray, list) and len(codeArray) >= 1:
            for index, code in enumerate(codeArray):
                if utils.isValidStr(code):
                    codes.add(code)
                else:
                    self.__timber.log('EmojiRepository', f'Encountered malformed emoji code ({index=}) ({code=}) ({emojiJson=})')

        category: str | None = None
        if 'category' in emojiJson and utils.isValidStr(emojiJson.get('category')):
            category = utils.getStrFromDict(emojiJson, 'category')

        emoji = utils.getStrFromDict(emojiJson, 'emoji')
        name = utils.getStrFromDict(emojiJson, 'name')

        subCategory: str | None = None
        if 'subcategory' in emojiJson and utils.isValidStr(emojiJson.get('subcategory')):
            subCategory = utils.getStrFromDict(emojiJson, 'subcategory')

        return EmojiData(
            codes = frozenset(codes),
            category = category,
            emoji = emoji,
            name = name,
            subCategory = subCategory,
        )

    async def __readJson(self):
        if self.__isLoaded:
            return

        self.__isLoaded = True
        self.__timber.log('EmojiRepository', f'Reading in emoji data...')

        jsonContents = await self.__emojiJsonReader.readJsonAsync()
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            self.__timber.log('EmojiRepository', f'Structure of emoji JSON data is wrong or malformed! ({jsonContents=})')
            return

        emojisArray: list[dict[str, Any]] | Any | None = jsonContents.get('emojis')
        if not isinstance(emojisArray, list) or len(emojisArray) == 0:
            self.__timber.log('EmojiRepository', f'\"emojis\" field is missing, malformed, or empty! ({emojisArray=}) ({jsonContents=})')
            return

        for index, emojiJson in enumerate(emojisArray):
            emojiData: EmojiData | None = None
            exception: Exception | None = None

            try:
                emojiData = await self.__parseJsonToEmojiData(
                    emojiJson = emojiJson,
                )
            except Exception as e:
                exception = e

            if emojiData is None or exception is not None:
                self.__timber.log('EmojiRepository', f'Failed to read in emoji data at index {index} ({emojiData=}) ({emojiJson=}) ({exception=})', exception, traceback.format_exc())
            else:
                self.__emojiData[emojiData.emoji] = emojiData

        self.__timber.log('EmojiRepository', f'Finished reading in {len(self.__emojiData)} emoji(s)')
