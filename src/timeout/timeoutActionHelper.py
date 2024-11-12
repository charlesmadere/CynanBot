from dataclasses import dataclass
from datetime import datetime, timedelta

from .guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from .timeoutActionData import TimeoutActionData
from .timeoutActionHelperInterface import TimeoutActionHelperInterface
from .timeoutActionHistoryRepositoryInterface import TimeoutActionHistoryRepositoryInterface
from .timeoutActionSettingsRepositoryInterface import TimeoutActionSettingsRepositoryInterface
from ..misc import utils as utils
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ..tts.ttsEvent import TtsEvent
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ..twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ..twitch.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from ..twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ..twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from ..twitch.twitchConstantsInterface import TwitchConstantsInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userInterface import UserInterface


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
        timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface,
        timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        trollmojiHelper: TrollmojiHelperInterface,
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
        elif not isinstance(timeoutActionHistoryRepository, TimeoutActionHistoryRepositoryInterface):
            raise TypeError(f'timeoutActionHistoryRepository argument is malformed: \"{timeoutActionHistoryRepository}\"')
        elif not isinstance(timeoutActionSettingsRepository, TimeoutActionSettingsRepositoryInterface):
            raise TypeError(f'timeoutActionSettingsRepository argument is malformed: \"{timeoutActionSettingsRepository}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
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
        self.__timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface = timeoutActionHistoryRepository
        self.__timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface = timeoutActionSettingsRepository
        self.__timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface = timeoutImmuneUserIdsRepository
        self.__trollmojiHelper: TrollmojiHelperInterface = trollmojiHelper
        self.__twitchConstants: TwitchConstantsInterface = twitchConstants
        self.__twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface = twitchFollowingStatusRepository
        self.__twitchTimeoutHelper: TwitchTimeoutHelperInterface = twitchTimeoutHelper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __alertViaTextToSpeech(
        self,
        isReverse: bool,
        cheerUserId: str,
        cheerUserName: str,
        twitchChannelId: str,
        userNameToTimeout: str,
        timeoutData: TimeoutActionData,
        user: UserInterface
    ):
        if not user.isTtsEnabled():
            return

        message: str
        if isReverse:
            message = f'Oh noo! {userNameToTimeout} got hit with a reverse! Rip bozo!'
        else:
            message = f'{cheerUserName} timed out {userNameToTimeout} for {timeoutData.durationSecondsStr} seconds! Rip bozo!'

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

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    async def timeout(self, timeoutData: TimeoutActionData) -> bool:
        if not isinstance(timeoutData, TimeoutActionData):
            raise TypeError(f'timeoutData argument is malformed: \"{timeoutData}\"')

        return False

    async def __verifyStreamStatus(
        self,
        twitchChannelId: str,
        timeoutData: TimeoutActionData,
        user: UserInterface
    ) -> bool:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(timeoutData, TimeoutActionData):
            raise TypeError(f'timeoutData argument is malformed: \"{timeoutData}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        requirement = timeoutData.streamStatusRequirement
        if requirement is TimeoutActionData.StreamStatusRequirement.ANY:
            return True

        isLive = await self.__isLiveOnTwitchRepository.isLive(twitchChannelId)
        return isLive and requirement is TimeoutActionData.StreamStatusRequirement.ONLINE or \
            not isLive and requirement is TimeoutActionData.StreamStatusRequirement.OFFLINE
