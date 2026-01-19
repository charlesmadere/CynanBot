from abc import ABC, abstractmethod
from datetime import tzinfo

from frozendict import frozendict
from frozenlist import FrozenList

from .chatSoundAlert.absChatSoundAlert import AbsChatSoundAlert
from .crowdControl.crowdControlBoosterPack import CrowdControlBoosterPack
from .cuteness.cutenessBoosterPack import CutenessBoosterPack
from .decTalkSongs.decTalkSongBoosterPack import DecTalkSongBoosterPack
from .pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from .redemptionCounter.redemptionCounterBoosterPack import RedemptionCounterBoosterPack
from .soundAlert.soundAlertRedemption import SoundAlertRedemption
from .supStreamer.supStreamerBoosterPack import SupStreamerBoosterPack
from .timeout.timeoutBoosterPack import TimeoutBoosterPack
from .tts.ttsBoosterPack import TtsBoosterPack
from ..aniv.models.whichAnivUser import WhichAnivUser
from ..language.languageEntry import LanguageEntry
from ..tts.models.ttsProvider import TtsProvider


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
    def areAsplodieStatsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def areBeanStatsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def areChatSoundAlertsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def areCheerActionsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def arePranksEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def areRecurringActionsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def areRedemptionCountersEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def areSoundAlertsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def areTtsChattersEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def blueSkyUrl(self) -> str | None:
        pass

    @property
    @abstractmethod
    def chatSoundAlerts(self) -> FrozenList[AbsChatSoundAlert] | None:
        pass

    @property
    @abstractmethod
    def chatterPreferredNameRewardId(self) -> str | None:
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

    @property
    @abstractmethod
    def decTalkSongBoosterPacks(self) -> frozendict[str, DecTalkSongBoosterPack] | None:
        pass

    @property
    @abstractmethod
    def defaultLanguage(self) -> LanguageEntry:
        pass

    @property
    @abstractmethod
    def defaultTtsProvider(self) -> TtsProvider:
        pass

    @property
    @abstractmethod
    def casualGamePollRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def casualGamePollUrl(self) -> str | None:
        pass

    @property
    @abstractmethod
    def chatBackMessages(self) -> FrozenList[str] | None:
        pass

    @property
    @abstractmethod
    def discordUrl(self) -> str | None:
        pass

    @property
    @abstractmethod
    def handle(self) -> str:
        pass

    @property
    @abstractmethod
    def locationId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def mastodonUrl(self) -> str | None:
        pass

    @property
    @abstractmethod
    def maximumTtsCheerAmount(self) -> int | None:
        pass

    @property
    @abstractmethod
    def minimumTtsCheerAmount(self) -> int | None:
        pass

    @property
    @abstractmethod
    def pkmnEvolveRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def pkmnShinyRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def randomSoundAlertRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def speedrunProfile(self) -> str | None:
        pass

    @property
    @abstractmethod
    def soundAlertRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def superTriviaCheerTriggerAmount(self) -> int | None:
        pass

    @property
    @abstractmethod
    def superTriviaCheerTriggerMaximum(self) -> int | None:
        pass

    @property
    @abstractmethod
    def superTriviaGamePoints(self) -> int | None:
        pass

    @property
    @abstractmethod
    def superTriviaGameRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def superTriviaLotrGameRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def superTriviaGameShinyMultiplier(self) -> int | None:
        pass

    @property
    @abstractmethod
    def superTriviaGameToxicMultiplier(self) -> int | None:
        pass

    @property
    @abstractmethod
    def superTriviaGameToxicPunishmentMultiplier(self) -> int | None:
        pass

    @property
    @abstractmethod
    def superTriviaPerUserAttempts(self) -> int | None:
        pass

    @property
    @abstractmethod
    def superTriviaSubscribeTriggerAmount(self) -> float | None:
        pass

    @property
    @abstractmethod
    def superTriviaSubscribeTriggerMaximum(self) -> int | None:
        pass

    @property
    @abstractmethod
    def supStreamerMessage(self) -> str | None:
        pass

    @property
    @abstractmethod
    def supStreamerBoosterPacks(self) -> FrozenList[SupStreamerBoosterPack] | None:
        pass

    @property
    @abstractmethod
    def triviaGamePoints(self) -> int | None:
        pass

    @property
    @abstractmethod
    def triviaGameRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def triviaGameShinyMultiplier(self) -> int | None:
        pass

    @property
    @abstractmethod
    def ttsChatterRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def waitForSuperTriviaAnswerDelay(self) -> int | None:
        pass

    @property
    @abstractmethod
    def waitForTriviaAnswerDelay(self) -> int | None:
        pass

    @property
    @abstractmethod
    def hasLocationId(self) -> bool:
        pass

    @property
    @abstractmethod
    def hasSpeedrunProfile(self) -> bool:
        pass

    @property
    @abstractmethod
    def hasTimeZones(self) -> bool:
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

    @property
    @abstractmethod
    def isCasualGamePollEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isChannelPredictionChartEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isChatBackMessagesEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isChatLoggingEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isChatterInventoryEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isChatterPreferredNameEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isChatterPreferredTtsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isCrowdControlEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isCutenessEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isDecTalkSongsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isEccoEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isGiveCutenessEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isJishoEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isLoremIpsumEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isNotifyOfHypeTrainProgressEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isNotifyOfHypeTrainStartEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isNotifyOfPollResultsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isNotifyOfPollStartEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isNotifyOfPredictionResultsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isNotifyOfPredictionStartEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isNotifyOfRaidEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isPkmnEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isPokepediaEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isRaceEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isShinyTriviaEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isStarWarsQuotesEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isSubGiftThankingEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isSuperTriviaGameEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isSuperTriviaLotrTimeoutEnabled(self) -> bool:
        pass

    @property
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

    @property
    @abstractmethod
    def isToxicTriviaEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isTranslateEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isTriviaGameEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isTriviaScoreEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isTtsEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isVoicemailEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isVulnerableChattersEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isWatchStreakTtsAnnounceEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isWeatherEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def isWordOfTheDayEnabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def minimumRaidViewersForNotification(self) -> int | None:
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
    def redemptionCounterBoosterPacks(self) -> frozendict[str, RedemptionCounterBoosterPack] | None:
        pass

    @property
    @abstractmethod
    def setChatterPreferredTtsRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def soundAlertRedemptions(self) -> frozendict[str, SoundAlertRedemption] | None:
        pass

    @property
    @abstractmethod
    def timeoutActionFollowShieldDays(self) -> int | None:
        pass

    @property
    @abstractmethod
    def timeoutBoosterPacks(self) -> frozendict[str, TimeoutBoosterPack] | None:
        pass

    @property
    @abstractmethod
    def timeZones(self) -> FrozenList[tzinfo] | None:
        pass

    @property
    @abstractmethod
    def ttsBoosterPacks(self) -> FrozenList[TtsBoosterPack] | None:
        pass

    @property
    @abstractmethod
    def voicemailRewardId(self) -> str | None:
        pass

    @property
    @abstractmethod
    def whichAnivUser(self) -> WhichAnivUser | None:
        pass
