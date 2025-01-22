import asyncio
from asyncio import AbstractEventLoop

from src.chatBand.chatBandInstrumentSoundsRepository import ChatBandInstrumentSoundsRepository
from src.chatBand.chatBandInstrumentSoundsRepositoryInterface import ChatBandInstrumentSoundsRepositoryInterface
from src.contentScanner.bannedWordsRepository import BannedWordsRepository
from src.contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from src.contentScanner.contentScanner import ContentScanner
from src.contentScanner.contentScannerInterface import ContentScannerInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.misc.backgroundTaskHelper import BackgroundTaskHelper
from src.misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from src.soundPlayerManager.audioPlayer.audioPlayerSoundPlayerManagerProvider import \
    AudioPlayerSoundPlayerManagerProvider
from src.soundPlayerManager.soundAlert import SoundAlert
from src.soundPlayerManager.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from src.soundPlayerManager.soundPlayerSettingsRepository import SoundPlayerSettingsRepository
from src.soundPlayerManager.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from src.soundPlayerManager.soundPlayerType import SoundPlayerType
from src.soundPlayerManager.stub.stubSoundPlayerManagerProvider import StubSoundPlayerManagerProvider
from src.soundPlayerManager.vlc.vlcSoundPlayerManagerProvider import VlcSoundPlayerManagerProvider
from src.storage.jsonStaticReader import JsonStaticReader
from src.storage.linesStaticReader import LinesStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub

soundPlayerType = SoundPlayerType.VLC

eventLoop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

backgroundTaskHelper: BackgroundTaskHelperInterface = BackgroundTaskHelper(
    eventLoop = eventLoop
)

timber: TimberInterface = TimberStub()

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

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
            backgroundTaskHelper = backgroundTaskHelper,
            chatBandInstrumentSoundsRepository = chatBandInstrumentSoundsRepository,
            soundPlayerSettingsRepository = soundPlayerSettingsRepository,
            timber = timber,
            timeZoneRepository = timeZoneRepository
        )

    case SoundPlayerType.STUB:
        soundPlayerManagerProvider = StubSoundPlayerManagerProvider()

    case SoundPlayerType.VLC:
        soundPlayerManagerProvider = VlcSoundPlayerManagerProvider(
            chatBandInstrumentSoundsRepository = chatBandInstrumentSoundsRepository,
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
