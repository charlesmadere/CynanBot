import traceback

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..network.exceptions import GenericNetworkException
from ..pkmn.pokepediaRepositoryInterface import PokepediaRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class PkMoveChatCommand(AbsChatCommand):

    def __init__(
        self,
        pokepediaRepository: PokepediaRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(pokepediaRepository, PokepediaRepositoryInterface):
            raise TypeError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__pokepediaRepository: PokepediaRepositoryInterface = pokepediaRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isPokepediaEnabled:
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            await self.__twitchUtils.safeSend(ctx, '⚠ A Pokémon move name is necessary for the !pkmove command. Example: !pkmove fire spin')
            return

        name = ' '.join(splits[1:])

        try:
            move = await self.__pokepediaRepository.searchMoves(name)

            for string in move.toStrList():
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = string,
                    replyMessageId = await ctx.getMessageId()
                )
        except (GenericNetworkException, RuntimeError, ValueError) as e:
            self.__timber.log('PkMoveChatCommand', f'Error retrieving Pokemon move ({name=}): {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Error retrieving Pokémon move: \"{name}\"')

        self.__timber.log('PkMoveChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
