from abc import ABC, abstractmethod

from .bongoTriviaQuestion import BongoTriviaQuestion


class BongoApiServiceInterface(ABC):

    @abstractmethod
    async def fetchTriviaQuestion(self) -> BongoTriviaQuestion:
        pass
