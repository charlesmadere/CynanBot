from typing import Any, Dict, List, Optional, Set

import aiofiles
import aiofiles.ospath
import aiosqlite

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.compilers.triviaQuestionCompilerInterface import \
    TriviaQuestionCompilerInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class MillionaireTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        timber: TimberInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaDatabaseFile: str = 'millionaireTriviaQuestionsDatabase.sqlite'
    ):
        super().__init__(triviaSettingsRepository)

        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface), f"malformed {triviaQuestionCompiler=}"
        if not utils.isValidStr(triviaDatabaseFile):
            raise ValueError(f'triviaDatabaseFile argument is malformed: \"{triviaDatabaseFile}\"')

        self.__timber: TimberInterface = timber
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler
        self.__triviaDatabaseFile: str = triviaDatabaseFile

        self.__hasQuestionSetAvailable: Optional[bool] = None

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        assert isinstance(fetchOptions, TriviaFetchOptions), f"malformed {fetchOptions=}"

        self.__timber.log('MillionaireTriviaQuestionRepository', f'Fetching trivia question... (fetchOptions={fetchOptions})')

        triviaDict = await self.__fetchTriviaQuestionDict()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('MillionaireTriviaQuestionRepository', f'{triviaDict}')

        triviaId = utils.getStrFromDict(triviaDict, 'triviaId')

        correctAnswer = utils.getStrFromDict(triviaDict, 'answer')
        correctAnswer = await self.__triviaQuestionCompiler.compileResponse(correctAnswer)

        question = utils.getStrFromDict(triviaDict, 'question')
        question = await self.__triviaQuestionCompiler.compileResponse(question)

        correctAnswers: List[str] = list()
        correctAnswers.append(correctAnswer)

        multipleChoiceResponses = await self.__triviaQuestionCompiler.compileResponses(triviaDict['responses'])
        multipleChoiceResponses = await self._buildMultipleChoiceResponsesList(
            correctAnswers = correctAnswers,
            multipleChoiceResponses = multipleChoiceResponses
        )

        return MultipleChoiceTriviaQuestion(
            correctAnswers = correctAnswers,
            multipleChoiceResponses = multipleChoiceResponses,
            category = None,
            categoryId = None,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            triviaSource = TriviaSource.MILLIONAIRE
        )

    async def __fetchTriviaQuestionDict(self) -> Dict[str, Any]:
        if not await aiofiles.ospath.exists(self.__triviaDatabaseFile):
            raise FileNotFoundError(f'Millionaire trivia database file not found: \"{self.__triviaDatabaseFile}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        cursor = await connection.execute(
            '''
                SELECT answer, question, responseA, responseB, responseC, responseD, triviaId FROM millionaireQuestions
                ORDER BY RANDOM()
                LIMIT 1
            '''
        )

        row = await cursor.fetchone()
        if not utils.hasItems(row) or len(row) != 7:
            raise RuntimeError(f'Received malformed data from Millionaire database: {row}')

        triviaQuestionDict: Dict[str, Any] = {
            'answer': row[0],
            'question': row[1],
            'responses': [ row[2], row[3], row[4], row[5] ],
            'triviaId': row[6]
        }

        await cursor.close()
        await connection.close()
        return triviaQuestionDict

    def getSupportedTriviaTypes(self) -> Set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.MILLIONAIRE

    async def hasQuestionSetAvailable(self) -> bool:
        if self.__hasQuestionSetAvailable is not None:
            return self.__hasQuestionSetAvailable

        hasQuestionSetAvailable = await aiofiles.ospath.exists(self.__triviaDatabaseFile)
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable

        return hasQuestionSetAvailable
