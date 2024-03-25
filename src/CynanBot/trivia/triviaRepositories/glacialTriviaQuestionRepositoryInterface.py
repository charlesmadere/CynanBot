from abc import abstractmethod

from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaRepositories.triviaQuestionRepositoryInterface import \
    TriviaQuestionRepositoryInterface


class GlacialTriviaQuestionRepositoryInterface(TriviaQuestionRepositoryInterface):

    @abstractmethod
    async def remove(self, triviaId: str, originalTriviaSource: TriviaSource):
        pass

    @abstractmethod
    async def store(self, question: AbsTriviaQuestion) -> bool:
        pass
