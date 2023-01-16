from datetime import tzinfo
from typing import List

try:
    from CynanBotCommon.cuteness.cutenessBoosterPack import CutenessBoosterPack
    from CynanBotCommon.timeZoneRepository import TimeZoneRepository
    from pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
    from pkmn.pkmnCatchType import PkmnCatchType
    from users.user import User
except:
    from ...CynanBotCommon.cuteness.cutenessBoosterPack import \
        CutenessBoosterPack
    from ...CynanBotCommon.timeZoneRepository import TimeZoneRepository
    from ...pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
    from ...pkmn.pkmnCatchType import PkmnCatchType
    from ...users.user import User


class TestUser():

    def createUser(
        self,
        isAnalogueEnabled: bool = False,
        isCatJamMessageEnabled: bool = False,
        isChatBandEnabled: bool = False,
        isChatLoggingEnabled: bool = False,
        isCutenessEnabled: bool = False,
        isCynanMessageEnabled: bool = False,
        isCynanSourceEnabled: bool = False,
        isDeerForceMessageEnabled: bool = False,
        isEyesMessageEnabled: bool = False,
        isGiftSubscriptionThanksMessageEnabled: bool = False,
        isGiveCutenessEnabled: bool = False,
        isJamCatMessageEnabled: bool = False,
        isJishoEnabled: bool = False,
        isJokesEnabled: bool = False,
        isJokeTriviaRepositoryEnabled: bool = False,
        isLoremIpsumEnabled: bool = False,
        isPicOfTheDayEnabled: bool = False,
        isPkmnEnabled: bool = False,
        isPokepediaEnabled: bool = False,
        isRaceEnabled: bool = False,
        isRaidLinkMessagingEnabled: bool = False,
        isRatJamMessageEnabled: bool = False,
        isRewardIdPrintingEnabled: bool = False,
        isStarWarsQuotesEnabled: bool = False,
        isSuperTriviaGameEnabled: bool = False,
        isTranslateEnabled: bool = False,
        isTriviaEnabled: bool = False,
        isTriviaGameEnabled: bool = False,
        isWeatherEnabled: bool = False,
        isWordOfTheDayEnabled: bool = False,
        superTriviaGameMultiplier: int = 5,
        triviaGamePoints: int = 5,
        waitForTriviaAnswerDelay: int = 45,
        discord: str = None,
        handle: str = "TestUser",
        increaseCutenessDoubleRewardId: str = None,
        instagram: str = None,
        locationId: str = None,
        picOfTheDayFile: str = None,
        picOfTheDayRewardId: str = None,
        pkmnBattleRewardId: str = None,
        pkmnEvolveRewardId: str = None,
        pkmnShinyRewardId: str = None,
        speedrunProfile: str = None,
        triviaGameRewardId: str = None,
        twitter: str = None,
        cutenessBoosterPacks: List[CutenessBoosterPack] = None,
        pkmnCatchBoosterPacks: List[PkmnCatchBoosterPack] = None,
        superTriviaGameControllers: List[str] = None,
        timeZones: List[tzinfo] = None
    ) -> User:
        return User(
            isAnalogueEnabled = isAnalogueEnabled,
            isCatJamMessageEnabled = isCatJamMessageEnabled,
            isChatBandEnabled = isChatBandEnabled,
            isChatLoggingEnabled = isChatLoggingEnabled,
            isCutenessEnabled = isCutenessEnabled,
            isCynanMessageEnabled = isCynanMessageEnabled,
            isCynanSourceEnabled = isCynanSourceEnabled,
            isDeerForceMessageEnabled = isDeerForceMessageEnabled,
            isEyesMessageEnabled = isEyesMessageEnabled,
            isGiftSubscriptionThanksMessageEnabled = isGiftSubscriptionThanksMessageEnabled,
            isGiveCutenessEnabled = isGiveCutenessEnabled,
            isJamCatMessageEnabled = isJamCatMessageEnabled,
            isJishoEnabled = isJishoEnabled,
            isJokesEnabled = isJokesEnabled,
            isJokeTriviaRepositoryEnabled = isJokeTriviaRepositoryEnabled,
            isLoremIpsumEnabled = isLoremIpsumEnabled,
            isPicOfTheDayEnabled = isPicOfTheDayEnabled,
            isPkmnEnabled = isPkmnEnabled,
            isPokepediaEnabled = isPokepediaEnabled,
            isRaceEnabled = isRaceEnabled,
            isRaidLinkMessagingEnabled = isRaidLinkMessagingEnabled,
            isRatJamMessageEnabled = isRatJamMessageEnabled,
            isRewardIdPrintingEnabled = isRewardIdPrintingEnabled,
            isStarWarsQuotesEnabled = isStarWarsQuotesEnabled,
            isSuperTriviaGameEnabled = isSuperTriviaGameEnabled,
            isTranslateEnabled = isTranslateEnabled,
            isTriviaEnabled = isTriviaEnabled,
            isTriviaGameEnabled = isTriviaGameEnabled,
            isWeatherEnabled = isWeatherEnabled,
            isWordOfTheDayEnabled = isWordOfTheDayEnabled,
            superTriviaGameMultiplier = superTriviaGameMultiplier,
            triviaGamePoints = triviaGamePoints,
            waitForTriviaAnswerDelay = waitForTriviaAnswerDelay,
            discord = discord,
            handle = handle,
            increaseCutenessDoubleRewardId = increaseCutenessDoubleRewardId,
            instagram = instagram,
            locationId = locationId,
            picOfTheDayFile = picOfTheDayFile,
            picOfTheDayRewardId = picOfTheDayRewardId,
            pkmnBattleRewardId = pkmnBattleRewardId,
            pkmnEvolveRewardId = pkmnEvolveRewardId,
            pkmnShinyRewardId = pkmnShinyRewardId,
            speedrunProfile = speedrunProfile,
            triviaGameRewardId = triviaGameRewardId,
            twitter = twitter,
            cutenessBoosterPacks = cutenessBoosterPacks,
            pkmnCatchBoosterPacks = pkmnCatchBoosterPacks,
            superTriviaGameControllers = superTriviaGameControllers,
            timeZones = timeZones
        )

    def test_hasCutenessBoosterPacks(self):
        user = self.createUser(cutenessBoosterPacks = [
            CutenessBoosterPack(amount = 1, rewardId = "a")
        ])
        assert user.hasCutenessBoosterPacks() is True

        user = self.createUser(cutenessBoosterPacks = [
            CutenessBoosterPack(amount = 1, rewardId = "a"),
            CutenessBoosterPack(amount = 2, rewardId = "b"),
            CutenessBoosterPack(amount = 3, rewardId = "c")
        ])
        assert user.hasCutenessBoosterPacks() is True

        user = self.createUser(cutenessBoosterPacks = list())
        assert user.hasCutenessBoosterPacks() is False

        user = self.createUser(cutenessBoosterPacks = None)
        assert user.hasCutenessBoosterPacks() is False

    def test_hasDiscord(self):
        user = self.createUser(discord = "https://example.com/")
        assert user.hasDiscord() is True

        user = self.createUser(discord = "example")
        assert user.hasDiscord() is False

        user = self.createUser(discord = "")
        assert user.hasDiscord() is False

        user = self.createUser(discord = None)
        assert user.hasDiscord() is False

    def test_hasInstagram(self):
        user = self.createUser(instagram = "https://example.com/")
        assert user.hasInstagram() is True

        user = self.createUser(instagram = "example")
        assert user.hasInstagram() is False

        user = self.createUser(instagram = "")
        assert user.hasInstagram() is False

        user = self.createUser(instagram = None)
        assert user.hasInstagram() is False

    def test_hasLocationId(self):
        user = self.createUser(locationId = "locationId")
        assert user.hasLocationId() is True

        user = self.createUser(locationId = None)
        assert user.hasLocationId() is False

    def test_hasPkmnCatchBoosterPacks(self):
        user = self.createUser(pkmnCatchBoosterPacks = [
            PkmnCatchBoosterPack(pkmnCatchType = PkmnCatchType.NORMAL, rewardId = "a")
        ])
        assert user.hasPkmnCatchBoosterPacks() is True

        user = self.createUser(pkmnCatchBoosterPacks = [
            PkmnCatchBoosterPack(pkmnCatchType = PkmnCatchType.NORMAL, rewardId = "a"),
            PkmnCatchBoosterPack(pkmnCatchType = PkmnCatchType.GREAT, rewardId = "b"),
            PkmnCatchBoosterPack(pkmnCatchType = PkmnCatchType.ULTRA, rewardId = "c")
        ])
        assert user.hasPkmnCatchBoosterPacks() is True

        user = self.createUser(pkmnCatchBoosterPacks = list())
        assert user.hasPkmnCatchBoosterPacks() is False

        user = self.createUser(pkmnCatchBoosterPacks = None)
        assert user.hasPkmnCatchBoosterPacks() is False

    def test_hasSpeedrunProfile(self):
        user = self.createUser(speedrunProfile = "https://example.com/")
        assert user.hasSpeedrunProfile() is True

        user = self.createUser(speedrunProfile = "example")
        assert user.hasSpeedrunProfile() is False

        user = self.createUser(speedrunProfile = "")
        assert user.hasSpeedrunProfile() is False

        user = self.createUser(speedrunProfile = None)
        assert user.hasSpeedrunProfile() is False

    def hasTimeZones(self):
        timeZoneRepository = TimeZoneRepository()

        user = self.createUser(timeZones = [
            timeZoneRepository.getTimeZone("Asia/Tokyo"),
            timeZoneRepository.getTimeZone("US/Pacific")
        ])
        assert user.hasTimeZones() is True

        user = self.createUser(timeZones = [
            timeZoneRepository.getTimeZone("America/New_York")
        ])
        assert user.hasTimeZones() is True

        user = self.createUser(timeZones = list())
        assert user.hasTimeZones() is False

        user = self.createUser(timeZones = None)
        assert user.hasTimeZones() is False

    def test_hasTriviaGamePoints(self):
        user = self.createUser(triviaGamePoints = 0)
        assert user.hasTriviaGamePoints() is True

        user = self.createUser(triviaGamePoints = 1)
        assert user.hasTriviaGamePoints() is True

        user = self.createUser(triviaGamePoints = -1)
        assert user.hasTriviaGamePoints() is True

        user = self.createUser(triviaGamePoints = None)
        assert user.hasTriviaGamePoints() is False

    def test_hasTwitter(self):
        user = self.createUser(twitter = "https://example.com/")
        assert user.hasTwitter() is True

        user = self.createUser(twitter = "example")
        assert user.hasTwitter() is False

        user = self.createUser(twitter = "")
        assert user.hasTwitter() is False

        user = self.createUser(twitter = None)
        assert user.hasTwitter() is False

    def test_hasWaitForTriviaAnswerDelay(self):
        user = self.createUser(waitForTriviaAnswerDelay = 0)
        assert user.hasWaitForTriviaAnswerDelay() is True

        user = self.createUser(waitForTriviaAnswerDelay = 1)
        assert user.hasWaitForTriviaAnswerDelay() is True

        user = self.createUser(waitForTriviaAnswerDelay = -1)
        assert user.hasWaitForTriviaAnswerDelay() is True

        user = self.createUser(waitForTriviaAnswerDelay = None)
        assert user.hasWaitForTriviaAnswerDelay() is False
