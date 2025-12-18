from typing import Final

from .absChatCommand import AbsChatCommand
from ..cuteness.cutenessPresenterInterface import CutenessPresenterInterface
from ..cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class CutenessChatCommand(AbsChatCommand):

    def __init__(
        self,
        cutenessPresenter: CutenessPresenterInterface,
        cutenessRepository: CutenessRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        delimiter: str = ', ',
    ):
        if not isinstance(cutenessPresenter, CutenessPresenterInterface):
            raise TypeError(f'cutenessPresenter argument is malformed: \"{cutenessPresenter}\"')
        elif not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        self.__cutenessPresenter: Final[CutenessPresenterInterface] = cutenessPresenter
        self.__cutenessRepository: Final[CutenessRepositoryInterface] = cutenessRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
        self.__delimiter: Final[str] = delimiter

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCutenessEnabled:
            return

        userName = ctx.getAuthorName()
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) >= 2 and utils.strContainsAlphanumericCharacters(splits[1]):
            userName = utils.removePreceedingAt(splits[1])

        # this means that a user is querying for another user's cuteness
        if userName.casefold() != ctx.getAuthorName().casefold():
            userId = await self.__userIdsRepository.fetchUserId(userName = userName)

            if not utils.isValidStr(userId):
                self.__twitchChatMessenger.send(
                    text = f'⚠ Unable to find cuteness info for \"{userName}\"',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )
                return

            result = await self.__cutenessRepository.fetchCuteness(
                twitchChannel = user.handle,
                twitchChannelId = await ctx.getTwitchChannelId(),
                userId = userId,
                userName = userName,
            )

            printOut = await self.__cutenessPresenter.printCuteness(result)

            self.__twitchChatMessenger.send(
                text = printOut,
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
        else:
            userId = ctx.getAuthorId()

            result = await self.__cutenessRepository.fetchCutenessLeaderboard(
                twitchChannel = user.handle,
                twitchChannelId = await ctx.getTwitchChannelId(),
                specificLookupUserId = userId,
                specificLookupUserName = userName,
            )

            printOut = await self.__cutenessPresenter.printLeaderboard(
                result = result,
                delimiter = self.__delimiter,
            )

            self.__twitchChatMessenger.send(
                text = printOut,
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        self.__timber.log('CutenessChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
