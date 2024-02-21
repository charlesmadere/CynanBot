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
from CynanBot.trivia.questions.trueFalseTriviaQuestion import \
    TrueFalseTriviaQuestion
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import UnsupportedTriviaTypeException
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class TriviaDatabaseTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        timber: TimberInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaDatabaseFile: str = 'triviaDatabaseTriviaQuestionRepository.sqlite'
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

        self.__timber.log('TriviaDatabaseTriviaQuestionRepository', f'Fetching trivia question... (fetchOptions={fetchOptions})')

        triviaDict = await self.__fetchTriviaQuestionDict()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('TriviaDatabaseTriviaQuestionRepository', f'{triviaDict}')

        triviaId = utils.getStrFromDict(triviaDict, 'triviaId')
        triviaType = TriviaQuestionType.fromStr(utils.getStrFromDict(triviaDict, 'type'))
        triviaDifficultyInt = utils.getIntFromDict(triviaDict, 'difficulty', fallback = -1)
        triviaDifficulty = TriviaDifficulty.fromInt(triviaDifficultyInt)

        category = await self.__triviaQuestionCompiler.compileCategory(utils.getStrFromDict(triviaDict, 'category', fallback = ''))
        question = await self.__triviaQuestionCompiler.compileQuestion(utils.getStrFromDict(triviaDict, 'question'))

        if triviaType is TriviaQuestionType.MULTIPLE_CHOICE:
            correctAnswer = await self.__triviaQuestionCompiler.compileResponse(
                response = utils.getStrFromDict(triviaDict, 'correctAnswer')
            )
            correctAnswerStrings: List[str] = list()
            correctAnswerStrings.append(correctAnswer)

            wrongAnswers = await self.__triviaQuestionCompiler.compileResponses(triviaDict['wrongAnswers'])

            multipleChoiceResponses = await self._buildMultipleChoiceResponsesList(
                correctAnswers = correctAnswerStrings,
                multipleChoiceResponses = wrongAnswers
            )

            return MultipleChoiceTriviaQuestion(
                correctAnswers = correctAnswerStrings,
                multipleChoiceResponses = multipleChoiceResponses,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                triviaSource = TriviaSource.TRIVIA_DATABASE
            )
        elif triviaType is TriviaQuestionType.TRUE_FALSE:
            correctAnswer = utils.getBoolFromDict(triviaDict, 'correctAnswer')
            correctAnswerBools: List[bool] = list()
            correctAnswerBools.append(correctAnswer)

            return TrueFalseTriviaQuestion(
                correctAnswers = correctAnswerBools,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                triviaSource = TriviaSource.TRIVIA_DATABASE
            )

        raise UnsupportedTriviaTypeException(f'triviaType \"{triviaType}\" is not supported for Trivia Database: {triviaDict}')

    async def __fetchTriviaQuestionDict(self) -> Dict[str, Any]:
        if not await aiofiles.ospath.exists(self.__triviaDatabaseFile):
            raise FileNotFoundError(f'Trivia Database trivia database file not found: \"{self.__triviaDatabaseFile}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        cursor = await connection.execute(
            '''
                SELECT category, correctAnswer, difficulty, question, questionId, triviaType, wrongAnswer1, wrongAnswer2, wrongAnswer3 FROM tdQuestions
                ORDER BY RANDOM()
                LIMIT 1
            '''
        )

        row = await cursor.fetchone()
        if not utils.hasItems(row) or len(row) != 9:
            raise RuntimeError(f'Received malformed data from {self.getTriviaSource()} database: {row}')

        triviaQuestionDict: Dict[str, Any] = {
            'category': row[0],
            'correctAnswer': row[1],
            'difficulty': row[2],
            'question': row[3],
            'triviaId': row[4],
            'type': row[5],
            'wrongAnswers': [ row[6], row[7], row[8] ]
        }

        await cursor.close()
        await connection.close()
        return triviaQuestionDict

    def getSupportedTriviaTypes(self) -> Set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.TRIVIA_DATABASE

    async def hasQuestionSetAvailable(self) -> bool:
        if self.__hasQuestionSetAvailable is not None:
            return self.__hasQuestionSetAvailable

        hasQuestionSetAvailable = await aiofiles.ospath.exists(self.__triviaDatabaseFile)
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable

        return hasQuestionSetAvailable
