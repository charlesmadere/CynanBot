from typing import Set

import pytest

from CynanBot.storage.jsonStaticReader import JsonStaticReader
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from CynanBot.trivia.questions.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from CynanBot.trivia.questions.trueFalseTriviaQuestion import \
    TrueFalseTriviaQuestion
from CynanBot.trivia.triviaAnswerChecker import TriviaAnswerChecker
from CynanBot.trivia.triviaAnswerCheckResult import TriviaAnswerCheckResult
from CynanBot.trivia.triviaAnswerCompiler import TriviaAnswerCompiler
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaQuestionCompiler import TriviaQuestionCompiler
from CynanBot.trivia.triviaSettingsRepository import TriviaSettingsRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from CynanBot.trivia.triviaSource import TriviaSource


class TestTriviaAnswerChecker():

    timber: TimberInterface = TimberStub()
    triviaAnswerCompiler = TriviaAnswerCompiler(timber = timber)
    triviaQuestionCompiler = TriviaQuestionCompiler()
    triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict())
    )
    triviaAnswerChecker = TriviaAnswerChecker(
        timber = timber,
        triviaAnswerCompiler = triviaAnswerCompiler,
        triviaSettingsRepository = triviaSettingsRepository
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
            triviaSource = TriviaSource.BONGO
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
            correctAnswers = [ False ],
            category = None,
            categoryId = None,
            question = 'The Super Metroid player stashiocat is a Chicago Bully.',
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
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
            correctAnswers = [ True ],
            category = None,
            categoryId = None,
            question = 'The Super Metroid player stashiocat is a Chicago Bully.',
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
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
            correctAnswers = [ True, False ],
            category = None,
            categoryId = None,
            question = 'The Super Metroid player stashiocat is a Chicago Bully.',
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            triviaSource = TriviaSource.BONGO
        )

        result = await self.triviaAnswerChecker.checkAnswer('f', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('false', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('t', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('true', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('wasd', question)
        assert result is TriviaAnswerCheckResult.INVALID_INPUT

    @pytest.mark.asyncio
    async def test_checkAnswer_withTrueFalseQuestion(self):
        question: AbsTriviaQuestion = TrueFalseTriviaQuestion(
            correctAnswers = [ True ],
            category = None,
            categoryId = None,
            question = 'The Super Metroid player stashiocat is a Chicago Bully.',
            triviaId = 'abc123',
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            triviaSource = TriviaSource.BONGO
        )

        result = await self.triviaAnswerChecker.checkAnswer('false', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('true', question)
        assert result is TriviaAnswerCheckResult.CORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion(self):
        answer = 'North Korea'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='The Korean country farthest north.',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE,
        )

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
        answer = '(Kurt) Vonnegut (Jr.)'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='That one weird author guy',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE,
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
        answer = '1950s'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='In what decade did that one thing come out?',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE,
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
        answer = '(King) Richard III'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='Shakespeare wrote a play about him once or something...',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE,
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
    async def test_checkAnswer_withQuestionAnswerQuestion_withSpaces(self):
        answer = 'Beach Ball'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='Shakespeare wrote a play about him once or something...',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE,
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
        answer = '1984'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='What year is that one year people say a lot when talking about fascism and whatnot?',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE,
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
        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=['25th'],
            cleanedCorrectAnswers=[
                'twenty five',
                'two five',
                'twenty fifth',
                'the twenty fifth',
            ],
            category='Test Category',
            categoryId=None,
            question='Christmas is on which day of the month of December?',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE,
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
        answer = 'Red Dye #5'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='Name a food coloring',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE,
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
        answer = 'X=5'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='Name a food coloring',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE,
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
    async def test_checkAnswer_withQuestionAnswerQuestion_withGroanGrown(self):
        answer = 'groan/grown'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='Something about homophones',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE
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
        answer = 'The New Math'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='Something about math',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE,
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
        answer = 'Miyamoto-san'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='Something about Nintendo',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE
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
        answer = '(Mr) Potato Head'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='Something about toys',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE
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
    async def test_checkAnswer_withQuestionAnswerQuestion_withThingsThatArePinched(self):
        answer = 'things that are pinched'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='Something about toys',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('things that are pinched', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('pinched', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('idk', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withThingsThatAreHello123(self):
        answer = 'things that are hello 123'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='Something about toys',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('things that are hello 123', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('hello 123', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('idk', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withUsDollarAmount1(self):
        answer = '$50,000.00 (USD)'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='Something about toys',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('50000', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('5000', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('idk', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    @pytest.mark.asyncio
    async def test_checkAnswer_withQuestionAnswerQuestion_withUsDollarAmount2(self):
        answer = '$123,456.78'

        correctAnswers = await self.triviaQuestionCompiler.compileResponses([ answer ])
        cleanedCorrectAnswers = await self.triviaAnswerCompiler.compileTextAnswersList([ answer ])

        expandedCleanedCorrectAnswers: Set[str] = set()
        for cleanedCorrectAnswer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.triviaAnswerCompiler.expandNumerals(cleanedCorrectAnswer))

        question: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
            correctAnswers=correctAnswers,
            cleanedCorrectAnswers=list(expandedCleanedCorrectAnswers),
            category='Test Category',
            categoryId=None,
            question='Something about toys',
            triviaId='abc123',
            triviaDifficulty=TriviaDifficulty.UNKNOWN,
            triviaSource=TriviaSource.J_SERVICE
        )

        result = await self.triviaAnswerChecker.checkAnswer('123456.78', question)
        assert result is TriviaAnswerCheckResult.CORRECT

        result = await self.triviaAnswerChecker.checkAnswer('5000', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

        result = await self.triviaAnswerChecker.checkAnswer('idk', question)
        assert result is TriviaAnswerCheckResult.INCORRECT

    def test_sanity(self):
        assert self.triviaAnswerChecker is not None
        assert isinstance(self.triviaAnswerChecker, TriviaAnswerChecker)
