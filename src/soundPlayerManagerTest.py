import asyncio
from asyncio import AbstractEventLoop

from aniv.anivContentScanner import AnivContentScanner
from aniv.anivContentScannerInterface import AnivContentScannerInterface
from contentScanner.bannedWordsRepository import BannedWordsRepository
from contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from contentScanner.contentScanner import ContentScanner
from contentScanner.contentScannerInterface import ContentScannerInterface
from misc.backgroundTaskHelper import BackgroundTaskHelper
from misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from soundPlayerManager.soundAlert import SoundAlert
from soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from soundPlayerManager.soundPlayerSettingsRepository import SoundPlayerSettingsRepository
from soundPlayerManager.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from soundPlayerManager.vlc.vlcSoundPlayerManager import VlcSoundPlayerManager
from storage.jsonStaticReader import JsonStaticReader
from storage.linesStaticReader import LinesStaticReader
from systemCommandHelper.systemCommandHelper import SystemCommandHelper
from systemCommandHelper.systemCommandHelperInterface import SystemCommandHelperInterface
from timber.timberInterface import TimberInterface
from timber.timberStub import TimberStub
from trivia.compilers.triviaAnswerCompiler import TriviaAnswerCompiler
from trivia.compilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface

eventLoop: AbstractEventLoop = asyncio.get_event_loop()

backgroundTaskHelper: BackgroundTaskHelperInterface = BackgroundTaskHelper(
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

soundPlayerManager: SoundPlayerManagerInterface = VlcSoundPlayerManager(
    backgroundTaskHelper = backgroundTaskHelper,
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    timber = timber
)

async def main():
    pass
    await soundPlayerManager.playSoundAlert(SoundAlert.SUBSCRIBE)
    print('sleep')
    await asyncio.sleep(10)
    pass

eventLoop.run_until_complete(main())
