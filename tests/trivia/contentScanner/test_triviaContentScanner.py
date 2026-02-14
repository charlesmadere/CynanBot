import pytest

from src.contentScanner.bannedWordsRepository import BannedWordsRepository
from src.contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from src.contentScanner.contentScanner import ContentScanner
from src.contentScanner.contentScannerInterface import ContentScannerInterface
from src.storage.jsonStaticReader import JsonStaticReader
from src.storage.linesReaderInterface import LinesReaderInterface
from src.storage.linesStaticReader import LinesStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.trivia.content.triviaContentCode import TriviaContentCode
from src.trivia.content.triviaContentScanner import TriviaContentScanner
from src.trivia.content.triviaContentScannerInterface import TriviaContentScannerInterface
from src.trivia.misc.triviaSourceParser import TriviaSourceParser
from src.trivia.misc.triviaSourceParserInterface import TriviaSourceParserInterface
from src.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from src.trivia.questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from src.trivia.questions.questionAnswerTriviaQuestion import QuestionAnswerTriviaQuestion
from src.trivia.questions.triviaSource import TriviaSource
from src.trivia.questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from src.trivia.settings.triviaSettings import TriviaSettings
from src.trivia.settings.triviaSettingsInterface import TriviaSettingsInterface
from src.trivia.triviaDifficulty import TriviaDifficulty


class TestTriviaContentScanner:

    triviaSourceParser: TriviaSourceParserInterface = TriviaSourceParser()

    triviaSettings: TriviaSettingsInterface = TriviaSettings(
        settingsJsonReader = JsonStaticReader(dict()),
        triviaSourceParser = triviaSourceParser,
    )

    bannedWordsLinesReader: LinesReaderInterface = LinesStaticReader(
        lines = [ 'bitch', '"trump"' ],
    )

    timber: TimberInterface = TimberStub()

    bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
        bannedWordsLinesReader = bannedWordsLinesReader,
        timber = timber,
    )

    contentScanner: ContentScannerInterface = ContentScanner(
        bannedWordsRepository = bannedWordsRepository,
        timber = timber,
    )

    triviaContentScanner: TriviaContentScannerInterface = TriviaContentScanner(
        bannedWordsRepository = bannedWordsRepository,
        contentScanner = contentScanner,
        timber = timber,
        triviaSettings = triviaSettings,
    )

    @pytest.mark.asyncio
    async def test_verify_withGnarlyTriviaQuestion1(self):
        question: AbsTriviaQuestion = TrueFalseTriviaQuestion(
            correctAnswer = False,
            category = None,
            categoryId = None,
            question = 'QAnon is Trump fighting the deep state and it\'s real.',
            triviaId = 'asdfasdfasdf',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.OPEN_TRIVIA_QA
        )

        result = await self.triviaContentScanner.verify(question)
        assert result is TriviaContentCode.CONTAINS_BANNED_CONTENT

    @pytest.mark.asyncio
    async def test_verify_withGnarlyTriviaQuestion2(self):
        correctAnswers: list[str] = list()
        correctAnswers.append('two')

        multipleChoiceResponses: list[str] = list()
        multipleChoiceResponses.append('one')
        multipleChoiceResponses.append('two')
        multipleChoiceResponses.append('three')

        question: AbsTriviaQuestion = MultipleChoiceTriviaQuestion(
            correctAnswers = correctAnswers,
            multipleChoiceResponses = multipleChoiceResponses,
            category = None,
            categoryId = None,
            question = 'bitching', # The banned word is actually "bitch", but
                                   # that word is contained within "bitching",
                                   # so this question should end up banned.
            triviaId = 'asdfasdfasdf',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaContentScanner.verify(question)
        assert result is TriviaContentCode.CONTAINS_BANNED_CONTENT

    @pytest.mark.asyncio
    async def test_verify_withTriviaQuestionThatAlmostContainsBannedWord(self):
        # the banned word is "trump", but this answer contains "trumpet", which is not banned
        correctAnswers: list[str] = list()
        correctAnswers.append('a trumpet')

        compiledCorrectAnswers: list[str] = list()
        compiledCorrectAnswers.append('trumpet')

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = None,
            compiledCorrectAnswers = compiledCorrectAnswers,
            correctAnswers = correctAnswers,
            originalCorrectAnswers = correctAnswers,
            category = 'Politics',
            categoryId = None,
            question = 'This instrument is made from brass.',
            triviaId = 'asdfasdfasdf',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON
        )

        result = await self.triviaContentScanner.verify(question)
        assert result is TriviaContentCode.OK

    @pytest.mark.asyncio
    async def test_verify_withNone(self):
        result = await self.triviaContentScanner.verify(None)
        assert result is TriviaContentCode.IS_NONE

    @pytest.mark.asyncio
    async def test_verify_withSimpleTriviaQuestion1(self):
        question: AbsTriviaQuestion = TrueFalseTriviaQuestion(
            correctAnswer = True,
            category = None,
            categoryId = None,
            question = 'What is?',
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.TRIVIA_DATABASE
        )

        result = await self.triviaContentScanner.verify(question)
        assert result is TriviaContentCode.OK

    @pytest.mark.asyncio
    async def test_verify_withSimpleTriviaQuestion2(self):
        correctAnswers: list[bool] = list()
        correctAnswers.append(False)

        question: AbsTriviaQuestion = TrueFalseTriviaQuestion(
            correctAnswer = False,
            category = None,
            categoryId = None,
            question = 'Blah blah question here?',
            triviaId = 'abc456',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaContentScanner.verify(question)
        assert result is TriviaContentCode.OK

    @pytest.mark.asyncio
    async def test_verify_withSimpleTriviaQuestion3(self):
        correctAnswers: list[str] = list()
        correctAnswers.append('Nintendo 64')

        multipleChoiceResponses: list[str] = list()
        multipleChoiceResponses.append('Nintendo Entertainment System')
        multipleChoiceResponses.append('Nintendo 64')
        multipleChoiceResponses.append('Sony PlayStation')

        question: AbsTriviaQuestion = MultipleChoiceTriviaQuestion(
            correctAnswers = correctAnswers,
            multipleChoiceResponses = multipleChoiceResponses,
            category = None,
            categoryId = None,
            question = 'What is \"N64\" an abbreviation for?',
            triviaId = 'qwerty',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.OPEN_TRIVIA_DATABASE
        )

        result = await self.triviaContentScanner.verify(question)
        assert result is TriviaContentCode.OK

    @pytest.mark.asyncio
    async def test_verify_withSimpleTriviaQuestion4(self):
        correctAnswers: list[str] = list()
        correctAnswers.append('(King) James')

        compiledCorrectAnswers: list[str] = list()
        compiledCorrectAnswers.append('(King) James')

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = None,
            compiledCorrectAnswers = compiledCorrectAnswers,
            correctAnswers = correctAnswers,
            originalCorrectAnswers = correctAnswers,
            category = 'The Dark Ages',
            categoryId = None,
            question = 'Who was a king from way back?',
            triviaId = 'azerty',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.OPEN_TRIVIA_DATABASE
        )

        result = await self.triviaContentScanner.verify(question)
        assert result is TriviaContentCode.OK
