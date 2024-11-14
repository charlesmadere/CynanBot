from datetime import datetime
from typing import Collection

from .crowdControlButtonPressCheerAction import CrowdControlButtonPressCheerAction
from .crowdControlCheerAction import CrowdControlCheerAction
from .crowdControlCheerActionHelperInterface import CrowdControlCheerActionHelperInterface
from .crowdControlGameShuffleCheerAction import CrowdControlGameShuffleCheerAction
from ..absCheerAction import AbsCheerAction
from ...crowdControl.actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from ...crowdControl.actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from ...crowdControl.crowdControlMachineInterface import CrowdControlMachineInterface
from ...crowdControl.idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from ...crowdControl.utils.crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...users.userInterface import UserInterface


class CrowdControlCheerActionHelper(CrowdControlCheerActionHelperInterface):

    def __init__(
        self,
        crowdControlIdGenerator: CrowdControlIdGeneratorInterface,
        crowdControlMachine: CrowdControlMachineInterface,
        crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(crowdControlIdGenerator, CrowdControlIdGeneratorInterface):
            raise TypeError(f'crowdControlIdGenerator argument is malformed: \"{crowdControlIdGenerator}\"')
        elif not isinstance(crowdControlMachine, CrowdControlMachineInterface):
            raise TypeError(f'crowdControlMachine argument is malformed: \"{crowdControlMachine}\"')
        elif not isinstance(crowdControlUserInputUtils, CrowdControlUserInputUtilsInterface):
            raise TypeError(f'crowdControlUserInputUtils argument is malformed: \"{crowdControlUserInputUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__crowdControlIdGenerator: CrowdControlIdGeneratorInterface = crowdControlIdGenerator
        self.__crowdControlMachine: CrowdControlMachineInterface = crowdControlMachine
        self.__crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface = crowdControlUserInputUtils
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def handleCrowdControlCheerAction(
        self,
        actions: Collection[AbsCheerAction],
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
        if not user.areCheerActionsEnabled or not user.isCrowdControlEnabled:
            return False

        crowdControlAction: CrowdControlCheerAction | None = None

        for action in actions:
            if isinstance(action, CrowdControlCheerAction) and action.isEnabled and action.bits == bits:
                crowdControlAction = action
                break

        if crowdControlAction is None:
            return False

        elif isinstance(crowdControlAction, CrowdControlButtonPressCheerAction):
            return await self.__inputButtonPressIntoCrowdControl(
                action = crowdControlAction,
                cheerUserId = cheerUserId,
                cheerUserName = cheerUserName,
                message = message,
                twitchChannelId = broadcasterUserId,
                user = user
            )

        elif isinstance(crowdControlAction, CrowdControlGameShuffleCheerAction):
            return await self.__inputGameShuffleIntoCrowdControl(
                action = crowdControlAction,
                cheerUserId = cheerUserId,
                cheerUserName = cheerUserName,
                message = message,
                twitchChannelId = broadcasterUserId,
                user = user
            )

        else:
            self.__timber.log('CrowdControlCheerActionHelper', f'Encountered unknown CrowdControlCheerActionType value: \"{crowdControlAction.crowdControlCheerActionType}\"')
            return False

    async def __inputButtonPressIntoCrowdControl(
        self,
        action: CrowdControlButtonPressCheerAction,
        cheerUserId: str,
        cheerUserName: str,
        message: str | None,
        twitchChannelId: str,
        user: UserInterface
    ) -> bool:
        if not isinstance(action, CrowdControlButtonPressCheerAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        button = await self.__crowdControlUserInputUtils.parseButtonFromUserInput(
            userInput = message
        )

        if button is None:
            self.__timber.log('CrowdControlCheerActionHelper', f'Unable to parse user input into CrowdControlButton ({action=}) ({cheerUserId=}) ({cheerUserName=}) ({message=}) ({user=})')
            return False

        dateTime = datetime.now(self.__timeZoneRepository.getDefault())
        actionId = await self.__crowdControlIdGenerator.generateActionId()

        self.__crowdControlMachine.submitAction(ButtonPressCrowdControlAction(
            button = button,
            dateTime = dateTime,
            actionId = actionId,
            chatterUserId = cheerUserId,
            chatterUserName = cheerUserName,
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId
        ))

        return True

    async def __inputGameShuffleIntoCrowdControl(
        self,
        action: CrowdControlGameShuffleCheerAction,
        cheerUserId: str,
        cheerUserName: str,
        message: str | None,
        twitchChannelId: str,
        user: UserInterface
    ) -> bool:
        if not isinstance(action, CrowdControlGameShuffleCheerAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        dateTime = datetime.now(self.__timeZoneRepository.getDefault())
        actionId = await self.__crowdControlIdGenerator.generateActionId()

        self.__crowdControlMachine.submitAction(GameShuffleCrowdControlAction(
            dateTime = dateTime,
            actionId = actionId,
            chatterUserId = cheerUserId,
            chatterUserName = cheerUserName,
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId
        ))

        return True

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
