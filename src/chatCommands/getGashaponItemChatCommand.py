import re
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..chatterInventory.idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ..chatterInventory.machine.chatterInventoryMachineInterface import ChatterInventoryMachineInterface
from ..chatterInventory.models.requestGashaponRewardAction import RequestGashaponRewardAction
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class GetGashaponItemChatCommand(AbsChatCommand):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface,
        chatterInventoryMachine: ChatterInventoryMachineInterface,
        timber: TimberInterface,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(chatterInventoryIdGenerator, ChatterInventoryIdGeneratorInterface):
            raise TypeError(f'chatterInventoryIdGenerator argument is malformed: \"{chatterInventoryIdGenerator}\"')
        elif not isinstance(chatterInventoryMachine, ChatterInventoryMachineInterface):
            raise TypeError(f'chatterInventoryMachine argument is malformed: \"{chatterInventoryMachine}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__chatterInventoryIdGenerator: Final[ChatterInventoryIdGeneratorInterface] = chatterInventoryIdGenerator
        self.__chatterInventoryMachine: Final[ChatterInventoryMachineInterface] = chatterInventoryMachine
        self.__timber: Final[TimberInterface] = timber

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!(?:get\s*)?chest\b', re.IGNORECASE),
            re.compile(r'^\s*!(?:get\s*)?gat?cha(?:pon)?\b', re.IGNORECASE),
            re.compile(r'^\s*!(?:get\s*)?gat?chi(?:pon)?\b', re.IGNORECASE),
            re.compile(r'^\s*!(?:get\s*)?gasha(?:pon)?\b', re.IGNORECASE),
            re.compile(r'^\s*!(?:get\s*)?loot(?:box)?\b', re.IGNORECASE),
            re.compile(r'^\s*!(?:get\s*)?loot(?:crate)?\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'GetGashaponItemChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isChatterInventoryEnabled:
            return ChatCommandResult.IGNORED

        self.__chatterInventoryMachine.submitAction(RequestGashaponRewardAction(
            actionId = await self.__chatterInventoryIdGenerator.generateActionId(),
            chatMessage = chatMessage.text,
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
            twitchChatMessageId = chatMessage.twitchChatMessageId,
            user = chatMessage.twitchUser,
        ))

        self.__timber.log(self.commandName, f'Handled ({chatMessage=})')
        return ChatCommandResult.HANDLED
