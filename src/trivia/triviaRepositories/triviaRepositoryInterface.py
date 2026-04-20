from abc import ABC, abstractmethod

from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..triviaFetchOptions import TriviaFetchOptions
from ...misc.startable import Startable


class TriviaRepositoryInterface(Startable, ABC):

    @abstractmethod
    async def fetchTrivia(
        self,
        emote: str,
        triviaFetchOptions: TriviaFetchOptions,
    ) -> AbsTriviaQuestion | None:
        pass
