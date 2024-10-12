from datetime import timedelta

from .absChatCommand import AbsChatCommand
from ..cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..cuteness.cutenessUtilsInterface import CutenessUtilsInterface
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class MyCutenessChatCommand(AbsChatCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        cutenessUtils: CutenessUtilsInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(seconds = 1)
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

        userId = ctx.getAuthorId()

        # this means that a user is querying for another user's cuteness history
        if userName.casefold() != ctx.getAuthorName().casefold():
            userId = await self.__userIdsRepository.fetchUserId(userName = userName)

            if not utils.isValidStr(userId):
                self.__timber.log('MyCutenessHistoryChatCommand', f'Unable to find user ID for \"{userName}\" in the database')
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'⚠ Unable to find user info for \"{userName}\" in the database!',
                    replyMessageId = await ctx.getMessageId()
                )
                return

        result = await self.__cutenessRepository.fetchCutenessHistory(
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = userId,
            userName = userName
        )

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = self.__cutenessUtils.getCutenessHistory(result, self.__delimiter),
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('MyCutenessHistoryChatCommand', f'Handled !mycutenesshistory command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
