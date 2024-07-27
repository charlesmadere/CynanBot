from datetime import datetime

import pytest

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.trivia.games.superTriviaGameState import SuperTriviaGameState
from src.trivia.games.triviaGameState import TriviaGameState
from src.trivia.games.triviaGameStore import TriviaGameStore
from src.trivia.games.triviaGameStoreInterface import TriviaGameStoreInterface
from src.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from src.trivia.questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from src.trivia.questions.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from src.trivia.questions.triviaSource import TriviaSource
from src.trivia.questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from src.trivia.triviaDifficulty import TriviaDifficulty


class TriviaGameStoreTests:

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    normalQuestion1: AbsTriviaQuestion = MultipleChoiceTriviaQuestion(
        correctAnswers = [ 'Chicago Bullies' ],
        multipleChoiceResponses = [ 'Chicago Bullies', 'Chicago Bulls', 'Minnesota Chipmunks' ],
        category = None,
        categoryId = None,
        question = 'What team is stashiocat a member of?',
        triviaId = 'abc123',
        triviaDifficulty = TriviaDifficulty.UNKNOWN,
        originalTriviaSource = None,
        triviaSource = TriviaSource.WILL_FRY_TRIVIA
    )

    normalQuestion2: AbsTriviaQuestion = TrueFalseTriviaQuestion(
        correctAnswer = True,
        category = None,
        categoryId = None,
        question = 'Is stashiocat a member of the Chicago Bullies?',
        triviaId = 'def456',
        triviaDifficulty = TriviaDifficulty.UNKNOWN,
        originalTriviaSource = None,
        triviaSource = TriviaSource.OPEN_TRIVIA_DATABASE
    )

    normalQuestion3: AbsTriviaQuestion = MultipleChoiceTriviaQuestion(
        correctAnswers = [ 'Nintendo' ],
        multipleChoiceResponses = [ 'Microsoft', 'Nintendo', 'Sega', 'Sony' ],
        category = None,
        categoryId = None,
        question = 'Which company made the SNES?',
        triviaId = 'xyz321',
        triviaDifficulty = TriviaDifficulty.UNKNOWN,
        originalTriviaSource = None,
        triviaSource = TriviaSource.MILLIONAIRE
    )

    superQuestion1: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
        correctAnswers = [ 'Chicago Bullies' ],
        cleanedCorrectAnswers = [ 'chicago bullies' ],
        category = None,
        categoryId = None,
        originalCorrectAnswers = [ 'Chicago Bullies' ],
        question = 'One of this team\'s members is stashiocat.',
        triviaId = 'ghi789',
        triviaDifficulty = TriviaDifficulty.UNKNOWN,
        originalTriviaSource = None,
        triviaSource = TriviaSource.FUNTOON
    )

    superQuestion2: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
        correctAnswers = [ 'stashiocat' ],
        cleanedCorrectAnswers = [ 'stashiocat' ],
        category = None,
        categoryId = None,
        originalCorrectAnswers = [ 'stashiocat' ],
        question = 'This player forgot to fight Phantoon in a randomizer match.',
        triviaId = 'jkl012',
        triviaDifficulty = TriviaDifficulty.UNKNOWN,
        originalTriviaSource = None,
        triviaSource = TriviaSource.J_SERVICE
    )

    game1 = TriviaGameState(
        triviaQuestion = normalQuestion1,
        endTime = datetime.now(timeZoneRepository.getDefault()),
        basePointsForWinning = 5,
        pointsForWinning = 5,
        secondsToLive = 60,
        specialTriviaStatus = None,
        actionId = 'abc123',
        emote = '🍔',
        gameId = 'fdsdsavfdsaf',
        twitchChannel = 'smCharles',
        twitchChannelId = 'c',
        userId = 'e',
        userName = 'Eddie'
    )

    game2 = TriviaGameState(
        triviaQuestion = normalQuestion2,
        endTime = datetime.now(timeZoneRepository.getDefault()),
        basePointsForWinning = 5,
        pointsForWinning = 5,
        secondsToLive = 60,
        specialTriviaStatus = None,
        actionId = 'abc123',
        emote = '🍔',
        gameId = 'qwefsafsa',
        twitchChannel = 'smCharles',
        twitchChannelId = 'c',
        userId = 's',
        userName = 'stashiocat'
    )

    game3 = TriviaGameState(
        triviaQuestion = normalQuestion3,
        endTime = datetime.now(timeZoneRepository.getDefault()),
        basePointsForWinning = 5,
        pointsForWinning = 5,
        secondsToLive = 60,
        specialTriviaStatus = None,
        actionId = 'abc123',
        emote = '🍔',
        gameId = 'fdsadsa',
        twitchChannel = 'Imyt',
        twitchChannelId = 'i',
        userId = 's',
        userName = 'stashiocat'
    )

    game4 = SuperTriviaGameState(
        triviaQuestion = superQuestion1,
        endTime = datetime.now(timeZoneRepository.getDefault()),
        basePointsForWinning = 25,
        perUserAttempts = 2,
        pointsForWinning = 25,
        regularTriviaPointsForWinning = 5,
        secondsToLive = 60,
        toxicTriviaPunishmentMultiplier = 2,
        specialTriviaStatus = None,
        actionId = 'abc123',
        emote = '🍔',
        gameId = 'fdsafdsafsafdsafasz',
        twitchChannel = 'smCharles',
        twitchChannelId = 'c'
    )

    game5 = SuperTriviaGameState(
        triviaQuestion = superQuestion2,
        endTime = datetime.now(timeZoneRepository.getDefault()),
        basePointsForWinning = 25,
        perUserAttempts = 2,
        pointsForWinning = 25,
        regularTriviaPointsForWinning = 5,
        secondsToLive = 60,
        toxicTriviaPunishmentMultiplier = 2,
        specialTriviaStatus = None,
        actionId = 'abc123',
        emote = '🍔',
        gameId = 'fdsafdsfdere',
        twitchChannel = 'imyt',
        twitchChannelId = 'i'
    )

    triviaGameStore: TriviaGameStoreInterface = TriviaGameStore()

    @pytest.mark.asyncio
    async def test_add(self):
        await self.triviaGameStore.add(self.game1)

        games = await self.triviaGameStore.getAll()
        assert len(games) == 1
        assert self.game1 in games

        games = await self.triviaGameStore.getNormalGames()
        assert len(games) == 1
        assert self.game1 in games

        games = await self.triviaGameStore.getSuperGames()
        assert len(games) == 0
        assert self.game1 not in games

        await self.triviaGameStore.add(self.game4)

        games = await self.triviaGameStore.getAll()
        assert len(games) == 2
        assert self.game1 in games
        assert self.game4 in games

        games = await self.triviaGameStore.getNormalGames()
        assert len(games) == 1
        assert self.game1 in games
        assert self.game4 not in games

        games = await self.triviaGameStore.getSuperGames()
        assert len(games) == 1
        assert self.game1 not in games
        assert self.game4 in games

    @pytest.mark.asyncio
    async def test_getAll_isEmptyList(self):
        games = await self.triviaGameStore.getAll()
        assert len(games) == 0

    @pytest.mark.asyncio
    async def test_getNormalGame_isNone(self):
        game = await self.triviaGameStore.getNormalGame(
            twitchChannelId = 'c',
            userId = 'e'
        )

        assert game is None

    @pytest.mark.asyncio
    async def test_getNormalGames_withEmptyTriviaGameStore_returnsEmptyList(self):
        games = await self.triviaGameStore.getNormalGames()
        assert len(games) == 0

    @pytest.mark.asyncio
    async def test_getSuperGame_withEmptyTriviaGameStore_returnsNone(self):
        game = await self.triviaGameStore.getSuperGame(
            twitchChannelId = 'c'
        )

        assert game is None

    @pytest.mark.asyncio
    async def test_getSuperGames_withEmptyTriviaGameStoree_returnsEmptyList(self):
        games = await self.triviaGameStore.getSuperGames()
        assert len(games) == 0

    @pytest.mark.asyncio
    async def test_remove(self):
        # removing a game from an empty TriviaGameStore should do nothing
        result = await self.triviaGameStore.removeNormalGame(
            twitchChannelId = self.game1.getTwitchChannelId(),
            userId = self.game1.getUserId()
        )
        assert result is False

        await self.triviaGameStore.add(self.game1)
        await self.triviaGameStore.add(self.game2)
        await self.triviaGameStore.add(self.game4)

        games = await self.triviaGameStore.getAll()
        assert len(games) == 3
        assert self.game1 in games
        assert self.game2 in games
        assert self.game4 in games

        # try removing a game that does not exist
        result = await self.triviaGameStore.removeNormalGame(
            twitchChannelId = self.game2.getTwitchChannelId(),
            userId = self.game1.getUserId()
        )
        assert result is False

        games = await self.triviaGameStore.getAll()
        assert len(games) == 3
        assert self.game1 in games
        assert self.game2 in games
        assert self.game4 in games

        # remove a game that does exist
        result = await self.triviaGameStore.removeNormalGame(
            twitchChannelId = self.game2.getTwitchChannelId(),
            userId = self.game2.getUserId()
        )
        assert result is True

        games = await self.triviaGameStore.getAll()
        assert len(games) == 2
        assert self.game1 in games
        assert self.game4 in games

        # remove another game that does exist
        result = await self.triviaGameStore.removeNormalGame(
            twitchChannelId = self.game1.getTwitchChannelId(),
            userId = self.game1.getUserId()
        )
        assert result is True

        games = await self.triviaGameStore.getAll()
        assert len(games) == 1
        assert self.game4 in games

        # try one more time to remove the same game that was just removed
        result = await self.triviaGameStore.removeNormalGame(
            twitchChannelId = self.game1.getTwitchChannelId(),
            userId = self.game1.getUserId()
        )
        assert result is False

        games = await self.triviaGameStore.getAll()
        assert len(games) == 1
        assert self.game4 in games

        # try removing an super trivia game that does not exist
        result = await self.triviaGameStore.removeSuperGame(
            twitchChannelId = self.game5.getTwitchChannelId()
        )
        assert result is False

        games = await self.triviaGameStore.getAll()
        assert len(games) == 1
        assert self.game4 in games

        # remove the final super trivia game
        result = await self.triviaGameStore.removeSuperGame(
            twitchChannelId = self.game4.getTwitchChannelId()
        )
        assert result is True

        games = await self.triviaGameStore.getAll()
        assert len(games) == 0

    @pytest.mark.asyncio
    async def test_removeNormalGame_withEmptyTriviaGameStore_returnsFalse(self):
        result = await self.triviaGameStore.removeNormalGame(
            twitchChannelId = self.game3.getTwitchChannelId(),
            userId = self.game3.getUserId()
        )

        assert result is False

    @pytest.mark.asyncio
    async def test_removeSuperGame_withEmptyTriviaGameStore_returnsFalse(self):
        result = await self.triviaGameStore.removeSuperGame(
            twitchChannelId = self.game5.getTwitchChannelId()
        )

        assert result is False

    def test_sanity(self):
        assert self.triviaGameStore is not None
        assert isinstance(self.triviaGameStore, TriviaGameStoreInterface)
