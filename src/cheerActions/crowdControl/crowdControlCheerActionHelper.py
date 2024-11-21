import random
from datetime import datetime
from typing import Collection

from frozenlist import FrozenList

from .crowdControlButtonPressCheerAction import CrowdControlButtonPressCheerAction
from .crowdControlCheerActionHelperInterface import CrowdControlCheerActionHelperInterface
from .crowdControlGameShuffleCheerAction import CrowdControlGameShuffleCheerAction
from ..absCheerAction import AbsCheerAction
from ...crowdControl.actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from ...crowdControl.actions.crowdControlAction import CrowdControlAction
from ...crowdControl.actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from ...crowdControl.crowdControlMachineInterface import CrowdControlMachineInterface
from ...crowdControl.crowdControlSettingsRepositoryInterface import CrowdControlSettingsRepositoryInterface
from ...crowdControl.idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from ...crowdControl.utils.crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...users.userInterface import UserInterface


class CrowdControlCheerActionHelper(CrowdControlCheerActionHelperInterface):

    def __init__(
        self,
        crowdControlIdGenerator: CrowdControlIdGeneratorInterface,
        crowdControlMachine: CrowdControlMachineInterface,
        crowdControlSettingsRepository: CrowdControlSettingsRepositoryInterface,
        crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface
    ):
        if not isinstance(crowdControlIdGenerator, CrowdControlIdGeneratorInterface):
            raise TypeError(f'crowdControlIdGenerator argument is malformed: \"{crowdControlIdGenerator}\"')
        elif not isinstance(crowdControlMachine, CrowdControlMachineInterface):
            raise TypeError(f'crowdControlMachine argument is malformed: \"{crowdControlMachine}\"')
        elif not isinstance(crowdControlSettingsRepository, CrowdControlSettingsRepositoryInterface):
            raise TypeError(f'crowdControlSettingsRepository argument is malformed: \"{crowdControlSettingsRepository}\"')
        elif not isinstance(crowdControlUserInputUtils, CrowdControlUserInputUtilsInterface):
            raise TypeError(f'crowdControlUserInputUtils argument is malformed: \"{crowdControlUserInputUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__crowdControlIdGenerator: CrowdControlIdGeneratorInterface = crowdControlIdGenerator
        self.__crowdControlMachine: CrowdControlMachineInterface = crowdControlMachine
        self.__crowdControlSettingsRepository: CrowdControlSettingsRepositoryInterface = crowdControlSettingsRepository
        self.__crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface = crowdControlUserInputUtils
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

    async def __createGameShuffleActions(
        self,
        action: CrowdControlGameShuffleCheerAction,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None
    ) -> Collection[CrowdControlAction]:
        dateTime = datetime.now(self.__timeZoneRepository.getDefault())
        actions: FrozenList[CrowdControlAction] = FrozenList()

        gigaShuffleChance = action.gigaShuffleChance
        if await self.__crowdControlSettingsRepository.isGigaShuffleEnabled() and utils.isValidInt(gigaShuffleChance) and gigaShuffleChance > 0:
            gigaShuffleFloat = float(gigaShuffleChance) / float(100)
            randomNumber = random.random()

            if randomNumber < gigaShuffleFloat:
                gigaMinimum = await self.__crowdControlSettingsRepository.getMinGigaShuffleCount()
                gigaMaximum = await self.__crowdControlSettingsRepository.getMaxGigaShuffleCount()
                gigaScale = random.random()
                gigaShuffleCount = int(round(pow(gigaScale, 9) * (gigaMaximum - gigaMinimum) + gigaMinimum))

                self.__timber.log('CrowdControlCheerActionHelper', f'Encountered giga shuffle event: ({gigaShuffleFloat=}) ({randomNumber=}) ({gigaMinimum=}) ({gigaMaximum=}) ({gigaScale=}) ({gigaShuffleCount=})')

                if gigaShuffleCount >= 1:
                    actions.append(GameShuffleCrowdControlAction(
                        dateTime = dateTime,
                        startOfGigaShuffleSize = gigaShuffleCount,
                        actionId = await self.__crowdControlIdGenerator.generateActionId(),
                        chatterUserId = chatterUserId,
                        chatterUserName = chatterUserName,
                        twitchChannel = twitchChannel,
                        twitchChannelId = twitchChannelId,
                        twitchChatMessageId = twitchChatMessageId
                    ))

                    for _ in range(gigaShuffleCount - 1):
                        actions.append(GameShuffleCrowdControlAction(
                            dateTime = dateTime,
                            startOfGigaShuffleSize = None,
                            actionId = await self.__crowdControlIdGenerator.generateActionId(),
                            chatterUserId = chatterUserId,
                            chatterUserName = chatterUserName,
                            twitchChannel = twitchChannel,
                            twitchChannelId = twitchChannelId,
                            twitchChatMessageId = twitchChatMessageId
                        ))

        if len(actions) == 0:
            actions.append(GameShuffleCrowdControlAction(
                dateTime = dateTime,
                startOfGigaShuffleSize = None,
                actionId = await self.__crowdControlIdGenerator.generateActionId(),
                chatterUserId = chatterUserId,
                chatterUserName = chatterUserName,
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId,
                twitchChatMessageId = twitchChatMessageId
            ))

        actions.freeze()
        return actions

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
        twitchChatMessageId: str | None,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        if not user.isCrowdControlEnabled:
            return False

        crowdControlAction: AbsCheerAction | None = None

        for action in actions:
            if not isinstance(action, CrowdControlButtonPressCheerAction) and not isinstance(action, CrowdControlGameShuffleCheerAction):
                continue
            elif not action.isEnabled or action.bits != bits:
                continue
            else:
                crowdControlAction = action
                break

        if crowdControlAction is None:
            return False

        elif isinstance(crowdControlAction, CrowdControlButtonPressCheerAction):
            return await self.__inputButtonPressIntoCrowdControl(
                action = crowdControlAction,
                chatterUserId = cheerUserId,
                chatterUserName = cheerUserName,
                message = message,
                twitchChannelId = broadcasterUserId,
                twitchChatMessageId = twitchChatMessageId,
                user = user
            )

        elif isinstance(crowdControlAction, CrowdControlGameShuffleCheerAction):
            return await self.__inputGameShuffleIntoCrowdControl(
                action = crowdControlAction,
                chatterUserId = cheerUserId,
                chatterUserName = cheerUserName,
                message = message,
                twitchChannelId = broadcasterUserId,
                twitchChatMessageId = twitchChatMessageId,
                user = user
            )

        else:
            raise RuntimeError(f'Encountered unknown AbsCheerAction value: \"{crowdControlAction}\"')

    async def __inputButtonPressIntoCrowdControl(
        self,
        action: CrowdControlButtonPressCheerAction,
        chatterUserId: str,
        chatterUserName: str,
        message: str | None,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface
    ) -> bool:
        if not isinstance(action, CrowdControlButtonPressCheerAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        button = await self.__crowdControlUserInputUtils.parseButtonFromUserInput(
            userInput = message
        )

        if button is None:
            self.__timber.log('CrowdControlCheerActionHelper', f'Unable to parse user input into CrowdControlButton ({action=}) ({chatterUserId=}) ({chatterUserName=}) ({message=}) ({user=})')
            return False

        dateTime = datetime.now(self.__timeZoneRepository.getDefault())
        actionId = await self.__crowdControlIdGenerator.generateActionId()

        self.__crowdControlMachine.submitAction(ButtonPressCrowdControlAction(
            button = button,
            dateTime = dateTime,
            actionId = actionId,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId
        ))

        return True

    async def __inputGameShuffleIntoCrowdControl(
        self,
        action: CrowdControlGameShuffleCheerAction,
        chatterUserId: str,
        chatterUserName: str,
        message: str | None,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface
    ) -> bool:
        if not isinstance(action, CrowdControlGameShuffleCheerAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        gameShuffleActions = await self.__createGameShuffleActions(
            action = action,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId
        )

        for gameShuffleAction in gameShuffleActions:
            self.__crowdControlMachine.submitAction(gameShuffleAction)

        return True
