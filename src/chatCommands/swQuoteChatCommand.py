from datetime import timedelta
from typing import Final

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..starWars.starWarsQuotesRepositoryInterface import StarWarsQuotesRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class SwQuoteChatCommand(AbsChatCommand):

    def __init__(
        self,
        starWarsQuotesRepository: StarWarsQuotesRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 30),
    ):
        if not isinstance(starWarsQuotesRepository, StarWarsQuotesRepositoryInterface):
            raise TypeError(f'starWarsQuotesRepository argument is malformed: \"{starWarsQuotesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__starWarsQuotesRepository: Final[StarWarsQuotesRepositoryInterface] = starWarsQuotesRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
        self.__lastMessageTimes: Final[TimedDict] = TimedDict(cooldown)

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isStarWarsQuotesEnabled:
            return
        elif not ctx.isAuthorMod and not self.__lastMessageTimes.isReadyAndUpdate(user.handle):
            return

        randomSpaceEmoji = utils.getRandomSpaceEmoji()
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) < 2:
            swQuote = await self.__starWarsQuotesRepository.fetchRandomQuote()
            self.__twitchChatMessenger.send(
                text = f'{swQuote} {randomSpaceEmoji}',
                twitchChannelId = await ctx.getTwitchChannelId(),
            )
            return

        query = ' '.join(splits[1:])

        try:
            swQuote = await self.__starWarsQuotesRepository.searchQuote(query)

            if utils.isValidStr(swQuote):
                self.__twitchChatMessenger.send(
                    text = f'{swQuote} {randomSpaceEmoji}',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                )
            else:
                self.__twitchChatMessenger.send(
                    text = f'⚠ No Star Wars quote found for the given query: \"{query}\"',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                )
        except ValueError:
            self.__timber.log('SwQuoteCommand', f'Error retrieving Star Wars quote with query: \"{query}\"')
            self.__twitchChatMessenger.send(
                text = f'⚠ Error retrieving Star Wars quote with query: \"{query}\"',
                twitchChannelId = await ctx.getTwitchChannelId(),
            )
