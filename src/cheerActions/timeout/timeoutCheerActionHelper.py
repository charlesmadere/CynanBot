from dataclasses import dataclass
from typing import Collection

from .timeoutCheerActionHelperInterface import TimeoutCheerActionHelperInterface
from .timeoutCheerActionMapper import TimeoutCheerActionMapper
from ..absCheerAction import AbsCheerAction
from ..timeoutCheerAction import TimeoutCheerAction
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...timeout.timeoutActionData import TimeoutActionData
from ...timeout.timeoutActionHelperInterface import TimeoutActionHelperInterface
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
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
        timber: TimberInterface,
        timeoutActionHelper: TimeoutActionHelperInterface,
        timeoutCheerActionMapper: TimeoutCheerActionMapper,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionHelper, TimeoutActionHelperInterface):
            raise TypeError(f'timeoutActionHelper argument is malformed: \"{timeoutActionHelper}\"')
        elif not isinstance(timeoutCheerActionMapper, TimeoutCheerActionMapper):
            raise TypeError(f'timeoutCheerActionMapper argument is malformed: \"{timeoutCheerActionMapper}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__timber: TimberInterface = timber
        self.__timeoutActionHelper: TimeoutActionHelperInterface = timeoutActionHelper
        self.__timeoutCheerActionMapper: TimeoutCheerActionMapper = timeoutCheerActionMapper
        self.__twitchMessageStringUtils: TwitchMessageStringUtilsInterface = twitchMessageStringUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

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

        if not user.areCheerActionsEnabled or not user.areTimeoutActionsEnabled:
            return False

        timeoutAction: TimeoutCheerAction | None = None

        for action in actions:
            if isinstance(action, TimeoutCheerAction) and action.isEnabled and action.bits == bits:
                timeoutAction = action
                break

        if timeoutAction is None:
            return False

        timeoutTargetUserName = await self.__twitchMessageStringUtils.getUserNameFromCheerMessage(message)
        if not utils.isValidStr(timeoutTargetUserName):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout from {cheerUserName}:{cheerUserId} in {user.getHandle()}, but was unable to find a user name: ({message=}) ({timeoutAction=})')
            return False

        timeoutTargetUserId = await self.__userIdsRepository.fetchUserId(
            userName = timeoutTargetUserName,
            twitchAccessToken = userTwitchAccessToken
        )

        if not utils.isValidStr(timeoutTargetUserId):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout \"{timeoutTargetUserName}\" from {cheerUserName}:{cheerUserId} in {user.getHandle()}, but was unable to find a user ID: ({message=}) ({timeoutAction=})')
            return False

        streamStatusRequirement = await self.__timeoutCheerActionMapper.toTimeoutActionDataStreamStatusRequirement(
            streamStatusRequirement = timeoutAction.streamStatusRequirement
        )

        return await self.__timeoutActionHelper.timeout(TimeoutActionData(
            bits = bits,
            durationSeconds = action.durationSeconds,
            chatMessage = message,
            instigatorUserId = cheerUserId,
            instigatorUserName = cheerUserName,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            pointRedemptionEventId = None,
            pointRedemptionMessage = None,
            pointRedemptionRewardId = None,
            timeoutTargetUserId = timeoutTargetUserId,
            timeoutTargetUserName = timeoutTargetUserName,
            twitchChannelId = broadcasterUserId,
            twitchChatMessageId = twitchChatMessageId,
            userTwitchAccessToken = userTwitchAccessToken,
            streamStatusRequirement = streamStatusRequirement,
            user = user
        ))
