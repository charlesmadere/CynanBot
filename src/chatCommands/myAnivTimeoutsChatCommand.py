from datetime import timedelta

from .absChatCommand import AbsChatCommand
from ..aniv.anivCopyMessageTimeoutScorePresenterInterface import AnivCopyMessageTimeoutScorePresenterInterface
from ..aniv.anivCopyMessageTimeoutScoreRepositoryInterface import AnivCopyMessageTimeoutScoreRepositoryInterface
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class MyAnivTimeoutsChatCommand(AbsChatCommand):

    def __init__(
        self,
        anivCopyMessageTimeoutScorePresenter: AnivCopyMessageTimeoutScorePresenterInterface,
        anivCopyMessageTimeoutScoreRepository: AnivCopyMessageTimeoutScoreRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 1)
    ):
        if not isinstance(anivCopyMessageTimeoutScorePresenter, AnivCopyMessageTimeoutScorePresenterInterface):
            raise TypeError(f'anivCopyMessageTimeoutScorePresenter argument is malformed: \"{anivCopyMessageTimeoutScorePresenter}\"')
        if not isinstance(anivCopyMessageTimeoutScoreRepository, AnivCopyMessageTimeoutScoreRepositoryInterface):
            raise TypeError(f'anivCopyMessageTimeoutScoreRepository argument is malformed: \"{anivCopyMessageTimeoutScoreRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__anivCopyMessageTimeoutScorePresenter: AnivCopyMessageTimeoutScorePresenterInterface = anivCopyMessageTimeoutScorePresenter
        self.__anivCopyMessageTimeoutScoreRepository: AnivCopyMessageTimeoutScoreRepositoryInterface = anivCopyMessageTimeoutScoreRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isAnivMessageCopyTimeoutEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        score = await self.__anivCopyMessageTimeoutScoreRepository.getScore(
            chatterUserId = ctx.getAuthorId(),
            chatterUserName = ctx.getAuthorName(),
            twitchChannel = ctx.getTwitchChannelName(),
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if score is None:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ @{ctx.getAuthorName()} has no aniv timeouts')
        else:
            printOut = await self.__anivCopyMessageTimeoutScorePresenter.toString(score)
            await self.__twitchUtils.safeSend(ctx, printOut)

        self.__timber.log('MyAnivTimeoutsChatCommand', f'Handled !myanivtimeouts command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
