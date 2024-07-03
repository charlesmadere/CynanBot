from misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from soundPlayerManager.soundPlayerManagerInterface import \
    SoundPlayerManagerInterface
from soundPlayerManager.soundPlayerManagerProviderInterface import \
    SoundPlayerManagerProviderInterface
from soundPlayerManager.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from soundPlayerManager.vlc.vlcSoundPlayerManager import VlcSoundPlayerManager
from timber.timberInterface import TimberInterface


class VlcSoundPlayerManagerProvider(SoundPlayerManagerProviderInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__timber: TimberInterface = timber

    def constructSoundPlayerManagerInstance(self) -> SoundPlayerManagerInterface:
        return VlcSoundPlayerManager(
            backgroundTaskHelper = self.__backgroundTaskHelper,
            soundPlayerSettingsRepository = self.__soundPlayerSettingsRepository,
            timber = self.__timber
        )
