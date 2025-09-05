import asyncio
from asyncio import AbstractEventLoop

from src.chatBand.chatBandInstrumentSoundsRepository import ChatBandInstrumentSoundsRepository
from src.chatBand.chatBandInstrumentSoundsRepositoryInterface import ChatBandInstrumentSoundsRepositoryInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.misc.backgroundTaskHelper import BackgroundTaskHelper
from src.misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from src.misc.generalSettingsRepository import GeneralSettingsRepository
from src.network.networkJsonMapper import NetworkJsonMapper
from src.network.networkJsonMapperInterface import NetworkJsonMapperInterface
from src.soundPlayerManager.jsonMapper.soundPlayerJsonMapper import SoundPlayerJsonMapper
from src.soundPlayerManager.jsonMapper.soundPlayerJsonMapperInterface import SoundPlayerJsonMapperInterface
from src.soundPlayerManager.provider.soundPlayerManagerProvider import SoundPlayerManagerProvider
from src.soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from src.soundPlayerManager.settings.soundPlayerSettingsRepository import SoundPlayerSettingsRepository
from src.soundPlayerManager.settings.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from src.soundPlayerManager.soundAlert import SoundAlert
from src.soundPlayerManager.soundPlayerType import SoundPlayerType
from src.storage.jsonStaticReader import JsonStaticReader
from src.storage.storageJsonMapper import StorageJsonMapper
from src.storage.storageJsonMapperInterface import StorageJsonMapperInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub

eventLoop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

backgroundTaskHelper: BackgroundTaskHelperInterface = BackgroundTaskHelper(
    eventLoop = eventLoop
)

timber: TimberInterface = TimberStub()

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

networkJsonMapper: NetworkJsonMapperInterface = NetworkJsonMapper()

soundPlayerJsonMapper: SoundPlayerJsonMapperInterface = SoundPlayerJsonMapper()

storageJsonMapper: StorageJsonMapperInterface = StorageJsonMapper()

generalSettingsRepository = GeneralSettingsRepository(
    settingsJsonReader = JsonStaticReader(dict()),
    networkJsonMapper = networkJsonMapper,
    soundPlayerJsonMapper = soundPlayerJsonMapper,
    storageJsonMapper = storageJsonMapper,
    defaultSoundPlayerType = SoundPlayerType.AUDIO_PLAYER
)

chatBandInstrumentSoundsRepository: ChatBandInstrumentSoundsRepositoryInterface = ChatBandInstrumentSoundsRepository(
    backgroundTaskHelper = backgroundTaskHelper,
    timber = timber
)

soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = SoundPlayerSettingsRepository(
    settingsJsonReader = JsonStaticReader(dict())
)

soundPlayerManagerProvider: SoundPlayerManagerProviderInterface = SoundPlayerManagerProvider(
    backgroundTaskHelper = backgroundTaskHelper,
    generalSettingsRepository = generalSettingsRepository,
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
)

async def main():
    pass
    soundPlayerManager = soundPlayerManagerProvider.constructNewInstance()
    await soundPlayerManager.playSoundAlert(SoundAlert.SUBSCRIBE)
    print('sleep')
    await asyncio.sleep(10)
    pass

eventLoop.run_until_complete(main())
