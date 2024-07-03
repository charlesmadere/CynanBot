from datetime import tzinfo

from .pkmnCatchBoosterPack import PkmnCatchBoosterPack
from .soundAlertRedemption import SoundAlertRedemption
from .userInterface import UserInterface
from ..cuteness.cutenessBoosterPack import CutenessBoosterPack
from ..misc import utils as utils


class User(UserInterface):

    def __init__(
        self,
        areCheerActionsEnabled: bool,
        areRecurringActionsEnabled: bool,
        areSoundAlertsEnabled: bool,
        isAnivContentScanningEnabled: bool,
        isAnivMessageCopyTimeoutEnabled: bool,
        isCatJamMessageEnabled: bool,
        isCasualGamePollEnabled: bool,
        isChannelPredictionChartEnabled: bool,
        isChatBandEnabled: bool,
        isChatLoggingEnabled: bool,
        isCutenessEnabled: bool,
        isCynanSourceEnabled: bool,
        isDeerForceMessageEnabled: bool,
        isEnabled: bool,
        isEyesMessageEnabled: bool,
        isGiveCutenessEnabled: bool,
        isImytSlurpMessageEnabled: bool,
        isJamCatMessageEnabled: bool,
        isJishoEnabled: bool,
        isLoremIpsumEnabled: bool,
        isPkmnEnabled: bool,
        isPokepediaEnabled: bool,
        isRaceEnabled: bool,
        isRaidLinkMessagingEnabled: bool,
        isRatJamMessageEnabled: bool,
        isRewardIdPrintingEnabled: bool,
        isRoachMessageEnabled: bool,
        isSchubertWalkMessageEnabled: bool,
        isShinyTriviaEnabled: bool,
        isStarWarsQuotesEnabled: bool,
        isSubGiftThankingEnabled: bool,
        isSuperTriviaGameEnabled: bool,
        isSupStreamerEnabled: bool,
        isToxicTriviaEnabled: bool,
        isTranslateEnabled: bool,
        isTriviaGameEnabled: bool,
        isTriviaScoreEnabled: bool,
        isTtsEnabled: bool,
        isWeatherEnabled: bool,
        isWelcomeTtsEnabled: bool,
        isWordOfTheDayEnabled: bool,
        anivMessageCopyTimeoutProbability: float | None,
        superTriviaCheerTriggerAmount: float | None,
        superTriviaSubscribeTriggerAmount: float | None,
        anivMessageCopyMaxAgeSeconds: int | None,
        anivMessageCopyTimeoutSeconds: int | None,
        maximumTtsCheerAmount: int | None,
        minimumTtsCheerAmount: int | None,
        superTriviaCheerTriggerMaximum: int | None,
        superTriviaGamePoints: int | None,
        superTriviaGameRewardId: str | None,
        superTriviaGameShinyMultiplier: int | None,
        superTriviaGameToxicMultiplier: int | None,
        superTriviaGameToxicPunishmentMultiplier: int | None,
        superTriviaPerUserAttempts: int | None,
        superTriviaSubscribeTriggerMaximum: int | None,
        timeoutCheerActionFollowShieldDays: int | None,
        triviaGamePoints: int | None,
        triviaGameShinyMultiplier: int | None,
        waitForSuperTriviaAnswerDelay: int | None,
        waitForTriviaAnswerDelay: int | None,
        casualGamePollRewardId: str | None,
        casualGamePollUrl: str | None,
        discord: str | None,
        handle: str,
        instagram: str | None,
        locationId: str | None,
        mastodonUrl: str | None,
        pkmnBattleRewardId: str | None,
        pkmnEvolveRewardId: str | None,
        pkmnShinyRewardId: str | None,
        randomSoundAlertRewardId: str | None,
        soundAlertRewardId: str | None,
        speedrunProfile: str | None,
        supStreamerMessage: str | None,
        triviaGameRewardId: str | None,
        twitterUrl: str,
        soundAlertRedemptions: dict[str, SoundAlertRedemption] | None,
        cutenessBoosterPacks: list[CutenessBoosterPack] | None,
        pkmnCatchBoosterPacks: list[PkmnCatchBoosterPack] | None,
        timeZones: list[tzinfo] | None
    ):
        if not utils.isValidBool(areCheerActionsEnabled):
            raise TypeError(f'areCheerActionsEnabled argument is malformed: \"{areCheerActionsEnabled}\"')
        elif not utils.isValidBool(areRecurringActionsEnabled):
            raise TypeError(f'areRecurringActionsEnabled argument is malformed: \"{areRecurringActionsEnabled}\"')
        elif not utils.isValidBool(areSoundAlertsEnabled):
            raise TypeError(f'areSoundAlertsEnabled argument is malformed: \"{areSoundAlertsEnabled}\"')
        elif not utils.isValidBool(isAnivContentScanningEnabled):
            raise TypeError(f'isAnivContentScanningEnabled argument is malformed: \"{isAnivContentScanningEnabled}\"')
        elif not utils.isValidBool(isAnivMessageCopyTimeoutEnabled):
            raise TypeError(f'isAnivMessageCopyTimeoutEnabled argument is malformed: \"{isAnivMessageCopyTimeoutEnabled}\"')
        elif not utils.isValidBool(isCasualGamePollEnabled):
            raise TypeError(f'isCasualGamePollEnabled argument is malformed: \"{isCasualGamePollEnabled}\"')
        elif not utils.isValidBool(isCatJamMessageEnabled):
            raise TypeError(f'isCatJamMessageEnabled argument is malformed: \"{isCatJamMessageEnabled}\"')
        elif not utils.isValidBool(isChannelPredictionChartEnabled):
            raise TypeError(f'isChannelPredictionChartEnabled argument is malformed: \"{isChannelPredictionChartEnabled}\"')
        elif not utils.isValidBool(isChatBandEnabled):
            raise TypeError(f'isChatBandEnabled argument is malformed: \"{isChatBandEnabled}\"')
        elif not utils.isValidBool(isChatLoggingEnabled):
            raise TypeError(f'isChatLoggingEnabled argument is malformed: \"{isChatLoggingEnabled}\"')
        elif not utils.isValidBool(isCutenessEnabled):
            raise TypeError(f'isCutenessEnabled argument is malformed: \"{isCutenessEnabled}\"')
        elif not utils.isValidBool(isCynanSourceEnabled):
            raise TypeError(f'isCynanSourceEnabled argument is malformed: \"{isCynanSourceEnabled}\"')
        elif not utils.isValidBool(isDeerForceMessageEnabled):
            raise TypeError(f'isDeerForceMessageEnabled argument is malformed: \"{isDeerForceMessageEnabled}\"')
        elif not utils.isValidBool(isEnabled):
            raise TypeError(f'isEnabled argument is malformed: \"{isEnabled}\"')
        elif not utils.isValidBool(isEyesMessageEnabled):
            raise TypeError(f'isEyesMessageEnabled argument is malformed: \"{isEyesMessageEnabled}\"')
        elif not utils.isValidBool(isGiveCutenessEnabled):
            raise TypeError(f'isGiveCutenessEnabled argument is malformed: \"{isGiveCutenessEnabled}\"')
        elif not utils.isValidBool(isImytSlurpMessageEnabled):
            raise TypeError(f'isImytSlurpMessageEnabled argument is malformed: \"{isImytSlurpMessageEnabled}\"')
        elif not utils.isValidBool(isJamCatMessageEnabled):
            raise TypeError(f'isJamCatMessageEnabled argument is malformed: \"{isJamCatMessageEnabled}\"')
        elif not utils.isValidBool(isJishoEnabled):
            raise TypeError(f'isJishoEnabled argument is malformed: \"{isJishoEnabled}\"')
        elif not utils.isValidBool(isLoremIpsumEnabled):
            raise TypeError(f'isLoremIpsumEnabled argument is malformed: \"{isLoremIpsumEnabled}\"')
        elif not utils.isValidBool(isPkmnEnabled):
            raise TypeError(f'isPkmnEnabled argument is malformed: \"{isPkmnEnabled}\"')
        elif not utils.isValidBool(isPokepediaEnabled):
            raise TypeError(f'isPokepediaEnabled argument is malformed: \"{isPokepediaEnabled}\"')
        elif not utils.isValidBool(isRaceEnabled):
            raise TypeError(f'isRaceEnabled argument is malformed: \"{isRaceEnabled}\"')
        elif not utils.isValidBool(isRaidLinkMessagingEnabled):
            raise TypeError(f'isRaidLinkMessagingEnabled argument is malformed: \"{isRaidLinkMessagingEnabled}\"')
        elif not utils.isValidBool(isRatJamMessageEnabled):
            raise TypeError(f'isRatJamMessageEnabled argument is malformed: \"{isRatJamMessageEnabled}\"')
        elif not utils.isValidBool(isRewardIdPrintingEnabled):
            raise TypeError(f'isRewardIdPrintingEnabled argument is malformed: \"{isRewardIdPrintingEnabled}\"')
        elif not utils.isValidBool(isRoachMessageEnabled):
            raise TypeError(f'isRoachMessageEnabled argument is malformed: \"{isRoachMessageEnabled}\"')
        elif not utils.isValidBool(isSchubertWalkMessageEnabled):
            raise TypeError(f'isSchubertWalkMessageEnabled argument is malformed: \"{isSchubertWalkMessageEnabled}\"')
        elif not utils.isValidBool(isShinyTriviaEnabled):
            raise TypeError(f'isShinyTriviaEnabled argument is malformed: \"{isShinyTriviaEnabled}\"')
        elif not utils.isValidBool(isStarWarsQuotesEnabled):
            raise TypeError(f'isStarWarsQuotesEnabled argument is malformed: \"{isStarWarsQuotesEnabled}\"')
        elif not utils.isValidBool(isSubGiftThankingEnabled):
            raise TypeError(f'isSubGiftThankingEnabled argument is malformed: \"{isSubGiftThankingEnabled}\"')
        elif not utils.isValidBool(isSuperTriviaGameEnabled):
            raise TypeError(f'isSuperTriviaGameEnabled argument is malformed: \"{isSuperTriviaGameEnabled}\"')
        elif not utils.isValidBool(isSupStreamerEnabled):
            raise TypeError(f'isSupStreamerEnabled argument is malformed: \"{isSupStreamerEnabled}\"')
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
        elif not utils.isValidBool(isWeatherEnabled):
            raise TypeError(f'isWeatherEnabled argument is malformed: \"{isWeatherEnabled}\"')
        elif not utils.isValidBool(isWelcomeTtsEnabled):
            raise TypeError(f'isWelcomeTtsEnabled argument is malformed: \"{isWelcomeTtsEnabled}\"')
        elif not utils.isValidBool(isWordOfTheDayEnabled):
            raise TypeError(f'isWordOfTheDayEnabled argument is malformed: \"{isWordOfTheDayEnabled}\"')
        elif anivMessageCopyTimeoutProbability is not None and not utils.isValidNum(anivMessageCopyTimeoutProbability):
            raise TypeError(f'anivMessageCopyTimeoutProbability argument is malformed: \"{anivMessageCopyTimeoutProbability}\"')
        elif superTriviaCheerTriggerAmount is not None and not utils.isValidNum(superTriviaCheerTriggerAmount):
            raise TypeError(f'superTriviaCheerTriggerAmount argument is malformed: \"{superTriviaCheerTriggerAmount}\"')
        elif superTriviaSubscribeTriggerAmount is not None and not utils.isValidNum(superTriviaSubscribeTriggerAmount):
            raise TypeError(f'superTriviaSubscribeTriggerAmount argument is malformed: \"{superTriviaSubscribeTriggerAmount}\"')
        elif anivMessageCopyMaxAgeSeconds is not None and not utils.isValidInt(anivMessageCopyMaxAgeSeconds):
            raise TypeError(f'anivMessageCopyMaxAgeSeconds argument is malformed: \"{anivMessageCopyMaxAgeSeconds}\"')
        elif anivMessageCopyTimeoutSeconds is not None and not utils.isValidInt(anivMessageCopyTimeoutSeconds):
            raise TypeError(f'anivMessageCopyTimeoutSeconds argument is malformed: \"{anivMessageCopyTimeoutSeconds}\"')
        elif maximumTtsCheerAmount is not None and not utils.isValidInt(maximumTtsCheerAmount):
            raise TypeError(f'maximumTtsCheerAmount argument is malformed: \"{maximumTtsCheerAmount}\"')
        elif minimumTtsCheerAmount is not None and not utils.isValidInt(minimumTtsCheerAmount):
            raise TypeError(f'minimumTtsCheerAmount argument is malformed: \"{minimumTtsCheerAmount}\"')
        elif superTriviaGamePoints is not None and not utils.isValidInt(superTriviaGamePoints):
            raise TypeError(f'superTriviaGamePoints argument is malformed: \"{superTriviaGamePoints}\"')
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
        elif timeoutCheerActionFollowShieldDays is not None and not utils.isValidInt(timeoutCheerActionFollowShieldDays):
            raise TypeError(f'timeoutCheerActionFollowShieldDays argument is malformed: \"{timeoutCheerActionFollowShieldDays}\"')
        elif triviaGamePoints is not None and not utils.isValidInt(triviaGamePoints):
            raise TypeError(f'triviaGamePoints argument is malformed: \"{triviaGamePoints}\"')
        elif triviaGameShinyMultiplier is not None and not utils.isValidInt(triviaGameShinyMultiplier):
            raise TypeError(f'triviaGameShinyMultiplier argument is malformed: \"{triviaGameShinyMultiplier}\"')
        elif waitForSuperTriviaAnswerDelay is not None and not utils.isValidInt(waitForSuperTriviaAnswerDelay):
            raise TypeError(f'waitForSuperTriviaAnswerDelay argument is malformed: \"{waitForSuperTriviaAnswerDelay}\"')
        elif waitForTriviaAnswerDelay is not None and not utils.isValidInt(waitForTriviaAnswerDelay):
            raise TypeError(f'waitForTriviaAnswerDelay argument is malformed: \"{waitForTriviaAnswerDelay}\"')
        elif casualGamePollRewardId is not None and not isinstance(casualGamePollRewardId, str):
            raise TypeError(f'casualGamePollRewardId argument is malformed: \"{casualGamePollRewardId}\"')
        elif casualGamePollUrl is not None and not isinstance(casualGamePollUrl, str):
            raise TypeError(f'casualGamePollUrl argument is malformed: \"{casualGamePollUrl}\"')
        elif discord is not None and not isinstance(discord, str):
            raise TypeError(f'discord argument is malformed: \"{discord}\"')
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
        elif soundAlertRewardId is not None and not isinstance(soundAlertRewardId, str):
            raise TypeError(f'soundAlertRewardId argument is malformed: \"{soundAlertRewardId}\"')
        elif speedrunProfile is not None and not isinstance(speedrunProfile, str):
            raise TypeError(f'speedrunProfile argument is malformed: \"{speedrunProfile}\"')
        elif supStreamerMessage is not None and not isinstance(supStreamerMessage, str):
            raise TypeError(f'supStreamerMessage argument is malformed: \"{supStreamerMessage}\"')
        elif triviaGameRewardId is not None and not isinstance(triviaGameRewardId, str):
            raise TypeError(f'triviaGameRewardId argument is malformed: \"{triviaGameRewardId}\"')
        elif twitterUrl is not None and not isinstance(twitterUrl, str):
            raise TypeError(f'twitterUrl argument is malformed: \"{twitterUrl}\"')
        elif soundAlertRedemptions is not None and not isinstance(soundAlertRedemptions, dict):
            raise TypeError(f'soundAlertRedemptions argument is malformed: \"{soundAlertRedemptions}\"')
        elif cutenessBoosterPacks is not None and not isinstance(cutenessBoosterPacks, list):
            raise TypeError(f'cutenessBoosterPacks argument is malformed: \"{cutenessBoosterPacks}\"')
        elif pkmnCatchBoosterPacks is not None and not isinstance(pkmnCatchBoosterPacks, list):
            raise TypeError(f'pkmnCatchBoosterPacks argument is malformed: \"{pkmnCatchBoosterPacks}\"')
        elif timeZones is not None and not isinstance(timeZones, list):
            raise TypeError(f'timeZones argument is malformed: \"{timeZones}\"')

        self.__areCheerActionsEnabled: bool = areCheerActionsEnabled
        self.__areRecurringActionsEnabled: bool = areRecurringActionsEnabled
        self.__areSoundAlertsEnabled: bool = areSoundAlertsEnabled
        self.__isAnivContentScanningEnabled: bool = isAnivContentScanningEnabled
        self.__isAnivMessageCopyTimeoutEnabled: bool = isAnivMessageCopyTimeoutEnabled
        self.__isCasualGamePollEnabled: bool = isCasualGamePollEnabled
        self.__isCatJamMessageEnabled: bool = isCatJamMessageEnabled
        self.__isChannelPredictionChartEnabled: bool = isChannelPredictionChartEnabled
        self.__isChatBandEnabled: bool = isChatBandEnabled
        self.__isChatLoggingEnabled: bool = isChatLoggingEnabled
        self.__isCutenessEnabled: bool = isCutenessEnabled
        self.__isCynanSourceEnabled: bool = isCynanSourceEnabled
        self.__isDeerForceMessageEnabled: bool = isDeerForceMessageEnabled
        self.__isEnabled: bool = isEnabled
        self.__isEyesMessageEnabled: bool = isEyesMessageEnabled
        self.__isGiveCutenessEnabled: bool = isGiveCutenessEnabled
        self.__isImytSlurpMessageEnabled: bool = isImytSlurpMessageEnabled
        self.__isJamCatMessageEnabled: bool = isJamCatMessageEnabled
        self.__isJishoEnabled: bool = isJishoEnabled
        self.__isLoremIpsumEnabled: bool = isLoremIpsumEnabled
        self.__isPkmnEnabled: bool = isPkmnEnabled
        self.__isPokepediaEnabled: bool = isPokepediaEnabled
        self.__isRaceEnabled: bool = isRaceEnabled
        self.__isRaidLinkMessagingEnabled: bool = isRaidLinkMessagingEnabled
        self.__isRatJamMessageEnabled: bool = isRatJamMessageEnabled
        self.__isRewardIdPrintingEnabled: bool = isRewardIdPrintingEnabled
        self.__isRoachMessageEnabled: bool = isRoachMessageEnabled
        self.__isSchubertWalkMessageEnabled: bool = isSchubertWalkMessageEnabled
        self.__isShinyTriviaEnabled: bool = isShinyTriviaEnabled
        self.__isStarWarsQuotesEnabled: bool = isStarWarsQuotesEnabled
        self.__isSubGiftThankingEnabled: bool = isSubGiftThankingEnabled
        self.__isSuperTriviaGameEnabled: bool = isSuperTriviaGameEnabled
        self.__isSupStreamerEnabled: bool = isSupStreamerEnabled
        self.__isToxicTriviaEnabled: bool = isToxicTriviaEnabled
        self.__isTranslateEnabled: bool = isTranslateEnabled
        self.__isTriviaGameEnabled: bool = isTriviaGameEnabled
        self.__isTriviaScoreEnabled: bool = isTriviaScoreEnabled
        self.__isTtsEnabled: bool = isTtsEnabled
        self.__isWeatherEnabled: bool = isWeatherEnabled
        self.__isWelcomeTtsEnabled: bool = isWelcomeTtsEnabled
        self.__isWordOfTheDayEnabled: bool = isWordOfTheDayEnabled
        self.__anivMessageCopyTimeoutProbability: float | None = anivMessageCopyTimeoutProbability
        self.__superTriviaCheerTriggerAmount: float | None = superTriviaCheerTriggerAmount
        self.__superTriviaSubscribeTriggerAmount: float | None = superTriviaSubscribeTriggerAmount
        self.__anivMessageCopyMaxAgeSeconds: int | None = anivMessageCopyMaxAgeSeconds
        self.__anivMessageCopyTimeoutSeconds: int | None = anivMessageCopyTimeoutSeconds
        self.__maximumTtsCheerAmount: int | None = maximumTtsCheerAmount
        self.__minimumTtsCheerAmount: int | None = minimumTtsCheerAmount
        self.__superTriviaCheerTriggerMaximum: int | None = superTriviaCheerTriggerMaximum
        self.__superTriviaGamePoints: int | None = superTriviaGamePoints
        self.__superTriviaGameRewardId: str | None = superTriviaGameRewardId
        self.__superTriviaGameShinyMultiplier: int | None = superTriviaGameShinyMultiplier
        self.__superTriviaGameToxicMultiplier: int | None = superTriviaGameToxicMultiplier
        self.__superTriviaGameToxicPunishmentMultiplier: int | None = superTriviaGameToxicPunishmentMultiplier
        self.__superTriviaPerUserAttempts: int | None = superTriviaPerUserAttempts
        self.__superTriviaSubscribeTriggerMaximum: int | None = superTriviaSubscribeTriggerMaximum
        self.__timeoutCheerActionFollowShieldDays: int | None = timeoutCheerActionFollowShieldDays
        self.__triviaGamePoints: int | None = triviaGamePoints
        self.__triviaGameShinyMultiplier: int | None = triviaGameShinyMultiplier
        self.__waitForTriviaAnswerDelay: int | None = waitForTriviaAnswerDelay
        self.__waitForSuperTriviaAnswerDelay: int | None = waitForSuperTriviaAnswerDelay
        self.__casualGamePollRewardId: str | None = casualGamePollRewardId
        self.__casualGamePollUrl: str | None = casualGamePollUrl
        self.__discord: str | None = discord
        self.__handle: str = handle
        self.__instagram: str | None = instagram
        self.__locationId: str | None = locationId
        self.__mastodonUrl: str | None = mastodonUrl
        self.__pkmnBattleRewardId: str | None = pkmnBattleRewardId
        self.__pkmnEvolveRewardId: str | None = pkmnEvolveRewardId
        self.__pkmnShinyRewardId: str | None = pkmnShinyRewardId
        self.__randomSoundAlertRewardId: str | None = randomSoundAlertRewardId
        self.__soundAlertRewardId: str | None = soundAlertRewardId
        self.__speedrunProfile: str | None = speedrunProfile
        self.__supStreamerMessage: str | None = supStreamerMessage
        self.__triviaGameRewardId: str | None = triviaGameRewardId
        self.__twitterUrl: str | None = twitterUrl
        self.__soundAlertRedemptions: dict[str, SoundAlertRedemption] | None = soundAlertRedemptions
        self.__cutenessBoosterPacks: list[CutenessBoosterPack] | None = cutenessBoosterPacks
        self.__pkmnCatchBoosterPacks: list[PkmnCatchBoosterPack] | None = pkmnCatchBoosterPacks
        self.__timeZones: list[tzinfo] | None = timeZones

    @property
    def anivMessageCopyMaxAgeSeconds(self) -> int | None:
        return self.__anivMessageCopyMaxAgeSeconds

    @property
    def anivMessageCopyTimeoutProbability(self) -> float | None:
        return self.__anivMessageCopyTimeoutProbability

    def areCheerActionsEnabled(self) -> bool:
        return self.__areCheerActionsEnabled

    def areRecurringActionsEnabled(self) -> bool:
        return self.__areRecurringActionsEnabled

    def areSoundAlertsEnabled(self) -> bool:
        return self.__areSoundAlertsEnabled

    def getAnivMessageCopyTimeoutSeconds(self) -> int | None:
        return self.__anivMessageCopyTimeoutSeconds

    def getCasualGamePollRewardId(self) -> str | None:
        return self.__casualGamePollRewardId

    def getCasualGamePollUrl(self) -> str | None:
        return self.__casualGamePollUrl

    def getCutenessBoosterPacks(self) -> list[CutenessBoosterPack] | None:
        return self.__cutenessBoosterPacks

    def getDiscordUrl(self) -> str | None:
        return self.__discord

    def getHandle(self) -> str:
        return self.__handle

    def getInstagramUrl(self) -> str | None:
        return self.__instagram

    def getLocationId(self) -> str | None:
        return self.__locationId

    def getMastodonUrl(self) -> str | None:
        return self.__mastodonUrl

    def getMaximumTtsCheerAmount(self) -> int | None:
        return self.__maximumTtsCheerAmount

    def getMinimumTtsCheerAmount(self) -> int | None:
        return self.__minimumTtsCheerAmount

    def getPkmnBattleRewardId(self) -> str | None:
        return self.__pkmnBattleRewardId

    def getPkmnCatchBoosterPacks(self) -> list[PkmnCatchBoosterPack] | None:
        return self.__pkmnCatchBoosterPacks

    def getPkmnEvolveRewardId(self) -> str | None:
        return self.__pkmnEvolveRewardId

    def getPkmnShinyRewardId(self) -> str | None:
        return self.__pkmnShinyRewardId

    def getRandomSoundAlertRewardId(self) -> str | None:
        return self.__randomSoundAlertRewardId

    def getSoundAlertRedemptions(self) -> dict[str, SoundAlertRedemption] | None:
        return self.__soundAlertRedemptions

    def getSoundAlertRewardId(self) -> str | None:
        return self.__soundAlertRewardId

    def getSpeedrunProfile(self) -> str | None:
        return self.__speedrunProfile

    def getSuperTriviaCheerTriggerAmount(self) -> float | None:
        return self.__superTriviaCheerTriggerAmount

    def getSuperTriviaCheerTriggerMaximum(self) -> int | None:
        return self.__superTriviaCheerTriggerMaximum

    def getSuperTriviaGamePoints(self) -> int | None:
        return self.__superTriviaGamePoints

    def getSuperTriviaGameRewardId(self) -> str | None:
        return self.__superTriviaGameRewardId

    def getSuperTriviaGameShinyMultiplier(self) -> int | None:
        return self.__superTriviaGameShinyMultiplier

    def getSuperTriviaGameToxicMultiplier(self) -> int | None:
        return self.__superTriviaGameToxicMultiplier

    def getSuperTriviaGameToxicPunishmentMultiplier(self) -> int | None:
        return self.__superTriviaGameToxicPunishmentMultiplier

    def getSuperTriviaPerUserAttempts(self) -> int | None:
        return self.__superTriviaPerUserAttempts

    def getSuperTriviaSubscribeTriggerAmount(self) -> float | None:
        return self.__superTriviaSubscribeTriggerAmount

    def getSuperTriviaSubscribeTriggerMaximum(self) -> int | None:
        return self.__superTriviaSubscribeTriggerMaximum

    def getSupStreamerMessage(self) -> str | None:
        return self.__supStreamerMessage

    def getTimeZones(self) -> list[tzinfo] | None:
        return self.__timeZones

    def getTriviaGamePoints(self) -> int | None:
        return self.__triviaGamePoints

    def getTriviaGameRewardId(self) -> str | None:
        return self.__triviaGameRewardId

    def getTriviaGameShinyMultiplier(self) -> int | None:
        return self.__triviaGameShinyMultiplier

    def getTwitchUrl(self) -> str:
        return f'https://twitch.tv/{self.__handle.lower()}'

    def getTwitterUrl(self) -> str | None:
        return self.__twitterUrl

    def getWaitForSuperTriviaAnswerDelay(self) -> int | None:
        return self.__waitForSuperTriviaAnswerDelay

    def getWaitForTriviaAnswerDelay(self) -> int | None:
        return self.__waitForTriviaAnswerDelay

    def hasCutenessBoosterPacks(self) -> bool:
        return utils.hasItems(self.__cutenessBoosterPacks)

    def hasDiscord(self) -> bool:
        return utils.isValidUrl(self.__discord)

    def hasInstagram(self) -> bool:
        return utils.isValidUrl(self.__instagram)

    def hasLocationId(self) -> bool:
        return utils.isValidStr(self.__locationId)

    def hasMastodonUrl(self) -> bool:
        return utils.isValidUrl(self.__mastodonUrl)

    def hasPkmnCatchBoosterPacks(self) -> bool:
        return utils.hasItems(self.__pkmnCatchBoosterPacks)

    def hasSpeedrunProfile(self) -> bool:
        return utils.isValidUrl(self.__speedrunProfile)

    def hasTimeZones(self) -> bool:
        return utils.hasItems(self.__timeZones)

    def hasTwitter(self) -> bool:
        return utils.isValidUrl(self.__twitterUrl)

    def isAnivContentScanningEnabled(self) -> bool:
        return self.__isAnivContentScanningEnabled

    def isAnivMessageCopyTimeoutEnabled(self) -> bool:
        return self.__isAnivMessageCopyTimeoutEnabled

    def isCasualGamePollEnabled(self) -> bool:
        return self.__isCasualGamePollEnabled

    def isCatJamMessageEnabled(self) -> bool:
        return self.__isCatJamMessageEnabled

    def isChannelPredictionChartEnabled(self) -> bool:
        return self.__isChannelPredictionChartEnabled

    def isChatBandEnabled(self) -> bool:
        return self.__isChatBandEnabled

    def isChatLoggingEnabled(self) -> bool:
        return self.__isChatLoggingEnabled

    def isCutenessEnabled(self) -> bool:
        return self.__isCutenessEnabled

    def isCynanSourceEnabled(self) -> bool:
        return self.__isCynanSourceEnabled

    def isDeerForceMessageEnabled(self) -> bool:
        return self.__isDeerForceMessageEnabled

    def isEnabled(self) -> bool:
        return self.__isEnabled

    def isEyesMessageEnabled(self) -> bool:
        return self.__isEyesMessageEnabled

    def isGiveCutenessEnabled(self) -> bool:
        return self.__isGiveCutenessEnabled

    def isImytSlurpMessageEnabled(self) -> bool:
        return self.__isImytSlurpMessageEnabled

    def isJamCatMessageEnabled(self) -> bool:
        return self.__isJamCatMessageEnabled

    def isJishoEnabled(self) -> bool:
        return self.__isJishoEnabled

    def isLoremIpsumEnabled(self) -> bool:
        return self.__isLoremIpsumEnabled

    def isPkmnEnabled(self) -> bool:
        return self.__isPkmnEnabled

    def isPokepediaEnabled(self) -> bool:
        return self.__isPokepediaEnabled

    def isRaceEnabled(self) -> bool:
        return self.__isRaceEnabled

    def isRaidLinkMessagingEnabled(self) -> bool:
        return self.__isRaidLinkMessagingEnabled

    def isRatJamMessageEnabled(self) -> bool:
        return self.__isRatJamMessageEnabled

    def isRewardIdPrintingEnabled(self) -> bool:
        return self.__isRewardIdPrintingEnabled

    def isRoachMessageEnabled(self) -> bool:
        return self.__isRoachMessageEnabled

    def isSchubertWalkMessageEnabled(self) -> bool:
        return self.__isSchubertWalkMessageEnabled

    def isShinyTriviaEnabled(self) -> bool:
        return self.__isShinyTriviaEnabled

    def isStarWarsQuotesEnabled(self) -> bool:
        return self.__isStarWarsQuotesEnabled

    @property
    def isSubGiftThankingEnabled(self) -> bool:
        return self.__isSubGiftThankingEnabled

    def isSuperTriviaGameEnabled(self) -> bool:
        return self.__isSuperTriviaGameEnabled

    def isSupStreamerEnabled(self) -> bool:
        return self.__isSupStreamerEnabled

    def isToxicTriviaEnabled(self) -> bool:
        return self.__isToxicTriviaEnabled

    def isTranslateEnabled(self) -> bool:
        return self.__isTranslateEnabled

    def isTriviaGameEnabled(self) -> bool:
        return self.__isTriviaGameEnabled

    def isTriviaScoreEnabled(self) -> bool:
        return self.__isTriviaScoreEnabled

    def isTtsEnabled(self) -> bool:
        return self.__isTtsEnabled

    def isWeatherEnabled(self) -> bool:
        return self.__isWeatherEnabled

    def isWelcomeTtsEnabled(self) -> bool:
        return self.__isWelcomeTtsEnabled

    def isWordOfTheDayEnabled(self) -> bool:
        return self.__isWordOfTheDayEnabled

    def __repr__(self) -> str:
        return self.__handle

    @property
    def timeoutCheerActionFollowShieldDays(self) -> int | None:
        return self.__timeoutCheerActionFollowShieldDays