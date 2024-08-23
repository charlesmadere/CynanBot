from abc import ABC, abstractmethod

from .pokepediaTriviaQuestion import PokepediaTriviaQuestion


class PokepediaTriviaQuestionGeneratorInterface(ABC):

    @abstractmethod
    async def fetchTriviaQuestion(self) -> PokepediaTriviaQuestion:
        pass
