from dataclasses import dataclass

from .guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from .timeoutActionData import TimeoutActionData
from .timeoutActionHelperInterface import TimeoutActionHelperInterface
from .timeoutActionHistoryRepositoryInterface import TimeoutActionHistoryRepositoryInterface
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ..twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ..twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ..twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from ..twitch.twitchConstantsInterface import TwitchConstantsInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface


class TimeoutActionHelper(TimeoutActionHelperInterface):

    @dataclass(frozen = True)
    class DiceRoll:
        dieSize: int
        roll: int

    @dataclass(frozen = True)
    class RollFailureData:
        baseFailureProbability: float
        failureProbability: float
        maxBullyFailureProbability: float
        perBullyFailureProbabilityIncrease: float
        reverseProbability: float
        bullyOccurrences: int
        failureRoll: int
        maxBullyFailureOccurrences: int
        reverseRoll: int

    def __init__(
        self,
        guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchConstants: TwitchConstantsInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(guaranteedTimeoutUsersRepository, GuaranteedTimeoutUsersRepositoryInterface):
            raise TypeError(f'guaranteedTimeoutUsersRepository argument is malformed: \"{guaranteedTimeoutUsersRepository}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timeoutActionHistoryRepository, TimeoutActionHistoryRepositoryInterface):
            raise TypeError(f'timeoutActionHistoryRepository argument is malformed: \"{timeoutActionHistoryRepository}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchConstants, TwitchConstantsInterface):
            raise TypeError(f'twitchConstants argument is malformed: \"{twitchConstants}\"')
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface = guaranteedTimeoutUsersRepository
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface = timeoutActionHistoryRepository
        self.__trollmojiHelper: TrollmojiHelperInterface = trollmojiHelper
        self.__twitchConstants: TwitchConstantsInterface = twitchConstants
        self.__twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface = twitchFollowingStatusRepository
        self.__twitchTimeoutHelper: TwitchTimeoutHelperInterface = twitchTimeoutHelper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    async def timeout(self, data: TimeoutActionData) -> bool:
        if not isinstance(data, TimeoutActionData):
            raise TypeError(f'data argument is malformed: \"{data}\"')

        return False
