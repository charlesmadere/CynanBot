from datetime import timedelta

from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..misc.timedDict import TimedDict
from ..timber.timberInterface import TimberInterface
from ..trivia.score.triviaScoreRepositoryInterface import TriviaScoreRepositoryInterface
from ..trivia.specialStatus.shinyTriviaOccurencesRepositoryInterface import ShinyTriviaOccurencesRepositoryInterface
from ..trivia.specialStatus.toxicTriviaOccurencesRepositoryInterface import ToxicTriviaOccurencesRepositoryInterface
from ..trivia.triviaUtilsInterface import TriviaUtilsInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class TriviaScoreChatCommand(AbsChatCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepositoryInterface,
        timber: TimberInterface,
        toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface,
        triviaScoreRepository: TriviaScoreRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 2)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(shinyTriviaOccurencesRepository, ShinyTriviaOccurencesRepositoryInterface):
            raise TypeError(f'shinyTriviaOccurencesRepository argument is malformed: \"{shinyTriviaOccurencesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(toxicTriviaOccurencesRepository, ToxicTriviaOccurencesRepositoryInterface):
            raise TypeError(f'toxicTriviaOccurencesRepository argument is malformed: \"{toxicTriviaOccurencesRepository}\"')
        elif not isinstance(triviaScoreRepository, TriviaScoreRepositoryInterface):
            raise TypeError(f'triviaScoreRepository argument is malformed: \"{triviaScoreRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepositoryInterface = shinyTriviaOccurencesRepository
        self.__timber: TimberInterface = timber
        self.__toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface = toxicTriviaOccurencesRepository
        self.__triviaScoreRepository: TriviaScoreRepositoryInterface = triviaScoreRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaScoreEnabled:
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        userName = ctx.getAuthorName()
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) >= 2 and utils.strContainsAlphanumericCharacters(splits[1]):
            userName = utils.removePreceedingAt(splits[1])

        userId = ctx.getAuthorId()

        # this means that a user is querying for another user's trivia score
        if userName.casefold() != ctx.getAuthorName().casefold():
            userId = await self.__userIdsRepository.fetchUserId(userName = userName)

            if not utils.isValidStr(userId):
                self.__timber.log('TriviaScoreCommand', f'Unable to find user ID for \"{userName}\" in the database')
                await self.__twitchUtils.safeSend(
                    messageable = ctx,
                    message = f'⚠ Unable to find trivia score info for \"{userName}\"',
                    replyMessageId = await ctx.getMessageId()
                )
                return

        shinyResult = await self.__shinyTriviaOccurencesRepository.fetchDetails(
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = userId
        )

        toxicResult = await self.__toxicTriviaOccurencesRepository.fetchDetails(
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = userId
        )

        triviaResult = await self.__triviaScoreRepository.fetchTriviaScore(
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = userId
        )

        message = await self.__triviaUtils.getTriviaScoreMessage(
            shinyResult = shinyResult,
            userName = userName,
            toxicResult = toxicResult,
            triviaResult = triviaResult
        )

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = message,
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('TriviaScoreCommand', f'Handled !triviascore command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
