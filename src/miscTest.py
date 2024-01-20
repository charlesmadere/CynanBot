import asyncio
import re
from typing import Any, Optional, Pattern

from CynanBot.aniv.anivContentCode import AnivContentCode
from CynanBot.aniv.anivContentScanner import AnivContentScanner
from CynanBot.aniv.anivContentScannerInterface import \
    AnivContentScannerInterface
from CynanBot.contentScanner.bannedWordsRepository import BannedWordsRepository
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.contentScanner.contentScanner import ContentScanner
from CynanBot.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBot.soundPlayerHelper.soundAlert import SoundAlert
from CynanBot.soundPlayerHelper.soundPlayerHelper import SoundPlayerHelper
from CynanBot.soundPlayerHelper.soundPlayerHelperInterface import \
    SoundPlayerHelperInterface
from CynanBot.soundPlayerHelper.soundPlayerSettingsRepository import \
    SoundPlayerSettingsRepository
from CynanBot.soundPlayerHelper.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from CynanBot.storage.jsonStaticReader import JsonStaticReader
from CynanBot.storage.linesStaticReader import LinesStaticReader
from CynanBot.systemCommandHelper.systemCommandHelper import \
    SystemCommandHelper
from CynanBot.systemCommandHelper.systemCommandHelperInterface import \
    SystemCommandHelperInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub
from CynanBot.trivia.compilers.triviaAnswerCompiler import TriviaAnswerCompiler
from CynanBot.trivia.compilers.triviaAnswerCompilerInterface import \
    TriviaAnswerCompilerInterface

timber: TimberInterface = TimberStub()

bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
    bannedWordsLinesReader = LinesStaticReader(
        lines = [ 'Nintendo', 'SONY', '"QAnon"', 'sony' ]
    ),
    timber = timber
)

contentScanner: ContentScannerInterface = ContentScanner(
    bannedWordsRepository,
    timber = timber
)

anivContentScanner: AnivContentScannerInterface = AnivContentScanner(
    contentScanner = contentScanner,
    timber = timber
)

triviaAnswerCompiler: TriviaAnswerCompilerInterface = TriviaAnswerCompiler(
    timber = timber
)

soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = SoundPlayerSettingsRepository(
    settingsJsonReader = JsonStaticReader(dict())
)

systemCommandHelper: SystemCommandHelperInterface = SystemCommandHelper(
    timber = timber
)

soundPlayerHelper: SoundPlayerHelperInterface = SoundPlayerHelper(
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    systemCommandHelper = systemCommandHelper,
    timber = timber
)

eventLoop = asyncio.get_event_loop()

async def main():
    pass
    # result = await triviaAnswerCompiler.compileTextAnswersList([ 'Garfield the cat' ])
    # print(f'result=\"{result}\"')
    pass
    # result = await anivContentScanner.scan('(insanefirebat)')
    # print(f'{result=}')
    pass
    await soundPlayerHelper.play(SoundAlert.SUBSCRIBE)
    print('sleep')
    await asyncio.sleep(10000)
    pass

eventLoop.run_until_complete(main())
