from abc import ABC, abstractmethod

from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion


class TriviaScraperInterface(ABC):

    @abstractmethod
    async def store(self, question: AbsTriviaQuestion):
        pass
