import traceback
from typing import Final

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..network.exceptions import GenericNetworkException
from ..pkmn.pokepediaRepositoryInterface import PokepediaRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class PkMoveChatCommand(AbsChatCommand):

    def __init__(
        self,
        pokepediaRepository: PokepediaRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(pokepediaRepository, PokepediaRepositoryInterface):
            raise TypeError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__pokepediaRepository: Final[PokepediaRepositoryInterface] = pokepediaRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isPokepediaEnabled:
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__twitchChatMessenger.send(
                text = '⚠ A Pokémon move name is necessary for the !pkmove command. Example: !pkmove fire spin',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        name = ' '.join(splits[1:])

        try:
            move = await self.__pokepediaRepository.searchMoves(name)

            for string in move.toStrList():
                self.__twitchChatMessenger.send(
                    text = string,
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )
        except (GenericNetworkException, RuntimeError, ValueError) as e:
            self.__timber.log('PkMoveChatCommand', f'Error retrieving Pokemon move ({name=}): {e}', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Error retrieving Pokémon move: \"{name}\"',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        self.__timber.log('PkMoveChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
