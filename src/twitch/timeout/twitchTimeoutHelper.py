import asyncio
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
from ..handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..misc.globalTwitchConstants import GlobalTwitchConstants
from ..moderator.twitchModeratorHelperInterface import TwitchModeratorHelperInterface
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
        twitchModeratorHelper: TwitchModeratorHelperInterface,
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
        elif not isinstance(twitchModeratorHelper, TwitchModeratorHelperInterface):
            raise TypeError(f'twitchModeratorHelper argument is malformed: \"{twitchModeratorHelper}\"')
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
        self.__twitchModeratorHelper: Final[TwitchModeratorHelperInterface] = twitchModeratorHelper
        self.__twitchTimeoutRemodHelper: Final[TwitchTimeoutRemodHelperInterface] = twitchTimeoutRemodHelper
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

    async def __isAlreadyCurrentlyBannedOrTimedOut(
        self,
        twitchChannelAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str,
    ) -> bool:
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

    async def __removeMod(
        self,
        twitchChannelAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str,
    ) -> bool:
        try:
            return await self.__twitchApiService.removeModerator(
                broadcasterId = twitchChannelId,
                twitchAccessToken = twitchChannelAccessToken,
                userId = userIdToTimeout,
            )
        except Exception as e:
            self.__timber.log('TwitchTimeoutHelper', f'Failed to remove Twitch moderator for the given user ID ({twitchChannelId=}) ({userIdToTimeout=})', e, traceback.format_exc())
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
            self.__timber.log('TwitchTimeoutHelper', f'Abandoning timeout attempt, as we were unable to find a username for the given user ID ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({durationSeconds=}) ({reason=}) ({user=})')
            return TwitchTimeoutResult.INVALID_USER_NAME
        elif userIdToTimeout == twitchChannelId:
            self.__timber.log('TwitchTimeoutHelper', f'Abandoning timeout attempt, as we were going to timeout the streamer themselves ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({durationSeconds=}) ({reason=}) ({user=})')
            return TwitchTimeoutResult.IS_STREAMER
        elif await self.__timeoutImmuneUserIdsRepository.isImmune(
            userId = userIdToTimeout,
        ):
            self.__timber.log('TwitchTimeoutHelper', f'Abandoning timeout attempt, as we were going to timeout an immune user ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({durationSeconds=}) ({reason=}) ({user=})')
            return TwitchTimeoutResult.IMMUNE_USER
        elif await self.__isAlreadyCurrentlyBannedOrTimedOut(
            twitchChannelAccessToken = twitchChannelAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout,
        ):
            self.__timber.log('TwitchTimeoutHelper', f'Abandoning timeout attempt, as this user is already either banned or timed out ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({durationSeconds=}) ({reason=}) ({user=})')
            return TwitchTimeoutResult.ALREADY_BANNED_OR_TIMED_OUT

        cynanBotUserId = await self.__userIdsRepository.requireUserId(
            userName = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchAccessToken = twitchAccessToken,
        )

        isMod = await self.__twitchModeratorHelper.isModerator(
            request = TwitchModeratorHelperInterface.RequestWithAccessToken(
                chatterUserId = userIdToTimeout,
                twitchAccessToken = twitchChannelAccessToken,
                twitchChannelId = twitchChannelId,
            ),
        )

        if isMod and not await self.__removeMod(
            twitchChannelAccessToken = twitchChannelAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout,
        ):
            self.__timber.log('TwitchTimeoutHelper', f'Abandoning timeout attempt, as the given user is a mod that failed to be unmodded ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({durationSeconds=}) ({reason=}) ({user=})')
            return TwitchTimeoutResult.CANT_UNMOD

        self.__timber.log('TwitchTimeoutHelper', f'Timing out... ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({isMod=}) ({durationSeconds=}) ({reason=}) ({user=})')

        if not await self.__timeout(
            isMod = isMod,
            durationSeconds = durationSeconds,
            cynanBotUserId = cynanBotUserId,
            reason = reason,
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout,
            userNameToTimeout = userNameToTimeout,
            user = user,
        ):
            self.__timber.log('TwitchTimeoutHelper', f'Abandoning timeout attempt, as the Twitch API call failed ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({isMod=}) ({durationSeconds=}) ({reason=}) ({user=})')
            return TwitchTimeoutResult.API_CALL_FAILED

        await self.__activeChattersRepository.remove(
            chatterUserId = userIdToTimeout,
            twitchChannelId = twitchChannelId,
        )

        if isMod:
            await self.__twitchTimeoutRemodHelper.submitRemodData(
                timeoutDurationSeconds = durationSeconds,
                broadcasterUserId = twitchChannelId,
                userId = userIdToTimeout,
            )

        self.__timber.log('TwitchTimeoutHelper', f'Successfully timed out user ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({isMod=}) ({durationSeconds=}) ({reason=}) ({user=})')
        return TwitchTimeoutResult.SUCCESS

    async def __timeout(
        self,
        isMod: bool,
        durationSeconds: int,
        cynanBotUserId: str,
        reason: str | None,
        twitchAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str,
        userNameToTimeout: str,
        user: UserInterface,
    ) -> bool:
        banRequest = TwitchBanRequest(
            duration = durationSeconds,
            broadcasterUserId = twitchChannelId,
            moderatorUserId = cynanBotUserId,
            reason = reason,
            userIdToBan = userIdToTimeout,
        )

        if isMod:
            successfullyTimedOut = False
            attempts = 0

            for _ in range(3):
                successfullyTimedOut = await self.__timeoutAttempt(
                    twitchAccessToken = twitchAccessToken,
                    userNameToTimeout = userNameToTimeout,
                    banRequest = banRequest,
                    user = user,
                )

                if successfullyTimedOut:
                    break

                attempts += 1
                await asyncio.sleep(0.5)

            if successfullyTimedOut and attempts >= 1:
                self.__timber.log('TwitchTimeoutHelper', f'Timed out user after {attempts} attempt(s) ({twitchChannelId=}) ({userIdToTimeout=}) ({userNameToTimeout=}) ({isMod=}) ({durationSeconds=}) ({reason=}) ({user=})')

            return successfullyTimedOut
        else:
            return await self.__timeoutAttempt(
                twitchAccessToken = twitchAccessToken,
                userNameToTimeout = userNameToTimeout,
                banRequest = banRequest,
                user = user,
            )

    async def __timeoutAttempt(
        self,
        twitchAccessToken: str,
        userNameToTimeout: str,
        banRequest: TwitchBanRequest,
        user: UserInterface,
    ) -> bool:
        try:
            banResponse = await self.__twitchApiService.banUser(
                twitchAccessToken = twitchAccessToken,
                banRequest = banRequest,
            )
        except Exception as e:
            self.__timber.log('TwitchTimeoutHelper', f'Failed to timeout user ({userNameToTimeout=}) ({user=}) ({banRequest=})', e, traceback.format_exc())
            return False

        for banResponseEntry in banResponse.data:
            if banResponseEntry.userId == banRequest.userIdToBan:
                return True

        self.__timber.log('TwitchTimeoutHelper', f'Failed to timeout user ({userNameToTimeout=}) ({user=}) ({banRequest=}) ({banResponse=})')
        return False
