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


class PkMonChatCommand(AbsChatCommand):

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
                text = '⚠ A Pokémon name is necessary for the !pkmon command. Example: !pkmon charizard',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        name = splits[1]

        try:
            mon = await self.__pokepediaRepository.searchPokemon(name)

            for string in mon.toStrList():
                self.__twitchChatMessenger.send(
                    text = string,
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )
        except (GenericNetworkException, RuntimeError, ValueError) as e:
            self.__timber.log('PkMonChatCommand', f'Error retrieving Pokemon ({name=}): {e}', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Error retrieving Pokémon: \"{name}\"',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        self.__timber.log('PkMonChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
