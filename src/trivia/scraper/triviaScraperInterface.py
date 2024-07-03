from abc import ABC, abstractmethod

from ..questions.absTriviaQuestion import AbsTriviaQuestion


class TriviaScraperInterface(ABC):

    @abstractmethod
    async def store(self, question: AbsTriviaQuestion):
        pass
