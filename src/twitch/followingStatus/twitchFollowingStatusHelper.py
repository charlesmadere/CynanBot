import traceback
from typing import Final

from .preparedTwitchFollowingStatus import PreparedTwitchFollowingStatus
from .twitchFollowingStatusHelperInterface import TwitchFollowingStatusHelperInterface
from .twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ..exceptions import TwitchAccessTokenMissingException
from ..tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..userIds.exceptions import NoTwitchUserDataFoundException
from ..userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TwitchFollowingStatusHelper(TwitchFollowingStatusHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchFollowingStatusRepository: Final[TwitchFollowingStatusRepositoryInterface] = twitchFollowingStatusRepository
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper

    async def fetch(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> PreparedTwitchFollowingStatus | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        try:
            twitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
                twitchChannelId = twitchChannelId,
            )
        except TwitchAccessTokenMissingException as e:
            self.__timber.log('TwitchFollowingStatusHelper', f'Failed to fetch Twitch access token ({twitchChannelId=}) ({userId=})', e, traceback.format_exc())
            return None

        try:
            userData = await self.__twitchUserIdsHelper.requireById(
                userId = userId,
                twitchAccessToken = twitchAccessToken,
            )
        except NoTwitchUserDataFoundException as e:
            self.__timber.log('TwitchFollowingStatusHelper', f'Failed to fetch Twitch user data ({twitchChannelId=}) ({userId=})', e, traceback.format_exc())
            return None

        followingStatus = await self.__twitchFollowingStatusRepository.fetchFollowingStatus(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userId = userId,
        )

        if followingStatus is None:
            self.__timber.log('TwitchFollowingStatusHelper', f'The given user is not following ({followingStatus=}) ({userData=}) ({twitchChannelId=}) ({userId=})')
            return None

        now = self.__timeZoneRepository.getNow()
        followingDurationSeconds = max(int(round((now - followingStatus.followedAt).total_seconds())), 0)

        durationMessage = utils.secondsToDurationMessage(
            secondsDuration = followingDurationSeconds,
            includeMinutesAndSeconds = True,
        )

        shorthandDurationMessage = utils.secondsToShorthandDurationMessage(
            secondsDuration = followingDurationSeconds,
        )

        return PreparedTwitchFollowingStatus(
            followingDurationSeconds = followingDurationSeconds,
            followingStatus = followingStatus,
            durationMessage = durationMessage,
            shorthandDurationMessage = shorthandDurationMessage,
            userLogin = userData.getUserLogin(),
            userName = userData.getUserName(),
        )
