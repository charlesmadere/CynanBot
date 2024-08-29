import random
from datetime import datetime, timedelta

from frozenlist import FrozenList

from .timeoutCheerActionHelperInterface import TimeoutCheerActionHelperInterface
from .timeoutCheerActionHistoryRepositoryInterface import TimeoutCheerActionHistoryRepositoryInterface
from .timeoutCheerActionSettingsRepositoryInterface import TimeoutCheerActionSettingsRepositoryInterface
from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..timeoutCheerAction import TimeoutCheerAction
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
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
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
        timeoutCheerActionSettingsRepository: TimeoutCheerActionSettingsRepositoryInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
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
        elif not isinstance(timeoutCheerActionSettingsRepository, TimeoutCheerActionSettingsRepositoryInterface):
            raise TypeError(f'timeoutCheerActionSettingsRepository argument is malformed: \"{timeoutCheerActionSettingsRepository}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
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
        self.__timeoutCheerActionSettingsRepository: TimeoutCheerActionSettingsRepositoryInterface = timeoutCheerActionSettingsRepository
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface = twitchFollowingStatusRepository
        self.__twitchMessageStringUtils: TwitchMessageStringUtilsInterface = twitchMessageStringUtils
        self.__twitchTimeoutHelper: TwitchTimeoutHelperInterface = twitchTimeoutHelper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def handleTimeoutCheerAction(
        self,
        actions: FrozenList[AbsCheerAction],
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        if not isinstance(actions, FrozenList):
            raise TypeError(f'actions argument is malformed: \"{actions}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
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

        if not user.areCheerActionsEnabled or not user.areTimeoutCheerActionsEnabled:
            return False

        timeoutAction: TimeoutCheerAction | None = None

        for action in actions:
            if isinstance(action, TimeoutCheerAction) and action.isEnabled and action.bits == bits:
                timeoutAction = action
                break

        if timeoutAction is None:
            return False

        userNameToTimeout = await self.__twitchMessageStringUtils.getUserNameFromCheerMessage(message)
        if not utils.isValidStr(userNameToTimeout):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout from {cheerUserName}:{cheerUserId} in {user.getHandle()}, but was unable to find a user name: ({message=}) ({timeoutAction=})')
            return False

        userIdToTimeout = await self.__userIdsRepository.fetchUserId(
            userName = userNameToTimeout,
            twitchAccessToken = userTwitchAccessToken
        )

        if not utils.isValidStr(userIdToTimeout):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout \"{userNameToTimeout}\" from {cheerUserName}:{cheerUserId} in {user.getHandle()}, but was unable to find a user ID: ({message=}) ({timeoutAction=})')
            return False
        elif userIdToTimeout == broadcasterUserId:
            userIdToTimeout = cheerUserId
            userNameToTimeout = cheerUserName
            self.__timber.log('TimeoutCheerActionHelper', f'Attempt to timeout the broadcaster themself from {cheerUserName}:{cheerUserId} in {user.getHandle()}, so will instead time out the user: ({message=}) ({timeoutAction=})')

        return await self.__timeoutUser(
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            twitchChannelId = broadcasterUserId,
            userIdToTimeout = userIdToTimeout,
            userNameToTimeout = userNameToTimeout,
            userTwitchAccessToken = userTwitchAccessToken,
            action = timeoutAction,
            user = user
        )

    async def __isFailedTimeout(
        self,
        now: datetime,
        randomNumber: float,
        cheerUserId: str,
        cheerUserName: str,
        twitchChannelId: str,
        userIdToTimeout: str,
        userNameToTimeout: str,
        user: UserInterface
    ) -> bool:
        if not isinstance(now, datetime):
            raise TypeError(f'now argument is malformed: \"{now}\"')
        elif not utils.isValidNum(randomNumber):
            raise TypeError(f'randomNumber argument is malformed: \"{randomNumber}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')
        elif not utils.isValidStr(userNameToTimeout):
            raise TypeError(f'userNameToTimeout argument is malformed: \"{userNameToTimeout}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if not user.isTimeoutCheerActionFailureEnabled:
            return False
        elif cheerUserId == userIdToTimeout:
            # this user is trying to time themselves out, so don't bother with checking failure probability
            return False

        failureProbability = await self.__timeoutCheerActionSettingsRepository.getFailureProbability()

        if randomNumber <= failureProbability:
            return True
        elif not user.isTimeoutCheerActionIncreasedBullyFailureEnabled:
            return False

        history = await self.__timeoutCheerActionHistoryRepository.get(
            chatterUserId = userIdToTimeout,
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId
        )

        if history.entries is None or len(history.entries) == 0:
            return False

        bullyTimeToLiveDays = await self.__timeoutCheerActionSettingsRepository.getBullyTimeToLiveDays()
        bullyTimeBuffer = timedelta(days = bullyTimeToLiveDays)
        cheerUserOccurrences = 0

        for historyEntry in history.entries:
            if historyEntry.timedOutByUserId != cheerUserId:
                continue
            elif historyEntry.timedOutAtDateTime + bullyTimeBuffer < now:
                continue

            cheerUserOccurrences = cheerUserOccurrences + 1

        if cheerUserOccurrences == 0:
            return False

        maxBullyFailureOccurrences = await self.__timeoutCheerActionSettingsRepository.getMaxBullyFailureOccurrences()
        maxBullyFailureProbability = await self.__timeoutCheerActionSettingsRepository.getMaxBullyFailureProbability()
        perStepFailureProbabilityIncrease = (maxBullyFailureProbability - failureProbability) / float(maxBullyFailureOccurrences)
        cheerUserOccurrences = min(cheerUserOccurrences, maxBullyFailureOccurrences)
        newlyIncreasedFailureProbability = failureProbability + (perStepFailureProbabilityIncrease * float(cheerUserOccurrences))

        if randomNumber > newlyIncreasedFailureProbability:
            return False

        self.__timber.log('TimeoutCheerActionHelper', f'Attempt to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but they were thwarted by increased bully failure probability rates ({randomNumber=}) ({failureProbability=}) ({bullyTimeToLiveDays=}) ({cheerUserOccurrences=}) ({maxBullyFailureOccurrences=}) ({maxBullyFailureProbability=}) ({perStepFailureProbabilityIncrease=}) ({newlyIncreasedFailureProbability=})')
        return True

    async def __isNewFollower(
        self,
        now: datetime,
        followShieldDays: int | None,
        twitchAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str
    ) -> bool:
        if not isinstance(now, datetime):
            raise TypeError(f'now argument is malformed: \"{now}\"')
        elif followShieldDays is not None and not utils.isValidInt(followShieldDays):
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

        if followingStatus.followedAt + minimumFollowDuration >= now:
            self.__timber.log('TimeoutCheerActionHelper', f'The given user ID will not be timed out as this user started following the channel within the minimum follow duration window: ({followingStatus=}) ({minimumFollowDuration=}) ({twitchChannelId=}) ({userIdToTimeout=})')
            return True

        return False

    async def __isReverseTimeout(
        self,
        randomNumber: float,
        user: UserInterface
    ) -> bool:
        if not utils.isValidNum(randomNumber):
            raise TypeError(f'randomNumber argument is malformed: \"{randomNumber}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if not user.isTimeoutCheerActionReverseEnabled:
            return False

        reverseProbability = await self.__timeoutCheerActionSettingsRepository.getReverseProbability()
        return randomNumber <= reverseProbability

    async def __send(self, twitchChannel: TwitchMessageable | None, message: str):
        if twitchChannel is None:
            return

        await self.__twitchUtils.safeSend(twitchChannel, message)

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    async def __timeoutUser(
        self,
        cheerUserId: str,
        cheerUserName: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        twitchChannelId: str,
        userIdToTimeout: str,
        userNameToTimeout: str,
        userTwitchAccessToken: str,
        action: TimeoutCheerAction,
        user: UserInterface
    ) -> bool:
        if not utils.isValidStr(cheerUserId):
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
        elif not utils.isValidStr(userNameToTimeout):
            raise TypeError(f'userNameToTimeout argument is malformed: \"{userNameToTimeout}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(action, TimeoutCheerAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        twitchChannelProvider = self.__twitchChannelProvider
        twitchChannel: TwitchMessageable | None = None

        if twitchChannelProvider is not None:
            twitchChannel = await twitchChannelProvider.getTwitchChannel(user.getHandle())

        if not await self.__verifyStreamStatus(
            twitchChannelId = twitchChannelId,
            timeoutAction = action,
            user = user
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but the current stream status is invalid ({action=})')
            return False

        now = datetime.now(self.__timeZoneRepository.getDefault())

        if await self.__isNewFollower(
            now = now,
            followShieldDays = user.timeoutCheerActionFollowShieldDays,
            twitchAccessToken = userTwitchAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but this user is a new follower ({action=})')
            await self.__send(twitchChannel, f'ⓘ Sorry @{cheerUserName}, but @{userNameToTimeout} has the new follower shield')
            return False

        randomNumber = random.random()
        isReverse = False

        if await self.__isReverseTimeout(
            randomNumber = randomNumber,
            user = user
        ):
            isReverse = True
            self.__timber.log('TimeoutCheerActionHelper', f'Attempt to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but they hit the reverse RNG ({randomNumber=}) ({action=})')
            userIdToTimeout = cheerUserId
            userNameToTimeout = cheerUserName
        elif await self.__isFailedTimeout(
            now = now,
            randomNumber = randomNumber,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout,
            userNameToTimeout = userNameToTimeout,
            user = user
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempt to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but they hit the failure RNG ({randomNumber=}) ({action=})')
            await self.__send(twitchChannel, f'ⓘ Sorry @{cheerUserName}, but your timeout of @{userNameToTimeout} failed 🎲 🎰')
            return False

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = action.durationSeconds,
            reason = f'Cheer timeout from {cheerUserName} — {action.bits} bit(s), {action.durationSeconds} second(s)',
            twitchAccessToken = moderatorTwitchAccessToken,
            twitchChannelAccessToken = userTwitchAccessToken,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout,
            user = user
        )

        if timeoutResult is TwitchTimeoutResult.IMMUNE_USER:
            self.__timber.log('TimeoutCheerActionHelper', f'Attempt to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but they are immune ({randomNumber=}) ({timeoutResult=}) ({action=})')
            await self.__send(twitchChannel, f'⚠️ Sorry @{cheerUserName}, but @{userNameToTimeout} is immune')
            return False
        elif timeoutResult is not TwitchTimeoutResult.SUCCESS:
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but an error occurred ({randomNumber=}) ({timeoutResult=}) ({action=})')
            return False

        self.__timber.log('TimeoutCheerActionHelper', f'Timed out {userNameToTimeout}:{userIdToTimeout} in \"{user.getHandle()}\" due to cheer from {cheerUserName}:{cheerUserId} ({action=})')

        await self.__timeoutCheerActionHistoryRepository.add(
            bitAmount = action.bits,
            durationSeconds = action.durationSeconds,
            chatterUserId = userIdToTimeout,
            timedOutByUserId = cheerUserId,
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId
        )

        await self.__tts(
            isReverse = isReverse,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            twitchChannelId = twitchChannelId,
            userNameToTimeout = userNameToTimeout,
            action = action,
            user = user
        )

        await self.__send(twitchChannel, f'RIPBOZO @{userNameToTimeout} RIPBOZO')
        return True

    async def __tts(
        self,
        isReverse: bool,
        cheerUserId: str,
        cheerUserName: str,
        twitchChannelId: str,
        userNameToTimeout: str,
        action: TimeoutCheerAction,
        user: UserInterface
    ):
        if not user.isTtsEnabled():
            return

        message: str
        if isReverse:
            message = f'Uh oh! {cheerUserName} got themselves timed out for {action.durationSeconds}! rip bozo!'
        else:
            message = f'{cheerUserName} timed out {userNameToTimeout} for {action.durationSecondsStr} seconds! rip bozo!'

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

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId,
            ttsEvent = ttsEvent
        ))

    async def __verifyStreamStatus(
        self,
        twitchChannelId: str,
        timeoutAction: TimeoutCheerAction,
        user: UserInterface
    ) -> bool:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(timeoutAction, TimeoutCheerAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        requirement = timeoutAction.streamStatusRequirement
        if requirement is CheerActionStreamStatusRequirement.ANY:
            return True

        isLive = await self.__isLiveOnTwitchRepository.isLive(twitchChannelId)
        return isLive and requirement is CheerActionStreamStatusRequirement.ONLINE or \
            not isLive and requirement is CheerActionStreamStatusRequirement.OFFLINE
