from abc import ABC, abstractmethod
from datetime import tzinfo

from frozendict import frozendict
from frozenlist import FrozenList

from .crowdControl.crowdControlBoosterPack import CrowdControlBoosterPack
from .pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from .soundAlertRedemption import SoundAlertRedemption
from .tts.ttsBoosterPack import TtsBoosterPack
from ..cuteness.cutenessBoosterPack import CutenessBoosterPack


class UserInterface(ABC):

    @property
    @abstractmethod
    def anivMessageCopyMaxAgeSeconds(self) -> int | None:
        pass

    @property
    @abstractmethod
    def anivMessageCopyTimeoutProbability(self) -> float | None:
        pass

    @property
    @abstractmethod
    def anivMessageCopyTimeoutMinSeconds(self) -> int | None:
        pass

    @property
    @abstractmethod
    def anivMessageCopyTimeoutMaxSeconds(self) -> int | None:
        pass

    @property
    @abstractmethod
    def areBeanChancesEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def areCheerActionsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def areRecurringActionsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def areSoundAlertsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def areTimeoutCheerActionsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def crowdControlBoosterPacks(self) -> frozendict[str, CrowdControlBoosterPack] | None:
        pass

    @property
    @abstractmethod
    def crowdControlButtonPressRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def crowdControlGameShuffleRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def cutenessBoosterPacks(self) -> frozendict[str, CutenessBoosterPack] | None:
        pass

    @abstractmethod
    def getCasualGamePollRewardId(self) -> str | None:
        pass

    @abstractmethod
    def getCasualGamePollUrl(self) -> str | None:
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
    def hasDiscord(self) -> bool:
        pass

    @abstractmethod
    def hasLocationId(self) -> bool:
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

    @property
    @abstractmethod
    def isAnivContentScanningEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isAnivMessageCopyTimeoutChatReportingEnabled(self) -> bool:
        pass

    @property
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

    @property
    @abstractmethod
    def isCrowdControlEnabled(self) -> bool:
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

    @property
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

    @property
    @abstractmethod
    def isNotifyOfPollResultsEnabled(self) -> bool:
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

    @property
    @abstractmethod
    def isShizaMessageEnabled(self) -> bool:
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

    @property
    @abstractmethod
    def isSuperTriviaLotrTimeoutEnabled(self) -> bool:
        pass

    @abstractmethod
    def isSupStreamerEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isTimeoutCheerActionIncreasedBullyFailureEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isTimeoutCheerActionFailureEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isTimeoutCheerActionReverseEnabled(self) -> bool:
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

    @property
    @abstractmethod
    def isTtsMonsterApiUsageReportingEnabled(self) -> bool:
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
    def pkmnBattleRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def pkmnCatchBoosterPacks(self) -> frozendict[str, PkmnCatchBoosterPack] | None:
        pass

    @property
    @abstractmethod
    def shizaMessageRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def soundAlertRedemptions(self) -> frozendict[str, SoundAlertRedemption] | None:
        pass

    @property
    @abstractmethod
    def timeoutCheerActionFollowShieldDays(self) -> int | None:
        pass

    @property
    @abstractmethod
    def timeZones(self) -> FrozenList[tzinfo] | None:
        pass

    @property
    @abstractmethod
    def ttsBoosterPacks(self) -> frozendict[int, TtsBoosterPack] | None:
        pass
