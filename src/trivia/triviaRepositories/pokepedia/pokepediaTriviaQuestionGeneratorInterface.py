from abc import ABC, abstractmethod

from .pokepediaTriviaQuestion import PokepediaTriviaQuestion
from ....pkmn.pokepediaGeneration import PokepediaGeneration


class PokepediaTriviaQuestionGeneratorInterface(ABC):

    @abstractmethod
    async def fetchTriviaQuestion(
        self,
        maxGeneration: PokepediaGeneration
    ) -> PokepediaTriviaQuestion:
        pass
