from abc import abstractmethod

from frozenlist import FrozenList

from .triviaQuestionRepositoryInterface import TriviaQuestionRepositoryInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.questionAnswerTriviaQuestion import QuestionAnswerTriviaQuestion
from ..questions.triviaSource import TriviaSource
from ..triviaFetchOptions import TriviaFetchOptions


class GlacialTriviaQuestionRepositoryInterface(TriviaQuestionRepositoryInterface):

    @abstractmethod
    async def fetchAllQuestionAnswerTriviaQuestions(
        self,
        fetchOptions: TriviaFetchOptions,
    ) -> FrozenList[QuestionAnswerTriviaQuestion]:
        pass

    @abstractmethod
    async def remove(
        self,
        triviaId: str,
        originalTriviaSource: TriviaSource,
    ):
        pass

    @abstractmethod
    async def store(self, question: AbsTriviaQuestion) -> bool:
        pass
