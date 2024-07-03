import locale
import traceback
from collections import defaultdict

from ..cuteness.cutenessResult import CutenessResult
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from .banned.bannedTriviaGameController import BannedTriviaGameController
from .banned.bannedTriviaGameControllersRepositoryInterface import \
    BannedTriviaGameControllersRepositoryInterface
from .gameController.triviaGameController import TriviaGameController
from .gameController.triviaGameControllersRepositoryInterface import \
    TriviaGameControllersRepositoryInterface
from .gameController.triviaGameGlobalController import \
    TriviaGameGlobalController
from .gameController.triviaGameGlobalControllersRepositoryInterface import \
    TriviaGameGlobalControllersRepositoryInterface
from .questions.absTriviaQuestion import AbsTriviaQuestion
from .questions.triviaQuestionType import TriviaQuestionType
from .score.triviaScoreResult import TriviaScoreResult
from .specialStatus.shinyTriviaResult import ShinyTriviaResult
from .specialStatus.specialTriviaStatus import SpecialTriviaStatus
from .specialStatus.toxicTriviaPunishmentResult import \
    ToxicTriviaPunishmentResult
from .specialStatus.toxicTriviaResult import ToxicTriviaResult
from .triviaQuestionPresenterInterface import \
    TriviaQuestionPresenterInterface
from .triviaUtilsInterface import TriviaUtilsInterface
from ..twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from ..users.exceptions import NoSuchUserException
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.userInterface import UserInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface
from ..misc import utils as utils


class TriviaUtils(TriviaUtilsInterface):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface,
        timber: TimberInterface,
        triviaGameControllersRepository: TriviaGameControllersRepositoryInterface,
        triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface,
        triviaQuestionPresenter: TriviaQuestionPresenterInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface):
            raise TypeError(f'bannedTriviaGameControllersRepository argument is malformed: \"{bannedTriviaGameControllersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface):
            raise TypeError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif not isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepositoryInterface):
            raise TypeError(f'triviaGameGlobalControllersRepository argument is malformed: \"{triviaGameGlobalControllersRepository}\"')
        elif not isinstance(triviaQuestionPresenter, TriviaQuestionPresenterInterface):
            raise TypeError(f'triviaQuestionPresenter argument is malformed: \"{triviaQuestionPresenter}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface = bannedTriviaGameControllersRepository
        self.__timber: TimberInterface = timber
        self.__triviaGameControllersRepository: TriviaGameControllersRepositoryInterface = triviaGameControllersRepository
        self.__triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface = triviaGameGlobalControllersRepository
        self.__triviaQuestionPresenter: TriviaQuestionPresenterInterface = triviaQuestionPresenter
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def getClearedSuperTriviaQueueMessage(self, numberOfGamesRemoved: int) -> str:
        if not utils.isValidInt(numberOfGamesRemoved):
            raise TypeError(f'numberOfGamesRemoved argument is malformed: \"{numberOfGamesRemoved}\"')
        elif numberOfGamesRemoved < 0 or numberOfGamesRemoved > utils.getIntMaxSafeSize():
            raise ValueError(f'numberOfGamesRemoved argument is out of bounds: {numberOfGamesRemoved}')

        numberOfGamesRemovedStr = locale.format_string("%d", numberOfGamesRemoved, grouping = True)
        return f'ⓘ Cleared super trivia game queue — {numberOfGamesRemovedStr} game(s) removed'

    async def getCorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        newCuteness: CutenessResult,
        emote: str,
        userNameThatRedeemed: str,
        twitchUser: UserInterface,
        specialTriviaStatus: SpecialTriviaStatus | None = None,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not isinstance(newCuteness, CutenessResult):
            raise TypeError(f'newCuteness argument is malformed: \"{newCuteness}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise TypeError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise TypeError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise TypeError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt = emote
        if specialTriviaStatus is SpecialTriviaStatus.SHINY:
            emotePrompt = f'✨✨{emote}✨✨'
        elif specialTriviaStatus is SpecialTriviaStatus.TOXIC:
            emotePrompt = f'☠️☠️{emote}☠️☠️'

        prefix = f'{emotePrompt} Congratulations @{userNameThatRedeemed}, that\'s correct!'

        infix = ''
        if twitchUser.isCutenessEnabled():
            infix = f'Your new cuteness is {newCuteness.cutenessStr}.'

        correctAnswers = await self.__triviaQuestionPresenter.getCorrectAnswers(
            triviaQuestion = question,
            delimiter = delimiter
        )

        return f'{prefix} 🎉 {infix} 🎉 {correctAnswers}'.strip()

    async def getIncorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        userNameThatRedeemed: str,
        specialTriviaStatus: SpecialTriviaStatus | None = None,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise TypeError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise TypeError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt = emote
        if specialTriviaStatus is SpecialTriviaStatus.SHINY:
            emotePrompt = f'✨✨{emote}✨✨'
        elif specialTriviaStatus is SpecialTriviaStatus.TOXIC:
            emotePrompt = f'☠️☠️{emote}☠️☠️'

        prefix = f'{emotePrompt} Sorry @{userNameThatRedeemed}, that\'s incorrect. {utils.getRandomSadEmoji()}'

        correctAnswers = await self.__triviaQuestionPresenter.getCorrectAnswers(
            triviaQuestion = question,
            delimiter = delimiter
        )

        return f'{prefix} {correctAnswers}'.strip()

    async def getInvalidAnswerInputPrompt(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        userNameThatRedeemed: str,
        specialTriviaStatus: SpecialTriviaStatus | None = None
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise TypeError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise TypeError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')

        emotePrompt = emote
        if specialTriviaStatus is SpecialTriviaStatus.SHINY:
            emotePrompt = f'✨✨{emote}✨✨'
        elif specialTriviaStatus is SpecialTriviaStatus.TOXIC:
            emotePrompt = f'☠️☠️{emote}☠️☠️'

        prefix = f'{emotePrompt} Sorry @{userNameThatRedeemed}, that\'s an invalid input. {utils.getRandomSadEmoji()}'

        suffix = ''
        if question.triviaType is TriviaQuestionType.MULTIPLE_CHOICE:
            suffix = 'Please answer using A, B, C, …'
        elif question.triviaType is TriviaQuestionType.TRUE_FALSE:
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
            raise TypeError(f'emotePrompt argument is malformed: \"{emotePrompt}\"')
        elif not isinstance(toxicTriviaPunishmentResult, ToxicTriviaPunishmentResult):
            raise TypeError(f'toxicTriviaPunishmentResult argument is malformed: \"{toxicTriviaPunishmentResult}\"')
        elif not isinstance(bucketDelimiter, str):
            raise TypeError(f'bucketDelimiter argument is malformed: \"{bucketDelimiter}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        punishmentAmountToUserNames: dict[int, list[str]] = defaultdict(lambda: list())

        for punishment in toxicTriviaPunishmentResult.toxicTriviaPunishments:
            punishmentAmountToUserNames[punishment.punishedByPoints].append(punishment.userName)

        sortedKeys: list[int] = list(punishmentAmountToUserNames.keys())
        sortedKeys.sort(key = lambda punishmentAmount: punishmentAmount)

        buckets: list[str] = list()

        for punishmentAmount in sortedKeys:
            userNames: list[str] = list()

            for userName in punishmentAmountToUserNames[punishmentAmount]:
                userNames.append(userName)

            punishmentAmountString = locale.format_string("%d", abs(punishmentAmount), grouping = True)
            buckets.append(f'{delimiter.join(userNames)} punished by {punishmentAmountString} cuteness'.strip())

        punishmentTotal = f'{bucketDelimiter} for a total of {toxicTriviaPunishmentResult.totalPointsStolenStr} cuteness stolen'.strip()
        return f'{emotePrompt} {bucketDelimiter.join(buckets)}{punishmentTotal}'.strip()

    async def getOutOfTimeAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        userNameThatRedeemed: str,
        specialTriviaStatus: SpecialTriviaStatus | None = None,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise TypeError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise TypeError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt = emote
        if specialTriviaStatus is SpecialTriviaStatus.SHINY:
            emotePrompt = f'✨✨{emote}✨✨'
        elif specialTriviaStatus is SpecialTriviaStatus.TOXIC:
            emotePrompt = f'☠️☠️{emote}☠️☠️'

        prefix = f'{emotePrompt} Sorry @{userNameThatRedeemed}, you\'re out of time. {utils.getRandomSadEmoji()}'

        correctAnswers = await self.__triviaQuestionPresenter.getCorrectAnswers(
            triviaQuestion = question,
            delimiter = delimiter
        )

        return f'{prefix} {correctAnswers}'.strip()

    async def __getShortToxicTriviaPunishmentMessage(
        self,
        emotePrompt: str,
        toxicTriviaPunishmentResult: ToxicTriviaPunishmentResult,
        delimiter: str = ', '
    ) -> str:
        if not utils.isValidStr(emotePrompt):
            raise TypeError(f'emotePrompt argument is malformed: \"{emotePrompt}\"')
        elif not isinstance(toxicTriviaPunishmentResult, ToxicTriviaPunishmentResult):
            raise TypeError(f'toxicTriviaPunishmentResult argument is malformed: \"{toxicTriviaPunishmentResult}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        punishmentAmountToUserNames: dict[int, list[str]] = defaultdict(lambda: list())

        for punishment in toxicTriviaPunishmentResult.toxicTriviaPunishments:
            punishmentAmountToUserNames[punishment.punishedByPoints].append(punishment.userName)

        sortedKeys: list[int] = list(punishmentAmountToUserNames.keys())
        sortedKeys.sort(key = lambda punishmentAmount: punishmentAmount)

        buckets: list[str] = list()

        for punishmentAmount in sortedKeys:
            numberPunished = len(punishmentAmountToUserNames[punishmentAmount])
            punishmentAmountString = locale.format_string("%d", abs(punishmentAmount), grouping = True)

            if numberPunished == 1:
                buckets.append(f'1 person lost {punishmentAmountString} cuteness'.strip())
            else:
                buckets.append(f'{numberPunished} people lost {punishmentAmountString} cuteness'.strip())

        punishmentTotal = f'{delimiter} for a total of {toxicTriviaPunishmentResult.totalPointsStolenStr} cuteness stolen'.strip()
        return f'{emotePrompt} {delimiter.join(buckets)}{punishmentTotal}'.strip()

    async def getSuperTriviaCorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        newCuteness: CutenessResult,
        points: int,
        emote: str,
        userName: str,
        twitchUser: UserInterface,
        specialTriviaStatus: SpecialTriviaStatus | None = None,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not isinstance(newCuteness, CutenessResult):
            raise TypeError(f'newCuteness argument is malformed: \"{newCuteness}\"')
        elif not utils.isValidInt(points):
            raise TypeError(f'points argument is malformed: \"{points}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise TypeError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise TypeError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt = emote
        if specialTriviaStatus is SpecialTriviaStatus.SHINY:
            emotePrompt = f'✨✨{emote}✨✨'
        elif specialTriviaStatus is SpecialTriviaStatus.TOXIC:
            emotePrompt = f'☠️☠️{emote}☠️☠️'

        pointsStr = locale.format_string("%d", points, grouping = True)
        prefix = f'{emotePrompt} CONGRATULATIONS @{userName}, that\'s correct!'

        infix = ''
        if twitchUser.isCutenessEnabled():
            infix = f'You earned {pointsStr} cuteness, so your new cuteness is {newCuteness.cutenessStr}.'

        correctAnswers = await self.__triviaQuestionPresenter.getCorrectAnswers(
            triviaQuestion = question,
            delimiter = delimiter
        )

        return f'{prefix} 🎉 {infix} 🎉 {correctAnswers}'.strip()

    async def getSuperTriviaLaunchpadPrompt(self, remainingQueueSize: int) -> str | None:
        if not utils.isValidInt(remainingQueueSize):
            raise TypeError(f'remainingQueueSize argument is malformed: \"{remainingQueueSize}\"')

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
        specialTriviaStatus: SpecialTriviaStatus | None = None,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise TypeError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt = emote
        if specialTriviaStatus is SpecialTriviaStatus.SHINY:
            emotePrompt = f'✨✨{emote}✨✨'
        elif specialTriviaStatus is SpecialTriviaStatus.TOXIC:
            emotePrompt = f'☠️☠️{emote}☠️☠️'

        prefix = f'{emotePrompt} Sorry everyone, y\'all are out of time… {utils.getRandomSadEmoji()}'

        correctAnswers = await self.__triviaQuestionPresenter.getCorrectAnswers(
            triviaQuestion = question,
            delimiter = delimiter
        )

        return f'{prefix} {correctAnswers}'.strip()

    async def getSuperTriviaGameQuestionPrompt(
        self,
        triviaQuestion: AbsTriviaQuestion,
        delaySeconds: int,
        points: int,
        emote: str,
        twitchUser: UserInterface,
        specialTriviaStatus: SpecialTriviaStatus | None = None,
        delimiter: str = ' '
    ) -> str:
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not utils.isValidInt(delaySeconds):
            raise TypeError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif delaySeconds < 1 or delaySeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'delaySeconds argument is out of bounds: {delaySeconds}')
        elif not utils.isValidInt(points):
            raise TypeError(f'points argument is malformed: \"{points}\"')
        elif points < 1 or points > utils.getIntMaxSafeSize():
            raise ValueError(f'points argument is out of bounds: {points}')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise TypeError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise TypeError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

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

        questionPrompt = await self.__triviaQuestionPresenter.getPrompt(
            triviaQuestion = triviaQuestion,
            delimiter = delimiter
        )

        return f'{emotePrompt} EVERYONE can play, !superanswer in {delaySecondsStr}s {cutenessPrompt} {questionPrompt}'.strip()

    async def getToxicTriviaPunishmentMessage(
        self,
        toxicTriviaPunishmentResult: ToxicTriviaPunishmentResult | None,
        emote: str,
        twitchUser: UserInterface,
        bucketDelimiter: str = '; ',
        delimiter: str = ', '
    ) -> str | None:
        if toxicTriviaPunishmentResult is not None and not isinstance(toxicTriviaPunishmentResult, ToxicTriviaPunishmentResult):
            raise TypeError(f'toxicTriviaPunishmentResult argument is malformed: \"{toxicTriviaPunishmentResult}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise TypeError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not isinstance(bucketDelimiter, str):
            raise TypeError(f'bucketDelimiter argument is malformed: \"{bucketDelimiter}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        if not twitchUser.isCutenessEnabled() or toxicTriviaPunishmentResult is None:
            return None

        emotePrompt = f'☠️☠️{emote}☠️☠️'

        if toxicTriviaPunishmentResult.numberOfToxicTriviaPunishments >= 6:
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
        bannedControllers: list[BannedTriviaGameController] | None,
        delimiter: str = ', '
    ) -> str:
        if bannedControllers is not None and not isinstance(bannedControllers, list):
            raise TypeError(f'bannedControllers argument is malformed: \"{bannedControllers}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        if bannedControllers is None or len(bannedControllers) == 0:
            return f'ⓘ There are no banned trivia game controllers.'

        bannedControllersNames: list[str] = list()
        for bannedController in bannedControllers:
            bannedControllersNames.append(bannedController.userName)

        bannedControllersStr = delimiter.join(bannedControllersNames)
        return f'ⓘ Banned trivia game controllers — {bannedControllersStr}'

    async def getTriviaGameControllers(
        self,
        gameControllers: list[TriviaGameController] | None,
        delimiter: str = ', '
    ) -> str:
        if gameControllers is not None and not isinstance(gameControllers, list):
            raise TypeError(f'gameControllers argument is malformed: \"{gameControllers}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        if gameControllers is None or len(gameControllers) == 0:
            return f'ⓘ Your channel has no trivia game controllers.'

        gameControllersNames: list[str] = list()
        for gameController in gameControllers:
            gameControllersNames.append(gameController.userName)

        gameControllersStr = delimiter.join(gameControllersNames)
        return f'ⓘ Your trivia game controllers — {gameControllersStr}'

    async def getTriviaGameGlobalControllers(
        self,
        gameControllers: list[TriviaGameGlobalController] | None,
        delimiter: str = ', '
    ) -> str:
        if gameControllers is not None and not isinstance(gameControllers, list):
            raise TypeError(f'gameControllers argument is malformed: \"{gameControllers}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        if gameControllers is None or len(gameControllers) == 0:
            return f'ⓘ There are no global trivia game controllers.'

        gameControllersNames: list[str] = list()
        for gameController in gameControllers:
            gameControllersNames.append(gameController.userName)

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
        specialTriviaStatus: SpecialTriviaStatus | None = None,
        delimiter: str = ' '
    ) -> str:
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not utils.isValidInt(delaySeconds):
            raise TypeError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif delaySeconds < 1 or delaySeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'delaySeconds argument is out of bounds: {delaySeconds}')
        elif not utils.isValidInt(points):
            raise TypeError(f'points argument is malformed: \"{points}\"')
        elif points < 1 or points > utils.getIntMaxSafeSize():
            raise ValueError(f'points argument is out of bounds: {points}')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise TypeError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise TypeError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise TypeError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

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

        questionPrompt = await self.__triviaQuestionPresenter.getPrompt(
            triviaQuestion = triviaQuestion,
            delimiter = delimiter
        )

        return f'{emotePrompt} @{userNameThatRedeemed} !answer in {delaySecondsStr}s {cutenessPrompt} {questionPrompt}'.strip()

    async def getTriviaScoreMessage(
        self,
        shinyResult: ShinyTriviaResult,
        userName: str,
        toxicResult: ToxicTriviaResult,
        triviaResult: TriviaScoreResult
    ) -> str:
        if not isinstance(shinyResult, ShinyTriviaResult):
            raise TypeError(f'shinyResult argument is malformed: \"{shinyResult}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif not isinstance(toxicResult, ToxicTriviaResult):
            raise TypeError(f'toxicResult argument is malformed: \"{toxicResult}\"')
        elif not isinstance(triviaResult, TriviaScoreResult):
            raise TypeError(f'triviaResult argument is malformed: \"{triviaResult}\"')

        if triviaResult.getTotal() == 0 and triviaResult.getSuperTriviaWins() == 0:
            return f'{utils.getRandomSadEmoji()} @{userName} has not played any trivia games…'

        introStr = f'ⓘ @{userName} has'
        needsSemicolon = False

        triviaStr = ''
        if triviaResult.getTotal() >= 1:
            winLossStr = f'{triviaResult.getTriviaWinsStr()}-{triviaResult.getTriviaLossesStr()}'
            winsRatioStr = f'{triviaResult.getWinPercentStr()} wins'

            if triviaResult.getTotal() == 1:
                triviaStr = f' played {triviaResult.getTotalStr()} trivia game ({winLossStr}, {winsRatioStr})'
            else:
                triviaStr = f' played {triviaResult.getTotalStr()} trivia games ({winLossStr}, {winsRatioStr})'

            if triviaResult.getStreak() >= 3:
                triviaStr = f'{triviaStr}, and is on a {triviaResult.getAbsStreakStr()} game winning streak 😸'
            elif triviaResult.getStreak() <= -3:
                triviaStr = f'{triviaStr}, and is on a {triviaResult.getAbsStreakStr()} game losing streak 🙀'

            needsSemicolon = True

        superTriviaStr = ''
        if triviaResult.getSuperTriviaWins() >= 1:
            if needsSemicolon:
                superTriviaStr = ';'
            else:
                needsSemicolon = True

            if triviaResult.getSuperTriviaWins() == 1:
                superTriviaStr = f'{superTriviaStr} {triviaResult.getSuperTriviaWinsStr()} super trivia win'
            else:
                superTriviaStr = f'{superTriviaStr} {triviaResult.getSuperTriviaWinsStr()} super trivia wins'

        shinyStr = ''
        if shinyResult.newShinyCount >= 1:
            if needsSemicolon:
                shinyStr = ';'
            else:
                needsSemicolon = True

            if shinyResult.newShinyCount == 1:
                shinyStr = f'{shinyStr} {shinyResult.newShinyCountStr} shiny'
            else:
                shinyStr = f'{shinyStr} {shinyResult.newShinyCountStr} shinies'

        toxicStr = ''
        if toxicResult.newToxicCount >= 1:
            if needsSemicolon:
                toxicStr = ';'
            else:
                needsSemicolon = True

            if toxicResult.newToxicCount == 1:
                toxicStr = f'{toxicStr} {toxicResult.newToxicCountStr} toxic'
            else:
                toxicStr = f'{toxicStr} {toxicResult.newToxicCountStr} toxics'

        return f'{introStr}{triviaStr}{superTriviaStr}{shinyStr}{toxicStr}'.strip()

    async def isPrivilegedTriviaUser(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        try:
            twitchUser = await self.__usersRepository.getUserAsync(twitchChannel)
        except NoSuchUserException as e:
            # this exception should be impossible here, but let's just be safe
            self.__timber.log('TriviaUtils', f'Encountered an invalid Twitch user \"{twitchChannel}\" when trying to check userId \"{userId}\" for privileged trivia permissions', e, traceback.format_exc())
            return False

        bannedGameControllers = await self.__bannedTriviaGameControllersRepository.getBannedControllers()
        for bannedGameController in bannedGameControllers:
            if userId == bannedGameController.userId:
                return False

        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(twitchChannelId)

        twitchUserId = await self.__userIdsRepository.fetchUserId(
            userName = twitchUser.getHandle(),
            twitchAccessToken = twitchAccessToken
        )

        if utils.isValidStr(twitchUserId) and userId == twitchUserId:
            return True

        gameControllers = await self.__triviaGameControllersRepository.getControllers(
            twitchChannel = twitchUser.getHandle(),
            twitchChannelId = twitchChannelId
        )

        for gameController in gameControllers:
            if userId == gameController.userId:
                return True

        globalGameControllers = await self.__triviaGameGlobalControllersRepository.getControllers()
        for globalGameController in globalGameControllers:
            if userId == globalGameController.userId:
                return True

        administratorUserId = await self.__administratorProvider.getAdministratorUserId()

        return userId == administratorUserId
