from asyncio import AbstractEventLoop
from typing import Final

from ..audioPlayer.audioPlayerSoundPlayerManager import AudioPlayerSoundPlayerManager
from ..provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..settings.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...timber.timberInterface import TimberInterface


class AudioSoundPlayerManagerProvider(SoundPlayerManagerProviderInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__soundPlayerSettingsRepository: Final[SoundPlayerSettingsRepositoryInterface] = soundPlayerSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

        self.__soundPlayerManager: AudioPlayerSoundPlayerManager | None = None

    def constructNewInstance(self) -> AudioPlayerSoundPlayerManager:
        return AudioPlayerSoundPlayerManager(
            eventLoop = self.__eventLoop,
            soundPlayerSettingsRepository = self.__soundPlayerSettingsRepository,
            timber = self.__timber,
            timeZoneRepository = self.__timeZoneRepository,
        )

    def getSharedInstance(self) -> AudioPlayerSoundPlayerManager:
        soundPlayerManager = self.__soundPlayerManager

        if soundPlayerManager is None:
            soundPlayerManager = self.constructNewInstance()
            self.__soundPlayerManager = soundPlayerManager

        return soundPlayerManager
