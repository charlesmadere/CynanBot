from typing import Final

from frozendict import frozendict

from .timeoutCheerAction import TimeoutCheerAction
from .timeoutCheerActionHelperInterface import TimeoutCheerActionHelperInterface
from .timeoutCheerActionTargetType import TimeoutCheerActionTargetType
from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ...misc import utils as utils
from ...timeout.idGenerator.timeoutIdGeneratorInterface import TimeoutIdGeneratorInterface
from ...timeout.machine.timeoutActionMachineInterface import TimeoutActionMachineInterface
from ...timeout.models.absTimeoutDuration import AbsTimeoutDuration
from ...timeout.models.actions.absTimeoutAction import AbsTimeoutAction
from ...timeout.models.actions.bananaTimeoutAction import BananaTimeoutAction
from ...timeout.models.actions.grenadeTimeoutAction import GrenadeTimeoutAction
from ...timeout.models.exactTimeoutDuration import ExactTimeoutDuration
from ...timeout.models.timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ...users.userInterface import UserInterface


class TimeoutCheerActionHelper(TimeoutCheerActionHelperInterface):

    def __init__(
        self,
        timeoutActionMachine: TimeoutActionMachineInterface,
        timeoutIdGenerator: TimeoutIdGeneratorInterface,
    ):
        if not isinstance(timeoutActionMachine, TimeoutActionMachineInterface):
            raise TypeError(f'timeoutActionMachine argument is malformed: \"{timeoutActionMachine}\"')
        elif not isinstance(timeoutIdGenerator, TimeoutIdGeneratorInterface):
            raise TypeError(f'timeoutIdGenerator argument is malformed: \"{timeoutIdGenerator}\"')

        self.__timeoutActionMachine: Final[TimeoutActionMachineInterface] = timeoutActionMachine
        self.__timeoutIdGenerator: Final[TimeoutIdGeneratorInterface] = timeoutIdGenerator

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

        timeoutDuration: AbsTimeoutDuration = ExactTimeoutDuration(
            seconds = action.durationSeconds,
        )

        actionId = await self.__timeoutIdGenerator.generateActionId()

        streamStatusRequirement = await self.__mapStreamStatusRequirement(action.streamStatusRequirement)

        timeoutAction: AbsTimeoutAction

        if action.targetType is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY:
            timeoutAction = BananaTimeoutAction(
                timeoutDuration = timeoutDuration,
                ignoreInventory = True,
                isRandomChanceEnabled = True,
                actionId = actionId,
                chatMessage = message,
                instigatorUserId = cheerUserId,
                moderatorTwitchAccessToken = moderatorTwitchAccessToken,
                moderatorUserId = moderatorUserId,
                twitchChannelId = twitchChannelId,
                twitchChatMessageId = twitchChatMessageId,
                userTwitchAccessToken = userTwitchAccessToken,
                streamStatusRequirement = streamStatusRequirement,
                user = user,
            )
        else:
            timeoutAction = GrenadeTimeoutAction(
                timeoutDuration = timeoutDuration,
                ignoreInventory = True,
                actionId = actionId,
                instigatorUserId = cheerUserId,
                moderatorTwitchAccessToken = moderatorTwitchAccessToken,
                moderatorUserId = moderatorUserId,
                twitchChannelId = twitchChannelId,
                twitchChatMessageId = twitchChatMessageId,
                userTwitchAccessToken = userTwitchAccessToken,
                streamStatusRequirement = streamStatusRequirement,
                user = user,
            )

        self.__timeoutActionMachine.submitAction(timeoutAction)
        return True

    async def __mapStreamStatusRequirement(
        self,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
    ) -> TimeoutStreamStatusRequirement:
        match streamStatusRequirement:
            case CheerActionStreamStatusRequirement.ANY:
                return TimeoutStreamStatusRequirement.ANY

            case CheerActionStreamStatusRequirement.ONLINE:
                return TimeoutStreamStatusRequirement.ONLINE

            case CheerActionStreamStatusRequirement.OFFLINE:
                return TimeoutStreamStatusRequirement.OFFLINE

            case _:
                raise ValueError(f'Encountered unknown CheerActionStreamStatusRequirement value: \"{streamStatusRequirement}\"')
