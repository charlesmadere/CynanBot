from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.trivia.actions.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from CynanBot.trivia.actions.startNewTriviaGameAction import \
    StartNewTriviaGameAction
from CynanBot.trivia.builder.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBot.trivia.builder.triviaGameBuilderSettingsInterface import \
    TriviaGameBuilderSettingsInterface
from CynanBot.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class TriviaGameBuilder(TriviaGameBuilderInterface):

    def __init__(
        self,
        triviaGameBuilderSettings: TriviaGameBuilderSettingsInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert isinstance(triviaGameBuilderSettings, TriviaGameBuilderSettingsInterface), f"malformed {triviaGameBuilderSettings=}"
        assert isinstance(triviaIdGenerator, TriviaIdGeneratorInterface), f"malformed {triviaIdGenerator=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

        self.__triviaGameBuilderSettings: TriviaGameBuilderSettingsInterface = triviaGameBuilderSettings
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def createNewTriviaGame(
        self,
        twitchChannel: str,
        userId: str,
        userName: str
    ) -> Optional[StartNewTriviaGameAction]:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        if not utils.isValidStr(userName):
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
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED
        )

        return StartNewTriviaGameAction(
            isShinyTriviaEnabled = isShinyTriviaEnabled,
            pointsForWinning = points,
            secondsToLive = secondsToLive,
            shinyMultiplier = shinyMultiplier,
            actionId = actionId,
            twitchChannel = user.getHandle(),
            userId = userId,
            userName = userName,
            triviaFetchOptions = triviaFetchOptions
        )

    async def createNewSuperTriviaGame(
        self,
        twitchChannel: str,
        numberOfGames: int = 1
    ) -> Optional[StartNewSuperTriviaGameAction]:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidInt(numberOfGames):
            raise TypeError(f'numberOfGames argument is malformed: \"{numberOfGames}\"')
        if numberOfGames < 1 or numberOfGames > utils.getIntMaxSafeSize():
            raise ValueError(f'numberOfGames argument is out of bounds: {numberOfGames}')

        if not await self.__triviaGameBuilderSettings.isSuperTriviaGameEnabled():
            return None

        user = await self.__usersRepository.getUserAsync(twitchChannel)

        if not user.isSuperTriviaGameEnabled():
            return None

        isShinyTriviaEnabled = user.isShinyTriviaEnabled() and user.isCutenessEnabled()
        isToxicTriviaEnabled = user.isToxicTriviaEnabled() and user.isCutenessEnabled()

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
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
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
            triviaFetchOptions = triviaFetchOptions
        )
