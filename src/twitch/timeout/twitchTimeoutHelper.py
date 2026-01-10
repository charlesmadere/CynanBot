import traceback
from typing import Final

from .timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from .twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from .twitchTimeoutRemodHelperInterface import TwitchTimeoutRemodHelperInterface
from .twitchTimeoutResult import TwitchTimeoutResult
from ..activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ..api.models.twitchBanRequest import TwitchBanRequest
from ..api.models.twitchBannedUser import TwitchBannedUser
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..globalTwitchConstants import GlobalTwitchConstants
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TwitchTimeoutHelper(TwitchTimeoutHelperInterface):

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        globalTwitchConstants: GlobalTwitchConstants,
        timber: TimberInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTimeoutRemodHelper: TwitchTimeoutRemodHelperInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(globalTwitchConstants, GlobalTwitchConstants):
            raise TypeError(f'globalTwitchConstants argument is malformed: \"{globalTwitchConstants}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTimeoutRemodHelper, TwitchTimeoutRemodHelperInterface):
            raise TypeError(f'twitchTimeoutRemodHelper argument is malformed: \"{twitchTimeoutRemodHelper}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__globalTwitchConstants: Final[GlobalTwitchConstants] = globalTwitchConstants
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutImmuneUserIdsRepository: Final[TimeoutImmuneUserIdsRepositoryInterface] = timeoutImmuneUserIdsRepository
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTimeoutRemodHelper: Final[TwitchTimeoutRemodHelperInterface] = twitchTimeoutRemodHelper
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

    async def __isAlreadyCurrentlyBannedOrTimedOut(
        self,
        twitchChannelAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str,
    ) -> bool:
        if not utils.isValidStr(twitchChannelAccessToken):
            raise TypeError(f'twitchChannelAccessToken argument is malformed: \"{twitchChannelAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')

        try:
            bannedUsersResponse = await self.__twitchApiService.fetchBannedUsers(
                broadcasterId = twitchChannelId,
                twitchAccessToken = twitchChannelAccessToken,
                userId = userIdToTimeout,
            )
        except Exception as e:
            self.__timber.log('TwitchTimeoutHelper', f'Failed to verify if the given user ID can be timed out ({twitchChannelId=}) ({userIdToTimeout=})', e, traceback.format_exc())
            return False

        userToTimeout: TwitchBannedUser | None = None

        for bannedUser in bannedUsersResponse.data:
            if bannedUser.userId == userIdToTimeout:
                userToTimeout = bannedUser
                break

        if userToTimeout is None:
            return False
        elif userToTimeout.expiresAt is None:
            self.__timber.log('TwitchTimeoutHelper', f'The given user ID will not be timed out as this user is permanently banned: ({bannedUsersResponse=}) ({twitchChannelId=}) ({userIdToTimeout=})')
            return True
        else:
            self.__timber.log('TwitchTimeoutHelper', f'The given user ID will not be timed out as this user is already timed out: ({bannedUsersResponse=}) ({twitchChannelId=}) ({userIdToTimeout=})')
            return True

    async def __isMod(
        self,
        twitchChannelAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str,
    ) -> bool:
        if not utils.isValidStr(twitchChannelAccessToken):
            raise TypeError(f'twitchChannelAccessToken argument is malformed: \"{twitchChannelAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')

        try:
            moderatorsResponse = await self.__twitchApiService.fetchModerator(
                broadcasterId = twitchChannelId,
                twitchAccessToken = twitchChannelAccessToken,
                userId = userIdToTimeout,
            )
        except Exception as e:
            self.__timber.log('TwitchTimeoutHelper', f'Failed to fetch Twitch moderator info for the given user ID ({twitchChannelId=}) ({userIdToTimeout=})', e, traceback.format_exc())
            return False

        for moderatorUser in moderatorsResponse.data:
            if moderatorUser.userId == userIdToTimeout:
                return True

        return False

    async def __removeMod(
        self,
        twitchChannelAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str,
    ) -> bool:
        if not utils.isValidStr(twitchChannelAccessToken):
            raise TypeError(f'twitchChannelAccessToken argument is malformed: \"{twitchChannelAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')

        try:
            return await self.__twitchApiService.removeModerator(
                broadcasterId = twitchChannelId,
                moderatorId = userIdToTimeout,
                twitchAccessToken = twitchChannelAccessToken,
            )
        except Exception as e:
            self.__timber.log('TwitchTimeoutHelper', f'Failed to remove Twitch moderator for the given user ID ({twitchChannelId=}) ({userIdToTimeout=}): {e}', e, traceback.format_exc())
            return False

    async def timeout(
        self,
        durationSeconds: int,
        reason: str | None,
        twitchAccessToken: str,
        twitchChannelAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str,
        user: UserInterface,
    ) -> TwitchTimeoutResult:
        if not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > self.__globalTwitchConstants.maxTimeoutSeconds:
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
            twitchAccessToken = twitchAccessToken,
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
            userIdToTimeout = userIdToTimeout,
        ):
            self.__timber.log('TwitchTimeoutHelper', f'Abandoning timeout attempt, as this user is already either banned or timed out ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({user=})')
            return TwitchTimeoutResult.ALREADY_BANNED_OR_TIMED_OUT

        cynanBotUserId = await self.__userIdsRepository.requireUserId(
            userName = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchAccessToken = twitchAccessToken,
        )

        isMod = await self.__isMod(
            twitchChannelAccessToken = twitchChannelAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout,
        )

        if isMod and not await self.__removeMod(
            twitchChannelAccessToken = twitchChannelAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout,
        ):
            self.__timber.log('TwitchTimeoutHelper', f'Abandoning timeout attempt, as the given user is a mod that failed to be unmodded ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({user=})')
            return TwitchTimeoutResult.CANT_UNMOD

        await self.__activeChattersRepository.remove(
            chatterUserId = userIdToTimeout,
            twitchChannelId = twitchChannelId,
        )

        if not await self.__timeout(
            durationSeconds = durationSeconds,
            cynanBotUserId = cynanBotUserId,
            reason = reason,
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout,
            userNameToTimeout = userNameToTimeout,
            user = user,
        ):
            self.__timber.log('TwitchTimeoutHelper', f'Abandoning timeout attempt, as the Twitch API call failed ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({user=})')
            return TwitchTimeoutResult.API_CALL_FAILED

        if isMod:
            await self.__twitchTimeoutRemodHelper.submitRemodData(
                timeoutDurationSeconds = durationSeconds,
                broadcasterUserId = twitchChannelId,
                broadcasterUserName = user.handle,
                userId = userIdToTimeout,
            )

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
        user: UserInterface,
    ) -> bool:
        if not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > self.__globalTwitchConstants.maxTimeoutSeconds:
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
                    userIdToBan = userIdToTimeout,
                ),
            )
        except Exception as e:
            self.__timber.log('TwitchTimeoutHelper', f'Failed to timeout user ({reason=}) ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({user=}): {e}', e, traceback.format_exc())
            return False

        return True
