import traceback

import aiofiles
import aiofiles.os
import aiofiles.ospath
import aiosqlite
from frozenlist import FrozenList

from .booleanOpenTriviaQaTriviaQuestion import BooleanOpenTriviaQaTriviaQuestion
from .exceptions import NoTriviaIncorrectAnswersException, NoTriviaQuestionsAvailableException, \
    TriviaDatabaseFileDoesNotExistException
from .multipleChoiceOpenTriviaQaTriviaQuestion import MultipleChoiceOpenTriviaQaTriviaQuestion
from .openTriviaQaQuestionStorageInterface import OpenTriviaQaQuestionStorageInterface
from .openTriviaQaQuestionType import OpenTriviaQaQuestionType
from .openTriviaQaQuestionTypeParserInterface import OpenTriviaQaQuestionTypeParserInterface
from .openTriviaQaTriviaQuestion import OpenTriviaQaTriviaQuestion
from ...triviaExceptions import UnsupportedTriviaTypeException
from ....misc import utils as utils
from ....timber.timberInterface import TimberInterface


class OpenTriviaQaQuestionStorage(OpenTriviaQaQuestionStorageInterface):

    def __init__(
        self,
        questionTypeParser: OpenTriviaQaQuestionTypeParserInterface,
        timber: TimberInterface,
        databaseFile: str = 'openTriviaQaTriviaQuestionDatabase.sqlite'
    ):
        if not isinstance(questionTypeParser, OpenTriviaQaQuestionTypeParserInterface):
            raise TypeError(f'questionTypeParser argument is malformed: \"{questionTypeParser}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(databaseFile):
            raise TypeError(f'databaseFile argument is malformed: \"{databaseFile}\"')

        self.__timber: TimberInterface = timber
        self.__questionTypeParser: OpenTriviaQaQuestionTypeParserInterface = questionTypeParser
        self.__databaseFile: str = databaseFile

        self.__hasQuestionSetAvailable: bool | None = None

    async def __buildIncorrectAnswersList(
        self,
        incorrectAnswer0: str | None,
        incorrectAnswer1: str | None,
        incorrectAnswer2: str | None,
        questionId: str
    ) -> FrozenList[str]:
        if not utils.isValidStr(questionId):
            raise TypeError(f'questionId argument is malformed: \"{questionId}\"')

        incorrectAnswers: list[str] = list()

        if utils.isValidStr(incorrectAnswer0):
            incorrectAnswers.append(incorrectAnswer0)

        if utils.isValidStr(incorrectAnswer1):
            incorrectAnswers.append(incorrectAnswer1)

        if utils.isValidStr(incorrectAnswer2):
            incorrectAnswers.append(incorrectAnswer2)

        if len(incorrectAnswers) == 0:
            raise NoTriviaIncorrectAnswersException(f'Unable to build up list of any incorrect answers ({incorrectAnswer0=}) ({incorrectAnswer1=}) ({incorrectAnswer2=}) ({incorrectAnswers=}) ({questionId=})')

        incorrectAnswers.sort(key = lambda incorrectAnswer: incorrectAnswer.casefold())
        frozenIncorrectAnswers: FrozenList[str] = FrozenList(incorrectAnswers)
        frozenIncorrectAnswers.freeze()

        return frozenIncorrectAnswers

    async def fetchTriviaQuestion(self) -> OpenTriviaQaTriviaQuestion:
        if not await aiofiles.ospath.exists(self.__databaseFile):
            raise TriviaDatabaseFileDoesNotExistException(f'Open Trivia QA database file not found: \"{self.__databaseFile}\"')

        self.__timber.log('OpenTriviaQaQuestionStorage', f'Fetching trivia question...')

        connection = await aiosqlite.connect(self.__databaseFile)
        cursor = await connection.execute(
            '''
                SELECT correctAnswer, newCategory, question, questionId, questionType, response1, response2, response3, response4 FROM triviaQuestions
                ORDER BY RANDOM()
                LIMIT 1
            '''
        )

        row = await cursor.fetchone()

        if row is None or len(row) == 0:
            raise NoTriviaQuestionsAvailableException(f'Unable to fetch trivia question data from Open Trivia QA! ({self.__databaseFile=}) ({row=})')

        correctAnswer: str = row[0]
        category: str | None = row[1]
        question: str = row[2]
        questionId: str = row[3]
        questionType = await self.__questionTypeParser.require(row[4])
        incorrectAnswer0: str | None = row[5]
        incorrectAnswer1: str | None = row[6]
        incorrectAnswer2: str | None = row[7]

        await cursor.close()
        await connection.close()

        match questionType:
            case OpenTriviaQaQuestionType.BOOLEAN:
                return BooleanOpenTriviaQaTriviaQuestion(
                    correctAnswer = utils.strictStrToBool(correctAnswer),
                    category = category,
                    question = question,
                    questionId = questionId
                )

            case OpenTriviaQaQuestionType.MULTIPLE_CHOICE:
                incorrectAnswers = await self.__buildIncorrectAnswersList(
                    incorrectAnswer0 = incorrectAnswer0,
                    incorrectAnswer1 = incorrectAnswer1,
                    incorrectAnswer2 = incorrectAnswer2,
                    questionId = questionId
                )

                return MultipleChoiceOpenTriviaQaTriviaQuestion(
                    incorrectAnswers = incorrectAnswers,
                    category = category,
                    correctAnswer = correctAnswer,
                    question = question,
                    questionId = questionId
                )

            case _:
                raise UnsupportedTriviaTypeException(f'questionType \"{questionType}\" is not supported for Open Trivia QA ({row=})')

    async def hasQuestionSetAvailable(self) -> bool:
        hasQuestionSetAvailable = self.__hasQuestionSetAvailable

        if hasQuestionSetAvailable is not None:
            return hasQuestionSetAvailable

        question: OpenTriviaQaTriviaQuestion | None = None
        exception: Exception | None = None

        try:
            question = await self.fetchTriviaQuestion()
        except Exception as e:
            self.__timber.log('OpenTriviaQaQuestionStorage', f'Encountered exception when attempting to fetch a trivia question: {e}', e, traceback.format_exc())
            exception = e

        hasQuestionSetAvailable = question is not None and exception is None
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable
        return hasQuestionSetAvailable
