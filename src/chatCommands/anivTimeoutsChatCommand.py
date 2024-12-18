from .absChatCommand import AbsChatCommand
from ..aniv.anivCopyMessageTimeoutScorePresenterInterface import AnivCopyMessageTimeoutScorePresenterInterface
from ..aniv.anivCopyMessageTimeoutScoreRepositoryInterface import AnivCopyMessageTimeoutScoreRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class AnivTimeoutsChatCommand(AbsChatCommand):

    def __init__(
        self,
        anivCopyMessageTimeoutScorePresenter: AnivCopyMessageTimeoutScorePresenterInterface,
        anivCopyMessageTimeoutScoreRepository: AnivCopyMessageTimeoutScoreRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(anivCopyMessageTimeoutScorePresenter, AnivCopyMessageTimeoutScorePresenterInterface):
            raise TypeError(f'anivCopyMessageTimeoutScorePresenter argument is malformed: \"{anivCopyMessageTimeoutScorePresenter}\"')
        if not isinstance(anivCopyMessageTimeoutScoreRepository, AnivCopyMessageTimeoutScoreRepositoryInterface):
            raise TypeError(f'anivCopyMessageTimeoutScoreRepository argument is malformed: \"{anivCopyMessageTimeoutScoreRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__anivCopyMessageTimeoutScorePresenter: AnivCopyMessageTimeoutScorePresenterInterface = anivCopyMessageTimeoutScorePresenter
        self.__anivCopyMessageTimeoutScoreRepository: AnivCopyMessageTimeoutScoreRepositoryInterface = anivCopyMessageTimeoutScoreRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isAnivMessageCopyTimeoutEnabled:
            return

        userId = ctx.getAuthorId()
        userName = ctx.getAuthorName()
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) >= 2 and utils.strContainsAlphanumericCharacters(splits[1]):
            userName = utils.removePreceedingAt(splits[1])

        # this means that a user is querying for another user's timeout score
        if userName.casefold() != ctx.getAuthorName().casefold():
            userId = await self.__userIdsRepository.fetchUserId(userName = userName)

            if not utils.isValidStr(userId):
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'⚠ Unable to find aniv timeout score for \"{userName}\"',
                    replyMessageId = await ctx.getMessageId()
                )
                return

        score = await self.__anivCopyMessageTimeoutScoreRepository.getScore(
            chatterUserId = userId,
            chatterUserName = userName,
            twitchChannel = user.handle,
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        printOut = await self.__anivCopyMessageTimeoutScorePresenter.toString(
            score = score,
            language = user.defaultLanguage,
            chatterUserName = userName
        )

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = printOut,
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('MyAnivTimeoutsChatCommand', f'Handled !myanivtimeouts command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
