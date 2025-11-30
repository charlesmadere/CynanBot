from typing import Final

from .googleTtsManager import GoogleTtsManager
from .googleTtsManagerInterface import GoogleTtsManagerInterface
from .googleTtsManagerProviderInterface import GoogleTtsManagerProviderInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...google.googleTtsMessageCleanerInterface import GoogleTtsMessageCleanerInterface
from ...google.helpers.googleTtsHelperInterface import GoogleTtsHelperInterface
from ...google.helpers.googleTtsVoicesHelperInterface import GoogleTtsVoicesHelperInterface
from ...google.settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class GoogleTtsManagerProvider(GoogleTtsManagerProviderInterface):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        googleSettingsRepository: GoogleSettingsRepositoryInterface,
        googleTtsHelper: GoogleTtsHelperInterface,
        googleTtsMessageCleaner: GoogleTtsMessageCleanerInterface,
        googleTtsVoicesHelper: GoogleTtsVoicesHelperInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(googleSettingsRepository, GoogleSettingsRepositoryInterface):
            raise TypeError(f'googleSettingsRepository argument is malformed: \"{googleSettingsRepository}\"')
        elif not isinstance(googleTtsHelper, GoogleTtsHelperInterface):
            raise TypeError(f'googleTtsHelper argument is malformed: \"{googleTtsHelper}\"')
        elif not isinstance(googleTtsMessageCleaner, GoogleTtsMessageCleanerInterface):
            raise TypeError(f'googleTtsMessageCleaner argument is malformed: \"{googleTtsMessageCleaner}\"')
        elif not isinstance(googleTtsVoicesHelper, GoogleTtsVoicesHelperInterface):
            raise TypeError(f'googleTtsVoicesHelper argument is malformed: \"{googleTtsVoicesHelper}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__googleSettingsRepository: Final[GoogleSettingsRepositoryInterface] = googleSettingsRepository
        self.__googleTtsHelper: Final[GoogleTtsHelperInterface] = googleTtsHelper
        self.__googleTtsMessageCleaner: Final[GoogleTtsMessageCleanerInterface] = googleTtsMessageCleaner
        self.__googleTtsVoicesHelper: Final[GoogleTtsVoicesHelperInterface] = googleTtsVoicesHelper
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__timber: Final[TimberInterface] = timber
        self.__ttsCommandBuilder: Final[TtsCommandBuilderInterface] = ttsCommandBuilder
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__sharedInstance: GoogleTtsManagerInterface | None = None

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True,
    ) -> GoogleTtsManagerInterface | None:
        if not utils.isValidBool(useSharedSoundPlayerManager):
            raise TypeError(f'useSharedSoundPlayerManager argument is malformed: \"{useSharedSoundPlayerManager}\"')

        soundPlayerManager: SoundPlayerManagerInterface

        if useSharedSoundPlayerManager:
            soundPlayerManager = self.__soundPlayerManagerProvider.getSharedInstance()
        else:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()

        return GoogleTtsManager(
            chatterPreferredTtsHelper = self.__chatterPreferredTtsHelper,
            googleSettingsRepository = self.__googleSettingsRepository,
            googleTtsHelper = self.__googleTtsHelper,
            googleTtsMessageCleaner = self.__googleTtsMessageCleaner,
            googleTtsVoicesHelper = self.__googleTtsVoicesHelper,
            soundPlayerManager = soundPlayerManager,
            timber = self.__timber,
            ttsCommandBuilder = self.__ttsCommandBuilder,
            ttsSettingsRepository = self.__ttsSettingsRepository,
        )

    def getSharedInstance(self) -> GoogleTtsManagerInterface | None:
        sharedInstance = self.__sharedInstance

        if sharedInstance is None:
            sharedInstance = self.constructNewInstance()
            self.__sharedInstance = sharedInstance

        return sharedInstance
