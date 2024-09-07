import traceback

import aiofiles
import aiofiles.os
import aiofiles.ospath
import aiosqlite
from frozenlist import FrozenList

from .exceptions import NoTriviaIncorrectAnswersException, NoTriviaQuestionsAvailableException, \
    TriviaDatabaseFileDoesNotExistException
from .millionaireTriviaQuestion import MillionaireTriviaQuestion
from .millionaireTriviaQuestionStorageInterface import MillionaireTriviaQuestionStorageInterface
from ....misc import utils as utils
from ....timber.timberInterface import TimberInterface


class MillionaireTriviaQuestionStorage(MillionaireTriviaQuestionStorageInterface):

    def __init__(
        self,
        timber: TimberInterface,
        databaseFile: str = 'millionaireTriviaQuestionsDatabase.sqlite'
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(databaseFile):
            raise TypeError(f'databaseFile argument is malformed: \"{databaseFile}\"')

        self.__timber: TimberInterface = timber
        self.__databaseFile: str = databaseFile

        self.__hasQuestionSetAvailable: bool | None = None

    async def __buildIncorrectAnswersList(
        self,
        incorrectAnswer0: str | None,
        incorrectAnswer1: str | None,
        incorrectAnswer2: str | None,
        incorrectAnswer3: str | None,
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

    async def fetchTriviaQuestion(self) -> MillionaireTriviaQuestion:
        if not await aiofiles.ospath.exists(self.__databaseFile):
            raise TriviaDatabaseFileDoesNotExistException(f'Millionaire database file not found: \"{self.__databaseFile}\"')

        self.__timber.log('MillionaireQuestionStorage', f'Fetching trivia question...')

        connection = await aiosqlite.connect(self.__databaseFile)
        cursor = await connection.execute(
            '''
                SELECT answer, question, responseA, responseB, responseC, responseD, triviaId FROM millionaireQuestions
                ORDER BY RANDOM()
                LIMIT 1
            '''
        )

        row = await cursor.fetchone()

        if row is None or len(row) == 0:
            raise NoTriviaQuestionsAvailableException(f'Unable to fetch trivia question data from Millionaire! ({self.__databaseFile=}) ({row=})')

        await cursor.close()
        await connection.close()

        correctAnswer: str = row[0]
        question: str = row[1]
        incorrectAnswer0: str | None = row[2]
        incorrectAnswer1: str | None = row[3]
        incorrectAnswer2: str | None = row[4]
        incorrectAnswer3: str | None = row[5]
        questionId: str = row[6]

        incorrectAnswers = await self.__buildIncorrectAnswersList(
            incorrectAnswer0 = incorrectAnswer0,
            incorrectAnswer1 = incorrectAnswer1,
            incorrectAnswer2 = incorrectAnswer2,
            incorrectAnswer3 = incorrectAnswer3,
            questionId = questionId
        )

        return MillionaireTriviaQuestion(
            incorrectAnswers = incorrectAnswers,
            correctAnswer = correctAnswer,
            question = question,
            questionId = questionId
        )

    async def hasQuestionSetAvailable(self) -> bool:
        hasQuestionSetAvailable = self.__hasQuestionSetAvailable

        if hasQuestionSetAvailable is not None:
            return hasQuestionSetAvailable

        question: MillionaireTriviaQuestion | None = None
        exception: Exception | None = None

        try:
            question = await self.fetchTriviaQuestion()
        except Exception as e:
            self.__timber.log('MillionaireTriviaQuestionStorage', f'Encountered exception when attempting to fetch a trivia question: {e}', e, traceback.format_exc())
            exception = e

        hasQuestionSetAvailable = question is not None and exception is None
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable
        return hasQuestionSetAvailable
