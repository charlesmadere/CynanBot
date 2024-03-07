from abc import abstractmethod

from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.triviaRepositories.triviaQuestionRepositoryInterface import \
    TriviaQuestionRepositoryInterface


class GlacialTriviaQuestionRepositoryInterface(TriviaQuestionRepositoryInterface):

    @abstractmethod
    async def store(self, question: AbsTriviaQuestion) -> bool:
        pass
