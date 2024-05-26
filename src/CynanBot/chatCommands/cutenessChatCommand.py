from datetime import timedelta

import CynanBot.misc.utils as utils
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.cuteness.cutenessLeaderboardResult import \
    CutenessLeaderboardResult
from CynanBot.cuteness.cutenessRepositoryInterface import \
    CutenessRepositoryInterface
from CynanBot.cuteness.cutenessResult import CutenessResult
from CynanBot.cuteness.cutenessUtilsInterface import CutenessUtilsInterface
from CynanBot.misc.timedDict import TimedDict
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class CutenessChatCommand(AbsChatCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        cutenessUtils: CutenessUtilsInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(seconds = 2)
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(cutenessUtils, CutenessUtilsInterface):
            raise TypeError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepositoryInterface = cutenessRepository
        self.__cutenessUtils: CutenessUtilsInterface = cutenessUtils
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__delimiter: str = delimiter
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    def __cutenessLeaderboardResultToStr(self, result: CutenessLeaderboardResult) -> str:
        if not isinstance(result, CutenessLeaderboardResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')

        if result.entries is None or len(result.entries) == 0:
            return f'{result.cutenessDate.getHumanString()} Leaderboard is empty 😿'

        specificLookupText: str | None = None

        if result.specificLookupCutenessResult is not None:
            userName = result.specificLookupCutenessResult.userName
            cutenessStr = result.specificLookupCutenessResult.cutenessStr
            specificLookupText = f'@{userName} your cuteness is {cutenessStr}'

        leaderboard = self.__cutenessUtils.getLeaderboard(
            entries = result.entries,
            delimiter = self.__delimiter
        )

        if utils.isValidStr(specificLookupText):
            return f'{specificLookupText}, and the {result.cutenessDate.getHumanString()} Leaderboard is: {leaderboard} ✨'
        else:
            return f'{result.cutenessDate.getHumanString()} Leaderboard {leaderboard} ✨'

    def __cutenessResultToStr(self, result: CutenessResult) -> str:
        if not isinstance(result, CutenessResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')

        cuteness = result.cuteness

        if utils.isValidInt(cuteness) and cuteness >= 1:
            return f'{result.userName}\'s {result.cutenessDate.getHumanString()} cuteness is {result.cutenessStr} ✨'
        else:
            return f'{result.userName} has no cuteness in {result.cutenessDate.getHumanString()}'

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCutenessEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        userName = ctx.getAuthorName()
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) >= 2 and utils.strContainsAlphanumericCharacters(splits[1]):
            userName = utils.removePreceedingAt(splits[1])

        # this means that a user is querying for another user's cuteness
        if userName.lower() != ctx.getAuthorName().lower():
            userId = await self.__userIdsRepository.fetchUserId(userName = userName)

            if not utils.isValidStr(userId):
                await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to find user info for \"{userName}\" in the database!')
                return

            result = await self.__cutenessRepository.fetchCuteness(
                twitchChannel = user.getHandle(),
                twitchChannelId = await ctx.getTwitchChannelId(),
                userId = userId,
                userName = userName
            )

            await self.__twitchUtils.safeSend(ctx, self.__cutenessResultToStr(result))
        else:
            userId = ctx.getAuthorId()

            result = await self.__cutenessRepository.fetchCutenessLeaderboard(
                twitchChannel = user.getHandle(),
                twitchChannelId = await ctx.getTwitchChannelId(),
                specificLookupUserId = userId,
                specificLookupUserName = userName
            )

            await self.__twitchUtils.safeSend(ctx, self.__cutenessLeaderboardResultToStr(result))

        self.__timber.log('CutenessChatCommand', f'Handled !cuteness command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
