import asyncio
import queue
import traceback
from datetime import datetime, timedelta, timezone
from queue import SimpleQueue
from typing import Any, Dict, List, Optional, Set

import CynanBot.misc.utils as utils
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.cuteness.cutenessRepositoryInterface import \
    CutenessRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.actions.absTriviaAction import AbsTriviaAction
from CynanBot.trivia.actions.checkAnswerTriviaAction import \
    CheckAnswerTriviaAction
from CynanBot.trivia.actions.checkSuperAnswerTriviaAction import \
    CheckSuperAnswerTriviaAction
from CynanBot.trivia.actions.clearSuperTriviaQueueTriviaAction import \
    ClearSuperTriviaQueueTriviaAction
from CynanBot.trivia.actions.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from CynanBot.trivia.actions.startNewTriviaGameAction import \
    StartNewTriviaGameAction
from CynanBot.trivia.actions.triviaActionType import TriviaActionType
from CynanBot.trivia.events.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.events.clearedSuperTriviaQueueTriviaEvent import \
    ClearedSuperTriviaQueueTriviaEvent
from CynanBot.trivia.events.correctAnswerTriviaEvent import \
    CorrectAnswerTriviaEvent
from CynanBot.trivia.events.correctSuperAnswerTriviaEvent import \
    CorrectSuperAnswerTriviaEvent
from CynanBot.trivia.events.failedToFetchQuestionSuperTriviaEvent import \
    FailedToFetchQuestionSuperTriviaEvent
from CynanBot.trivia.events.failedToFetchQuestionTriviaEvent import \
    FailedToFetchQuestionTriviaEvent
from CynanBot.trivia.events.gameAlreadyInProgressTriviaEvent import \
    GameAlreadyInProgressTriviaEvent
from CynanBot.trivia.events.gameNotReadyCheckAnswerTriviaEvent import \
    GameNotReadyCheckAnswerTriviaEvent
from CynanBot.trivia.events.incorrectAnswerTriviaEvent import \
    IncorrectAnswerTriviaEvent
from CynanBot.trivia.events.incorrectSuperAnswerTriviaEvent import \
    IncorrectSuperAnswerTriviaEvent
from CynanBot.trivia.events.invalidAnswerInputTriviaEvent import \
    InvalidAnswerInputTriviaEvent
from CynanBot.trivia.events.newQueuedSuperTriviaGameEvent import \
    NewQueuedSuperTriviaGameEvent
from CynanBot.trivia.events.newSuperTriviaGameEvent import \
    NewSuperTriviaGameEvent
from CynanBot.trivia.events.newTriviaGameEvent import NewTriviaGameEvent
from CynanBot.trivia.events.outOfTimeSuperTriviaEvent import \
    OutOfTimeSuperTriviaEvent
from CynanBot.trivia.events.outOfTimeTriviaEvent import OutOfTimeTriviaEvent
from CynanBot.trivia.events.superGameNotReadyCheckAnswerTriviaEvent import \
    SuperGameNotReadyCheckAnswerTriviaEvent
from CynanBot.trivia.events.wrongUserCheckAnswerTriviaEvent import \
    WrongUserCheckAnswerTriviaEvent
from CynanBot.trivia.games.absTriviaGameState import AbsTriviaGameState
from CynanBot.trivia.games.queuedTriviaGameStoreInterface import \
    QueuedTriviaGameStoreInterface
from CynanBot.trivia.games.superTriviaGameState import SuperTriviaGameState
from CynanBot.trivia.games.triviaGameState import TriviaGameState
from CynanBot.trivia.games.triviaGameStoreInterface import \
    TriviaGameStoreInterface
from CynanBot.trivia.games.triviaGameType import TriviaGameType
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.score.triviaScoreRepositoryInterface import \
    TriviaScoreRepositoryInterface
from CynanBot.trivia.specialStatus.shinyTriviaHelper import ShinyTriviaHelper
from CynanBot.trivia.specialStatus.specialTriviaStatus import \
    SpecialTriviaStatus
from CynanBot.trivia.specialStatus.toxicTriviaHelper import ToxicTriviaHelper
from CynanBot.trivia.specialStatus.toxicTriviaPunishment import \
    ToxicTriviaPunishment
from CynanBot.trivia.specialStatus.toxicTriviaPunishmentResult import \
    ToxicTriviaPunishmentResult
from CynanBot.trivia.superTriviaCooldownHelperInterface import \
    SuperTriviaCooldownHelperInterface
from CynanBot.trivia.triviaAnswerCheckerInterface import \
    TriviaAnswerCheckerInterface
from CynanBot.trivia.triviaAnswerCheckResult import TriviaAnswerCheckResult
from CynanBot.trivia.triviaEmoteGeneratorInterface import \
    TriviaEmoteGeneratorInterface
from CynanBot.trivia.triviaEventListener import TriviaEventListener
from CynanBot.trivia.triviaExceptions import (
    TooManyTriviaFetchAttemptsException, UnknownTriviaActionTypeException,
    UnknownTriviaGameTypeException)
from CynanBot.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface
from CynanBot.trivia.triviaRepositories.triviaRepositoryInterface import \
    TriviaRepositoryInterface
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface


class TriviaGameMachine(TriviaGameMachineInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        cutenessRepository: CutenessRepositoryInterface,
        queuedTriviaGameStore: QueuedTriviaGameStoreInterface,
        shinyTriviaHelper: ShinyTriviaHelper,
        superTriviaCooldownHelper: SuperTriviaCooldownHelperInterface,
        timber: TimberInterface,
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
        queueTimeoutSeconds: int = 3,
        sleepTimeSeconds: float = 0.5,
        timeZone: timezone = timezone.utc
    ):
        assert isinstance(backgroundTaskHelper, BackgroundTaskHelper), f"malformed {backgroundTaskHelper=}"
        assert isinstance(cutenessRepository, CutenessRepositoryInterface), f"malformed {cutenessRepository=}"
        assert isinstance(queuedTriviaGameStore, QueuedTriviaGameStoreInterface), f"malformed {queuedTriviaGameStore=}"
        assert isinstance(shinyTriviaHelper, ShinyTriviaHelper), f"malformed {shinyTriviaHelper=}"
        assert isinstance(superTriviaCooldownHelper, SuperTriviaCooldownHelperInterface), f"malformed {superTriviaCooldownHelper=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(toxicTriviaHelper, ToxicTriviaHelper), f"malformed {toxicTriviaHelper=}"
        assert isinstance(triviaAnswerChecker, TriviaAnswerCheckerInterface), f"malformed {triviaAnswerChecker=}"
        assert isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface), f"malformed {triviaEmoteGenerator=}"
        assert isinstance(triviaGameStore, TriviaGameStoreInterface), f"malformed {triviaGameStore=}"
        assert isinstance(triviaIdGenerator, TriviaIdGeneratorInterface), f"malformed {triviaIdGenerator=}"
        assert isinstance(triviaRepository, TriviaRepositoryInterface), f"malformed {triviaRepository=}"
        assert isinstance(triviaScoreRepository, TriviaScoreRepositoryInterface), f"malformed {triviaScoreRepository=}"
        assert isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface), f"malformed {triviaSettingsRepository=}"
        assert isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface), f"malformed {twitchTokensRepository=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        if not utils.isValidNum(queueTimeoutSeconds):
            raise ValueError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        if queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')
        if not utils.isValidNum(sleepTimeSeconds):
            raise ValueError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        if sleepTimeSeconds < 0.25 or sleepTimeSeconds > 3:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        assert isinstance(timeZone, timezone), f"malformed {timeZone=}"

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__cutenessRepository: CutenessRepositoryInterface = cutenessRepository
        self.__queuedTriviaGameStore: QueuedTriviaGameStoreInterface = queuedTriviaGameStore
        self.__shinyTriviaHelper: ShinyTriviaHelper = shinyTriviaHelper
        self.__superTriviaCooldownHelper: SuperTriviaCooldownHelperInterface = superTriviaCooldownHelper
        self.__timber: TimberInterface = timber
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
        self.__queueTimeoutSeconds: float = queueTimeoutSeconds
        self.__sleepTimeSeconds: float = sleepTimeSeconds
        self.__timeZone: timezone = timeZone

        self.__isStarted: bool = False
        self.__eventListener: Optional[TriviaEventListener] = None
        self.__actionQueue: SimpleQueue[AbsTriviaAction] = SimpleQueue()
        self.__eventQueue: SimpleQueue[AbsTriviaEvent] = SimpleQueue()

    async def __applyToxicSuperTriviaPunishment(
        self,
        action: Optional[CheckSuperAnswerTriviaAction],
        state: SuperTriviaGameState
    ) -> Optional[ToxicTriviaPunishmentResult]:
        assert action is None or isinstance(action, CheckSuperAnswerTriviaAction), f"malformed {action=}"
        assert isinstance(state, SuperTriviaGameState), f"malformed {state=}"

        if not state.isToxic():
            return None

        toxicTriviaPunishmentMultiplier = state.getToxicTriviaPunishmentMultiplier()

        if toxicTriviaPunishmentMultiplier <= 0:
            return None

        answeredUserIds = state.getAnsweredUserIds()

        if action is not None:
            del answeredUserIds[action.getUserId()]

        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(state.getTwitchChannel())
        toxicTriviaPunishments: List[ToxicTriviaPunishment] = list()
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

        toxicTriviaPunishments.sort(key = lambda punishment: (punishment.getPunishedByPoints(), punishment.getUserName().lower()))

        return ToxicTriviaPunishmentResult(
            totalPointsStolen = totalPointsStolen,
            toxicTriviaPunishments = toxicTriviaPunishments,
        )

    async def __beginQueuedTriviaGames(self):
        activeChannelsSet: Set[str] = set()
        activeChannelsSet.update(await self.__triviaGameStore.getTwitchChannelsWithActiveSuperGames())
        activeChannelsSet.update(await self.__superTriviaCooldownHelper.getTwitchChannelsInCooldown())

        queuedSuperGames = await self.__queuedTriviaGameStore.popQueuedSuperGames(activeChannelsSet)

        for queuedSuperGame in queuedSuperGames:
            remainingQueueSize = await self.__queuedTriviaGameStore.getQueuedSuperGamesSize(
                twitchChannel = queuedSuperGame.getTwitchChannel()
            )

            self.__timber.log('TriviaGameMachine', f'Starting new queued super trivia game for \"{queuedSuperGame.getTwitchChannel()}\", with {remainingQueueSize} game(s) remaining in their queue (actionId=\"{queuedSuperGame.getActionId()}\")')
            await self.__handleActionStartNewSuperTriviaGame(queuedSuperGame)

    async def __checkAnswer(
        self,
        answer: Optional[str],
        triviaQuestion: AbsTriviaQuestion,
        extras: Optional[Dict[str, Any]] = None
    ) -> TriviaAnswerCheckResult:
        assert isinstance(triviaQuestion, AbsTriviaQuestion), f"malformed {triviaQuestion=}"

        return await self.__triviaAnswerChecker.checkAnswer(answer, triviaQuestion, extras)

    async def __handleActionCheckAnswer(self, action: CheckAnswerTriviaAction):
        assert isinstance(action, CheckAnswerTriviaAction), f"malformed {action=}"
        if action.getTriviaActionType() is not TriviaActionType.CHECK_ANSWER:
            raise RuntimeError(f'TriviaActionType is not {TriviaActionType.CHECK_ANSWER}: \"{action.getTriviaActionType()}\"')

        state = await self.__triviaGameStore.getNormalGame(
            twitchChannel = action.getTwitchChannel(),
            userId = action.getUserId()
        )

        if state is None:
            await self.__submitEvent(GameNotReadyCheckAnswerTriviaEvent(
                actionId = action.getActionId(),
                answer = action.getAnswer(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                twitchChannel = action.getTwitchChannel(),
                userId = action.getUserId(),
                userName = action.getUserName()
            ))
            return

        if state.getUserId() != action.getUserId():
            await self.__submitEvent(WrongUserCheckAnswerTriviaEvent(
                triviaQuestion = state.getTriviaQuestion(),
                actionId = action.getActionId(),
                answer = action.getAnswer(),
                emote = state.getEmote(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                gameId = state.getGameId(),
                twitchChannel = action.getTwitchChannel(),
                userId = action.getUserId(),
                userName = action.getUserName()
            ))
            return

        checkResult = await self.__checkAnswer(
            answer = action.getAnswer(),
            triviaQuestion = state.getTriviaQuestion(),
            extras = {
                'actionId': action.getActionId(),
                'twitchChannel': action.getTwitchChannel(),
                'userId': action.getUserId(),
                'userName': action.getUserName()
            }
        )

        if checkResult is TriviaAnswerCheckResult.INVALID_INPUT:
            await self.__submitEvent(InvalidAnswerInputTriviaEvent(
                triviaQuestion = state.getTriviaQuestion(),
                specialTriviaStatus = state.getSpecialTriviaStatus(),
                actionId = action.getActionId(),
                answer = action.getAnswer(),
                emote = state.getEmote(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                gameId = state.getGameId(),
                twitchChannel = action.getTwitchChannel(),
                userId = action.getUserId(),
                userName = action.getUserName()
            ))
            return

        await self.__removeNormalTriviaGame(
            twitchChannel = action.getTwitchChannel(),
            userId = action.getUserId()
        )

        if checkResult is TriviaAnswerCheckResult.INCORRECT:
            triviaScoreResult = await self.__triviaScoreRepository.incrementTriviaLosses(
                twitchChannel = action.getTwitchChannel(),
                userId = action.getUserId()
            )

            await self.__submitEvent(IncorrectAnswerTriviaEvent(
                triviaQuestion = state.getTriviaQuestion(),
                specialTriviaStatus = state.getSpecialTriviaStatus(),
                actionId = action.getActionId(),
                answer = action.getAnswer(),
                emote = state.getEmote(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                gameId = state.getGameId(),
                twitchChannel = action.getTwitchChannel(),
                userId = action.getUserId(),
                userName = action.getUserName(),
                triviaScoreResult = triviaScoreResult
            ))
            return

        if state.isShiny():
            await self.__shinyTriviaHelper.shinyTriviaWin(
                twitchChannel = state.getTwitchChannel(),
                userId = action.getUserId(),
                userName = action.getUserName()
            )
        elif state.isToxic():
            await self.__toxicTriviaHelper.toxicTriviaWin(
                twitchChannel = state.getTwitchChannel(),
                userId = action.getUserId(),
                userName = action.getUserName()
            )

        cutenessResult = await self.__cutenessRepository.fetchCutenessIncrementedBy(
            incrementAmount = state.getPointsForWinning(),
            twitchChannel = state.getTwitchChannel(),
            userId = action.getUserId(),
            userName = action.getUserName()
        )

        triviaScoreResult = await self.__triviaScoreRepository.incrementTriviaWins(
            twitchChannel = action.getTwitchChannel(),
            userId = action.getUserId()
        )

        await self.__submitEvent(CorrectAnswerTriviaEvent(
            triviaQuestion = state.getTriviaQuestion(),
            cutenessResult = cutenessResult,
            pointsForWinning = state.getPointsForWinning(),
            specialTriviaStatus = state.getSpecialTriviaStatus(),
            actionId = action.getActionId(),
            answer = action.getAnswer(),
            emote = state.getEmote(),
            eventId = await self.__triviaIdGenerator.generateEventId(),
            gameId = state.getGameId(),
            twitchChannel = action.getTwitchChannel(),
            userId = action.getUserId(),
            userName = action.getUserName(),
            triviaScoreResult = triviaScoreResult
        ))

    async def __handleActionCheckSuperAnswer(self, action: CheckSuperAnswerTriviaAction):
        assert isinstance(action, CheckSuperAnswerTriviaAction), f"malformed {action=}"
        if action.getTriviaActionType() is not TriviaActionType.CHECK_SUPER_ANSWER:
            raise RuntimeError(f'TriviaActionType is not {TriviaActionType.CHECK_SUPER_ANSWER}: \"{action.getTriviaActionType()}\"')

        state = await self.__triviaGameStore.getSuperGame(action.getTwitchChannel())

        if state is None:
            await self.__submitEvent(SuperGameNotReadyCheckAnswerTriviaEvent(
                actionId = action.getActionId(),
                answer = action.getAnswer(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                twitchChannel = action.getTwitchChannel(),
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
                'actionId': action.getActionId(),
                'twitchChannel': action.getTwitchChannel(),
                'userId': action.getUserId(),
                'userName': action.getUserName()
            }
        )

        # we're intentionally ONLY checking for TriviaAnswerCheckResult.CORRECT
        if checkResult is not TriviaAnswerCheckResult.CORRECT:
            await self.__submitEvent(IncorrectSuperAnswerTriviaEvent(
                triviaQuestion = state.getTriviaQuestion(),
                specialTriviaStatus = state.getSpecialTriviaStatus(),
                actionId = action.getActionId(),
                answer = action.getAnswer(),
                emote = state.getEmote(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                gameId = state.getGameId(),
                twitchChannel = action.getTwitchChannel(),
                userId = action.getUserId(),
                userName = action.getUserName()
            ))
            return

        await self.__removeSuperTriviaGame(action.getTwitchChannel())
        toxicTriviaPunishmentResult: Optional[ToxicTriviaPunishmentResult] = None
        pointsForWinning = state.getPointsForWinning()

        if state.isShiny():
            await self.__shinyTriviaHelper.shinyTriviaWin(
                twitchChannel = state.getTwitchChannel(),
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
                    userId = action.getUserId(),
                    userName = action.getUserName()
                )

                pointsForWinning = pointsForWinning + toxicTriviaPunishmentResult.getTotalPointsStolen()

        cutenessResult = await self.__cutenessRepository.fetchCutenessIncrementedBy(
            incrementAmount = pointsForWinning,
            twitchChannel = state.getTwitchChannel(),
            userId = action.getUserId(),
            userName = action.getUserName()
        )

        remainingQueueSize = await self.__queuedTriviaGameStore.getQueuedSuperGamesSize(
            twitchChannel = action.getTwitchChannel()
        )

        triviaScoreResult = await self.__triviaScoreRepository.incrementSuperTriviaWins(
            twitchChannel = action.getTwitchChannel(),
            userId = action.getUserId()
        )

        await self.__submitEvent(CorrectSuperAnswerTriviaEvent(
            triviaQuestion = state.getTriviaQuestion(),
            cutenessResult = cutenessResult,
            pointsForWinning = pointsForWinning,
            remainingQueueSize = remainingQueueSize,
            toxicTriviaPunishmentResult = toxicTriviaPunishmentResult,
            specialTriviaStatus = state.getSpecialTriviaStatus(),
            actionId = action.getActionId(),
            answer = action.getAnswer(),
            emote = state.getEmote(),
            eventId = await self.__triviaIdGenerator.generateEventId(),
            gameId = state.getGameId(),
            twitchChannel = action.getTwitchChannel(),
            userId = action.getUserId(),
            userName = action.getUserName(),
            triviaScoreResult = triviaScoreResult
        ))

    async def __handleActionClearSuperTriviaQueue(self, action: ClearSuperTriviaQueueTriviaAction):
        assert isinstance(action, ClearSuperTriviaQueueTriviaAction), f"malformed {action=}"
        if action.getTriviaActionType() is not TriviaActionType.CLEAR_SUPER_TRIVIA_QUEUE:
            raise RuntimeError(f'TriviaActionType is not {TriviaActionType.CLEAR_SUPER_TRIVIA_QUEUE}: \"{action.getTriviaActionType()}\"')

        result = await self.__queuedTriviaGameStore.clearQueuedSuperGames(
            twitchChannel = action.getTwitchChannel()
        )

        self.__timber.log('TriviaGameMachine', f'Cleared Super Trivia game queue for \"{action.getTwitchChannel()}\" (actionId=\"{action.getActionId()}\"): {result.toStr()}')

        await self.__submitEvent(ClearedSuperTriviaQueueTriviaEvent(
            numberOfGamesRemoved = result.getAmountRemoved(),
            previousQueueSize = result.getOldQueueSize(),
            actionId = action.getActionId(),
            eventId = await self.__triviaIdGenerator.generateEventId(),
            twitchChannel = action.getTwitchChannel()
        ))

    async def __handleActionStartNewTriviaGame(self, action: StartNewTriviaGameAction):
        assert isinstance(action, StartNewTriviaGameAction), f"malformed {action=}"
        if action.getTriviaActionType() is not TriviaActionType.START_NEW_GAME:
            raise RuntimeError(f'TriviaActionType is not {TriviaActionType.START_NEW_GAME}: \"{action.getTriviaActionType()}\"')

        now = datetime.now(self.__timeZone)
        state = await self.__triviaGameStore.getNormalGame(
            twitchChannel = action.getTwitchChannel(),
            userId = action.getUserId()
        )

        if state is not None and state.getEndTime() >= now:
            await self.__submitEvent(GameAlreadyInProgressTriviaEvent(
                gameId = state.getGameId(),
                actionId = action.getActionId(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                twitchChannel = action.getTwitchChannel(),
                userId = action.getUserId(),
                userName = action.getUserName()
            ))
            return

        emote = await self.__triviaEmoteGenerator.getNextEmoteFor(action.getTwitchChannel())
        triviaQuestion: Optional[AbsTriviaQuestion] = None
        try:
            triviaQuestion = await self.__triviaRepository.fetchTrivia(
                emote = emote,
                triviaFetchOptions = action.getTriviaFetchOptions()
            )
        except TooManyTriviaFetchAttemptsException as e:
            self.__timber.log('TriviaGameMachine', f'Reached limit on trivia fetch attempts without being able to successfully retrieve a trivia question for \"{action.getTwitchChannel()}\": {e}', e, traceback.format_exc())

        if triviaQuestion is None:
            await self.__submitEvent(FailedToFetchQuestionTriviaEvent(
                actionId = action.getActionId(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                twitchChannel = action.getTwitchChannel(),
                userId = action.getUserId(),
                userName = action.getUserName()
            ))
            return

        specialTriviaStatus: Optional[SpecialTriviaStatus] = None
        pointsForWinning = action.getPointsForWinning()

        if action.isShinyTriviaEnabled() and await self.__shinyTriviaHelper.isShinyTriviaQuestion(
            twitchChannel = action.getTwitchChannel(),
            userId = action.getUserId(),
            userName = action.getUserName()
        ):
            specialTriviaStatus = SpecialTriviaStatus.SHINY
            pointsForWinning = pointsForWinning * action.getShinyMultiplier()

        state = TriviaGameState(
            triviaQuestion = triviaQuestion,
            basePointsForWinning = action.getPointsForWinning(),
            pointsForWinning = pointsForWinning,
            secondsToLive = action.getSecondsToLive(),
            specialTriviaStatus = specialTriviaStatus,
            actionId = action.getActionId(),
            emote = emote,
            twitchChannel = action.getTwitchChannel(),
            userId = action.getUserId(),
            userName = action.getUserName()
        )

        await self.__triviaGameStore.add(state)

        await self.__submitEvent(NewTriviaGameEvent(
            triviaQuestion = triviaQuestion,
            pointsForWinning = pointsForWinning,
            secondsToLive = action.getSecondsToLive(),
            specialTriviaStatus = specialTriviaStatus,
            actionId = action.getActionId(),
            emote = emote,
            eventId = await self.__triviaIdGenerator.generateEventId(),
            gameId = state.getGameId(),
            twitchChannel = action.getTwitchChannel(),
            userId = action.getUserId(),
            userName = action.getUserName()
        ))

    async def __handleActionStartNewSuperTriviaGame(self, action: StartNewSuperTriviaGameAction):
        assert isinstance(action, StartNewSuperTriviaGameAction), f"malformed {action=}"
        if action.getTriviaActionType() is not TriviaActionType.START_NEW_SUPER_GAME:
            raise RuntimeError(f'TriviaActionType is not {TriviaActionType.START_NEW_SUPER_GAME}: \"{action.getTriviaActionType()}\"')

        now = datetime.now(self.__timeZone)
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

        state = await self.__triviaGameStore.getSuperGame(action.getTwitchChannel())
        isSuperTriviaGameCurrentlyInProgress = state is not None and state.getEndTime() >= now

        queueResult = await self.__queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = isSuperTriviaGameCurrentlyInProgress,
            action = action
        )

        if queueResult.getAmountAdded() >= 1:
            self.__timber.log('TriviaGameMachine', f'Queued new Super Trivia game(s) for \"{action.getTwitchChannel()}\" (actionId=\"{action.getActionId()}\"): {queueResult}')

            await self.__submitEvent(NewQueuedSuperTriviaGameEvent(
                numberOfGames = queueResult.getAmountAdded(),
                pointsForWinning = action.getPointsForWinning(),
                secondsToLive = action.getSecondsToLive(),
                shinyMultiplier = action.getShinyMultiplier(),
                actionId = action.getActionId(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                twitchChannel = action.getTwitchChannel()
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

        emote = await self.__triviaEmoteGenerator.getNextEmoteFor(action.getTwitchChannel())
        triviaQuestion: Optional[AbsTriviaQuestion] = None
        try:
            triviaQuestion = await self.__triviaRepository.fetchTrivia(
                emote = emote,
                triviaFetchOptions = action.getTriviaFetchOptions()
            )
        except TooManyTriviaFetchAttemptsException as e:
            self.__timber.log('TriviaGameMachine', f'Reached limit on trivia fetch attempts without being able to successfully retrieve a super trivia question for \"{action.getTwitchChannel()}\": {e}', e, traceback.format_exc())

        if triviaQuestion is None:
            await self.__submitEvent(FailedToFetchQuestionSuperTriviaEvent(
                actionId = action.getActionId(),
                eventId = await self.__triviaIdGenerator.generateEventId(),
                twitchChannel = action.getTwitchChannel()
            ))
            return

        specialTriviaStatus: Optional[SpecialTriviaStatus] = None
        pointsForWinning = action.getPointsForWinning()

        if action.isShinyTriviaEnabled() and await self.__shinyTriviaHelper.isShinySuperTriviaQuestion(
            twitchChannel = action.getTwitchChannel()
        ):
            specialTriviaStatus = SpecialTriviaStatus.SHINY
            pointsForWinning = pointsForWinning * action.getShinyMultiplier()
        elif action.isToxicTriviaEnabled() and await self.__toxicTriviaHelper.isToxicSuperTriviaQuestion(
            twitchChannel = action.getTwitchChannel()
        ):
            specialTriviaStatus = SpecialTriviaStatus.TOXIC
            pointsForWinning = pointsForWinning * action.getToxicMultiplier()

        state = SuperTriviaGameState(
            triviaQuestion = triviaQuestion,
            basePointsForWinning = action.getPointsForWinning(),
            perUserAttempts = action.getPerUserAttempts(),
            pointsForWinning = pointsForWinning,
            regularTriviaPointsForWinning = action.getRegularTriviaPointsForWinning(),
            secondsToLive = action.getSecondsToLive(),
            toxicTriviaPunishmentMultiplier = action.getToxicTriviaPunishmentMultiplier(),
            specialTriviaStatus = specialTriviaStatus,
            actionId = action.getActionId(),
            emote = emote,
            twitchChannel = action.getTwitchChannel()
        )

        await self.__triviaGameStore.add(state)

        await self.__submitEvent(NewSuperTriviaGameEvent(
            triviaQuestion = triviaQuestion,
            pointsForWinning = pointsForWinning,
            secondsToLive = action.getSecondsToLive(),
            specialTriviaStatus = specialTriviaStatus,
            actionId = action.getActionId(),
            emote = emote,
            eventId = await self.__triviaIdGenerator.generateEventId(),
            gameId = state.getGameId(),
            twitchChannel = action.getTwitchChannel(),
        ))

    async def __refreshStatusOfTriviaGames(self):
        await self.__removeDeadTriviaGames()
        await self.__beginQueuedTriviaGames()

    async def __removeDeadTriviaGames(self):
        now = datetime.now(self.__timeZone)
        gameStates = await self.__triviaGameStore.getAll()
        gameStatesToRemove: List[AbsTriviaGameState] = list()

        for state in gameStates:
            if state.getEndTime() < now:
                gameStatesToRemove.append(state)

        for state in gameStatesToRemove:
            if state.getTriviaGameType() is TriviaGameType.NORMAL:
                await self.__removeDeadNormalTriviaGame(state)
            elif state.getTriviaGameType() is TriviaGameType.SUPER:
                await self.__removeDeadSuperTriviaGame(state)
            else:
                raise UnknownTriviaGameTypeException(f'Unknown TriviaGameType (gameId=\"{state.getGameId()}\") (twitchChannel=\"{state.getTwitchChannel()}\") (actionId=\"{state.getActionId()}\"): \"{state.getTriviaGameType()}\"')

    async def __removeDeadNormalTriviaGame(self, state: TriviaGameState):
        assert isinstance(state, TriviaGameState), f"malformed {state=}"

        await self.__removeNormalTriviaGame(
            twitchChannel = state.getTwitchChannel(),
            userId = state.getUserId()
        )

        triviaScoreResult = await self.__triviaScoreRepository.incrementTriviaLosses(
            twitchChannel = state.getTwitchChannel(),
            userId = state.getUserId()
        )

        await self.__submitEvent(OutOfTimeTriviaEvent(
            triviaQuestion = state.getTriviaQuestion(),
            pointsForWinning = state.getPointsForWinning(),
            specialTriviaStatus = state.getSpecialTriviaStatus(),
            actionId = state.getActionId(),
            emote = state.getEmote(),
            eventId = await self.__triviaIdGenerator.generateEventId(),
            gameId = state.getGameId(),
            twitchChannel = state.getTwitchChannel(),
            userId = state.getUserId(),
            userName = state.getUserName(),
            triviaScoreResult = triviaScoreResult
        ))

    async def __removeDeadSuperTriviaGame(self, state: SuperTriviaGameState):
        assert isinstance(state, SuperTriviaGameState), f"malformed {state=}"

        await self.__removeSuperTriviaGame(state.getTwitchChannel())
        toxicTriviaPunishmentResult: Optional[ToxicTriviaPunishmentResult] = None
        pointsForWinning = state.getPointsForWinning()

        if state.isToxic():
            toxicTriviaPunishmentResult = await self.__applyToxicSuperTriviaPunishment(
                action = None,
                state = state
            )

            if toxicTriviaPunishmentResult is not None:
                pointsForWinning = pointsForWinning + toxicTriviaPunishmentResult.getTotalPointsStolen()

        remainingQueueSize = await self.__queuedTriviaGameStore.getQueuedSuperGamesSize(
            twitchChannel = state.getTwitchChannel()
        )

        await self.__submitEvent(OutOfTimeSuperTriviaEvent(
            triviaQuestion = state.getTriviaQuestion(),
            pointsForWinning = pointsForWinning,
            remainingQueueSize = remainingQueueSize,
            toxicTriviaPunishmentResult = toxicTriviaPunishmentResult,
            specialTriviaStatus = state.getSpecialTriviaStatus(),
            actionId = state.getActionId(),
            emote = state.getEmote(),
            eventId = await self.__triviaIdGenerator.generateEventId(),
            gameId = state.getGameId(),
            twitchChannel = state.getTwitchChannel()
        ))

    async def __removeNormalTriviaGame(self, twitchChannel: str, userId: str):
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        await self.__triviaGameStore.removeNormalGame(
            twitchChannel = twitchChannel,
            userId = userId
        )

    async def __removeSuperTriviaGame(self, twitchChannel: str):
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        await self.__triviaGameStore.removeSuperGame(twitchChannel)
        await self.__superTriviaCooldownHelper.update(twitchChannel)

    def setEventListener(self, listener: Optional[TriviaEventListener]):
        assert listener is None or isinstance(listener, TriviaEventListener), f"malformed {listener=}"

        self.__eventListener = listener

    async def __startActionLoop(self):
        while True:
            actions: List[AbsTriviaAction] = list()

            try:
                while not self.__actionQueue.empty():
                    actions.append(self.__actionQueue.get_nowait())
            except queue.Empty as e:
                self.__timber.log('TriviaGameMachine', f'Encountered queue.Empty when building up actions list (queue size: {self.__actionQueue.qsize()}) (actions size: {len(actions)}): {e}', e)

            try:
                for action in actions:
                    triviaActionType = action.getTriviaActionType()

                    if triviaActionType is TriviaActionType.CHECK_ANSWER:
                        await self.__handleActionCheckAnswer(action)
                    elif triviaActionType is TriviaActionType.CHECK_SUPER_ANSWER:
                        await self.__handleActionCheckSuperAnswer(action)
                    elif triviaActionType is TriviaActionType.CLEAR_SUPER_TRIVIA_QUEUE:
                        await self.__handleActionClearSuperTriviaQueue(action)
                    elif triviaActionType is TriviaActionType.START_NEW_GAME:
                        await self.__handleActionStartNewTriviaGame(action)
                    elif triviaActionType is TriviaActionType.START_NEW_SUPER_GAME:
                        await self.__handleActionStartNewSuperTriviaGame(action)
                    else:
                        raise UnknownTriviaActionTypeException(f'Unknown TriviaActionType: \"{triviaActionType}\"')
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
                events: List[AbsTriviaEvent] = list()

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
        assert isinstance(action, AbsTriviaAction), f"malformed {action=}"

        try:
            self.__actionQueue.put(action, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TriviaGameMachine', f'Encountered queue.Full when submitting a new action ({action}) into the action queue (queue size: {self.__actionQueue.qsize()}): {e}', e, traceback.format_exc())

    async def __submitEvent(self, event: AbsTriviaEvent):
        assert isinstance(event, AbsTriviaEvent), f"malformed {event=}"

        try:
            self.__eventQueue.put(event, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TriviaGameMachine', f'Encountered queue.Full when submitting a new event ({event}) into the event queue (queue size: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())
