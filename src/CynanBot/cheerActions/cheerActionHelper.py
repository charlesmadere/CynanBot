import re
import traceback
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Pattern

import CynanBot.misc.utils as utils
from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.cheerActions.cheerAction import CheerAction
from CynanBot.cheerActions.cheerActionHelperInterface import \
    CheerActionHelperInterface
from CynanBot.cheerActions.cheerActionRemodData import CheerActionRemodData
from CynanBot.cheerActions.cheerActionRemodHelperInterface import \
    CheerActionRemodHelperInterface
from CynanBot.cheerActions.cheerActionRequirement import CheerActionRequirement
from CynanBot.cheerActions.cheerActionsRepositoryInterface import \
    CheerActionsRepositoryInterface
from CynanBot.cheerActions.cheerActionType import CheerActionType
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.api.twitchBannedUserRequest import TwitchBannedUserRequest
from CynanBot.twitch.api.twitchBanRequest import TwitchBanRequest
from CynanBot.twitch.api.twitchModUser import TwitchModUser
from CynanBot.twitch.twitchHandleProviderInterface import \
    TwitchHandleProviderInterface
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface


class CheerActionHelper(CheerActionHelperInterface):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        cheerActionRemodHelper: CheerActionRemodHelperInterface,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        timber: TimberInterface,
        ttsManager: Optional[TtsManagerInterface],
        twitchApiService: TwitchApiServiceInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        timeZone: timezone = timezone.utc
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(cheerActionRemodHelper, CheerActionRemodHelperInterface):
            raise ValueError(f'cheerActionRemodHelper argument is malformed: \"{cheerActionRemodHelper}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise ValueError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif ttsManager is not None and not isinstance(ttsManager, TtsManagerInterface):
            raise ValueError(f'ttsManager argument is malformed: \"{ttsManager}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise ValueError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise ValueError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(timeZone, timezone):
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__cheerActionRemodHelper: CheerActionRemodHelperInterface = cheerActionRemodHelper
        self.__cheerActionsRepository: CheerActionsRepositoryInterface = cheerActionsRepository
        self.__timber: TimberInterface = timber
        self.__ttsManager: Optional[TtsManagerInterface] = ttsManager
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__timeZone: timezone = timeZone

        self.__userNameRegEx: Pattern = re.compile(r'^\s*(\w+\d+)\s+@?(\w+)\s*$', re.IGNORECASE)

    async def __getTwitchAccessToken(self, userName: str) -> str:
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        await self.__twitchTokensRepository.validateAndRefreshAccessToken(userName)
        return await self.__twitchTokensRepository.requireAccessToken(userName)

    async def handleCheerAction(
        self,
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        user: UserInterface
    ) -> bool:
        if not utils.isValidInt(bits):
            raise ValueError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 0 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(cheerUserId):
            raise ValueError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise ValueError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        moderatorTwitchAccessToken = await self.__getTwitchAccessToken(
            userName = await self.__twitchHandleProvider.getTwitchHandle()
        )

        userTwitchAccessToken = await self.__getTwitchAccessToken(user.getHandle())

        broadcasterUserId = await self.__userIdsRepository.requireUserId(
            userName = user.getHandle(),
            twitchAccessToken = userTwitchAccessToken
        )

        moderatorUserId = await self.__userIdsRepository.requireUserId(
            userName = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchAccessToken = userTwitchAccessToken
        )

        actions = await self.__cheerActionsRepository.getActions(broadcasterUserId)

        if not utils.hasItems(actions):
            return False

        return await self.__processTimeoutActions(
            bits = bits,
            actions = actions,
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            message = message,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            userTwitchAccessToken = userTwitchAccessToken,
            user = user
        )

    async def __isMod(
        self,
        broadcasterUserId: str,
        twitchAccessToken: str,
        userIdToTimeout: str
    ) -> bool:
        if not utils.isValidStr(broadcasterUserId):
            raise ValueError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise ValueError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')

        moderatorInfo: Optional[TwitchModUser] = None

        try:
            moderatorInfo = await self.__twitchApiService.fetchModerator(
                broadcasterId = broadcasterUserId,
                twitchAccessToken = twitchAccessToken,
                userId = userIdToTimeout
            )
        except Exception as e:
            self.__timber.log('CheerActionHelper', f'Failed to fetch Twitch moderator info ({broadcasterUserId=}) ({userIdToTimeout=})', e, traceback.format_exc())

        return moderatorInfo is not None

    async def __processTimeoutActions(
        self,
        bits: int,
        actions: List[CheerAction],
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        if not utils.isValidInt(bits):
            raise ValueError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 0 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not isinstance(actions, List):
            raise ValueError(f'actions argument is malformed: \"{actions}\"')
        elif not utils.isValidStr(broadcasterUserId):
            raise ValueError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(cheerUserId):
            raise ValueError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise ValueError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(moderatorTwitchAccessToken):
            raise ValueError(f'moderatorTwitchAccessToken argument is malformed: \"{moderatorTwitchAccessToken}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise ValueError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise ValueError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        timeoutActions: List[CheerAction] = list()

        for action in actions:
            if action.getActionType() is CheerActionType.TIMEOUT:
                timeoutActions.append(action)

        if len(timeoutActions) == 0:
            return False

        timeoutActions.sort(key = lambda action: action.getAmount(), reverse = True)
        timeoutAction: Optional[CheerAction] = None

        for action in timeoutActions:
            if action.getActionRequirement() is CheerActionRequirement.EXACT and bits == action.getAmount():
                timeoutAction = action
                break

        if timeoutAction is None:
            for action in timeoutActions:
                if action.getActionRequirement() is CheerActionRequirement.GREATER_THAN_OR_EQUAL_TO and bits >= action.getAmount():
                    timeoutAction = action
                    break

        if timeoutAction is None:
            return False

        userNameToTimeoutMatch = self.__userNameRegEx.fullmatch(message)
        if userNameToTimeoutMatch is None or not utils.isValidStr(userNameToTimeoutMatch.group(2)):
            self.__timber.log('CheerActionHelper', f'Attempted to timeout from {cheerUserName}:{cheerUserId} in {user.getHandle()}, but was unable to find a user name: ({message=}) ({timeoutAction=})')
            return False

        userNameToTimeout = userNameToTimeoutMatch.group(2)

        userIdToTimeout = await self.__userIdsRepository.fetchUserId(
            userName = userNameToTimeout,
            twitchAccessToken = userTwitchAccessToken
        )

        if not utils.isValidStr(userIdToTimeout):
            self.__timber.log('CheerActionHelper', f'Attempted to timeout \"{userNameToTimeout}\" from {cheerUserName}:{cheerUserId} in {user.getHandle()}, but was unable to find a user ID: ({message=}) ({timeoutAction=})')
            return False
        elif userIdToTimeout.lower() == broadcasterUserId.lower():
            userIdToTimeout = cheerUserId
            self.__timber.log('CheerActionHelper', f'Attempt to timeout the broadcaster themself from {cheerUserName}:{cheerUserId} in {user.getHandle()}, so will instead time out the user: ({message=}) ({timeoutAction=})')

        return await self.__timeoutUser(
            action = timeoutAction,
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            userIdToTimeout = userIdToTimeout,
            userTwitchAccessToken = userTwitchAccessToken,
            user = user
        )

    async def __timeoutUser(
        self,
        action: CheerAction,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        userIdToTimeout: str,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        if not isinstance(action, CheerAction):
            raise ValueError(f'action argument is malformed: \"{action}\"')
        elif not utils.isValidStr(broadcasterUserId):
            raise ValueError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(cheerUserId):
            raise ValueError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise ValueError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(moderatorTwitchAccessToken):
            raise ValueError(f'moderatorTwitchAccessToken argument is malformed: \"{moderatorTwitchAccessToken}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise ValueError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise ValueError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise ValueError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        if not await self.__verifyUserCanBeTimedOut(
            broadcasterUserId = broadcasterUserId,
            twitchAccessToken = userTwitchAccessToken,
            userIdToTimeout = userIdToTimeout
        ):
            return False

        isMod = await self.__isMod(
            broadcasterUserId = broadcasterUserId,
            twitchAccessToken = userTwitchAccessToken,
            userIdToTimeout = userIdToTimeout
        )

        try:
            await self.__twitchApiService.banUser(
                twitchAccessToken = moderatorTwitchAccessToken,
                banRequest = TwitchBanRequest(
                    duration = action.getDurationSeconds(),
                    broadcasterUserId = broadcasterUserId,
                    moderatorUserId = moderatorUserId,
                    reason = f'cheer timeout from {cheerUserName}',
                    userIdToBan = userIdToTimeout
                )
            )
        except Exception as e:
            self.__timber.log('CheerActionHelper', f'Failed to timeout {userIdToTimeout=} in \"{user.getHandle()}\": {e}', e, traceback.format_exc())
            return False

        userNameToTimeout = await self.__userIdsRepository.requireUserName(
            userId = userIdToTimeout,
            twitchAccessToken = userTwitchAccessToken
        )

        self.__timber.log('CheerActionHelper', f'Timed out {userNameToTimeout}:{userIdToTimeout} in \"{user.getHandle()}\" for {action.getDurationSeconds()} second(s)')

        if isMod:
            self.__timber.log('CheerActionHelper', f'In \"{user.getHandle()}\", {userNameToTimeout}:{userIdToTimeout} is a mod, so they will be given mod back when the timeout is over')

            remodDateTime = datetime.now(self.__timeZone) + timedelta(seconds = action.getDurationSeconds())

            await self.__cheerActionRemodHelper.submitRemodData(CheerActionRemodData(
                remodDateTime = SimpleDateTime(remodDateTime),
                broadcasterUserId = broadcasterUserId,
                broadcasterUserName = user.getHandle(),
                userId = userIdToTimeout
            ))

        if user.isTtsEnabled() and self.__ttsManager is not None:
            self.__ttsManager.submitTtsEvent(TtsEvent(
                message = f'{cheerUserName} timed out {userNameToTimeout} for {action.getDurationSeconds()} seconds!',
                twitchChannel = user.getHandle(),
                userId = cheerUserId,
                userName = cheerUserName,
                donation = None,
                raidInfo = None
            ))

            return True
        else:
            return False

    async def __verifyUserCanBeTimedOut(
        self,
        broadcasterUserId: str,
        twitchAccessToken: str,
        userIdToTimeout: str
    ) -> bool:
        if not utils.isValidStr(broadcasterUserId):
            raise ValueError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise ValueError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')

        try:
            bannedUsersResponse = await self.__twitchApiService.fetchBannedUsers(
                twitchAccessToken = twitchAccessToken,
                bannedUserRequest = TwitchBannedUserRequest(
                    broadcasterId = broadcasterUserId,
                    requestedUserId = userIdToTimeout
                )
            )
        except Exception as e:
            self.__timber.log('CheerActionHelper', f'Failed to verify if the given user ID (\"{userIdToTimeout}\") can be timed out: {e}', e, traceback.format_exc())
            return False

        bannedUsers = bannedUsersResponse.getUsers()

        if not utils.hasItems(bannedUsers):
            return True

        for bannedUser in bannedUsers:
            if bannedUser.getUserId() == userIdToTimeout:
                if bannedUser.getExpiresAt() is None:
                    self.__timber.log('CheerActionHelper', f'The given user ID (\"{userIdToTimeout}\") will not be timed out as this user is banned: {bannedUser=}')
                else:
                    self.__timber.log('CheerActionHelper', f'The given user ID (\"{userIdToTimeout}\") will not be timed out as this user is already timed out: {bannedUser=}')

                return False

        return True
