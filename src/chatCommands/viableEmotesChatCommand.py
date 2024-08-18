import traceback

from .absChatCommand import AbsChatCommand
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from ..twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class ViableEmotesChatCommand(AbsChatCommand):

    def __init__(
        self,
        timber: TimberInterface,
        twitchEmotesHelper: TwitchEmotesHelperInterface,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchEmotesHelper, TwitchEmotesHelperInterface):
            raise TypeError(f'twitchEmotesHelper argument is malformed: \"{twitchEmotesHelper}\"')
        elif not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: TimberInterface = timber
        self.__twitchEmotesHelper: TwitchEmotesHelperInterface = twitchEmotesHelper
        self.__twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface = twitchFriendsUserIdRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        charlesUserId = await self.__twitchFriendsUserIdRepository.getCharlesUserId()
        viableEmotes: frozenset[str] = frozenset()

        try:
            viableEmotes = await self.__twitchEmotesHelper.fetchViableSubscriptionEmoteNames(
                twitchChannelId = charlesUserId
            )
        except Exception as e:
            self.__timber.log('ViableEmotesChatCommand', f'Encountered exception when fetching viable subscription emote names for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} ({charlesUserId=}) ({viableEmotes=}): {e}', e, traceback.format_exc())

        viableEmoteStrs = await self.__toStrList(viableEmotes)
        await self.__twitchUtils.safeSend(ctx, f'ⓘ Viable emotes: {viableEmoteStrs}')
        self.__timber.log('ViableEmotesChatCommand', f'Handled !viableemotes command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')

    async def __toStrList(self, viableEmotes: frozenset[str]) -> list[str]:
        viableEmotesList: list[str] = list(viableEmotes)
        return sorted(viableEmotesList, key = lambda emoteName: emoteName.casefold())
