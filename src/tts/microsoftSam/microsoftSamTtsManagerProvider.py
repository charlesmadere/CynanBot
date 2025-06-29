from typing import Final

from .microsoftSamTtsManager import MicrosoftSamTtsManager
from .microsoftSamTtsManagerInterface import MicrosoftSamTtsManagerInterface
from .microsoftSamTtsManagerProviderInterface import MicrosoftSamTtsManagerProviderInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...microsoftSam.helper.microsoftSamHelperInterface import MicrosoftSamHelperInterface
from ...microsoftSam.microsoftSamMessageCleanerInterface import MicrosoftSamMessageCleanerInterface
from ...microsoftSam.settings.microsoftSamSettingsRepositoryInterface import MicrosoftSamSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class MicrosoftSamTtsManagerProvider(MicrosoftSamTtsManagerProviderInterface):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        microsoftSamHelper: MicrosoftSamHelperInterface,
        microsoftSamMessageCleaner: MicrosoftSamMessageCleanerInterface,
        microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(microsoftSamHelper, MicrosoftSamHelperInterface):
            raise TypeError(f'microsoftSamHelper argument is malformed: \"{microsoftSamHelper}\"')
        elif not isinstance(microsoftSamMessageCleaner, MicrosoftSamMessageCleanerInterface):
            raise TypeError(f'microsoftSamMessageCleaner argument is malformed: \"{microsoftSamMessageCleaner}\"')
        elif not isinstance(microsoftSamSettingsRepository, MicrosoftSamSettingsRepositoryInterface):
            raise TypeError(f'microsoftSamSettingsRepository argument is malformed: \"{microsoftSamSettingsRepository}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__microsoftSamHelper: Final[MicrosoftSamHelperInterface] = microsoftSamHelper
        self.__microsoftSamMessageCleaner: Final[MicrosoftSamMessageCleanerInterface] = microsoftSamMessageCleaner
        self.__microsoftSamSettingsRepository: Final[MicrosoftSamSettingsRepositoryInterface] = microsoftSamSettingsRepository
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__timber: Final[TimberInterface] = timber
        self.__ttsCommandBuilder: Final[TtsCommandBuilderInterface] = ttsCommandBuilder
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__sharedInstance: MicrosoftSamTtsManagerInterface | None = None

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> MicrosoftSamTtsManagerInterface | None:
        if not utils.isValidBool(useSharedSoundPlayerManager):
            raise TypeError(f'useSharedSoundPlayerManager argument is malformed: \"{useSharedSoundPlayerManager}\"')

        soundPlayerManager: SoundPlayerManagerInterface

        if useSharedSoundPlayerManager:
            soundPlayerManager = self.__soundPlayerManagerProvider.getSharedInstance()
        else:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()

        return MicrosoftSamTtsManager(
            chatterPreferredTtsHelper = self.__chatterPreferredTtsHelper,
            microsoftSamHelper = self.__microsoftSamHelper,
            microsoftSamMessageCleaner = self.__microsoftSamMessageCleaner,
            microsoftSamSettingsRepository = self.__microsoftSamSettingsRepository,
            soundPlayerManager = soundPlayerManager,
            timber = self.__timber,
            ttsCommandBuilder = self.__ttsCommandBuilder,
            ttsSettingsRepository = self.__ttsSettingsRepository
        )

    def getSharedInstance(self) -> MicrosoftSamTtsManagerInterface | None:
        sharedInstance = self.__sharedInstance

        if sharedInstance is None:
            sharedInstance = self.constructNewInstance()
            self.__sharedInstance = sharedInstance

        return sharedInstance
