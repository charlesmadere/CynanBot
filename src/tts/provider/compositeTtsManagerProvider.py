from typing import Final

from .compositeTtsManagerProviderInterface import CompositeTtsManagerProviderInterface
from ..commodoreSam.commodoreSamTtsManagerProviderInterface import CommodoreSamTtsManagerProviderInterface
from ..compositeTtsManager import CompositeTtsManager
from ..compositeTtsManagerInterface import CompositeTtsManagerInterface
from ..decTalk.decTalkTtsManagerProviderInterface import DecTalkTtsManagerProviderInterface
from ..google.googleTtsManagerProviderInterface import GoogleTtsManagerProviderInterface
from ..halfLife.halfLifeTtsManagerProviderInterface import HalfLifeTtsManagerProviderInterface
from ..microsoft.microsoftTtsManagerProviderInterface import MicrosoftTtsManagerProviderInterface
from ..microsoftSam.microsoftSamTtsManagerProviderInterface import MicrosoftSamTtsManagerProviderInterface
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ..shotgun.shotgunTtsManagerProviderInterface import ShotgunTtsManagerProviderInterface
from ..streamElements.streamElementsTtsManagerProviderInterface import StreamElementsTtsManagerProviderInterface
from ..ttsMonster.ttsMonsterTtsManagerProviderInterface import TtsMonsterTtsManagerProviderInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface


class CompositeTtsManagerProvider(CompositeTtsManagerProviderInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface | None,
        commodoreSamTtsManagerProvider: CommodoreSamTtsManagerProviderInterface,
        decTalkTtsManagerProvider: DecTalkTtsManagerProviderInterface,
        googleTtsManagerProvider: GoogleTtsManagerProviderInterface,
        halfLifeTtsManagerProvider: HalfLifeTtsManagerProviderInterface,
        microsoftTtsManagerProvider: MicrosoftTtsManagerProviderInterface,
        microsoftSamTtsManagerProvider: MicrosoftSamTtsManagerProviderInterface,
        shotgunTtsManagerProvider: ShotgunTtsManagerProviderInterface,
        singingDecTalkTtsManagerProvider: DecTalkTtsManagerProviderInterface,
        streamElementsTtsManagerProvider: StreamElementsTtsManagerProviderInterface,
        timber: TimberInterface,
        ttsMonsterTtsManagerProvider: TtsMonsterTtsManagerProviderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif chatterPreferredTtsHelper is not None and not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(commodoreSamTtsManagerProvider, CommodoreSamTtsManagerProviderInterface):
            raise TypeError(f'commodoreSamTtsManagerProvider argument is malformed: \"{commodoreSamTtsManagerProvider}\"')
        elif not isinstance(decTalkTtsManagerProvider, DecTalkTtsManagerProviderInterface):
            raise TypeError(f'decTalkTtsManagerProvider argument is malformed: \"{decTalkTtsManagerProvider}\"')
        elif not isinstance(googleTtsManagerProvider, GoogleTtsManagerProviderInterface):
            raise TypeError(f'googleTtsManagerProvider argument is malformed: \"{googleTtsManagerProvider}\"')
        elif not isinstance(halfLifeTtsManagerProvider, HalfLifeTtsManagerProviderInterface):
            raise TypeError(f'halfLifeTtsManagerProvider argument is malformed: \"{halfLifeTtsManagerProvider}\"')
        elif not isinstance(microsoftTtsManagerProvider, MicrosoftTtsManagerProviderInterface):
            raise TypeError(f'microsoftTtsManagerProvider argument is malformed: \"{microsoftTtsManagerProvider}\"')
        elif not isinstance(microsoftSamTtsManagerProvider, MicrosoftSamTtsManagerProviderInterface):
            raise TypeError(f'microsoftSamTtsManagerProvider argument is malformed: \"{microsoftSamTtsManagerProvider}\"')
        elif not isinstance(shotgunTtsManagerProvider, ShotgunTtsManagerProviderInterface):
            raise TypeError(f'shotgunTtsManagerProvider argument is malformed: \"{shotgunTtsManagerProvider}\"')
        elif not isinstance(singingDecTalkTtsManagerProvider, DecTalkTtsManagerProviderInterface):
            raise TypeError(f'singingDecTalkTtsManagerProvider argument is malformed: \"{singingDecTalkTtsManagerProvider}\"')
        elif not isinstance(streamElementsTtsManagerProvider, StreamElementsTtsManagerProviderInterface):
            raise TypeError(f'streamElementsTtsManagerProvider argument is malformed: \"{streamElementsTtsManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterTtsManagerProvider, TtsMonsterTtsManagerProviderInterface):
            raise TypeError(f'ttsMonsterTtsManagerProvider argument is malformed: \"{ttsMonsterTtsManagerProvider}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface | None] = chatterPreferredTtsHelper
        self.__commodoreSamTtsManagerProvider: Final[CommodoreSamTtsManagerProviderInterface] = commodoreSamTtsManagerProvider
        self.__decTalkTtsManagerProvider: Final[DecTalkTtsManagerProviderInterface] = decTalkTtsManagerProvider
        self.__googleTtsManagerProvider: Final[GoogleTtsManagerProviderInterface] = googleTtsManagerProvider
        self.__halfLifeTtsManagerProvider: Final[HalfLifeTtsManagerProviderInterface] = halfLifeTtsManagerProvider
        self.__microsoftTtsManagerProvider: Final[MicrosoftTtsManagerProviderInterface] = microsoftTtsManagerProvider
        self.__microsoftSamTtsManagerProvider: Final[MicrosoftSamTtsManagerProviderInterface] = microsoftSamTtsManagerProvider
        self.__shotgunTtsManagerProvider: Final[ShotgunTtsManagerProviderInterface] = shotgunTtsManagerProvider
        self.__singingDecTalkTtsManagerProvider: Final[DecTalkTtsManagerProviderInterface] = singingDecTalkTtsManagerProvider
        self.__streamElementsTtsManagerProvider: Final[StreamElementsTtsManagerProviderInterface] = streamElementsTtsManagerProvider
        self.__timber: Final[TimberInterface] = timber
        self.__ttsMonsterTtsManagerProvider: Final[TtsMonsterTtsManagerProviderInterface] = ttsMonsterTtsManagerProvider
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__sharedInstance: CompositeTtsManagerInterface | None = None

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> CompositeTtsManagerInterface:
        if not utils.isValidBool(useSharedSoundPlayerManager):
            raise TypeError(f'useSharedSoundPlayerManager argument is malformed: \"{useSharedSoundPlayerManager}\"')

        commodoreSamTtsManager = self.__commodoreSamTtsManagerProvider.constructNewInstance(
            useSharedSoundPlayerManager = useSharedSoundPlayerManager
        )

        decTalkTtsManager = self.__decTalkTtsManagerProvider.constructNewInstance(
            useSharedSoundPlayerManager = useSharedSoundPlayerManager
        )

        googleTtsManager = self.__googleTtsManagerProvider.constructNewInstance(
            useSharedSoundPlayerManager = useSharedSoundPlayerManager
        )

        halfLifeTtsManager = self.__halfLifeTtsManagerProvider.constructNewInstance(
            useSharedSoundPlayerManager = useSharedSoundPlayerManager
        )

        microsoftTtsManager = self.__microsoftTtsManagerProvider.constructNewInstance(
            useSharedSoundPlayerManager = useSharedSoundPlayerManager
        )

        microsoftSamTtsManager = self.__microsoftSamTtsManagerProvider.constructNewInstance(
            useSharedSoundPlayerManager = useSharedSoundPlayerManager
        )

        shotgunTtsManager = self.__shotgunTtsManagerProvider.constructNewInstance(
            useSharedSoundPlayerManager = useSharedSoundPlayerManager
        )

        singingDecTalkTtsManager = self.__singingDecTalkTtsManagerProvider.constructNewInstance(
            useSharedSoundPlayerManager = useSharedSoundPlayerManager
        )

        streamElementsTtsManager = self.__streamElementsTtsManagerProvider.constructNewInstance(
            useSharedSoundPlayerManager = useSharedSoundPlayerManager
        )

        ttsMonsterTtsManager = self.__ttsMonsterTtsManagerProvider.constructNewInstance(
            useSharedSoundPlayerManager = useSharedSoundPlayerManager
        )

        return CompositeTtsManager(
            backgroundTaskHelper = self.__backgroundTaskHelper,
            chatterPreferredTtsHelper = self.__chatterPreferredTtsHelper,
            commodoreSamTtsManager = commodoreSamTtsManager,
            decTalkTtsManager = decTalkTtsManager,
            googleTtsManager = googleTtsManager,
            halfLifeTtsManager = halfLifeTtsManager,
            microsoftTtsManager = microsoftTtsManager,
            microsoftSamTtsManager = microsoftSamTtsManager,
            shotgunTtsManager = shotgunTtsManager,
            singingDecTalkTtsManager = singingDecTalkTtsManager,
            streamElementsTtsManager = streamElementsTtsManager,
            timber = self.__timber,
            ttsMonsterTtsManager = ttsMonsterTtsManager,
            ttsSettingsRepository = self.__ttsSettingsRepository,
        )

    def getSharedInstance(self) -> CompositeTtsManagerInterface:
        sharedInstance = self.__sharedInstance

        if sharedInstance is not None:
            return sharedInstance

        commodoreSamTtsManager = self.__commodoreSamTtsManagerProvider.getSharedInstance()
        decTalkTtsManager = self.__decTalkTtsManagerProvider.getSharedInstance()
        googleTtsManager = self.__googleTtsManagerProvider.getSharedInstance()
        halfLifeTtsManager = self.__halfLifeTtsManagerProvider.getSharedInstance()
        microsoftTtsManager = self.__microsoftTtsManagerProvider.getSharedInstance()
        microsoftSamTtsManager = self.__microsoftSamTtsManagerProvider.getSharedInstance()
        shotgunTtsManager = self.__shotgunTtsManagerProvider.getSharedInstance()
        singingDecTalkTtsManager = self.__singingDecTalkTtsManagerProvider.getSharedInstance()
        streamElementsTtsManager = self.__streamElementsTtsManagerProvider.getSharedInstance()
        ttsMonsterTtsManager = self.__ttsMonsterTtsManagerProvider.getSharedInstance()

        sharedInstance = CompositeTtsManager(
            backgroundTaskHelper = self.__backgroundTaskHelper,
            chatterPreferredTtsHelper = self.__chatterPreferredTtsHelper,
            commodoreSamTtsManager = commodoreSamTtsManager,
            decTalkTtsManager = decTalkTtsManager,
            googleTtsManager = googleTtsManager,
            halfLifeTtsManager = halfLifeTtsManager,
            microsoftTtsManager = microsoftTtsManager,
            microsoftSamTtsManager = microsoftSamTtsManager,
            shotgunTtsManager = shotgunTtsManager,
            singingDecTalkTtsManager = singingDecTalkTtsManager,
            streamElementsTtsManager = streamElementsTtsManager,
            timber = self.__timber,
            ttsMonsterTtsManager = ttsMonsterTtsManager,
            ttsSettingsRepository = self.__ttsSettingsRepository,
        )

        self.__sharedInstance = sharedInstance
        return sharedInstance
