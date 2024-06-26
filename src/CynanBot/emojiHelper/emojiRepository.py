import traceback
from typing import TypedDict

from CynanBot.misc.type_check import validate_typeddict
import CynanBot.misc.utils as utils
from CynanBot.emojiHelper.emojiInfo import EmojiInfo
from CynanBot.emojiHelper.emojiRepositoryInterface import \
    EmojiRepositoryInterface
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface
from CynanBot.timber.timberInterface import TimberInterface


class EmojiJson(TypedDict):
    code: list[str]
    category: str
    emoji: str
    name: str
    subcategory: str


class EmojiDataJson(TypedDict):
    emojis: list[EmojiJson]


class EmojiRepository(EmojiRepositoryInterface):

    def __init__(
        self,
        emojiJsonReader: JsonReaderInterface,
        timber: TimberInterface
    ):
        if not isinstance(emojiJsonReader, JsonReaderInterface):
            raise TypeError(f'emojiJsonReader argument is malformed: \"{emojiJsonReader}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__emojiJsonReader: JsonReaderInterface = emojiJsonReader
        self.__timber: TimberInterface = timber

        self.__isLoaded: bool = False
        self.__emojiInfoData: dict[str, EmojiInfo | None] = dict()

    async def fetchEmojiInfo(self, emoji: str | None) -> EmojiInfo | None:
        if emoji is None:
            return None
        elif not isinstance(emoji, str):
            raise TypeError(f'emoji argument is malformed: \"{emoji}\"')
        elif not utils.isValidStr(emoji):
            return None

        await self.__readJson()
        return self.__emojiInfoData.get(emoji)

    async def __parseDictToEmojiInfo(
        self,
        emojiDict: EmojiJson
    ) -> EmojiInfo:
        codes = set(emojiDict['code'])
        category = emojiDict['category']
        emoji = emojiDict['emoji']
        name = emojiDict['name']
        subCategory = emojiDict['subcategory']

        return EmojiInfo(
            codes = codes,
            category = category,
            emoji = emoji,
            name = name,
            subCategory = subCategory
        )

    async def __readJson(self):
        if self.__isLoaded:
            return

        self.__isLoaded = True
        self.__timber.log('EmojiRepository', f'Reading in emoji info data...')
        jsonContents = await self.__emojiJsonReader.readJsonAsync()

        if not validate_typeddict(jsonContents, EmojiDataJson):
            self.__timber.log('EmojiRepository', f'structure of emoji data json is wrong\n{jsonContents=}')
            return

        emojisList = jsonContents['emojis']

        if len(emojisList) == 0:
            self.__timber.log('EmojiRepository', f'\"emojis\" field is empty!')
            return

        for index, emojiDict in enumerate(emojisList):
            emojiInfo: EmojiInfo | None = None
            exception: Exception | None = None

            try:
                emojiInfo = await self.__parseDictToEmojiInfo(emojiDict)
            except Exception as e:
                exception = e

            if emojiInfo is None or exception is not None:
                self.__timber.log('EmojiRepository', f'Failed to read in emoji info at index {index} ({emojiDict=}): {exception}', exception, traceback.format_exc())
            else:
                self.__emojiInfoData[emojiInfo.emoji] = emojiInfo

        self.__timber.log('EmojiRepository', f'Finished reading in {len(self.__emojiInfoData)} emoji(s)')
