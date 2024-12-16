import random
from dataclasses import dataclass
from datetime import datetime, timedelta

from .guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from .timeoutActionData import TimeoutActionData
from .timeoutActionHelperInterface import TimeoutActionHelperInterface
from .timeoutActionHistoryRepositoryInterface import TimeoutActionHistoryRepositoryInterface
from .timeoutActionSettingsRepositoryInterface import TimeoutActionSettingsRepositoryInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..timber.timberInterface import TimberInterface
from ..trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ..tts.ttsEvent import TtsEvent
from ..twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ..twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ..twitch.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from ..twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ..twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from ..twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult
from ..twitch.twitchConstantsInterface import TwitchConstantsInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface


class TimeoutActionHelper(TimeoutActionHelperInterface):

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
        twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface,
        twitchConstants: TwitchConstantsInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(guaranteedTimeoutUsersRepository, GuaranteedTimeoutUsersRepositoryInterface):
            raise TypeError(f'guaranteedTimeoutUsersRepository argument is malformed: \"{guaranteedTimeoutUsersRepository}\"')
        elif not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
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
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchChannelEditorsRepository, TwitchChannelEditorsRepositoryInterface):
            raise TypeError(f'twitchChannelEditorsRepository argument is malformed: \"{twitchChannelEditorsRepository}\"')
        elif not isinstance(twitchConstants, TwitchConstantsInterface):
            raise TypeError(f'twitchConstants argument is malformed: \"{twitchConstants}\"')
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface = guaranteedTimeoutUsersRepository
        self.__isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface = isLiveOnTwitchRepository
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface = timeoutActionHistoryRepository
        self.__timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface = timeoutActionSettingsRepository
        self.__timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface = timeoutImmuneUserIdsRepository
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__trollmojiHelper: TrollmojiHelperInterface = trollmojiHelper
        self.__twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface = twitchChannelEditorsRepository
        self.__twitchConstants: TwitchConstantsInterface = twitchConstants
        self.__twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface = twitchFollowingStatusRepository
        self.__twitchTimeoutHelper: TwitchTimeoutHelperInterface = twitchTimeoutHelper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __alertViaTextToSpeech(self, isReverse: bool, timeoutData: TimeoutActionData):
        if not timeoutData.user.isTtsEnabled:
            return

        message: str
        if isReverse:
            message = f'Oh noo! {timeoutData.instigatorUserName} got hit with a reverse! Rip bozo!'
        else:
            message = f'{timeoutData.instigatorUserName} timed out {timeoutData.timeoutTargetUserName} for {timeoutData.durationSecondsStr} seconds! Rip bozo!'

        ttsEvent = TtsEvent(
            message = message,
            twitchChannel = timeoutData.twitchChannel,
            twitchChannelId = timeoutData.twitchChannelId,
            userId = timeoutData.instigatorUserId,
            userName = timeoutData.instigatorUserName,
            donation = None,
            provider = timeoutData.user.defaultTtsProvider,
            raidInfo = None
        )

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = timeoutData.twitchChannel,
            twitchChannelId = timeoutData.twitchChannelId,
            ttsEvent = ttsEvent
        ))

    async def __alertViaTwitchChat(
        self,
        isGuaranteed: bool,
        isReverse: bool,
        diceRoll: DiceRoll,
        rollFailureData: RollFailureData,
        ripBozoEmote: str,
        timeoutData: TimeoutActionData,
        twitchChannel: TwitchChannel
    ):
        message: str

        if isReverse:
            message = f'{ripBozoEmote} Oh noo! @{timeoutData.instigatorUserName} rolled a d{diceRoll.dieSize} and got a {diceRoll.roll} {ripBozoEmote} reverse! {ripBozoEmote} (needed greater than {rollFailureData.reverseRoll}) {ripBozoEmote}'
        elif isGuaranteed or not timeoutData.isRandomChanceEnabled:
            message = f'{ripBozoEmote} @{timeoutData.timeoutTargetUserName} {ripBozoEmote}'
        else:
            message = f'{ripBozoEmote} Timed out @{timeoutData.timeoutTargetUserName} after rolling a d{diceRoll.dieSize} and got a {diceRoll.roll} {ripBozoEmote} (needed greater than {rollFailureData.failureRoll}) {ripBozoEmote}'

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = timeoutData.twitchChatMessageId
        )

    async def __generateRollFailureData(
        self,
        now: datetime,
        diceRoll: DiceRoll,
        timeoutTargetUserId: str,
        timeoutData: TimeoutActionData
    ) -> RollFailureData:
        baseFailureProbability = await self.__timeoutActionSettingsRepository.getFailureProbability()
        maxBullyFailureProbability = await self.__timeoutActionSettingsRepository.getMaxBullyFailureProbability()
        maxBullyFailureOccurrences = await self.__timeoutActionSettingsRepository.getMaxBullyFailureOccurrences()
        perBullyFailureProbabilityIncrease = (maxBullyFailureProbability - baseFailureProbability) / float(maxBullyFailureOccurrences)

        bullyOccurrences = 0

        if timeoutData.user.isTimeoutCheerActionIncreasedBullyFailureEnabled:
            history = await self.__timeoutActionHistoryRepository.get(
                chatterUserId = timeoutTargetUserId,
                twitchChannel = timeoutData.twitchChannel,
                twitchChannelId = timeoutData.twitchChannelId
            )

            bullyTimeToLiveDays = await self.__timeoutActionSettingsRepository.getBullyTimeToLiveDays()
            bullyTimeBuffer = timedelta(days = bullyTimeToLiveDays)

            if history.entries is not None and len(history.entries) >= 1:
                for historyEntry in history.entries:
                    if historyEntry.timedOutByUserId != timeoutData.instigatorUserId:
                        continue
                    elif historyEntry.timedOutAtDateTime + bullyTimeBuffer < now:
                        continue

                    bullyOccurrences += 1

        failureProbability = baseFailureProbability + (perBullyFailureProbabilityIncrease * float(bullyOccurrences))
        failureRoll = int(round(failureProbability * diceRoll.dieSize))

        reverseProbability = await self.__timeoutActionSettingsRepository.getReverseProbability()
        reverseRoll = int(round(reverseProbability * float(diceRoll.dieSize)))

        return TimeoutActionHelper.RollFailureData(
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

    async def __isFailedTimeout(
        self,
        diceRoll: DiceRoll,
        rollFailureData: RollFailureData,
        ripBozoEmote: str,
        timeoutTargetUserName: str,
        timeoutData: TimeoutActionData,
        twitchChannel: TwitchChannel
    ) -> bool:
        if not timeoutData.user.isTimeoutCheerActionFailureEnabled:
            return False
        elif not timeoutData.isRandomChanceEnabled:
            return False
        elif diceRoll.roll > rollFailureData.failureRoll:
            return False

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'{ripBozoEmote} Sorry @{timeoutData.instigatorUserName}, but your timeout of @{timeoutTargetUserName} failed {ripBozoEmote} (rolled a d{diceRoll.dieSize} and got a {diceRoll.roll}, but needed greater than {rollFailureData.failureRoll}) {ripBozoEmote}',
            replyMessageId = timeoutData.twitchChatMessageId
        )

        return True

    async def __isGuaranteedTimeoutUser(
        self,
        timeoutTargetUserId: str
    ) -> bool:
        return await self.__guaranteedTimeoutUsersRepository.isGuaranteed(timeoutTargetUserId)

    async def __isImmuneUser(
        self,
        timeoutTargetUserId: str,
        timeoutTargetUserName: str,
        timeoutData: TimeoutActionData,
        twitchChannel: TwitchChannel
    ) -> bool:
        if not await self.__timeoutImmuneUserIdsRepository.isImmune(timeoutTargetUserId):
            return False
        elif not await self.__twitchChannelEditorsRepository.isEditor(
            chatterUserId = timeoutTargetUserId,
            twitchChannelId = timeoutData.twitchChannelId
        ):
            return False

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'⚠ Sorry @{timeoutData.instigatorUserName}, but @{timeoutTargetUserName} is an immune user',
            replyMessageId = timeoutData.twitchChatMessageId
        )

        return True

    async def __isReverseTimeout(
        self,
        diceRoll: DiceRoll,
        rollFailureData: RollFailureData,
        timeoutData: TimeoutActionData
    ) -> bool:
        if not timeoutData.user.isTimeoutCheerActionReverseEnabled:
            return False
        elif not timeoutData.isRandomChanceEnabled:
            return False

        return diceRoll.roll < rollFailureData.reverseRoll

    async def __isTryingToTimeoutTheStreamer(
        self,
        timeoutTargetUserId: str,
        timeoutData: TimeoutActionData
    ) -> bool:
        return timeoutTargetUserId == timeoutData.twitchChannelId

    async def __hasNewFollowerShield(
        self,
        now: datetime,
        ripBozoEmote: str,
        timeoutTargetUserId: str,
        timeoutTargetUserName: str,
        timeoutData: TimeoutActionData,
        twitchChannel: TwitchChannel
    ) -> bool:
        followShieldDays = timeoutData.user.timeoutActionFollowShieldDays

        if followShieldDays is None:
            # this user doesn't use a follow shield
            return False

        followingStatus = await self.__twitchFollowingStatusRepository.fetchFollowingStatus(
            twitchAccessToken = timeoutData.userTwitchAccessToken,
            twitchChannelId = timeoutData.twitchChannelId,
            userId = timeoutTargetUserId
        )

        minimumFollowDuration = timedelta(days = followShieldDays)

        if followingStatus is not None and followingStatus.followedAt + minimumFollowDuration < now:
            return False

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'⚠ Wow @{timeoutData.instigatorUserName} are you trying to bully? @{timeoutTargetUserName} has the new follower shield! {ripBozoEmote}',
            replyMessageId = timeoutData.twitchChatMessageId
        )

        return True

    async def __rollDice(self) -> DiceRoll:
        dieSize = await self.__timeoutActionSettingsRepository.getDieSize()
        roll = random.randint(1, dieSize)

        return TimeoutActionHelper.DiceRoll(
            dieSize = dieSize,
            roll = roll
        )

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    async def timeout(self, timeoutData: TimeoutActionData) -> bool:
        if not isinstance(timeoutData, TimeoutActionData):
            raise TypeError(f'timeoutData argument is malformed: \"{timeoutData}\"')

        twitchChannelProvider = self.__twitchChannelProvider
        if twitchChannelProvider is None:
            self.__timber.log('TimeoutActionHelper', f'No TwitchChannelProvider instance has been set: \"{twitchChannelProvider}\"')
            return False

        twitchChannel = await twitchChannelProvider.getTwitchChannel(timeoutData.twitchChannel)
        isGuaranteed = False
        isReverse = False
        timeoutTargetUserId = timeoutData.timeoutTargetUserId
        timeoutTargetUserName = timeoutData.timeoutTargetUserName
        now = datetime.now(self.__timeZoneRepository.getDefault())
        diceRoll = await self.__rollDice()

        rollFailureData = await self.__generateRollFailureData(
            now = now,
            diceRoll = diceRoll,
            timeoutTargetUserId = timeoutTargetUserId,
            timeoutData = timeoutData
        )

        ripBozoEmote = await self.__trollmojiHelper.getGottemEmoteOrBackup()

        if not await self.__verifyStreamStatus(
            timeoutData = timeoutData
        ):
            self.__timber.log('TimeoutActionHelper', f'Attempted to timeout {timeoutTargetUserName}:{timeoutTargetUserId} by {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} in {timeoutData.twitchChannel}, but the current stream status is invalid ({timeoutData=})')
            return False

        elif await self.__isGuaranteedTimeoutUser(
            timeoutTargetUserId = timeoutTargetUserId
        ):
            self.__timber.log('TimeoutActionHelper', f'Attempting to timeout {timeoutTargetUserName}:{timeoutTargetUserId} by {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} in {timeoutData.twitchChannel}, who is a guaranteed timeout user ({timeoutData=})')
            isGuaranteed = True

        elif await self.__isTryingToTimeoutTheStreamer(
            timeoutTargetUserId = timeoutTargetUserId,
            timeoutData = timeoutData
        ):
            self.__timber.log('TimeoutActionHelper', f'Attempted to timeout {timeoutTargetUserName}:{timeoutTargetUserId} by {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} in {timeoutData.twitchChannel}, but user ID \"{timeoutTargetUserId}\" is the streamer, so they will be hit with a reverse ({timeoutData=})')
            isReverse = True
            timeoutTargetUserId = timeoutData.instigatorUserId
            timeoutTargetUserName = timeoutData.instigatorUserName

        elif await self.__isImmuneUser(
            timeoutTargetUserId = timeoutTargetUserId,
            timeoutTargetUserName = timeoutTargetUserName,
            timeoutData = timeoutData,
            twitchChannel = twitchChannel
        ):
            self.__timber.log('TimeoutActionHelper', f'Attempted to timeout {timeoutTargetUserName}:{timeoutTargetUserId} by {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} in {timeoutData.twitchChannel}, but user ID \"{timeoutTargetUserId}\" is immune ({timeoutData=})')
            return False

        elif await self.__hasNewFollowerShield(
            now = now,
            ripBozoEmote = ripBozoEmote,
            timeoutTargetUserId = timeoutTargetUserId,
            timeoutTargetUserName = timeoutTargetUserName,
            timeoutData = timeoutData,
            twitchChannel = twitchChannel
        ):
            self.__timber.log('TimeoutActionHelper', f'Attempted to timeout {timeoutTargetUserName}:{timeoutTargetUserId} by {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} in {timeoutData.twitchChannel}, but this user is a new follower ({timeoutData=})')
            return False

        elif await self.__isReverseTimeout(
            diceRoll = diceRoll,
            rollFailureData = rollFailureData,
            timeoutData = timeoutData
        ):
            self.__timber.log('TimeoutActionHelper', f'Attempted to timeout {timeoutTargetUserName}:{timeoutTargetUserId} by {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} in {timeoutData.twitchChannel}, but they hit the reverse roll ({diceRoll=}) ({rollFailureData=}) ({timeoutData=})')
            isReverse = True
            timeoutTargetUserId = timeoutData.instigatorUserId
            timeoutTargetUserName = timeoutData.instigatorUserName

        elif await self.__isFailedTimeout(
            diceRoll = diceRoll,
            rollFailureData = rollFailureData,
            ripBozoEmote = ripBozoEmote,
            timeoutTargetUserName = timeoutTargetUserName,
            twitchChannel= twitchChannel,
            timeoutData = timeoutData
        ):
            self.__timber.log('TimeoutActionHelper', f'Attempted to timeout {timeoutTargetUserName}:{timeoutTargetUserId} by {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} in {timeoutData.twitchChannel}, but they hit the failure roll ({diceRoll=}) ({rollFailureData=}) ({timeoutData=})')
            return False

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = timeoutData.durationSeconds,
            reason = f'Timeout from {timeoutData.instigatorUserName} — {timeoutData.durationSeconds} second(s)',
            twitchAccessToken = timeoutData.moderatorTwitchAccessToken,
            twitchChannelAccessToken = timeoutData.userTwitchAccessToken,
            twitchChannelId = timeoutData.twitchChannelId,
            userIdToTimeout = timeoutTargetUserId,
            user = timeoutData.user
        )

        if timeoutResult is not TwitchTimeoutResult.SUCCESS:
            self.__timber.log('TimeoutActionHelper', f'Attempted to timeout {timeoutTargetUserName}:{timeoutTargetUserId} by {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} in {timeoutData.twitchChannel}, but an error occurred ({timeoutResult=}) ({diceRoll=}) ({rollFailureData=}) ({timeoutData=})')
            return False

        self.__timber.log('TimeoutActionHelper', f'Timed out {timeoutTargetUserName}:{timeoutTargetUserId} in \"{timeoutData.twitchChannel}\" from {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} ({diceRoll=}) ({rollFailureData=}) ({timeoutResult=}) ({timeoutData=})')

        await self.__timeoutActionHistoryRepository.add(
            durationSeconds = timeoutData.durationSeconds,
            chatterUserId = timeoutTargetUserId,
            timedOutByUserId = timeoutData.instigatorUserId,
            twitchChannel = timeoutData.twitchChannel,
            twitchChannelId = timeoutData.twitchChannelId
        )

        await self.__alertViaTextToSpeech(
            isReverse = isReverse,
            timeoutData = timeoutData
        )

        await self.__alertViaTwitchChat(
            isGuaranteed = isGuaranteed,
            isReverse = isReverse,
            diceRoll = diceRoll,
            rollFailureData = rollFailureData,
            ripBozoEmote = ripBozoEmote,
            timeoutData = timeoutData,
            twitchChannel = twitchChannel
        )

        return True

    async def __verifyStreamStatus(
        self,
        timeoutData: TimeoutActionData
    ) -> bool:
        requirement = timeoutData.streamStatusRequirement
        if requirement is TimeoutActionData.StreamStatusRequirement.ANY:
            return True

        isLive = await self.__isLiveOnTwitchRepository.isLive(timeoutData.twitchChannelId)
        return isLive and requirement is TimeoutActionData.StreamStatusRequirement.ONLINE or \
            not isLive and requirement is TimeoutActionData.StreamStatusRequirement.OFFLINE
