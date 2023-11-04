import asyncio
from typing import Any, Optional

from CynanBotCommon.contentScanner.bannedWordsRepository import \
    BannedWordsRepository
from CynanBotCommon.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBotCommon.contentScanner.contentScanner import ContentScanner
from CynanBotCommon.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBotCommon.emojiHelper.emojiHelper import EmojiHelper
from CynanBotCommon.emojiHelper.emojiHelperInterface import \
    EmojiHelperInterface
from CynanBotCommon.emojiHelper.emojiRepository import EmojiRepository
from CynanBotCommon.emojiHelper.emojiRepositoryInterface import \
    EmojiRepositoryInterface
from CynanBotCommon.storage.jsonFileReader import JsonFileReader
from CynanBotCommon.storage.jsonStaticReader import JsonStaticReader
from CynanBotCommon.storage.linesStaticReader import LinesStaticReader
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.timber.timberStub import TimberStub
from CynanBotCommon.tts.decTalkCommandBuilder import DecTalkCommandBuilder
from CynanBotCommon.tts.ttsCommandBuilderInterface import \
    TtsCommandBuilderInterface
from CynanBotCommon.tts.ttsSettingsRepository import TtsSettingsRepository
from CynanBotCommon.tts.ttsSettingsRepositoryInterface import \
    TtsSettingsRepositoryInterface

timber: TimberInterface = TimberStub()

bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
    bannedWordsLinesReader = LinesStaticReader(
        lines = [ 'hydroxychloroquine' ]
    ),
    timber = timber
)

contentScanner: ContentScannerInterface = ContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    timber = timber
)

emojiRepository: EmojiRepositoryInterface = EmojiRepository(
    emojiJsonReader = JsonStaticReader(
        jsonContents = {
            'emojis': [
                {
                    'code': [
                        "1F600"
                    ],
                    'emoji': '😀',
                    'name': 'grinning face',
                    'category': 'Smileys & Emotion',
                    'subcategory': 'face-smiling',
                    'support': {
                        'apple': True,
                        'google': True,
                        'windows': True
                    }
                },
                {
                    'code': [
                        "1F988"
                    ],
                    'emoji': '🦈',
                    'name': 'shark',
                    'category': 'Animals & Nature',
                    'subcategory': 'animal-marine',
                    'support': {
                        'apple': True,
                        'google': True,
                        'windows': True
                    }
                }
            ]
        }
    ),
    timber = timber
)

emojiHelper: EmojiHelperInterface = EmojiHelper(
    emojiRepository = emojiRepository
)

ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
    settingsJsonReader = JsonStaticReader(
        jsonContents = {
            'isEnabled': True
        }
    )
)

decTalkCommandBuilder: TtsCommandBuilderInterface = DecTalkCommandBuilder(
    contentScanner = contentScanner,
    emojiHelper = emojiHelper,
    timber = timber,
    ttsSettingsRepository = ttsSettingsRepository
)

eventLoop = asyncio.get_event_loop()

async def main():
    pass
    result = await decTalkCommandBuilder.buildAndCleanMessage('shark 🦈 shark 😀 🤔')
    print(f'result=\"{result}\"')
    pass

eventLoop.run_until_complete(main())
