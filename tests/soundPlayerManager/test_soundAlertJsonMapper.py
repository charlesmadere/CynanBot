import pytest

from src.soundPlayerManager.jsonMapper.soundAlertJsonMapper import SoundAlertJsonMapper
from src.soundPlayerManager.jsonMapper.soundAlertJsonMapperInterface import SoundAlertJsonMapperInterface
from src.soundPlayerManager.soundAlert import SoundAlert


class TestSoundAlertJsonMapper:

    jsonMapper: SoundAlertJsonMapperInterface = SoundAlertJsonMapper()

    def test_parseSoundAlert_withAirStrikeString(self):
        result = self.jsonMapper.parseSoundAlert('air_strike')
        assert result is SoundAlert.AIR_STRIKE

    def test_parseSoundAlert_withBeanString(self):
        result = self.jsonMapper.parseSoundAlert('bean')
        assert result is SoundAlert.BEAN

    def test_parseSoundAlert_withCheerString(self):
        result = self.jsonMapper.parseSoundAlert('cheer')
        assert result is SoundAlert.CHEER

    def test_parseSoundAlert_withClickNavigationString(self):
        result = self.jsonMapper.parseSoundAlert('click_navigation')
        assert result is SoundAlert.CLICK_NAVIGATION

    def test_parseSoundAlert_withEmptyString(self):
        result = self.jsonMapper.parseSoundAlert('')
        assert result is None

    def test_parseSoundAlert_withFollow(self):
        result = self.jsonMapper.parseSoundAlert('follow')
        assert result is SoundAlert.FOLLOW

    def test_parseSoundAlert_withGrenade_1String(self):
        result = self.jsonMapper.parseSoundAlert('grenade_1')
        assert result is SoundAlert.GRENADE_1

    def test_parseSoundAlert_withGrenade_2String(self):
        result = self.jsonMapper.parseSoundAlert('grenade_2')
        assert result is SoundAlert.GRENADE_2

    def test_parseSoundAlert_withGrenade_3String(self):
        result = self.jsonMapper.parseSoundAlert('grenade_3')
        assert result is SoundAlert.GRENADE_3

    def test_parseSoundAlert_withHypeTrainString(self):
        result = self.jsonMapper.parseSoundAlert('hype_train')
        assert result is SoundAlert.HYPE_TRAIN

    def test_parseSoundAlert_withJackpotString(self):
        result = self.jsonMapper.parseSoundAlert('jackpot')
        assert result is SoundAlert.JACKPOT

    def test_parseSoundAlert_withLaunchAirStrikeString(self):
        result = self.jsonMapper.parseSoundAlert('launch_air_strike')
        assert result is SoundAlert.LAUNCH_AIR_STRIKE

    def test_parseSoundAlert_withMegaGrenade1String(self):
        result = self.jsonMapper.parseSoundAlert('mega_grenade_1')
        assert result is SoundAlert.MEGA_GRENADE_1

    def test_parseSoundAlert_withMegaGrenade2String(self):
        result = self.jsonMapper.parseSoundAlert('mega_grenade_2')
        assert result is SoundAlert.MEGA_GRENADE_2

    def test_parseSoundAlert_withMegaGrenade3String(self):
        result = self.jsonMapper.parseSoundAlert('mega_grenade_3')
        assert result is SoundAlert.MEGA_GRENADE_3

    def test_parseSoundAlert_withNone(self):
        result = self.jsonMapper.parseSoundAlert(None)
        assert result is None

    def test_parseSoundAlert_withPointRedemption01String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_01')
        assert result is SoundAlert.POINT_REDEMPTION_01

    def test_parseSoundAlert_withPointRedemption02String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_02')
        assert result is SoundAlert.POINT_REDEMPTION_02

    def test_parseSoundAlert_withPointRedemption03String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_03')
        assert result is SoundAlert.POINT_REDEMPTION_03

    def test_parseSoundAlert_withPointRedemption04String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_04')
        assert result is SoundAlert.POINT_REDEMPTION_04

    def test_parseSoundAlert_withPointRedemption05String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_05')
        assert result is SoundAlert.POINT_REDEMPTION_05

    def test_parseSoundAlert_withPointRedemption06String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_06')
        assert result is SoundAlert.POINT_REDEMPTION_06

    def test_parseSoundAlert_withPointRedemption07String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_07')
        assert result is SoundAlert.POINT_REDEMPTION_07

    def test_parseSoundAlert_withPointRedemption08String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_08')
        assert result is SoundAlert.POINT_REDEMPTION_08

    def test_parseSoundAlert_withPointRedemption09String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_09')
        assert result is SoundAlert.POINT_REDEMPTION_09

    def test_parseSoundAlert_withPointRedemption10String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_10')
        assert result is SoundAlert.POINT_REDEMPTION_10

    def test_parseSoundAlert_withPointRedemption11String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_11')
        assert result is SoundAlert.POINT_REDEMPTION_11

    def test_parseSoundAlert_withPointRedemption12String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_12')
        assert result is SoundAlert.POINT_REDEMPTION_12

    def test_parseSoundAlert_withPointRedemption13String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_13')
        assert result is SoundAlert.POINT_REDEMPTION_13

    def test_parseSoundAlert_withPointRedemption14String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_14')
        assert result is SoundAlert.POINT_REDEMPTION_14

    def test_parseSoundAlert_withPointRedemption15String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_15')
        assert result is SoundAlert.POINT_REDEMPTION_15

    def test_parseSoundAlert_withPointRedemption16String(self):
        result = self.jsonMapper.parseSoundAlert('point_redemption_16')
        assert result is SoundAlert.POINT_REDEMPTION_16

    def test_parseSoundAlert_withPredictionString(self):
        result = self.jsonMapper.parseSoundAlert('prediction')
        assert result is SoundAlert.PREDICTION

    def test_parseSoundAlert_withRaidString(self):
        result = self.jsonMapper.parseSoundAlert('raid')
        assert result is SoundAlert.RAID

    def test_parseSoundAlert_withRandomFromDirectory(self):
        result = self.jsonMapper.parseSoundAlert('random_from_directory')
        assert result is SoundAlert.RANDOM_FROM_DIRECTORY

    def test_parseSoundAlert_withSplatString(self):
        result = self.jsonMapper.parseSoundAlert('splat')
        assert result is SoundAlert.SPLAT

    def test_parseSoundAlert_withSubscribeString(self):
        result = self.jsonMapper.parseSoundAlert('subscribe')
        assert result is SoundAlert.SUBSCRIBE

    def test_parseSoundAlert_withTntString(self):
        result = self.jsonMapper.parseSoundAlert('tnt')
        assert result is SoundAlert.AIR_STRIKE

    def test_parseSoundAlert_withWhitespaceString(self):
        result = self.jsonMapper.parseSoundAlert(' ')
        assert result is None

    def test_requireSoundAlert_withAirStrike(self):
        result = self.jsonMapper.requireSoundAlert('air_strike')
        assert result is SoundAlert.AIR_STRIKE

    def test_requireSoundAlert_withCheer(self):
        result = self.jsonMapper.requireSoundAlert('cheer')
        assert result is SoundAlert.CHEER

    def test_requireSoundAlert_withClick(self):
        result = self.jsonMapper.requireSoundAlert('click_navigation')
        assert result is SoundAlert.CLICK_NAVIGATION

    def test_requireSoundAlert_withEmptyString(self):
        result: SoundAlert | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.requireSoundAlert('')

        assert result is None

    def test_requireSoundAlert_withFollow(self):
        result = self.jsonMapper.requireSoundAlert('follow')
        assert result is SoundAlert.FOLLOW

    def test_requireSoundAlert_withHypeTrain(self):
        result = self.jsonMapper.requireSoundAlert('hype_train')
        assert result is SoundAlert.HYPE_TRAIN

    def test_requireSoundAlert_withNone(self):
        result: SoundAlert | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.requireSoundAlert(None)

        assert result is None

    def test_requireSoundAlert_withPrediction(self):
        result = self.jsonMapper.requireSoundAlert('prediction')
        assert result is SoundAlert.PREDICTION

    def test_requireSoundAlert_withRaid(self):
        result = self.jsonMapper.requireSoundAlert('raid')
        assert result is SoundAlert.RAID

    def test_requireSoundAlert_withSubscribe(self):
        result = self.jsonMapper.requireSoundAlert('subscribe')
        assert result is SoundAlert.SUBSCRIBE

    def test_requireSoundAlert_withWhitespaceString(self):
        result: SoundAlert | None = None

        with pytest.raises(Exception):
            result = self.jsonMapper.requireSoundAlert(' ')

        assert result is None

    def test_sanity(self):
        assert self.jsonMapper is not None
        assert isinstance(self.jsonMapper, SoundAlertJsonMapper)
        assert isinstance(self.jsonMapper, SoundAlertJsonMapperInterface)

    def test_serializeSoundAlert_withAirStrike(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.AIR_STRIKE)
        assert result == 'air_strike'

    def test_serializeSoundAlert_withAllSoundAlertValues(self):
        strings: set[str] = set()

        for soundAlert in SoundAlert:
            serialized = self.jsonMapper.serializeSoundAlert(soundAlert)
            strings.add(serialized)

            parsed = self.jsonMapper.parseSoundAlert(serialized)
            assert parsed == soundAlert

        assert len(strings) == len(SoundAlert)

    def test_serializeSoundAlert_withBean(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.BEAN)
        assert result == 'bean'

    def test_serializeSoundAlert_withCheer(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.CHEER)
        assert result == 'cheer'

    def test_serializeSoundAlert_withClickNavigation(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.CLICK_NAVIGATION)
        assert result == 'click_navigation'

    def test_serializeSoundAlert_withFollow(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.FOLLOW)
        assert result == 'follow'

    def test_serializeSoundAlert_withGrenade_1(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.GRENADE_1)
        assert result == 'grenade_1'

    def test_serializeSoundAlert_withGrenade_2(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.GRENADE_2)
        assert result == 'grenade_2'

    def test_serializeSoundAlert_withGrenade_3(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.GRENADE_3)
        assert result == 'grenade_3'

    def test_serializeSoundAlert_withHypeTrain(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.HYPE_TRAIN)
        assert result == 'hype_train'

    def test_serializeSoundAlert_withJackpot(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.JACKPOT)
        assert result == 'jackpot'

    def test_serializeSoundAlert_withLaunchAirStrike(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.LAUNCH_AIR_STRIKE)
        assert result == 'launch_air_strike'

    def test_serializeSoundAlert_withMegaGrenade1(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.MEGA_GRENADE_1)
        assert result == 'mega_grenade_1'

    def test_serializeSoundAlert_withMegaGrenade2(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.MEGA_GRENADE_2)
        assert result == 'mega_grenade_2'

    def test_serializeSoundAlert_withMegaGrenade3(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.MEGA_GRENADE_3)
        assert result == 'mega_grenade_3'

    def test_serializeSoundAlert_withPointRedemption01(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_01)
        assert result == 'point_redemption_01'

    def test_serializeSoundAlert_withPointRedemption02(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_02)
        assert result == 'point_redemption_02'

    def test_serializeSoundAlert_withPointRedemption03(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_03)
        assert result == 'point_redemption_03'

    def test_serializeSoundAlert_withPointRedemption04(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_04)
        assert result == 'point_redemption_04'

    def test_serializeSoundAlert_withPointRedemption05(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_05)
        assert result == 'point_redemption_05'

    def test_serializeSoundAlert_withPointRedemption06(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_06)
        assert result == 'point_redemption_06'

    def test_serializeSoundAlert_withPointRedemption07(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_07)
        assert result == 'point_redemption_07'

    def test_serializeSoundAlert_withPointRedemption08(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_08)
        assert result == 'point_redemption_08'

    def test_serializeSoundAlert_withPointRedemption09(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_09)
        assert result == 'point_redemption_09'

    def test_serializeSoundAlert_withPointRedemption10(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_10)
        assert result == 'point_redemption_10'

    def test_serializeSoundAlert_withPointRedemption11(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_11)
        assert result == 'point_redemption_11'

    def test_serializeSoundAlert_withPointRedemption12(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_12)
        assert result == 'point_redemption_12'

    def test_serializeSoundAlert_withPointRedemption13(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_13)
        assert result == 'point_redemption_13'

    def test_serializeSoundAlert_withPointRedemption14(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_14)
        assert result == 'point_redemption_14'

    def test_serializeSoundAlert_withPointRedemption15(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_15)
        assert result == 'point_redemption_15'

    def test_serializeSoundAlert_withPointRedemption16(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.POINT_REDEMPTION_16)
        assert result == 'point_redemption_16'

    def test_serializeSoundAlert_withRaid(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.RAID)
        assert result == 'raid'

    def test_serializeSoundAlert_withRandomFromDirectory(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.RANDOM_FROM_DIRECTORY)
        assert result == 'random_from_directory'

    def test_serializeSoundAlert_withSplat(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.SPLAT)
        assert result == 'splat'

    def test_serializeSoundAlert_withSubscribe(self):
        result = self.jsonMapper.serializeSoundAlert(SoundAlert.SUBSCRIBE)
        assert result == 'subscribe'
