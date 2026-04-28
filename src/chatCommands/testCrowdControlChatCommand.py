import re
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..crowdControl.actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from ..crowdControl.actions.crowdControlAction import CrowdControlAction
from ..crowdControl.actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from ..crowdControl.crowdControlMachineInterface import CrowdControlMachineInterface
from ..crowdControl.idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from ..crowdControl.utils.crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class TestCrowdControlChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        crowdControlIdGenerator: CrowdControlIdGeneratorInterface,
        crowdControlMachine: CrowdControlMachineInterface,
        crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(crowdControlIdGenerator, CrowdControlIdGeneratorInterface):
            raise TypeError(f'crowdControlIdGenerator argument is malformed: \"{crowdControlIdGenerator}\"')
        elif not isinstance(crowdControlMachine, CrowdControlMachineInterface):
            raise TypeError(f'crowdControlMachine argument is malformed: \"{crowdControlMachine}\"')
        elif not isinstance(crowdControlUserInputUtils, CrowdControlUserInputUtilsInterface):
            raise TypeError(f'crowdControlUserInputUtils  argument is malformed: \"{crowdControlUserInputUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__crowdControlIdGenerator: Final[CrowdControlIdGeneratorInterface] = crowdControlIdGenerator
        self.__crowdControlMachine: Final[CrowdControlMachineInterface] = crowdControlMachine
        self.__crowdControlUserInputUtils: Final[CrowdControlUserInputUtilsInterface] = crowdControlUserInputUtils
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!testcrowdcontrol\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'TestCrowdControlChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isCrowdControlEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)

        userInput: str | None = None
        if len(splits) >= 2:
            userInput = splits[1].strip()

        button = await self.__crowdControlUserInputUtils.parseButtonFromUserInput(
            userInput = userInput,
        )

        now = self.__timeZoneRepository.getNow()
        actionId = await self.__crowdControlIdGenerator.generateActionId()
        crowdControlAction: CrowdControlAction

        if button is None:
            crowdControlAction = GameShuffleCrowdControlAction(
                dateTime = now,
                entryWithinGigaShuffle = False,
                startOfGigaShuffleSize = None,
                actionId = actionId,
                chatterUserId = chatMessage.chatterUserId,
                chatterUserName = chatMessage.chatterUserName,
                twitchChannel = chatMessage.twitchChannel,
                twitchChannelId = chatMessage.twitchChannelId,
                twitchChatMessageId = chatMessage.twitchChatMessageId,
            )
        else:
            crowdControlAction = ButtonPressCrowdControlAction(
                button = button,
                dateTime = now,
                actionId = actionId,
                chatterUserId = chatMessage.chatterUserId,
                chatterUserName = chatMessage.chatterUserName,
                twitchChannel = chatMessage.twitchChannel,
                twitchChannelId = chatMessage.twitchChannelId,
                twitchChatMessageId = chatMessage.twitchChatMessageId,
            )

        self.__crowdControlMachine.submitAction(crowdControlAction)

        self.__twitchChatMessenger.send(
            text = f'ⓘ Submitted crowd control action ({button=}) ({crowdControlAction.actionType=})',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({crowdControlAction=}) ({button=}) ({chatMessage=})')
        return ChatCommandResult.HANDLED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId
        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()
        return isStreamer or isAdministrator
