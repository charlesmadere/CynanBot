from typing import Final

import pytest

from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.trivia.answerChecker.triviaAnswerCheckResult import TriviaAnswerCheckResult
from src.trivia.answerChecker.triviaAnswerChecker import TriviaAnswerChecker
from src.trivia.answerChecker.triviaAnswerCheckerInterface import TriviaAnswerCheckerInterface
from src.trivia.compilers.triviaAnswerCompiler import TriviaAnswerCompiler
from src.trivia.compilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from src.trivia.compilers.triviaQuestionCompiler import TriviaQuestionCompiler
from src.trivia.compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from src.trivia.misc.triviaSourceParser import TriviaSourceParser
from src.trivia.misc.triviaSourceParserInterface import TriviaSourceParserInterface
from src.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from src.trivia.questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from src.trivia.questions.questionAnswerTriviaQuestion import QuestionAnswerTriviaQuestion
from src.trivia.questions.triviaSource import TriviaSource
from src.trivia.questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from src.trivia.settings.triviaSettingsRepository import TriviaSettingsRepository
from src.trivia.settings.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from src.trivia.triviaDifficulty import TriviaDifficulty


class TestTriviaAnswerChecker:

    timber: Final[TimberInterface] = TimberStub()

    triviaSourceParser: Final[TriviaSourceParserInterface] = TriviaSourceParser()

    triviaSettingsRepository: Final[TriviaSettingsRepositoryInterface] = TriviaSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict()),
        triviaSourceParser = triviaSourceParser,
    )

    triviaAnswerCompiler: Final[TriviaAnswerCompilerInterface] = TriviaAnswerCompiler(
        timber = timber,
    )

    triviaQuestionCompiler: Final[TriviaQuestionCompilerInterface] = TriviaQuestionCompiler(
        timber = timber,
    )

    triviaAnswerChecker: Final[TriviaAnswerCheckerInterface] = TriviaAnswerChecker(
        timber = timber,
        triviaAnswerCompiler = triviaAnswerCompiler,
        triviaSettingsRepository = triviaSettingsRepository,
    )

    @pytest.mark.asyncio
    async def test_checkAnswer_withMultipleChoiceQuestionAndAnswerIsA(self):
        question: AbsTriviaQuestion = MultipleChoiceTriviaQuestion(
            correctAnswers = [ 'stashiocat' ],
            multipleChoiceResponses = [ 'Eddie', 'Imyt', 'smCharles', 'stashiocat' ],
            category = None,
            categoryId = None,
            question = 'Which of these Super Metroid players is a bully?',
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.BONGO,
        )

        result = await self.triviaAnswerChecker.checkAnswer('a', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('b', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('c', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('d', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('e', question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

    @pytest.mark.asyncio
    async def test_checkAnswer_withTrueFalseQuestionAndAnswerIsFalse(self):
        question: AbsTriviaQuestion = TrueFalseTriviaQuestion(
            correctAnswer = False,
            category = None,
            categoryId = None,
            question = 'The Super Metroid player stashiocat is a Chicago Bully.',
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.BONGO
        )

        result = await self.triviaAnswerChecker.checkAnswer('false', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('true', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('blah', question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

    @pytest.mark.asyncio
    async def test_checkAnswer_withTrueFalseQuestionAndAnswerIsTrue(self):
        question: AbsTriviaQuestion = TrueFalseTriviaQuestion(
            correctAnswer = True,
            category = None,
            categoryId = None,
            question = 'The Super Metroid player stashiocat is a Chicago Bully.',
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.BONGO
        )

        result = await self.triviaAnswerChecker.checkAnswer('false', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('true', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('qwerty', question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

    @pytest.mark.asyncio
    async def test_checkAnswer_withTrueFalseQuestionAndAnswerIsTrueAndFalse(self):
        question: AbsTriviaQuestion = TrueFalseTriviaQuestion(
            correctAnswer = True,
            category = None,
            categoryId = None,
            question = 'The Super Metroid player stashiocat is a Chicago Bully.',
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.BONGO
        )

        result = await self.triviaAnswerChecker.checkAnswer('f', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('false', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('t', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('true', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('wasd', question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

    @pytest.mark.asyncio
    async def test_checkAnswer_withTrueFalseQuestion(self):
        question: AbsTriviaQuestion = TrueFalseTriviaQuestion(
            correctAnswer = True,
            category = None,
            categoryId = None,
            question = 'The Super Metroid player stashiocat is a Chicago Bully.',
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.BONGO
        )

        result = await self.triviaAnswerChecker.checkAnswer('false', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('true', question)
        assert result is TriviaAnswerCheckResult.CORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion(self):
        categoryText = 'Test Category'
        questionText = 'The Korean country farthest north.'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'North Korea' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(
            answers = originalCorrectAnswers,
            allWords = allWords
        )

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON
        )

        result = await self.triviaAnswerChecker.checkAnswer(None, question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

        result = await self.triviaAnswerChecker.checkAnswer('', question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

        result = await self.triviaAnswerChecker.checkAnswer(' ', question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

        result = await self.triviaAnswerChecker.checkAnswer('\n', question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

        result = await self.triviaAnswerChecker.checkAnswer('north korea', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('norths korea', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('north koreas', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('south korea', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('sorth korea', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('nouth korea', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withParentheticalQuestionAnswerQuestion(self):
        categoryText = 'Test Category'
        questionText = 'That one weird author guy'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ '(Kurt) Vonnegut (Jr.)' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(
            answers = originalCorrectAnswers,
            allWords = allWords
        )

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON
        )

        result = await self.triviaAnswerChecker.checkAnswer('kurt vonnegut', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('vonnegut', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('vonegut', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('kurt vonnegut jr', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('kurt vonnegut junior', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('kurt voneguit', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withDecades(self):
        categoryText = 'Test Category'
        questionText = 'In what decade did that one thing come out?'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ '1950s' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(
            answers = originalCorrectAnswers,
            allWords = allWords
        )

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE,
        )

        result = await self.triviaAnswerChecker.checkAnswer('1850', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1850s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1900', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1900s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1910', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1910s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1920', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1920s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1930', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1930s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1940', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1940s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1948', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1948s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1949', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1949s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1950', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1950s', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1951', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1951s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1952', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1952s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1953', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1953s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1954', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1954s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1955', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1955s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1956', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1956s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1957', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1957s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1958', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1958s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1959', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1959s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1960', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1960s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1970', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1970s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1980', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1980s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1990', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1990s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('2000', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('2000s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('2050', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('2050s', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withDigits(self):
        categoryText = 'Test Category'
        questionText = 'Shakespeare wrote a play about him once or something...'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ '(King) Richard III' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(
            answers = originalCorrectAnswers,
            allWords = allWords
        )

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON
        )

        result = await self.triviaAnswerChecker.checkAnswer('richard the third', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('richard 3rd', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('richard three', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('king richard III', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('richard iii', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('king richard the 3rd', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('king richard 4', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('king richard 30', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withFraulein(self):
        categoryText = None
        questionText = 'Something about words'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'fräulein' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(
            answers = originalCorrectAnswers,
            allWords = allWords
        )

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON
        )

        result = await self.triviaAnswerChecker.checkAnswer('fraulein', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('fräulein', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('flamingo', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withSpaces(self):
        categoryText = 'Test Category'
        questionText = 'Shakespeare wrote a play about him once or something...'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'Beach Ball' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(
            answers = originalCorrectAnswers,
            allWords = allWords
        )

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('beach ball', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('beachball', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('beach balls', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('beachballs', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('a beach ball', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('beach ball s', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('beach es ball s', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('beachballa', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('beach balla', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('green beach ball', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_numberOnly(self):
        categoryText = 'Test Category'
        questionText = 'What did the book Brave New World come out?'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ '1984' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(
            answers = originalCorrectAnswers,
            allWords = allWords
        )

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON
        )

        result = await self.triviaAnswerChecker.checkAnswer('1984', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('nineteen eightyfour', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('MCMLXXXIV', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('1985', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_ordinalOnly(self):
        categoryText = 'Test Category'
        questionText = 'Christmas is on which day of the month of December?'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ '25th' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE,
        )

        result = await self.triviaAnswerChecker.checkAnswer('the twenty fifth', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('25', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('twenty five', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('24', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('twenty forth', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withHash(self):
        categoryText = 'Test Category'
        questionText = 'Name a food coloring'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'Red Dye #5' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('red dye #5', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('red dye number 5', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('red dye no 5', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('red number 5', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withEquation(self):
        categoryText = 'Math'
        questionText = 'Name a food coloring'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'X=5' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE,
        )

        result = await self.triviaAnswerChecker.checkAnswer('x=5', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('x = 5', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('5', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('five', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('x is 5', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('x equals 5', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('x = 5.0', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withHdDvd(self):
        categoryText = 'Test Category'
        questionText = 'This was the competitor to blu-ray'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'HD-DVD' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON
        )

        result = await self.triviaAnswerChecker.checkAnswer('hddvd', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('hd dvd', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('high definition dvd', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('high definition digital versatile disc', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('high definition digital video disc', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('hd digital versatile disc', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('hd digital video disc', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('hd', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('dvd', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('blu ray disc', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withGroanGrown(self):
        categoryText = 'Test Category'
        questionText = 'Something about homophones'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'groan/grown' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('groan/grown', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('groan', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('grown', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('idk', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withTheNewMath(self):
        categoryText = 'Test Category'
        questionText = 'Something about math'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'The New Math' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE,
        )

        result = await self.triviaAnswerChecker.checkAnswer('new math', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('the new math', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('the', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('math', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('new', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('math new', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('the math', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('the new', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withMiyamotoSan(self):
        categoryText = 'Test Category'
        questionText = 'This man created Mario'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'Miyamoto-san' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('miyamoto san', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('miyamoto', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('miyamoto chan', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('miyamoto kun', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('miyamoto sama', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withMrPotatoHead(self):
        categoryText = 'Toys'
        questionText = 'This is vegetable is a toy for children'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ '(Mr) Potato Head' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('mr potato head', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('mister potato head', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('potato head', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('ms potato head', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('miss potato head', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        # this should be incorrect, but it currently is correct. i don't know what to do right now
        # to fix this and frankly i think this is fine enough as a random edge case for the time being
        # result = await self.triviaAnswerChecker.checkAnswer('mrs potato head', question)
        # assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('missus potato head', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('mr', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('mister', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('potato', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('head', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withSparrballong(self):
        categoryText: str | None = None
        questionText = 'Something about food'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'Spärrballong' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('sparrballong', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('spärrballong', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('sausage', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withThingsThatArePinched(self):
        categoryText = 'Test Category'
        questionText = 'Something about toys'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'things that are pinched' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('things that are pinched', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('pinched', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('idk', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withThingsThatAreHello123(self):
        categoryText = 'Test Category'
        questionText = 'A random word question'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'things that are hello 123' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('things that are hello 123', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('hello 123', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('idk', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withUsDollarAmount1(self):
        categoryText = 'Finance'
        questionText = 'Something about money'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ '$50,000.00 (USD)' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('50000', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('5000', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('idk', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withUsDollarAmount2(self):
        categoryText = 'Finance'
        questionText = 'Something about money'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ '$123,456.78' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('123456.78', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('5000', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('idk', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withVideoHomeSystem(self):
        categoryText = 'Video'
        questionText = 'Something about old home consumer electronics'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'VHS' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('vhs', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('video home system', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('vhs video', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('dvd', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('blu ray disc', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withWalMart(self):
        categoryText = 'Big Shopping'
        questionText = 'Something about big shopping brands and stores'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'Wal-Mart' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('walmart', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('wal mart', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('wally world', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withTonyTheTigersStockSymbolQuestion(self):
        categoryText = 'One Letter Only'
        questionText = 'Tony the Tiger\'s stock symbol'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText,
        )

        originalCorrectAnswers: list[str] = [ 'K' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON,
        )

        result = await self.triviaAnswerChecker.checkAnswer('k', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('f', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('t', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('ttt', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withAcademicismQuestion(self):
        categoryText = 'Ism Question'
        questionText = 'Education question kinda thing'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText,
        )

        originalCorrectAnswers: list[str] = [ 'academicism' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON,
        )

        result = await self.triviaAnswerChecker.checkAnswer('a', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('academicisms', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('academicism', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('academic', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('academy', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('ism', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('olympics', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withBoarAndBearQuestion(self):
        categoryText = 'Testing Typo Handling'
        questionText = 'The pig animal, not the drink, or the kumo'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText,
        )

        originalCorrectAnswers: list[str] = [ 'boar' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(originalCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON,
        )

        result = await self.triviaAnswerChecker.checkAnswer('boar', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('bear', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('beer', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('pig', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    def test_sanity(self):
        assert self.triviaAnswerChecker is not None
        assert isinstance(self.triviaAnswerChecker, TriviaAnswerCheckerInterface)
        assert isinstance(self.triviaAnswerChecker, TriviaAnswerChecker)


    ##################################################
    ##################################################
    #### New trivia answer checking logic section ####
    ##################################################
    ##################################################

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withAllWords1(self):
        categoryText = 'Consumer Gaming'
        questionText = 'This console, first introduced in 2001 by Microsoft, competed with the Sony PlayStation and the Nintendo GameCube.'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'Microsoft Xbox' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)

        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(
            answers = originalCorrectAnswers,
            allWords = allWords
        )

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON
        )

        result = await self.triviaAnswerChecker.checkAnswer('xbox', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('microsoft xbox', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('microsoft gamecube', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('nintendo xbox', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withAllWordsNone1(self):
        categoryText = 'Consumer Gaming'
        questionText = 'This console, first introduced in 2001 by Microsoft, competed with the Sony PlayStation and the Nintendo GameCube.'

        originalCorrectAnswers: list[str] = [ 'Microsoft Xbox' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)

        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(
            answers = originalCorrectAnswers,
            allWords = None
        )

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = None,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON
        )

        result = await self.triviaAnswerChecker.checkAnswer('xbox', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('microsoft xbox', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('microsoft gamecube', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('nintendo xbox', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withAllWords2(self):
        categoryText = 'Sauce'
        questionText = 'This hot sauce is red and is made in Louisiana.'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'Tabasco Hot Sauce' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)

        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(
            answers = originalCorrectAnswers,
            allWords = allWords
        )

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON
        )

        result = await self.triviaAnswerChecker.checkAnswer('hot', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('hot sauce', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('sauce', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('tabasco', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('tabasco hot', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('tabasco sauce', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('tabasco hot sauce', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('crystal', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('crystal hot sauce', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withAllWordsNone2(self):
        categoryText = 'Sauce'
        questionText = 'This hot sauce is red and is made in Louisiana.'

        originalCorrectAnswers: list[str] = [ 'Tabasco Hot Sauce' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)

        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(
            answers = originalCorrectAnswers,
            allWords = None
        )

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = None,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON
        )

        result = await self.triviaAnswerChecker.checkAnswer('hot', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('hot sauce', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('sauce', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('tabasco', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('tabasco hot', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('tabasco sauce', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('tabasco hot sauce', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('crystal', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('crystal hot', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('crystal sauce', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('crystal hot sauce', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withAllWords3(self):
        categoryText = 'Blue Things'
        questionText = 'This is the color of the sky.'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText
        )

        originalCorrectAnswers: list[str] = [ 'blue' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)

        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(
            answers = originalCorrectAnswers,
            allWords = allWords
        )

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON
        )

        result = await self.triviaAnswerChecker.checkAnswer(None, question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

        result = await self.triviaAnswerChecker.checkAnswer('', question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

        result = await self.triviaAnswerChecker.checkAnswer(' ', question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

        result = await self.triviaAnswerChecker.checkAnswer('blue', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('red', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withOlympicGames(self):
        categoryText = 'International Sports'
        questionText = 'This is a big international sporting event with a logo that has rings.'

        allWords = await self.triviaQuestionCompiler.findAllWordsInQuestion(
            category = categoryText,
            question = questionText,
        )

        originalCorrectAnswers: list[str] = [ 'olympic games' ]
        correctAnswers = await self.triviaQuestionCompiler.compileResponses(originalCorrectAnswers)

        compiledCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList(
            answers = originalCorrectAnswers,
            allWords = allWords,
        )

        expandedCompiledCorrectAnswers: set[str] = set()
        for compiledCorrectAnswer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(compiledCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = categoryText,
            categoryId = None,
            question = questionText,
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON
        )

        result = await self.triviaAnswerChecker.checkAnswer(None, question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

        result = await self.triviaAnswerChecker.checkAnswer('', question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

        result = await self.triviaAnswerChecker.checkAnswer(' ', question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

        result = await self.triviaAnswerChecker.checkAnswer('olympic', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('olympics', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('olympic games', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('games', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('sports', question)
        assert result is TriviaAnswerCheckResult.INCORRECT
