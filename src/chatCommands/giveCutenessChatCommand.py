import traceback
from typing import Final

from .absChatCommand import AbsChatCommand
from ..cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..trivia.triviaUtilsInterface import TriviaUtilsInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class GiveCutenessChatCommand(AbsChatCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        timber: TimberInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__cutenessRepository: Final[CutenessRepositoryInterface] = cutenessRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaUtils: Final[TriviaUtilsInterface] = triviaUtils
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCutenessEnabled or not user.isGiveCutenessEnabled:
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = ctx.getAuthorId(),
        ):
            return

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 3:
            self.__timber.log('GiveCutenessChatCommand', f'Less than 2 arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
            self.__twitchChatMessenger.send(
                text = f'⚠ Username and amount is necessary for this command. Example: !givecuteness {twitchHandle} 5',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        userName: str | None = splits[1]
        if not utils.isValidStr(userName) or not utils.strContainsAlphanumericCharacters(userName):
            self.__timber.log('GiveCutenessChatCommand', f'Username given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} is malformed: \"{userName}\"')
            self.__twitchChatMessenger.send(
                text = f'⚠ Username argument is malformed. Example: !givecuteness {twitchHandle} 5',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        incrementAmountStr: str | None = splits[2]
        if not utils.isValidStr(incrementAmountStr):
            self.__timber.log('GiveCutenessChatCommand', f'Increment amount given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} is malformed: \"{incrementAmountStr}\"')
            self.__twitchChatMessenger.send(
                text = f'⚠ Increment amount argument is malformed. Example: !givecuteness {userName} 5',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        try:
            incrementAmount = int(incrementAmountStr)
        except (SyntaxError, TypeError, ValueError) as e:
            self.__timber.log('GiveCutenessChatCommand', f'Unable to convert increment amount given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} into an int: \"{incrementAmountStr}\": {e}', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Increment amount argument is malformed. Example: !givecuteness @{userName} 5',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        userName = utils.removePreceedingAt(userName)
        userId = await self.__userIdsRepository.fetchUserId(userName = userName)

        if not utils.isValidStr(userId):
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to fetch user ID for \"{userName}\"',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        try:
            result = await self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = user.handle,
                twitchChannelId = await ctx.getTwitchChannelId(),
                userId = userId,
                userName = userName,
            )

            self.__twitchChatMessenger.send(
                text = f'ⓘ Cuteness for @{userName} is now {result.newCutenessStr} (was previously {result.previousCutenessStr})',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
        except (OverflowError, ValueError) as e:
            self.__timber.log('GiveCutenessChatCommand', f'Error giving {incrementAmount} cuteness from {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} to {userName}:{userId} in {user.handle}: {e}', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Error giving cuteness to \"{userName}\"',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        self.__timber.log('GiveCutenessChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
