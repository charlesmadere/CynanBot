from abc import ABC, abstractmethod
from datetime import tzinfo
from typing import List, Optional

from CynanBot.cuteness.cutenessBoosterPack import CutenessBoosterPack


class UserInterface(ABC):

    @abstractmethod
    def areCheerActionsEnabled(self) -> bool:
        pass

    @abstractmethod
    def areRecurringActionsEnabled(self) -> bool:
        pass

    @abstractmethod
    def getCasualGamePollRewardId(self) -> Optional[str]:
        pass

    @abstractmethod
    def getCasualGamePollUrl(self) -> Optional[str]:
        pass

    @abstractmethod
    def getCutenessBoosterPacks(self) -> Optional[List[CutenessBoosterPack]]:
        pass

    @abstractmethod
    def getDiscordUrl(self) -> Optional[str]:
        pass

    @abstractmethod
    def getHandle(self) -> str:
        pass

    @abstractmethod
    def getLocationId(self) -> Optional[str]:
        pass

    @abstractmethod
    def getMastodonUrl(self) -> Optional[str]:
        pass

    @abstractmethod
    def getMaximumTtsCheerAmount(self) -> Optional[int]:
        pass

    @abstractmethod
    def getMinimumTtsCheerAmount(self) -> Optional[int]:
        pass

    @abstractmethod
    def getPkmnBattleRewardId(self) -> Optional[str]:
        pass

    @abstractmethod
    def getPkmnEvolveRewardId(self) -> Optional[str]:
        pass

    @abstractmethod
    def getPkmnShinyRewardId(self) -> Optional[str]:
        pass

    @abstractmethod
    def getSpeedrunProfile(self) -> Optional[str]:
        pass

    @abstractmethod
    def getSuperTriviaCheerTriggerAmount(self) -> Optional[int]:
        pass

    @abstractmethod
    def getSuperTriviaCheerTriggerMaximum(self) -> Optional[int]:
        pass

    @abstractmethod
    def getSuperTriviaGamePoints(self) -> Optional[int]:
        pass

    @abstractmethod
    def getSuperTriviaGameRewardId(self) -> Optional[str]:
        pass

    @abstractmethod
    def getSuperTriviaGameShinyMultiplier(self) -> Optional[int]:
        pass

    @abstractmethod
    def getSuperTriviaGameToxicMultiplier(self) -> Optional[int]:
        pass

    @abstractmethod
    def getSuperTriviaGameToxicPunishmentMultiplier(self) -> Optional[int]:
        pass

    @abstractmethod
    def getSuperTriviaPerUserAttempts(self) -> Optional[int]:
        pass

    @abstractmethod
    def getSuperTriviaSubscribeTriggerAmount(self) -> Optional[float]:
        pass

    @abstractmethod
    def getSuperTriviaSubscribeTriggerMaximum(self) -> Optional[float]:
        pass

    @abstractmethod
    def getSupStreamerMessage(self) -> Optional[str]:
        pass

    @abstractmethod
    def getTimeZones(self) -> Optional[List[tzinfo]]:
        pass

    @abstractmethod
    def getTriviaGamePoints(self) -> Optional[int]:
        pass

    @abstractmethod
    def getTriviaGameRewardId(self) -> Optional[str]:
        pass

    @abstractmethod
    def getTriviaGameShinyMultiplier(self) -> Optional[int]:
        pass

    @abstractmethod
    def getTwitterUrl(self) -> Optional[str]:
        pass

    @abstractmethod
    def getWaitForSuperTriviaAnswerDelay(self) -> Optional[int]:
        pass

    @abstractmethod
    def getWaitForTriviaAnswerDelay(self) -> Optional[int]:
        pass

    @abstractmethod
    def hasCutenessBoosterPacks(self) -> bool:
        pass

    @abstractmethod
    def hasDiscord(self) -> bool:
        pass

    @abstractmethod
    def hasLocationId(self) -> bool:
        pass

    @abstractmethod
    def hasPkmnCatchBoosterPacks(self) -> bool:
        pass

    @abstractmethod
    def hasSpeedrunProfile(self) -> bool:
        pass

    @abstractmethod
    def hasTimeZones(self) -> bool:
        pass

    @abstractmethod
    def hasTwitter(self) -> bool:
        pass

    @abstractmethod
    def isAnivContentScanningEnabled(self) -> bool:
        pass

    @abstractmethod
    def isCasualGamePollEnabled(self) -> bool:
        pass

    @abstractmethod
    def isCatJamMessageEnabled(self) -> bool:
        pass

    @abstractmethod
    def isChannelPredictionChartEnabled(self) -> bool:
        pass

    @abstractmethod
    def isChatLoggingEnabled(self) -> bool:
        pass

    @abstractmethod
    def isCutenessEnabled(self) -> bool:
        pass

    @abstractmethod
    def isCynanSourceEnabled(self) -> bool:
        pass

    @abstractmethod
    def isDeerForceMessageEnabled(self) -> bool:
        pass

    @abstractmethod
    def isEnabled(self) -> bool:
        pass

    @abstractmethod
    def isGiveCutenessEnabled(self) -> bool:
        pass

    @abstractmethod
    def isJishoEnabled(self) -> bool:
        pass

    @abstractmethod
    def isLoremIpsumEnabled(self) -> bool:
        pass

    @abstractmethod
    def isPkmnEnabled(self) -> bool:
        pass

    @abstractmethod
    def isPokepediaEnabled(self) -> bool:
        pass

    @abstractmethod
    def isRaceEnabled(self) -> bool:
        pass

    @abstractmethod
    def isSchubertWalkMessageEnabled(self) -> bool:
        pass

    @abstractmethod
    def isShinyTriviaEnabled(self) -> bool:
        pass

    @abstractmethod
    def isStarWarsQuotesEnabled(self) -> bool:
        pass

    @abstractmethod
    def isSuperTriviaGameEnabled(self) -> bool:
        pass

    @abstractmethod
    def isSupStreamerEnabled(self) -> bool:
        pass

    @abstractmethod
    def isToxicTriviaEnabled(self) -> bool:
        pass

    @abstractmethod
    def isTranslateEnabled(self) -> bool:
        pass

    @abstractmethod
    def isTriviaGameEnabled(self) -> bool:
        pass

    @abstractmethod
    def isTriviaScoreEnabled(self) -> bool:
        pass

    @abstractmethod
    def isTtsEnabled(self) -> bool:
        pass

    @abstractmethod
    def isWeatherEnabled(self) -> bool:
        pass

    @abstractmethod
    def isWelcomeTtsEnabled(self) -> bool:
        pass

    @abstractmethod
    def isWordOfTheDayEnabled(self) -> bool:
        pass
