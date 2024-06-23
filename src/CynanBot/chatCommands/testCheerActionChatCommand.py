import traceback

import CynanBot.misc.utils as utils
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.cheerActions.cheerActionHelperInterface import \
    CheerActionHelperInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class TestCheerActionChatCommand(AbsChatCommand):

    def __init__(
        self,
        cheerActionHelper: CheerActionHelperInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(cheerActionHelper, CheerActionHelperInterface):
            raise TypeError(f'cheerActionHelper argument is malformed: \"{cheerActionHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__cheerActionHelper: CheerActionHelperInterface = cheerActionHelper
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        twitchChannelId = await ctx.getTwitchChannelId()

        if twitchChannelId != ctx.getAuthorId():
            self.__timber.log('TestCheerActionChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            return

        bits: int | None = None

        try:
            bits = int(splits[1])
        except Exception:
            pass

        if not utils.isValidInt(bits) or bits < 1 or bits > utils.getIntMaxSafeSize():
            self.__timber.log('TestCheerActionChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} specified an invalid bit amount ({splits=}) ({bits=})')
            return

        result: bool | None = None
        exception: Exception | None = None

        try:
            result = await self.__cheerActionHelper.handleCheerAction(
                bits = bits,
                broadcasterUserId = twitchChannelId,
                cheerUserId = ctx.getAuthorId(),
                cheerUserName = ctx.getAuthorName(),
                message = ' '.join(splits),
                user = user
            )
        except Exception as e:
            exception = e
            self.__timber.log('TestCheerActionChatCommand', f'Encountered exception when attempting to perform cheer action test for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()}: {e}', e, traceback.format_exc())

        await self.__twitchUtils.safeSend(ctx, f'ⓘ Cheer Action test results ({result=}) ({exception=})')
        self.__timber.log('TestCheerActionChatCommand', f'Handled !testcheeraction command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()} ({result=})')
