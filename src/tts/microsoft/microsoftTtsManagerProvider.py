from typing import Final

from .microsoftTtsManager import MicrosoftTtsManager
from .microsoftTtsManagerInterface import MicrosoftTtsManagerInterface
from .microsoftTtsManagerProviderInterface import MicrosoftTtsManagerProviderInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...microsoft.helper.microsoftTtsHelperInterface import MicrosoftTtsHelperInterface
from ...microsoft.microsoftTtsMessageCleanerInterface import MicrosoftTtsMessageCleanerInterface
from ...microsoft.settings.microsoftTtsSettingsRepositoryInterface import MicrosoftTtsSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class MicrosoftTtsManagerProvider(MicrosoftTtsManagerProviderInterface):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        microsoftTtsHelper: MicrosoftTtsHelperInterface,
        microsoftTtsMessageCleaner: MicrosoftTtsMessageCleanerInterface,
        microsoftTtsSettingsRepository: MicrosoftTtsSettingsRepositoryInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(microsoftTtsHelper, MicrosoftTtsHelperInterface):
            raise TypeError(f'microsoftTtsHelper argument is malformed: \"{microsoftTtsHelper}\"')
        elif not isinstance(microsoftTtsMessageCleaner, MicrosoftTtsMessageCleanerInterface):
            raise TypeError(f'microsoftTtsMessageCleaner argument is malformed: \"{microsoftTtsMessageCleaner}\"')
        elif not isinstance(microsoftTtsSettingsRepository, MicrosoftTtsSettingsRepositoryInterface):
            raise TypeError(f'microsoftTtsSettingsRepository argument is malformed: \"{microsoftTtsSettingsRepository}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__microsoftTtsHelper: Final[MicrosoftTtsHelperInterface] = microsoftTtsHelper
        self.__microsoftTtsMessageCleaner: Final[MicrosoftTtsMessageCleanerInterface] = microsoftTtsMessageCleaner
        self.__microsoftTtsSettingsRepository: Final[MicrosoftTtsSettingsRepositoryInterface] = microsoftTtsSettingsRepository
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__timber: Final[TimberInterface] = timber
        self.__ttsCommandBuilder: Final[TtsCommandBuilderInterface] = ttsCommandBuilder
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__sharedInstance: MicrosoftTtsManagerInterface | None = None

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> MicrosoftTtsManagerInterface | None:
        if not utils.isValidBool(useSharedSoundPlayerManager):
            raise TypeError(f'useSharedSoundPlayerManager argument is malformed: \"{useSharedSoundPlayerManager}\"')

        soundPlayerManager: SoundPlayerManagerInterface

        if useSharedSoundPlayerManager:
            soundPlayerManager = self.__soundPlayerManagerProvider.getSharedInstance()
        else:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()

        return MicrosoftTtsManager(
            chatterPreferredTtsHelper = self.__chatterPreferredTtsHelper,
            microsoftTtsHelper = self.__microsoftTtsHelper,
            microsoftTtsMessageCleaner = self.__microsoftTtsMessageCleaner,
            microsoftTtsSettingsRepository = self.__microsoftTtsSettingsRepository,
            soundPlayerManager = soundPlayerManager,
            timber = self.__timber,
            ttsCommandBuilder = self.__ttsCommandBuilder,
            ttsSettingsRepository = self.__ttsSettingsRepository
        )

    def getSharedInstance(self) -> MicrosoftTtsManagerInterface | None:
        sharedInstance = self.__sharedInstance

        if sharedInstance is None:
            sharedInstance = self.constructNewInstance()
            self.__sharedInstance = sharedInstance

        return sharedInstance
