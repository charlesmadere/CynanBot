import asyncio
from asyncio import AbstractEventLoop

from .chatBand.chatBandInstrumentSoundsRepository import ChatBandInstrumentSoundsRepository
from .chatBand.chatBandInstrumentSoundsRepositoryInterface import ChatBandInstrumentSoundsRepositoryInterface
from .contentScanner.bannedWordsRepository import BannedWordsRepository
from .contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from .contentScanner.contentScanner import ContentScanner
from .contentScanner.contentScannerInterface import ContentScannerInterface
from .misc.backgroundTaskHelper import BackgroundTaskHelper
from .misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from .soundPlayerManager.audioPlayer.audioPlayerSoundPlayerManagerProvider import AudioPlayerSoundPlayerManagerProvider
from .soundPlayerManager.soundAlert import SoundAlert
from .soundPlayerManager.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from .soundPlayerManager.soundPlayerSettingsRepository import SoundPlayerSettingsRepository
from .soundPlayerManager.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from .soundPlayerManager.soundPlayerType import SoundPlayerType
from .soundPlayerManager.stub.stubSoundPlayerManagerProvider import StubSoundPlayerManagerProvider
from .soundPlayerManager.vlc.vlcSoundPlayerManagerProvider import VlcSoundPlayerManagerProvider
from .storage.jsonStaticReader import JsonStaticReader
from .storage.linesStaticReader import LinesStaticReader
from .timber.timberInterface import TimberInterface
from .timber.timberStub import TimberStub

soundPlayerType = SoundPlayerType.VLC

eventLoop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

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

soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = SoundPlayerSettingsRepository(
    settingsJsonReader = JsonStaticReader(dict())
)

soundPlayerManagerProvider: SoundPlayerManagerProviderInterface

match soundPlayerType:
    case SoundPlayerType.AUDIO_PLAYER:
        soundPlayerManagerProvider = AudioPlayerSoundPlayerManagerProvider(
            chatBandInstrumentSoundsRepository = None,
            soundPlayerSettingsRepository = soundPlayerSettingsRepository,
            timber = timber
        )

    case SoundPlayerType.STUB:
        soundPlayerManagerProvider = StubSoundPlayerManagerProvider()

    case SoundPlayerType.VLC:
        soundPlayerManagerProvider = VlcSoundPlayerManagerProvider(
            chatBandInstrumentSoundsRepository = None,
            soundPlayerSettingsRepository = soundPlayerSettingsRepository,
            timber = timber
        )

    case _:
        raise RuntimeError(f'Unknown/misconfigured SoundPlayerType: \"{soundPlayerType}\"')

async def main():
    pass
    soundPlayerManager = soundPlayerManagerProvider.constructNewSoundPlayerManagerInstance()
    await soundPlayerManager.playSoundAlert(SoundAlert.SUBSCRIBE)
    print('sleep')
    await asyncio.sleep(10)
    pass

eventLoop.run_until_complete(main())
