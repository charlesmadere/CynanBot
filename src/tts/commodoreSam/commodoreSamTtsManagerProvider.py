from typing import Final

from .commodoreSamTtsManager import CommodoreSamTtsManager
from .commodoreSamTtsManagerInterface import CommodoreSamTtsManagerInterface
from .commodoreSamTtsManagerProviderInterface import CommodoreSamTtsManagerProviderInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...commodoreSam.commodoreSamMessageCleanerInterface import CommodoreSamMessageCleanerInterface
from ...commodoreSam.helper.commodoreSamHelperInterface import CommodoreSamHelperInterface
from ...commodoreSam.settings.commodoreSamSettingsRepositoryInterface import CommodoreSamSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class CommodoreSamTtsManagerProvider(CommodoreSamTtsManagerProviderInterface):

    def __init__(
        self,
        commodoreSamHelper: CommodoreSamHelperInterface,
        commodoreSamMessageCleaner: CommodoreSamMessageCleanerInterface,
        commodoreSamSettingsRepository: CommodoreSamSettingsRepositoryInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
    ):
        if not isinstance(commodoreSamHelper, CommodoreSamHelperInterface):
            raise TypeError(f'commodoreSamHelper argument is malformed: \"{commodoreSamHelper}\"')
        elif not isinstance(commodoreSamMessageCleaner, CommodoreSamMessageCleanerInterface):
            raise TypeError(f'commodoreSamMessageCleaner argument is malformed: \"{commodoreSamMessageCleaner}\"')
        elif not isinstance(commodoreSamSettingsRepository, CommodoreSamSettingsRepositoryInterface):
            raise TypeError(f'commodoreSamSettingsRepository argument is malformed: \"{commodoreSamSettingsRepository}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__commodoreSamHelper: Final[CommodoreSamHelperInterface] = commodoreSamHelper
        self.__commodoreSamMessageCleaner: Final[CommodoreSamMessageCleanerInterface] = commodoreSamMessageCleaner
        self.__commodoreSamSettingsRepository: Final[CommodoreSamSettingsRepositoryInterface] = commodoreSamSettingsRepository
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__timber: Final[TimberInterface] = timber
        self.__ttsCommandBuilder: Final[TtsCommandBuilderInterface] = ttsCommandBuilder
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__sharedInstance: CommodoreSamTtsManagerInterface | None = None

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True,
    ) -> CommodoreSamTtsManagerInterface | None:
        if not utils.isValidBool(useSharedSoundPlayerManager):
            raise TypeError(f'useSharedSoundPlayerManager argument is malformed: \"{useSharedSoundPlayerManager}\"')

        soundPlayerManager: SoundPlayerManagerInterface

        if useSharedSoundPlayerManager:
            soundPlayerManager = self.__soundPlayerManagerProvider.getSharedInstance()
        else:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()

        return CommodoreSamTtsManager(
            commodoreSamHelper = self.__commodoreSamHelper,
            commodoreSamMessageCleaner = self.__commodoreSamMessageCleaner,
            commodoreSamSettingsRepository = self.__commodoreSamSettingsRepository,
            soundPlayerManager = soundPlayerManager,
            timber = self.__timber,
            ttsCommandBuilder = self.__ttsCommandBuilder,
            ttsSettingsRepository = self.__ttsSettingsRepository,
        )

    def getSharedInstance(self) -> CommodoreSamTtsManagerInterface | None:
        sharedInstance = self.__sharedInstance

        if sharedInstance is None:
            sharedInstance = self.constructNewInstance()
            self.__sharedInstance = sharedInstance

        return sharedInstance
