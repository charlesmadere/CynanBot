from typing import Final

from .decTalkTtsManager import DecTalkTtsManager
from .decTalkTtsManagerInterface import DecTalkTtsManagerInterface
from .decTalkTtsManagerProviderInterface import DecTalkTtsManagerProviderInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..models.ttsProvider import TtsProvider
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...decTalk.decTalkMessageCleanerInterface import DecTalkMessageCleanerInterface
from ...decTalk.helper.decTalkHelperInterface import DecTalkHelperInterface
from ...decTalk.settings.decTalkSettingsRepositoryInterface import DecTalkSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class DecTalkTtsManagerProvider(DecTalkTtsManagerProviderInterface):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        decTalkHelper: DecTalkHelperInterface,
        decTalkMessageCleaner: DecTalkMessageCleanerInterface,
        decTalkSettingsRepository: DecTalkSettingsRepositoryInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(decTalkHelper, DecTalkHelperInterface):
            raise TypeError(f'decTalkHelper argument is malformed: \"{decTalkHelper}\"')
        elif not isinstance(decTalkMessageCleaner, DecTalkMessageCleanerInterface):
            raise TypeError(f'decTalkMessageCleaner argument is malformed: \"{decTalkMessageCleaner}\"')
        elif not isinstance(decTalkSettingsRepository, DecTalkSettingsRepositoryInterface):
            raise TypeError(f'decTalkSettingsRepository argument is malformed: \"{decTalkSettingsRepository}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__decTalkHelper: Final[DecTalkHelperInterface] = decTalkHelper
        self.__decTalkMessageCleaner: Final[DecTalkMessageCleanerInterface] = decTalkMessageCleaner
        self.__decTalkSettingsRepository: Final[DecTalkSettingsRepositoryInterface] = decTalkSettingsRepository
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__timber: Final[TimberInterface] = timber
        self.__ttsCommandBuilder: Final[TtsCommandBuilderInterface] = ttsCommandBuilder
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__sharedInstance: DecTalkTtsManagerInterface | None = None

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True,
    ) -> DecTalkTtsManagerInterface | None:
        if not utils.isValidBool(useSharedSoundPlayerManager):
            raise TypeError(f'useSharedSoundPlayerManager argument is malformed: \"{useSharedSoundPlayerManager}\"')

        soundPlayerManager: SoundPlayerManagerInterface

        if useSharedSoundPlayerManager:
            soundPlayerManager = self.__soundPlayerManagerProvider.getSharedInstance()
        else:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()

        return DecTalkTtsManager(
            chatterPreferredTtsHelper = self.__chatterPreferredTtsHelper,
            decTalkHelper = self.__decTalkHelper,
            decTalkMessageCleaner = self.__decTalkMessageCleaner,
            decTalkSettingsRepository = self.__decTalkSettingsRepository,
            soundPlayerManager = soundPlayerManager,
            timber = self.__timber,
            ttsCommandBuilder = self.__ttsCommandBuilder,
            ttsSettingsRepository = self.__ttsSettingsRepository,
        )

    def getSharedInstance(self) -> DecTalkTtsManagerInterface | None:
        sharedInstance = self.__sharedInstance

        if sharedInstance is None:
            sharedInstance = self.constructNewInstance()
            self.__sharedInstance = sharedInstance

        return sharedInstance

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.DEC_TALK
