from typing import Final

from .compositeTtsManagerProviderInterface import CompositeTtsManagerProviderInterface
from ..commodoreSam.commodoreSamTtsManagerInterface import CommodoreSamTtsManagerInterface
from ..compositeTtsManager import CompositeTtsManager
from ..compositeTtsManagerInterface import CompositeTtsManagerInterface
from ..decTalk.decTalkTtsManagerInterface import DecTalkTtsManagerInterface
from ..google.googleTtsManagerInterface import GoogleTtsManagerInterface
from ..halfLife.halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from ..microsoft.microsoftTtsManagerInterface import MicrosoftTtsManagerInterface
from ..microsoftSam.microsoftSamTtsManagerInterface import MicrosoftSamTtsManagerInterface
from ..settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ..streamElements.streamElementsTtsManagerInterface import StreamElementsTtsManagerInterface
from ..ttsMonster.ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
from ...chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface


class CompositeTtsManagerProvider(CompositeTtsManagerProviderInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface | None,
        commodoreSamTtsManager: CommodoreSamTtsManagerInterface | None,
        decTalkTtsManager: DecTalkTtsManagerInterface | None,
        googleTtsManager: GoogleTtsManagerInterface | None,
        halfLifeTtsManager: HalfLifeTtsManagerInterface | None,
        microsoftTtsManager: MicrosoftTtsManagerInterface | None,
        microsoftSamTtsManager: MicrosoftSamTtsManagerInterface | None,
        singingDecTalkTtsManager: DecTalkTtsManagerInterface | None,
        streamElementsTtsManager: StreamElementsTtsManagerInterface | None,
        timber: TimberInterface,
        ttsMonsterTtsManager: TtsMonsterTtsManagerInterface | None,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif chatterPreferredTtsHelper is not None and not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif commodoreSamTtsManager is not None and not isinstance(commodoreSamTtsManager, CommodoreSamTtsManagerInterface):
            raise TypeError(f'commodoreSamTtsManager argument is malformed: \"{commodoreSamTtsManager}\"')
        elif decTalkTtsManager is not None and not isinstance(decTalkTtsManager, DecTalkTtsManagerInterface):
            raise TypeError(f'decTalkTtsManager argument is malformed: \"{decTalkTtsManager}\"')
        elif googleTtsManager is not None and not isinstance(googleTtsManager, GoogleTtsManagerInterface):
            raise TypeError(f'googleTtsManager argument is malformed: \"{googleTtsManager}\"')
        elif halfLifeTtsManager is not None and not isinstance(halfLifeTtsManager, HalfLifeTtsManagerInterface):
            raise TypeError(f'halfLifeTtsManager argument is malformed: \"{halfLifeTtsManager}\"')
        elif microsoftTtsManager is not None and not isinstance(microsoftTtsManager, MicrosoftTtsManagerInterface):
            raise TypeError(f'microsoftTtsManager argument is malformed: \"{microsoftTtsManager}\"')
        elif microsoftSamTtsManager is not None and not isinstance(microsoftSamTtsManager, MicrosoftSamTtsManagerInterface):
            raise TypeError(f'microsoftSamTtsManager argument is malformed: \"{microsoftSamTtsManager}\"')
        elif singingDecTalkTtsManager is not None and not isinstance(singingDecTalkTtsManager, DecTalkTtsManagerInterface):
            raise TypeError(f'singingDecTalkTtsManager argument is malformed: \"{singingDecTalkTtsManager}\"')
        elif streamElementsTtsManager is not None and not isinstance(streamElementsTtsManager, StreamElementsTtsManagerInterface):
            raise TypeError(f'streamElementsTtsManager argument is malformed: \"{streamElementsTtsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif ttsMonsterTtsManager is not None and not isinstance(ttsMonsterTtsManager, TtsMonsterTtsManagerInterface):
            raise TypeError(f'ttsMonsterTtsManager argument is malformed: \"{ttsMonsterTtsManager}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface | None] = chatterPreferredTtsHelper
        self.__commodoreSamTtsManager: Final[CommodoreSamTtsManagerInterface | None] = commodoreSamTtsManager
        self.__decTalkTtsManager: Final[DecTalkTtsManagerInterface | None] = decTalkTtsManager
        self.__googleTtsManager: Final[GoogleTtsManagerInterface | None] = googleTtsManager
        self.__halfLifeTtsManager: Final[HalfLifeTtsManagerInterface | None] = halfLifeTtsManager
        self.__microsoftTtsManager: Final[MicrosoftTtsManagerInterface | None] = microsoftTtsManager
        self.__microsoftSamTtsManager: Final[MicrosoftSamTtsManagerInterface | None] = microsoftSamTtsManager
        self.__singingDecTalkTtsManager: Final[DecTalkTtsManagerInterface | None] = singingDecTalkTtsManager
        self.__streamElementsTtsManager: Final[StreamElementsTtsManagerInterface | None] = streamElementsTtsManager
        self.__timber: Final[TimberInterface] = timber
        self.__ttsMonsterTtsManager: Final[TtsMonsterTtsManagerInterface | None] = ttsMonsterTtsManager
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository

        self.__compositeTtsManager: CompositeTtsManagerInterface | None = None

    def constructNewCompositeTtsManagerInstance(self) -> CompositeTtsManagerInterface:
        return CompositeTtsManager(
            backgroundTaskHelper = self.__backgroundTaskHelper,
            chatterPreferredTtsHelper = self.__chatterPreferredTtsHelper,
            commodoreSamTtsManager = self.__commodoreSamTtsManager,
            decTalkTtsManager = self.__decTalkTtsManager,
            googleTtsManager = self.__googleTtsManager,
            halfLifeTtsManager = self.__halfLifeTtsManager,
            microsoftTtsManager = self.__microsoftTtsManager,
            microsoftSamTtsManager = self.__microsoftSamTtsManager,
            singingDecTalkTtsManager = self.__singingDecTalkTtsManager,
            streamElementsTtsManager = self.__streamElementsTtsManager,
            timber = self.__timber,
            ttsMonsterTtsManager = self.__ttsMonsterTtsManager,
            ttsSettingsRepository = self.__ttsSettingsRepository
        )

    def getSharedCompositeTtsManagerInstance(self) -> CompositeTtsManagerInterface:
        compositeTtsManager = self.__compositeTtsManager

        if compositeTtsManager is None:
            compositeTtsManager = self.constructNewCompositeTtsManagerInstance()
            self.__compositeTtsManager = compositeTtsManager

        return compositeTtsManager
