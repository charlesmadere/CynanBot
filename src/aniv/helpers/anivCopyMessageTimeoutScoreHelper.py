from typing import Final

from .anivCopyMessageTimeoutScoreHelperInterface import AnivCopyMessageTimeoutScoreHelperInterface
from ..models.anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from ..models.preparedAnivCopyMessageTimeoutScore import PreparedAnivCopyMessageTimeoutScore
from ..repositories.anivCopyMessageTimeoutScoreRepositoryInterface import AnivCopyMessageTimeoutScoreRepositoryInterface
from ..settings.anivSettingsInterface import AnivSettingsInterface
from ...misc import utils as utils
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class AnivCopyMessageTimeoutScoreHelper(AnivCopyMessageTimeoutScoreHelperInterface):

    def __init__(
        self,
        anivCopyMessageTimeoutScoreRepository: AnivCopyMessageTimeoutScoreRepositoryInterface,
        anivSettings: AnivSettingsInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(anivCopyMessageTimeoutScoreRepository, AnivCopyMessageTimeoutScoreRepositoryInterface):
            raise TypeError(f'anivCopyMessageTimeoutScoreRepository argument is malformed: \"{anivCopyMessageTimeoutScoreRepository}\"')
        elif not isinstance(anivSettings, AnivSettingsInterface):
            raise TypeError(f'anivSettings argument is malformed: \"{anivSettings}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__anivCopyMessageTimeoutScoreRepository: Final[AnivCopyMessageTimeoutScoreRepositoryInterface] = anivCopyMessageTimeoutScoreRepository
        self.__anivSettings: Final[AnivSettingsInterface] = anivSettings
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

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

        chatterUserName = await self.__userIdsRepository.requireUserName(
            userId = chatterUserId,
            twitchAccessToken = twitchAccessToken,
        )

        twitchChannel = await self.__userIdsRepository.requireUserName(
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
                chatterUserName = chatterUserName,
                twitchChannel = twitchChannel,
            )

        score = await self.__anivCopyMessageTimeoutScoreRepository.getScore(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        return PreparedAnivCopyMessageTimeoutScore(
            score = score,
            chatterUserName = chatterUserName,
            twitchChannel = twitchChannel,
        )
