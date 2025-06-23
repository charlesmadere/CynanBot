import asyncio
import locale
import queue
import random
import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta
from queue import SimpleQueue

from frozenlist import FrozenList

from .guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from .timeoutActionData import TimeoutActionData
from .timeoutActionHelperInterface import TimeoutActionHelperInterface
from .timeoutActionHistoryRepositoryInterface import TimeoutActionHistoryRepositoryInterface
from .timeoutActionSettingsRepositoryInterface import TimeoutActionSettingsRepositoryInterface
from .timeoutActionType import TimeoutActionType
from .timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ..asplodieStats.repository.asplodieStatsRepositoryInterface import AsplodieStatsRepositoryInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..soundPlayerManager.soundAlert import SoundAlert
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..timber.timberInterface import TimberInterface
from ..trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ..twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ..twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ..twitch.isLive.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from ..twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ..twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from ..twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult
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
        activeChattersRepository: ActiveChattersRepositoryInterface,
        asplodieStatsRepository: AsplodieStatsRepositoryInterface,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface,
        timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface,
        twitchUtils: TwitchUtilsInterface,
        queueTimeoutSeconds: int = 3
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(asplodieStatsRepository, AsplodieStatsRepositoryInterface):
            raise TypeError(f'asplodieStatsRepository argument is malformed: \"{asplodieStatsRepository}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(guaranteedTimeoutUsersRepository, GuaranteedTimeoutUsersRepositoryInterface):
            raise TypeError(f'guaranteedTimeoutUsersRepository argument is malformed: \"{guaranteedTimeoutUsersRepository}\"')
        elif not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
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
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidInt(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__activeChattersRepository: ActiveChattersRepositoryInterface = activeChattersRepository
        self.__asplodieStatsRepository: AsplodieStatsRepositoryInterface = asplodieStatsRepository
        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface = guaranteedTimeoutUsersRepository
        self.__isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface = isLiveOnTwitchRepository
        self.__soundPlayerManagerProvider: SoundPlayerManagerProviderInterface = soundPlayerManagerProvider
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface = timeoutActionHistoryRepository
        self.__timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface = timeoutActionSettingsRepository
        self.__timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface = timeoutImmuneUserIdsRepository
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__trollmojiHelper: TrollmojiHelperInterface = trollmojiHelper
        self.__twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface = twitchChannelEditorsRepository
        self.__twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface = twitchFollowingStatusRepository
        self.__twitchTimeoutHelper: TwitchTimeoutHelperInterface = twitchTimeoutHelper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__queueTimeoutSeconds: int = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__actionQueue: SimpleQueue[TimeoutActionData] = SimpleQueue()
        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __alertViaSoundAndTextToSpeech(
        self,
        isReverse: bool,
        timeoutTargetUserName: str,
        timeoutData: TimeoutActionData
    ):
        match timeoutData.actionType:
            case TimeoutActionType.AIR_STRIKE:
                # Air Strike actions don't play alerts here
                pass

            case TimeoutActionType.GRENADE:
                await self.__alertViaSoundAndTextToSpeechForGrenade(
                    timeoutData = timeoutData
                )

            case TimeoutActionType.TARGETED:
                await self.__alertViaSoundAndTextToSpeechForTargeted(
                    isReverse = isReverse,
                    timeoutTargetUserName = timeoutTargetUserName,
                    timeoutData = timeoutData
                )

            case _:
                raise ValueError(f'Unknown TimeoutActionType: \"{timeoutData}\"')

    async def __alertViaSoundAndTextToSpeechForGrenade(
        self,
        timeoutData: TimeoutActionData
    ):
        soundAlert = await self.__chooseGrenadeSoundAlert(timeoutData)

        if soundAlert is None:
            return

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
        await soundPlayerManager.playSoundAlert(soundAlert)

    async def __alertViaSoundAndTextToSpeechForTargeted(
        self,
        isReverse: bool,
        timeoutTargetUserName: str,
        timeoutData: TimeoutActionData
    ):
        soundAlert = await self.__chooseGrenadeSoundAlert(timeoutData)
        ttsEvent: TtsEvent | None = None

        if timeoutData.user.isTtsEnabled:
            message: str

            if isReverse:
                message = f'Oh noo! @{timeoutData.instigatorUserName} got hit with a reverse! Rip bozo!'
            else:
                message = f'{timeoutData.instigatorUserName} timed out {timeoutTargetUserName} for {timeoutData.durationSecondsStr} seconds! Rip bozo!'

            providerOverridableStatus: TtsProviderOverridableStatus

            if timeoutData.user.isChatterPreferredTtsEnabled:
                providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
            else:
                providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

            ttsEvent = TtsEvent(
                message = message,
                twitchChannel = timeoutData.twitchChannel,
                twitchChannelId = timeoutData.twitchChannelId,
                userId = timeoutData.instigatorUserId,
                userName = timeoutData.instigatorUserName,
                donation = None,
                provider = timeoutData.user.defaultTtsProvider,
                providerOverridableStatus = providerOverridableStatus,
                raidInfo = None
            )

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = soundAlert,
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
        timeoutTargetUserName: str,
        timeoutData: TimeoutActionData,
        twitchChannel: TwitchChannel
    ):
        if timeoutData.actionType is TimeoutActionType.AIR_STRIKE:
            # Air Strike actions don't send Twitch chats within this class
            return

        message: str

        if isGuaranteed or not timeoutData.isRandomChanceEnabled or timeoutData.actionType is TimeoutActionType.GRENADE:
            message = f'{ripBozoEmote} @{timeoutTargetUserName} {ripBozoEmote}'
        elif isReverse:
            message = f'{ripBozoEmote} Oh noo! @{timeoutData.instigatorUserName} rolled a d{diceRoll.dieSize} and got a {diceRoll.roll} reverse! (needed greater than {rollFailureData.reverseRoll}) {ripBozoEmote}'
        else:
            message = f'{ripBozoEmote} Timed out @{timeoutTargetUserName} after rolling a d{diceRoll.dieSize} and got a {diceRoll.roll} (needed greater than {rollFailureData.failureRoll}) {ripBozoEmote}'

        if timeoutData.remainingGrenades is not None:
            availableGrenadesString = locale.format_string("%d", timeoutData.remainingGrenades, grouping = True)

            grenadesPluralization: str
            if timeoutData.remainingGrenades == 1:
                grenadesPluralization = 'grenade'
            else:
                grenadesPluralization = 'grenades'

            message = f'{message} ({availableGrenadesString} {grenadesPluralization} remaining for @{timeoutData.instigatorUserName})'

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = timeoutData.twitchChatMessageId
        )

    async def __chooseGrenadeSoundAlert(
        self,
        timeoutData: TimeoutActionData
    ) -> SoundAlert | None:
        if not timeoutData.user.areSoundAlertsEnabled:
            return None

        massiveTimeoutSoundAlertsEnabled = await self.__timeoutActionSettingsRepository.areMassiveTimeoutSoundAlertsEnabled()
        massiveTimeoutHoursTransitionPoint = await self.__timeoutActionSettingsRepository.getMassiveTimeoutHoursTransitionPoint()
        useMassiveTimeoutSoundAlerts = False

        if massiveTimeoutSoundAlertsEnabled and utils.isValidInt(massiveTimeoutHoursTransitionPoint):
            timeoutDurationHours = float(timeoutData.durationSeconds) / float(60) / float(60)
            useMassiveTimeoutSoundAlerts = timeoutDurationHours >= massiveTimeoutHoursTransitionPoint

        soundAlerts: FrozenList[SoundAlert] = FrozenList()

        if useMassiveTimeoutSoundAlerts:
            soundAlerts.append(SoundAlert.MEGA_GRENADE_1)
            soundAlerts.append(SoundAlert.MEGA_GRENADE_2)
        else:
            soundAlerts.append(SoundAlert.GRENADE_1)
            soundAlerts.append(SoundAlert.GRENADE_2)
            soundAlerts.append(SoundAlert.GRENADE_3)

        soundAlerts.freeze()
        return random.choice(soundAlerts)

    async def __discoverBullyOccurrenceCount(
        self,
        now: datetime,
        timeoutTargetUserId: str,
        timeoutData: TimeoutActionData
    ) -> int:
        if not timeoutData.isTimeoutCheerActionIncreasedBullyFailureEnabled:
            return 0

        history = await self.__timeoutActionHistoryRepository.get(
            chatterUserId = timeoutTargetUserId,
            twitchChannel = timeoutData.twitchChannel,
            twitchChannelId = timeoutData.twitchChannelId
        )

        if history.entries is None or len(history.entries) == 0:
            return 0

        bullyTimeToLiveDays = await self.__timeoutActionSettingsRepository.getBullyTimeToLiveDays()
        bullyTimeBuffer = timedelta(days = bullyTimeToLiveDays)

        bullyOccurrences = 0

        for historyEntry in history.entries:
            if historyEntry.timedOutByUserId != timeoutData.instigatorUserId:
                continue
            elif historyEntry.timedOutAtDateTime + bullyTimeBuffer < now:
                continue

            bullyOccurrences += 1

        return bullyOccurrences

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

        bullyOccurrences = await self.__discoverBullyOccurrenceCount(
            now = now,
            timeoutTargetUserId = timeoutTargetUserId,
            timeoutData = timeoutData
        )

        failureProbability = baseFailureProbability + (perBullyFailureProbabilityIncrease * float(bullyOccurrences))
        failureProbability = float(min(failureProbability, maxBullyFailureProbability))
        failureRoll = int(round(failureProbability * float(diceRoll.dieSize)))
        failureRoll = int(min(failureRoll, diceRoll.dieSize))

        reverseProbability = await self.__timeoutActionSettingsRepository.getReverseProbability()
        reverseRoll = int(round(reverseProbability * float(diceRoll.dieSize)))
        reverseRoll = int(min(reverseRoll, diceRoll.dieSize))

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

    async def __buildTimeoutReasonString(
        self,
        timeoutData: TimeoutActionData
    ) -> str:
        baseTimeoutReason = f'Timeout from {timeoutData.instigatorUserName} — {timeoutData.durationSeconds} second(s)'

        if timeoutData.remainingGrenades is None:
            return baseTimeoutReason

        availableGrenadesString = locale.format_string("%d", timeoutData.remainingGrenades, grouping = True)

        grenadesPluralization: str
        if timeoutData.remainingGrenades == 1:
            grenadesPluralization = 'grenade'
        else:
            grenadesPluralization = 'grenades'

        return f'{baseTimeoutReason} — you have {availableGrenadesString} {grenadesPluralization} available'

    async def __isFailedDiceRoll(
        self,
        isGuaranteed: bool,
        diceRoll: DiceRoll,
        rollFailureData: RollFailureData,
        ripBozoEmote: str,
        timeoutTargetUserName: str,
        timeoutData: TimeoutActionData,
        twitchChannel: TwitchChannel
    ) -> bool:
        if isGuaranteed:
            return False
        elif not timeoutData.user.isTimeoutCheerActionFailureEnabled:
            return False
        elif not timeoutData.isRandomChanceEnabled:
            return False
        elif diceRoll.roll > rollFailureData.failureRoll:
            return False

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'{ripBozoEmote} Sorry @{timeoutData.instigatorUserName}, your timeout of @{timeoutTargetUserName} failed {ripBozoEmote} (rolled a d{diceRoll.dieSize} and got a {diceRoll.roll}, but needed greater than {rollFailureData.failureRoll}) {ripBozoEmote}',
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
            message = f'⚠ Sorry @{timeoutData.instigatorUserName}, @{timeoutTargetUserName} is an immune user',
            replyMessageId = timeoutData.twitchChatMessageId
        )

        return True

    async def __isReverseTimeout(
        self,
        isGuaranteed: bool,
        diceRoll: DiceRoll,
        rollFailureData: RollFailureData,
        timeoutData: TimeoutActionData
    ) -> bool:
        if isGuaranteed:
            return False
        elif not timeoutData.user.isTimeoutCheerActionReverseEnabled:
            return False
        elif not timeoutData.isRandomChanceEnabled:
            return False

        return diceRoll.roll < rollFailureData.reverseRoll

    async def __isTryingToTimeoutSelf(
        self,
        timeoutTargetUserId: str,
        timeoutData: TimeoutActionData
    ) -> bool:
        return timeoutTargetUserId == timeoutData.instigatorUserId

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
        if not timeoutData.isRandomChanceEnabled:
            return False

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

    async def __processTimeout(self, timeoutData: TimeoutActionData):
        if not isinstance(timeoutData, TimeoutActionData):
            raise TypeError(f'timeoutData argument is malformed: \"{timeoutData}\"')

        twitchChannelProvider = self.__twitchChannelProvider
        if twitchChannelProvider is None:
            self.__timber.log('TimeoutActionHelper', f'No TwitchChannelProvider instance has been set: \"{twitchChannelProvider}\"')
            return

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
            return

        elif await self.__isImmuneUser(
            timeoutTargetUserId = timeoutTargetUserId,
            timeoutTargetUserName = timeoutTargetUserName,
            timeoutData = timeoutData,
            twitchChannel = twitchChannel
        ):
            self.__timber.log('TimeoutActionHelper', f'Attempted to timeout {timeoutTargetUserName}:{timeoutTargetUserId} by {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} in {timeoutData.twitchChannel}, but user ID \"{timeoutTargetUserId}\" is immune ({timeoutData=})')
            return

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
            isGuaranteed = True
            isReverse = True
            timeoutTargetUserId = timeoutData.instigatorUserId
            timeoutTargetUserName = timeoutData.instigatorUserName

        elif await self.__isTryingToTimeoutSelf(
            timeoutTargetUserId = timeoutTargetUserId,
            timeoutData = timeoutData
        ):
            self.__timber.log('TimeoutActionHelper', f'Attempting to timeout self by {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} in {timeoutData.twitchChannel} ({timeoutData=})')
            isGuaranteed = True

        elif await self.__hasNewFollowerShield(
            now = now,
            ripBozoEmote = ripBozoEmote,
            timeoutTargetUserId = timeoutTargetUserId,
            timeoutTargetUserName = timeoutTargetUserName,
            timeoutData = timeoutData,
            twitchChannel = twitchChannel
        ):
            self.__timber.log('TimeoutActionHelper', f'Attempted to timeout {timeoutTargetUserName}:{timeoutTargetUserId} by {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} in {timeoutData.twitchChannel}, but this user is a new follower ({timeoutData=})')
            return

        elif await self.__isReverseTimeout(
            isGuaranteed = isGuaranteed,
            diceRoll = diceRoll,
            rollFailureData = rollFailureData,
            timeoutData = timeoutData
        ):
            self.__timber.log('TimeoutActionHelper', f'Attempted to timeout {timeoutTargetUserName}:{timeoutTargetUserId} by {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} in {timeoutData.twitchChannel}, but they hit the reverse roll ({diceRoll=}) ({rollFailureData=}) ({timeoutData=})')
            isReverse = True
            timeoutTargetUserId = timeoutData.instigatorUserId
            timeoutTargetUserName = timeoutData.instigatorUserName

        elif await self.__isFailedDiceRoll(
            isGuaranteed = isGuaranteed,
            diceRoll = diceRoll,
            rollFailureData = rollFailureData,
            ripBozoEmote = ripBozoEmote,
            timeoutTargetUserName = timeoutTargetUserName,
            timeoutData = timeoutData,
            twitchChannel = twitchChannel
        ):
            self.__timber.log('TimeoutActionHelper', f'Attempted to timeout {timeoutTargetUserName}:{timeoutTargetUserId} by {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} in {timeoutData.twitchChannel}, but they hit the failure roll ({diceRoll=}) ({rollFailureData=}) ({timeoutData=})')
            return

        timeoutReasonString = await self.__buildTimeoutReasonString(
            timeoutData = timeoutData
        )

        timeoutResult = await self.__twitchTimeoutHelper.timeout(
            durationSeconds = timeoutData.durationSeconds,
            reason = timeoutReasonString,
            twitchAccessToken = timeoutData.moderatorTwitchAccessToken,
            twitchChannelAccessToken = timeoutData.userTwitchAccessToken,
            twitchChannelId = timeoutData.twitchChannelId,
            userIdToTimeout = timeoutTargetUserId,
            user = timeoutData.user
        )

        if timeoutResult is not TwitchTimeoutResult.SUCCESS:
            self.__timber.log('TimeoutActionHelper', f'Attempted to timeout {timeoutTargetUserName}:{timeoutTargetUserId} by {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} in {timeoutData.twitchChannel}, but an error occurred ({timeoutResult=}) ({diceRoll=}) ({rollFailureData=}) ({timeoutData=})')
            return

        self.__timber.log('TimeoutActionHelper', f'Timed out {timeoutTargetUserName}:{timeoutTargetUserId} in \"{timeoutData.twitchChannel}\" from {timeoutData.instigatorUserName}:{timeoutData.instigatorUserId} ({diceRoll=}) ({rollFailureData=}) ({timeoutResult=}) ({timeoutData=})')

        await self.__activeChattersRepository.remove(
            chatterUserId = timeoutTargetUserId,
            twitchChannelId = timeoutData.twitchChannelId
        )

        await self.__asplodieStatsRepository.addAsplodie(
            isSelfAsplodie = timeoutTargetUserId == timeoutData.instigatorUserId,
            durationAsplodiedSeconds = timeoutData.durationSeconds,
            chatterUserId = timeoutTargetUserId,
            twitchChannelId = timeoutData.twitchChannelId
        )

        await self.__timeoutActionHistoryRepository.add(
            durationSeconds = timeoutData.durationSeconds,
            chatterUserId = timeoutTargetUserId,
            timedOutByUserId = timeoutData.instigatorUserId,
            twitchChannel = timeoutData.twitchChannel,
            twitchChannelId = timeoutData.twitchChannelId
        )

        await self.__alertViaSoundAndTextToSpeech(
            isReverse = isReverse,
            timeoutTargetUserName = timeoutTargetUserName,
            timeoutData = timeoutData
        )

        await self.__alertViaTwitchChat(
            isGuaranteed = isGuaranteed,
            isReverse = isReverse,
            diceRoll = diceRoll,
            rollFailureData = rollFailureData,
            ripBozoEmote = ripBozoEmote,
            timeoutTargetUserName = timeoutTargetUserName,
            timeoutData = timeoutData,
            twitchChannel = twitchChannel
        )

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

    def start(self):
        if self.__isStarted:
            self.__timber.log('TimeoutActionHelper', 'Not starting TimeoutActionHelper as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TimeoutActionHelper', 'Starting TimeoutActionHelper...')
        self.__backgroundTaskHelper.createTask(self.__startActionLoop())

    async def __startActionLoop(self):
        while True:
            timeoutData: TimeoutActionData | None = None

            try:
                if not self.__actionQueue.empty():
                    timeoutData = self.__actionQueue.get_nowait()
            except queue.Empty as e:
                self.__timber.log('TimeoutActionHelper', f'Encountered queue.Empty when grabbing action (queue size: {self.__actionQueue.qsize()}) ({timeoutData=}): {e}', e, traceback.format_exc())

            if timeoutData is None:
                actionLoopCooldownSeconds = await self.__timeoutActionSettingsRepository.getActionLoopCooldownSeconds()
                await asyncio.sleep(actionLoopCooldownSeconds)
            else:
                await self.__processTimeout(timeoutData)

    def submitTimeout(self, timeoutData: TimeoutActionData):
        if not isinstance(timeoutData, TimeoutActionData):
            raise TypeError(f'timeoutData argument is malformed: \"{timeoutData}\"')

        try:
            self.__actionQueue.put(timeoutData, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TimeoutActionHelper', f'Encountered queue.Full when submitting a new action ({timeoutData}) into the action queue (queue size: {self.__actionQueue.qsize()}): {e}', e, traceback.format_exc())

    async def __verifyStreamStatus(
        self,
        timeoutData: TimeoutActionData
    ) -> bool:
        requirement = timeoutData.streamStatusRequirement
        if requirement is TimeoutStreamStatusRequirement.ANY:
            return True

        isLive = await self.__isLiveOnTwitchRepository.isLive(
            twitchChannelId = timeoutData.twitchChannelId
        )

        return isLive and requirement is TimeoutStreamStatusRequirement.ONLINE or \
            not isLive and requirement is TimeoutStreamStatusRequirement.OFFLINE
