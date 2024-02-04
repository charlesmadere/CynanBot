import asyncio
import re
from asyncio import AbstractEventLoop
from typing import Any, Optional, Pattern

from CynanBot.aniv.anivContentCode import AnivContentCode
from CynanBot.vlcHelper.vlcHelper import VlcHelper
from CynanBot.vlcHelper.vlcHelperInterface import VlcHelperInterface
from CynanBot.aniv.anivContentScanner import AnivContentScanner
from CynanBot.aniv.anivContentScannerInterface import \
    AnivContentScannerInterface
from CynanBot.contentScanner.bannedWordsRepository import BannedWordsRepository
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.contentScanner.contentScanner import ContentScanner
from CynanBot.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.soundPlayerHelper.soundAlertHelper import SoundPlayerHelper
from CynanBot.soundPlayerHelper.soundAlertHelperInterface import \
    SoundPlayerHelperInterface
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.soundPlayerManager.soundPlayerSettingsRepository import \
    SoundPlayerSettingsRepository
from CynanBot.soundPlayerManager.soundPlayerSettingsRepositoryInterface import \
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

eventLoop: AbstractEventLoop = asyncio.get_event_loop()
backgroundTaskHelper = BackgroundTaskHelper(
    eventLoop = eventLoop
)
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

vlcHelper: VlcHelperInterface = VlcHelper(
    timber = timber
)

soundPlayerHelper: SoundPlayerHelperInterface = SoundPlayerHelper(
    backgroundTaskHelper = backgroundTaskHelper,
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    timber = timber,
    vlcHelper = vlcHelper
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
