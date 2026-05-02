from typing import Final

from frozenlist import FrozenList

from .cutenessHelperInterface import CutenessHelperInterface
from ..exceptions import CutenessFeatureIsDisabledException
from ..models.preparedCutenessChampionsResult import PreparedCutenessChampionsResult
from ..models.preparedCutenessLeaderboardEntry import PreparedCutenessLeaderboardEntry
from ..models.preparedCutenessResult import PreparedCutenessResult
from ..repositories.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..settings.cutenessSettingsInterface import CutenessSettingsInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class CutenessHelper(CutenessHelperInterface):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        cutenessSettings: CutenessSettingsInterface,
        timber: TimberInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(cutenessSettings, CutenessSettingsInterface):
            raise TypeError(f'cutenessSettings argument is malformed: \"{cutenessSettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__cutenessRepository: Final[CutenessRepositoryInterface] = cutenessRepository
        self.__cutenessSettings: Final[CutenessSettingsInterface] = cutenessSettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

    async def fetchCuteness(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> PreparedCutenessResult:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__cutenessSettings.isEnabled():
            raise CutenessFeatureIsDisabledException()

        cutenessResult = await self.__cutenessRepository.fetchCuteness(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        chatterUserName = await self.__userIdsRepository.requireUserName(
            userId = chatterUserId,
            twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                twitchChannelId = twitchChannelId,
            ),
        )

        return PreparedCutenessResult(
            cutenessResult = cutenessResult,
            chatterUserLogin = chatterUserName,
            chatterUserName = chatterUserName,
        )

    async def fetchCutenessChampions(
        self,
        twitchChannelId: str,
    ) -> PreparedCutenessChampionsResult:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__cutenessSettings.isEnabled():
            raise CutenessFeatureIsDisabledException()

        cutenessChampionsResult = await self.__cutenessRepository.fetchCutenessChampions(
            twitchChannelId = twitchChannelId,
        )

        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId,
        )

        preparedChampions: FrozenList[PreparedCutenessLeaderboardEntry] = FrozenList()

        for index, cutenessChampion in enumerate(cutenessChampionsResult.champions):
            chatterUserName = await self.__userIdsRepository.fetchUserName(
                userId = cutenessChampion.chatterUserId,
                twitchAccessToken = twitchAccessToken,
            )

            if utils.isValidStr(chatterUserName):
                preparedChampions.append(PreparedCutenessLeaderboardEntry(
                    cutenessLeaderboardEntry = cutenessChampion,
                    chatterUserName = chatterUserName,
                ))
            else:
                self.__timber.log('CutenessHelper', f'Failed to fetch userName when fetching cuteness champions ({chatterUserName=}) ({index=}) ({cutenessChampion=}) ({cutenessChampionsResult=}) ({twitchChannelId=})')

        preparedChampions.freeze()

        return PreparedCutenessChampionsResult(
            champions = preparedChampions,
            twitchChannelId = twitchChannelId,
        )
