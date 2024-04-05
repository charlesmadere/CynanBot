import queue
from collections import defaultdict
from queue import SimpleQueue

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.actions.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from CynanBot.trivia.addQueuedGamesResult import AddQueuedGamesResult
from CynanBot.trivia.clearQueuedGamesResult import ClearQueuedGamesResult
from CynanBot.trivia.games.queuedTriviaGameStoreInterface import \
    QueuedTriviaGameStoreInterface
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class QueuedTriviaGameStore(QueuedTriviaGameStoreInterface):

    def __init__(
        self,
        timber: TimberInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        queueTimeoutSeconds: float = 3
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__timber: TimberInterface = timber
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository
        self.__queueTimeoutSeconds: float = queueTimeoutSeconds

        self.__queuedSuperGames: dict[str, SimpleQueue[StartNewSuperTriviaGameAction]] = defaultdict(lambda: SimpleQueue())

    async def addSuperGames(
        self,
        isSuperTriviaGameCurrentlyInProgress: bool,
        action: StartNewSuperTriviaGameAction
    ) -> AddQueuedGamesResult:
        if not utils.isValidBool(isSuperTriviaGameCurrentlyInProgress):
            raise TypeError(f'isSuperTriviaGameCurrentlyInProgress argument is malformed: \"{isSuperTriviaGameCurrentlyInProgress}\"')
        elif not isinstance(action, StartNewSuperTriviaGameAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        queuedSuperGames = self.__queuedSuperGames[action.getTwitchChannelId()]
        oldQueueSize = queuedSuperGames.qsize()

        if action.isQueueActionConsumed():
            return AddQueuedGamesResult(
                amountAdded = 0,
                newQueueSize = oldQueueSize,
                oldQueueSize = oldQueueSize
            )

        action.consumeQueueAction()
        maxSuperTriviaGameQueueSize = await self.__triviaSettingsRepository.getMaxSuperTriviaGameQueueSize()

        if maxSuperTriviaGameQueueSize < 1:
            return AddQueuedGamesResult(
                amountAdded = 0,
                newQueueSize = oldQueueSize,
                oldQueueSize = oldQueueSize
            )

        numberOfGames = action.getNumberOfGames()

        if not isSuperTriviaGameCurrentlyInProgress:
            numberOfGames = numberOfGames - 1

            if numberOfGames < 1:
                return AddQueuedGamesResult(
                    amountAdded = 0,
                    newQueueSize = oldQueueSize,
                    oldQueueSize = oldQueueSize
                )

        amountAdded = 0

        for _ in range(numberOfGames):
            if queuedSuperGames.qsize() < maxSuperTriviaGameQueueSize:
                queuedSuperGames.put(StartNewSuperTriviaGameAction(
                    isQueueActionConsumed = True,
                    isShinyTriviaEnabled = action.isShinyTriviaEnabled(),
                    isToxicTriviaEnabled = action.isToxicTriviaEnabled(),
                    numberOfGames = 1,
                    perUserAttempts = action.getPerUserAttempts(),
                    pointsForWinning = action.getPointsForWinning(),
                    regularTriviaPointsForWinning = action.getRegularTriviaPointsForWinning(),
                    secondsToLive = action.getSecondsToLive(),
                    shinyMultiplier = action.getShinyMultiplier(),
                    toxicMultiplier = action.getToxicMultiplier(),
                    toxicTriviaPunishmentMultiplier = action.getToxicTriviaPunishmentMultiplier(),
                    actionId = await self.__triviaIdGenerator.generateActionId(),
                    twitchChannel = action.getTwitchChannel(),
                    twitchChannelId = action.getTwitchChannelId(),
                    triviaFetchOptions = action.getTriviaFetchOptions()
                ))

                amountAdded += 1
            else:
                break

        return AddQueuedGamesResult(
            amountAdded = amountAdded,
            newQueueSize = queuedSuperGames.qsize(),
            oldQueueSize = oldQueueSize
        )

    async def clearQueuedSuperGames(self, twitchChannelId: str) -> ClearQueuedGamesResult:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        queuedSuperGames = self.__queuedSuperGames[twitchChannelId]
        oldQueueSize = queuedSuperGames.qsize()
        amountRemoved = 0

        try:
            while not queuedSuperGames.empty():
                queuedSuperGames.get(block = True, timeout = self.__queueTimeoutSeconds)
                amountRemoved = amountRemoved + 1
        except queue.Empty as e:
            self.__timber.log('QueuedTriviaGameStore', f'Unable to clear all queued super games for \"{twitchChannelId}\" (queue size: {queuedSuperGames.qsize()}) (oldQueueSize: {oldQueueSize}): {e}', e)

        return ClearQueuedGamesResult(
            amountRemoved = amountRemoved,
            oldQueueSize = oldQueueSize
        )

    async def getQueuedSuperGamesSize(self, twitchChannelId: str) -> int:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if twitchChannelId in self.__queuedSuperGames:
            return self.__queuedSuperGames[twitchChannelId].qsize()
        else:
            return 0

    async def popQueuedSuperGames(self, activeChannelIds: set[str]) -> list[StartNewSuperTriviaGameAction]:
        superGames: list[StartNewSuperTriviaGameAction] = list()

        for twitchChannelId, queuedSuperGames in self.__queuedSuperGames.items():
            if twitchChannelId in activeChannelIds:
                continue
            elif queuedSuperGames.empty():
                continue

            try:
                superGames.append(queuedSuperGames.get(block = True, timeout = self.__queueTimeoutSeconds))
            except queue.Empty as e:
                self.__timber.log('QueuedTriviaGameStore', f'Unable to get queued super game for \"{twitchChannelId}\" (queue size: {queuedSuperGames.qsize()}): {e}', e)

        return superGames
