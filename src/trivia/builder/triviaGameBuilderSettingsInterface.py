from abc import ABC, abstractmethod


class TriviaGameBuilderSettingsInterface(ABC):

    @abstractmethod
    async def getSuperTriviaGamePerUserAttempts(self) -> int:
        pass

    @abstractmethod
    async def getSuperTriviaGamePoints(self) -> int:
        pass

    @abstractmethod
    async def getSuperTriviaGameShinyMultiplier(self) -> int:
        pass

    @abstractmethod
    async def getSuperTriviaGameToxicMultiplier(self) -> int:
        pass

    @abstractmethod
    async def getSuperTriviaGameToxicPunishmentMultiplier(self) -> int:
        pass

    @abstractmethod
    async def getTriviaGamePoints(self) -> int:
        pass

    @abstractmethod
    async def getTriviaGameShinyMultiplier(self) -> int:
        pass

    @abstractmethod
    async def getWaitForSuperTriviaAnswerDelay(self) -> int:
        pass

    @abstractmethod
    async def getWaitForTriviaAnswerDelay(self) -> int:
        pass

    @abstractmethod
    async def isSuperTriviaGameEnabled(self) -> bool:
        pass

    @abstractmethod
    async def isTriviaGameEnabled(self) -> bool:
        pass
