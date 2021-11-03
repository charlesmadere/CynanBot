import unittest
from datetime import tzinfo
from typing import List

from cuteness.cutenessBoosterPack import CutenessBoosterPack
from pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack

from user.user import User


class TestUser(unittest.TestCase):

    def createUser(
        self,
        isAnalogueEnabled: bool = False,
        isCatJamEnabled: bool = False,
        isChatBandEnabled: bool = False,
        isCutenessEnabled: bool = False,
        isCynanMessageEnabled: bool = False,
        isCynanSourceEnabled: bool = False,
        isDeerForceMessageEnabled: bool = False,
        isDiccionarioEnabled: bool = False,
        isGiveCutenessEnabled: bool = False,
        isJamCatEnabled: bool = False,
        isJishoEnabled: bool = False,
        isJokesEnabled: bool = False,
        isLocalTriviaRepositoryEnabled: bool = False,
        isPicOfTheDayEnabled: bool = False,
        isPkmnEnabled: bool = False,
        isPokepediaEnabled: bool = False,
        isRaceEnabled: bool = False,
        isRaidLinkMessagingEnabled: bool = False,
        isRatJamEnabled: bool = False,
        isRewardIdPrintingEnabled: bool = False,
        isStarWarsQuotesEnabled: bool = False,
        isTamalesEnabled: bool = False,
        isTranslateEnabled: bool = False,
        isTriviaEnabled: bool = False,
        isTriviaGameEnabled: bool = False,
        isWeatherEnabled: bool = False,
        isWordOfTheDayEnabled: bool = False,
        triviaGamePoints: int = 5,
        triviaGameTutorialCutenessThreshold: int = 50,
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
        timeZones: List[tzinfo] = None
    ) -> User:
        return User(
            isAnalogueEnabled = isAnalogueEnabled,
            isCatJamEnabled = isCatJamEnabled,
            isChatBandEnabled = isChatBandEnabled,
            isCutenessEnabled = isCutenessEnabled,
            isCynanMessageEnabled = isCynanMessageEnabled,
            isCynanSourceEnabled = isCynanSourceEnabled,
            isDeerForceMessageEnabled = isDeerForceMessageEnabled,
            isDiccionarioEnabled = isDiccionarioEnabled,
            isGiveCutenessEnabled = isGiveCutenessEnabled,
            isJamCatEnabled = isJamCatEnabled,
            isJishoEnabled = isJishoEnabled,
            isJokesEnabled = isJokesEnabled,
            isLocalTriviaRepositoryEnabled = isLocalTriviaRepositoryEnabled,
            isPicOfTheDayEnabled = isPicOfTheDayEnabled,
            isPkmnEnabled = isPkmnEnabled,
            isPokepediaEnabled = isPokepediaEnabled,
            isRaceEnabled = isRaceEnabled,
            isRaidLinkMessagingEnabled = isRaidLinkMessagingEnabled,
            isRatJamEnabled = isRatJamEnabled,
            isRewardIdPrintingEnabled = isRewardIdPrintingEnabled,
            isStarWarsQuotesEnabled = isStarWarsQuotesEnabled,
            isTamalesEnabled = isTamalesEnabled,
            isTranslateEnabled = isTranslateEnabled,
            isTriviaEnabled = isTriviaEnabled,
            isTriviaGameEnabled = isTriviaGameEnabled,
            isWeatherEnabled = isWeatherEnabled,
            isWordOfTheDayEnabled = isWordOfTheDayEnabled,
            triviaGamePoints = triviaGamePoints,
            triviaGameTutorialCutenessThreshold = triviaGameTutorialCutenessThreshold,
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
            timeZones = timeZones
        )

    def test_hasDiscord(self):
        user = self.createUser(discord = "https://example.com/")
        self.assertEqual(True, user.hasDiscord())

        user = self.createUser(discord = "example")
        self.assertEqual(False, user.hasDiscord())

        user = self.createUser(discord = "")
        self.assertEqual(False, user.hasDiscord())

        user = self.createUser(discord = None)
        self.assertEqual(False, user.hasDiscord())

    def test_hasInstagram(self):
        user = self.createUser(instagram = "https://example.com/")
        self.assertEqual(True, user.hasInstagram())

        user = self.createUser(instagram = "example")
        self.assertEqual(False, user.hasInstagram())

        user = self.createUser(instagram = "")
        self.assertEqual(False, user.hasInstagram())

        user = self.createUser(instagram = None)
        self.assertEqual(False, user.hasInstagram())

    def test_hasLocationId(self):
        user = self.createUser(locationId = "locationId")
        self.assertEqual(True, user.hasLocationId())

        user = self.createUser(locationId = None)
        self.assertEqual(False, user.hasLocationId())

    def test_hasSpeedrunProfile(self):
        user = self.createUser(speedrunProfile = "https://example.com/")
        self.assertEqual(True, user.hasSpeedrunProfile())

        user = self.createUser(speedrunProfile = "example")
        self.assertEqual(False, user.hasSpeedrunProfile())

        user = self.createUser(speedrunProfile = "")
        self.assertEqual(False, user.hasSpeedrunProfile())

        user = self.createUser(speedrunProfile = None)
        self.assertEqual(False, user.hasSpeedrunProfile())

    def test_hasTwitter(self):
        user = self.createUser(twitter = "https://example.com/")
        self.assertEqual(True, user.hasTwitter())

        user = self.createUser(twitter = "example")
        self.assertEqual(False, user.hasTwitter())

        user = self.createUser(twitter = "")
        self.assertEqual(False, user.hasTwitter())

        user = self.createUser(twitter = None)
        self.assertEqual(False, user.hasTwitter())
