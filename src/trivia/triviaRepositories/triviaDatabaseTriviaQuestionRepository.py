from typing import Any

import aiofiles
import aiofiles.ospath
import aiosqlite

from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from .triviaDatabase.triviaDatabaseQuestionStorageInterface import TriviaDatabaseQuestionStorageInterface
from ..compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import UnsupportedTriviaTypeException
from ..triviaFetchOptions import TriviaFetchOptions
from ..triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TriviaDatabaseTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        timber: TimberInterface,
        triviaDatabaseQuestionStorage: TriviaDatabaseQuestionStorageInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        super().__init__(triviaSettingsRepository)

        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaDatabaseQuestionStorage, TriviaDatabaseQuestionStorageInterface):
            raise TypeError(f'triviaDatabaseQuestionStorage argument is malformed: \"{triviaDatabaseQuestionStorage}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')

        self.__timber: TimberInterface = timber
        self.__triviaDatabaseQuestionStorage: TriviaDatabaseQuestionStorageInterface = triviaDatabaseQuestionStorage
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        self.__timber.log('TriviaDatabaseTriviaQuestionRepository', f'Fetching trivia question... ({fetchOptions=})')

        triviaDict = await self.__fetchTriviaQuestionDict()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('TriviaDatabaseTriviaQuestionRepository', f'{triviaDict}')

        triviaId = utils.getStrFromDict(triviaDict, 'triviaId')
        triviaType = TriviaQuestionType.fromStr(utils.getStrFromDict(triviaDict, 'type'))
        triviaDifficultyInt = utils.getIntFromDict(triviaDict, 'difficulty', fallback = -1)
        triviaDifficulty = TriviaDifficulty.fromInt(triviaDifficultyInt)

        try:
            triviaDatabaseQuestion = await self.__triviaDatabaseQuestionStorage.fetchTriviaQuestion()
        except Exception as e:
            pass

        category = await self.__triviaQuestionCompiler.compileCategory(utils.getStrFromDict(triviaDict, 'category', fallback = ''))
        question = await self.__triviaQuestionCompiler.compileQuestion(utils.getStrFromDict(triviaDict, 'question'))

        match triviaType:
            case TriviaQuestionType.MULTIPLE_CHOICE:
                originalCorrectAnswers: list[str] = [ utils.getStrFromDict(triviaDict, 'correctAnswer') ]
                correctAnswers = await self.__triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
                wrongAnswers = await self.__triviaQuestionCompiler.compileResponses(triviaDict['wrongAnswers'])

                multipleChoiceResponses = await self._buildMultipleChoiceResponsesList(
                    correctAnswers = correctAnswers,
                    multipleChoiceResponses = wrongAnswers
                )

                return MultipleChoiceTriviaQuestion(
                    correctAnswers = correctAnswers,
                    multipleChoiceResponses = multipleChoiceResponses,
                    category = category,
                    categoryId = None,
                    question = question,
                    triviaId = triviaId,
                    triviaDifficulty = triviaDifficulty,
                    originalTriviaSource = None,
                    triviaSource = self.triviaSource
                )

            case TriviaQuestionType.TRUE_FALSE:
                correctAnswer = utils.getBoolFromDict(triviaDict, 'correctAnswer')

                return TrueFalseTriviaQuestion(
                    correctAnswer = correctAnswer,
                    category = category,
                    categoryId = None,
                    question = question,
                    triviaId = triviaId,
                    triviaDifficulty = triviaDifficulty,
                    originalTriviaSource = None,
                    triviaSource = self.triviaSource
                )

            case _:
                raise UnsupportedTriviaTypeException(f'triviaType \"{triviaType}\" is not supported for Trivia Database: {triviaDict}')

    async def hasQuestionSetAvailable(self) -> bool:
        return await self.__triviaDatabaseQuestionStorage.hasQuestionSetAvailable()

    @property
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    @property
    def triviaSource(self) -> TriviaSource:
        return TriviaSource.TRIVIA_DATABASE
