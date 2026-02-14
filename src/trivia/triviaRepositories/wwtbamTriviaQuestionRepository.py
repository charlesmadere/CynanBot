from typing import Any

import aiofiles
import aiofiles.ospath
import aiosqlite

from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from ..compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ..triviaDifficulty import TriviaDifficulty
from ..triviaFetchOptions import TriviaFetchOptions
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class WwtbamTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        timber: TimberInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettings: TriviaSettingsInterface,
        triviaDatabaseFile: str = '../db/wwtbamTriviaQuestionDatabase.sqlite',
    ):
        super().__init__(
            triviaSettings = triviaSettings,
        )

        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')
        elif not utils.isValidStr(triviaDatabaseFile):
            raise TypeError(f'triviaDatabaseFile argument is malformed: \"{triviaDatabaseFile}\"')

        self.__timber: TimberInterface = timber
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler
        self.__triviaDatabaseFile: str = triviaDatabaseFile

        self.__hasQuestionSetAvailable: bool | None = None

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        self.__timber.log('WwtbamTriviaQuestionRepository', f'Fetching trivia question... ({fetchOptions=})')

        triviaDict = await self.__fetchTriviaQuestionDict()

        if await self._triviaSettings.isDebugLoggingEnabled():
            self.__timber.log('WwtbamTriviaQuestionRepository', f'{triviaDict}')

        triviaId = utils.getStrFromDict(triviaDict, 'triviaId')

        question = utils.getStrFromDict(triviaDict, 'question')
        question = await self.__triviaQuestionCompiler.compileQuestion(question)

        responses: list[str] = list()
        responses.append(utils.getStrFromDict(triviaDict, 'responseA'))
        responses.append(utils.getStrFromDict(triviaDict, 'responseB'))
        responses.append(utils.getStrFromDict(triviaDict, 'responseC'))
        responses.append(utils.getStrFromDict(triviaDict, 'responseD'))

        correctAnswerIndex = utils.getStrFromDict(triviaDict, 'correctAnswer', clean = True)

        correctAnswer: str | None = None
        if correctAnswerIndex.lower() == 'a':
            correctAnswer = responses[0]
        elif correctAnswerIndex.lower() == 'b':
            correctAnswer = responses[1]
        elif correctAnswerIndex.lower() == 'c':
            correctAnswer = responses[2]
        elif correctAnswerIndex.lower() == 'd':
            correctAnswer = responses[3]

        if not utils.isValidStr(correctAnswer):
            raise RuntimeError(f'Unknown correctAnswerIndex: \"{correctAnswerIndex}\"')

        correctAnswers: list[str] = list()
        correctAnswers.append(correctAnswer)

        correctAnswers = await self.__triviaQuestionCompiler.compileResponses(correctAnswers)
        responses = await self.__triviaQuestionCompiler.compileResponses(responses)

        multipleChoiceResponses = await self._buildMultipleChoiceResponsesList(
            correctAnswers = correctAnswers,
            multipleChoiceResponses = responses
        )

        return MultipleChoiceTriviaQuestion(
            correctAnswers = correctAnswers,
            multipleChoiceResponses = multipleChoiceResponses,
            category = None,
            categoryId = None,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = self.triviaSource
        )

    async def __fetchTriviaQuestionDict(self) -> dict[str, Any]:
        if not await aiofiles.ospath.exists(self.__triviaDatabaseFile):
            raise FileNotFoundError(f'WWTBAM trivia database file not found: \"{self.__triviaDatabaseFile}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        cursor = await connection.execute(
            '''
                SELECT correctAnswer, question, responseA, responseB, responseC, responseD, triviaId FROM wwtbamTriviaQuestions
                ORDER BY RANDOM()
                LIMIT 1
            '''
        )

        row = await cursor.fetchone()
        if row is None or len(row) != 7:
            raise RuntimeError(f'Received malformed data from WWTBAM database: {row}')

        triviaQuestionDict: dict[str, Any] = {
            'correctAnswer': row[0],
            'question': row[1],
            'responseA': row[2],
            'responseB': row[3],
            'responseC': row[4],
            'responseD': row[5],
            'triviaId': row[6]
        }

        await cursor.close()
        await connection.close()
        return triviaQuestionDict

    async def hasQuestionSetAvailable(self) -> bool:
        if self.__hasQuestionSetAvailable is not None:
            return self.__hasQuestionSetAvailable

        hasQuestionSetAvailable = await aiofiles.ospath.exists(self.__triviaDatabaseFile)
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable

        return hasQuestionSetAvailable

    @property
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE }

    @property
    def triviaSource(self) -> TriviaSource:
        return TriviaSource.WWTBAM
