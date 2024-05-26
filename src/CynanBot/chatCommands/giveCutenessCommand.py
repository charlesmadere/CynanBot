import traceback

import CynanBot.misc.utils as utils
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.cuteness.cutenessRepositoryInterface import \
    CutenessRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.triviaUtilsInterface import TriviaUtilsInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class GiveCutenessCommand(AbsChatCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        timber: TimberInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__cutenessRepository: CutenessRepositoryInterface = cutenessRepository
        self.__timber: TimberInterface = timber
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCutenessEnabled() or not user.isGiveCutenessEnabled():
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = ctx.getAuthorId()
        ):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 3:
            self.__timber.log('GiveCutenessCommand', f'Less than 3 arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Username and amount is necessary for the !givecuteness command. Example: !givecuteness {user.getHandle()} 5')
            return

        userName: str | None = splits[1]
        if not utils.isValidStr(userName) or not utils.strContainsAlphanumericCharacters(userName):
            self.__timber.log('GiveCutenessCommand', f'Username given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is malformed: \"{userName}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Username argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        incrementAmountStr: str | None = splits[2]
        if not utils.isValidStr(incrementAmountStr):
            self.__timber.log('GiveCutenessCommand', f'Increment amount given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is malformed: \"{incrementAmountStr}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Increment amount argument is malformed. Example: !givecuteness {userName} 5')
            return

        try:
            incrementAmount = int(incrementAmountStr)
        except (SyntaxError, TypeError, ValueError) as e:
            self.__timber.log('GiveCutenessCommand', f'Unable to convert increment amount given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} into an int: \"{incrementAmountStr}\": {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Increment amount argument is malformed. Example: !givecuteness {userName} 5')
            return

        userName = utils.removePreceedingAt(userName)
        userId = await self.__userIdsRepository.fetchUserId(userName = userName)

        if not utils.isValidStr(userId):
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to fetch user ID for \"{userName}\"!')
            return

        try:
            result = await self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = user.getHandle(),
                twitchChannelId = await ctx.getTwitchChannelId(),
                userId = userId,
                userName = userName
            )

            await self.__twitchUtils.safeSend(ctx, f'ⓘ Cuteness for {userName} is now {result.cutenessStr} ✨')
        except (OverflowError, ValueError) as e:
            self.__timber.log('GiveCutenessCommand', f'Error giving {incrementAmount} cuteness from {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} to {userName}:{userId} in {user.getHandle()}: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Error giving cuteness to \"{userName}\"')

        self.__timber.log('GiveCutenessCommand', f'Handled !givecuteness command of {incrementAmount} for {userName}:{userId} from {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
