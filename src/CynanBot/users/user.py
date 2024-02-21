from datetime import tzinfo
from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.cuteness.cutenessBoosterPack import CutenessBoosterPack
from CynanBot.users.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from CynanBot.users.userInterface import UserInterface


class User(UserInterface):

    def __init__(
        self,
        areCheerActionsEnabled: bool,
        areRecurringActionsEnabled: bool,
        isAnivContentScanningEnabled: bool,
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
        isGiftSubscriptionThanksMessageEnabled: bool,
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
        isTriviaEnabled: bool,
        isTriviaGameEnabled: bool,
        isTriviaScoreEnabled: bool,
        isTtsEnabled: bool,
        isWeatherEnabled: bool,
        isWelcomeTtsEnabled: bool,
        isWordOfTheDayEnabled: bool,
        superTriviaCheerTriggerAmount: Optional[float],
        superTriviaSubscribeTriggerAmount: Optional[float],
        maximumTtsCheerAmount: Optional[int],
        minimumTtsCheerAmount: Optional[int],
        superTriviaCheerTriggerMaximum: Optional[int],
        superTriviaGamePoints: Optional[int],
        superTriviaGameRewardId: Optional[str],
        superTriviaGameShinyMultiplier: Optional[int],
        superTriviaGameToxicMultiplier: Optional[int],
        superTriviaGameToxicPunishmentMultiplier: Optional[int],
        superTriviaPerUserAttempts: Optional[int],
        superTriviaSubscribeTriggerMaximum: Optional[int],
        triviaGamePoints: Optional[int],
        triviaGameShinyMultiplier: Optional[int],
        waitForSuperTriviaAnswerDelay: Optional[int],
        waitForTriviaAnswerDelay: Optional[int],
        casualGamePollRewardId: Optional[str],
        casualGamePollUrl: Optional[str],
        discord: Optional[str],
        handle: str,
        instagram: Optional[str],
        locationId: Optional[str],
        mastodonUrl: Optional[str],
        pkmnBattleRewardId: Optional[str],
        pkmnEvolveRewardId: Optional[str],
        pkmnShinyRewardId: Optional[str],
        speedrunProfile: Optional[str],
        supStreamerMessage: Optional[str],
        triviaGameRewardId: Optional[str],
        twitter: str,
        cutenessBoosterPacks: Optional[List[CutenessBoosterPack]],
        pkmnCatchBoosterPacks: Optional[List[PkmnCatchBoosterPack]],
        timeZones: Optional[List[tzinfo]]
    ):
        if not utils.isValidBool(areCheerActionsEnabled):
            raise TypeError(f'areCheerActionsEnabled argument is malformed: \"{areCheerActionsEnabled}\"')
        if not utils.isValidBool(areRecurringActionsEnabled):
            raise TypeError(f'areRecurringActionsEnabled argument is malformed: \"{areRecurringActionsEnabled}\"')
        if not utils.isValidBool(isAnivContentScanningEnabled):
            raise TypeError(f'isAnivContentScanningEnabled argument is malformed: \"{isAnivContentScanningEnabled}\"')
        if not utils.isValidBool(isCasualGamePollEnabled):
            raise TypeError(f'isCasualGamePollEnabled argument is malformed: \"{isCasualGamePollEnabled}\"')
        if not utils.isValidBool(isCatJamMessageEnabled):
            raise TypeError(f'isCatJamMessageEnabled argument is malformed: \"{isCatJamMessageEnabled}\"')
        if not utils.isValidBool(isChannelPredictionChartEnabled):
            raise TypeError(f'isChannelPredictionChartEnabled argument is malformed: \"{isChannelPredictionChartEnabled}\"')
        if not utils.isValidBool(isChatBandEnabled):
            raise TypeError(f'isChatBandEnabled argument is malformed: \"{isChatBandEnabled}\"')
        if not utils.isValidBool(isChatLoggingEnabled):
            raise TypeError(f'isChatLoggingEnabled argument is malformed: \"{isChatLoggingEnabled}\"')
        if not utils.isValidBool(isCutenessEnabled):
            raise TypeError(f'isCutenessEnabled argument is malformed: \"{isCutenessEnabled}\"')
        if not utils.isValidBool(isCynanSourceEnabled):
            raise TypeError(f'isCynanSourceEnabled argument is malformed: \"{isCynanSourceEnabled}\"')
        if not utils.isValidBool(isDeerForceMessageEnabled):
            raise TypeError(f'isDeerForceMessageEnabled argument is malformed: \"{isDeerForceMessageEnabled}\"')
        if not utils.isValidBool(isEnabled):
            raise TypeError(f'isEnabled argument is malformed: \"{isEnabled}\"')
        if not utils.isValidBool(isEyesMessageEnabled):
            raise TypeError(f'isEyesMessageEnabled argument is malformed: \"{isEyesMessageEnabled}\"')
        if not utils.isValidBool(isGiftSubscriptionThanksMessageEnabled):
            raise TypeError(f'isGiftSubscriptionThanksMessageEnabled argument is malformed: \"{isGiftSubscriptionThanksMessageEnabled}\"')
        if not utils.isValidBool(isGiveCutenessEnabled):
            raise TypeError(f'isGiveCutenessEnabled argument is malformed: \"{isGiveCutenessEnabled}\"')
        if not utils.isValidBool(isImytSlurpMessageEnabled):
            raise TypeError(f'isImytSlurpMessageEnabled argument is malformed: \"{isImytSlurpMessageEnabled}\"')
        if not utils.isValidBool(isJamCatMessageEnabled):
            raise TypeError(f'isJamCatMessageEnabled argument is malformed: \"{isJamCatMessageEnabled}\"')
        if not utils.isValidBool(isJishoEnabled):
            raise TypeError(f'isJishoEnabled argument is malformed: \"{isJishoEnabled}\"')
        if not utils.isValidBool(isLoremIpsumEnabled):
            raise TypeError(f'isLoremIpsumEnabled argument is malformed: \"{isLoremIpsumEnabled}\"')
        if not utils.isValidBool(isPkmnEnabled):
            raise TypeError(f'isPkmnEnabled argument is malformed: \"{isPkmnEnabled}\"')
        if not utils.isValidBool(isPokepediaEnabled):
            raise TypeError(f'isPokepediaEnabled argument is malformed: \"{isPokepediaEnabled}\"')
        if not utils.isValidBool(isRaceEnabled):
            raise TypeError(f'isRaceEnabled argument is malformed: \"{isRaceEnabled}\"')
        if not utils.isValidBool(isRaidLinkMessagingEnabled):
            raise TypeError(f'isRaidLinkMessagingEnabled argument is malformed: \"{isRaidLinkMessagingEnabled}\"')
        if not utils.isValidBool(isRatJamMessageEnabled):
            raise TypeError(f'isRatJamMessageEnabled argument is malformed: \"{isRatJamMessageEnabled}\"')
        if not utils.isValidBool(isRewardIdPrintingEnabled):
            raise TypeError(f'isRewardIdPrintingEnabled argument is malformed: \"{isRewardIdPrintingEnabled}\"')
        if not utils.isValidBool(isRoachMessageEnabled):
            raise TypeError(f'isRoachMessageEnabled argument is malformed: \"{isRoachMessageEnabled}\"')
        if not utils.isValidBool(isSchubertWalkMessageEnabled):
            raise TypeError(f'isSchubertWalkMessageEnabled argument is malformed: \"{isSchubertWalkMessageEnabled}\"')
        if not utils.isValidBool(isShinyTriviaEnabled):
            raise TypeError(f'isShinyTriviaEnabled argument is malformed: \"{isShinyTriviaEnabled}\"')
        if not utils.isValidBool(isStarWarsQuotesEnabled):
            raise TypeError(f'isStarWarsQuotesEnabled argument is malformed: \"{isStarWarsQuotesEnabled}\"')
        if not utils.isValidBool(isSubGiftThankingEnabled):
            raise TypeError(f'isSubGiftThankingEnabled argument is malformed: \"{isSubGiftThankingEnabled}\"')
        if not utils.isValidBool(isSuperTriviaGameEnabled):
            raise TypeError(f'isSuperTriviaGameEnabled argument is malformed: \"{isSuperTriviaGameEnabled}\"')
        if not utils.isValidBool(isSupStreamerEnabled):
            raise TypeError(f'isSupStreamerEnabled argument is malformed: \"{isSupStreamerEnabled}\"')
        if not utils.isValidBool(isToxicTriviaEnabled):
            raise TypeError(f'isToxicTriviaEnabled argument is malformed: \"{isToxicTriviaEnabled}\"')
        if not utils.isValidBool(isTranslateEnabled):
            raise TypeError(f'isTranslateEnabled argument is malformed: \"{isTranslateEnabled}\"')
        if not utils.isValidBool(isTriviaEnabled):
            raise TypeError(f'isTriviaEnabled argument is malformed: \"{isTriviaEnabled}\"')
        if not utils.isValidBool(isTriviaGameEnabled):
            raise TypeError(f'isTriviaGameEnabled argument is malformed: \"{isTriviaGameEnabled}\"')
        if not utils.isValidBool(isTriviaScoreEnabled):
            raise TypeError(f'isTriviaScoreEnabled argument is malformed: \"{isTriviaScoreEnabled}\"')
        if not utils.isValidBool(isTtsEnabled):
            raise TypeError(f'isTtsEnabled argument is malformed: \"{isTtsEnabled}\"')
        if not utils.isValidBool(isWeatherEnabled):
            raise TypeError(f'isWeatherEnabled argument is malformed: \"{isWeatherEnabled}\"')
        if not utils.isValidBool(isWelcomeTtsEnabled):
            raise TypeError(f'isWelcomeTtsEnabled argument is malformed: \"{isWelcomeTtsEnabled}\"')
        if not utils.isValidBool(isWordOfTheDayEnabled):
            raise TypeError(f'isWordOfTheDayEnabled argument is malformed: \"{isWordOfTheDayEnabled}\"')
        if superTriviaCheerTriggerAmount is not None and not utils.isValidNum(superTriviaCheerTriggerAmount):
            raise TypeError(f'superTriviaCheerTriggerAmount argument is malformed: \"{superTriviaCheerTriggerAmount}\"')
        if superTriviaSubscribeTriggerAmount is not None and not utils.isValidNum(superTriviaSubscribeTriggerAmount):
            raise TypeError(f'superTriviaSubscribeTriggerAmount argument is malformed: \"{superTriviaSubscribeTriggerAmount}\"')
        if maximumTtsCheerAmount is not None and not utils.isValidInt(maximumTtsCheerAmount):
            raise TypeError(f'maximumTtsCheerAmount argument is malformed: \"{maximumTtsCheerAmount}\"')
        if minimumTtsCheerAmount is not None and not utils.isValidInt(minimumTtsCheerAmount):
            raise TypeError(f'minimumTtsCheerAmount argument is malformed: \"{minimumTtsCheerAmount}\"')
        if superTriviaGamePoints is not None and not utils.isValidInt(superTriviaGamePoints):
            raise TypeError(f'superTriviaGamePoints argument is malformed: \"{superTriviaGamePoints}\"')
        if superTriviaCheerTriggerMaximum is not None and not utils.isValidInt(superTriviaCheerTriggerMaximum):
            raise TypeError(f'superTriviaCheerTriggerMaximum argument is malformed: \"{superTriviaCheerTriggerMaximum}\"')
        assert superTriviaGameRewardId is None or isinstance(superTriviaGameRewardId, str), f"malformed {superTriviaGameRewardId=}"
        if superTriviaGameShinyMultiplier is not None and not utils.isValidInt(superTriviaGameShinyMultiplier):
            raise TypeError(f'superTriviaGameShinyMultiplier argument is malformed: \"{superTriviaGameShinyMultiplier}\"')
        if superTriviaGameToxicPunishmentMultiplier is not None and not utils.isValidInt(superTriviaGameToxicPunishmentMultiplier):
            raise TypeError(f'superTriviaGameToxicPunishmentMultiplier argument is malformed: \"{superTriviaGameToxicPunishmentMultiplier}\"')
        if superTriviaPerUserAttempts is not None and not utils.isValidInt(superTriviaPerUserAttempts):
            raise TypeError(f'superTriviaPeruserAttempts argument is malformed: \"{superTriviaPerUserAttempts}\"')
        if superTriviaSubscribeTriggerMaximum is not None and not utils.isValidInt(superTriviaSubscribeTriggerMaximum):
            raise TypeError(f'superTriviaSubscribeTriggerMaximum argument is malformed: \"{superTriviaSubscribeTriggerMaximum}\"')
        if triviaGamePoints is not None and not utils.isValidInt(triviaGamePoints):
            raise TypeError(f'triviaGamePoints argument is malformed: \"{triviaGamePoints}\"')
        if triviaGameShinyMultiplier is not None and not utils.isValidInt(triviaGameShinyMultiplier):
            raise TypeError(f'triviaGameShinyMultiplier argument is malformed: \"{triviaGameShinyMultiplier}\"')
        if waitForSuperTriviaAnswerDelay is not None and not utils.isValidInt(waitForSuperTriviaAnswerDelay):
            raise TypeError(f'waitForSuperTriviaAnswerDelay argument is malformed: \"{waitForSuperTriviaAnswerDelay}\"')
        if waitForTriviaAnswerDelay is not None and not utils.isValidInt(waitForTriviaAnswerDelay):
            raise TypeError(f'waitForTriviaAnswerDelay argument is malformed: \"{waitForTriviaAnswerDelay}\"')
        assert casualGamePollRewardId is None or isinstance(casualGamePollRewardId, str), f"malformed {casualGamePollRewardId=}"
        assert casualGamePollUrl is None or isinstance(casualGamePollUrl, str), f"malformed {casualGamePollUrl=}"
        assert discord is None or isinstance(discord, str), f"malformed {discord=}"
        if not utils.isValidStr(handle):
            raise TypeError(f'handle argument is malformed: \"{handle}\"')
        assert locationId is None or isinstance(locationId, str), f"malformed {locationId=}"
        assert mastodonUrl is None or isinstance(mastodonUrl, str), f"malformed {mastodonUrl=}"
        assert pkmnBattleRewardId is None or isinstance(pkmnBattleRewardId, str), f"malformed {pkmnBattleRewardId=}"
        if pkmnEvolveRewardId and not isinstance(pkmnEvolveRewardId, str):
            raise TypeError(f'pkmnEvolveRewardId argument is malformed: \"{pkmnEvolveRewardId}\"')
        if pkmnShinyRewardId and not isinstance(pkmnShinyRewardId, str):
            raise TypeError(f'pkmnShinyRewardId argument is malformed: \"{pkmnShinyRewardId}\"')
        assert speedrunProfile is None or isinstance(speedrunProfile, str), f"malformed {speedrunProfile=}"
        assert supStreamerMessage is None or isinstance(supStreamerMessage, str), f"malformed {supStreamerMessage=}"
        assert triviaGameRewardId is None or isinstance(triviaGameRewardId, str), f"malformed {triviaGameRewardId=}"
        assert twitter is None or isinstance(twitter, str), f"malformed {twitter=}"

        self.__areCheerActionsEnabled: bool = areCheerActionsEnabled
        self.__areRecurringActionsEnabled: bool = areRecurringActionsEnabled
        self.__isAnivContentScanningEnabled: bool = isAnivContentScanningEnabled
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
        self.__isGiftSubscriptionThanksMessageEnabled: bool = isGiftSubscriptionThanksMessageEnabled
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
        self.__isTriviaEnabled: bool = isTriviaEnabled
        self.__isTriviaGameEnabled: bool = isTriviaGameEnabled
        self.__isTriviaScoreEnabled: bool = isTriviaScoreEnabled
        self.__isTtsEnabled: bool = isTtsEnabled
        self.__isWeatherEnabled: bool = isWeatherEnabled
        self.__isWelcomeTtsEnabled: bool = isWelcomeTtsEnabled
        self.__isWordOfTheDayEnabled: bool = isWordOfTheDayEnabled
        self.__superTriviaCheerTriggerAmount: Optional[float] = superTriviaCheerTriggerAmount
        self.__superTriviaSubscribeTriggerAmount: Optional[float] = superTriviaSubscribeTriggerAmount
        self.__maximumTtsCheerAmount: Optional[int] = maximumTtsCheerAmount
        self.__minimumTtsCheerAmount: Optional[int] = minimumTtsCheerAmount
        self.__superTriviaCheerTriggerMaximum: Optional[int] = superTriviaCheerTriggerMaximum
        self.__superTriviaGamePoints: Optional[int] = superTriviaGamePoints
        self.__superTriviaGameRewardId: Optional[str] = superTriviaGameRewardId
        self.__superTriviaGameShinyMultiplier: Optional[int] = superTriviaGameShinyMultiplier
        self.__superTriviaGameToxicMultiplier: Optional[int] = superTriviaGameToxicMultiplier
        self.__superTriviaGameToxicPunishmentMultiplier: Optional[int] = superTriviaGameToxicPunishmentMultiplier
        self.__superTriviaPerUserAttempts: Optional[int] = superTriviaPerUserAttempts
        self.__superTriviaSubscribeTriggerMaximum: Optional[int] = superTriviaSubscribeTriggerMaximum
        self.__triviaGamePoints: Optional[int] = triviaGamePoints
        self.__triviaGameShinyMultiplier: Optional[int] = triviaGameShinyMultiplier
        self.__waitForTriviaAnswerDelay: Optional[int] = waitForTriviaAnswerDelay
        self.__waitForSuperTriviaAnswerDelay: Optional[int] = waitForSuperTriviaAnswerDelay
        self.__casualGamePollRewardId: Optional[str] = casualGamePollRewardId
        self.__casualGamePollUrl: Optional[str] = casualGamePollUrl
        self.__discord: Optional[str] = discord
        self.__handle: str = handle
        self.__instagram: Optional[str] = instagram
        self.__locationId: Optional[str] = locationId
        self.__mastodonUrl: Optional[str] = mastodonUrl
        self.__pkmnBattleRewardId: Optional[str] = pkmnBattleRewardId
        self.__pkmnEvolveRewardId: Optional[str] = pkmnEvolveRewardId
        self.__pkmnShinyRewardId: Optional[str] = pkmnShinyRewardId
        self.__speedrunProfile: Optional[str] = speedrunProfile
        self.__supStreamerMessage: Optional[str] = supStreamerMessage
        self.__triviaGameRewardId: Optional[str] = triviaGameRewardId
        self.__twitter: Optional[str] = twitter
        self.__cutenessBoosterPacks: Optional[List[CutenessBoosterPack]] = cutenessBoosterPacks
        self.__pkmnCatchBoosterPacks: Optional[List[PkmnCatchBoosterPack]] = pkmnCatchBoosterPacks
        self.__timeZones: Optional[List[tzinfo]] = timeZones

    def areCheerActionsEnabled(self) -> bool:
        return self.__areCheerActionsEnabled

    def areRecurringActionsEnabled(self) -> bool:
        return self.__areRecurringActionsEnabled

    def getCasualGamePollRewardId(self) -> Optional[str]:
        return self.__casualGamePollRewardId

    def getCasualGamePollUrl(self) -> Optional[str]:
        return self.__casualGamePollUrl

    def getCutenessBoosterPacks(self) -> Optional[List[CutenessBoosterPack]]:
        return self.__cutenessBoosterPacks

    def getDiscordUrl(self) -> Optional[str]:
        return self.__discord

    def getHandle(self) -> str:
        return self.__handle

    def getInstagramUrl(self) -> Optional[str]:
        return self.__instagram

    def getLocationId(self) -> Optional[str]:
        return self.__locationId

    def getMastodonUrl(self) -> Optional[str]:
        return self.__mastodonUrl

    def getMaximumTtsCheerAmount(self) -> Optional[int]:
        return self.__maximumTtsCheerAmount

    def getMinimumTtsCheerAmount(self) -> Optional[int]:
        return self.__minimumTtsCheerAmount

    def getPkmnBattleRewardId(self) -> Optional[str]:
        return self.__pkmnBattleRewardId

    def getPkmnCatchBoosterPacks(self) -> Optional[List[PkmnCatchBoosterPack]]:
        return self.__pkmnCatchBoosterPacks

    def getPkmnEvolveRewardId(self) -> Optional[str]:
        return self.__pkmnEvolveRewardId

    def getPkmnShinyRewardId(self) -> Optional[str]:
        return self.__pkmnShinyRewardId

    def getSpeedrunProfile(self) -> Optional[str]:
        return self.__speedrunProfile

    def getSuperTriviaCheerTriggerAmount(self) -> Optional[float]:
        return self.__superTriviaCheerTriggerAmount

    def getSuperTriviaCheerTriggerMaximum(self) -> Optional[int]:
        return self.__superTriviaCheerTriggerMaximum

    def getSuperTriviaGamePoints(self) -> Optional[int]:
        return self.__superTriviaGamePoints

    def getSuperTriviaGameRewardId(self) -> Optional[str]:
        return self.__superTriviaGameRewardId

    def getSuperTriviaGameShinyMultiplier(self) -> Optional[int]:
        return self.__superTriviaGameShinyMultiplier

    def getSuperTriviaGameToxicMultiplier(self) -> Optional[int]:
        return self.__superTriviaGameToxicMultiplier

    def getSuperTriviaGameToxicPunishmentMultiplier(self) -> Optional[int]:
        return self.__superTriviaGameToxicPunishmentMultiplier

    def getSuperTriviaPerUserAttempts(self) -> Optional[int]:
        return self.__superTriviaPerUserAttempts

    def getSuperTriviaSubscribeTriggerAmount(self) -> Optional[float]:
        return self.__superTriviaSubscribeTriggerAmount

    def getSuperTriviaSubscribeTriggerMaximum(self) -> Optional[int]:
        return self.__superTriviaSubscribeTriggerMaximum

    def getSupStreamerMessage(self) -> Optional[str]:
        return self.__supStreamerMessage

    def getTimeZones(self) -> Optional[List[tzinfo]]:
        return self.__timeZones

    def getTriviaGamePoints(self) -> Optional[int]:
        return self.__triviaGamePoints

    def getTriviaGameRewardId(self) -> Optional[str]:
        return self.__triviaGameRewardId

    def getTriviaGameShinyMultiplier(self) -> Optional[int]:
        return self.__triviaGameShinyMultiplier

    def getTwitchUrl(self) -> str:
        return f'https://twitch.tv/{self.__handle.lower()}'

    def getTwitterUrl(self) -> Optional[str]:
        return self.__twitter

    def getWaitForSuperTriviaAnswerDelay(self) -> Optional[int]:
        return self.__waitForSuperTriviaAnswerDelay

    def getWaitForTriviaAnswerDelay(self) -> Optional[int]:
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
        return utils.isValidUrl(self.__twitter)

    def isAnivContentScanningEnabled(self) -> bool:
        return self.__isAnivContentScanningEnabled

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

    def isGiftSubscriptionThanksMessageEnabled(self) -> bool:
        return self.__isGiftSubscriptionThanksMessageEnabled

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

    def isTriviaEnabled(self) -> bool:
        return self.__isTriviaEnabled

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
