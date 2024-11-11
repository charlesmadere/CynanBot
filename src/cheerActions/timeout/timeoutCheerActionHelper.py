import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Collection

from .timeoutCheerActionHelperInterface import TimeoutCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..timeoutCheerAction import TimeoutCheerAction
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...timeout.guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from ...timeout.timeoutActionHistoryRepositoryInterface import TimeoutActionHistoryRepositoryInterface
from ...timeout.timeoutActionSettingsRepositoryInterface import TimeoutActionSettingsRepositoryInterface
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ...tts.ttsEvent import TtsEvent
from ...twitch.configuration.twitchChannel import TwitchChannel
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ...twitch.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from ...twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TimeoutCheerActionHelper(TimeoutCheerActionHelperInterface):

    @dataclass(frozen = True)
    class DiceRoll:
        dieSize: int
        roll: int

    @dataclass(frozen = True)
    class RollFailureData:
        baseFailureProbability: float
        failureProbability: float
        maxBullyFailureProbability: float
        perBullyFailureProbabilityIncrease: float
        reverseProbability: float
        bullyOccurrences: int
        failureRoll: int
        maxBullyFailureOccurrences: int
        reverseRoll: int

    def __init__(
        self,
        guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface,
        timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
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
        elif not isinstance(timeoutActionHistoryRepository, TimeoutActionHistoryRepositoryInterface):
            raise TypeError(f'timeoutActionHistoryRepository argument is malformed: \"{timeoutActionHistoryRepository}\"')
        elif not isinstance(timeoutActionSettingsRepository, TimeoutActionSettingsRepositoryInterface):
            raise TypeError(f'timeoutActionSettingsRepository argument is malformed: \"{timeoutActionSettingsRepository}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
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
        self.__timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface = timeoutActionHistoryRepository
        self.__timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface = timeoutActionSettingsRepository
        self.__timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface = timeoutImmuneUserIdsRepository
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
        isGuaranteed: bool,
        isReverse: bool,
        diceRoll: DiceRoll,
        rollFailureData: RollFailureData,
        ripBozoEmote: str,
        twitchChatMessageId: str | None,
        userNameToTimeout: str,
        twitchChannel: TwitchChannel
    ):
        message: str
        if isReverse:
            message = f'{ripBozoEmote} Oh noo! @{userNameToTimeout} rolled a d{diceRoll.dieSize} and got a {diceRoll.roll} {ripBozoEmote} reverse! {ripBozoEmote} (needed greater than {rollFailureData.reverseRoll}) {ripBozoEmote}'
        elif isGuaranteed:
            message = f'{ripBozoEmote} @{userNameToTimeout} {ripBozoEmote}'
        else:
            message = f'{ripBozoEmote} Timed out @{userNameToTimeout} after rolling a d{diceRoll.dieSize} and got a {diceRoll.roll} {ripBozoEmote} (needed greater than {rollFailureData.failureRoll}) {ripBozoEmote}'

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = twitchChatMessageId
        )

    async def __generateRollFailureData(
        self,
        now: datetime,
        diceRoll: DiceRoll,
        cheerUserId: str,
        twitchChannelId: str,
        userIdToTimeout: str,
        user: UserInterface
    ) -> RollFailureData:
        baseFailureProbability = await self.__timeoutActionSettingsRepository.getFailureProbability()
        maxBullyFailureProbability = await self.__timeoutActionSettingsRepository.getMaxBullyFailureProbability()
        maxBullyFailureOccurrences = await self.__timeoutActionSettingsRepository.getMaxBullyFailureOccurrences()
        perBullyFailureProbabilityIncrease = (maxBullyFailureProbability - baseFailureProbability) / float(maxBullyFailureOccurrences)

        bullyOccurrences = 0

        if user.isTimeoutCheerActionIncreasedBullyFailureEnabled:
            history = await self.__timeoutActionHistoryRepository.get(
                chatterUserId = userIdToTimeout,
                twitchChannel = user.getHandle(),
                twitchChannelId = twitchChannelId
            )

            bullyTimeToLiveDays = await self.__timeoutActionSettingsRepository.getBullyTimeToLiveDays()
            bullyTimeBuffer = timedelta(days = bullyTimeToLiveDays)

            if history.entries is not None and len(history.entries) >= 1:
                for historyEntry in history.entries:
                    if historyEntry.timedOutByUserId != cheerUserId:
                        continue
                    elif historyEntry.timedOutAtDateTime + bullyTimeBuffer < now:
                        continue

                    bullyOccurrences += 1

        failureProbability = baseFailureProbability + (perBullyFailureProbabilityIncrease * float(bullyOccurrences))
        failureRoll = int(round(failureProbability * diceRoll.dieSize))

        reverseProbability = await self.__timeoutActionSettingsRepository.getReverseProbability()
        reverseRoll = int(round(reverseProbability * float(diceRoll.dieSize)))

        return TimeoutCheerActionHelper.RollFailureData(
            baseFailureProbability = baseFailureProbability,
            failureProbability = failureProbability,
            maxBullyFailureProbability = maxBullyFailureProbability,
            perBullyFailureProbabilityIncrease = perBullyFailureProbabilityIncrease,
            reverseProbability = reverseProbability,
            bullyOccurrences = bullyOccurrences,
            failureRoll = failureRoll,
            maxBullyFailureOccurrences = maxBullyFailureOccurrences,
            reverseRoll = reverseRoll
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
        diceRoll: DiceRoll,
        rollFailureData: RollFailureData,
        cheerUserName: str,
        ripBozoEmote: str,
        twitchChatMessageId: str | None,
        userNameToTimeout: str,
        twitchChannel: TwitchChannel,
        user: UserInterface
    ) -> bool:
        if not user.isTimeoutCheerActionFailureEnabled or diceRoll.roll > rollFailureData.failureRoll:
            return False

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'{ripBozoEmote} Sorry @{cheerUserName}, but your timeout of @{userNameToTimeout} failed {ripBozoEmote} (rolled a d{diceRoll.dieSize} and got a {diceRoll.roll}, but needed greater than {rollFailureData.failureRoll}) {ripBozoEmote}',
            replyMessageId = twitchChatMessageId
        )

        return True

    async def __isGuaranteedTimeoutUser(
        self,
        userIdToTimeout: str
    ) -> bool:
        return await self.__guaranteedTimeoutUsersRepository.isGuaranteed(userIdToTimeout)

    async def __isImmuneUser(
        self,
        cheerUserName: str,
        twitchChatMessageId: str | None,
        userIdToTimeout: str,
        userNameToTimeout: str,
        twitchChannel: TwitchChannel
    ) -> bool:
        if not await self.__timeoutImmuneUserIdsRepository.isImmune(userIdToTimeout):
            return False

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'⚠ Sorry @{cheerUserName}, but @{userNameToTimeout} is an immune user',
            replyMessageId = twitchChatMessageId
        )

        return True

    async def __hasNewFollowerShield(
        self,
        now: datetime,
        cheerUserName: str,
        twitchAccessToken: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        userIdToTimeout: str,
        userNameToTimeout: str,
        twitchChannel: TwitchChannel,
        user: UserInterface
    ) -> bool:
        followShieldDays = user.timeoutCheerActionFollowShieldDays

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
            message = f'⚠ Wow @{cheerUserName} are you trying to bully? @{userNameToTimeout} has the new follower shield!',
            replyMessageId = twitchChatMessageId
        )

        return True

    async def __isReverseTimeout(
        self,
        diceRoll: DiceRoll,
        rollFailureData: RollFailureData,
        user: UserInterface
    ) -> bool:
        if not user.isTimeoutCheerActionReverseEnabled:
            return False

        return diceRoll.roll < rollFailureData.reverseRoll

    async def __isTryingToTimeoutTheStreamer(
        self,
        twitchChannelId: str,
        userIdToTimeout: str
    ) -> bool:
        return twitchChannelId == userIdToTimeout

    async def __rollDice(self) -> DiceRoll:
        dieSize = await self.__timeoutActionSettingsRepository.getDieSize()
        roll = random.randint(1, dieSize)

        return TimeoutCheerActionHelper.DiceRoll(
            dieSize = dieSize,
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
        isGuaranteed = False
        isReverse = False
        now = datetime.now(self.__timeZoneRepository.getDefault())
        diceRoll = await self.__rollDice()

        rollFailureData = await self.__generateRollFailureData(
            now = now,
            diceRoll = diceRoll,
            cheerUserId = cheerUserId,
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout,
            user = user
        )

        ripBozoEmote = await self.__trollmojiHelper.getGottemEmoteOrBackup()

        if not await self.__verifyStreamStatus(
            twitchChannelId = twitchChannelId,
            timeoutAction = action,
            user = user
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but the current stream status is invalid ({action=})')
            return False

        elif await self.__isGuaranteedTimeoutUser(
            userIdToTimeout = userIdToTimeout
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempting to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, who is a guaranteed timeout user ({action=})')
            isGuaranteed = True

        elif await self.__isImmuneUser(
            cheerUserName = cheerUserName,
            twitchChatMessageId = twitchChatMessageId,
            userIdToTimeout = userIdToTimeout,
            userNameToTimeout = userNameToTimeout,
            twitchChannel = twitchChannel
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but user ID \"{userIdToTimeout}\" is immune ({action=})')
            return False

        elif await self.__isTryingToTimeoutTheStreamer(
            twitchChannelId = twitchChannelId,
            userIdToTimeout = userIdToTimeout
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but user ID \"{userIdToTimeout}\" is the streamer, so they will be hit with a reverse ({action=})')
            isReverse = True
            userIdToTimeout = cheerUserId
            userNameToTimeout = cheerUserName

        elif await self.__hasNewFollowerShield(
            now = now,
            cheerUserName = cheerUserName,
            twitchAccessToken = userTwitchAccessToken,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
            userIdToTimeout = userIdToTimeout,
            userNameToTimeout = userNameToTimeout,
            twitchChannel = twitchChannel,
            user = user
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but this user is a new follower ({action=})')
            return False

        elif await self.__isReverseTimeout(
            diceRoll = diceRoll,
            rollFailureData = rollFailureData,
            user = user
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but they hit the reverse roll ({diceRoll=}) ({rollFailureData=}) ({action=})')
            isReverse = True
            userIdToTimeout = cheerUserId
            userNameToTimeout = cheerUserName

        elif await self.__isFailedTimeout(
            diceRoll = diceRoll,
            rollFailureData = rollFailureData,
            cheerUserName = cheerUserName,
            ripBozoEmote = ripBozoEmote,
            twitchChatMessageId = twitchChatMessageId,
            userNameToTimeout = userNameToTimeout,
            twitchChannel = twitchChannel,
            user = user
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but they hit the failure roll ({diceRoll=}) ({rollFailureData=}) ({action=})')
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
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout {userNameToTimeout}:{userIdToTimeout} by {cheerUserName}:{cheerUserId} in {user.getHandle()}, but an error occurred ({timeoutResult=}) ({diceRoll=}) ({rollFailureData=}) ({action=})')
            return False

        self.__timber.log('TimeoutCheerActionHelper', f'Timed out {userNameToTimeout}:{userIdToTimeout} in \"{user.getHandle()}\" due to cheer from {cheerUserName}:{cheerUserId} ({diceRoll=}) ({rollFailureData=}) ({timeoutResult=}) ({action=})')

        await self.__timeoutActionHistoryRepository.add(
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
            isGuaranteed = isGuaranteed,
            isReverse = isReverse,
            diceRoll = diceRoll,
            rollFailureData = rollFailureData,
            ripBozoEmote = ripBozoEmote,
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
