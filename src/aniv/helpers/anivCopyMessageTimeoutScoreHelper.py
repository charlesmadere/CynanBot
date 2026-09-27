from typing import Final

from .anivCopyMessageTimeoutScoreHelperInterface import AnivCopyMessageTimeoutScoreHelperInterface
from ..models.anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from ..models.preparedAnivCopyMessageTimeoutScore import PreparedAnivCopyMessageTimeoutScore
from ..repositories.anivCopyMessageTimeoutScoreRepositoryInterface import AnivCopyMessageTimeoutScoreRepositoryInterface
from ..settings.anivSettingsInterface import AnivSettingsInterface
from ...misc import utils as utils
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface


class AnivCopyMessageTimeoutScoreHelper(AnivCopyMessageTimeoutScoreHelperInterface):

    def __init__(
        self,
        anivCopyMessageTimeoutScoreRepository: AnivCopyMessageTimeoutScoreRepositoryInterface,
        anivSettings: AnivSettingsInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
    ):
        if not isinstance(anivCopyMessageTimeoutScoreRepository, AnivCopyMessageTimeoutScoreRepositoryInterface):
            raise TypeError(f'anivCopyMessageTimeoutScoreRepository argument is malformed: \"{anivCopyMessageTimeoutScoreRepository}\"')
        elif not isinstance(anivSettings, AnivSettingsInterface):
            raise TypeError(f'anivSettings argument is malformed: \"{anivSettings}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')

        self.__anivCopyMessageTimeoutScoreRepository: Final[AnivCopyMessageTimeoutScoreRepositoryInterface] = anivCopyMessageTimeoutScoreRepository
        self.__anivSettings: Final[AnivSettingsInterface] = anivSettings
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper

    async def getScore(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> PreparedAnivCopyMessageTimeoutScore:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId,
        )

        chatterUserData = await self.__twitchUserIdsHelper.requireById(
            userId = chatterUserId,
            twitchAccessToken = twitchAccessToken,
        )

        twitchChannelData = await self.__twitchUserIdsHelper.requireById(
            userId = twitchChannelId,
            twitchAccessToken = twitchAccessToken,
        )

        if not await self.__anivSettings.areCopyMessageTimeoutsEnabled():
            return PreparedAnivCopyMessageTimeoutScore(
                score = AnivCopyMessageTimeoutScore(
                    mostRecentDodge = None,
                    mostRecentTimeout = None,
                    dodgeScore = 0,
                    timeoutScore = 0,
                    chatterUserId = chatterUserId,
                    twitchChannelId = twitchChannelId,
                ),
                twitchChannel = twitchChannelData.userLogin,
                chatterUserData = chatterUserData,
            )

        score = await self.__anivCopyMessageTimeoutScoreRepository.getScore(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        return PreparedAnivCopyMessageTimeoutScore(
            score = score,
            twitchChannel = twitchChannelData.userLogin,
            chatterUserData = chatterUserData,
        )
