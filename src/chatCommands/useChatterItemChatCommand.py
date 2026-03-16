import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..chatterInventory.helpers.useChatterItemHelperInterface import UseChatterItemHelperInterface
from ..chatterInventory.idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ..chatterInventory.models.useChatterItemRequest import UseChatterItemRequest
from ..chatterInventory.models.useChatterItemResult import UseChatterItemResult
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class UseChatterItemChatCommand(AbsChatCommand2):

    def __init__(
        self,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        useChatterItemHelper: UseChatterItemHelperInterface,
    ):
        if not isinstance(chatterInventoryIdGenerator, ChatterInventoryIdGeneratorInterface):
            raise TypeError(f'chatterInventoryIdGenerator argument is malformed: \"{chatterInventoryIdGenerator}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(useChatterItemHelper, UseChatterItemHelperInterface):
            raise TypeError(f'useChatterItemHelper argument is malformed: \"{useChatterItemHelper}\"')

        self.__chatterInventoryIdGenerator: Final[ChatterInventoryIdGeneratorInterface] = chatterInventoryIdGenerator
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__useChatterItemHelper: Final[UseChatterItemHelperInterface] = useChatterItemHelper

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!use\b', re.IGNORECASE),
            re.compile(r'^\s*!use(?:\s+|_|-)?item\b', re.IGNORECASE),
            re.compile(r'^\s*!use(?:\s+|_|-)?chatter(?:\s+|_|-)?item\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'UseChatterItemChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isChatterInventoryEnabled:
            return ChatCommandResult.IGNORED

        # As it is currently written, this chat command does not specify an item type. Instead,
        # there is some logic within the UseChatterItemHelper class that will parse the user's
        # message and determine which item to use.

        result = await self.__useChatterItemHelper.useItem(UseChatterItemRequest(
            ignoreInventory = False,
            itemType = None,
            chatMessage = chatMessage.text,
            chatterUserId = chatMessage.chatterUserId,
            requestId = await self.__chatterInventoryIdGenerator.generateRequestId(),
            twitchChannelId = chatMessage.twitchChannelId,
            twitchChatMessageId = chatMessage.twitchChatMessageId,
            user = chatMessage.twitchUser,
        ))

        match result:
            case UseChatterItemResult.FEATURE_DISABLED:
                # this case is intentionally empty
                pass

            case UseChatterItemResult.INVALID_REQUEST:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Invalid item use request! Please try again',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

            case UseChatterItemResult.ITEM_DISABLED:
                # this case is intentionally empty
                pass

            case UseChatterItemResult.OK:
                # this case is intentionally empty
                pass

        self.__timber.log(self.commandName, f'Handled ({chatMessage=}) ({result=})')
        return ChatCommandResult.HANDLED
