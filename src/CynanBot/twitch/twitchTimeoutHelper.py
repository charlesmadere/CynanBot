import traceback
from datetime import timedelta
from CynanBot.cheerActions.cheerAction import CheerAction
from CynanBot.cheerActions.cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from CynanBot.misc.simpleDateTime import SimpleDateTime
import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.api.twitchBannedUserRequest import TwitchBannedUserRequest
from CynanBot.twitch.api.twitchBannedUsersResponse import TwitchBannedUsersResponse
from CynanBot.twitch.api.twitchFollower import TwitchFollower
from CynanBot.twitch.api.twitchModUser import TwitchModUser
from CynanBot.twitch.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from CynanBot.twitch.twitchFollowerRepositoryInterface import TwitchFollowerRepositoryInterface
from CynanBot.twitch.twitchTimeoutHelperInterface import \
    TwitchTimeoutHelperInterface
from CynanBot.twitch.twitchTimeoutRemodData import TwitchTimeoutRemodData
from CynanBot.twitch.twitchTimeoutRemodHelperInterface import \
    TwitchTimeoutRemodHelperInterface
from CynanBot.users.userInterface import UserInterface


class TwitchTimeoutHelper(TwitchTimeoutHelperInterface):

    def __init__(
        self,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchFollowerRepository: TwitchFollowerRepositoryInterface,
        twitchTimeoutRemodHelper: TwitchTimeoutRemodHelperInterface,
        minimumFollowDuration: timedelta = timedelta(weeks = 1)
    ):
        if not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchFollowerRepository, TwitchFollowerRepositoryInterface):
            raise TypeError(f'twitchFollowerRepository argument is malformed: \"{twitchFollowerRepository}\"')
        elif not isinstance(twitchTimeoutRemodHelper, TwitchTimeoutRemodHelperInterface):
            raise TypeError(f'twitchTimeoutRemodHelper argument is malformed: \"{twitchTimeoutRemodHelper}\"')
        elif not isinstance(minimumFollowDuration, timedelta):
            raise TypeError(f'minimumFollowDuration argument is malformed: \"{minimumFollowDuration}\"')

        self.__isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface = isLiveOnTwitchRepository
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchFollowerRepository: TwitchFollowerRepositoryInterface = twitchFollowerRepository
        self.__twitchTimeoutRemodHelper: TwitchTimeoutRemodHelperInterface = twitchTimeoutRemodHelper
        self.__minimumFollowDuration: timedelta = minimumFollowDuration

    async def __isAlreadyCurrentlyBannedOrTimedOut(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str
    ) -> bool:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')

        bannedUsersResponse: TwitchBannedUsersResponse | None = None

        try:
            bannedUsersResponse = await self.__twitchApiService.fetchBannedUsers(
                twitchAccessToken = twitchAccessToken,
                bannedUserRequest = TwitchBannedUserRequest(
                    broadcasterId = twitchChannelId,
                    requestedUserId = userIdToTimeout
                )
            )
        except Exception as e:
            self.__timber.log('TwitchTimeoutHelper', f'Failed to verify if the given user ID can be timed out ({twitchChannelId=}) ({userIdToTimeout=}): {e}', e, traceback.format_exc())
            return False

        if bannedUsersResponse is None:
            return False

        bannedUsers = bannedUsersResponse.getUsers()

        if bannedUsers is None or len(bannedUsers) == 0:
            return False

        for bannedUser in bannedUsers:
            if bannedUser.getUserId() == userIdToTimeout:
                if bannedUser.getExpiresAt() is None:
                    self.__timber.log('TwitchTimeoutHelper', f'The given user ID will not be timed out as this user is banned: ({bannedUser=}) ({twitchChannelId=}) ({userIdToTimeout=})')
                else:
                    self.__timber.log('TwitchTimeoutHelper', f'The given user ID will not be timed out as this user is already timed out: ({bannedUser=}) ({twitchChannelId=}) ({userIdToTimeout=})')

                return True

        return False

    async def __isMod(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str
    ) -> bool:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')

        moderatorInfo: TwitchModUser | None = None

        try:
            moderatorInfo = await self.__twitchApiService.fetchModerator(
                broadcasterId = twitchChannelId,
                twitchAccessToken = twitchAccessToken,
                userId = userIdToTimeout
            )
        except Exception as e:
            self.__timber.log('TwitchTimeoutHelper', f'Failed to fetch Twitch moderator info for the given user ID ({twitchChannelId=}) ({userIdToTimeout=}): {e}', e, traceback.format_exc())
            return False

        return moderatorInfo is not None

    async def __isValidStreamStatus(
        self,
        timeoutAction: CheerAction,
        twitchChannelId: str,
        user: UserInterface
    ) -> bool:
        if not isinstance(timeoutAction, CheerAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        requirement = timeoutAction.getStreamStatusRequirement()

        if requirement is CheerActionStreamStatusRequirement.ANY:
            return True

        isLiveDictionary = await self.__isLiveOnTwitchRepository.isLive([ user.getHandle() ])
        isLive = isLiveDictionary.get(user.getHandle(), False) is True

        return isLive and requirement is CheerActionStreamStatusRequirement.ONLINE or \
            not isLive and requirement is CheerActionStreamStatusRequirement.OFFLINE

    async def __isWithinMinimumFollowDuration(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str
    ) -> bool:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')

        followInfo: TwitchFollower | None = None

        try:
            followInfo = await self.__twitchFollowerRepository.fetchFollowingInfo(
                twitchAccessToken = twitchAccessToken,
                twitchChannelId = twitchChannelId,
                userId = userIdToTimeout
            )
        except Exception as e:
            self.__timber.log('TwitchTimeoutHelper', f'Failed to fetch Twitch follow info for the given user ID ({twitchChannelId=}) ({userIdToTimeout=}): {e}', e, traceback.format_exc())
            return True

        if followInfo is None:
            self.__timber.log('TwitchTimeoutHelper', f'The given user ID will not be timed out as this user is not following the channel ({twitchChannelId=}) ({userIdToTimeout=}) ({followInfo=})')
            return True

        now = SimpleDateTime()

        if followInfo.getFollowedAt() + self.__minimumFollowDuration <= now:
            self.__timber.log('TwitchTimeoutHelper', f'The given user ID will not be timed out as this user started following the channel within the minimum follow duration window: ({self.__minimumFollowDuration=}) ({twitchChannelId=}) ({userIdToTimeout=}) ({followInfo=})')
            return True
        else:
            return False

    async def timeout(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str,
        user: UserInterface
    ) -> bool:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        # TODO

        if await self.__isMod(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout
        ):
            # TODO
            pass

        # TODO
        return False
