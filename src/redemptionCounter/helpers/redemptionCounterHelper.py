from typing import Final

from .redemptionCounterHelperInterface import RedemptionCounterHelperInterface
from ..exceptions import RedemptionCounterIsDisabledException, RedemptionCounterNoSuchUserException
from ..models.preparedRedemptionCount import PreparedRedemptionCount
from ..models.redemptionCount import RedemptionCount
from ..repositories.redemptionCounterRepositoryInterface import RedemptionCounterRepositoryInterface
from ..settings.redemptionCounterSettingsInterface import RedemptionCounterSettingsInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class RedemptionCounterHelper(RedemptionCounterHelperInterface):

    def __init__(
        self,
        redemptionCounterRepository: RedemptionCounterRepositoryInterface,
        redemptionCounterSettings: RedemptionCounterSettingsInterface,
        timber: TimberInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(redemptionCounterRepository, RedemptionCounterRepositoryInterface):
            raise TypeError(f'redemptionCounterRepository argument is malformed: \"{redemptionCounterRepository}\"')
        elif not isinstance(redemptionCounterSettings, RedemptionCounterSettingsInterface):
            raise TypeError(f'redemptionCounterSettings argument is malformed: \"{redemptionCounterSettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__redemptionCounterRepository: Final[RedemptionCounterRepositoryInterface] = redemptionCounterRepository
        self.__redemptionCounterSettings: Final[RedemptionCounterSettingsInterface] = redemptionCounterSettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

    async def get(
        self,
        chatterUserId: str,
        counterName: str,
        twitchChannelId: str
    ) -> PreparedRedemptionCount:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(counterName):
            raise TypeError(f'counterName argument is malformed: \"{counterName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__redemptionCounterSettings.isEnabled():
            raise RedemptionCounterIsDisabledException(f'Redemption counter feature is currently disabled ({chatterUserId=}) ({counterName=}) ({twitchChannelId=})')

        redemptionCount = await self.__redemptionCounterRepository.get(
            chatterUserId = chatterUserId,
            counterName = counterName,
            twitchChannelId = twitchChannelId
        )

        return await self.__prepareRedemptionCount(
            redemptionCount = redemptionCount
        )

    async def increment(
        self,
        incrementAmount: int,
        chatterUserId: str,
        counterName: str,
        twitchChannelId: str
    ) -> PreparedRedemptionCount:
        if not utils.isValidInt(incrementAmount):
            raise TypeError(f'incrementAmount argument is malformed: \"{incrementAmount}\"')
        elif incrementAmount < 1 or incrementAmount > utils.getShortMaxSafeSize():
            raise ValueError(f'incrementAmount argument is out of bounds: {incrementAmount}')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(counterName):
            raise TypeError(f'counterName argument is malformed: \"{counterName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__redemptionCounterSettings.isEnabled():
            raise RedemptionCounterIsDisabledException(f'Redemption counter feature is currently disabled ({incrementAmount=}) ({chatterUserId=}) ({counterName=}) ({twitchChannelId=})')

        redemptionCount = await self.__redemptionCounterRepository.increment(
            incrementAmount = incrementAmount,
            chatterUserId = chatterUserId,
            counterName = counterName,
            twitchChannelId = twitchChannelId
        )

        return await self.__prepareRedemptionCount(
            redemptionCount = redemptionCount
        )

    async def __prepareRedemptionCount(
        self,
        redemptionCount: RedemptionCount
    ) -> PreparedRedemptionCount:
        chatterUserName = await self.__userIdsRepository.fetchUserName(
            userId = redemptionCount.chatterUserId,
            twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                twitchChannelId = redemptionCount.twitchChannelId
            )
        )

        if not utils.isValidStr(chatterUserName):
            self.__timber.log('RedemptionCounterHelper', f'Unable to find chatter user name when preparing redemption count ({redemptionCount=}) ({chatterUserName=})')

            raise RedemptionCounterNoSuchUserException(
                chatterUserId = redemptionCount.chatterUserId,
                counterName = redemptionCount.counterName,
                twitchChannelId = redemptionCount.twitchChannelId
            )

        return PreparedRedemptionCount(
            redemptionCount = redemptionCount,
            chatterUserName = chatterUserName
        )
