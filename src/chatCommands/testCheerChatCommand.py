import traceback
from typing import Final

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class TestCheerChatCommand(AbsChatCommand):

    def __init__(
        self,
        twitchCheerHandler: AbsTwitchCheerHandler,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(twitchCheerHandler, AbsTwitchCheerHandler):
            raise TypeError(f'twitchCheerHandler argument is malformed: \"{twitchCheerHandler}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__twitchCheerHandler: Final[AbsTwitchCheerHandler] = twitchCheerHandler
        self.__timber: Final[TimberInterface] = timber
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        twitchChannelId = await ctx.getTwitchChannelId()

        if twitchChannelId != ctx.getAuthorId():
            self.__timber.log('TestCheerChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        if not user.areCheerActionsEnabled:
            self.__timber.log('TestCheerChatCommand', f'Command use by {ctx.getAuthorName()}:{ctx.getAuthorId()} will not proceed as cheer actions in {user.handle} are not enabled!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('TestCheerChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} didn\'t specify a bit amount ({splits=})')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Bit amount argument is missing. Example: !testcheer 100',
                replyMessageId = await ctx.getMessageId()
            )
            return

        bits: int | None = None

        try:
            bits = int(splits[1])
        except:
            pass

        if not utils.isValidInt(bits) or bits < 1 or bits > utils.getIntMaxSafeSize():
            self.__timber.log('TestCheerChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} specified an invalid bit amount ({splits=}) ({bits=})')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Bit amount argument is malformed. Example: !testcheer 100',
                replyMessageId = await ctx.getMessageId()
            )
            return

        chatMessage = utils.cleanStr(f'cheer{bits} ' + ' '.join(splits[2:]))
        exception: Exception | None = None

        try:
            await self.__twitchCheerHandler.onNewCheer(AbsTwitchCheerHandler.CheerData(
                bits = bits,
                chatMessage = chatMessage,
                cheerUserId = ctx.getAuthorId(),
                cheerUserLogin = ctx.getAuthorName(),
                cheerUserName = ctx.getAuthorDisplayName(),
                twitchChannelId = twitchChannelId,
                twitchChatMessageId = await ctx.getMessageId(),
                user = user,
            ))
        except Exception as e:
            exception = e
            self.__timber.log('TestCheerChatCommand', f'Encountered exception when attempting to run onNewCheer() for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({bits=}) ({chatMessage=}): {e}', e, traceback.format_exc())

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = f'ⓘ Cheer test results ({bits=}) ({chatMessage=}) ({exception=})',
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('TestCheerChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({bits=}) ({chatMessage=}) ({exception=})')
