import asyncio
from asyncio import AbstractEventLoop
from typing import Final

from src.emojiHelper.emojiHelper import EmojiHelper
from src.emojiHelper.emojiHelperInterface import EmojiHelperInterface
from src.emojiHelper.emojiRepository import EmojiRepository
from src.emojiHelper.emojiRepositoryInterface import EmojiRepositoryInterface
from src.storage.jsonFileReader import JsonFileReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub

eventLoop: Final[AbstractEventLoop] = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

timber: Final[TimberInterface] = TimberStub()

emojiRepository: Final[EmojiRepositoryInterface] = EmojiRepository(
    emojiJsonReader = JsonFileReader(
        eventLoop = eventLoop,
        fileName = '../emojiRepository.json'
    ),
    timber = timber,
)

emojiHelper: Final[EmojiHelperInterface] = EmojiHelper(
    emojiRepository = emojiRepository,
)

async def main():
    pass

    randomEmoji = await emojiHelper.getRandomAnimalEmoji()
    print(f'{randomEmoji=}')

    pass

eventLoop.run_until_complete(main())
