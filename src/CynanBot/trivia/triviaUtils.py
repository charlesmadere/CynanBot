import locale
import traceback
from collections import defaultdict
from typing import Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.cuteness.cutenessResult import CutenessResult
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.banned.bannedTriviaGameController import \
    BannedTriviaGameController
from CynanBot.trivia.banned.bannedTriviaGameControllersRepositoryInterface import \
    BannedTriviaGameControllersRepositoryInterface
from CynanBot.trivia.gameController.triviaGameController import \
    TriviaGameController
from CynanBot.trivia.gameController.triviaGameControllersRepositoryInterface import \
    TriviaGameControllersRepositoryInterface
from CynanBot.trivia.gameController.triviaGameGlobalController import \
    TriviaGameGlobalController
from CynanBot.trivia.gameController.triviaGameGlobalControllersRepositoryInterface import \
    TriviaGameGlobalControllersRepositoryInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.specialStatus.shinyTriviaResult import ShinyTriviaResult
from CynanBot.trivia.specialStatus.specialTriviaStatus import \
    SpecialTriviaStatus
from CynanBot.trivia.specialStatus.toxicTriviaPunishmentResult import \
    ToxicTriviaPunishmentResult
from CynanBot.trivia.specialStatus.toxicTriviaResult import ToxicTriviaResult
from CynanBot.trivia.score.triviaScoreResult import TriviaScoreResult
from CynanBot.trivia.triviaUtilsInterface import TriviaUtilsInterface
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.users.exceptions import NoSuchUserException
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class TriviaUtils(TriviaUtilsInterface):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface,
        timber: TimberInterface,
        triviaGameControllersRepository: TriviaGameControllersRepositoryInterface,
        triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface):
            raise ValueError(f'bannedTriviaGameControllersRepository argument is malformed: \"{bannedTriviaGameControllersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface):
            raise ValueError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif not isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepositoryInterface):
            raise ValueError(f'triviaGameGlobalControllersRepository argument is malformed: \"{triviaGameGlobalControllersRepository}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface = bannedTriviaGameControllersRepository
        self.__timber: TimberInterface = timber
        self.__triviaGameControllersRepository: TriviaGameControllersRepositoryInterface = triviaGameControllersRepository
        self.__triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface = triviaGameGlobalControllersRepository
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def getClearedSuperTriviaQueueMessage(self, numberOfGamesRemoved: int) -> str:
        if not utils.isValidInt(numberOfGamesRemoved):
            raise ValueError(f'numberOfGamesRemoved argument is malformed: \"{numberOfGamesRemoved}\"')
        elif numberOfGamesRemoved < 0 or numberOfGamesRemoved > utils.getIntMaxSafeSize():
            raise ValueError(f'numberOfGamesRemoved argument is out of bounds: {numberOfGamesRemoved}')

        numberOfGamesRemovedStr = locale.format_string("%d", numberOfGamesRemoved, grouping = True)
        return f'ⓘ Cleared super trivia game queue ({numberOfGamesRemovedStr} game(s) removed).'

    async def getCorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        newCuteness: CutenessResult,
        emote: str,
        userNameThatRedeemed: str,
        twitchUser: UserInterface,
        specialTriviaStatus: Optional[SpecialTriviaStatus] = None,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not isinstance(newCuteness, CutenessResult):
            raise ValueError(f'newCuteness argument is malformed: \"{newCuteness}\"')
        elif not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise ValueError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt = emote
        if specialTriviaStatus is SpecialTriviaStatus.SHINY:
            emotePrompt = f'✨✨{emote}✨✨'
        elif specialTriviaStatus is SpecialTriviaStatus.TOXIC:
            emotePrompt = f'☠️☠️{emote}☠️☠️'

        prefix = f'{emotePrompt} Congratulations @{userNameThatRedeemed}, that\'s correct!'

        infix = ''
        if twitchUser.isCutenessEnabled():
            infix = f'Your new cuteness is {newCuteness.getCutenessStr()}.'

        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} 🎉 {infix} 🎉 The correct answer was: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} 🎉 {infix} 🎉 The correct answers were: {correctAnswersStr}'

    async def getIncorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        userNameThatRedeemed: str,
        specialTriviaStatus: Optional[SpecialTriviaStatus] = None,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise ValueError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt = emote
        if specialTriviaStatus is SpecialTriviaStatus.SHINY:
            emotePrompt = f'✨✨{emote}✨✨'
        elif specialTriviaStatus is SpecialTriviaStatus.TOXIC:
            emotePrompt = f'☠️☠️{emote}☠️☠️'

        prefix = f'{emotePrompt} Sorry @{userNameThatRedeemed}, that\'s incorrect. {utils.getRandomSadEmoji()}'
        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} The correct answer is: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} The correct answers are: {correctAnswersStr}'

    async def getInvalidAnswerInputPrompt(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        userNameThatRedeemed: str,
        specialTriviaStatus: Optional[SpecialTriviaStatus] = None
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise ValueError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')

        emotePrompt = emote
        if specialTriviaStatus is SpecialTriviaStatus.SHINY:
            emotePrompt = f'✨✨{emote}✨✨'
        elif specialTriviaStatus is SpecialTriviaStatus.TOXIC:
            emotePrompt = f'☠️☠️{emote}☠️☠️'

        prefix = f'{emotePrompt} Sorry @{userNameThatRedeemed}, that\'s an invalid input. {utils.getRandomSadEmoji()}'

        suffix = ''
        if question.getTriviaType() is TriviaQuestionType.MULTIPLE_CHOICE:
            suffix = 'Please answer using A, B, C, …'
        elif question.getTriviaType() is TriviaQuestionType.TRUE_FALSE:
            suffix = 'Please answer using either true or false.'
        else:
            suffix = 'Please check your answer and try again.'

        return f'{prefix} {suffix}'.strip()

    async def __getLongToxicTriviaPunishmentMessage(
        self,
        emotePrompt: str,
        toxicTriviaPunishmentResult: ToxicTriviaPunishmentResult,
        bucketDelimiter: str = '; ',
        delimiter: str = ', '
    ) -> str:
        if not utils.isValidStr(emotePrompt):
            raise ValueError(f'emotePrompt argument is malformed: \"{emotePrompt}\"')
        elif not isinstance(toxicTriviaPunishmentResult, ToxicTriviaPunishmentResult):
            raise ValueError(f'toxicTriviaPunishmentResult argument is malformed: \"{toxicTriviaPunishmentResult}\"')
        elif not isinstance(bucketDelimiter, str):
            raise ValueError(f'bucketDelimiter argument is malformed: \"{bucketDelimiter}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        punishmentAmountToUserNames: Dict[int, List[str]] = defaultdict(lambda: list())

        for punishment in toxicTriviaPunishmentResult.getToxicTriviaPunishments():
            punishmentAmountToUserNames[punishment.getPunishedByPoints()].append(punishment.getUserName())

        sortedKeys: List[int] = list(punishmentAmountToUserNames.keys())
        sortedKeys.sort(key = lambda punishmentAmount: punishmentAmount)

        buckets: List[str] = list()

        for punishmentAmount in sortedKeys:
            userNames: List[str] = list()

            for userName in punishmentAmountToUserNames[punishmentAmount]:
                userNames.append(userName)

            punishmentAmountString = locale.format_string("%d", abs(punishmentAmount), grouping = True)
            buckets.append(f'{delimiter.join(userNames)} punished by {punishmentAmountString} cuteness'.strip())

        punishmentTotal = f'{bucketDelimiter} for a total of {toxicTriviaPunishmentResult.getTotalPointsStolenStr()} cuteness stolen'.strip()
        return f'{emotePrompt} {bucketDelimiter.join(buckets)}{punishmentTotal}'.strip()

    async def getOutOfTimeAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        userNameThatRedeemed: str,
        specialTriviaStatus: Optional[SpecialTriviaStatus] = None,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise ValueError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt = emote
        if specialTriviaStatus is SpecialTriviaStatus.SHINY:
            emotePrompt = f'✨✨{emote}✨✨'
        elif specialTriviaStatus is SpecialTriviaStatus.TOXIC:
            emotePrompt = f'☠️☠️{emote}☠️☠️'

        prefix = f'{emotePrompt} Sorry @{userNameThatRedeemed}, you\'re out of time. {utils.getRandomSadEmoji()}'
        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} The correct answer is: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} The correct answers are: {correctAnswersStr}'

    async def __getShortToxicTriviaPunishmentMessage(
        self,
        emotePrompt: str,
        toxicTriviaPunishmentResult: ToxicTriviaPunishmentResult,
        delimiter: str = ', '
    ) -> str:
        if not utils.isValidStr(emotePrompt):
            raise ValueError(f'emotePrompt argument is malformed: \"{emotePrompt}\"')
        elif not isinstance(toxicTriviaPunishmentResult, ToxicTriviaPunishmentResult):
            raise ValueError(f'toxicTriviaPunishmentResult argument is malformed: \"{toxicTriviaPunishmentResult}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        punishmentAmountToUserNames: Dict[int, List[str]] = defaultdict(lambda: list())

        for punishment in toxicTriviaPunishmentResult.getToxicTriviaPunishments():
            punishmentAmountToUserNames[punishment.getPunishedByPoints()].append(punishment.getUserName())

        sortedKeys: List[int] = list(punishmentAmountToUserNames.keys())
        sortedKeys.sort(key = lambda punishmentAmount: punishmentAmount)

        buckets: List[str] = list()

        for punishmentAmount in sortedKeys:
            numberPunished = len(punishmentAmountToUserNames[punishmentAmount])
            punishmentAmountString = locale.format_string("%d", abs(punishmentAmount), grouping = True)

            if numberPunished == 1:
                buckets.append(f'1 person lost {punishmentAmountString} cuteness'.strip())
            else:
                buckets.append(f'{numberPunished} people lost {punishmentAmountString} cuteness'.strip())

        punishmentTotal = f'{delimiter} for a total of {toxicTriviaPunishmentResult.getTotalPointsStolenStr()} cuteness stolen'.strip()
        return f'{emotePrompt} {delimiter.join(buckets)}{punishmentTotal}'.strip()

    async def getSuperTriviaCorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        newCuteness: CutenessResult,
        points: int,
        emote: str,
        userName: str,
        twitchUser: UserInterface,
        specialTriviaStatus: Optional[SpecialTriviaStatus] = None,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not isinstance(newCuteness, CutenessResult):
            raise ValueError(f'newCuteness argument is malformed: \"{newCuteness}\"')
        elif not utils.isValidInt(points):
            raise ValueError(f'points argument is malformed: \"{points}\"')
        elif not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise ValueError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt = emote
        if specialTriviaStatus is SpecialTriviaStatus.SHINY:
            emotePrompt = f'✨✨{emote}✨✨'
        elif specialTriviaStatus is SpecialTriviaStatus.TOXIC:
            emotePrompt = f'☠️☠️{emote}☠️☠️'

        pointsStr = locale.format_string("%d", points, grouping = True)
        prefix = f'{emotePrompt} CONGRATULATIONS @{userName}, that\'s correct!'

        infix = ''
        if twitchUser.isCutenessEnabled():
            infix = f'You earned {pointsStr} cuteness, so your new cuteness is {newCuteness.getCutenessStr()}.'

        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} 🎉 {infix} 🎉 The correct answer was: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} 🎉 {infix} 🎉 The correct answers were: {correctAnswersStr}'

    async def getSuperTriviaLaunchpadPrompt(self, remainingQueueSize: int) -> Optional[str]:
        if not utils.isValidInt(remainingQueueSize):
            raise ValueError(f'remainingQueueSize argument is malformed: \"{remainingQueueSize}\"')

        if remainingQueueSize < 1:
            return None
        elif remainingQueueSize == 1:
            return f'One more super trivia game coming up!'
        else:
            remainingQueueSizeStr = locale.format_string("%d", remainingQueueSize, grouping = True)
            return f'{remainingQueueSizeStr} more super trivia games coming up!'

    async def getSuperTriviaOutOfTimeAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        specialTriviaStatus: Optional[SpecialTriviaStatus] = None,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise ValueError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt = emote
        if specialTriviaStatus is SpecialTriviaStatus.SHINY:
            emotePrompt = f'✨✨{emote}✨✨'
        elif specialTriviaStatus is SpecialTriviaStatus.TOXIC:
            emotePrompt = f'☠️☠️{emote}☠️☠️'

        prefix = f'{emotePrompt} Sorry everyone, y\'all are out of time… {utils.getRandomSadEmoji()} …'
        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} The correct answer is: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} The correct answers are: {correctAnswersStr}'

    async def getSuperTriviaGameQuestionPrompt(
        self,
        triviaQuestion: AbsTriviaQuestion,
        delaySeconds: int,
        points: int,
        emote: str,
        twitchUser: UserInterface,
        specialTriviaStatus: Optional[SpecialTriviaStatus] = None,
        delimiter: str = ' '
    ) -> str:
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise ValueError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not utils.isValidInt(delaySeconds):
            raise ValueError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif delaySeconds < 1 or delaySeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'delaySeconds argument is out of bounds: {delaySeconds}')
        elif not utils.isValidInt(points):
            raise ValueError(f'points argument is malformed: \"{points}\"')
        elif points < 1 or points > utils.getIntMaxSafeSize():
            raise ValueError(f'points argument is out of bounds: {points}')
        elif not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise ValueError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt = emote
        if specialTriviaStatus is SpecialTriviaStatus.SHINY:
            emotePrompt = f'✨✨{emote}✨✨'
        elif specialTriviaStatus is SpecialTriviaStatus.TOXIC:
            emotePrompt = f'☠️☠️{emote}☠️☠️'

        delaySecondsStr = locale.format_string("%d", delaySeconds, grouping = True)

        cutenessPrompt = ''
        if twitchUser.isCutenessEnabled():
            pointsStr = locale.format_string("%d", points, grouping = True)
            cutenessPrompt = f'for {pointsStr} cuteness '

        questionPrompt = ''
        if triviaQuestion.getTriviaType() is TriviaQuestionType.QUESTION_ANSWER and triviaQuestion.hasCategory():
            questionPrompt = f'— category is {triviaQuestion.getCategory()} — {triviaQuestion.getQuestion()}'
        else:
            questionPrompt = f'— {triviaQuestion.getPrompt(delimiter)}'

        return f'{emotePrompt} EVERYONE can play, !superanswer in {delaySecondsStr}s {cutenessPrompt}{questionPrompt}'

    async def getToxicTriviaPunishmentMessage(
        self,
        toxicTriviaPunishmentResult: Optional[ToxicTriviaPunishmentResult],
        emote: str,
        twitchUser: UserInterface,
        bucketDelimiter: str = '; ',
        delimiter: str = ', '
    ) -> Optional[str]:
        if toxicTriviaPunishmentResult is not None and not isinstance(toxicTriviaPunishmentResult, ToxicTriviaPunishmentResult):
            raise ValueError(f'toxicTriviaPunishmentResult argument is malformed: \"{toxicTriviaPunishmentResult}\"')
        elif not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not isinstance(bucketDelimiter, str):
            raise ValueError(f'bucketDelimiter argument is malformed: \"{bucketDelimiter}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if not twitchUser.isCutenessEnabled() or toxicTriviaPunishmentResult is None:
            return None

        emotePrompt = f'☠️☠️{emote}☠️☠️'

        if toxicTriviaPunishmentResult.getNumberOfToxicTriviaPunishments() >= 6:
            return await self.__getShortToxicTriviaPunishmentMessage(
                emotePrompt = emotePrompt,
                toxicTriviaPunishmentResult = toxicTriviaPunishmentResult,
                delimiter = delimiter
            )
        else:
            return await self.__getLongToxicTriviaPunishmentMessage(
                emotePrompt = emotePrompt,
                toxicTriviaPunishmentResult = toxicTriviaPunishmentResult,
                bucketDelimiter = bucketDelimiter,
                delimiter = delimiter
            )

    async def getTriviaGameBannedControllers(
        self,
        bannedControllers: Optional[List[BannedTriviaGameController]],
        delimiter: str = ', '
    ) -> str:
        if not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if not utils.hasItems(bannedControllers):
            return f'ⓘ There are no banned trivia game controllers.'

        bannedControllersNames: List[str] = list()
        for bannedController in bannedControllers:
            bannedControllersNames.append(bannedController.getUserName())

        bannedControllersStr = delimiter.join(bannedControllersNames)
        return f'ⓘ Banned trivia game controllers — {bannedControllersStr}'

    async def getTriviaGameControllers(
        self,
        gameControllers: Optional[List[TriviaGameController]],
        delimiter: str = ', '
    ) -> str:
        if not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if not utils.hasItems(gameControllers):
            return f'ⓘ Your channel has no trivia game controllers.'

        gameControllersNames: List[str] = list()
        for gameController in gameControllers:
            gameControllersNames.append(gameController.getUserName())

        gameControllersStr = delimiter.join(gameControllersNames)
        return f'ⓘ Your trivia game controllers — {gameControllersStr}'

    async def getTriviaGameGlobalControllers(
        self,
        gameControllers: Optional[List[TriviaGameGlobalController]],
        delimiter: str = ', '
    ) -> str:
        if not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if not utils.hasItems(gameControllers):
            return f'ⓘ There are no global trivia game controllers.'

        gameControllersNames: List[str] = list()
        for gameController in gameControllers:
            gameControllersNames.append(gameController.getUserName())

        gameControllersStr = delimiter.join(gameControllersNames)
        return f'ⓘ Global trivia game controllers — {gameControllersStr}'

    async def getTriviaGameQuestionPrompt(
        self,
        triviaQuestion: AbsTriviaQuestion,
        delaySeconds: int,
        points: int,
        emote: str,
        userNameThatRedeemed: str,
        twitchUser: UserInterface,
        specialTriviaStatus: Optional[SpecialTriviaStatus] = None,
        delimiter: str = ' '
    ) -> str:
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise ValueError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not utils.isValidInt(delaySeconds):
            raise ValueError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif delaySeconds < 1 or delaySeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'delaySeconds argument is out of bounds: {delaySeconds}')
        elif not utils.isValidInt(points):
            raise ValueError(f'points argument is malformed: \"{points}\"')
        elif points < 1 or points > utils.getIntMaxSafeSize():
            raise ValueError(f'points argument is out of bounds: {points}')
        elif not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise ValueError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt = emote
        if specialTriviaStatus is SpecialTriviaStatus.SHINY:
            emotePrompt = f'✨✨{emote}✨✨'
        elif specialTriviaStatus is SpecialTriviaStatus.TOXIC:
            emotePrompt = f'☠️☠️{emote}☠️☠️'

        delaySecondsStr = locale.format_string("%d", delaySeconds, grouping = True)

        cutenessPrompt = ''
        if twitchUser.isCutenessEnabled():
            pointsStr = locale.format_string("%d", points, grouping = True)
            cutenessPrompt = f'for {pointsStr} cuteness '

        questionPrompt = ''
        if triviaQuestion.getTriviaType() is TriviaQuestionType.QUESTION_ANSWER and triviaQuestion.hasCategory():
            questionPrompt = f'(category is \"{triviaQuestion.getCategory()}\") — {triviaQuestion.getQuestion()}'
        else:
            questionPrompt = f'— {triviaQuestion.getPrompt(delimiter)}'

        return f'{emotePrompt} @{userNameThatRedeemed} !answer in {delaySecondsStr}s {cutenessPrompt}{questionPrompt}'

    async def getTriviaScoreMessage(
        self,
        shinyResult: ShinyTriviaResult,
        userName: str,
        toxicResult: ToxicTriviaResult,
        triviaResult: TriviaScoreResult
    ) -> str:
        if not isinstance(shinyResult, ShinyTriviaResult):
            raise ValueError(f'shinyResult argument is malformed: \"{shinyResult}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif not isinstance(toxicResult, ToxicTriviaResult):
            raise ValueError(f'toxicResult argument is malformed: \"{toxicResult}\"')
        elif not isinstance(triviaResult, TriviaScoreResult):
            raise ValueError(f'triviaResult argument is malformed: \"{triviaResult}\"')

        triviaStr = ''
        if triviaResult.getTotal() >= 1:
            winLossStr = f'{triviaResult.getTriviaWinsStr()}-{triviaResult.getTriviaLossesStr()}'
            winsRatioStr = f'{triviaResult.getWinPercentStr()} wins'

            if triviaResult.getTotal() == 1:
                triviaStr = f'@{userName} has played {triviaResult.getTotalStr()} trivia game ({winLossStr}, {winsRatioStr})'
            else:
                triviaStr = f'@{userName} has played {triviaResult.getTotalStr()} trivia games ({winLossStr}, {winsRatioStr})'

            if triviaResult.getStreak() >= 3:
                triviaStr = f'{triviaStr}, and is on a {triviaResult.getAbsStreakStr()} game winning streak 😸'
            elif triviaResult.getStreak() <= -3:
                triviaStr = f'{triviaStr}, and is on a {triviaResult.getAbsStreakStr()} game losing streak 🙀'
        else:
            triviaStr = f'@{userName} hasn\'t played any trivia games 😿'

        superTriviaStr = ''
        if triviaResult.getSuperTriviaWins() >= 1:
            if triviaResult.getSuperTriviaWins() == 1:
                superTriviaStr = f'; {triviaResult.getSuperTriviaWinsStr()} super trivia win'
            else:
                superTriviaStr = f'; {triviaResult.getSuperTriviaWinsStr()} super trivia wins'

        shinyStr = ''
        if shinyResult.getNewShinyCount() >= 1:
            if shinyResult.getNewShinyCount() == 1:
                shinyStr = f'; {shinyResult.getNewShinyCountStr()} shiny'
            else:
                shinyStr = f'; {shinyResult.getNewShinyCountStr()} shinies'

        toxicStr = ''
        if toxicResult.getNewToxicCount() >= 1:
            if toxicResult.getNewToxicCount() == 1:
                toxicStr = f'; {toxicResult.getNewToxicCountStr()} toxic'
            else:
                toxicStr = f'; {toxicResult.getNewToxicCountStr()} toxics'

        return f'{triviaStr}{superTriviaStr}{shinyStr}{toxicStr}'.strip()

    async def isPrivilegedTriviaUser(self, twitchChannel: str, userId: str) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        twitchUser: Optional[UserInterface] = None

        try:
            twitchUser = await self.__usersRepository.getUserAsync(twitchChannel)
        except NoSuchUserException as e:
            # this exception should be impossible here, but let's just be safe
            self.__timber.log('TriviaUtils', f'Encountered an invalid Twitch user \"{twitchChannel}\" when trying to check userId \"{userId}\" for privileged trivia permissions', e, traceback.format_exc())

        if twitchUser is None:
            self.__timber.log('TriviaUtils', f'No Twitch user instance available for \"{twitchChannel}\" when trying to check userId \"{userId}\" for privileged trivia permissions')
            return False

        bannedGameControllers = await self.__bannedTriviaGameControllersRepository.getBannedControllers()
        for bannedGameController in bannedGameControllers:
            if userId == bannedGameController.getUserId():
                return False

        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(twitchUser.getHandle())

        twitchUserId = await self.__userIdsRepository.fetchUserId(
            userName = twitchUser.getHandle(),
            twitchAccessToken = twitchAccessToken
        )

        if utils.isValidStr(twitchUserId) and userId == twitchUserId:
            return True

        gameControllers = await self.__triviaGameControllersRepository.getControllers(twitchUser.getHandle())
        for gameController in gameControllers:
            if userId == gameController.getUserId():
                return True

        globalGameControllers = await self.__triviaGameGlobalControllersRepository.getControllers()
        for globalGameController in globalGameControllers:
            if userId == globalGameController.getUserId():
                return True

        administratorUserId = await self.__administratorProvider.getAdministratorUserId()

        return userId == administratorUserId
