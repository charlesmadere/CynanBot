from typing import Final

from ..provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..settings.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from ..vlc.vlcSoundPlayerManager import VlcSoundPlayerManager
from ...timber.timberInterface import TimberInterface


class VlcSoundPlayerManagerProvider(SoundPlayerManagerProviderInterface):

    def __init__(
        self,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface,
    ):
        if not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__soundPlayerSettingsRepository: Final[SoundPlayerSettingsRepositoryInterface] = soundPlayerSettingsRepository
        self.__timber: Final[TimberInterface] = timber

        self.__soundPlayerManager: VlcSoundPlayerManager | None = None

    def constructNewInstance(self) -> VlcSoundPlayerManager:
        return VlcSoundPlayerManager(
            soundPlayerSettingsRepository = self.__soundPlayerSettingsRepository,
            timber = self.__timber,
        )

    def getSharedInstance(self) -> VlcSoundPlayerManager:
        soundPlayerManager = self.__soundPlayerManager

        if soundPlayerManager is None:
            soundPlayerManager = self.constructNewInstance()
            self.__soundPlayerManager = soundPlayerManager

        return soundPlayerManager
