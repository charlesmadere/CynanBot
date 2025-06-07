import queue
import random
from collections import defaultdict

from frozenlist import FrozenList

from .queuedTriviaGameStoreInterface import QueuedTriviaGameStoreInterface
from ..actions.startNewSuperTriviaGameAction import StartNewSuperTriviaGameAction
from ..addQueuedGamesResult import AddQueuedGamesResult
from ..clearQueuedGamesResult import ClearQueuedGamesResult
from ..settings.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ..triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


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

        self.__queuedSuperGames: dict[str, list[StartNewSuperTriviaGameAction]] = defaultdict(lambda: list())

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
        oldQueueSize = len(queuedSuperGames)

        if action.isQueueActionConsumed:
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

        numberOfGames = action.numberOfGames

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
            if len(queuedSuperGames) < maxSuperTriviaGameQueueSize:
                queuedSuperGames.append(StartNewSuperTriviaGameAction(
                    isQueueActionConsumed = True,
                    isShinyTriviaEnabled = action.isShinyTriviaEnabled,
                    isToxicTriviaEnabled = action.isToxicTriviaEnabled,
                    numberOfGames = 1,
                    perUserAttempts = action.perUserAttempts,
                    pointsForWinning = action.pointsForWinning,
                    regularTriviaPointsForWinning = action.getRegularTriviaPointsForWinning(),
                    secondsToLive = action.secondsToLive,
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

        def shouldShuffle() -> bool:
            for item in queuedSuperGames:
                if item.getTriviaFetchOptions().requiredTriviaSource is not None:
                    return True
            return False

        if shouldShuffle() and oldQueueSize > 0:
            random.shuffle(queuedSuperGames)

        return AddQueuedGamesResult(
            amountAdded = amountAdded,
            newQueueSize = len(queuedSuperGames),
            oldQueueSize = oldQueueSize
        )

    async def clearQueuedSuperGames(
        self,
        twitchChannelId: str
    ) -> ClearQueuedGamesResult:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        queuedSuperGames = self.__queuedSuperGames[twitchChannelId]
        oldQueueSize = len(queuedSuperGames)
        queuedSuperGames.clear()
        amountRemoved = oldQueueSize

        return ClearQueuedGamesResult(
            amountRemoved = amountRemoved,
            oldQueueSize = oldQueueSize
        )

    async def getQueuedSuperGamesSize(
        self,
        twitchChannelId: str
    ) -> int:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if twitchChannelId in self.__queuedSuperGames:
            return len(self.__queuedSuperGames[twitchChannelId])
        else:
            return 0

    async def popQueuedSuperGames(
        self,
        activeChannelIds: set[str]
    ) -> FrozenList[StartNewSuperTriviaGameAction]:
        superGames: FrozenList[StartNewSuperTriviaGameAction] = FrozenList()

        for twitchChannelId, queuedSuperGames in self.__queuedSuperGames.items():
            if twitchChannelId in activeChannelIds:
                continue
            elif len(queuedSuperGames) == 0:
                continue

            try:
                superGames.append(queuedSuperGames.pop(0))
            except queue.Empty as e:
                self.__timber.log('QueuedTriviaGameStore', f'Unable to get queued super game for \"{twitchChannelId}\" (queue size: {len(queuedSuperGames)}): {e}', e)

        superGames.freeze()
        return superGames
