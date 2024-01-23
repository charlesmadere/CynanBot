from typing import List

import pytest

from CynanBot.contentScanner.bannedWordsRepository import BannedWordsRepository
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.contentScanner.contentScanner import ContentScanner
from CynanBot.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBot.storage.jsonStaticReader import JsonStaticReader
from CynanBot.storage.linesReaderInterface import LinesReaderInterface
from CynanBot.storage.linesStaticReader import LinesStaticReader
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from CynanBot.trivia.questions.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.questions.trueFalseTriviaQuestion import \
    TrueFalseTriviaQuestion
from CynanBot.trivia.content.triviaContentCode import TriviaContentCode
from CynanBot.trivia.content.triviaContentScanner import TriviaContentScanner
from CynanBot.trivia.content.triviaContentScannerInterface import \
    TriviaContentScannerInterface
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaSettingsRepository import TriviaSettingsRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class TestTriviaContentScanner():

    triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict())
    )

    bannedWordsLinesReader: LinesReaderInterface = LinesStaticReader(
        lines = [ 'bitch', '"trump"' ]
    )

    timber: TimberInterface = TimberStub()

    bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
        bannedWordsLinesReader = bannedWordsLinesReader,
        timber = timber
    )

    contentScanner: ContentScannerInterface = ContentScanner(
        bannedWordsRepository = bannedWordsRepository,
        timber = timber
    )

    triviaContentScanner: TriviaContentScannerInterface = TriviaContentScanner(
        bannedWordsRepository = bannedWordsRepository,
        contentScanner = contentScanner,
        timber = timber,
        triviaSettingsRepository = triviaSettingsRepository
    )

    @pytest.mark.asyncio
    async def test_verify_withGnarlyTriviaQuestion1(self):
        correctAnswers: List[bool] = list()
        correctAnswers.append(False)

        question: AbsTriviaQuestion = TrueFalseTriviaQuestion(
            correctAnswers = correctAnswers,
            category = None,
            categoryId = None,
            question = 'QAnon is Trump fighting the deep state and it\'s real.',
            triviaId = 'asdfasdfasdf',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            triviaSource = TriviaSource.OPEN_TRIVIA_QA
        )

        result = await self.triviaContentScanner.verify(question)
        assert result is TriviaContentCode.CONTAINS_BANNED_CONTENT

    @pytest.mark.asyncio
    async def test_verify_withGnarlyTriviaQuestion2(self):
        correctAnswers: List[bool] = list()
        correctAnswers.append('two')

        multipleChoiceResponses: List[str] = list()
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
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaContentScanner.verify(question)
        assert result is TriviaContentCode.CONTAINS_BANNED_CONTENT

    @pytest.mark.asyncio
    async def test_verify_withTriviaQuestionThatAlmostContainsBannedWord(self):
        # the banned word is "trump", but this answer contains "trumpet", which is not banned
        correctAnswers: List[str] = list()
        correctAnswers.append('a trumpet')

        cleanedCorrectAnswers: List[str] = list()
        cleanedCorrectAnswers.append('trumpet')

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers = correctAnswers,
            cleanedCorrectAnswers = cleanedCorrectAnswers,
            category = 'Politics',
            categoryId = None,
            question = 'This instrument is made from brass.', 
            triviaId = 'asdfasdfasdf',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
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
        correctAnswers: List[bool] = list()
        correctAnswers.append(True)

        question: AbsTriviaQuestion = TrueFalseTriviaQuestion(
            correctAnswers = correctAnswers,
            category = None,
            categoryId = None,
            question = 'What is?',
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            triviaSource = TriviaSource.TRIVIA_DATABASE
        )

        result = await self.triviaContentScanner.verify(question)
        assert result is TriviaContentCode.OK

    @pytest.mark.asyncio
    async def test_verify_withSimpleTriviaQuestion2(self):
        correctAnswers: List[bool] = list()
        correctAnswers.append(False)

        question: AbsTriviaQuestion = TrueFalseTriviaQuestion(
            correctAnswers = correctAnswers,
            category = None,
            categoryId = None,
            question = 'Blah blah question here?',
            triviaId = 'abc456',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaContentScanner.verify(question)
        assert result is TriviaContentCode.OK

    @pytest.mark.asyncio
    async def test_verify_withSimpleTriviaQuestion3(self):
        correctAnswers: List[str] = list()
        correctAnswers.append('Nintendo 64')

        multipleChoiceResponses: List[str] = list()
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
            triviaSource = TriviaSource.OPEN_TRIVIA_DATABASE
        )

        result = await self.triviaContentScanner.verify(question)
        assert result is TriviaContentCode.OK

    @pytest.mark.asyncio
    async def test_verify_withSimpleTriviaQuestion4(self):
        correctAnswers: List[str] = list()
        correctAnswers.append('(King) James')

        cleanedCorrectAnswers: List[str] = list()
        cleanedCorrectAnswers.append('(King) James')

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers = correctAnswers,
            cleanedCorrectAnswers = cleanedCorrectAnswers,
            category = 'The Dark Ages',
            categoryId = None,
            question = 'Who was a king from way back?',
            triviaId = 'azerty',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            triviaSource = TriviaSource.OPEN_TRIVIA_DATABASE
        )

        result = await self.triviaContentScanner.verify(question)
        assert result is TriviaContentCode.OK
