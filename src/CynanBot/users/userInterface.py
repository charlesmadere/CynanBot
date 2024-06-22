from abc import ABC, abstractmethod
from datetime import tzinfo

from CynanBot.cuteness.cutenessBoosterPack import CutenessBoosterPack
from CynanBot.users.soundAlertRedemption import SoundAlertRedemption


class UserInterface(ABC):

    @property
    @abstractmethod
    def anivMessageCopyMaxAgeSeconds(self) -> int | None:
        pass

    @abstractmethod
    def areCheerActionsEnabled(self) -> bool:
        pass

    @abstractmethod
    def areRecurringActionsEnabled(self) -> bool:
        pass

    @abstractmethod
    def areSoundAlertsEnabled(self) -> bool:
        pass

    @abstractmethod
    def getAnivMessageCopyTimeoutChance(self) -> float | None:
        pass

    @abstractmethod
    def getAnivMessageCopyTimeoutSeconds(self) -> int | None:
        pass

    @abstractmethod
    def getCasualGamePollRewardId(self) -> str | None:
        pass

    @abstractmethod
    def getCasualGamePollUrl(self) -> str | None:
        pass

    @abstractmethod
    def getCutenessBoosterPacks(self) -> list[CutenessBoosterPack] | None:
        pass

    @abstractmethod
    def getDiscordUrl(self) -> str | None:
        pass

    @abstractmethod
    def getHandle(self) -> str:
        pass

    @abstractmethod
    def getLocationId(self) -> str | None:
        pass

    @abstractmethod
    def getMastodonUrl(self) -> str | None:
        pass

    @abstractmethod
    def getMaximumTtsCheerAmount(self) -> int | None:
        pass

    @abstractmethod
    def getMinimumTtsCheerAmount(self) -> int | None:
        pass

    @abstractmethod
    def getPkmnBattleRewardId(self) -> str | None:
        pass

    @abstractmethod
    def getPkmnEvolveRewardId(self) -> str | None:
        pass

    @abstractmethod
    def getPkmnShinyRewardId(self) -> str | None:
        pass

    @abstractmethod
    def getRandomSoundAlertRewardId(self) -> str | None:
        pass

    @abstractmethod
    def getSpeedrunProfile(self) -> str | None:
        pass

    @abstractmethod
    def getSoundAlertRedemptions(self) -> dict[str, SoundAlertRedemption] | None:
        pass

    @abstractmethod
    def getSoundAlertRewardId(self) -> str | None:
        pass

    @abstractmethod
    def getSuperTriviaCheerTriggerAmount(self) -> float | None:
        pass

    @abstractmethod
    def getSuperTriviaCheerTriggerMaximum(self) -> int | None:
        pass

    @abstractmethod
    def getSuperTriviaGamePoints(self) -> int | None:
        pass

    @abstractmethod
    def getSuperTriviaGameRewardId(self) -> str | None:
        pass

    @abstractmethod
    def getSuperTriviaGameShinyMultiplier(self) -> int | None:
        pass

    @abstractmethod
    def getSuperTriviaGameToxicMultiplier(self) -> int | None:
        pass

    @abstractmethod
    def getSuperTriviaGameToxicPunishmentMultiplier(self) -> int | None:
        pass

    @abstractmethod
    def getSuperTriviaPerUserAttempts(self) -> int | None:
        pass

    @abstractmethod
    def getSuperTriviaSubscribeTriggerAmount(self) -> float | None:
        pass

    @abstractmethod
    def getSuperTriviaSubscribeTriggerMaximum(self) -> float | None:
        pass

    @abstractmethod
    def getSupStreamerMessage(self) -> str | None:
        pass

    @abstractmethod
    def getTimeZones(self) -> list[tzinfo] | None:
        pass

    @abstractmethod
    def getTriviaGamePoints(self) -> int | None:
        pass

    @abstractmethod
    def getTriviaGameRewardId(self) -> str | None:
        pass

    @abstractmethod
    def getTriviaGameShinyMultiplier(self) -> int | None:
        pass

    @abstractmethod
    def getTwitterUrl(self) -> str | None:
        pass

    @abstractmethod
    def getWaitForSuperTriviaAnswerDelay(self) -> int | None:
        pass

    @abstractmethod
    def getWaitForTriviaAnswerDelay(self) -> int | None:
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
    def isAnivMessageCopyTimeoutEnabled(self) -> bool:
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

    @property
    @abstractmethod
    def isSubGiftThankingEnabled(self) -> bool:
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

    @property
    @abstractmethod
    def timeoutCheerActionFollowShieldDays(self) -> int | None:
        pass
