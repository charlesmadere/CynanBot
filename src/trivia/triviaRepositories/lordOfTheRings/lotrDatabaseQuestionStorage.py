import traceback
from typing import Final

import aiofiles
import aiofiles.os
import aiofiles.ospath
import aiosqlite
from frozenlist import FrozenList

from .exceptions import (NoTriviaAnswersException,
                         NoTriviaQuestionsAvailableException,
                         TriviaDatabaseFileDoesNotExistException)
from .lotrDatabaseQuestionStorageInterface import LotrDatabaseQuestionStorageInterface
from .lotrTriviaQuestion import LotrTriviaQuestion
from ....misc import utils as utils
from ....timber.timberInterface import TimberInterface


class LotrDatabaseQuestionStorage(LotrDatabaseQuestionStorageInterface):

    def __init__(
        self,
        timber: TimberInterface,
        databaseFile: str = '../db/lotrTriviaQuestionsDatabase.sqlite',
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(databaseFile):
            raise TypeError(f'databaseFile argument is malformed: \"{databaseFile}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__databaseFile: Final[str] = databaseFile

        self.__hasQuestionSetAvailable: bool | None = None

    async def __buildAnswersList(
        self,
        answerA: str | None,
        answerB: str | None,
        answerC: str | None,
        answerD: str | None,
        triviaId: str,
    ) -> FrozenList[str]:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')

        answers: list[str] = list()

        if utils.isValidStr(answerA):
            answers.append(answerA)

        if utils.isValidStr(answerB):
            answers.append(answerB)

        if utils.isValidStr(answerC):
            answers.append(answerC)

        if utils.isValidStr(answerD):
            answers.append(answerD)

        if len(answers) == 0:
            raise NoTriviaAnswersException(f'Unable to build up list of any correct answers ({answerA=}) ({answerB=}) ({answerC=}) ({answerD=}) ({triviaId=}) ({answers=})')

        answers.sort(key = lambda answer: answer.casefold())
        frozenAnswers: FrozenList[str] = FrozenList(answers)
        frozenAnswers.freeze()

        return frozenAnswers

    async def fetchTriviaQuestion(self) -> LotrTriviaQuestion:
        if not await aiofiles.ospath.exists(self.__databaseFile):
            raise TriviaDatabaseFileDoesNotExistException(f'LOTR database question file not found: \"{self.__databaseFile}\"')

        self.__timber.log('LotrDatabaseQuestionStorage', f'Fetching trivia question...')

        connection = await aiosqlite.connect(self.__databaseFile)
        cursor = await connection.execute(
            '''
                SELECT answerA, answerB, answerC, answerD, category, question, triviaId FROM lotrQuestions
                ORDER BY RANDOM()
                LIMIT 1
            ''',
        )

        row = await cursor.fetchone()

        if row is None or len(row) != 7:
            raise NoTriviaQuestionsAvailableException(f'Unable to fetch trivia question data from LOTR! ({self.__databaseFile=}) ({row=})')

        answerA: str | None = row[0]
        answerB: str | None = row[1]
        answerC: str | None = row[2]
        answerD: str | None = row[3]
        category: str | None = row[4]
        question: str = row[5]
        triviaId: str = row[6]

        await cursor.close()
        await connection.close()

        answers = await self.__buildAnswersList(
            answerA = answerA,
            answerB = answerB,
            answerC = answerC,
            answerD = answerD,
            triviaId = triviaId,
        )

        return LotrTriviaQuestion(
            answers = answers,
            category = category,
            question = question,
            triviaId = triviaId,
        )

    async def hasQuestionSetAvailable(self) -> bool:
        hasQuestionSetAvailable = self.__hasQuestionSetAvailable

        if hasQuestionSetAvailable is not None:
            return hasQuestionSetAvailable

        question: LotrTriviaQuestion | None = None
        exception: Exception | None = None

        try:
            question = await self.fetchTriviaQuestion()
        except Exception as e:
            self.__timber.log('LotrDatabaseQuestionStorage', f'Encountered exception when attempting to fetch a trivia question: {e}', e, traceback.format_exc())
            exception = e

        hasQuestionSetAvailable = question is not None and exception is None
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable
        return hasQuestionSetAvailable
