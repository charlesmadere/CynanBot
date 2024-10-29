import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Collection

from .guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
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
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ...tts.ttsEvent import TtsEvent
from ...twitch.configuration.twitchChannel import TwitchChannel
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ...twitch.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from ...twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from ...twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TimeoutCheerActionHelper(TimeoutCheerActionHelperInterface):

    @dataclass(frozen = True)
    class DiceRoll:
        maxRoll: int
        roll: int

    def __init__(
        self,
        guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        timeoutCheerActionHistoryRepository: TimeoutCheerActionHistoryRepositoryInterface,
        timeoutCheerActionSettingsRepository: TimeoutCheerActionSettingsRepositoryInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif not isinstance(guaranteedTimeoutUsersRepository, GuaranteedTimeoutUsersRepositoryInterface):
            raise TypeError(f'guaranteedTimeoutUsersRepository argument is malformed: \"{guaranteedTimeoutUsersRepository}\"')
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
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
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

        self.__guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface = guaranteedTimeoutUsersRepository
        self.__isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface = isLiveOnTwitchRepository
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__timeoutCheerActionHistoryRepository: TimeoutCheerActionHistoryRepositoryInterface = timeoutCheerActionHistoryRepository
        self.__timeoutCheerActionSettingsRepository: TimeoutCheerActionSettingsRepositoryInterface = timeoutCheerActionSettingsRepository
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__trollmojiHelper: TrollmojiHelperInterface = trollmojiHelper
        self.__twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface = twitchFollowingStatusRepository
        self.__twitchMessageStringUtils: TwitchMessageStringUtilsInterface = twitchMessageStringUtils
        self.__twitchTimeoutHelper: TwitchTimeoutHelperInterface = twitchTimeoutHelper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __alertViaTextToSpeech(
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
            message = f'Oh noo! {userNameToTimeout} got hit with a reverse! Rip bozo!'
        else:
            message = f'{cheerUserName} timed out {userNameToTimeout} for {action.durationSecondsStr} seconds! Rip bozo!'

        ttsEvent = TtsEvent(
            message = message,
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId,
            userId = cheerUserId,
            userName = cheerUserName,
            donation = None,
            provider = user.defaultTtsProvider,
            raidInfo = None
        )

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId,
            ttsEvent = ttsEvent
        ))

    async def __alertViaTwitchChat(
        self,
        isReverse: bool,
        twitchChatMessageId: str | None,
        userNameToTimeout: str,
        twitchChannel: TwitchChannel
    ):
        ripbozoEmote = await self.__trollmojiHelper.getGottemEmote()
        if not utils.isValidStr(ripbozoEmote):
            ripbozoEmote = 'RIPBOZO'

        message: str
        if isReverse:
            message = f'Oh noo! @{userNameToTimeout} got hit with a reverse! {ripbozoEmote}'
        else:
            message = f'{ripbozoEmote} @{userNameToTimeout} {ripbozoEmote}'

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = twitchChatMessageId
        )

    async def handleTimeoutCheerAction(
        self,
        actions: Collection[AbsCheerAction],
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        twitchChatMessageId: str | None,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        if not isinstance(actions, Collection):
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
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
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

        twitchChannelProvider = self.__twitchChannelProvider
        if twitchChannelProvider is None:
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout \"{userNameToTimeout}\" from {cheerUserName}:{cheerUserId} in {user.getHandle()}, but no TwitchChannelProvider has been set: ({twitchChannelProvider=}) ({message=}) ({timeoutAction=})')
            return False

        return await self.__timeoutUser(
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            twitchChannelId = broadcasterUserId,
            twitchChatMessageId = twitchChatMessageId,
            userIdToTimeout = userIdToTimeout,
            userNameToTimeout = userNameToTimeout,
            userTwitchAccessToken = userTwitchAccessToken,
            action = timeoutAction,
            twitchChannelProvider = twitchChannelProvider,
            user = user
        )

    async def __isFailedTimeout(
        self,
        now: datetime,
        diceRoll: DiceRoll,
        cheerUserId: str,
        cheerUserName: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        userIdToTimeout: str,
        userNameToTimeout: str,
        twitchChannel: TwitchChannel,
        user: UserInterface
    ) -> bool:
        if not user.isTimeoutCheerActionFailureEnabled:
            return False
        elif cheerUserId == userIdToTimeout:
            # this user is trying to time themselves out, so don't bother with checking failure probability
            return False
        elif userIdToTimeout in await self.__guaranteedTimeoutUsersRepository.getUserIds():
            # this user is trying to time out a user who should always get timed out
            return False

        failureProbability = await self.__timeoutCheerActionSettingsRepository.getFailureProbability()
        failureRoll = int(round(failureProbability * diceRoll.maxRoll))

        if diceRoll.roll < failureRoll:
            await self.__twitchUtils.safeSend(
                messageable = twitchChannel,
                message = f'ⓘ Sorry @{cheerUserName}, but your timeout of @{userNameToTimeout} failed 🎲 🎰 (rolled d{diceRoll.roll} but needed greater than d{failureRoll}) 🎲 🎰',
                replyMessageId = twitchChatMessageId
            )

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
        cheerUserOccurrences = int(min(cheerUserOccurrences, maxBullyFailureOccurrences))
        newlyIncreasedFailureProbability = failureProbability + (perStepFailureProbabilityIncrease * float(cheerUserOccurrences))
        newlyIncreasedFailureRoll = int(round(newlyIncreasedFailureProbability * diceRoll.maxRoll))

        if diceRoll.roll < newlyIncreasedFailureRoll:
            await self.__twitchUtils.safeSend(
                messageable = twitchChannel,
                message = f'ⓘ Sorry @{cheerUserName}, but your timeout of @{userNameToTimeout} failed 🎲 🎰 (rolled d{diceRoll.roll} but needed greater than d{newlyIncreasedFailureRoll}) 🎲 🎰',
                replyMessageId = twitchChatMessageId
            )

            return True

        return False

    async def __isImmuneUser(
        self,
        userIdToTimeout: str
    ) -> bool:
        # TODO
        return False

    async def __hasNewFollowerShield(
        self,
        now: datetime,
        cheerUserName: str,
        followShieldDays: int | None,
        twitchAccessToken: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        userIdToTimeout: str,
        userNameToTimeout: str,
        twitchChannel: TwitchChannel
    ) -> bool:
        if followShieldDays is None:
            # this user doesn't use a follow shield
            return False

        followingStatus = await self.__twitchFollowingStatusRepository.fetchFollowingStatus(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userId = userIdToTimeout
        )

        minimumFollowDuration = timedelta(days = followShieldDays)

        if followingStatus is not None and followingStatus.followedAt + minimumFollowDuration < now:
            return False

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'ⓘ Wow @{cheerUserName} are you trying to bully? @{userNameToTimeout} has the new follower shield!',
            replyMessageId = twitchChatMessageId
        )

        return True


    async def __isReverseTimeout(
        self,
        diceRoll: DiceRoll,
        user: UserInterface
    ) -> bool:
        if not user.isTimeoutCheerActionReverseEnabled:
            return False

        reverseProbability = await self.__timeoutCheerActionSettingsRepository.getReverseProbability()
        reverseRoll = int(round(reverseProbability * float(diceRoll.maxRoll)))

        return diceRoll.roll < reverseRoll

    async def __isTryingToTimeoutTheStreamer(
        self,
        twitchChannelId: str,
        userIdToTimeout: str
    ) -> bool:
        return twitchChannelId == userIdToTimeout

    async def __rollTheDice(self) -> DiceRoll:
        randomNumber = random.random()
        maxRoll = await self.__timeoutCheerActionSettingsRepository.getDiceMaxRoll()
        roll = int(round(randomNumber * float(maxRoll)))

        return TimeoutCheerActionHelper.DiceRoll(
            maxRoll = maxRoll,
            roll = roll
        )

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
        twitchChatMessageId: str | None,
        userIdToTimeout: str,
        userNameToTimeout: str,
        userTwitchAccessToken: str,
        action: TimeoutCheerAction,
        twitchChannelProvider: TwitchChannelProvider,
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
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')
        elif not utils.isValidStr(userNameToTimeout):
            raise TypeError(f'userNameToTimeout argument is malformed: \"{userNameToTimeout}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(action, TimeoutCheerAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise TypeError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.getHandle())
        proceedWithTimeout = True
        isReverse = False
        now = datetime.now(self.__timeZoneRepository.getDefault())
        diceRoll = await self.__rollTheDice()

        if not await self.__verifyStreamStatus(
            twitchChannelId = twitchChannelId,
            timeoutAction = action,
            user = user
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but the current stream status is invalid ({action=})')
            proceedWithTimeout = False

        elif await self.__isTryingToTimeoutTheStreamer(
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempt to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but user ID {userIdToTimeout} is the streamer, so they will be hit with a reverse ({action=})')
            isReverse = True
            userIdToTimeout = cheerUserId
            userNameToTimeout = cheerUserName

        elif await self.__isImmuneUser(
            userIdToTimeout = userIdToTimeout
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempt to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but user ID {userIdToTimeout} is immune ({action=})')
            proceedWithTimeout = False

            await self.__twitchUtils.safeSend(
                messageable = twitchChannel,
                message = f'⚠️ Sorry @{cheerUserName}, but @{userNameToTimeout} is an immune user',
                replyMessageId = twitchChatMessageId
            )

        elif await self.__hasNewFollowerShield(
            now = now,
            followShieldDays = user.timeoutCheerActionFollowShieldDays,
            cheerUserName = cheerUserName,
            twitchAccessToken = userTwitchAccessToken,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
            userIdToTimeout = userIdToTimeout,
            userNameToTimeout = userNameToTimeout,
            twitchChannel = twitchChannel
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but this user is a new follower ({action=})')
            proceedWithTimeout = False

        elif await self.__isReverseTimeout(
            diceRoll = diceRoll,
            user = user
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempt to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but they hit the reverse roll ({diceRoll=}) ({action=})')
            isReverse = True
            userIdToTimeout = cheerUserId
            userNameToTimeout = cheerUserName

        elif await self.__isFailedTimeout(
            now = now,
            diceRoll = diceRoll,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
            userIdToTimeout = userIdToTimeout,
            userNameToTimeout = userNameToTimeout,
            twitchChannel = twitchChannel,
            user = user
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempt to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but they hit the failure roll ({diceRoll=}) ({action=})')
            proceedWithTimeout = False

        if not proceedWithTimeout:
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

        if timeoutResult is not TwitchTimeoutResult.SUCCESS:
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but an error occurred ({timeoutResult=}) ({action=})')
            return False

        self.__timber.log('TimeoutCheerActionHelper', f'Timed out {userNameToTimeout}:{userIdToTimeout} in \"{user.getHandle()}\" due to cheer from {cheerUserName}:{cheerUserId} ({diceRoll=}) ({action=})')

        await self.__timeoutCheerActionHistoryRepository.add(
            bitAmount = action.bits,
            durationSeconds = action.durationSeconds,
            chatterUserId = userIdToTimeout,
            timedOutByUserId = cheerUserId,
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId
        )

        await self.__alertViaTextToSpeech(
            isReverse = isReverse,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            twitchChannelId = twitchChannelId,
            userNameToTimeout = userNameToTimeout,
            action = action,
            user = user
        )

        await self.__alertViaTwitchChat(
            isReverse = isReverse,
            twitchChatMessageId = twitchChatMessageId,
            userNameToTimeout = userNameToTimeout,
            twitchChannel = twitchChannel
        )

        return True

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
