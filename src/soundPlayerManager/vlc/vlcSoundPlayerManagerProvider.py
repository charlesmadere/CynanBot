from .vlcSoundPlayerManager import VlcSoundPlayerManager
from ..playSessionIdGenerator.playSessionIdGeneratorInterface import PlaySessionIdGeneratorInterface
from ..soundPlayerManagerInterface import SoundPlayerManagerInterface
from ..soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from ...chatBand.chatBandInstrumentSoundsRepositoryInterface import ChatBandInstrumentSoundsRepositoryInterface
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface


class VlcSoundPlayerManagerProvider(SoundPlayerManagerProviderInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        chatBandInstrumentSoundsRepository: ChatBandInstrumentSoundsRepositoryInterface | None,
        playSessionIdGenerator: PlaySessionIdGeneratorInterface,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif chatBandInstrumentSoundsRepository is not None and not isinstance(chatBandInstrumentSoundsRepository, ChatBandInstrumentSoundsRepositoryInterface):
            raise TypeError(f'chatBandInstrumentSoundsRepository argument is malformed: \"{chatBandInstrumentSoundsRepository}\"')
        elif not isinstance(playSessionIdGenerator, PlaySessionIdGeneratorInterface):
            raise TypeError(f'playSessionIdGenerator argument is malformed: \"{playSessionIdGenerator}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__chatBandInstrumentSoundsRepository: ChatBandInstrumentSoundsRepositoryInterface | None = chatBandInstrumentSoundsRepository
        self.__playSessionIdGenerator: PlaySessionIdGeneratorInterface = playSessionIdGenerator
        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__timber: TimberInterface = timber

        self.__soundPlayerManager: SoundPlayerManagerInterface | None = None

    def constructNewSoundPlayerManagerInstance(self) -> SoundPlayerManagerInterface:
        return VlcSoundPlayerManager(
            backgroundTaskHelper = self.__backgroundTaskHelper,
            chatBandInstrumentSoundsRepository = self.__chatBandInstrumentSoundsRepository,
            playSessionIdGenerator = self.__playSessionIdGenerator,
            soundPlayerSettingsRepository = self.__soundPlayerSettingsRepository,
            timber = self.__timber
        )

    def getSharedSoundPlayerManagerInstance(self) -> SoundPlayerManagerInterface:
        soundPlayerManager = self.__soundPlayerManager

        if soundPlayerManager is None:
            soundPlayerManager = self.constructNewSoundPlayerManagerInstance()
            self.__soundPlayerManager = soundPlayerManager

        return soundPlayerManager
