from abc import abstractmethod
from typing import Dict

from CynanBot.misc.clearable import Clearable
from CynanBot.trivia.triviaSource import TriviaSource


class TriviaSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def areAdditionalTriviaAnswersEnabled(self) -> bool:
        pass

    @abstractmethod
    async def areShinyTriviasEnabled(self) -> bool:
        pass

    @abstractmethod
    async def areToxicTriviasEnabled(self) -> bool:
        pass

    @abstractmethod
    async def getAvailableTriviaSourcesAndWeights(self) -> Dict[TriviaSource, int]:
        pass

    @abstractmethod
    async def getLevenshteinThresholdGrowthRate(self) -> int:
        pass

    @abstractmethod
    async def getMaxAdditionalTriviaAnswerLength(self) -> int:
        pass

    @abstractmethod
    async def getMaxAdditionalTriviaAnswers(self) -> int:
        pass

    @abstractmethod
    async def getMaxAnswerLength(self) -> int:
        pass

    @abstractmethod
    async def getMaxMultipleChoiceResponses(self) -> int:
        pass

    @abstractmethod
    async def getMaxQuestionLength(self) -> int:
        pass

    @abstractmethod
    async def getMaxPhraseAnswerLength(self) -> int:
        pass

    @abstractmethod
    async def getMaxPhraseGuessLength(self) -> int:
        pass

    @abstractmethod
    async def getMaxSuperTriviaQuestionSpoolSize(self) -> int:
        pass

    @abstractmethod
    async def getMaxTriviaQuestionSpoolSize(self) -> int:
        pass

    @abstractmethod
    async def getMaxRetryCount(self) -> int:
        pass

    @abstractmethod
    async def getMaxSuperTriviaGameQueueSize(self) -> int:
        pass

    @abstractmethod
    async def getMinDaysBeforeRepeatQuestion(self) -> int:
        pass

    @abstractmethod
    async def getMinMultipleChoiceResponses(self) -> int:
        pass

    @abstractmethod
    async def getShinyProbability(self) -> float:
        pass

    @abstractmethod
    async def getSuperTriviaCooldownSeconds(self) -> int:
        pass

    @abstractmethod
    async def getSuperTriviaFirstQuestionDelaySeconds(self) -> int:
        pass

    @abstractmethod
    async def getToxicProbability(self) -> float:
        pass

    @abstractmethod
    async def getTriviaSourceInstabilityThreshold(self) -> int:
        pass

    @abstractmethod
    async def isBanListEnabled(self) -> bool:
        pass

    @abstractmethod
    async def isDebugLoggingEnabled(self) -> bool:
        pass
