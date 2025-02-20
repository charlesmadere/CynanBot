from .absChatCommand import AbsChatCommand
from ..chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter
from ..chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class GetChatterPreferredTtsChatCommand(AbsChatCommand):

    def __init__(
        self,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        chatterPreferredTtsPresenter: ChatterPreferredTtsPresenter,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(chatterPreferredTtsPresenter, ChatterPreferredTtsPresenter):
            raise TypeError(f'chatterPreferredTtsPresenter argument is malformed: \"{chatterPreferredTtsPresenter}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface = chatterPreferredTtsHelper
        self.__chatterPreferredTtsPresenter: ChatterPreferredTtsPresenter = chatterPreferredTtsPresenter
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        if not user.isChatterPreferredTtsEnabled:
            return

        preferredTts = await self.__chatterPreferredTtsHelper.get(
            chatterUserId = ctx.getAuthorId(),
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if preferredTts is None:
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'ⓘ You have no preferred TTS',
                replyMessageId = await ctx.getMessageId()
            )
            return

        printOut = await self.__chatterPreferredTtsPresenter.printOut(preferredTts)

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = f'ⓘ Your preferred TTS: {printOut}',
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('GetChatterPreferredTtsChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
