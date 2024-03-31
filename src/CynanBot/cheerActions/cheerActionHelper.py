import re
import traceback
from datetime import datetime, timedelta, timezone, tzinfo
from typing import Pattern

import CynanBot.misc.utils as utils
from CynanBot.aniv.anivUserIdProviderInterface import \
    AnivUserIdProviderInterface
from CynanBot.cheerActions.cheerAction import CheerAction
from CynanBot.cheerActions.cheerActionBitRequirement import \
    CheerActionBitRequirement
from CynanBot.cheerActions.cheerActionHelperInterface import \
    CheerActionHelperInterface
from CynanBot.cheerActions.cheerActionRemodData import CheerActionRemodData
from CynanBot.cheerActions.cheerActionRemodHelperInterface import \
    CheerActionRemodHelperInterface
from CynanBot.cheerActions.cheerActionsRepositoryInterface import \
    CheerActionsRepositoryInterface
from CynanBot.cheerActions.cheerActionStreamStatusRequirement import \
    CheerActionStreamStatusRequirement
from CynanBot.cheerActions.cheerActionType import CheerActionType
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.api.twitchBannedUserRequest import TwitchBannedUserRequest
from CynanBot.twitch.api.twitchBanRequest import TwitchBanRequest
from CynanBot.twitch.api.twitchModUser import TwitchModUser
from CynanBot.twitch.configuration.twitchChannelProvider import \
    TwitchChannelProvider
from CynanBot.twitch.isLiveOnTwitchRepositoryInterface import \
    IsLiveOnTwitchRepositoryInterface
from CynanBot.twitch.twitchFollowerRepositoryInterface import \
    TwitchFollowerRepositoryInterface
from CynanBot.twitch.twitchHandleProviderInterface import \
    TwitchHandleProviderInterface
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface


class CheerActionHelper(CheerActionHelperInterface):

    def __init__(
        self,
        anivUserIdProvider: AnivUserIdProviderInterface,
        cheerActionRemodHelper: CheerActionRemodHelperInterface,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface,
        streamAlertsManager: StreamAlertsManagerInterface | None,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchFollowerRepository: TwitchFollowerRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        minimumFollowDuration: timedelta = timedelta(weeks = 1),
        timeZone: tzinfo = timezone.utc
    ):
        if not isinstance(anivUserIdProvider, AnivUserIdProviderInterface):
            raise TypeError(f'anivUserIdProvider argument is malformed: \"{anivUserIdProvider}\"')
        if not isinstance(cheerActionRemodHelper, CheerActionRemodHelperInterface):
            raise TypeError(f'cheerActionRemodHelper argument is malformed: \"{cheerActionRemodHelper}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif streamAlertsManager is not None and not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchFollowerRepository, TwitchFollowerRepositoryInterface):
            raise TypeError(f'twitchFollowerRepository argument is malformed: \"{twitchFollowerRepository}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(minimumFollowDuration, timedelta):
            raise TypeError(f'minimumFollowDuration argument is malformed: \"{minimumFollowDuration}\"')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__anivUserIdProvider: AnivUserIdProviderInterface = anivUserIdProvider
        self.__cheerActionRemodHelper: CheerActionRemodHelperInterface = cheerActionRemodHelper
        self.__cheerActionsRepository: CheerActionsRepositoryInterface = cheerActionsRepository
        self.__isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface = isLiveOnTwitchRepository
        self.__streamAlertsManager: StreamAlertsManagerInterface | None = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchFollowerRepository: TwitchFollowerRepositoryInterface = twitchFollowerRepository
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__minimumFollowDuration: timedelta = minimumFollowDuration
        self.__timeZone: tzinfo = timeZone

        self.__userNameRegEx: Pattern = re.compile(r'^\s*(\w+\d+)\s+@?(\w+)\s*$', re.IGNORECASE)
        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __getTwitchAccessToken(self, twitchChannel: str) -> str:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        await self.__twitchTokensRepository.validateAndRefreshAccessToken(twitchChannel)
        return await self.__twitchTokensRepository.requireAccessToken(twitchChannel)

    async def handleCheerAction(
        self,
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        user: UserInterface
    ) -> bool:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 0 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        moderatorTwitchAccessToken = await self.__getTwitchAccessToken(
            twitchChannel = await self.__twitchHandleProvider.getTwitchHandle()
        )

        userTwitchAccessToken = await self.__getTwitchAccessToken(
            twitchChannel = user.getHandle()
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
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')

        moderatorInfo: TwitchModUser | None = None

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
        actions: list[CheerAction],
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
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 0 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not isinstance(actions, list):
            raise TypeError(f'actions argument is malformed: \"{actions}\"')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(moderatorTwitchAccessToken):
            raise TypeError(f'moderatorTwitchAccessToken argument is malformed: \"{moderatorTwitchAccessToken}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        timeoutActions: list[CheerAction] = list()

        for action in actions:
            if action.getActionType() is CheerActionType.TIMEOUT:
                timeoutActions.append(action)

        if len(timeoutActions) == 0:
            return False

        timeoutActions.sort(key = lambda action: action.getAmount(), reverse = True)
        timeoutAction: CheerAction | None = None

        for action in timeoutActions:
            if action.getBitRequirement() is CheerActionBitRequirement.EXACT and bits == action.getAmount():
                timeoutAction = action
                break

        if timeoutAction is None:
            for action in timeoutActions:
                if action.getBitRequirement() is CheerActionBitRequirement.GREATER_THAN_OR_EQUAL_TO and bits >= action.getAmount():
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

        if not await self.__verifyStreamStatus(
            timeoutAction = timeoutAction,
            user = user
        ):
            self.__timber.log('CheerActionHelper', f'Attempted to timeout {cheerUserName}:{cheerUserId} in {user.getHandle()}, but failed to verify the current stream status: ({timeoutAction=})')
            return False

        return await self.__timeoutUser(
            action = timeoutAction,
            bits = bits,
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            userIdToTimeout = userIdToTimeout,
            userTwitchAccessToken = userTwitchAccessToken,
            user = user
        )

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    async def __timeoutUser(
        self,
        action: CheerAction,
        bits: int,
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
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(moderatorTwitchAccessToken):
            raise TypeError(f'moderatorTwitchAccessToken argument is malformed: \"{moderatorTwitchAccessToken}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

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
                    reason = f'cheer timeout from {cheerUserName} ({bits} bit(s), {action.getDurationSeconds()} second(s))',
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

        streamAlertsManager = self.__streamAlertsManager
        twitchChannelProvider = self.__twitchChannelProvider

        if user.isTtsEnabled() and streamAlertsManager is not None:
            message = f'{cheerUserName} timed out {userNameToTimeout} for {action.getDurationSeconds()} seconds! rip bozo!'

            if twitchChannelProvider is not None:
                twitchChannel = await twitchChannelProvider.getTwitchChannel(user.getHandle())
                await self.__twitchUtils.safeSend(twitchChannel, 'RIPBOZO')

            streamAlertsManager.submitAlert(StreamAlert(
                soundAlert = None,
                twitchChannel = user.getHandle(),
                twitchChannelId = broadcasterUserId,
                ttsEvent = TtsEvent(
                    message = message,
                    twitchChannel = user.getHandle(),
                    userId = cheerUserId,
                    userName = cheerUserName,
                    donation = None,
                    provider = TtsProvider.GOOGLE,
                    raidInfo = None
                )
            ))

            return True
        else:
            return False

    async def __verifyStreamStatus(
        self,
        timeoutAction: CheerAction,
        user: UserInterface
    ) -> bool:
        if not isinstance(timeoutAction, CheerAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        requirement = timeoutAction.getStreamStatusRequirement()

        if requirement is CheerActionStreamStatusRequirement.ANY:
            return True

        isLiveDictionary = await self.__isLiveOnTwitchRepository.isLive(list(user.getHandle()))
        isLive = isLiveDictionary.get(user.getHandle()) is True

        return isLive and requirement is CheerActionStreamStatusRequirement.ONLINE or \
            not isLive and requirement is CheerActionStreamStatusRequirement.OFFLINE

    async def __verifyUserCanBeTimedOut(
        self,
        broadcasterUserId: str,
        twitchAccessToken: str,
        userIdToTimeout: str
    ) -> bool:
        if not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')

        try:
            bannedUsersResponse = await self.__twitchApiService.fetchBannedUsers(
                twitchAccessToken = twitchAccessToken,
                bannedUserRequest = TwitchBannedUserRequest(
                    broadcasterId = broadcasterUserId,
                    requestedUserId = userIdToTimeout
                )
            )
        except Exception as e:
            self.__timber.log('CheerActionHelper', f'Failed to verify if the given user ID can be timed out ({broadcasterUserId=}) ({twitchAccessToken=}) ({userIdToTimeout=}): {e}', e, traceback.format_exc())
            return False

        bannedUsers = bannedUsersResponse.getUsers()

        if not utils.hasItems(bannedUsers):
            return True

        for bannedUser in bannedUsers:
            if bannedUser.getUserId() == userIdToTimeout:
                if bannedUser.getExpiresAt() is None:
                    self.__timber.log('CheerActionHelper', f'The given user ID will not be timed out as this user is banned: {bannedUser=} ({broadcasterUserId=}) ({twitchAccessToken=}) ({userIdToTimeout=})')
                else:
                    self.__timber.log('CheerActionHelper', f'The given user ID will not be timed out as this user is already timed out: {bannedUser=} ({broadcasterUserId=}) ({twitchAccessToken=}) ({userIdToTimeout=})')

                return False

        twitchFollower = await self.__twitchFollowerRepository.fetchFollowingInfo(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = broadcasterUserId,
            userId = userIdToTimeout
        )

        if twitchFollower is None:
            self.__timber.log('CheerActionHelper', f'The given user ID will not be timed out as this user is not following the channel ({broadcasterUserId=}) ({twitchAccessToken=}) ({userIdToTimeout=})')
            return False

        now = SimpleDateTime()

        if twitchFollower.getFollowedAt() + self.__minimumFollowDuration <= now:
            self.__timber.log('CheerActionHelper', f'The given user ID will not be timed out as this user started following the channel within the minimum follow duration window: {twitchFollower} ({self.__minimumFollowDuration=}) ({broadcasterUserId=}) ({twitchAccessToken=}) ({userIdToTimeout=})')
            return False

        return True
