import traceback
from typing import Final

from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from ..additionalAnswers.additionalTriviaAnswersRepositoryInterface import AdditionalTriviaAnswersRepositoryInterface
from ..compilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from ..compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.questionAnswerTriviaQuestion import QuestionAnswerTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..settings.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import GenericTriviaNetworkException
from ..triviaFetchOptions import TriviaFetchOptions
from ...funtoon.apiService.funtoonApiServiceInterface import FuntoonApiServiceInterface
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class FuntoonTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        funtoonApiService: FuntoonApiServiceInterface,
        timber: TimberInterface,
        triviaAnswerCompiler: TriviaAnswerCompilerInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
    ):
        super().__init__(
            triviaSettingsRepository = triviaSettingsRepository,
        )

        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise TypeError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(funtoonApiService, FuntoonApiServiceInterface):
            raise TypeError(f'funtoonApiService argument is malformed: \"{funtoonApiService}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaAnswerCompiler, TriviaAnswerCompilerInterface):
            raise TypeError(f'triviaAnswerCompiler argument is malformed: \"{triviaAnswerCompiler}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')

        self.__additionalTriviaAnswersRepository: Final[AdditionalTriviaAnswersRepositoryInterface] = additionalTriviaAnswersRepository
        self.__funtoonApiService: Final[FuntoonApiServiceInterface] = funtoonApiService
        self.__timber: Final[TimberInterface] = timber
        self.__triviaAnswerCompiler: Final[TriviaAnswerCompilerInterface] = triviaAnswerCompiler
        self.__triviaQuestionCompiler: Final[TriviaQuestionCompilerInterface] = triviaQuestionCompiler

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        try:
            funtoonQuestion = await self.__funtoonApiService.fetchTriviaQuestion()
        except GenericNetworkException as e:
            self.__timber.log('FuntoonTriviaQuestionRepository', f'Encountered network error: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.triviaSource, e)

        categoryId = str(funtoonQuestion.categoryId)
        triviaId = str(funtoonQuestion.triviaId)
        category = await self.__triviaQuestionCompiler.compileCategory(funtoonQuestion.category)
        question = await self.__triviaQuestionCompiler.compileQuestion(funtoonQuestion.clue)

        allWords: frozenset[str] | None = None
        if await self._triviaSettingsRepository.useNewAnswerCheckingMethod():
            allWords = await self.__triviaQuestionCompiler.findAllWordsInQuestion(
                category = category,
                question = question,
            )

        originalCorrectAnswers: list[str] = list()
        originalCorrectAnswers.append(funtoonQuestion.answer)

        correctAnswers: list[str] = list()
        correctAnswers.extend(originalCorrectAnswers)

        if await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswers(
            currentAnswers = correctAnswers,
            triviaId = triviaId,
            triviaQuestionType = TriviaQuestionType.QUESTION_ANSWER,
            triviaSource = self.triviaSource
        ):
            self.__timber.log('FuntoonTriviaQuestionRepository', f'Added additional answers to question ({triviaId=})')

        correctAnswers = await self.__triviaQuestionCompiler.compileResponses(correctAnswers)

        compiledCorrectAnswers: list[str] = list()
        compiledCorrectAnswers.append(funtoonQuestion.answer)

        await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswers(
            currentAnswers = compiledCorrectAnswers,
            triviaId = triviaId,
            triviaQuestionType = TriviaQuestionType.QUESTION_ANSWER,
            triviaSource = self.triviaSource
        )

        compiledCorrectAnswers = await self.__triviaAnswerCompiler.compileTextAnswersList(
            answers = compiledCorrectAnswers,
            allWords = allWords,
        )

        expandedCompiledCorrectAnswers: set[str] = set()
        for answer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.__triviaAnswerCompiler.expandNumerals(answer))

        return QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = category,
            categoryId = categoryId,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = self.triviaSource,
        )

    async def hasQuestionSetAvailable(self) -> bool:
        return True

    @property
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.QUESTION_ANSWER }

    @property
    def triviaSource(self) -> TriviaSource:
        return TriviaSource.FUNTOON
