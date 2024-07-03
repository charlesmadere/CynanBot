import re
from datetime import datetime, timedelta
from typing import Pattern

from .timeoutCheerActionHelperInterface import TimeoutCheerActionHelperInterface
from .timeoutCheerActionHistoryRepositoryInterface import TimeoutCheerActionHistoryRepositoryInterface
from ..cheerAction import CheerAction
from ..cheerActionBitRequirement import CheerActionBitRequirement
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActionType import CheerActionType
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...tts.ttsEvent import TtsEvent
from ...tts.ttsProvider import TtsProvider
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.configuration.twitchMessageable import TwitchMessageable
from ...twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ...twitch.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from ...twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from ...twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TimeoutCheerActionHelper(TimeoutCheerActionHelperInterface):

    def __init__(
        self,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        timeoutCheerActionHistoryRepository: TimeoutCheerActionHistoryRepositoryInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutCheerActionHistoryRepository, TimeoutCheerActionHistoryRepositoryInterface):
            raise TypeError(f'timeoutCheerActionHistoryRepository argument is malformed: \"{timeoutCheerActionHistoryRepository}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface = isLiveOnTwitchRepository
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__timeoutCheerActionHistoryRepository: TimeoutCheerActionHistoryRepositoryInterface = timeoutCheerActionHistoryRepository
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface = twitchFollowingStatusRepository
        self.__twitchTimeoutHelper: TwitchTimeoutHelperInterface = twitchTimeoutHelper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__userNameRegEx: Pattern = re.compile(r'^\s*(\w+\d+)\s+@?(\w+)\s*$', re.IGNORECASE)
        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def handleTimeoutCheerAction(
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

        if not user.areCheerActionsEnabled():
            return False

        timeoutActions: list[CheerAction] = list()
        for action in actions:
            if action.actionType is CheerActionType.TIMEOUT:
                timeoutActions.append(action)

        if len(timeoutActions) == 0:
            return False

        timeoutActions.sort(key = lambda action: action.amount, reverse = True)
        timeoutAction: CheerAction | None = None

        for action in timeoutActions:
            if action.bitRequirement is CheerActionBitRequirement.EXACT and bits == action.amount:
                timeoutAction = action
                break

        if timeoutAction is None:
            for action in timeoutActions:
                if action.bitRequirement is CheerActionBitRequirement.GREATER_THAN_OR_EQUAL_TO and bits >= action.amount:
                    timeoutAction = action
                    break

        if timeoutAction is None:
            return False
        elif not utils.isValidInt(action.durationSeconds):
            self.__timber.log('TimeoutCheerActionHelper', f'Encountered a valid timeout CheerAction instance but it has no durationSeconds value, this should be impossible: {timeoutAction}')
            return False

        userNameToTimeoutMatch = self.__userNameRegEx.fullmatch(message)
        if userNameToTimeoutMatch is None or not utils.isValidStr(userNameToTimeoutMatch.group(2)):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout from {cheerUserName}:{cheerUserId} in {user.getHandle()}, but was unable to find a user name: ({message=}) ({timeoutAction=})')
            return False

        userNameToTimeout = userNameToTimeoutMatch.group(2)

        userIdToTimeout = await self.__userIdsRepository.fetchUserId(
            userName = userNameToTimeout,
            twitchAccessToken = userTwitchAccessToken
        )

        if not utils.isValidStr(userIdToTimeout):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout \"{userNameToTimeout}\" from {cheerUserName}:{cheerUserId} in {user.getHandle()}, but was unable to find a user ID: ({message=}) ({timeoutAction=})')
            return False
        elif userIdToTimeout == broadcasterUserId:
            userIdToTimeout = cheerUserId
            self.__timber.log('TimeoutCheerActionHelper', f'Attempt to timeout the broadcaster themself from {cheerUserName}:{cheerUserId} in {user.getHandle()}, so will instead time out the user: ({message=}) ({timeoutAction=})')

        return await self.__timeoutUser(
            action = timeoutAction,
            bits = bits,
            twitchChannelId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            userIdToTimeout = userIdToTimeout,
            userTwitchAccessToken = userTwitchAccessToken,
            user = user
        )

    async def __isNewFollower(
        self,
        followShieldDays: int | None,
        twitchAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str
    ) -> bool:
        if followShieldDays is not None and not utils.isValidInt(followShieldDays):
            raise TypeError(f'followShieldDays argument is malformed: \"{followShieldDays}\"')
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')

        if followShieldDays is None:
            # this user doesn't use a follow shield
            return False

        followingStatus = await self.__twitchFollowingStatusRepository.fetchFollowingStatus(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userId = userIdToTimeout
        )

        minimumFollowDuration = timedelta(days = followShieldDays)

        if followingStatus is None:
            self.__timber.log('TimeoutCheerActionHelper', f'The given user ID will not be timed out as this user is not following the channel ({followingStatus=}) ({minimumFollowDuration=}) ({twitchChannelId=}) ({userIdToTimeout=})')
            return True

        now = datetime.now(self.__timeZoneRepository.getDefault())

        if followingStatus.followedAt + minimumFollowDuration >= now:
            self.__timber.log('TimeoutCheerActionHelper', f'The given user ID will not be timed out as this user started following the channel within the minimum follow duration window: ({followingStatus=}) ({minimumFollowDuration=}) ({twitchChannelId=}) ({userIdToTimeout=})')
            return True

        return False

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    async def __timeoutUser(
        self,
        action: CheerAction,
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        twitchChannelId: str,
        userIdToTimeout: str,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        if not isinstance(action, CheerAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(moderatorTwitchAccessToken):
            raise TypeError(f'moderatorTwitchAccessToken argument is malformed: \"{moderatorTwitchAccessToken}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        twitchChannelProvider = self.__twitchChannelProvider
        twitchChannel: TwitchMessageable | None = None

        if twitchChannelProvider is not None:
            twitchChannel = await twitchChannelProvider.getTwitchChannel(user.getHandle())

        userNameToTimeout = await self.__userIdsRepository.requireUserName(
            userId = userIdToTimeout,
            twitchAccessToken = userTwitchAccessToken
        )

        if not await self.__verifyStreamStatus(
            timeoutAction = action,
            twitchChannelId = twitchChannelId,
            user = user
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} in {user.getHandle()}, but the current stream status is invalid ({action=})')
            return False
        elif await self.__isNewFollower(
            followShieldDays = user.timeoutCheerActionFollowShieldDays,
            twitchAccessToken = userTwitchAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} in {user.getHandle()}, but this user is a new follower ({action=})')
            return False

        durationSeconds = action.requireDurationSeconds()

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = durationSeconds,
            reason = f'Cheer timeout from {cheerUserName} — {bits} bit(s), {durationSeconds} second(s), action ID \"{action.actionId}\"',
            twitchAccessToken = moderatorTwitchAccessToken,
            twitchChannelAccessToken = userTwitchAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout,
            user = user
        )

        if timeoutResult is TwitchTimeoutResult.FOLLOW_SHIELD:
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} in {user.getHandle()}, but they have the follow shield ({timeoutResult=}) ({action=})')

            if twitchChannel is not None:
                await self.__twitchUtils.safeSend(twitchChannel, f'ⓘ Sorry @{cheerUserName}, but @{userNameToTimeout} has the follow shield')

            return False
        elif timeoutResult is TwitchTimeoutResult.IMMUNE_USER:
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} in {user.getHandle()}, but they are immune ({timeoutResult=}) ({action=})')

            if twitchChannel is not None:
                await self.__twitchUtils.safeSend(twitchChannel, f'⚠️ Sorry @{cheerUserName}, but @{userNameToTimeout} is immune')

            return False
        elif timeoutResult is not TwitchTimeoutResult.SUCCESS:
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} in {user.getHandle()}, but an error occurred ({timeoutResult=}) ({action=})')
            return False

        self.__timber.log('TimeoutCheerActionHelper', f'Timed out {userNameToTimeout}:{userIdToTimeout} in \"{user.getHandle()}\" for {durationSeconds} second(s)')

        await self.__timeoutCheerActionHistoryRepository.add(
            bitAmount = bits,
            durationSeconds = durationSeconds,
            chatterUserId = userIdToTimeout,
            timedOutByUserId = cheerUserId,
            twitchAccessToken = userTwitchAccessToken,
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId
        )

        if user.isTtsEnabled():
            message = f'{cheerUserName} timed out {userNameToTimeout} for {durationSeconds} seconds! rip bozo!'

            self.__streamAlertsManager.submitAlert(StreamAlert(
                soundAlert = None,
                twitchChannel = user.getHandle(),
                twitchChannelId = twitchChannelId,
                ttsEvent = TtsEvent(
                    message = message,
                    twitchChannel = user.getHandle(),
                    twitchChannelId = twitchChannelId,
                    userId = cheerUserId,
                    userName = cheerUserName,
                    donation = None,
                    provider = TtsProvider.GOOGLE,
                    raidInfo = None
                )
            ))

        if twitchChannel is not None:
            await self.__twitchUtils.safeSend(twitchChannel, 'RIPBOZO')

        return True

    async def __verifyStreamStatus(
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

        requirement = timeoutAction.streamStatusRequirement
        if requirement is CheerActionStreamStatusRequirement.ANY:
            return True

        isLive = await self.__isLiveOnTwitchRepository.isLive(twitchChannelId)
        return isLive and requirement is CheerActionStreamStatusRequirement.ONLINE or \
            not isLive and requirement is CheerActionStreamStatusRequirement.OFFLINE
