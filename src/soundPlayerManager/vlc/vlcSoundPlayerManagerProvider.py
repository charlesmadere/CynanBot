from .vlcSoundPlayerManager import VlcSoundPlayerManager
from ..soundPlayerManagerInterface import SoundPlayerManagerInterface
from ..soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from ...chatBand.chatBandInstrumentSoundsRepositoryInterface import ChatBandInstrumentSoundsRepositoryInterface
from ...timber.timberInterface import TimberInterface


class VlcSoundPlayerManagerProvider(SoundPlayerManagerProviderInterface):

    def __init__(
        self,
        chatBandInstrumentSoundsRepository: ChatBandInstrumentSoundsRepositoryInterface | None,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface
    ):
        if chatBandInstrumentSoundsRepository is not None and not isinstance(chatBandInstrumentSoundsRepository, ChatBandInstrumentSoundsRepositoryInterface):
            raise TypeError(f'chatBandInstrumentSoundsRepository argument is malformed: \"{chatBandInstrumentSoundsRepository}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__chatBandInstrumentSoundsRepository: ChatBandInstrumentSoundsRepositoryInterface | None = chatBandInstrumentSoundsRepository
        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__timber: TimberInterface = timber

        self.__soundPlayerManager: SoundPlayerManagerInterface | None = None

    def constructNewSoundPlayerManagerInstance(self) -> SoundPlayerManagerInterface:
        return VlcSoundPlayerManager(
            chatBandInstrumentSoundsRepository = self.__chatBandInstrumentSoundsRepository,
            soundPlayerSettingsRepository = self.__soundPlayerSettingsRepository,
            timber = self.__timber
        )

    def getSharedSoundPlayerManagerInstance(self) -> SoundPlayerManagerInterface:
        soundPlayerManager = self.__soundPlayerManager

        if soundPlayerManager is None:
            soundPlayerManager = self.constructNewSoundPlayerManagerInstance()
            self.__soundPlayerManager = soundPlayerManager

        return soundPlayerManager
