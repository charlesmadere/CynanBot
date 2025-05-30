import traceback
from typing import Final

from .absChatCommand import AbsChatCommand
from ..cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class TestCheerActionChatCommand(AbsChatCommand):

    def __init__(
        self,
        twitchCheerHandler: AbsTwitchCheerHandler | None,
        cheerActionHelper: CheerActionHelperInterface | None,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if twitchCheerHandler is not None and not isinstance(twitchCheerHandler, AbsTwitchCheerHandler):
            raise TypeError(f'twitchCheerHandler argument is malformed: \"{twitchCheerHandler}\"')
        elif cheerActionHelper is not None and not isinstance(cheerActionHelper, CheerActionHelperInterface):
            raise TypeError(f'cheerActionHelper argument is malformed: \"{cheerActionHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__twitchCheerHandler: Final[AbsTwitchCheerHandler | None] = twitchCheerHandler
        self.__cheerActionHelper: Final[CheerActionHelperInterface | None] = cheerActionHelper
        self.__timber: Final[TimberInterface] = timber
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        twitchChannelId = await ctx.getTwitchChannelId()

        if twitchChannelId != ctx.getAuthorId():
            self.__timber.log('TestCheerActionChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        if not user.areCheerActionsEnabled:
            self.__timber.log('TestCheerActionChatCommand', f'Command use by {ctx.getAuthorName()}:{ctx.getAuthorId()} will not proceed as cheer actions in {user.handle} are not enabled!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('TestCheerActionChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} didn\'t specify a bit amount ({splits=})')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Bit amount argument is missing. Example: !testcheeraction 100',
                replyMessageId = await ctx.getMessageId()
            )
            return

        bits: int | None = None

        try:
            bits = int(splits[1])
        except Exception:
            pass

        if not utils.isValidInt(bits) or bits < 1 or bits > utils.getIntMaxSafeSize():
            self.__timber.log('TestCheerActionChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} specified an invalid bit amount ({splits=}) ({bits=})')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Bit amount argument is malformed. Example: !testcheeraction 100',
                replyMessageId = await ctx.getMessageId()
            )
            return

        message = utils.cleanStr(f'cheer{bits} ' + ' '.join(splits[2:]))
        result: bool | None = None
        exception: Exception | None = None

        if self.__twitchCheerHandler is not None:
            try:
                await self.__twitchCheerHandler.onNewCheer(
                    bits = bits,
                    broadcasterUserId = twitchChannelId,
                    chatMessage = message,
                    cheerUserId = ctx.getAuthorId(),
                    cheerUserLogin = ctx.getAuthorName(),
                    cheerUserName = ctx.getAuthorName(),
                    twitchChatMessageId = await ctx.getMessageId(),
                    user = user
                )
            except Exception as e:
                exception = e
                self.__timber.log('TestCheerActionChatCommand', f'Encountered exception when attempting to perform onNewCheer test for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({bits=}) ({message=}): {e}', e, traceback.format_exc())

        elif self.__twitchCheerHandler is not None:
            try:
                result = await self.__cheerActionHelper.handleCheerAction(
                    bits = bits,
                    broadcasterUserId = twitchChannelId,
                    cheerUserId = ctx.getAuthorId(),
                    cheerUserName = ctx.getAuthorName(),
                    message = message,
                    twitchChatMessageId = await ctx.getMessageId(),
                    user = user
                )
            except Exception as e:
                exception = e
                self.__timber.log('TestCheerActionChatCommand', f'Encountered exception when attempting to perform cheer action test for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({bits=}) ({message=}): {e}', e, traceback.format_exc())

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = f'ⓘ Cheer Action test results ({bits=}) ({message=}) ({result=}) ({exception=})',
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('TestCheerActionChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({bits=}) ({message=}) ({result=})')
