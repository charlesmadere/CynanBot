from typing import Final

from frozendict import frozendict

from .airStrikeCheerAction import AirStrikeCheerAction
from .airStrikeCheerActionHelperInterface import AirStrikeCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ..timeout.timeoutCheerActionMapper import TimeoutCheerActionMapper
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...timeout.idGenerator.timeoutIdGeneratorInterface import TimeoutIdGeneratorInterface
from ...timeout.machine.timeoutActionMachineInterface import TimeoutActionMachineInterface
from ...timeout.models.absTimeoutDuration import AbsTimeoutDuration
from ...timeout.models.actions.airStrikeTimeoutAction import AirStrikeTimeoutAction
from ...timeout.models.randomLinearTimeoutDuration import RandomLinearTimeoutDuration
from ...timeout.models.timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ...timeout.settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ...users.userInterface import UserInterface


class AirStrikeCheerActionHelper(AirStrikeCheerActionHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeoutActionMachine: TimeoutActionMachineInterface,
        timeoutActionSettings: TimeoutActionSettingsInterface,
        timeoutCheerActionMapper: TimeoutCheerActionMapper,
        timeoutIdGenerator: TimeoutIdGeneratorInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionMachine, TimeoutActionMachineInterface):
            raise TypeError(f'timeoutActionMachine argument is malformed: \"{timeoutActionMachine}\"')
        elif not isinstance(timeoutActionSettings, TimeoutActionSettingsInterface):
            raise TypeError(f'timeoutActionSettings argument is malformed: \"{timeoutActionSettings}\"')
        elif not isinstance(timeoutCheerActionMapper, TimeoutCheerActionMapper):
            raise TypeError(f'timeoutCheerActionMapper argument is malformed: \"{timeoutCheerActionMapper}\"')
        elif not isinstance(timeoutIdGenerator, TimeoutIdGeneratorInterface):
            raise TypeError(f'timeoutIdGenerator argument is malformed: \"{timeoutIdGenerator}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionMachine: Final[TimeoutActionMachineInterface] = timeoutActionMachine
        self.__timeoutActionSettings: Final[TimeoutActionSettingsInterface] = timeoutActionSettings
        self.__timeoutCheerActionMapper: Final[TimeoutCheerActionMapper] = timeoutCheerActionMapper
        self.__timeoutIdGenerator: Final[TimeoutIdGeneratorInterface] = timeoutIdGenerator

    async def handleAirStrikeCheerAction(
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

        if not isinstance(action, AirStrikeCheerAction) or not action.isEnabled:
            return False

        timeoutDuration: AbsTimeoutDuration = RandomLinearTimeoutDuration(
            maximumSeconds = action.maxDurationSeconds,
            minimumSeconds = action.minDurationSeconds,
        )

        self.__timeoutActionMachine.submitAction(AirStrikeTimeoutAction(
            timeoutDuration = timeoutDuration,
            ignoreInventory = True,
            maxTimeoutTargets = action.maxTimeoutChatters,
            minTimeoutTargets = action.minTimeoutChatters,
            pointRedemption = None,
            actionId = await self.__timeoutIdGenerator.generateActionId(),
            instigatorUserId = cheerUserId,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
            userTwitchAccessToken = userTwitchAccessToken,
            streamStatusRequirement = TimeoutStreamStatusRequirement.ANY,
            user = user,
        ))

        return True
