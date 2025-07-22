import random
from dataclasses import dataclass

from frozendict import frozendict

from .timeoutCheerAction import TimeoutCheerAction
from .timeoutCheerActionHelperInterface import TimeoutCheerActionHelperInterface
from .timeoutCheerActionMapper import TimeoutCheerActionMapper
from .timeoutCheerActionTargetType import TimeoutCheerActionTargetType
from ..absCheerAction import AbsCheerAction
from ...misc import utils as utils
from ...recentGrenadeAttacks.helper.recentGrenadeAttacksHelperInterface import RecentGrenadeAttacksHelperInterface
from ...timber.timberInterface import TimberInterface
from ...timeout.timeoutActionData import TimeoutActionData
from ...timeout.timeoutActionHelperInterface import TimeoutActionHelperInterface
from ...timeout.timeoutActionSettingsRepositoryInterface import TimeoutActionSettingsRepositoryInterface
from ...timeout.timeoutActionType import TimeoutActionType
from ...twitch.activeChatters.activeChatter import ActiveChatter
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TimeoutCheerActionHelper(TimeoutCheerActionHelperInterface):

    @dataclass(frozen = True)
    class TimeoutTarget:
        isRandomChanceEnabled: bool
        isRandomTarget: bool
        userId: str
        userName: str

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        recentGrenadeAttacksHelper: RecentGrenadeAttacksHelperInterface,
        timber: TimberInterface,
        timeoutActionHelper: TimeoutActionHelperInterface,
        timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface,
        timeoutCheerActionMapper: TimeoutCheerActionMapper,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(recentGrenadeAttacksHelper, RecentGrenadeAttacksHelperInterface):
            raise TypeError(f'recentGrenadeAttacksHelper argument is malformed: \"{recentGrenadeAttacksHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionHelper, TimeoutActionHelperInterface):
            raise TypeError(f'timeoutActionHelper argument is malformed: \"{timeoutActionHelper}\"')
        elif not isinstance(timeoutActionSettingsRepository, TimeoutActionSettingsRepositoryInterface):
            raise TypeError(f'timeoutActionSettingsRepository argument is malformed: \"{timeoutActionSettingsRepository}\"')
        elif not isinstance(timeoutCheerActionMapper, TimeoutCheerActionMapper):
            raise TypeError(f'timeoutCheerActionMapper argument is malformed: \"{timeoutCheerActionMapper}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__activeChattersRepository: ActiveChattersRepositoryInterface = activeChattersRepository
        self.__recentGrenadeAttacksHelper: RecentGrenadeAttacksHelperInterface = recentGrenadeAttacksHelper
        self.__timber: TimberInterface = timber
        self.__timeoutActionHelper: TimeoutActionHelperInterface = timeoutActionHelper
        self.__timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface = timeoutActionSettingsRepository
        self.__timeoutCheerActionMapper: TimeoutCheerActionMapper = timeoutCheerActionMapper
        self.__timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface = timeoutImmuneUserIdsRepository
        self.__twitchMessageStringUtils: TwitchMessageStringUtilsInterface = twitchMessageStringUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    async def __determineRandomTimeoutTarget(
        self,
        cheerUserId: str,
        cheerUserName: str,
        twitchChannelId: str,
        timeoutAction: TimeoutCheerAction,
        user: UserInterface,
    ) -> TimeoutTarget | None:
        additionalReverseProbability = await self.__timeoutActionSettingsRepository.getGrenadeAdditionalReverseProbability()
        randomReverseNumber = random.random()

        if randomReverseNumber <= additionalReverseProbability:
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout random target from {cheerUserName}:{cheerUserId} in {user.handle}, but they got the additional reverse probability RNG ({timeoutAction=}) ({additionalReverseProbability=}) ({randomReverseNumber=})')

            return TimeoutCheerActionHelper.TimeoutTarget(
                isRandomChanceEnabled = False,
                isRandomTarget = True,
                userId = cheerUserId,
                userName = cheerUserName,
            )

        activeChatters = await self.__activeChattersRepository.get(
            twitchChannelId = twitchChannelId,
        )

        vulnerableChatters: dict[str, ActiveChatter] = dict(activeChatters)
        vulnerableChatters.pop(twitchChannelId, None)

        allImmuneUserIds = await self.__timeoutImmuneUserIdsRepository.getAllUserIds()

        for immuneUserId in allImmuneUserIds:
            vulnerableChatters.pop(immuneUserId, None)

        if len(vulnerableChatters) == 0:
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout random target from {cheerUserName}:{cheerUserId} in {user.handle}, but no active chatter was found ({timeoutAction=}) ({additionalReverseProbability=}) ({randomReverseNumber=}) ({activeChatters=}) ({vulnerableChatters=})')
            return None

        randomChatter = random.choice(list(vulnerableChatters.values()))

        await self.__activeChattersRepository.remove(
            chatterUserId = randomChatter.chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        return TimeoutCheerActionHelper.TimeoutTarget(
            isRandomChanceEnabled = False,
            isRandomTarget = True,
            userId = randomChatter.chatterUserId,
            userName = randomChatter.chatterUserName,
        )

    async def __determineAnyTimeoutTarget(
        self,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        twitchChannelId: str,
        userTwitchAccessToken: str,
        timeoutAction: TimeoutCheerAction,
        user: UserInterface,
    ) -> TimeoutTarget | None:
        specificUserTimeoutTarget = await self.__determineUserTimeoutTarget(
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            message = message,
            userTwitchAccessToken = userTwitchAccessToken,
            timeoutAction = timeoutAction,
            user = user,
        )

        if specificUserTimeoutTarget is not None:
            return specificUserTimeoutTarget

        return await self.__determineRandomTimeoutTarget(
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            twitchChannelId = twitchChannelId,
            timeoutAction = timeoutAction,
            user = user,
        )

    async def __determineTimeoutTarget(
        self,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        twitchChannelId: str,
        userTwitchAccessToken: str,
        timeoutAction: TimeoutCheerAction,
        user: UserInterface,
    ) -> TimeoutTarget | None:
        match timeoutAction.targetType:
            case TimeoutCheerActionTargetType.ANY:
                return await self.__determineAnyTimeoutTarget(
                    cheerUserId = cheerUserId,
                    cheerUserName = cheerUserName,
                    message = message,
                    twitchChannelId = twitchChannelId,
                    userTwitchAccessToken = userTwitchAccessToken,
                    timeoutAction = timeoutAction,
                    user = user,
                )

            case TimeoutCheerActionTargetType.RANDOM_ONLY:
                return await self.__determineRandomTimeoutTarget(
                    cheerUserId = cheerUserId,
                    cheerUserName = cheerUserName,
                    twitchChannelId = twitchChannelId,
                    timeoutAction = timeoutAction,
                    user = user,
                )

            case TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY:
                return await self.__determineUserTimeoutTarget(
                    cheerUserId = cheerUserId,
                    cheerUserName = cheerUserName,
                    message = message,
                    userTwitchAccessToken = userTwitchAccessToken,
                    timeoutAction = timeoutAction,
                    user = user,
                )

            case _:
                raise ValueError(f'Encountered unknown TimeoutCheerActionTargetType: {timeoutAction}')

    async def __determineUserTimeoutTarget(
        self,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        userTwitchAccessToken: str,
        timeoutAction: TimeoutCheerAction,
        user: UserInterface,
    ) -> TimeoutTarget | None:
        timeoutTargetUserName = await self.__twitchMessageStringUtils.getUserNameFromCheerMessage(message)
        if not utils.isValidStr(timeoutTargetUserName):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout from {cheerUserName}:{cheerUserId} in {user.handle}, but was unable to find a user name ({message=}) ({timeoutAction=})')
            return None

        timeoutTargetUserId = await self.__userIdsRepository.fetchUserId(
            userName = timeoutTargetUserName,
            twitchAccessToken = userTwitchAccessToken,
        )

        if not utils.isValidStr(timeoutTargetUserId):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout \"{timeoutTargetUserName}\" from {cheerUserName}:{cheerUserId} in {user.handle}, but was unable to find a user ID ({message=}) ({timeoutAction=})')
            return None

        return TimeoutCheerActionHelper.TimeoutTarget(
            isRandomChanceEnabled = timeoutAction.isRandomChanceEnabled,
            isRandomTarget = False,
            userId = timeoutTargetUserId,
            userName = timeoutTargetUserName,
        )

    async def handleTimeoutCheerAction(
        self,
        actions: frozendict[int, AbsCheerAction],
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        userTwitchAccessToken: str,
        user: UserInterface,
    ) -> bool:
        if not isinstance(actions, frozendict):
            raise TypeError(f'actions argument is malformed: \"{actions}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
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
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        action = actions.get(bits, None)

        if not isinstance(action, TimeoutCheerAction) or not action.isEnabled:
            return False
        elif not await self.__recentGrenadeAttacksHelper.canThrowGrenade(
            attackerUserId = cheerUserId,
            twitchChannel = user.handle,
            twitchChannelId = twitchChannelId,
        ):
            self.__timber.log('TimeoutCheerActionHelper', f'No grenades available for this user ({cheerUserId=}) ({cheerUserName=}) ({user=}) ({action=})')
            return False

        timeoutTarget = await self.__determineTimeoutTarget(
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            message = message,
            twitchChannelId = twitchChannelId,
            userTwitchAccessToken = userTwitchAccessToken,
            timeoutAction = action,
            user = user,
        )

        if timeoutTarget is None:
            return False

        remainingGrenades = await self.__recentGrenadeAttacksHelper.throwGrenade(
            attackedUserId = timeoutTarget.userId,
            attackerUserId = cheerUserId,
            twitchChannel = user.handle,
            twitchChannelId = twitchChannelId,
        )

        actionType: TimeoutActionType

        if timeoutTarget.isRandomTarget:
            actionType = TimeoutActionType.GRENADE
        else:
            actionType = TimeoutActionType.TARGETED

        streamStatusRequirement = await self.__timeoutCheerActionMapper.toTimeoutActionDataStreamStatusRequirement(
            streamStatusRequirement = action.streamStatusRequirement,
        )

        self.__timeoutActionHelper.submitTimeout(TimeoutActionData(
            isRandomChanceEnabled = timeoutTarget.isRandomChanceEnabled,
            bits = bits,
            durationSeconds = action.durationSeconds,
            remainingGrenades = remainingGrenades,
            chatMessage = message,
            instigatorUserId = cheerUserId,
            instigatorUserName = cheerUserName,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            pointRedemptionEventId = None,
            pointRedemptionMessage = None,
            pointRedemptionRewardId = None,
            timeoutTargetUserId = timeoutTarget.userId,
            timeoutTargetUserName = timeoutTarget.userName,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
            userTwitchAccessToken = userTwitchAccessToken,
            actionType = actionType,
            streamStatusRequirement = streamStatusRequirement,
            user = user,
        ))

        return True
