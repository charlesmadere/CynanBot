import traceback

import aiofiles
import aiofiles.os
import aiofiles.ospath
import aiosqlite
from frozenlist import FrozenList

from .booleanTriviaDatabaseTriviaQuestion import BooleanTriviaDatabaseTriviaQuestion
from .exceptions import (NoTriviaQuestionsAvailableException,
                         TriviaDatabaseFileDoesNotExistException,
                         NoTriviaIncorrectAnswersException)
from .multipleChoiceTriviaDatabaseTriviaQuestion import MultipleChoiceTriviaDatabaseTriviaQuestion
from .triviaDatabaseQuestionStorageInterface import TriviaDatabaseQuestionStorageInterface
from .triviaDatabaseTriviaQuestion import TriviaDatabaseTriviaQuestion
from ...misc.triviaDifficultyParserInterface import TriviaDifficultyParserInterface
from ...misc.triviaQuestionTypeParserInterface import TriviaQuestionTypeParserInterface
from ...questions.triviaQuestionType import TriviaQuestionType
from ...triviaExceptions import UnsupportedTriviaTypeException
from ....misc import utils as utils
from ....timber.timberInterface import TimberInterface


class TriviaDatabaseQuestionStorage(TriviaDatabaseQuestionStorageInterface):

    def __init__(
        self,
        timber: TimberInterface,
        triviaDifficultyParser: TriviaDifficultyParserInterface,
        triviaQuestionTypeParser: TriviaQuestionTypeParserInterface,
        databaseFile: str = 'triviaDatabaseTriviaQuestionRepository.sqlite'
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaDifficultyParser, TriviaDifficultyParserInterface):
            raise TypeError(f'triviaDifficultyParser argument is malformed: \"{triviaDifficultyParser}\"')
        elif not isinstance(triviaQuestionTypeParser, TriviaQuestionTypeParserInterface):
            raise TypeError(f'triviaQuestionTypeParser argument is malformed: \"{triviaQuestionTypeParser}\"')
        elif not utils.isValidStr(databaseFile):
            raise TypeError(f'databaseFile argument is malformed: \"{databaseFile}\"')

        self.__timber: TimberInterface = timber
        self.__triviaDifficultyParser: TriviaDifficultyParserInterface = triviaDifficultyParser
        self.__triviaQuestionTypeParser: TriviaQuestionTypeParserInterface = triviaQuestionTypeParser
        self.__databaseFile: str = databaseFile

        self.__hasQuestionSetAvailable: bool | None = None

    async def __buildIncorrectAnswersList(
        self,
        incorrectAnswer0: str | None,
        incorrectAnswer1: str | None,
        incorrectAnswer2: str | None,
        triviaId: str
    ) -> FrozenList[str]:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')

        incorrectAnswers: list[str] = list()

        if utils.isValidStr(incorrectAnswer0):
            incorrectAnswers.append(incorrectAnswer0)

        if utils.isValidStr(incorrectAnswer1):
            incorrectAnswers.append(incorrectAnswer1)

        if utils.isValidStr(incorrectAnswer2):
            incorrectAnswers.append(incorrectAnswer2)

        if len(incorrectAnswers) == 0:
            raise NoTriviaIncorrectAnswersException(f'Unable to build up list of any incorrect answers ({incorrectAnswer0=}) ({incorrectAnswer1=}) ({incorrectAnswer2=}) ({incorrectAnswers=}) ({triviaId=})')

        incorrectAnswers.sort(key = lambda incorrectAnswer: incorrectAnswer.casefold())
        frozenIncorrectAnswers: FrozenList[str] = FrozenList(incorrectAnswers)
        frozenIncorrectAnswers.freeze()

        return frozenIncorrectAnswers

    async def fetchTriviaQuestion(self) -> TriviaDatabaseTriviaQuestion:
        if not await aiofiles.ospath.exists(self.__databaseFile):
            raise TriviaDatabaseFileDoesNotExistException(f'Trivia Database database file not found: \"{self.__databaseFile}\"')

        self.__timber.log('TriviaDatabaseQuestionStorage', f'Fetching trivia question...')

        connection = await aiosqlite.connect(self.__databaseFile)
        cursor = await connection.execute(
            '''
                SELECT category, correctAnswer, difficulty, question, questionId, triviaType, wrongAnswer1, wrongAnswer2, wrongAnswer3 FROM tdQuestions
                ORDER BY RANDOM()
                LIMIT 1
            '''
        )

        row = await cursor.fetchone()

        if row is None or len(row) != 9:
            raise NoTriviaQuestionsAvailableException(f'Unable to fetch trivia question data from Trivia Database! ({self.__databaseFile=}) ({row=})')

        category: str | None = row[0]
        correctAnswer: str = row[1]
        difficulty = await self.__triviaDifficultyParser.parse(row[2])
        question: str = row[3]
        triviaId: str = row[4]
        triviaType = await self.__triviaQuestionTypeParser.parse(row[5])
        incorrectAnswer0: str | None = row[6]
        incorrectAnswer1: str | None = row[7]
        incorrectAnswer2: str | None = row[8]

        await cursor.close()
        await connection.close()

        match triviaType:
            case TriviaQuestionType.MULTIPLE_CHOICE:
                incorrectAnswers = await self.__buildIncorrectAnswersList(
                    incorrectAnswer0 = incorrectAnswer0,
                    incorrectAnswer1 = incorrectAnswer1,
                    incorrectAnswer2 = incorrectAnswer2,
                    triviaId = triviaId
                )

                return MultipleChoiceTriviaDatabaseTriviaQuestion(
                    incorrectAnswers = incorrectAnswers,
                    category = category,
                    correctAnswer = correctAnswer,
                    question = question,
                    triviaId = triviaId,
                    difficulty = difficulty
                )

            case TriviaQuestionType.TRUE_FALSE:
                return BooleanTriviaDatabaseTriviaQuestion(
                    correctAnswer = utils.strictStrToBool(correctAnswer),
                    category = category,
                    question = question,
                    triviaId = triviaId,
                    difficulty = difficulty
                )

            case _:
                raise UnsupportedTriviaTypeException(f'triviaType \"{triviaType}\" is not supported for Trivia Database ({row=})')

    async def hasQuestionSetAvailable(self) -> bool:
        hasQuestionSetAvailable = self.__hasQuestionSetAvailable

        if hasQuestionSetAvailable is not None:
            return hasQuestionSetAvailable

        question: TriviaDatabaseTriviaQuestion | None = None
        exception: Exception | None = None

        try:
            question = await self.fetchTriviaQuestion()
        except Exception as e:
            self.__timber.log('TriviaDatabaseQuestionStorage', f'Encountered exception when attempting to fetch a trivia question: {e}', e, traceback.format_exc())
            exception = e

        hasQuestionSetAvailable = question is not None and exception is None
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable
        return hasQuestionSetAvailable
