from typing import Final

from frozenlist import FrozenList

from .cutenessHelperInterface import CutenessHelperInterface
from ..exceptions import CutenessFeatureIsDisabledException
from ..models.preparedCutenessChampionsResult import PreparedCutenessChampionsResult
from ..models.preparedCutenessLeaderboardEntry import PreparedCutenessLeaderboardEntry
from ..models.preparedCutenessLeaderboardHistoryResult import PreparedCutenessLeaderboardHistoryResult
from ..models.preparedCutenessLeaderboardResult import PreparedCutenessLeaderboardResult
from ..models.preparedCutenessResult import PreparedCutenessResult
from ..models.preparedIncrementedCutenessResult import PreparedIncrementedCutenessResult
from ..repositories.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..settings.cutenessSettingsInterface import CutenessSettingsInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...twitch.userIds.twitchUserData import TwitchUserData
from ...twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface


class CutenessHelper(CutenessHelperInterface):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        cutenessSettings: CutenessSettingsInterface,
        timber: TimberInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(cutenessSettings, CutenessSettingsInterface):
            raise TypeError(f'cutenessSettings argument is malformed: \"{cutenessSettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')

        self.__cutenessRepository: Final[CutenessRepositoryInterface] = cutenessRepository
        self.__cutenessSettings: Final[CutenessSettingsInterface] = cutenessSettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper

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

        chatterUserData = await self.__twitchUserIdsHelper.requireById(
            userId = chatterUserId,
            twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                twitchChannelId = twitchChannelId,
            ),
        )

        return PreparedCutenessResult(
            cutenessResult = cutenessResult,
            chatterUserLogin = chatterUserData.userLogin,
            chatterUserName = chatterUserData.userName,
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

        champions: FrozenList[PreparedCutenessLeaderboardEntry] = FrozenList()

        for index, champion in enumerate(cutenessChampionsResult.champions):
            chatterUserData = await self.__twitchUserIdsHelper.getById(
                userId = champion.chatterUserId,
                twitchAccessToken = twitchAccessToken,
            )

            if chatterUserData is None:
                self.__timber.log('CutenessHelper', f'Failed to fetch user when fetching cuteness champion ({chatterUserData=}) ({index=}) ({champion=}) ({cutenessChampionsResult=}) ({twitchChannelId=})')
            else:
                champions.append(PreparedCutenessLeaderboardEntry(
                    cutenessLeaderboardEntry = champion,
                    chatterUserLogin = chatterUserData.userLogin,
                    chatterUserName = chatterUserData.userName,
                ))

        champions.freeze()

        return PreparedCutenessChampionsResult(
            champions = champions,
            twitchChannelId = twitchChannelId,
        )

    async def fetchCutenessIncrementedBy(
        self,
        incrementAmount: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> PreparedIncrementedCutenessResult:
        if not utils.isValidInt(incrementAmount):
            raise TypeError(f'incrementAmount argument is malformed: \"{incrementAmount}\"')
        elif incrementAmount < utils.getShortMinSafeSize() or incrementAmount > utils.getShortMaxSafeSize():
            raise ValueError(f'incrementAmount argument is out of bounds: {incrementAmount}')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__cutenessSettings.isEnabled():
            raise CutenessFeatureIsDisabledException()

        incrementedCutenessResult = await self.__cutenessRepository.fetchCutenessIncrementedBy(
            incrementAmount = incrementAmount,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        chatterUserData = await self.__twitchUserIdsHelper.requireById(
            userId = chatterUserId,
            twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                twitchChannelId = twitchChannelId,
            ),
        )

        return PreparedIncrementedCutenessResult(
            incrementedCutenessResult = incrementedCutenessResult,
            chatterUserLogin = chatterUserData.userLogin,
            chatterUserName = chatterUserData.userName,
        )

    async def fetchCutenessLeaderboard(
        self,
        twitchChannelId: str,
        specificLookupUserId: str | None = None,
    ) -> PreparedCutenessLeaderboardResult:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif specificLookupUserId is not None and not isinstance(specificLookupUserId, str):
            raise TypeError(f'specificLookupUserId argument is malformed: \"{specificLookupUserId}\"')

        if not await self.__cutenessSettings.isEnabled():
            raise CutenessFeatureIsDisabledException()

        cutenessLeaderboardResult = await self.__cutenessRepository.fetchCutenessLeaderboard(
            twitchChannelId = twitchChannelId,
            specificLookupUserId = specificLookupUserId,
        )

        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId,
        )

        specificLookupCutenessResult: PreparedCutenessResult | None = None

        if cutenessLeaderboardResult.specificLookupCutenessResult is not None:
            lookupUserData = await self.__twitchUserIdsHelper.getById(
                userId = cutenessLeaderboardResult.specificLookupCutenessResult.chatterUserId,
                twitchAccessToken = twitchAccessToken,
            )

            if lookupUserData is None:
                self.__timber.log('CutenessHelper', f'Failed to fetch user when fetching specific cuteness lookup ({lookupUserData=}) ({cutenessLeaderboardResult=}) ({twitchChannelId=})')
            else:
                specificLookupCutenessResult = PreparedCutenessResult(
                    cutenessResult = cutenessLeaderboardResult.specificLookupCutenessResult,
                    chatterUserLogin = lookupUserData.userLogin,
                    chatterUserName = lookupUserData.userName,
                )

        entries: FrozenList[PreparedCutenessLeaderboardEntry] = FrozenList()

        for index, entry in enumerate(cutenessLeaderboardResult.entries):
            chatterUserData = await self.__twitchUserIdsHelper.getById(
                userId = entry.chatterUserId,
                twitchAccessToken = twitchAccessToken,
            )

            if chatterUserData is None:
                self.__timber.log('CutenessHelper', f'Failed to fetch user when fetching leaderboard entry ({chatterUserData=}) ({index=}) ({entry=}) ({cutenessLeaderboardResult=}) ({twitchChannelId=})')
            else:
                entries.append(PreparedCutenessLeaderboardEntry(
                    cutenessLeaderboardEntry = entry,
                    chatterUserLogin = chatterUserData.userLogin,
                    chatterUserName = chatterUserData.userName,
                ))

        entries.freeze()

        return PreparedCutenessLeaderboardResult(
            cutenessLeaderboardResult = cutenessLeaderboardResult,
            entries = entries,
            specificLookupCutenessResult = specificLookupCutenessResult,
        )

    async def fetchCutenessLeaderboardHistory(
        self,
        twitchChannelId: str,
    ) -> PreparedCutenessLeaderboardHistoryResult:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__cutenessSettings.isEnabled():
            raise CutenessFeatureIsDisabledException()

        leaderboardHistoryResult = await self.__cutenessRepository.fetchCutenessLeaderboardHistory(
            twitchChannelId = twitchChannelId,
        )

        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId,
        )

        cachedChatters: dict[str, TwitchUserData | None] = dict()
        history: FrozenList[PreparedCutenessLeaderboardResult] = FrozenList()

        for leaderboardHistory in leaderboardHistoryResult.history:
            entries: FrozenList[PreparedCutenessLeaderboardEntry] = FrozenList()

            for entry in leaderboardHistory.entries:
                if entry.chatterUserId not in cachedChatters:
                    chatterUserData = await self.__twitchUserIdsHelper.getById(
                        userId = entry.chatterUserId,
                        twitchAccessToken = twitchAccessToken,
                    )

                    cachedChatters[entry.chatterUserId] = chatterUserData

                chatterUserData = cachedChatters.get(entry.chatterUserId, None)

                if chatterUserData is None:
                    self.__timber.log('CutenessHelper', f'Failed to fetch user when fetching leaderboard entry ({chatterUserData=}) ({entry=}) ({leaderboardHistory=}) ({twitchChannelId=})')
                else:
                    entries.append(PreparedCutenessLeaderboardEntry(
                        cutenessLeaderboardEntry = entry,
                        chatterUserLogin = chatterUserData.getUserLogin(),
                        chatterUserName = chatterUserData.getUserName(),
                    ))

            entries.freeze()

            history.append(PreparedCutenessLeaderboardResult(
                cutenessLeaderboardResult = leaderboardHistory,
                entries = entries,
                specificLookupCutenessResult = None,
            ))

        history.freeze()

        return PreparedCutenessLeaderboardHistoryResult(
            history = history,
            twitchChannelId = twitchChannelId,
        )
