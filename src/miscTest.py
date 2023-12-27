import asyncio
import re
from typing import Any, Optional, Pattern

import CynanBot.misc.utils as utils

# from CynanBot.contentScanner.bannedWordsRepository import \
#     BannedWordsRepository
# from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
#     BannedWordsRepositoryInterface
# from CynanBot.contentScanner.contentScanner import ContentScanner
# from CynanBot.contentScanner.contentScannerInterface import \
#     ContentScannerInterface
# from CynanBot.emojiHelper.emojiHelper import EmojiHelper
# from CynanBot.emojiHelper.emojiHelperInterface import \
#     EmojiHelperInterface
# from CynanBot.emojiHelper.emojiRepository import EmojiRepository
# from CynanBot.emojiHelper.emojiRepositoryInterface import \
#     EmojiRepositoryInterface
# from CynanBot.storage.jsonFileReader import JsonFileReader
# from CynanBot.storage.jsonStaticReader import JsonStaticReader
# from CynanBot.storage.linesStaticReader import LinesStaticReader
# from CynanBot.timber.timberInterface import TimberInterface
# from CynanBot.timber.timberStub import TimberStub
# from CynanBot.tts.decTalk.decTalkCommandBuilder import \
#     DecTalkCommandBuilder
# from CynanBot.tts.ttsCommandBuilderInterface import \
#     TtsCommandBuilderInterface
# from CynanBot.tts.ttsSettingsRepository import TtsSettingsRepository
# from CynanBot.tts.ttsSettingsRepositoryInterface import \
#     TtsSettingsRepositoryInterface

# timber: TimberInterface = TimberStub()

# bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
#     bannedWordsLinesReader = LinesStaticReader(
#         lines = [ 'hydroxychloroquine' ]
#     ),
#     timber = timber
# )

# contentScanner: ContentScannerInterface = ContentScanner(
#     bannedWordsRepository = bannedWordsRepository,
#     timber = timber
# )

# emojiRepository: EmojiRepositoryInterface = EmojiRepository(
#     emojiJsonReader = JsonStaticReader(
#         jsonContents = {
#             'emojis': [
#                 {
#                     'code': [
#                         "1F600"
#                     ],
#                     'emoji': '😀',
#                     'name': 'grinning face',
#                     'category': 'Smileys & Emotion',
#                     'subcategory': 'face-smiling',
#                     'support': {
#                         'apple': True,
#                         'google': True,
#                         'windows': True
#                     }
#                 },
#                 {
#                     'code': [
#                         "1F988"
#                     ],
#                     'emoji': '🦈',
#                     'name': 'shark',
#                     'category': 'Animals & Nature',
#                     'subcategory': 'animal-marine',
#                     'support': {
#                         'apple': True,
#                         'google': True,
#                         'windows': True
#                     }
#                 }
#             ]
#         }
#     ),
#     timber = timber
# )

# emojiHelper: EmojiHelperInterface = EmojiHelper(
#     emojiRepository = emojiRepository
# )

# ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
#     settingsJsonReader = JsonStaticReader(
#         jsonContents = {
#             'isEnabled': True
#         }
#     )
# )

# decTalkCommandBuilder: TtsCommandBuilderInterface = DecTalkCommandBuilder(
#     contentScanner = contentScanner,
#     emojiHelper = emojiHelper,
#     timber = timber,
#     ttsSettingsRepository = ttsSettingsRepository
# )

# eventLoop = asyncio.get_event_loop()

# async def main():
#     pass
#     result = await decTalkCommandBuilder.buildAndCleanMessage('hello 🦈😺 world')
#     print(f'result=\"{result}\"')
#     pass

# eventLoop.run_until_complete(main())

# x = utils.getDateTimeFromStr('2023-11-11T17:13:41Z+00:00')
# print(x)

# y = utils.getDateTimeFromStr('2023-10-21T14:11:45.338014562Z')
# print(y)

# z = utils.getDateTimeFromStr('2023-10-21T14:11:45.338014562Z+00:00')
# print(z)

wordTheWordRegEx: Pattern = re.compile(r'^(\w+)\s+(a|an|the)\s+(\w+)$', re.IGNORECASE)
match = wordTheWordRegEx.fullmatch('Silvervale of twitch')
print(match)

if match is not None:
    print(match.group())
    print(match.group(1))
    print(match.group(2))
    print(match.group(3))
    answer = f'{match.group(1)} ({match.group(2)}) {match.group(3)}'
    print(answer)
