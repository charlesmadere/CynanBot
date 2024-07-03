import asyncio
import queue
import traceback
from datetime import datetime, timedelta
from queue import SimpleQueue
from typing import Any

from ..cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..timber.timberInterface import TimberInterface
from .actions.absTriviaAction import AbsTriviaAction
from .actions.checkAnswerTriviaAction import CheckAnswerTriviaAction
from .actions.checkSuperAnswerTriviaAction import \
    CheckSuperAnswerTriviaAction
from .actions.clearSuperTriviaQueueTriviaAction import \
    ClearSuperTriviaQueueTriviaAction
from .actions.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from .actions.startNewTriviaGameAction import StartNewTriviaGameAction
from .actions.triviaActionType import TriviaActionType
from .emotes.triviaEmoteGeneratorInterface import \
    TriviaEmoteGeneratorInterface
from .events.absTriviaEvent import AbsTriviaEvent
from .events.clearedSuperTriviaQueueTriviaEvent import \
    ClearedSuperTriviaQueueTriviaEvent
from .events.correctAnswerTriviaEvent import CorrectAnswerTriviaEvent
from .events.correctSuperAnswerTriviaEvent import \
    CorrectSuperAnswerTriviaEvent
from .events.failedToFetchQuestionSuperTriviaEvent import \
    FailedToFetchQuestionSuperTriviaEvent
from .events.failedToFetchQuestionTriviaEvent import \
    FailedToFetchQuestionTriviaEvent
from .events.gameAlreadyInProgressTriviaEvent import \
    GameAlreadyInProgressTriviaEvent
from .events.gameNotReadyCheckAnswerTriviaEvent import \
    GameNotReadyCheckAnswerTriviaEvent
from .events.incorrectAnswerTriviaEvent import IncorrectAnswerTriviaEvent
from .events.incorrectSuperAnswerTriviaEvent import \
    IncorrectSuperAnswerTriviaEvent
from .events.invalidAnswerInputTriviaEvent import \
    InvalidAnswerInputTriviaEvent
from .events.newQueuedSuperTriviaGameEvent import \
    NewQueuedSuperTriviaGameEvent
from .events.newSuperTriviaGameEvent import NewSuperTriviaGameEvent
from .events.newTriviaGameEvent import NewTriviaGameEvent
from .events.outOfTimeSuperTriviaEvent import OutOfTimeSuperTriviaEvent
from .events.outOfTimeTriviaEvent import OutOfTimeTriviaEvent
from .events.superGameNotReadyCheckAnswerTriviaEvent import \
    SuperGameNotReadyCheckAnswerTriviaEvent
from .events.wrongUserCheckAnswerTriviaEvent import \
    WrongUserCheckAnswerTriviaEvent
from .games.absTriviaGameState import AbsTriviaGameState
from .games.queuedTriviaGameStoreInterface import \
    QueuedTriviaGameStoreInterface
from .games.superTriviaGameState import SuperTriviaGameState
from .games.triviaGameState import TriviaGameState
from .games.triviaGameStoreInterface import TriviaGameStoreInterface
from .questions.absTriviaQuestion import AbsTriviaQuestion
from .score.triviaScoreRepositoryInterface import \
    TriviaScoreRepositoryInterface
from .specialStatus.shinyTriviaHelper import ShinyTriviaHelper
from .specialStatus.specialTriviaStatus import SpecialTriviaStatus
from .specialStatus.toxicTriviaHelper import ToxicTriviaHelper
from .specialStatus.toxicTriviaPunishment import ToxicTriviaPunishment
from .specialStatus.toxicTriviaPunishmentResult import \
    ToxicTriviaPunishmentResult
from .superTriviaCooldownHelperInterface import \
    SuperTriviaCooldownHelperInterface
from .triviaAnswerCheckResult import TriviaAnswerCheckResult
from .triviaAnswerCheckerInterface import TriviaAnswerCheckerInterface
from .triviaEventListener import TriviaEventListener
from .triviaExceptions import (TooManyTriviaFetchAttemptsException,
                                     UnknownTriviaActionTypeException,
                                     UnknownTriviaGameTypeException)
from .triviaGameMachineInterface import TriviaGameMachineInterface
from .triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from .triviaRepositories.triviaRepositoryInterface import \
    TriviaRepositoryInterface
from .triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from ..twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..misc import utils as utils


class TriviaGameMachine(TriviaGameMachineInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        cutenessRepository: CutenessRepositoryInterface,
        queuedTriviaGameStore: QueuedTriviaGameStoreInterface,
        shinyTriviaHelper: ShinyTriviaHelper,
        superTriviaCooldownHelper: SuperTriviaCooldownHelperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        toxicTriviaHelper: ToxicTriviaHelper,
        triviaAnswerChecker: TriviaAnswerCheckerInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaGameStore: TriviaGameStoreInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaRepository: TriviaRepositoryInterface,
        triviaScoreRepository: TriviaScoreRepositoryInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        sleepTimeSeconds: float = 0.5,
        queueTimeoutSeconds: int = 3
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(queuedTriviaGameStore, QueuedTriviaGameStoreInterface):
            raise TypeError(f'queuedTriviaGameStore argument is malformed: \"{queuedTriviaGameStore}\"')
        elif not isinstance(shinyTriviaHelper, ShinyTriviaHelper):
            raise TypeError(f'shinyTriviaHelper argument is malformed: \"{shinyTriviaHelper}\"')
        elif not isinstance(superTriviaCooldownHelper, SuperTriviaCooldownHelperInterface):
            raise TypeError(f'superTriviaCooldownHelper argument is malformed: \"{superTriviaCooldownHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(toxicTriviaHelper, ToxicTriviaHelper):
            raise TypeError(f'toxicTriviaHelper argument is malformed: \"{toxicTriviaHelper}\"')
        elif not isinstance(triviaAnswerChecker, TriviaAnswerCheckerInterface):
            raise TypeError(f'triviaAnswerChecker argument is malformed: \"{triviaAnswerChecker}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface):
            raise TypeError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaGameStore, TriviaGameStoreInterface):
            raise TypeError(f'triviaGameStore argument is malformed: \"{triviaGameStore}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif not isinstance(triviaRepository, TriviaRepositoryInterface):
            raise TypeError(f'triviaRepository argument is malformed: \"{triviaRepository}\"')
        elif not isinstance(triviaScoreRepository, TriviaScoreRepositoryInterface):
            raise TypeError(f'triviaScoreRepository argument is malformed: \"{triviaScoreRepository}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepositoryInterface argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise TypeError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 0.25 or sleepTimeSeconds > 3:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidInt(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__cutenessRepository: CutenessRepositoryInterface = cutenessRepository
        self.__queuedTriviaGameStore: QueuedTriviaGameStoreInterface = queuedTriviaGameStore
        self.__shinyTriviaHelper: ShinyTriviaHelper = shinyTriviaHelper
        self.__superTriviaCooldownHelper: SuperTriviaCooldownHelperInterface = superTriviaCooldownHelper
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__toxicTriviaHelper: ToxicTriviaHelper = toxicTriviaHelper
        self.__triviaAnswerChecker: TriviaAnswerCheckerInterface = triviaAnswerChecker
        self.__triviaEmoteGenerator: TriviaEmoteGeneratorInterface = triviaEmoteGenerator
        self.__triviaGameStore: TriviaGameStoreInterface = triviaGameStore
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__triviaRepository: TriviaRepositoryInterface = triviaRepository
        self.__triviaScoreRepository: TriviaScoreRepositoryInterface = triviaScoreRepository
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__sleepTimeSeconds: float = sleepTimeSeconds
        self.__queueTimeoutSeconds: int = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__eventListener: TriviaEventListener | None = None
        self.__actionQueue: SimpleQueue[AbsTriviaAction] = SimpleQueue()
        self.__eventQueue: SimpleQueue[AbsTriviaEvent] = SimpleQueue()

    async def __applyToxicSuperTriviaPunishment(
        self,
        action: CheckSuperAnswerTriviaAction | None,
        state: SuperTriviaGameState
    ) -> ToxicTriviaPunishmentResult | None:
        if action is not None and not isinstance(action, CheckSuperAnswerTriviaAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not isinstance(state, SuperTriviaGameState):
            raise TypeError(f'state argument is malformed: \"{state}\"')

        if not state.isToxic():
            return None

        toxicTriviaPunishmentMultiplier = state.getToxicTriviaPunishmentMultiplier()

        if toxicTriviaPunishmentMultiplier <= 0:
            return None

        answeredUserIds = state.getAnsweredUserIds()

        if action is not None:
            del answeredUserIds[action.getUserId()]

        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(state.getTwitchChannelId())
        toxicTriviaPunishments: list[ToxicTriviaPunishment] = list()
        totalPointsStolen = 0

        for userId, answerCount in answeredUserIds.items():
            punishedByPoints = -1 * answerCount * toxicTriviaPunishmentMultiplier * state.getRegularTriviaPointsForWinning()
            totalPointsStolen = totalPointsStolen + abs(punishedByPoints)

            userName = await self.__userIdsRepository.requireUserName(
                userId = userId,
                twitchAccessToken = twitchAccessToken
            )

            cutenessResult = await self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = punishedByPoints,
                twitchChannel = state.getTwitchChannel(),
                twitchChannelId = state.getTwitchChannelId(),
                userId = userId,
                userName = userName
            )

            toxicTriviaPunishments.append(ToxicTriviaPunishment(
                cutenessResult = cutenessResult,
                numberOfPunishments = answerCount,
                punishedByPoints = punishedByPoints,
                userId = userId,
                userName = userName
            ))

        self.__timber.log('TriviaGameMachine', f'Applied toxic trivia punishments to {len(toxicTriviaPunishments)} user(s) in \"{state.getTwitchChannel()}\" for a total punishment of {totalPointsStolen} point(s)')

        if len(toxicTriviaPunishments) == 0:
            return None

        toxicTriviaPunishments.sort(
            key = lambda punishment: (punishment.punishedByPoints, punishment.userName.casefold())
        )

        return ToxicTriviaPunishmentResult(
            totalPointsStolen = totalPointsStolen,
            toxicTriviaPunishments = toxicTriviaPunishments,
        )

    async def __beginQueuedTriviaGames(self):
        activeChannelIdsSet: set[str] = set()
        activeChannelIdsSet.update(await self.__triviaGameStore.getTwitchChannelIdsWithActiveSuperGames())
        activeChannelIdsSet.update(await self.__superTriviaCooldownHelper.getTwitchChannelIdsInCooldown())

        queuedSuperGames = await self.__queuedTriviaGameStore.popQueuedSuperGames(activeChannelIdsSet)

        for queuedSuperGame in queuedSuperGames:
            remainingQueueSize = await self.__queuedTriviaGameStore.getQueuedSuperGamesSize(
                twitchChannelId = queuedSuperGame.getTwitchChannelId()
            )

            self.__timber.log('TriviaGameMachine', f'Starting new queued super trivia game for \"{queuedSuperGame.getTwitchChannel()}\", with {remainingQueueSize} game(s) remaining in their queue ({queuedSuperGame.actionId=})')
            await self.__handleActionStartNewSuperTriviaGame(queuedSuperGame)

    async def __checkAnswer(
        self,
        answer: str | None,
        triviaQuestion: AbsTriviaQuestion,
        extras: dict[str, Any] | None = None
    ) -> TriviaAnswerCheckResult:
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')

        return await self.__triviaAnswerChecker.checkAnswer(
            answer = answer,
            triviaQuestion = triviaQuestion,
            extras = extras
        )

    async def __handleActionCheckAnswer(self, action: CheckAnswerTriviaAction):
        if not isinstance(action, CheckAnswerTriviaAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif action.triviaActionType is not TriviaActionType.CHECK_ANSWER:
            raise RuntimeError(f'TriviaActionType is not {TriviaActionType.CHECK_ANSWER}: \"{action.triviaActionType}\"')

        state = await self.__triviaGameStore.getNormalGame(
            twitchChannelId = action.getTwitchChannelId(),
            userId = action.getUserId()
        )

        if state is None:
            await self.__submitEvent(GameNotReadyCheckAnswerTriviaEvent(
                actionId = action.actionId,
                answer = action.getAnswer(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                twitchChannel = action.getTwitchChannel(),
                twitchChannelId = action.getTwitchChannelId(),
                userId = action.getUserId(),
                userName = action.getUserName()
            ))
            return

        if state.getUserId() != action.getUserId():
            await self.__submitEvent(WrongUserCheckAnswerTriviaEvent(
                triviaQuestion = state.getTriviaQuestion(),
                actionId = action.actionId,
                answer = action.getAnswer(),
                emote = state.getEmote(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                gameId = state.getGameId(),
                twitchChannel = action.getTwitchChannel(),
                twitchChannelId = action.getTwitchChannelId(),
                userId = action.getUserId(),
                userName = action.getUserName()
            ))
            return

        checkResult = await self.__checkAnswer(
            answer = action.getAnswer(),
            triviaQuestion = state.getTriviaQuestion(),
            extras = {
                'actionId': action.actionId,
                'twitchChannel': action.getTwitchChannel(),
                'twitchChannelId': action.getTwitchChannelId(),
                'userId': action.getUserId(),
                'userName': action.getUserName()
            }
        )

        if checkResult is TriviaAnswerCheckResult.INVALID_INPUT:
            await self.__submitEvent(InvalidAnswerInputTriviaEvent(
                triviaQuestion = state.getTriviaQuestion(),
                specialTriviaStatus = state.getSpecialTriviaStatus(),
                actionId = action.actionId,
                answer = action.getAnswer(),
                emote = state.getEmote(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                gameId = state.getGameId(),
                twitchChannel = action.getTwitchChannel(),
                twitchChannelId = action.getTwitchChannelId(),
                userId = action.getUserId(),
                userName = action.getUserName()
            ))
            return

        await self.__removeNormalTriviaGame(
            twitchChannelId = action.getTwitchChannelId(),
            userId = action.getUserId()
        )

        if checkResult is TriviaAnswerCheckResult.INCORRECT:
            triviaScoreResult = await self.__triviaScoreRepository.incrementTriviaLosses(
                twitchChannel = action.getTwitchChannel(),
                twitchChannelId = action.getTwitchChannelId(),
                userId = action.getUserId()
            )

            await self.__submitEvent(IncorrectAnswerTriviaEvent(
                triviaQuestion = state.getTriviaQuestion(),
                specialTriviaStatus = state.getSpecialTriviaStatus(),
                actionId = action.actionId,
                answer = action.getAnswer(),
                emote = state.getEmote(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                gameId = state.getGameId(),
                twitchChannel = action.getTwitchChannel(),
                twitchChannelId = action.getTwitchChannelId(),
                userId = action.getUserId(),
                userName = action.getUserName(),
                triviaScoreResult = triviaScoreResult
            ))
            return

        if state.isShiny():
            await self.__shinyTriviaHelper.shinyTriviaWin(
                twitchChannel = state.getTwitchChannel(),
                twitchChannelId = state.getTwitchChannelId(),
                userId = action.getUserId(),
                userName = action.getUserName()
            )
        elif state.isToxic():
            await self.__toxicTriviaHelper.toxicTriviaWin(
                twitchChannel = state.getTwitchChannel(),
                twitchChannelId = state.getTwitchChannelId(),
                userId = action.getUserId(),
                userName = action.getUserName()
            )

        cutenessResult = await self.__cutenessRepository.fetchCutenessIncrementedBy(
            incrementAmount = state.getPointsForWinning(),
            twitchChannel = state.getTwitchChannel(),
            twitchChannelId = state.getTwitchChannelId(),
            userId = action.getUserId(),
            userName = action.getUserName()
        )

        triviaScoreResult = await self.__triviaScoreRepository.incrementTriviaWins(
            twitchChannel = action.getTwitchChannel(),
            twitchChannelId = action.getTwitchChannelId(),
            userId = action.getUserId()
        )

        await self.__submitEvent(CorrectAnswerTriviaEvent(
            triviaQuestion = state.getTriviaQuestion(),
            cutenessResult = cutenessResult,
            pointsForWinning = state.getPointsForWinning(),
            specialTriviaStatus = state.getSpecialTriviaStatus(),
            actionId = action.actionId,
            answer = action.requireAnswer(),
            emote = state.getEmote(),
            eventId = await self.__triviaIdGenerator.generateEventId(),
            gameId = state.getGameId(),
            twitchChannel = action.getTwitchChannel(),
            twitchChannelId = action.getTwitchChannelId(),
            userId = action.getUserId(),
            userName = action.getUserName(),
            triviaScoreResult = triviaScoreResult
        ))

    async def __handleActionCheckSuperAnswer(self, action: CheckSuperAnswerTriviaAction):
        if not isinstance(action, CheckSuperAnswerTriviaAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif action.triviaActionType is not TriviaActionType.CHECK_SUPER_ANSWER:
            raise RuntimeError(f'TriviaActionType is not {TriviaActionType.CHECK_SUPER_ANSWER}: \"{action.triviaActionType}\"')

        state = await self.__triviaGameStore.getSuperGame(
            twitchChannelId = action.getTwitchChannelId()
        )

        if state is None:
            await self.__submitEvent(SuperGameNotReadyCheckAnswerTriviaEvent(
                actionId = action.actionId,
                answer = action.getAnswer(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                twitchChannel = action.getTwitchChannel(),
                twitchChannelId = action.getTwitchChannelId(),
                userId = action.getUserId(),
                userName = action.getUserName()
            ))
            return

        if not state.isEligibleToAnswer(action.getUserId()):
            return

        state.incrementAnswerCount(action.getUserId())

        checkResult = await self.__checkAnswer(
            answer = action.getAnswer(),
            triviaQuestion = state.getTriviaQuestion(),
            extras = {
                'actionId': action.actionId,
                'twitchChannel': action.getTwitchChannel(),
                'twitchChannelId': action.getTwitchChannelId(),
                'userId': action.getUserId(),
                'userName': action.getUserName()
            }
        )

        # we're intentionally ONLY checking for TriviaAnswerCheckResult.CORRECT
        if checkResult is not TriviaAnswerCheckResult.CORRECT:
            await self.__submitEvent(IncorrectSuperAnswerTriviaEvent(
                triviaQuestion = state.getTriviaQuestion(),
                specialTriviaStatus = state.getSpecialTriviaStatus(),
                actionId = action.actionId,
                answer = action.requireAnswer(),
                emote = state.getEmote(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                gameId = state.getGameId(),
                twitchChannel = action.getTwitchChannel(),
                twitchChannelId = action.getTwitchChannelId(),
                userId = action.getUserId(),
                userName = action.getUserName()
            ))
            return

        await self.__removeSuperTriviaGame(
            twitchChannelId = action.getTwitchChannelId()
        )

        toxicTriviaPunishmentResult: ToxicTriviaPunishmentResult | None = None
        pointsForWinning = state.getPointsForWinning()

        if state.isShiny():
            await self.__shinyTriviaHelper.shinyTriviaWin(
                twitchChannel = state.getTwitchChannel(),
                twitchChannelId = state.getTwitchChannelId(),
                userId = action.getUserId(),
                userName = action.getUserName()
            )
        elif state.isToxic():
            toxicTriviaPunishmentResult = await self.__applyToxicSuperTriviaPunishment(
                action = action,
                state = state
            )

            if toxicTriviaPunishmentResult is not None:
                await self.__toxicTriviaHelper.toxicTriviaWin(
                    twitchChannel = state.getTwitchChannel(),
                    twitchChannelId = state.getTwitchChannelId(),
                    userId = action.getUserId(),
                    userName = action.getUserName()
                )

                pointsForWinning = pointsForWinning + toxicTriviaPunishmentResult.totalPointsStolen

        cutenessResult = await self.__cutenessRepository.fetchCutenessIncrementedBy(
            incrementAmount = pointsForWinning,
            twitchChannel = state.getTwitchChannel(),
            twitchChannelId = state.getTwitchChannelId(),
            userId = action.getUserId(),
            userName = action.getUserName()
        )

        remainingQueueSize = await self.__queuedTriviaGameStore.getQueuedSuperGamesSize(
            twitchChannelId = action.getTwitchChannelId()
        )

        triviaScoreResult = await self.__triviaScoreRepository.incrementSuperTriviaWins(
            twitchChannel = action.getTwitchChannel(),
            twitchChannelId = action.getTwitchChannelId(),
            userId = action.getUserId()
        )

        await self.__submitEvent(CorrectSuperAnswerTriviaEvent(
            triviaQuestion = state.getTriviaQuestion(),
            cutenessResult = cutenessResult,
            pointsForWinning = pointsForWinning,
            remainingQueueSize = remainingQueueSize,
            toxicTriviaPunishmentResult = toxicTriviaPunishmentResult,
            specialTriviaStatus = state.getSpecialTriviaStatus(),
            actionId = action.actionId,
            answer = action.requireAnswer(),
            emote = state.getEmote(),
            eventId = await self.__triviaIdGenerator.generateEventId(),
            gameId = state.getGameId(),
            twitchChannel = action.getTwitchChannel(),
            twitchChannelId = action.getTwitchChannelId(),
            userId = action.getUserId(),
            userName = action.getUserName(),
            triviaScoreResult = triviaScoreResult
        ))

    async def __handleActionClearSuperTriviaQueue(self, action: ClearSuperTriviaQueueTriviaAction):
        if not isinstance(action, ClearSuperTriviaQueueTriviaAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif action.triviaActionType is not TriviaActionType.CLEAR_SUPER_TRIVIA_QUEUE:
            raise RuntimeError(f'TriviaActionType is not {TriviaActionType.CLEAR_SUPER_TRIVIA_QUEUE}: \"{action.triviaActionType}\"')

        result = await self.__queuedTriviaGameStore.clearQueuedSuperGames(
            twitchChannelId = action.getTwitchChannelId()
        )

        self.__timber.log('TriviaGameMachine', f'Cleared Super Trivia game queue for \"{action.getTwitchChannel()}\" ({action.actionId=}): {result}')

        await self.__submitEvent(ClearedSuperTriviaQueueTriviaEvent(
            numberOfGamesRemoved = result.amountRemoved,
            previousQueueSize = result.oldQueueSize,
            actionId = action.actionId,
            eventId = await self.__triviaIdGenerator.generateEventId(),
            twitchChannel = action.getTwitchChannel(),
            twitchChannelId = action.getTwitchChannelId()
        ))

    async def __handleActionStartNewTriviaGame(self, action: StartNewTriviaGameAction):
        if not isinstance(action, StartNewTriviaGameAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif action.triviaActionType is not TriviaActionType.START_NEW_GAME:
            raise RuntimeError(f'TriviaActionType is not {TriviaActionType.START_NEW_GAME}: \"{action.triviaActionType}\"')

        now = datetime.now(self.__timeZoneRepository.getDefault())
        state = await self.__triviaGameStore.getNormalGame(
            twitchChannelId = action.getTwitchChannelId(),
            userId = action.getUserId()
        )

        if state is not None and state.getEndTime() >= now:
            await self.__submitEvent(GameAlreadyInProgressTriviaEvent(
                gameId = state.getGameId(),
                actionId = action.actionId,
                eventId = await self.__triviaIdGenerator.generateEventId(),
                twitchChannel = action.getTwitchChannel(),
                twitchChannelId = action.getTwitchChannelId(),
                userId = action.getUserId(),
                userName = action.getUserName()
            ))
            return

        emote = await self.__triviaEmoteGenerator.getNextEmoteFor(
            twitchChannelId = action.getTwitchChannelId()
        )

        triviaQuestion: AbsTriviaQuestion | None = None
        try:
            triviaQuestion = await self.__triviaRepository.fetchTrivia(
                emote = emote,
                triviaFetchOptions = action.getTriviaFetchOptions()
            )
        except TooManyTriviaFetchAttemptsException as e:
            self.__timber.log('TriviaGameMachine', f'Reached limit on trivia fetch attempts without being able to successfully retrieve a trivia question for \"{action.getTwitchChannel()}\": {e}', e, traceback.format_exc())

        if triviaQuestion is None:
            await self.__submitEvent(FailedToFetchQuestionTriviaEvent(
                actionId = action.actionId,
                eventId = await self.__triviaIdGenerator.generateEventId(),
                twitchChannel = action.getTwitchChannel(),
                twitchChannelId = action.getTwitchChannelId(),
                userId = action.getUserId(),
                userName = action.getUserName()
            ))
            return

        specialTriviaStatus: SpecialTriviaStatus | None = None
        pointsForWinning = action.getPointsForWinning()

        if action.isShinyTriviaEnabled() and await self.__shinyTriviaHelper.isShinyTriviaQuestion(
            twitchChannel = action.getTwitchChannel(),
            twitchChannelId = action.getTwitchChannelId(),
            userId = action.getUserId(),
            userName = action.getUserName()
        ):
            specialTriviaStatus = SpecialTriviaStatus.SHINY
            pointsForWinning = pointsForWinning * action.getShinyMultiplier()

        endTime = datetime.now(self.__timeZoneRepository.getDefault()) + timedelta(seconds = action.getSecondsToLive())

        state = TriviaGameState(
            triviaQuestion = triviaQuestion,
            endTime = endTime,
            basePointsForWinning = action.getPointsForWinning(),
            pointsForWinning = pointsForWinning,
            secondsToLive = action.getSecondsToLive(),
            specialTriviaStatus = specialTriviaStatus,
            actionId = action.actionId,
            emote = emote,
            gameId = await self.__triviaIdGenerator.generateGameId(),
            twitchChannel = action.getTwitchChannel(),
            twitchChannelId = action.getTwitchChannelId(),
            userId = action.getUserId(),
            userName = action.getUserName()
        )

        await self.__triviaGameStore.add(state)

        await self.__submitEvent(NewTriviaGameEvent(
            triviaQuestion = triviaQuestion,
            pointsForWinning = pointsForWinning,
            secondsToLive = action.getSecondsToLive(),
            specialTriviaStatus = specialTriviaStatus,
            actionId = action.actionId,
            emote = emote,
            eventId = await self.__triviaIdGenerator.generateEventId(),
            gameId = state.getGameId(),
            twitchChannel = action.getTwitchChannel(),
            userId = action.getUserId(),
            userName = action.getUserName()
        ))

    async def __handleActionStartNewSuperTriviaGame(self, action: StartNewSuperTriviaGameAction):
        if not isinstance(action, StartNewSuperTriviaGameAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif action.triviaActionType is not TriviaActionType.START_NEW_SUPER_GAME:
            raise RuntimeError(f'TriviaActionType is not {TriviaActionType.START_NEW_SUPER_GAME}: \"{action.triviaActionType}\"')

        now = datetime.now(self.__timeZoneRepository.getDefault())
        superTriviaFirstQuestionDelay = timedelta(
            seconds = await self.__triviaSettingsRepository.getSuperTriviaFirstQuestionDelaySeconds()
        )

        if action.getCreationTime() + superTriviaFirstQuestionDelay >= now:
            # Let's re-add this action back into the queue to try processing again later, as this action
            # was created too recently. We don't want super trivia questions to start instantaneously, as
            # it could mean that some people in chat are not ready to answer at first. So this minor delay
            # helps prevent such a situation.
            self.submitAction(action)
            return

        state = await self.__triviaGameStore.getSuperGame(
            twitchChannelId = action.getTwitchChannelId()
        )

        isSuperTriviaGameCurrentlyInProgress = state is not None and state.getEndTime() >= now

        queueResult = await self.__queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = isSuperTriviaGameCurrentlyInProgress,
            action = action
        )

        if queueResult.amountAdded >= 1:
            self.__timber.log('TriviaGameMachine', f'Queued new Super Trivia game(s) for \"{action.getTwitchChannel()}\" ({action.actionId=}): {queueResult}')

            await self.__submitEvent(NewQueuedSuperTriviaGameEvent(
                numberOfGames = queueResult.amountAdded,
                pointsForWinning = action.getPointsForWinning(),
                secondsToLive = action.getSecondsToLive(),
                shinyMultiplier = action.getShinyMultiplier(),
                actionId = action.actionId,
                eventId = await self.__triviaIdGenerator.generateEventId(),
                twitchChannel = action.getTwitchChannel(),
                twitchChannelId = action.getTwitchChannelId()
            ))

        if isSuperTriviaGameCurrentlyInProgress:
            return
        elif self.__superTriviaCooldownHelper.isTwitchChannelInCooldown(action.getTwitchChannel()):
            # Let's re-add this action back into the queue to try processing again later, as this Twitch
            # channel is on cooldown. This situation occurs if this Twitch channel just finished answering
            # a super trivia question, and prevents us from just immediately jumping into the next super
            # trivia question.
            self.submitAction(action)
            return

        emote = await self.__triviaEmoteGenerator.getNextEmoteFor(
            twitchChannelId = action.getTwitchChannelId()
        )

        triviaQuestion: AbsTriviaQuestion | None = None
        try:
            triviaQuestion = await self.__triviaRepository.fetchTrivia(
                emote = emote,
                triviaFetchOptions = action.getTriviaFetchOptions()
            )
        except TooManyTriviaFetchAttemptsException as e:
            self.__timber.log('TriviaGameMachine', f'Reached limit on trivia fetch attempts without being able to successfully retrieve a super trivia question for \"{action.getTwitchChannel()}\" ({action.actionId=}): {e}', e, traceback.format_exc())

        if triviaQuestion is None:
            await self.__submitEvent(FailedToFetchQuestionSuperTriviaEvent(
                actionId = action.actionId,
                eventId = await self.__triviaIdGenerator.generateEventId(),
                twitchChannel = action.getTwitchChannel(),
                twitchChannelId = action.getTwitchChannelId()
            ))
            return

        specialTriviaStatus: SpecialTriviaStatus | None = None
        pointsForWinning = action.getPointsForWinning()

        if action.isShinyTriviaEnabled() and await self.__shinyTriviaHelper.isShinySuperTriviaQuestion(
            twitchChannelId = action.getTwitchChannelId()
        ):
            specialTriviaStatus = SpecialTriviaStatus.SHINY
            pointsForWinning = pointsForWinning * action.getShinyMultiplier()
        elif action.isToxicTriviaEnabled() and await self.__toxicTriviaHelper.isToxicSuperTriviaQuestion(
            twitchChannelId = action.getTwitchChannelId()
        ):
            specialTriviaStatus = SpecialTriviaStatus.TOXIC
            pointsForWinning = pointsForWinning * action.getToxicMultiplier()

        endTime = datetime.now(self.__timeZoneRepository.getDefault()) + timedelta(seconds = action.getSecondsToLive())

        state = SuperTriviaGameState(
            triviaQuestion = triviaQuestion,
            endTime = endTime,
            basePointsForWinning = action.getPointsForWinning(),
            perUserAttempts = action.getPerUserAttempts(),
            pointsForWinning = pointsForWinning,
            regularTriviaPointsForWinning = action.getRegularTriviaPointsForWinning(),
            secondsToLive = action.getSecondsToLive(),
            toxicTriviaPunishmentMultiplier = action.getToxicTriviaPunishmentMultiplier(),
            specialTriviaStatus = specialTriviaStatus,
            actionId = action.actionId,
            emote = emote,
            gameId = await self.__triviaIdGenerator.generateGameId(),
            twitchChannel = action.getTwitchChannel(),
            twitchChannelId = action.getTwitchChannelId()
        )

        await self.__triviaGameStore.add(state)

        await self.__submitEvent(NewSuperTriviaGameEvent(
            triviaQuestion = triviaQuestion,
            pointsForWinning = pointsForWinning,
            secondsToLive = action.getSecondsToLive(),
            specialTriviaStatus = specialTriviaStatus,
            actionId = action.actionId,
            emote = emote,
            eventId = await self.__triviaIdGenerator.generateEventId(),
            gameId = state.getGameId(),
            twitchChannel = action.getTwitchChannel(),
            twitchChannelId = action.getTwitchChannelId()
        ))

    async def __refreshStatusOfTriviaGames(self):
        await self.__removeDeadTriviaGames()
        await self.__beginQueuedTriviaGames()

    async def __removeDeadTriviaGames(self):
        now = datetime.now(self.__timeZoneRepository.getDefault())
        gameStates = await self.__triviaGameStore.getAll()
        gameStatesToRemove: list[AbsTriviaGameState] = list()

        for state in gameStates:
            if state.getEndTime() < now:
                gameStatesToRemove.append(state)

        for state in gameStatesToRemove:
            if isinstance(state, TriviaGameState):
                await self.__removeDeadNormalTriviaGame(state)
            elif isinstance(state, SuperTriviaGameState):
                await self.__removeDeadSuperTriviaGame(state)
            else:
                raise UnknownTriviaGameTypeException(f'Unknown TriviaGameType ({state.getGameId()=}) ({state.getTwitchChannel()=}) ({state.actionId=}): \"{state.getTriviaGameType()}\"')

    async def __removeDeadNormalTriviaGame(self, state: TriviaGameState):
        if not isinstance(state, TriviaGameState):
            raise TypeError(f'state argument is malformed: \"{state}\"')

        await self.__removeNormalTriviaGame(
            twitchChannelId = state.getTwitchChannelId(),
            userId = state.getUserId()
        )

        triviaScoreResult = await self.__triviaScoreRepository.incrementTriviaLosses(
            twitchChannel = state.getTwitchChannel(),
            twitchChannelId = state.getTwitchChannelId(),
            userId = state.getUserId()
        )

        await self.__submitEvent(OutOfTimeTriviaEvent(
            triviaQuestion = state.getTriviaQuestion(),
            pointsForWinning = state.getPointsForWinning(),
            specialTriviaStatus = state.getSpecialTriviaStatus(),
            actionId = state.actionId,
            emote = state.getEmote(),
            eventId = await self.__triviaIdGenerator.generateEventId(),
            gameId = state.getGameId(),
            twitchChannel = state.getTwitchChannel(),
            twitchChannelId = state.getTwitchChannelId(),
            userId = state.getUserId(),
            userName = state.getUserName(),
            triviaScoreResult = triviaScoreResult
        ))

    async def __removeDeadSuperTriviaGame(self, state: SuperTriviaGameState):
        if not isinstance(state, SuperTriviaGameState):
            raise TypeError(f'state argument is malformed: \"{state}\"')

        await self.__removeSuperTriviaGame(
            twitchChannelId = state.getTwitchChannelId()
        )

        toxicTriviaPunishmentResult: ToxicTriviaPunishmentResult | None = None
        pointsForWinning = state.getPointsForWinning()

        if state.isToxic():
            toxicTriviaPunishmentResult = await self.__applyToxicSuperTriviaPunishment(
                action = None,
                state = state
            )

            if toxicTriviaPunishmentResult is not None:
                pointsForWinning = pointsForWinning + toxicTriviaPunishmentResult.totalPointsStolen

        remainingQueueSize = await self.__queuedTriviaGameStore.getQueuedSuperGamesSize(
            twitchChannelId = state.getTwitchChannelId()
        )

        await self.__submitEvent(OutOfTimeSuperTriviaEvent(
            triviaQuestion = state.getTriviaQuestion(),
            pointsForWinning = pointsForWinning,
            remainingQueueSize = remainingQueueSize,
            specialTriviaStatus = state.getSpecialTriviaStatus(),
            toxicTriviaPunishmentResult = toxicTriviaPunishmentResult,
            actionId = state.actionId,
            emote = state.getEmote(),
            eventId = await self.__triviaIdGenerator.generateEventId(),
            gameId = state.getGameId(),
            twitchChannel = state.getTwitchChannel(),
            twitchChannelId = state.getTwitchChannelId()
        ))

    async def __removeNormalTriviaGame(self, twitchChannelId: str, userId: str):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        await self.__triviaGameStore.removeNormalGame(
            twitchChannelId = twitchChannelId,
            userId = userId
        )

    async def __removeSuperTriviaGame(self, twitchChannelId: str):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        await self.__triviaGameStore.removeSuperGame(twitchChannelId)
        await self.__superTriviaCooldownHelper.update(twitchChannelId)

    def setEventListener(self, listener: TriviaEventListener | None):
        if listener is not None and not isinstance(listener, TriviaEventListener):
            raise TypeError(f'listener argument is malformed: \"{listener}\"')

        self.__eventListener = listener

    async def __startActionLoop(self):
        while True:
            actions: list[AbsTriviaAction] = list()

            try:
                while not self.__actionQueue.empty():
                    actions.append(self.__actionQueue.get_nowait())
            except queue.Empty as e:
                self.__timber.log('TriviaGameMachine', f'Encountered queue.Empty when building up actions list (queue size: {self.__actionQueue.qsize()}) (actions size: {len(actions)}): {e}', e)

            try:
                for action in actions:

                    if isinstance(action, CheckAnswerTriviaAction):
                        await self.__handleActionCheckAnswer(action)
                    elif isinstance(action, CheckSuperAnswerTriviaAction):
                        await self.__handleActionCheckSuperAnswer(action)
                    elif isinstance(action, ClearSuperTriviaQueueTriviaAction):
                        await self.__handleActionClearSuperTriviaQueue(action)
                    elif isinstance(action, StartNewTriviaGameAction):
                        await self.__handleActionStartNewTriviaGame(action)
                    elif isinstance(action, StartNewSuperTriviaGameAction):
                        await self.__handleActionStartNewSuperTriviaGame(action)
                    else:
                        raise UnknownTriviaActionTypeException(f'Unknown TriviaActionType: \"{type(action)=}\"')
            except Exception as e:
                self.__timber.log('TriviaGameMachine', f'Encountered unknown Exception when looping through actions (queue size: {self.__actionQueue.qsize()}) (actions size: {len(actions)}): {e}', e, traceback.format_exc())

            try:
                await self.__refreshStatusOfTriviaGames()
            except Exception as e:
                self.__timber.log('TriviaGameMachine', f'Encountered unknown Exception when refreshing status of trivia games: {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__sleepTimeSeconds)

    async def __startEventLoop(self):
        while True:
            eventListener = self.__eventListener

            if eventListener is not None:
                events: list[AbsTriviaEvent] = list()

                try:
                    while not self.__eventQueue.empty():
                        events.append(self.__eventQueue.get_nowait())
                except queue.Empty as e:
                    self.__timber.log('TriviaGameMachine', f'Encountered queue.Empty when building up events list (queue size: {self.__eventQueue.qsize()}) (events size: {len(events)}): {e}', e, traceback.format_exc())

                for event in events:
                    try:
                        await eventListener.onNewTriviaEvent(event)
                    except Exception as e:
                        self.__timber.log('TriviaGameMachine', f'Encountered unknown Exception when looping through events (queue size: {self.__eventQueue.qsize()}) (event: {event}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__sleepTimeSeconds)

    def startMachine(self):
        if self.__isStarted:
            self.__timber.log('TriviaGameMachine', 'Not starting TriviaGameMachine as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TriviaGameMachine', 'Starting TriviaGameMachine...')
        self.__backgroundTaskHelper.createTask(self.__startActionLoop())
        self.__backgroundTaskHelper.createTask(self.__startEventLoop())

    def submitAction(self, action: AbsTriviaAction):
        if not isinstance(action, AbsTriviaAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        try:
            self.__actionQueue.put(action, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TriviaGameMachine', f'Encountered queue.Full when submitting a new action ({action}) into the action queue (queue size: {self.__actionQueue.qsize()}): {e}', e, traceback.format_exc())

    async def __submitEvent(self, event: AbsTriviaEvent):
        if not isinstance(event, AbsTriviaEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        try:
            self.__eventQueue.put(event, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TriviaGameMachine', f'Encountered queue.Full when submitting a new event ({event}) into the event queue (queue size: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())
