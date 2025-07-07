import uuid
from typing import Final

from .absChatCommand import AbsChatCommand
from ..funtoon.tokens.funtoonTokensRepositoryInterface import FuntoonTokensRepositoryInterface
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class SetFuntoonTokenChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        funtoonTokensRepository: FuntoonTokensRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(funtoonTokensRepository, FuntoonTokensRepositoryInterface):
            raise TypeError(f'funtoonTokensRepository argument is malformed: \"{funtoonTokensRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__funtoonTokensRepository: Final[FuntoonTokensRepositoryInterface] = funtoonTokensRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        twitchChannelId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if twitchChannelId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('SetFuntoonTokenCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('SetFuntoonTokenCommand', f'Not enough arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} for the !setfuntoontoken command: \"{splits}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Token argument is necessary for the !setfuntoontoken command. Example: !setfuntoontoken {self.__getRandomTokenStr()}')
            return

        token: str | None = splits[1]
        if not utils.isValidStr(token):
            self.__timber.log('SetFuntoonTokenCommand', f'Invalid token argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} for the !setfuntoontoken command: \"{splits}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Token argument is necessary for the !setfuntoontoken command. Example: !setfuntoontoken {self.__getRandomTokenStr()}')
            return

        await self.__funtoonTokensRepository.setToken(
            token = token,
            twitchChannelId = twitchChannelId,
        )

        self.__timber.log('SetFuntoonTokenCommand', f'Handled !setfuntoontoken command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
        await self.__twitchUtils.safeSend(ctx, f'ⓘ Funtoon token has been updated')

    def __getRandomTokenStr(self) -> str:
        randomUuid = str(uuid.uuid4())
        randomUuid = randomUuid.replace('-', '')

        if len(randomUuid) > 16:
            randomUuid = randomUuid[0:16]

        return randomUuid
