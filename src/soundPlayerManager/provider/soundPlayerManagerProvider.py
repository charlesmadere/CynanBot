from typing import Final

from .soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..audioPlayer.audioPlayerSoundPlayerManager import AudioPlayerSoundPlayerManager
from ..settings.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from ..soundPlayerManagerInterface import SoundPlayerManagerInterface
from ..soundPlayerType import SoundPlayerType
from ..stub.stubSoundPlayerManager import StubSoundPlayerManager
from ..vlc.vlcSoundPlayerManager import VlcSoundPlayerManager
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...misc.generalSettingsRepository import GeneralSettingsRepository
from ...timber.timberInterface import TimberInterface


class SoundPlayerManagerProvider(SoundPlayerManagerProviderInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif generalSettingsRepository is not None and not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__soundPlayerSettingsRepository: Final[SoundPlayerSettingsRepositoryInterface] = soundPlayerSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

        self.__soundPlayerManager: SoundPlayerManagerInterface | None = None

    def constructNewInstance(self) -> SoundPlayerManagerInterface:
        snapshot = self.__generalSettingsRepository.getAll()
        soundPlayerType = snapshot.requireSoundPlayerType()

        match soundPlayerType:
            case SoundPlayerType.AUDIO_PLAYER:
                return AudioPlayerSoundPlayerManager(
                    eventLoop = self.__backgroundTaskHelper.eventLoop,
                    soundPlayerSettingsRepository = self.__soundPlayerSettingsRepository,
                    timber = self.__timber,
                    timeZoneRepository = self.__timeZoneRepository,
                )

            case SoundPlayerType.STUB:
                return StubSoundPlayerManager()

            case SoundPlayerType.VLC:
                return VlcSoundPlayerManager(
                    soundPlayerSettingsRepository = self.__soundPlayerSettingsRepository,
                    timber = self.__timber,
                )

            case _:
                raise RuntimeError(f'Unknown SoundPlayerType value: \"{soundPlayerType}\"')

    def getSharedInstance(self) -> SoundPlayerManagerInterface:
        soundPlayerManager = self.__soundPlayerManager

        if soundPlayerManager is None:
            soundPlayerManager = self.constructNewInstance()
            self.__soundPlayerManager = soundPlayerManager

        return soundPlayerManager
