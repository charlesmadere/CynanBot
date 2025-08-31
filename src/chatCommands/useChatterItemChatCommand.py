from typing import Final

from .absChatCommand import AbsChatCommand
from ..chatterInventory.helpers.useChatterItemHelperInterface import UseChatterItemHelperInterface
from ..chatterInventory.idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ..chatterInventory.models.useChatterItemRequest import UseChatterItemRequest
from ..chatterInventory.models.useChatterItemResult import UseChatterItemResult
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class UseChatterItemChatCommand(AbsChatCommand):

    def __init__(
        self,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        useChatterItemHelper: UseChatterItemHelperInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(chatterInventoryIdGenerator, ChatterInventoryIdGeneratorInterface):
            raise TypeError(f'chatterInventoryIdGenerator argument is malformed: \"{chatterInventoryIdGenerator}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(useChatterItemHelper, UseChatterItemHelperInterface):
            raise TypeError(f'useChatterItemHelper argument is malformed: \"{useChatterItemHelper}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__chatterInventoryIdGenerator: Final[ChatterInventoryIdGeneratorInterface] = chatterInventoryIdGenerator
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__useChatterItemHelper: Final[UseChatterItemHelperInterface] = useChatterItemHelper
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isChatterInventoryEnabled:
            return

        # As it is currently written, this chat command does not specify an item type. Instead,
        # there is some logic within the UseChatterItemHelper class that will parse the user's
        # message and determine which item to use.

        result = await self.__useChatterItemHelper.useItem(UseChatterItemRequest(
            ignoreInventory = False,
            itemType = None,
            pointRedemption = None,
            chatMessage = ctx.getMessageContent(),
            chatterUserId = ctx.getAuthorId(),
            requestId = await self.__chatterInventoryIdGenerator.generateRequestId(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            twitchChatMessageId = await ctx.getMessageId(),
            user = user,
        ))

        match result:
            case UseChatterItemResult.FEATURE_DISABLED:
                # this case is intentionally empty
                pass

            case UseChatterItemResult.INVALID_REQUEST:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Invalid item use request! Please try again',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )

            case UseChatterItemResult.ITEM_DISABLED:
                # this case is intentionally empty
                pass

            case UseChatterItemResult.OK:
                # this case is intentionally empty
                pass

        self.__timber.log('UseChatterItemChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
