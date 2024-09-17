from src.soundPlayerManager.soundAlert import SoundAlert
from src.soundPlayerManager.soundAlertJsonMapper import SoundAlertJsonMapper
from src.soundPlayerManager.soundAlertJsonMapperInterface import SoundAlertJsonMapperInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestSoundAlertJsonMapper:

    timber: TimberInterface = TimberStub()

    jsonMapper: SoundAlertJsonMapperInterface = SoundAlertJsonMapper(
        timber = timber
    )

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

    def test_parseSoundAlert_withRaidString(self):
        result = self.jsonMapper.parseSoundAlert('raid')
        assert result is SoundAlert.RAID

    def test_parseSoundAlert_withRandomFromDirectory(self):
        result = self.jsonMapper.parseSoundAlert('random_from_directory')
        assert result is SoundAlert.RANDOM_FROM_DIRECTORY

    def test_parseSoundAlert_withSubscribeString(self):
        result = self.jsonMapper.parseSoundAlert('subscribe')
        assert result is SoundAlert.SUBSCRIBE

    def test_parseSoundAlert_withWhitespaceString(self):
        result = self.jsonMapper.parseSoundAlert(' ')
        assert result is None
