import traceback
from datetime import datetime, timedelta

from .timeoutImmuneUserIdsRepositoryInterface import \
    TimeoutImmuneUserIdsRepositoryInterface
from .twitchTimeoutHelperInterface import \
    TwitchTimeoutHelperInterface
from .twitchTimeoutRemodData import TwitchTimeoutRemodData
from .twitchTimeoutRemodHelperInterface import \
    TwitchTimeoutRemodHelperInterface
from .twitchTimeoutResult import TwitchTimeoutResult
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..api.twitchBanRequest import TwitchBanRequest
from ..api.twitchBannedUserRequest import TwitchBannedUserRequest
from ..api.twitchBannedUsersResponse import TwitchBannedUsersResponse
from ..api.twitchModUser import TwitchModUser
from ..twitchConstantsInterface import TwitchConstantsInterface
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TwitchTimeoutHelper(TwitchTimeoutHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchConstants: TwitchConstantsInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTimeoutRemodHelper: TwitchTimeoutRemodHelperInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchConstants, TwitchConstantsInterface):
            raise TypeError(f'twitchConstants argument is malformed: \"{twitchConstants}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTimeoutRemodHelper, TwitchTimeoutRemodHelperInterface):
            raise TypeError(f'twitchTimeoutRemodHelper argument is malformed: \"{twitchTimeoutRemodHelper}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__timber: TimberInterface = timber
        self.__timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface = timeoutImmuneUserIdsRepository
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchConstants: TwitchConstantsInterface = twitchConstants
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTimeoutRemodHelper: TwitchTimeoutRemodHelperInterface = twitchTimeoutRemodHelper
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    async def __isAlreadyCurrentlyBannedOrTimedOut(
        self,
        twitchChannelAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str
    ) -> bool:
        if not utils.isValidStr(twitchChannelAccessToken):
            raise TypeError(f'twitchChannelAccessToken argument is malformed: \"{twitchChannelAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')

        bannedUsersResponse: TwitchBannedUsersResponse | None = None

        try:
            bannedUsersResponse = await self.__twitchApiService.fetchBannedUsers(
                twitchAccessToken = twitchChannelAccessToken,
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

        bannedUsers = bannedUsersResponse.users

        if bannedUsers is None or len(bannedUsers) == 0:
            return False

        for bannedUser in bannedUsers:
            if bannedUser.userId == userIdToTimeout:
                if bannedUser.expiresAt is None:
                    self.__timber.log('TwitchTimeoutHelper', f'The given user ID will not be timed out as this user is banned: ({bannedUser=}) ({twitchChannelId=}) ({userIdToTimeout=})')
                else:
                    self.__timber.log('TwitchTimeoutHelper', f'The given user ID will not be timed out as this user is already timed out: ({bannedUser=}) ({twitchChannelId=}) ({userIdToTimeout=})')

                return True

        return False

    async def __isMod(
        self,
        twitchChannelAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str
    ) -> bool:
        if not utils.isValidStr(twitchChannelAccessToken):
            raise TypeError(f'twitchChannelAccessToken argument is malformed: \"{twitchChannelAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')

        moderatorInfo: TwitchModUser | None = None

        try:
            moderatorInfo = await self.__twitchApiService.fetchModerator(
                broadcasterId = twitchChannelId,
                twitchAccessToken = twitchChannelAccessToken,
                userId = userIdToTimeout
            )
        except Exception as e:
            self.__timber.log('TwitchTimeoutHelper', f'Failed to fetch Twitch moderator info for the given user ID ({twitchChannelId=}) ({userIdToTimeout=}): {e}', e, traceback.format_exc())
            return False

        return moderatorInfo is not None

    async def timeout(
        self,
        durationSeconds: int,
        reason: str | None,
        twitchAccessToken: str,
        twitchChannelAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str,
        user: UserInterface
    ) -> TwitchTimeoutResult:
        if not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > self.__twitchConstants.getMaxTimeoutSeconds():
            raise ValueError(f'durationSeconds argument is out of bounds: \"{durationSeconds}\"')
        elif reason is not None and not isinstance(reason, str):
            raise TypeError(f'reason argument is malformed: \"{reason}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelAccessToken):
            raise TypeError(f'twitchChannelAccessToken argument is malformed: \"{twitchChannelAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        userNameToTimeout = await self.__userIdsRepository.fetchUserName(
            userId = userIdToTimeout,
            twitchAccessToken = twitchAccessToken
        )

        if not utils.isValidStr(userNameToTimeout):
            self.__timber.log('TwitchTimeoutHelper', f'Abandoning timeout attempt, as we were unable to find a username for the given user ID ({twitchChannelId=}) ({userIdToTimeout=}) ({user=})')
            return TwitchTimeoutResult.INVALID_USER_NAME
        elif userIdToTimeout == twitchChannelId:
            self.__timber.log('TwitchTimeoutHelper', f'Abandoning timeout attempt, as we were going to timeout the streamer themselves ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({user=})')
            return TwitchTimeoutResult.IS_STREAMER
        elif await self.__timeoutImmuneUserIdsRepository.isImmune(userIdToTimeout):
            self.__timber.log('TwitchTimeoutHelper', f'Abandoning timeout attempt, as we were going to timeout an immune user ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({user=})')
            return TwitchTimeoutResult.IMMUNE_USER
        elif await self.__isAlreadyCurrentlyBannedOrTimedOut(
            twitchChannelAccessToken = twitchChannelAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout
        ):
            self.__timber.log('TwitchTimeoutHelper', f'Abandoning timeout attempt, as this user is already either banned or timed out ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({user=})')
            return TwitchTimeoutResult.ALREADY_BANNED_OR_TIMED_OUT

        cynanBotUserId = await self.__userIdsRepository.requireUserId(
            userName = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchAccessToken = twitchAccessToken
        )

        mustRemod = await self.__isMod(
            twitchChannelAccessToken = twitchChannelAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout
        )

        if not await self.__timeout(
            durationSeconds = durationSeconds,
            cynanBotUserId = cynanBotUserId,
            reason = reason,
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout,
            userNameToTimeout = userNameToTimeout,
            user = user
        ):
            self.__timber.log('TwitchTimeoutHelper', f'Abandoning timeout attempt, as the Twitch API call failed ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({user=})')
            return TwitchTimeoutResult.API_CALL_FAILED

        if mustRemod:
            remodDateTime = datetime.now(self.__timeZoneRepository.getDefault()) + timedelta(seconds = durationSeconds)

            await self.__twitchTimeoutRemodHelper.submitRemodData(TwitchTimeoutRemodData(
                remodDateTime = remodDateTime,
                broadcasterUserId = twitchChannelId,
                broadcasterUserName = user.getHandle(),
                userId = userIdToTimeout
            ))

        self.__timber.log('TwitchTimeoutHelper', f'Successfully timed out user ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({user=})')
        return TwitchTimeoutResult.SUCCESS

    async def __timeout(
        self,
        durationSeconds: int,
        cynanBotUserId: str,
        reason: str | None,
        twitchAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str,
        userNameToTimeout: str,
        user: UserInterface
    ) -> bool:
        if not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > self.__twitchConstants.getMaxTimeoutSeconds():
            raise ValueError(f'durationSeconds argument is out of bounds: \"{durationSeconds}\"')
        elif not utils.isValidStr(cynanBotUserId):
            raise TypeError(f'cynanBotUserId argument is malformed: \"{cynanBotUserId}\"')
        elif reason is not None and not isinstance(reason, str):
            raise TypeError(f'reason argument is malformed: \"{reason}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')
        elif not utils.isValidStr(userNameToTimeout):
            raise TypeError(f'userNameToTimeout argument is malformed: \"{userNameToTimeout}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        try:
            await self.__twitchApiService.banUser(
                twitchAccessToken = twitchAccessToken,
                banRequest = TwitchBanRequest(
                    duration = durationSeconds,
                    broadcasterUserId = twitchChannelId,
                    moderatorUserId = cynanBotUserId,
                    reason = reason,
                    userIdToBan = userIdToTimeout
                )
            )
        except Exception as e:
            self.__timber.log('TwitchTimeoutHelper', f'Failed to timeout user ({reason=}) ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({user=}): {e}', e, traceback.format_exc())
            return False

        return True
