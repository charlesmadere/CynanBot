from .triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from .triviaGameBuilderSettingsInterface import \
    TriviaGameBuilderSettingsInterface
from ..actions.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from ..actions.startNewTriviaGameAction import StartNewTriviaGameAction
from ..questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions
from ..questions.triviaSource import TriviaSource
from ..triviaFetchOptions import TriviaFetchOptions
from ..triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ...misc import utils as utils
from ...users.usersRepositoryInterface import UsersRepositoryInterface


class TriviaGameBuilder(TriviaGameBuilderInterface):

    def __init__(
        self,
        triviaGameBuilderSettings: TriviaGameBuilderSettingsInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(triviaGameBuilderSettings, TriviaGameBuilderSettingsInterface):
            raise TypeError(f'triviaGameBuilderSettings argument is malformed: \"{triviaGameBuilderSettings}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__triviaGameBuilderSettings: TriviaGameBuilderSettingsInterface = triviaGameBuilderSettings
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def createNewTriviaGame(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str
    ) -> StartNewTriviaGameAction | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        if not await self.__triviaGameBuilderSettings.isTriviaGameEnabled():
            return None

        user = await self.__usersRepository.getUserAsync(twitchChannel)

        if not user.isTriviaGameEnabled():
            return None

        isShinyTriviaEnabled = user.isShinyTriviaEnabled() and user.isCutenessEnabled()

        points = user.getTriviaGamePoints()
        if not utils.isValidInt(points):
            points = await self.__triviaGameBuilderSettings.getTriviaGamePoints()

        secondsToLive = user.getWaitForTriviaAnswerDelay()
        if not utils.isValidInt(secondsToLive):
            secondsToLive = await self.__triviaGameBuilderSettings.getWaitForTriviaAnswerDelay()

        shinyMultiplier = user.getTriviaGameShinyMultiplier()
        if not utils.isValidInt(shinyMultiplier):
            shinyMultiplier = await self.__triviaGameBuilderSettings.getTriviaGameShinyMultiplier()

        actionId = await self.__triviaIdGenerator.generateActionId()

        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId,
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED
        )

        return StartNewTriviaGameAction(
            isShinyTriviaEnabled = isShinyTriviaEnabled,
            pointsForWinning = points,
            secondsToLive = secondsToLive,
            shinyMultiplier = shinyMultiplier,
            actionId = actionId,
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId,
            userId = userId,
            userName = userName,
            triviaFetchOptions = triviaFetchOptions
        )

    async def createNewSuperTriviaGame(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        numberOfGames: int = 1,
        requiredTriviaSource: TriviaSource | None = None
    ) -> StartNewSuperTriviaGameAction | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidInt(numberOfGames):
            raise TypeError(f'numberOfGames argument is malformed: \"{numberOfGames}\"')
        elif numberOfGames < 1 or numberOfGames > utils.getIntMaxSafeSize():
            raise ValueError(f'numberOfGames argument is out of bounds: {numberOfGames}')

        if not await self.__triviaGameBuilderSettings.isSuperTriviaGameEnabled():
            return None

        user = await self.__usersRepository.getUserAsync(twitchChannel)

        if not user.isSuperTriviaGameEnabled():
            return None

        isShinyTriviaEnabled = user.isShinyTriviaEnabled and user.isCutenessEnabled()
        isToxicTriviaEnabled = user.isToxicTriviaEnabled and user.isCutenessEnabled()

        perUserAttempts = user.getSuperTriviaPerUserAttempts()
        if not utils.isValidInt(perUserAttempts):
            perUserAttempts = await self.__triviaGameBuilderSettings.getSuperTriviaGamePerUserAttempts()

        pointsForWinning = user.getSuperTriviaGamePoints()
        if not utils.isValidInt(pointsForWinning):
            pointsForWinning = await self.__triviaGameBuilderSettings.getSuperTriviaGamePoints()

        regularTriviaPointsForWinning = user.getTriviaGamePoints()
        if not utils.isValidInt(regularTriviaPointsForWinning):
            regularTriviaPointsForWinning = await self.__triviaGameBuilderSettings.getTriviaGamePoints()

        secondsToLive = user.getWaitForSuperTriviaAnswerDelay()
        if not utils.isValidInt(secondsToLive):
            secondsToLive = await self.__triviaGameBuilderSettings.getWaitForSuperTriviaAnswerDelay()

        shinyMultiplier = user.getSuperTriviaGameShinyMultiplier()
        if not utils.isValidInt(shinyMultiplier):
            shinyMultiplier = await self.__triviaGameBuilderSettings.getSuperTriviaGameShinyMultiplier()

        toxicMultiplier = user.getSuperTriviaGameToxicMultiplier()
        if not utils.isValidInt(toxicMultiplier):
            toxicMultiplier = await self.__triviaGameBuilderSettings.getSuperTriviaGameToxicMultiplier()

        toxicTriviaPunishmentMultiplier = user.getSuperTriviaGameToxicPunishmentMultiplier()
        if not utils.isValidInt(toxicTriviaPunishmentMultiplier):
            toxicTriviaPunishmentMultiplier = await self.__triviaGameBuilderSettings.getSuperTriviaGameToxicPunishmentMultiplier()

        actionId = await self.__triviaIdGenerator.generateActionId()

        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId,
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED,
            requiredTriviaSource = requiredTriviaSource
        )

        return StartNewSuperTriviaGameAction(
            isQueueActionConsumed = False,
            isShinyTriviaEnabled = isShinyTriviaEnabled,
            isToxicTriviaEnabled = isToxicTriviaEnabled,
            numberOfGames = numberOfGames,
            perUserAttempts = perUserAttempts,
            pointsForWinning = pointsForWinning,
            regularTriviaPointsForWinning = regularTriviaPointsForWinning,
            secondsToLive = secondsToLive,
            shinyMultiplier = shinyMultiplier,
            toxicMultiplier = toxicMultiplier,
            toxicTriviaPunishmentMultiplier = toxicTriviaPunishmentMultiplier,
            actionId = actionId,
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId,
            triviaFetchOptions = triviaFetchOptions
        )
