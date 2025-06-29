from typing import Final

from .halfLifeTtsManager import HalfLifeTtsManager
from .halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from .halfLifeTtsManagerProviderInterface import HalfLifeTtsManagerProviderInterface
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...halfLife.halfLifeMessageCleanerInterface import HalfLifeMessageCleanerInterface
from ...halfLife.helper.halfLifeTtsHelperInterface import HalfLifeTtsHelperInterface
from ...halfLife.settings.halfLifeSettingsRepositoryInterface import HalfLifeSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class HalfLifeTtsManagerProvider(HalfLifeTtsManagerProviderInterface):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        halfLifeMessageCleaner: HalfLifeMessageCleanerInterface,
        halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface,
        halfLifeTtsHelper: HalfLifeTtsHelperInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        timber: TimberInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(halfLifeMessageCleaner, HalfLifeMessageCleanerInterface):
            raise TypeError(f'halfLifeMessageCleaner argument is malformed: \"{halfLifeMessageCleaner}\"')
        elif not isinstance(halfLifeSettingsRepository, HalfLifeSettingsRepositoryInterface):
            raise TypeError(f'halfLifeSettingsRepository argument is malformed: \"{halfLifeSettingsRepository}\"')
        elif not isinstance(halfLifeTtsHelper, HalfLifeTtsHelperInterface):
            raise TypeError(f'halfLifeTtsHelper argument is malformed: \"{halfLifeTtsHelper}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__halfLifeMessageCleaner: Final[HalfLifeMessageCleanerInterface] = halfLifeMessageCleaner
        self.__halfLifeSettingsRepository: Final[HalfLifeSettingsRepositoryInterface] = halfLifeSettingsRepository
        self.__halfLifeTtsHelper: Final[HalfLifeTtsHelperInterface] = halfLifeTtsHelper
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__timber: Final[TimberInterface] = timber
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__sharedInstance: HalfLifeTtsManagerInterface | None = None

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> HalfLifeTtsManagerInterface | None:
        if not utils.isValidBool(useSharedSoundPlayerManager):
            raise TypeError(f'useSharedSoundPlayerManager argument is malformed: \"{useSharedSoundPlayerManager}\"')

        soundPlayerManager: SoundPlayerManagerInterface

        if useSharedSoundPlayerManager:
            soundPlayerManager = self.__soundPlayerManagerProvider.getSharedInstance()
        else:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()

        return HalfLifeTtsManager(
            chatterPreferredTtsHelper = self.__chatterPreferredTtsHelper,
            halfLifeMessageCleaner = self.__halfLifeMessageCleaner,
            halfLifeSettingsRepository = self.__halfLifeSettingsRepository,
            halfLifeTtsHelper = self.__halfLifeTtsHelper,
            soundPlayerManager = soundPlayerManager,
            timber = self.__timber,
            ttsSettingsRepository = self.__ttsSettingsRepository
        )

    def getSharedInstance(self) -> HalfLifeTtsManagerInterface | None:
        sharedInstance = self.__sharedInstance

        if sharedInstance is None:
            sharedInstance = self.constructNewInstance()
            self.__sharedInstance = sharedInstance

        return sharedInstance
