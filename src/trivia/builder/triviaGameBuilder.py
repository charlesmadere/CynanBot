from typing import Final

from .triviaGameBuilderInterface import TriviaGameBuilderInterface
from .triviaGameBuilderSettingsInterface import TriviaGameBuilderSettingsInterface
from ..actions.startNewSuperTriviaGameAction import StartNewSuperTriviaGameAction
from ..actions.startNewTriviaGameAction import StartNewTriviaGameAction
from ..questionAnswerTriviaConditions import QuestionAnswerTriviaConditions
from ..questions.triviaSource import TriviaSource
from ..triviaFetchOptions import TriviaFetchOptions
from ..triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ...misc import utils as utils
from ...users.userInterface import UserInterface


class TriviaGameBuilder(TriviaGameBuilderInterface):

    def __init__(
        self,
        triviaGameBuilderSettings: TriviaGameBuilderSettingsInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
    ):
        if not isinstance(triviaGameBuilderSettings, TriviaGameBuilderSettingsInterface):
            raise TypeError(f'triviaGameBuilderSettings argument is malformed: \"{triviaGameBuilderSettings}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')

        self.__triviaGameBuilderSettings: Final[TriviaGameBuilderSettingsInterface] = triviaGameBuilderSettings
        self.__triviaIdGenerator: Final[TriviaIdGeneratorInterface] = triviaIdGenerator

    async def createNewTriviaGame(
        self,
        chatterUserId: str,
        chatterUserLogin: str,
        chatterUserName: str,
        twitchChannelId: str,
        twitchUser: UserInterface,
    ) -> StartNewTriviaGameAction | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(chatterUserLogin):
            raise TypeError(f'chatterUserLogin argument is malformed: \"{chatterUserLogin}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise TypeError(f'twitchUser argument is malformed: \"{twitchUser}\"')

        if not await self.__triviaGameBuilderSettings.isTriviaGameEnabled():
            return None
        elif not twitchUser.isTriviaGameEnabled:
            return None

        isShinyTriviaEnabled = twitchUser.isShinyTriviaEnabled and twitchUser.isCutenessEnabled

        pointsForWinning = twitchUser.triviaGamePoints
        if not utils.isValidInt(pointsForWinning):
            pointsForWinning = await self.__triviaGameBuilderSettings.getTriviaGamePoints()

        secondsToLive = twitchUser.waitForTriviaAnswerDelay
        if not utils.isValidInt(secondsToLive):
            secondsToLive = await self.__triviaGameBuilderSettings.getWaitForTriviaAnswerDelay()

        shinyMultiplier = twitchUser.triviaGameShinyMultiplier
        if not utils.isValidInt(shinyMultiplier):
            shinyMultiplier = await self.__triviaGameBuilderSettings.getTriviaGameShinyMultiplier()

        actionId = await self.__triviaIdGenerator.generateActionId()

        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = twitchUser.handle,
            twitchChannelId = twitchChannelId,
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED,
        )

        return StartNewTriviaGameAction(
            isShinyTriviaEnabled = isShinyTriviaEnabled,
            pointsForWinning = pointsForWinning,
            secondsToLive = secondsToLive,
            shinyMultiplier = shinyMultiplier,
            actionId = actionId,
            twitchChannel = twitchUser.handle,
            twitchChannelId = twitchChannelId,
            userId = chatterUserId,
            userName = chatterUserName,
            triviaFetchOptions = triviaFetchOptions,
        )

    async def createNewSuperTriviaGame(
        self,
        twitchChannelId: str,
        twitchUser: UserInterface,
        numberOfGames: int = 1,
        requiredTriviaSource: TriviaSource | None = None,
    ) -> StartNewSuperTriviaGameAction | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise TypeError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidInt(numberOfGames):
            raise TypeError(f'numberOfGames argument is malformed: \"{numberOfGames}\"')
        elif numberOfGames < 1 or numberOfGames > utils.getIntMaxSafeSize():
            raise ValueError(f'numberOfGames argument is out of bounds: {numberOfGames}')

        if not await self.__triviaGameBuilderSettings.isSuperTriviaGameEnabled():
            return None
        elif not twitchUser.isSuperTriviaGameEnabled:
            return None

        isShinyTriviaEnabled = twitchUser.isShinyTriviaEnabled and twitchUser.isCutenessEnabled
        isToxicTriviaEnabled = twitchUser.isToxicTriviaEnabled and twitchUser.isCutenessEnabled

        perUserAttempts = twitchUser.superTriviaPerUserAttempts
        if not utils.isValidInt(perUserAttempts):
            perUserAttempts = await self.__triviaGameBuilderSettings.getSuperTriviaGamePerUserAttempts()

        pointsForWinning = twitchUser.superTriviaGamePoints
        if not utils.isValidInt(pointsForWinning):
            pointsForWinning = await self.__triviaGameBuilderSettings.getSuperTriviaGamePoints()

        regularTriviaPointsForWinning = twitchUser.triviaGamePoints
        if not utils.isValidInt(regularTriviaPointsForWinning):
            regularTriviaPointsForWinning = await self.__triviaGameBuilderSettings.getTriviaGamePoints()

        secondsToLive = twitchUser.waitForSuperTriviaAnswerDelay
        if not utils.isValidInt(secondsToLive):
            secondsToLive = await self.__triviaGameBuilderSettings.getWaitForSuperTriviaAnswerDelay()

        shinyMultiplier = twitchUser.superTriviaGameShinyMultiplier
        if not utils.isValidInt(shinyMultiplier):
            shinyMultiplier = await self.__triviaGameBuilderSettings.getSuperTriviaGameShinyMultiplier()

        toxicMultiplier = twitchUser.superTriviaGameToxicMultiplier
        if not utils.isValidInt(toxicMultiplier):
            toxicMultiplier = await self.__triviaGameBuilderSettings.getSuperTriviaGameToxicMultiplier()

        toxicTriviaPunishmentMultiplier = twitchUser.superTriviaGameToxicPunishmentMultiplier
        if not utils.isValidInt(toxicTriviaPunishmentMultiplier):
            toxicTriviaPunishmentMultiplier = await self.__triviaGameBuilderSettings.getSuperTriviaGameToxicPunishmentMultiplier()

        actionId = await self.__triviaIdGenerator.generateActionId()

        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = twitchUser.handle,
            twitchChannelId = twitchChannelId,
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED,
            requiredTriviaSource = requiredTriviaSource,
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
            twitchChannel = twitchUser.handle,
            twitchChannelId = twitchChannelId,
            triviaFetchOptions = triviaFetchOptions,
        )
