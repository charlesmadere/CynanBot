from abc import ABC, abstractmethod


class TriviaIdGeneratorInterface(ABC):

    @abstractmethod
    async def generateActionId(self) -> str:
        pass

    @abstractmethod
    async def generateEventId(self) -> str:
        pass

    @abstractmethod
    async def generateGameId(self) -> str:
        pass

    @abstractmethod
    async def generateQuestionId(
        self,
        question: str,
        category: str | None = None,
        difficulty: str | None = None
    ) -> str:
        pass
