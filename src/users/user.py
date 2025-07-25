from datetime import tzinfo

from frozendict import frozendict
from frozenlist import FrozenList

from .aniv.whichAnivUser import WhichAnivUser
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
from .userInterface import UserInterface
from ..language.languageEntry import LanguageEntry
from ..misc import utils as utils
from ..tts.models.ttsProvider import TtsProvider


class User(UserInterface):

    def __init__(
        self,
        areAsplodieStatsEnabled: bool,
        areBeanStatsEnabled: bool,
        areChatSoundAlertsEnabled: bool,
        areCheerActionsEnabled: bool,
        arePranksEnabled: bool,
        areRecurringActionsEnabled: bool,
        areRedemptionCountersEnabled: bool,
        areSoundAlertsEnabled: bool,
        areTtsChattersEnabled: bool,
        isAnivContentScanningEnabled: bool,
        isAnivMessageCopyTimeoutChatReportingEnabled: bool,
        isAnivMessageCopyTimeoutEnabled: bool,
        isCasualGamePollEnabled: bool,
        isChannelPredictionChartEnabled: bool,
        isChatBackMessagesEnabled: bool,
        isChatBandEnabled: bool,
        isChatLoggingEnabled: bool,
        isChatterPreferredTtsEnabled: bool,
        isCrowdControlEnabled: bool,
        isCutenessEnabled: bool,
        isDecTalkSongsEnabled: bool,
        isEccoEnabled: bool,
        isEnabled: bool,
        isGiveCutenessEnabled: bool,
        isJishoEnabled: bool,
        isLoremIpsumEnabled: bool,
        isNotifyOfPollResultsEnabled: bool,
        isNotifyOfPollStartEnabled: bool,
        isNotifyOfPredictionResultsEnabled: bool,
        isNotifyOfPredictionStartEnabled: bool,
        isNotifyOfRaidEnabled: bool,
        isPkmnEnabled: bool,
        isPokepediaEnabled: bool,
        isRaceEnabled: bool,
        isShinyTriviaEnabled: bool,
        isStarWarsQuotesEnabled: bool,
        isSubGiftThankingEnabled: bool,
        isSuperTriviaGameEnabled: bool,
        isSuperTriviaLotrTimeoutEnabled: bool,
        isSupStreamerEnabled: bool,
        isTimeoutCheerActionIncreasedBullyFailureEnabled: bool,
        isTimeoutCheerActionFailureEnabled: bool,
        isTimeoutCheerActionReverseEnabled: bool,
        isToxicTriviaEnabled: bool,
        isTranslateEnabled: bool,
        isTriviaGameEnabled: bool,
        isTriviaScoreEnabled: bool,
        isTtsEnabled: bool,
        isTtsMonsterApiUsageReportingEnabled: bool,
        isVoicemailEnabled: bool,
        isVulnerableChattersEnabled: bool,
        isWeatherEnabled: bool,
        isWordOfTheDayEnabled: bool,
        anivMessageCopyTimeoutProbability: float | None,
        superTriviaSubscribeTriggerAmount: float | None,
        anivMessageCopyMaxAgeSeconds: int | None,
        anivMessageCopyTimeoutMinSeconds: int | None,
        anivMessageCopyTimeoutMaxSeconds: int | None,
        maximumGrenadesWithinCooldown: int | None,
        maximumTtsCheerAmount: int | None,
        minimumRaidViewersForNotification: int | None,
        minimumTtsCheerAmount: int | None,
        superTriviaCheerTriggerAmount: int | None,
        superTriviaCheerTriggerMaximum: int | None,
        superTriviaGamePoints: int | None,
        superTriviaGameRewardId: str | None,
        superTriviaGameShinyMultiplier: int | None,
        superTriviaGameToxicMultiplier: int | None,
        superTriviaGameToxicPunishmentMultiplier: int | None,
        superTriviaPerUserAttempts: int | None,
        superTriviaSubscribeTriggerMaximum: int | None,
        timeoutActionFollowShieldDays: int | None,
        triviaGamePoints: int | None,
        triviaGameShinyMultiplier: int | None,
        waitForSuperTriviaAnswerDelay: int | None,
        waitForTriviaAnswerDelay: int | None,
        defaultLanguage: LanguageEntry,
        blueSkyUrl: str | None,
        casualGamePollRewardId: str | None,
        casualGamePollUrl: str | None,
        crowdControlButtonPressRewardId: str | None,
        crowdControlGameShuffleRewardId: str | None,
        discordUrl: str | None,
        handle: str,
        instagram: str | None,
        locationId: str | None,
        mastodonUrl: str | None,
        pkmnBattleRewardId: str | None,
        pkmnEvolveRewardId: str | None,
        pkmnShinyRewardId: str | None,
        randomSoundAlertRewardId: str | None,
        setChatterPreferredTtsRewardId: str | None,
        soundAlertRewardId: str | None,
        speedrunProfile: str | None,
        supStreamerMessage: str | None,
        triviaGameRewardId: str | None,
        ttsChatterRewardId: str | None,
        voicemailRewardId: str | None,
        defaultTtsProvider: TtsProvider,
        whichAnivUser: WhichAnivUser | None,
        crowdControlBoosterPacks: frozendict[str, CrowdControlBoosterPack] | None,
        cutenessBoosterPacks: frozendict[str, CutenessBoosterPack] | None,
        decTalkSongBoosterPacks: frozendict[str, DecTalkSongBoosterPack] | None,
        pkmnCatchBoosterPacks: frozendict[str, PkmnCatchBoosterPack] | None,
        redemptionCounterBoosterPacks: frozendict[str, RedemptionCounterBoosterPack] | None,
        soundAlertRedemptions: frozendict[str, SoundAlertRedemption] | None,
        timeoutBoosterPacks: frozendict[str, TimeoutBoosterPack] | None,
        chatSoundAlerts: FrozenList[AbsChatSoundAlert] | None,
        chatBackMessages: FrozenList[str] | None,
        supStreamerBoosterPacks: FrozenList[SupStreamerBoosterPack] | None,
        ttsBoosterPacks: FrozenList[TtsBoosterPack] | None,
        timeZones: FrozenList[tzinfo] | None,
    ):
        if not utils.isValidBool(areAsplodieStatsEnabled):
            raise TypeError(f'areAsplodieStatsEnabled argument is malformed: \"{areAsplodieStatsEnabled}\"')
        elif not utils.isValidBool(areBeanStatsEnabled):
            raise TypeError(f'areBeanStatsEnabled argument is malformed: \"{areBeanStatsEnabled}\"')
        elif not utils.isValidBool(areChatSoundAlertsEnabled):
            raise TypeError(f'areChatSoundAlertsEnabled argument is malformed: \"{areChatSoundAlertsEnabled}\"')
        elif not utils.isValidBool(areCheerActionsEnabled):
            raise TypeError(f'areCheerActionsEnabled argument is malformed: \"{areCheerActionsEnabled}\"')
        elif not utils.isValidBool(arePranksEnabled):
            raise TypeError(f'arePranksEnabled argument is malformed: \"{arePranksEnabled}\"')
        elif not utils.isValidBool(areRecurringActionsEnabled):
            raise TypeError(f'areRecurringActionsEnabled argument is malformed: \"{areRecurringActionsEnabled}\"')
        elif not utils.isValidBool(areRedemptionCountersEnabled):
            raise TypeError(f'areRedemptionCountersEnabled argument is malformed: \"{areRedemptionCountersEnabled}\"')
        elif not utils.isValidBool(areSoundAlertsEnabled):
            raise TypeError(f'areSoundAlertsEnabled argument is malformed: \"{areSoundAlertsEnabled}\"')
        elif not utils.isValidBool(areTtsChattersEnabled):
            raise TypeError(f'areTtsChattersEnabled argument is malformed: \"{areTtsChattersEnabled}\"')
        elif not utils.isValidBool(isAnivContentScanningEnabled):
            raise TypeError(f'isAnivContentScanningEnabled argument is malformed: \"{isAnivContentScanningEnabled}\"')
        elif not utils.isValidBool(isAnivMessageCopyTimeoutChatReportingEnabled):
            raise TypeError(f'isAnivMessageCopyTimeoutChatReportingEnabled argument is malformed: \"{isAnivMessageCopyTimeoutChatReportingEnabled}\"')
        elif not utils.isValidBool(isAnivMessageCopyTimeoutEnabled):
            raise TypeError(f'isAnivMessageCopyTimeoutEnabled argument is malformed: \"{isAnivMessageCopyTimeoutEnabled}\"')
        elif not utils.isValidBool(isCasualGamePollEnabled):
            raise TypeError(f'isCasualGamePollEnabled argument is malformed: \"{isCasualGamePollEnabled}\"')
        elif not utils.isValidBool(isChannelPredictionChartEnabled):
            raise TypeError(f'isChannelPredictionChartEnabled argument is malformed: \"{isChannelPredictionChartEnabled}\"')
        elif not utils.isValidBool(isChatBackMessagesEnabled):
            raise TypeError(f'isChatBackMessagesEnabled argument is malformed: \"{isChatBackMessagesEnabled}\"')
        elif not utils.isValidBool(isChatBandEnabled):
            raise TypeError(f'isChatBandEnabled argument is malformed: \"{isChatBandEnabled}\"')
        elif not utils.isValidBool(isChatLoggingEnabled):
            raise TypeError(f'isChatLoggingEnabled argument is malformed: \"{isChatLoggingEnabled}\"')
        elif not utils.isValidBool(isChatterPreferredTtsEnabled):
            raise TypeError(f'isChatterPreferredTtsEnabled argument is malformed: \"{isChatterPreferredTtsEnabled}\"')
        elif not utils.isValidBool(isCrowdControlEnabled):
            raise TypeError(f'isCrowdControlEnabled argument is malformed: \"{isCrowdControlEnabled}\"')
        elif not utils.isValidBool(isCutenessEnabled):
            raise TypeError(f'isCutenessEnabled argument is malformed: \"{isCutenessEnabled}\"')
        elif not utils.isValidBool(isDecTalkSongsEnabled):
            raise TypeError(f'isDecTalkSongsEnabled argument is malformed: \"{isDecTalkSongsEnabled}\"')
        elif not utils.isValidBool(isEccoEnabled):
            raise TypeError(f'isEccoEnabled argument is malformed: \"{isEccoEnabled}\"')
        elif not utils.isValidBool(isEnabled):
            raise TypeError(f'isEnabled argument is malformed: \"{isEnabled}\"')
        elif not utils.isValidBool(isGiveCutenessEnabled):
            raise TypeError(f'isGiveCutenessEnabled argument is malformed: \"{isGiveCutenessEnabled}\"')
        elif not utils.isValidBool(isJishoEnabled):
            raise TypeError(f'isJishoEnabled argument is malformed: \"{isJishoEnabled}\"')
        elif not utils.isValidBool(isLoremIpsumEnabled):
            raise TypeError(f'isLoremIpsumEnabled argument is malformed: \"{isLoremIpsumEnabled}\"')
        elif not utils.isValidBool(isNotifyOfPollResultsEnabled):
            raise TypeError(f'isNotifyOfPollResultsEnabled argument is malformed: \"{isNotifyOfPollResultsEnabled}\"')
        elif not utils.isValidBool(isNotifyOfPollStartEnabled):
            raise TypeError(f'isNotifyOfPollStartEnabled argument is malformed: \"{isNotifyOfPollStartEnabled}\"')
        elif not utils.isValidBool(isNotifyOfPredictionResultsEnabled):
            raise TypeError(f'isNotifyOfPredictionResultsEnabled argument is malformed: \"{isNotifyOfPredictionResultsEnabled}\"')
        elif not utils.isValidBool(isNotifyOfPredictionStartEnabled):
            raise TypeError(f'isNotifyOfPredictionStartEnabled argument is malformed: \"{isNotifyOfPredictionStartEnabled}\"')
        elif not utils.isValidBool(isNotifyOfRaidEnabled):
            raise TypeError(f'isNotifyOfRaidEnabled argument is malformed: \"{isNotifyOfRaidEnabled}\"')
        elif not utils.isValidBool(isPkmnEnabled):
            raise TypeError(f'isPkmnEnabled argument is malformed: \"{isPkmnEnabled}\"')
        elif not utils.isValidBool(isPokepediaEnabled):
            raise TypeError(f'isPokepediaEnabled argument is malformed: \"{isPokepediaEnabled}\"')
        elif not utils.isValidBool(isRaceEnabled):
            raise TypeError(f'isRaceEnabled argument is malformed: \"{isRaceEnabled}\"')
        elif not utils.isValidBool(isShinyTriviaEnabled):
            raise TypeError(f'isShinyTriviaEnabled argument is malformed: \"{isShinyTriviaEnabled}\"')
        elif not utils.isValidBool(isStarWarsQuotesEnabled):
            raise TypeError(f'isStarWarsQuotesEnabled argument is malformed: \"{isStarWarsQuotesEnabled}\"')
        elif not utils.isValidBool(isSubGiftThankingEnabled):
            raise TypeError(f'isSubGiftThankingEnabled argument is malformed: \"{isSubGiftThankingEnabled}\"')
        elif not utils.isValidBool(isSuperTriviaGameEnabled):
            raise TypeError(f'isSuperTriviaGameEnabled argument is malformed: \"{isSuperTriviaGameEnabled}\"')
        elif not utils.isValidBool(isSuperTriviaLotrTimeoutEnabled):
            raise TypeError(f'isSuperTriviaLotrTimeoutEnabled argument is malformed: \"{isSuperTriviaLotrTimeoutEnabled}\"')
        elif not utils.isValidBool(isSupStreamerEnabled):
            raise TypeError(f'isSupStreamerEnabled argument is malformed: \"{isSupStreamerEnabled}\"')
        elif not utils.isValidBool(isTimeoutCheerActionIncreasedBullyFailureEnabled):
            raise TypeError(f'isTimeoutCheerActionIncreasedBullyFailureEnabled argument is malformed: \"{isTimeoutCheerActionIncreasedBullyFailureEnabled}\"')
        elif not utils.isValidBool(isTimeoutCheerActionFailureEnabled):
            raise TypeError(f'isTimeoutCheerActionFailureEnabled argument is malformed: \"{isTimeoutCheerActionFailureEnabled}\"')
        elif not utils.isValidBool(isTimeoutCheerActionReverseEnabled):
            raise TypeError(f'isTimeoutCheerActionReverseEnabled argument is malformed: \"{isTimeoutCheerActionReverseEnabled}\"')
        elif not utils.isValidBool(isToxicTriviaEnabled):
            raise TypeError(f'isToxicTriviaEnabled argument is malformed: \"{isToxicTriviaEnabled}\"')
        elif not utils.isValidBool(isTranslateEnabled):
            raise TypeError(f'isTranslateEnabled argument is malformed: \"{isTranslateEnabled}\"')
        elif not utils.isValidBool(isTriviaGameEnabled):
            raise TypeError(f'isTriviaGameEnabled argument is malformed: \"{isTriviaGameEnabled}\"')
        elif not utils.isValidBool(isTriviaScoreEnabled):
            raise TypeError(f'isTriviaScoreEnabled argument is malformed: \"{isTriviaScoreEnabled}\"')
        elif not utils.isValidBool(isTtsEnabled):
            raise TypeError(f'isTtsEnabled argument is malformed: \"{isTtsEnabled}\"')
        elif not utils.isValidBool(isTtsMonsterApiUsageReportingEnabled):
            raise TypeError(f'isTtsMonsterApiUsageReportingEnabled argument is malformed: \"{isTtsMonsterApiUsageReportingEnabled}\"')
        elif not utils.isValidBool(isVoicemailEnabled):
            raise TypeError(f'isVoicemailEnabled argument is malformed: \"{isVoicemailEnabled}\"')
        elif not utils.isValidBool(isVulnerableChattersEnabled):
            raise TypeError(f'isVulnerableChattersEnabled argument is malformed: \"{isVulnerableChattersEnabled}\"')
        elif not utils.isValidBool(isWeatherEnabled):
            raise TypeError(f'isWeatherEnabled argument is malformed: \"{isWeatherEnabled}\"')
        elif not utils.isValidBool(isWordOfTheDayEnabled):
            raise TypeError(f'isWordOfTheDayEnabled argument is malformed: \"{isWordOfTheDayEnabled}\"')
        elif anivMessageCopyTimeoutProbability is not None and not utils.isValidNum(anivMessageCopyTimeoutProbability):
            raise TypeError(f'anivMessageCopyTimeoutProbability argument is malformed: \"{anivMessageCopyTimeoutProbability}\"')
        elif superTriviaSubscribeTriggerAmount is not None and not utils.isValidNum(superTriviaSubscribeTriggerAmount):
            raise TypeError(f'superTriviaSubscribeTriggerAmount argument is malformed: \"{superTriviaSubscribeTriggerAmount}\"')
        elif anivMessageCopyMaxAgeSeconds is not None and not utils.isValidInt(anivMessageCopyMaxAgeSeconds):
            raise TypeError(f'anivMessageCopyMaxAgeSeconds argument is malformed: \"{anivMessageCopyMaxAgeSeconds}\"')
        elif anivMessageCopyTimeoutMinSeconds is not None and not utils.isValidInt(anivMessageCopyTimeoutMinSeconds):
            raise TypeError(f'anivMessageCopyTimeoutMinSeconds argument is malformed: \"{anivMessageCopyTimeoutMinSeconds}\"')
        elif anivMessageCopyTimeoutMaxSeconds is not None and not utils.isValidInt(anivMessageCopyTimeoutMaxSeconds):
            raise TypeError(f'anivMessageCopyTimeoutMaxSeconds argument is malformed: \"{anivMessageCopyTimeoutMaxSeconds}\"')
        elif maximumGrenadesWithinCooldown is not None and not utils.isValidInt(maximumGrenadesWithinCooldown):
            raise TypeError(f'maximumGrenadesWithinCooldown argument is malformed: \"{maximumGrenadesWithinCooldown}\"')
        elif maximumTtsCheerAmount is not None and not utils.isValidInt(maximumTtsCheerAmount):
            raise TypeError(f'maximumTtsCheerAmount argument is malformed: \"{maximumTtsCheerAmount}\"')
        elif minimumRaidViewersForNotification is not None and not utils.isValidInt(minimumRaidViewersForNotification):
            raise TypeError(f'minimumRaidViewersForNotification argument is malformed: \"{minimumRaidViewersForNotification}\"')
        elif minimumTtsCheerAmount is not None and not utils.isValidInt(minimumTtsCheerAmount):
            raise TypeError(f'minimumTtsCheerAmount argument is malformed: \"{minimumTtsCheerAmount}\"')
        elif superTriviaGamePoints is not None and not utils.isValidInt(superTriviaGamePoints):
            raise TypeError(f'superTriviaGamePoints argument is malformed: \"{superTriviaGamePoints}\"')
        elif superTriviaCheerTriggerAmount is not None and not utils.isValidInt(superTriviaCheerTriggerAmount):
            raise TypeError(f'superTriviaCheerTriggerAmount argument is malformed: \"{superTriviaCheerTriggerAmount}\"')
        elif superTriviaCheerTriggerMaximum is not None and not utils.isValidInt(superTriviaCheerTriggerMaximum):
            raise TypeError(f'superTriviaCheerTriggerMaximum argument is malformed: \"{superTriviaCheerTriggerMaximum}\"')
        elif superTriviaGameRewardId is not None and not isinstance(superTriviaGameRewardId, str):
            raise TypeError(f'superTriviaGameRewardId argument is malformed: \"{superTriviaGameRewardId}\"')
        elif superTriviaGameShinyMultiplier is not None and not utils.isValidInt(superTriviaGameShinyMultiplier):
            raise TypeError(f'superTriviaGameShinyMultiplier argument is malformed: \"{superTriviaGameShinyMultiplier}\"')
        elif superTriviaGameToxicPunishmentMultiplier is not None and not utils.isValidInt(superTriviaGameToxicPunishmentMultiplier):
            raise TypeError(f'superTriviaGameToxicPunishmentMultiplier argument is malformed: \"{superTriviaGameToxicPunishmentMultiplier}\"')
        elif superTriviaPerUserAttempts is not None and not utils.isValidInt(superTriviaPerUserAttempts):
            raise TypeError(f'superTriviaPeruserAttempts argument is malformed: \"{superTriviaPerUserAttempts}\"')
        elif superTriviaSubscribeTriggerMaximum is not None and not utils.isValidInt(superTriviaSubscribeTriggerMaximum):
            raise TypeError(f'superTriviaSubscribeTriggerMaximum argument is malformed: \"{superTriviaSubscribeTriggerMaximum}\"')
        elif timeoutActionFollowShieldDays is not None and not utils.isValidInt(timeoutActionFollowShieldDays):
            raise TypeError(f'timeoutActionFollowShieldDays argument is malformed: \"{timeoutActionFollowShieldDays}\"')
        elif triviaGamePoints is not None and not utils.isValidInt(triviaGamePoints):
            raise TypeError(f'triviaGamePoints argument is malformed: \"{triviaGamePoints}\"')
        elif triviaGameShinyMultiplier is not None and not utils.isValidInt(triviaGameShinyMultiplier):
            raise TypeError(f'triviaGameShinyMultiplier argument is malformed: \"{triviaGameShinyMultiplier}\"')
        elif waitForSuperTriviaAnswerDelay is not None and not utils.isValidInt(waitForSuperTriviaAnswerDelay):
            raise TypeError(f'waitForSuperTriviaAnswerDelay argument is malformed: \"{waitForSuperTriviaAnswerDelay}\"')
        elif waitForTriviaAnswerDelay is not None and not utils.isValidInt(waitForTriviaAnswerDelay):
            raise TypeError(f'waitForTriviaAnswerDelay argument is malformed: \"{waitForTriviaAnswerDelay}\"')
        elif not isinstance(defaultLanguage, LanguageEntry):
            raise TypeError(f'defaultLanguage argument is malformed: \"{defaultLanguage}\"')
        elif blueSkyUrl is not None and not isinstance(blueSkyUrl, str):
            raise TypeError(f'blueSkyUrl argument is malformed: \"{blueSkyUrl}\"')
        elif casualGamePollRewardId is not None and not isinstance(casualGamePollRewardId, str):
            raise TypeError(f'casualGamePollRewardId argument is malformed: \"{casualGamePollRewardId}\"')
        elif casualGamePollUrl is not None and not isinstance(casualGamePollUrl, str):
            raise TypeError(f'casualGamePollUrl argument is malformed: \"{casualGamePollUrl}\"')
        elif crowdControlButtonPressRewardId is not None and not isinstance(crowdControlButtonPressRewardId, str):
            raise TypeError(f'crowdControlButtonPressRewardId argument is malformed: \"{crowdControlButtonPressRewardId}\"')
        elif crowdControlGameShuffleRewardId is not None and not isinstance(crowdControlGameShuffleRewardId, str):
            raise TypeError(f'crowdControlGameShuffleRewardId argument is malformed: \"{crowdControlGameShuffleRewardId}\"')
        elif discordUrl is not None and not isinstance(discordUrl, str):
            raise TypeError(f'discordUrl argument is malformed: \"{discordUrl}\"')
        elif not utils.isValidStr(handle):
            raise TypeError(f'handle argument is malformed: \"{handle}\"')
        elif locationId is not None and not isinstance(locationId, str):
            raise TypeError(f'locationId argument is malformed: \"{locationId}\"')
        elif mastodonUrl is not None and not isinstance(mastodonUrl, str):
            raise TypeError(f'mastodonUrl argument is malformed: \"{mastodonUrl}\"')
        elif pkmnBattleRewardId is not None and not isinstance(pkmnBattleRewardId, str):
            raise TypeError(f'pkmnBattleRewardId argument is malformed: \"{pkmnBattleRewardId}\"')
        elif pkmnEvolveRewardId and not isinstance(pkmnEvolveRewardId, str):
            raise TypeError(f'pkmnEvolveRewardId argument is malformed: \"{pkmnEvolveRewardId}\"')
        elif pkmnShinyRewardId and not isinstance(pkmnShinyRewardId, str):
            raise TypeError(f'pkmnShinyRewardId argument is malformed: \"{pkmnShinyRewardId}\"')
        elif randomSoundAlertRewardId is not None and not isinstance(randomSoundAlertRewardId, str):
            raise TypeError(f'randomSoundAlertRewardId argument is malformed: \"{randomSoundAlertRewardId}\"')
        elif setChatterPreferredTtsRewardId is not None and not isinstance(setChatterPreferredTtsRewardId, str):
            raise TypeError(f'setChatterPreferredTtsRewardId argument is malformed: \"{setChatterPreferredTtsRewardId}\"')
        elif soundAlertRewardId is not None and not isinstance(soundAlertRewardId, str):
            raise TypeError(f'soundAlertRewardId argument is malformed: \"{soundAlertRewardId}\"')
        elif speedrunProfile is not None and not isinstance(speedrunProfile, str):
            raise TypeError(f'speedrunProfile argument is malformed: \"{speedrunProfile}\"')
        elif supStreamerMessage is not None and not isinstance(supStreamerMessage, str):
            raise TypeError(f'supStreamerMessage argument is malformed: \"{supStreamerMessage}\"')
        elif triviaGameRewardId is not None and not isinstance(triviaGameRewardId, str):
            raise TypeError(f'triviaGameRewardId argument is malformed: \"{triviaGameRewardId}\"')
        elif ttsChatterRewardId is not None and not isinstance(ttsChatterRewardId, str):
            raise TypeError(f'ttsChatterRewardId argument is malformed: \"{ttsChatterRewardId}\"')
        elif voicemailRewardId is not None and not isinstance(voicemailRewardId, str):
            raise TypeError(f'voicemailRewardId argument is malformed: \"{voicemailRewardId}\"')
        elif not isinstance(defaultTtsProvider, TtsProvider):
            raise TypeError(f'defaultTtsProvider argument is malformed: \"{defaultTtsProvider}\"')
        elif whichAnivUser is not None and not isinstance(whichAnivUser, WhichAnivUser):
            raise TypeError(f'whichAnivUser argument is malformed: \"{whichAnivUser}\"')
        elif crowdControlBoosterPacks is not None and not isinstance(crowdControlBoosterPacks, frozendict):
            raise TypeError(f'crowdControlBoosterPacks argument is malformed: \"{crowdControlBoosterPacks}\"')
        elif cutenessBoosterPacks is not None and not isinstance(cutenessBoosterPacks, frozendict):
            raise TypeError(f'cutenessBoosterPacks argument is malformed: \"{cutenessBoosterPacks}\"')
        elif decTalkSongBoosterPacks is not None and not isinstance(decTalkSongBoosterPacks, frozendict):
            raise TypeError(f'decTalkSongBoosterPacks argument is malformed: \"{decTalkSongBoosterPacks}\"')
        elif pkmnCatchBoosterPacks is not None and not isinstance(pkmnCatchBoosterPacks, frozendict):
            raise TypeError(f'pkmnCatchBoosterPacks argument is malformed: \"{pkmnCatchBoosterPacks}\"')
        elif redemptionCounterBoosterPacks is not None and not isinstance(redemptionCounterBoosterPacks, frozendict):
            raise TypeError(f'redemptionCounterBoosterPacks argument is malformed: \"{redemptionCounterBoosterPacks}\"')
        elif soundAlertRedemptions is not None and not isinstance(soundAlertRedemptions, frozendict):
            raise TypeError(f'soundAlertRedemptions argument is malformed: \"{soundAlertRedemptions}\"')
        elif timeoutBoosterPacks is not None and not isinstance(timeoutBoosterPacks, frozendict):
            raise TypeError(f'timeoutBoosterPacks argument is malformed: \"{timeoutBoosterPacks}\"')
        elif chatSoundAlerts is not None and not isinstance(chatSoundAlerts, FrozenList):
            raise TypeError(f'chatSoundAlerts argument is malformed: \"{chatSoundAlerts}\"')
        elif chatBackMessages is not None and not isinstance(chatBackMessages, FrozenList):
            raise TypeError(f'chatBackMessages argument is malformed: \"{chatBackMessages}\"')
        elif supStreamerBoosterPacks is not None and not isinstance(supStreamerBoosterPacks, FrozenList):
            raise TypeError(f'supStreamerBoosterPacks argument is malformed: \"{supStreamerBoosterPacks}\"')
        elif ttsBoosterPacks is not None and not isinstance(ttsBoosterPacks, FrozenList):
            raise TypeError(f'ttsBoosterPacks argument is malformed: \"{ttsBoosterPacks}\"')
        elif timeZones is not None and not isinstance(timeZones, FrozenList):
            raise TypeError(f'timeZones argument is malformed: \"{timeZones}\"')

        self.__areAsplodieStatsEnabled: bool = areAsplodieStatsEnabled
        self.__areBeanStatsEnabled: bool = areBeanStatsEnabled
        self.__areChatSoundAlertsEnabled: bool = areChatSoundAlertsEnabled
        self.__areCheerActionsEnabled: bool = areCheerActionsEnabled
        self.__arePranksEnabled: bool = arePranksEnabled
        self.__areRecurringActionsEnabled: bool = areRecurringActionsEnabled
        self.__areRedemptionCountersEnabled: bool = areRedemptionCountersEnabled
        self.__areSoundAlertsEnabled: bool = areSoundAlertsEnabled
        self.__isAnivContentScanningEnabled: bool = isAnivContentScanningEnabled
        self.__isAnivMessageCopyTimeoutChatReportingEnabled: bool = isAnivMessageCopyTimeoutChatReportingEnabled
        self.__isAnivMessageCopyTimeoutEnabled: bool = isAnivMessageCopyTimeoutEnabled
        self.__isCasualGamePollEnabled: bool = isCasualGamePollEnabled
        self.__isChannelPredictionChartEnabled: bool = isChannelPredictionChartEnabled
        self.__isChatBackMessagesEnabled: bool = isChatBackMessagesEnabled
        self.__isChatBandEnabled: bool = isChatBandEnabled
        self.__isChatLoggingEnabled: bool = isChatLoggingEnabled
        self.__isChatterPreferredTtsEnabled: bool = isChatterPreferredTtsEnabled
        self.__isCrowdControlEnabled: bool = isCrowdControlEnabled
        self.__isCutenessEnabled: bool = isCutenessEnabled
        self.__isDecTalkSongsEnabled: bool = isDecTalkSongsEnabled
        self.__isEccoEnabled: bool = isEccoEnabled
        self.__isEnabled: bool = isEnabled
        self.__isGiveCutenessEnabled: bool = isGiveCutenessEnabled
        self.__isJishoEnabled: bool = isJishoEnabled
        self.__isLoremIpsumEnabled: bool = isLoremIpsumEnabled
        self.__isNotifyOfPollResultsEnabled: bool = isNotifyOfPollResultsEnabled
        self.__isNotifyOfPollStartEnabled: bool = isNotifyOfPollStartEnabled
        self.__isNotifyOfPredictionResultsEnabled: bool = isNotifyOfPredictionResultsEnabled
        self.__isNotifyOfPredictionStartEnabled: bool = isNotifyOfPredictionStartEnabled
        self.__isNotifyOfRaidEnabled: bool = isNotifyOfRaidEnabled
        self.__isPkmnEnabled: bool = isPkmnEnabled
        self.__isPokepediaEnabled: bool = isPokepediaEnabled
        self.__isRaceEnabled: bool = isRaceEnabled
        self.__isShinyTriviaEnabled: bool = isShinyTriviaEnabled
        self.__isStarWarsQuotesEnabled: bool = isStarWarsQuotesEnabled
        self.__isSubGiftThankingEnabled: bool = isSubGiftThankingEnabled
        self.__isSuperTriviaGameEnabled: bool = isSuperTriviaGameEnabled
        self.__isSuperTriviaLotrTimeoutEnabled: bool = isSuperTriviaLotrTimeoutEnabled
        self.__isSupStreamerEnabled: bool = isSupStreamerEnabled
        self.__isTimeoutCheerActionIncreasedBullyFailureEnabled: bool = isTimeoutCheerActionIncreasedBullyFailureEnabled
        self.__isTimeoutCheerActionFailureEnabled: bool = isTimeoutCheerActionFailureEnabled
        self.__isTimeoutCheerActionReverseEnabled: bool = isTimeoutCheerActionReverseEnabled
        self.__isToxicTriviaEnabled: bool = isToxicTriviaEnabled
        self.__isTranslateEnabled: bool = isTranslateEnabled
        self.__isTriviaGameEnabled: bool = isTriviaGameEnabled
        self.__isTriviaScoreEnabled: bool = isTriviaScoreEnabled
        self.__areTtsChattersEnabled: bool = areTtsChattersEnabled
        self.__isTtsEnabled: bool = isTtsEnabled
        self.__isTtsMonsterApiUsageReportingEnabled: bool = isTtsMonsterApiUsageReportingEnabled
        self.__isVoicemailEnabled: bool = isVoicemailEnabled
        self.__isVulnerableChattersEnabled: bool = isVulnerableChattersEnabled
        self.__isWeatherEnabled: bool = isWeatherEnabled
        self.__isWordOfTheDayEnabled: bool = isWordOfTheDayEnabled
        self.__anivMessageCopyTimeoutProbability: float | None = anivMessageCopyTimeoutProbability
        self.__superTriviaSubscribeTriggerAmount: float | None = superTriviaSubscribeTriggerAmount
        self.__anivMessageCopyMaxAgeSeconds: int | None = anivMessageCopyMaxAgeSeconds
        self.__anivMessageCopyTimeoutMinSeconds: int | None = anivMessageCopyTimeoutMinSeconds
        self.__anivMessageCopyTimeoutMaxSeconds: int | None = anivMessageCopyTimeoutMaxSeconds
        self.__maximumGrenadesWithinCooldown: int | None = maximumGrenadesWithinCooldown
        self.__maximumTtsCheerAmount: int | None = maximumTtsCheerAmount
        self.__minimumRaidViewersForNotification: int | None = minimumRaidViewersForNotification
        self.__minimumTtsCheerAmount: int | None = minimumTtsCheerAmount
        self.__superTriviaCheerTriggerAmount: int | None = superTriviaCheerTriggerAmount
        self.__superTriviaCheerTriggerMaximum: int | None = superTriviaCheerTriggerMaximum
        self.__superTriviaGamePoints: int | None = superTriviaGamePoints
        self.__superTriviaGameRewardId: str | None = superTriviaGameRewardId
        self.__superTriviaGameShinyMultiplier: int | None = superTriviaGameShinyMultiplier
        self.__superTriviaGameToxicMultiplier: int | None = superTriviaGameToxicMultiplier
        self.__superTriviaGameToxicPunishmentMultiplier: int | None = superTriviaGameToxicPunishmentMultiplier
        self.__superTriviaPerUserAttempts: int | None = superTriviaPerUserAttempts
        self.__superTriviaSubscribeTriggerMaximum: int | None = superTriviaSubscribeTriggerMaximum
        self.__timeoutActionFollowShieldDays: int | None = timeoutActionFollowShieldDays
        self.__triviaGamePoints: int | None = triviaGamePoints
        self.__triviaGameShinyMultiplier: int | None = triviaGameShinyMultiplier
        self.__waitForTriviaAnswerDelay: int | None = waitForTriviaAnswerDelay
        self.__waitForSuperTriviaAnswerDelay: int | None = waitForSuperTriviaAnswerDelay
        self.__defaultLanguage: LanguageEntry = defaultLanguage
        self.__blueSkyUrl: str | None = blueSkyUrl
        self.__casualGamePollRewardId: str | None = casualGamePollRewardId
        self.__casualGamePollUrl: str | None = casualGamePollUrl
        self.__crowdControlButtonPressRewardId: str | None = crowdControlButtonPressRewardId
        self.__crowdControlGameShuffleRewardId: str | None = crowdControlGameShuffleRewardId
        self.__discordUrl: str | None = discordUrl
        self.__handle: str = handle
        self.__instagram: str | None = instagram
        self.__locationId: str | None = locationId
        self.__mastodonUrl: str | None = mastodonUrl
        self.__pkmnBattleRewardId: str | None = pkmnBattleRewardId
        self.__pkmnEvolveRewardId: str | None = pkmnEvolveRewardId
        self.__pkmnShinyRewardId: str | None = pkmnShinyRewardId
        self.__randomSoundAlertRewardId: str | None = randomSoundAlertRewardId
        self.__setChatterPreferredTtsRewardId: str | None = setChatterPreferredTtsRewardId
        self.__soundAlertRewardId: str | None = soundAlertRewardId
        self.__speedrunProfile: str | None = speedrunProfile
        self.__supStreamerMessage: str | None = supStreamerMessage
        self.__triviaGameRewardId: str | None = triviaGameRewardId
        self.__ttsChatterRewardId: str | None = ttsChatterRewardId
        self.__voicemailRewardId: str | None = voicemailRewardId
        self.__defaultTtsProvider: TtsProvider = defaultTtsProvider
        self.__whichAnivUser: WhichAnivUser | None = whichAnivUser
        self.__crowdControlBoosterPacks: frozendict[str, CrowdControlBoosterPack] | None = crowdControlBoosterPacks
        self.__cutenessBoosterPacks: frozendict[str, CutenessBoosterPack] | None = cutenessBoosterPacks
        self.__decTalkSongBoosterPacks: frozendict[str, DecTalkSongBoosterPack] | None = decTalkSongBoosterPacks
        self.__pkmnCatchBoosterPacks: frozendict[str, PkmnCatchBoosterPack] | None = pkmnCatchBoosterPacks
        self.__redemptionCounterBoosterPacks: frozendict[str, RedemptionCounterBoosterPack] | None = redemptionCounterBoosterPacks
        self.__soundAlertRedemptions: frozendict[str, SoundAlertRedemption] | None = soundAlertRedemptions
        self.__timeoutBoosterPacks: frozendict[str, TimeoutBoosterPack] | None = timeoutBoosterPacks
        self.__chatSoundAlerts: FrozenList[AbsChatSoundAlert] | None = chatSoundAlerts
        self.__chatBackMessages: FrozenList[str] | None = chatBackMessages
        self.__supStreamerBoosterPacks: FrozenList[SupStreamerBoosterPack] | None = supStreamerBoosterPacks
        self.__ttsBoosterPacks: FrozenList[TtsBoosterPack] | None = ttsBoosterPacks
        self.__timeZones: FrozenList[tzinfo] | None = timeZones

    @property
    def anivMessageCopyMaxAgeSeconds(self) -> int | None:
        return self.__anivMessageCopyMaxAgeSeconds

    @property
    def anivMessageCopyTimeoutMinSeconds(self) -> int | None:
        return self.__anivMessageCopyTimeoutMinSeconds

    @property
    def anivMessageCopyTimeoutMaxSeconds(self) -> int | None:
        return self.__anivMessageCopyTimeoutMaxSeconds

    @property
    def anivMessageCopyTimeoutProbability(self) -> float | None:
        return self.__anivMessageCopyTimeoutProbability

    @property
    def areAsplodieStatsEnabled(self) -> bool:
        return self.__areAsplodieStatsEnabled

    @property
    def areBeanStatsEnabled(self) -> bool:
        return self.__areBeanStatsEnabled

    @property
    def areChatSoundAlertsEnabled(self) -> bool:
        return self.__areChatSoundAlertsEnabled

    @property
    def areCheerActionsEnabled(self) -> bool:
        return self.__areCheerActionsEnabled

    @property
    def arePranksEnabled(self) -> bool:
        return self.__arePranksEnabled

    @property
    def areRecurringActionsEnabled(self) -> bool:
        return self.__areRecurringActionsEnabled

    @property
    def areRedemptionCountersEnabled(self) -> bool:
        return self.__areRedemptionCountersEnabled

    @property
    def areSoundAlertsEnabled(self) -> bool:
        return self.__areSoundAlertsEnabled

    @property
    def blueSkyUrl(self) -> str | None:
        return self.__blueSkyUrl

    @property
    def chatSoundAlerts(self) -> FrozenList[AbsChatSoundAlert] | None:
        return self.__chatSoundAlerts

    @property
    def crowdControlBoosterPacks(self) -> frozendict[str, CrowdControlBoosterPack] | None:
        return self.__crowdControlBoosterPacks

    @property
    def crowdControlButtonPressRewardId(self) -> str | None:
        return self.__crowdControlButtonPressRewardId

    @property
    def crowdControlGameShuffleRewardId(self) -> str | None:
        return self.__crowdControlGameShuffleRewardId

    @property
    def cutenessBoosterPacks(self) -> frozendict[str, CutenessBoosterPack] | None:
        return self.__cutenessBoosterPacks

    @property
    def defaultTtsProvider(self) -> TtsProvider:
        return self.__defaultTtsProvider

    @property
    def chatBackMessages(self) -> FrozenList[str] | None:
        return self.__chatBackMessages

    @property
    def casualGamePollRewardId(self) -> str | None:
        return self.__casualGamePollRewardId

    @property
    def casualGamePollUrl(self) -> str | None:
        return self.__casualGamePollUrl

    @property
    def decTalkSongBoosterPacks(self) -> frozendict[str, DecTalkSongBoosterPack] | None:
        return self.__decTalkSongBoosterPacks

    @property
    def defaultLanguage(self) -> LanguageEntry:
        return self.__defaultLanguage

    @property
    def discordUrl(self) -> str | None:
        return self.__discordUrl

    @property
    def handle(self) -> str:
        return self.__handle

    @property
    def instagramUrl(self) -> str | None:
        return self.__instagram

    @property
    def locationId(self) -> str | None:
        return self.__locationId

    @property
    def mastodonUrl(self) -> str | None:
        return self.__mastodonUrl

    @property
    def maximumGrenadesWithinCooldown(self) -> int | None:
        return self.__maximumGrenadesWithinCooldown

    @property
    def maximumTtsCheerAmount(self) -> int | None:
        return self.__maximumTtsCheerAmount

    @property
    def minimumTtsCheerAmount(self) -> int | None:
        return self.__minimumTtsCheerAmount

    @property
    def pkmnEvolveRewardId(self) -> str | None:
        return self.__pkmnEvolveRewardId

    @property
    def pkmnShinyRewardId(self) -> str | None:
        return self.__pkmnShinyRewardId

    @property
    def randomSoundAlertRewardId(self) -> str | None:
        return self.__randomSoundAlertRewardId

    @property
    def soundAlertRewardId(self) -> str | None:
        return self.__soundAlertRewardId

    @property
    def speedrunProfile(self) -> str | None:
        return self.__speedrunProfile

    @property
    def superTriviaCheerTriggerAmount(self) -> int | None:
        return self.__superTriviaCheerTriggerAmount

    @property
    def superTriviaCheerTriggerMaximum(self) -> int | None:
        return self.__superTriviaCheerTriggerMaximum

    @property
    def superTriviaGamePoints(self) -> int | None:
        return self.__superTriviaGamePoints

    @property
    def superTriviaGameRewardId(self) -> str | None:
        return self.__superTriviaGameRewardId

    @property
    def superTriviaGameShinyMultiplier(self) -> int | None:
        return self.__superTriviaGameShinyMultiplier

    @property
    def superTriviaGameToxicMultiplier(self) -> int | None:
        return self.__superTriviaGameToxicMultiplier

    @property
    def superTriviaGameToxicPunishmentMultiplier(self) -> int | None:
        return self.__superTriviaGameToxicPunishmentMultiplier

    @property
    def superTriviaPerUserAttempts(self) -> int | None:
        return self.__superTriviaPerUserAttempts

    @property
    def superTriviaSubscribeTriggerAmount(self) -> float | None:
        return self.__superTriviaSubscribeTriggerAmount

    @property
    def superTriviaSubscribeTriggerMaximum(self) -> int | None:
        return self.__superTriviaSubscribeTriggerMaximum

    @property
    def supStreamerMessage(self) -> str | None:
        return self.__supStreamerMessage

    @property
    def supStreamerBoosterPacks(self) -> FrozenList[SupStreamerBoosterPack] | None:
        return self.__supStreamerBoosterPacks

    @property
    def triviaGamePoints(self) -> int | None:
        return self.__triviaGamePoints

    @property
    def triviaGameRewardId(self) -> str | None:
        return self.__triviaGameRewardId

    @property
    def triviaGameShinyMultiplier(self) -> int | None:
        return self.__triviaGameShinyMultiplier

    @property
    def ttsChatterRewardId(self) -> str | None:
        return self.__ttsChatterRewardId

    @property
    def twitchUrl(self) -> str:
        return f'https://twitch.tv/{self.__handle.lower()}'

    @property
    def waitForSuperTriviaAnswerDelay(self) -> int | None:
        return self.__waitForSuperTriviaAnswerDelay

    @property
    def waitForTriviaAnswerDelay(self) -> int | None:
        return self.__waitForTriviaAnswerDelay

    @property
    def hasInstagram(self) -> bool:
        return utils.isValidUrl(self.__instagram)

    @property
    def hasLocationId(self) -> bool:
        return utils.isValidStr(self.__locationId)

    @property
    def hasMastodonUrl(self) -> bool:
        return utils.isValidUrl(self.__mastodonUrl)

    @property
    def hasSpeedrunProfile(self) -> bool:
        return utils.isValidUrl(self.__speedrunProfile)

    @property
    def hasTimeZones(self) -> bool:
        return self.__timeZones is not None and len(self.__timeZones) >= 1

    @property
    def isAnivContentScanningEnabled(self) -> bool:
        return self.__isAnivContentScanningEnabled

    @property
    def isAnivMessageCopyTimeoutChatReportingEnabled(self) -> bool:
        return self.__isAnivMessageCopyTimeoutChatReportingEnabled

    @property
    def isAnivMessageCopyTimeoutEnabled(self) -> bool:
        return self.__isAnivMessageCopyTimeoutEnabled

    @property
    def isCasualGamePollEnabled(self) -> bool:
        return self.__isCasualGamePollEnabled

    @property
    def isChannelPredictionChartEnabled(self) -> bool:
        return self.__isChannelPredictionChartEnabled

    @property
    def isChatBackMessagesEnabled(self) -> bool:
        return self.__isChatBackMessagesEnabled

    @property
    def isChatBandEnabled(self) -> bool:
        return self.__isChatBandEnabled

    @property
    def isChatLoggingEnabled(self) -> bool:
        return self.__isChatLoggingEnabled

    @property
    def isChatterPreferredTtsEnabled(self) -> bool:
        return self.__isChatterPreferredTtsEnabled

    @property
    def isCrowdControlEnabled(self) -> bool:
        return self.__isCrowdControlEnabled

    @property
    def isCutenessEnabled(self) -> bool:
        return self.__isCutenessEnabled

    @property
    def isDecTalkSongsEnabled(self) -> bool:
        return self.__isDecTalkSongsEnabled

    @property
    def isEccoEnabled(self) -> bool:
        return self.__isEccoEnabled

    @property
    def isEnabled(self) -> bool:
        return self.__isEnabled

    @property
    def isGiveCutenessEnabled(self) -> bool:
        return self.__isGiveCutenessEnabled

    @property
    def isJishoEnabled(self) -> bool:
        return self.__isJishoEnabled

    @property
    def isLoremIpsumEnabled(self) -> bool:
        return self.__isLoremIpsumEnabled

    @property
    def isNotifyOfPollResultsEnabled(self) -> bool:
        return self.__isNotifyOfPollResultsEnabled

    @property
    def isNotifyOfPollStartEnabled(self) -> bool:
        return self.__isNotifyOfPollStartEnabled

    @property
    def isNotifyOfPredictionResultsEnabled(self) -> bool:
        return self.__isNotifyOfPredictionResultsEnabled

    @property
    def isNotifyOfPredictionStartEnabled(self) -> bool:
        return self.__isNotifyOfPredictionStartEnabled

    @property
    def isNotifyOfRaidEnabled(self) -> bool:
        return self.__isNotifyOfRaidEnabled

    @property
    def isPkmnEnabled(self) -> bool:
        return self.__isPkmnEnabled

    @property
    def isPokepediaEnabled(self) -> bool:
        return self.__isPokepediaEnabled

    @property
    def isRaceEnabled(self) -> bool:
        return self.__isRaceEnabled

    @property
    def isShinyTriviaEnabled(self) -> bool:
        return self.__isShinyTriviaEnabled

    @property
    def isStarWarsQuotesEnabled(self) -> bool:
        return self.__isStarWarsQuotesEnabled

    @property
    def isSubGiftThankingEnabled(self) -> bool:
        return self.__isSubGiftThankingEnabled

    @property
    def isSuperTriviaGameEnabled(self) -> bool:
        return self.__isSuperTriviaGameEnabled

    @property
    def isSuperTriviaLotrTimeoutEnabled(self) -> bool:
        return self.__isSuperTriviaLotrTimeoutEnabled

    @property
    def isSupStreamerEnabled(self) -> bool:
        return self.__isSupStreamerEnabled

    @property
    def isTimeoutCheerActionIncreasedBullyFailureEnabled(self) -> bool:
        return self.__isTimeoutCheerActionIncreasedBullyFailureEnabled

    @property
    def isTimeoutCheerActionFailureEnabled(self) -> bool:
        return self.__isTimeoutCheerActionFailureEnabled

    @property
    def isTimeoutCheerActionReverseEnabled(self) -> bool:
        return self.__isTimeoutCheerActionReverseEnabled

    @property
    def isToxicTriviaEnabled(self) -> bool:
        return self.__isToxicTriviaEnabled

    @property
    def isTranslateEnabled(self) -> bool:
        return self.__isTranslateEnabled

    @property
    def isTriviaGameEnabled(self) -> bool:
        return self.__isTriviaGameEnabled

    @property
    def isTriviaScoreEnabled(self) -> bool:
        return self.__isTriviaScoreEnabled

    @property
    def isTtsEnabled(self) -> bool:
        return self.__isTtsEnabled

    @property
    def isVoicemailEnabled(self) -> bool:
        return self.__isVoicemailEnabled

    @property
    def isVulnerableChattersEnabled(self) -> bool:
        return self.__isVulnerableChattersEnabled

    @property
    def areTtsChattersEnabled(self) -> bool:
        return self.__areTtsChattersEnabled

    @property
    def isTtsMonsterApiUsageReportingEnabled(self) -> bool:
        return self.__isTtsMonsterApiUsageReportingEnabled

    @property
    def isWeatherEnabled(self) -> bool:
        return self.__isWeatherEnabled

    @property
    def isWordOfTheDayEnabled(self) -> bool:
        return self.__isWordOfTheDayEnabled

    @property
    def minimumRaidViewersForNotification(self) -> int | None:
        return self.__minimumRaidViewersForNotification

    @property
    def pkmnBattleRewardId(self) -> str | None:
        return self.__pkmnBattleRewardId

    @property
    def pkmnCatchBoosterPacks(self) -> frozendict[str, PkmnCatchBoosterPack] | None:
        return self.__pkmnCatchBoosterPacks

    def __repr__(self) -> str:
        return self.__handle

    @property
    def redemptionCounterBoosterPacks(self) -> frozendict[str, RedemptionCounterBoosterPack] | None:
        return self.__redemptionCounterBoosterPacks

    @property
    def setChatterPreferredTtsRewardId(self) -> str | None:
        return self.__setChatterPreferredTtsRewardId

    @property
    def soundAlertRedemptions(self) -> frozendict[str, SoundAlertRedemption] | None:
        return self.__soundAlertRedemptions

    @property
    def timeoutActionFollowShieldDays(self) -> int | None:
        return self.__timeoutActionFollowShieldDays

    @property
    def timeoutBoosterPacks(self) -> frozendict[str, TimeoutBoosterPack] | None:
        return self.__timeoutBoosterPacks

    @property
    def timeZones(self) -> FrozenList[tzinfo] | None:
        return self.__timeZones

    @property
    def ttsBoosterPacks(self) -> FrozenList[TtsBoosterPack] | None:
        return self.__ttsBoosterPacks

    @property
    def voicemailRewardId(self) -> str | None:
        return self.__voicemailRewardId

    @property
    def whichAnivUser(self) -> WhichAnivUser | None:
        return self.__whichAnivUser
