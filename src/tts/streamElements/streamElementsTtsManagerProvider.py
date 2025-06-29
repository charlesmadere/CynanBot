from typing import Final

from .streamElementsTtsManager import StreamElementsTtsManager
from .streamElementsTtsManagerInterface import StreamElementsTtsManagerInterface
from .streamElementsTtsManagerProviderInterface import StreamElementsTtsManagerProviderInterface
from ..commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...misc import utils as utils
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...streamElements.helper.streamElementsHelperInterface import StreamElementsHelperInterface
from ...streamElements.settings.streamElementsSettingsRepositoryInterface import \
    StreamElementsSettingsRepositoryInterface
from ...streamElements.streamElementsMessageCleanerInterface import StreamElementsMessageCleanerInterface
from ...timber.timberInterface import TimberInterface


class StreamElementsTtsManagerProvider(StreamElementsTtsManagerProviderInterface):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        streamElementsHelper: StreamElementsHelperInterface,
        streamElementsMessageCleaner: StreamElementsMessageCleanerInterface,
        streamElementsSettingsRepository: StreamElementsSettingsRepositoryInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(streamElementsHelper, StreamElementsHelperInterface):
            raise TypeError(f'streamElementsHelper argument is malformed: \"{streamElementsHelper}\"')
        elif not isinstance(streamElementsMessageCleaner, StreamElementsMessageCleanerInterface):
            raise TypeError(f'streamElementsMessageCleaner argument is malformed: \"{streamElementsMessageCleaner}\"')
        elif not isinstance(streamElementsSettingsRepository, StreamElementsSettingsRepositoryInterface):
            raise TypeError(f'streamElementsSettingsRepository argument is malformed: \"{streamElementsSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__streamElementsHelper: Final[StreamElementsHelperInterface] = streamElementsHelper
        self.__streamElementsMessageCleaner: Final[StreamElementsMessageCleanerInterface] = streamElementsMessageCleaner
        self.__streamElementsSettingsRepository: Final[StreamElementsSettingsRepositoryInterface] = streamElementsSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__ttsCommandBuilder: Final[TtsCommandBuilderInterface] = ttsCommandBuilder
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__sharedInstance: StreamElementsTtsManagerInterface | None = None

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> StreamElementsTtsManagerInterface | None:
        if not utils.isValidBool(useSharedSoundPlayerManager):
            raise TypeError(f'useSharedSoundPlayerManager argument is malformed: \"{useSharedSoundPlayerManager}\"')

        soundPlayerManager: SoundPlayerManagerInterface

        if useSharedSoundPlayerManager:
            soundPlayerManager = self.__soundPlayerManagerProvider.getSharedInstance()
        else:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()

        return StreamElementsTtsManager(
            chatterPreferredTtsHelper = self.__chatterPreferredTtsHelper,
            soundPlayerManager = soundPlayerManager,
            streamElementsHelper = self.__streamElementsHelper,
            streamElementsMessageCleaner = self.__streamElementsMessageCleaner,
            streamElementsSettingsRepository = self.__streamElementsSettingsRepository,
            timber = self.__timber,
            ttsCommandBuilder = self.__ttsCommandBuilder,
            ttsSettingsRepository = self.__ttsSettingsRepository
        )

    def getSharedInstance(self) -> StreamElementsTtsManagerInterface | None:
        sharedInstance = self.__sharedInstance

        if sharedInstance is None:
            sharedInstance = self.constructNewInstance()
            self.__sharedInstance = sharedInstance

        return sharedInstance
