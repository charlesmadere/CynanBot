import pytest

from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.trivia.actions.startNewSuperTriviaGameAction import StartNewSuperTriviaGameAction
from src.trivia.games.queuedTriviaGameStore import QueuedTriviaGameStore
from src.trivia.games.queuedTriviaGameStoreInterface import QueuedTriviaGameStoreInterface
from src.trivia.misc.triviaSourceParser import TriviaSourceParser
from src.trivia.misc.triviaSourceParserInterface import TriviaSourceParserInterface
from src.trivia.questionAnswerTriviaConditions import QuestionAnswerTriviaConditions
from src.trivia.settings.triviaSettings import TriviaSettings
from src.trivia.settings.triviaSettingsInterface import TriviaSettingsInterface
from src.trivia.triviaFetchOptions import TriviaFetchOptions
from src.trivia.triviaIdGenerator import TriviaIdGenerator
from src.trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface


class TestQueuedTriviaGameStore1:

    timber: TimberInterface = TimberStub()

    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    triviaSourceParser: TriviaSourceParserInterface = TriviaSourceParser()

    triviaSettings: TriviaSettingsInterface = TriviaSettings(
        settingsJsonReader = JsonStaticReader(dict()),
        triviaSourceParser = triviaSourceParser,
    )

    queuedTriviaGameStore: QueuedTriviaGameStoreInterface = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettings = triviaSettings,
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
        assert not self.startNewSuperTriviaGameAction1.isQueueActionConsumed

        addResult = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = False,
            action = self.startNewSuperTriviaGameAction1
        )
        assert addResult.amountAdded == 2
        assert addResult.newQueueSize == 2
        assert addResult.oldQueueSize == 0
        assert self.startNewSuperTriviaGameAction1.isQueueActionConsumed

        addResult = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = True,
            action = self.startNewSuperTriviaGameAction1
        )
        assert addResult.amountAdded == 0
        assert addResult.newQueueSize == 2
        assert addResult.oldQueueSize == 2
        assert self.startNewSuperTriviaGameAction1.isQueueActionConsumed

        addResult = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = True,
            action = self.startNewSuperTriviaGameAction2
        )
        assert addResult.amountAdded == 1
        assert addResult.newQueueSize == 3
        assert addResult.oldQueueSize == 2
        assert self.startNewSuperTriviaGameAction2.isQueueActionConsumed

        addResult = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = True,
            action = self.startNewSuperTriviaGameAction3
        )
        assert addResult.amountAdded == 0
        assert addResult.newQueueSize == 3
        assert addResult.oldQueueSize == 3
        assert self.startNewSuperTriviaGameAction3.isQueueActionConsumed

        addResult = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = False,
            action = self.startNewSuperTriviaGameAction4
        )
        assert addResult.amountAdded == 4
        assert addResult.newQueueSize == 4
        assert addResult.oldQueueSize == 0
        assert self.startNewSuperTriviaGameAction4.isQueueActionConsumed

    def test_sanity(self):
        assert self.queuedTriviaGameStore is not None
        assert isinstance(self.queuedTriviaGameStore, QueuedTriviaGameStoreInterface)


class TestQueuedTriviaGameStore2:

    timber: TimberInterface = TimberStub()

    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    triviaSourceParser: TriviaSourceParserInterface = TriviaSourceParser()

    triviaSettings: TriviaSettingsInterface = TriviaSettings(
        settingsJsonReader = JsonStaticReader(dict()),
        triviaSourceParser = triviaSourceParser,
    )

    queuedTriviaGameStore: QueuedTriviaGameStoreInterface = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettings = triviaSettings,
    )

    @pytest.mark.asyncio
    async def test_getQueuedSuperGamesSize_withEmptyTwitchChannel(self):
        size = await self.queuedTriviaGameStore.getQueuedSuperGamesSize('Oatsngoats')
        assert size == 0

    def test_sanity(self):
        assert self.queuedTriviaGameStore is not None
        assert isinstance(self.queuedTriviaGameStore, QueuedTriviaGameStoreInterface)


class TestQueuedTriviaGameStore3:

    timber: TimberInterface = TimberStub()

    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    triviaSourceParser: TriviaSourceParserInterface = TriviaSourceParser()

    triviaSettings: TriviaSettingsInterface = TriviaSettings(
        settingsJsonReader = JsonStaticReader(dict()),
        triviaSourceParser = triviaSourceParser,
    )

    queuedTriviaGameStore: QueuedTriviaGameStoreInterface = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettings = triviaSettings,
    )

    @pytest.mark.asyncio
    async def test_clearQueuedSuperGames_withEmptyTwitchChannel(self):
        clearResult = await self.queuedTriviaGameStore.clearQueuedSuperGames('imyt')
        assert clearResult.amountRemoved == 0
        assert clearResult.oldQueueSize == 0

    def test_sanity(self):
        assert self.queuedTriviaGameStore is not None
        assert isinstance(self.queuedTriviaGameStore, QueuedTriviaGameStoreInterface)


class TestQueuedTriviaGameStore4:

    timber: TimberInterface = TimberStub()

    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    triviaSourceParser: TriviaSourceParserInterface = TriviaSourceParser()

    triviaSettings: TriviaSettingsInterface = TriviaSettings(
        settingsJsonReader = JsonStaticReader(dict()),
        triviaSourceParser = triviaSourceParser,
    )

    queuedTriviaGameStore: QueuedTriviaGameStoreInterface = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettings = triviaSettings,
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
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED,
        ),
    )

    @pytest.mark.asyncio
    async def test_addQueuedSuperGamesSize_withEmptyTwitchChannel_andSuperGameIsInProgress(self):
        assert not self.startNewSuperTriviaGameAction.isQueueActionConsumed

        result = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = True,
            action = self.startNewSuperTriviaGameAction
        )

        assert result.amountAdded == 1
        assert result.newQueueSize == 1
        assert result.oldQueueSize == 0
        assert self.startNewSuperTriviaGameAction.isQueueActionConsumed

    def test_sanity(self):
        assert self.queuedTriviaGameStore is not None
        assert isinstance(self.queuedTriviaGameStore, QueuedTriviaGameStoreInterface)


class TestQueuedTriviaGameStore5:

    timber: TimberInterface = TimberStub()

    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    triviaSourceParser: TriviaSourceParserInterface = TriviaSourceParser()

    triviaSettings: TriviaSettingsInterface = TriviaSettings(
        settingsJsonReader = JsonStaticReader(dict()),
        triviaSourceParser = triviaSourceParser,
    )

    queuedTriviaGameStore: QueuedTriviaGameStoreInterface = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettings = triviaSettings,
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
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED,
        ),
    )

    @pytest.mark.asyncio
    async def test_addQueuedSuperGamesSize_withEmptyTwitchChannel_andSuperGameIsInProgress_andQueueActionConsumedIsTrue(self):
        assert not self.startNewSuperTriviaGameAction.isQueueActionConsumed

        result = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = True,
            action = self.startNewSuperTriviaGameAction
        )

        assert result.amountAdded == 5
        assert result.newQueueSize == 5
        assert result.oldQueueSize == 0
        assert self.startNewSuperTriviaGameAction.isQueueActionConsumed

    def test_sanity(self):
        assert self.queuedTriviaGameStore is not None
        assert isinstance(self.queuedTriviaGameStore, QueuedTriviaGameStoreInterface)


class TestQueuedTriviaGameStore6:

    timber: TimberInterface = TimberStub()

    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    triviaSourceParser: TriviaSourceParserInterface = TriviaSourceParser()

    triviaSettings: TriviaSettingsInterface = TriviaSettings(
        settingsJsonReader = JsonStaticReader(dict()),
        triviaSourceParser = triviaSourceParser,
    )

    queuedTriviaGameStore: QueuedTriviaGameStoreInterface = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettings = triviaSettings,
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
        assert not self.startNewSuperTriviaGameAction.isQueueActionConsumed

        clearResult = await self.queuedTriviaGameStore.clearQueuedSuperGames(
            twitchChannelId = self.startNewSuperTriviaGameAction.getTwitchChannelId()
        )
        assert clearResult.amountRemoved == 0
        assert clearResult.oldQueueSize == 0

        addResult = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = False,
            action = self.startNewSuperTriviaGameAction
        )
        assert addResult.amountAdded == 2
        assert addResult.newQueueSize == 2
        assert addResult.oldQueueSize == 0
        assert self.startNewSuperTriviaGameAction.isQueueActionConsumed

        queueSize = await self.queuedTriviaGameStore.getQueuedSuperGamesSize(
            twitchChannelId = self.startNewSuperTriviaGameAction.getTwitchChannelId()
        )
        assert queueSize == 2

        clearResult = await self.queuedTriviaGameStore.clearQueuedSuperGames(
            twitchChannelId = self.startNewSuperTriviaGameAction.getTwitchChannelId()
        )
        assert clearResult.amountRemoved == 2
        assert clearResult.oldQueueSize == 2

        queueSize = await self.queuedTriviaGameStore.getQueuedSuperGamesSize(
            twitchChannelId = self.startNewSuperTriviaGameAction.getTwitchChannelId()
        )
        assert queueSize == 0

    def test_sanity(self):
        assert self.queuedTriviaGameStore is not None
        assert isinstance(self.queuedTriviaGameStore, QueuedTriviaGameStoreInterface)


class TestQueuedTriviaGameStore7:

    timber: TimberInterface = TimberStub()

    triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()

    triviaSourceParser: TriviaSourceParserInterface = TriviaSourceParser()

    triviaSettings: TriviaSettingsInterface = TriviaSettings(
        settingsJsonReader = JsonStaticReader(dict()),
        triviaSourceParser = triviaSourceParser,
    )

    queuedTriviaGameStore: QueuedTriviaGameStoreInterface = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettings = triviaSettings,
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
        assert not self.startNewSuperTriviaGameAction.isQueueActionConsumed

        clearResult = await self.queuedTriviaGameStore.clearQueuedSuperGames('c')
        assert clearResult.amountRemoved == 0
        assert clearResult.oldQueueSize == 0

        addResult = await self.queuedTriviaGameStore.addSuperGames(
            isSuperTriviaGameCurrentlyInProgress = True,
            action = self.startNewSuperTriviaGameAction
        )
        assert addResult.amountAdded == 1
        assert addResult.newQueueSize == 1
        assert addResult.oldQueueSize == 0

        queueSize = await self.queuedTriviaGameStore.getQueuedSuperGamesSize('c')
        assert queueSize == 1

        queueSize = await self.queuedTriviaGameStore.getQueuedSuperGamesSize('c')
        assert queueSize == 1

        clearResult = await self.queuedTriviaGameStore.clearQueuedSuperGames('c')
        assert clearResult.amountRemoved == 1
        assert clearResult.oldQueueSize == 1

        queueSize = await self.queuedTriviaGameStore.getQueuedSuperGamesSize('c')
        assert queueSize == 0

    def test_sanity(self):
        assert self.queuedTriviaGameStore is not None
        assert isinstance(self.queuedTriviaGameStore, QueuedTriviaGameStoreInterface)
