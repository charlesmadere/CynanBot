import pytest

from CynanBot.storage.jsonStaticReader import JsonStaticReader
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub
from CynanBot.trivia.actions.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from CynanBot.trivia.games.queuedTriviaGameStore import QueuedTriviaGameStore
from CynanBot.trivia.games.queuedTriviaGameStoreInterface import \
    QueuedTriviaGameStoreInterface
from CynanBot.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface
from CynanBot.trivia.triviaSettingsRepository import TriviaSettingsRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class TestQueuedTriviaGameStore1():

    timber: TimberInterface = TimberStub()

    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict())
    )

    queuedTriviaGameStore: QueuedTriviaGameStoreInterface = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    )

    startNewSuperTriviaGameAction1 = StartNewSuperTriviaGameAction(
        isQueueActionConsumed = False,
        isShinyTriviaEnabled = False,
        isToxicTriviaEnabled = False,
        numberOfGames = 3,
        perUserAttempts = 2,
        pointsForWinning = 25,
        regularTriviaPointsForWinning = 5,
        secondsToLive = 50,
        shinyMultiplier = 8,
        toxicMultiplier = 16,
        toxicTriviaPunishmentMultiplier = 0,
        actionId = 'action1',
        twitchChannel = 'smCharles',
        twitchChannelId = 'c',
        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = 'smCharles',
            twitchChannelId = 'c',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
        )
    )

    startNewSuperTriviaGameAction2 = StartNewSuperTriviaGameAction(
        isQueueActionConsumed = False,
        isShinyTriviaEnabled = False,
        isToxicTriviaEnabled = False,
        numberOfGames = 1,
        perUserAttempts = 2,
        pointsForWinning = 25,
        regularTriviaPointsForWinning = 5,
        secondsToLive = 50,
        shinyMultiplier = 8,
        toxicMultiplier = 16,
        toxicTriviaPunishmentMultiplier = 0,
        actionId = 'action2',
        twitchChannel = 'smCharles',
        twitchChannelId = 'c',
        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = 'smCharles',
            twitchChannelId = 'c',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
        )
    )

    startNewSuperTriviaGameAction3 = StartNewSuperTriviaGameAction(
        isQueueActionConsumed = True,
        isShinyTriviaEnabled = False,
        isToxicTriviaEnabled = False,
        numberOfGames = 1,
        perUserAttempts = 2,
        pointsForWinning = 25,
        regularTriviaPointsForWinning = 5,
        secondsToLive = 50,
        shinyMultiplier = 8,
        toxicMultiplier = 16,
        toxicTriviaPunishmentMultiplier = 0,
        actionId = 'action3',
        twitchChannel = 'smCharles',
        twitchChannelId = 'c',
        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = 'smCharles',
            twitchChannelId = 'c',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
        )
    )

    startNewSuperTriviaGameAction4 = StartNewSuperTriviaGameAction(
        isQueueActionConsumed = False,
        isShinyTriviaEnabled = False,
        isToxicTriviaEnabled = False,
        numberOfGames = 5,
        perUserAttempts = 2,
        pointsForWinning = 25,
        regularTriviaPointsForWinning = 5,
        secondsToLive = 50,
        shinyMultiplier = 8,
        toxicMultiplier = 16,
        toxicTriviaPunishmentMultiplier = 0,
        actionId = 'action4',
        twitchChannel = 'stashiocat',
        twitchChannelId = 's',
        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = 'stashiocat',
            twitchChannelId = 's',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
        )
    )

    @pytest.mark.asyncio
    async def test_addQueuedSuperGamesSize_withEmptyTwitchChannel_andSuperGameIsNotInProgress(self):
        assert self.startNewSuperTriviaGameAction1.isQueueActionConsumed() is False

        addResult = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = False,
            action = self.startNewSuperTriviaGameAction1
        )
        assert addResult.getAmountAdded() == 2
        assert addResult.getNewQueueSize() == 2
        assert addResult.getOldQueueSize() == 0
        assert self.startNewSuperTriviaGameAction1.isQueueActionConsumed() is True

        addResult = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = True,
            action = self.startNewSuperTriviaGameAction1
        )
        assert addResult.getAmountAdded() == 0
        assert addResult.getNewQueueSize() == 2
        assert addResult.getOldQueueSize() == 2
        assert self.startNewSuperTriviaGameAction1.isQueueActionConsumed() is True

        addResult = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = True,
            action = self.startNewSuperTriviaGameAction2
        )
        assert addResult.getAmountAdded() == 1
        assert addResult.getNewQueueSize() == 3
        assert addResult.getOldQueueSize() == 2
        assert self.startNewSuperTriviaGameAction2.isQueueActionConsumed() is True

        addResult = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = True,
            action = self.startNewSuperTriviaGameAction3
        )
        assert addResult.getAmountAdded() == 0
        assert addResult.getNewQueueSize() == 3
        assert addResult.getOldQueueSize() == 3
        assert self.startNewSuperTriviaGameAction3.isQueueActionConsumed() is True

        addResult = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = False,
            action = self.startNewSuperTriviaGameAction4
        )
        assert addResult.getAmountAdded() == 4
        assert addResult.getNewQueueSize() == 4
        assert addResult.getOldQueueSize() == 0
        assert self.startNewSuperTriviaGameAction4.isQueueActionConsumed() is True

    def test_sanity(self):
        assert self.queuedTriviaGameStore is not None
        assert isinstance(self.queuedTriviaGameStore, QueuedTriviaGameStoreInterface)


class TestQueuedTriviaGameStore2():

    timber: TimberInterface = TimberStub()

    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict())
    )

    queuedTriviaGameStore: QueuedTriviaGameStoreInterface = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    )

    @pytest.mark.asyncio
    async def test_getQueuedSuperGamesSize_withEmptyTwitchChannel(self):
        size = await self.queuedTriviaGameStore.getQueuedSuperGamesSize('Oatsngoats')
        assert size == 0

    def test_sanity(self):
        assert self.queuedTriviaGameStore is not None
        assert isinstance(self.queuedTriviaGameStore, QueuedTriviaGameStoreInterface)


class TestQueuedTriviaGameStore3():

    timber: TimberInterface = TimberStub()

    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict())
    )

    queuedTriviaGameStore: QueuedTriviaGameStoreInterface = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    )

    @pytest.mark.asyncio
    async def test_clearQueuedSuperGames_withEmptyTwitchChannel(self):
        clearResult = await self.queuedTriviaGameStore.clearQueuedSuperGames('imyt')
        assert clearResult.getAmountRemoved() == 0
        assert clearResult.getOldQueueSize() == 0

    def test_sanity(self):
        assert self.queuedTriviaGameStore is not None
        assert isinstance(self.queuedTriviaGameStore, QueuedTriviaGameStoreInterface)


class TestQueuedTriviaGameStore4():

    timber: TimberInterface = TimberStub()

    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict())
    )

    queuedTriviaGameStore: QueuedTriviaGameStoreInterface = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    )

    startNewSuperTriviaGameAction = StartNewSuperTriviaGameAction(
        isQueueActionConsumed = False,
        isShinyTriviaEnabled = False,
        isToxicTriviaEnabled = False,
        numberOfGames = 1,
        perUserAttempts = 2,
        pointsForWinning = 25,
        regularTriviaPointsForWinning = 5,
        secondsToLive = 50,
        shinyMultiplier = 8,
        toxicMultiplier = 16,
        toxicTriviaPunishmentMultiplier = 0,
        actionId = 'action5',
        twitchChannel = 'smCharles',
        twitchChannelId = 'c',
        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = 'smCharles',
            twitchChannelId = 'c',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
        )
    )

    @pytest.mark.asyncio
    async def test_addQueuedSuperGamesSize_withEmptyTwitchChannel_andSuperGameIsInProgress(self):
        assert self.startNewSuperTriviaGameAction.isQueueActionConsumed() is False

        result = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = True,
            action = self.startNewSuperTriviaGameAction
        )

        assert result.getAmountAdded() == 1
        assert result.getNewQueueSize() == 1
        assert result.getOldQueueSize() == 0
        assert self.startNewSuperTriviaGameAction.isQueueActionConsumed() is True

    def test_sanity(self):
        assert self.queuedTriviaGameStore is not None
        assert isinstance(self.queuedTriviaGameStore, QueuedTriviaGameStoreInterface)


class TestQueuedTriviaGameStore5():

    timber: TimberInterface = TimberStub()

    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict())
    )

    queuedTriviaGameStore: QueuedTriviaGameStoreInterface = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    )

    startNewSuperTriviaGameAction = StartNewSuperTriviaGameAction(
        isQueueActionConsumed = False,
        isShinyTriviaEnabled = False,
        isToxicTriviaEnabled = False,
        numberOfGames = 5,
        perUserAttempts = 2,
        pointsForWinning = 25,
        regularTriviaPointsForWinning = 5,
        secondsToLive = 50,
        shinyMultiplier = 8,
        toxicMultiplier = 16,
        toxicTriviaPunishmentMultiplier = 0,
        actionId = 'action6',
        twitchChannel = 'stashiocat',
        twitchChannelId = 's',
        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = 'stashiocat',
            twitchChannelId = 's',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
        )
    )

    @pytest.mark.asyncio
    async def test_addQueuedSuperGamesSize_withEmptyTwitchChannel_andSuperGameIsInProgress_andQueueActionConsumedIsTrue(self):
        assert self.startNewSuperTriviaGameAction.isQueueActionConsumed() is False

        result = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = True,
            action = self.startNewSuperTriviaGameAction
        )

        assert result.getAmountAdded() == 5
        assert result.getNewQueueSize() == 5
        assert result.getOldQueueSize() == 0
        assert self.startNewSuperTriviaGameAction.isQueueActionConsumed() is True

    def test_sanity(self):
        assert self.queuedTriviaGameStore is not None
        assert isinstance(self.queuedTriviaGameStore, QueuedTriviaGameStoreInterface)


class TestQueuedTriviaGameStore6():

    timber: TimberInterface = TimberStub()

    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict())
    )

    queuedTriviaGameStore: QueuedTriviaGameStoreInterface = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    )

    startNewSuperTriviaGameAction = StartNewSuperTriviaGameAction(
        isQueueActionConsumed = False,
        isShinyTriviaEnabled = False,
        isToxicTriviaEnabled = False,
        numberOfGames = 3,
        perUserAttempts = 2,
        pointsForWinning = 25,
        regularTriviaPointsForWinning = 5,
        secondsToLive = 50,
        shinyMultiplier = 8,
        toxicMultiplier = 16,
        toxicTriviaPunishmentMultiplier = 0,
        actionId = 'action7',
        twitchChannel = 'smCharles',
        twitchChannelId = 'c',
        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = 'smCharles',
            twitchChannelId = 'c',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
        )
    )

    @pytest.mark.asyncio
    async def test_clearQueuedSuperGames(self):
        assert self.startNewSuperTriviaGameAction.isQueueActionConsumed() is False

        clearResult = await self.queuedTriviaGameStore.clearQueuedSuperGames(
            twitchChannelId = self.startNewSuperTriviaGameAction.getTwitchChannelId()
        )
        assert clearResult.getAmountRemoved() == 0
        assert clearResult.getOldQueueSize() == 0

        addResult = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = False,
            action = self.startNewSuperTriviaGameAction
        )
        assert addResult.getAmountAdded() == 2
        assert addResult.getNewQueueSize() == 2
        assert addResult.getOldQueueSize() == 0
        assert self.startNewSuperTriviaGameAction.isQueueActionConsumed()

        queueSize = await self.queuedTriviaGameStore.getQueuedSuperGamesSize(
            twitchChannelId = self.startNewSuperTriviaGameAction.getTwitchChannelId()
        )
        assert queueSize == 2

        clearResult = await self.queuedTriviaGameStore.clearQueuedSuperGames(
            twitchChannelId = self.startNewSuperTriviaGameAction.getTwitchChannelId()
        )
        assert clearResult.getAmountRemoved() == 2
        assert clearResult.getOldQueueSize() == 2

        queueSize = await self.queuedTriviaGameStore.getQueuedSuperGamesSize(
            twitchChannelId = self.startNewSuperTriviaGameAction.getTwitchChannelId()
        )
        assert queueSize == 0

    def test_sanity(self):
        assert self.queuedTriviaGameStore is not None
        assert isinstance(self.queuedTriviaGameStore, QueuedTriviaGameStoreInterface)


class TestQueuedTriviaGameStore7():

    timber: TimberInterface = TimberStub()

    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict())
    )

    queuedTriviaGameStore: QueuedTriviaGameStoreInterface = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    )

    startNewSuperTriviaGameAction = StartNewSuperTriviaGameAction(
        isQueueActionConsumed = False,
        isShinyTriviaEnabled = False,
        isToxicTriviaEnabled = False,
        numberOfGames = 1,
        perUserAttempts = 2,
        pointsForWinning = 25,
        regularTriviaPointsForWinning = 5,
        secondsToLive = 50,
        shinyMultiplier = 8,
        toxicMultiplier = 16,
        toxicTriviaPunishmentMultiplier = 0,
        actionId = 'action8',
        twitchChannel = 'smCharles',
        twitchChannelId = 'c',
        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = 'smCharles',
            twitchChannelId = 'c',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
        )
    )

    @pytest.mark.asyncio
    async def test_clearQueuedSuperGames_isCaseInsensitive(self):
        assert self.startNewSuperTriviaGameAction.isQueueActionConsumed() is False

        clearResult = await self.queuedTriviaGameStore.clearQueuedSuperGames('c')
        assert clearResult.getAmountRemoved() == 0
        assert clearResult.getOldQueueSize() == 0

        addResult = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = True,
            action = self.startNewSuperTriviaGameAction
        )
        assert addResult.getAmountAdded() == 1
        assert addResult.getNewQueueSize() == 1
        assert addResult.getOldQueueSize() == 0

        queueSize = await self.queuedTriviaGameStore.getQueuedSuperGamesSize('c')
        assert queueSize == 1

        queueSize = await self.queuedTriviaGameStore.getQueuedSuperGamesSize('c')
        assert queueSize == 1

        clearResult = await self.queuedTriviaGameStore.clearQueuedSuperGames('c')
        assert clearResult.getAmountRemoved() == 1
        assert clearResult.getOldQueueSize() == 1

        queueSize = await self.queuedTriviaGameStore.getQueuedSuperGamesSize('c')
        assert queueSize == 0

    def test_sanity(self):
        assert self.queuedTriviaGameStore is not None
        assert isinstance(self.queuedTriviaGameStore, QueuedTriviaGameStoreInterface)
