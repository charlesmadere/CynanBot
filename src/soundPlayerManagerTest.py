import asyncio
from asyncio import AbstractEventLoop

from .aniv.anivContentScanner import AnivContentScanner
from .aniv.anivContentScannerInterface import AnivContentScannerInterface
from .chatBand.chatBandInstrumentSoundsRepository import ChatBandInstrumentSoundsRepository
from .chatBand.chatBandInstrumentSoundsRepositoryInterface import ChatBandInstrumentSoundsRepositoryInterface
from .contentScanner.bannedWordsRepository import BannedWordsRepository
from .contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from .contentScanner.contentScanner import ContentScanner
from .contentScanner.contentScannerInterface import ContentScannerInterface
from .misc.backgroundTaskHelper import BackgroundTaskHelper
from .misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from .soundPlayerManager.playSessionIdGenerator.playSessionIdGenerator import PlaySessionIdGenerator
from .soundPlayerManager.playSessionIdGenerator.playSessionIdGeneratorInterface import PlaySessionIdGeneratorInterface
from .soundPlayerManager.soundAlert import SoundAlert
from .soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from .soundPlayerManager.soundPlayerSettingsRepository import SoundPlayerSettingsRepository
from .soundPlayerManager.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from .soundPlayerManager.vlc.vlcSoundPlayerManager import VlcSoundPlayerManager
from .storage.jsonStaticReader import JsonStaticReader
from .storage.linesStaticReader import LinesStaticReader
from .timber.timberInterface import TimberInterface
from .timber.timberStub import TimberStub
from .trivia.compilers.triviaAnswerCompiler import TriviaAnswerCompiler
from .trivia.compilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from .trivia.triviaSettingsRepository import TriviaSettingsRepository
from .trivia.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface

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

chatBandInstrumentSoundsRepository: ChatBandInstrumentSoundsRepositoryInterface = ChatBandInstrumentSoundsRepository(
    backgroundTaskHelper = backgroundTaskHelper,
    timber = timber
)

anivContentScanner: AnivContentScannerInterface = AnivContentScanner(
    contentScanner = contentScanner,
    timber = timber
)

triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
    settingsJsonReader = JsonStaticReader(dict())
)

triviaAnswerCompiler: TriviaAnswerCompilerInterface = TriviaAnswerCompiler(
    timber = timber
)

playSessionIdGenerator: PlaySessionIdGeneratorInterface = PlaySessionIdGenerator()

soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = SoundPlayerSettingsRepository(
    settingsJsonReader = JsonStaticReader(dict())
)

soundPlayerManager: SoundPlayerManagerInterface = VlcSoundPlayerManager(
    backgroundTaskHelper = backgroundTaskHelper,
    chatBandInstrumentSoundsRepository = chatBandInstrumentSoundsRepository,
    playSessionIdGenerator = playSessionIdGenerator,
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
