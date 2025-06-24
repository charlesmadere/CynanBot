import pytest
from frozendict import frozendict

from src.soundPlayerManager.jsonMapper.soundAlertJsonMapper import SoundAlertJsonMapper
from src.soundPlayerManager.jsonMapper.soundAlertJsonMapperInterface import SoundAlertJsonMapperInterface
from src.soundPlayerManager.soundAlert import SoundAlert
from src.users.soundAlert.soundAlertRedemption import SoundAlertRedemption
from src.users.soundAlert.soundAlertRedemptionJsonParser import SoundAlertRedemptionJsonParser
from src.users.soundAlert.soundAlertRedemptionJsonParserInterface import SoundAlertRedemptionJsonParserInterface


class TestSoundAlertRedemptionJsonParser:

    soundAlertJsonMapper: SoundAlertJsonMapperInterface = SoundAlertJsonMapper()

    jsonParser: SoundAlertRedemptionJsonParserInterface = SoundAlertRedemptionJsonParser(
        soundAlertJsonMapper = soundAlertJsonMapper
    )

    def test_parseRedemption(self):
        redemption = SoundAlertRedemption(
            isImmediate = True,
            soundAlert = SoundAlert.RANDOM_FROM_DIRECTORY,
            directoryPath = 'nay',
            rewardId = 'xyz789'
        )

        result = self.jsonParser.parseRedemption({
            'directoryPath': redemption.directoryPath,
            'isImmediate': redemption.isImmediate,
            'rewardId': redemption.rewardId,
            'soundAlert': self.soundAlertJsonMapper.serializeSoundAlert(redemption.soundAlert)
        })

        assert isinstance(result, SoundAlertRedemption)
        assert result == redemption
        assert result.directoryPath == redemption.directoryPath
        assert result.isImmediate == redemption.isImmediate
        assert result.rewardId == redemption.rewardId
        assert result.soundAlert == redemption.soundAlert

    def test_parseRedemption_withEmptyDictionary(self):
        result: SoundAlertRedemption | None = None

        with pytest.raises(Exception):
            self.jsonParser.parseRedemption(dict())

        assert result is None

    def test_parseRedemption_withNone(self):
        result: SoundAlertRedemption | None = None

        with pytest.raises(Exception):
            self.jsonParser.parseRedemption(None) # type: ignore

        assert result is None

    def test_parseRedemptions(self):
        redemption1 = SoundAlertRedemption(
            isImmediate = True,
            soundAlert = SoundAlert.POINT_REDEMPTION_01,
            directoryPath = None,
            rewardId = 'abc123'
        )

        redemption2 = SoundAlertRedemption(
            isImmediate = False,
            soundAlert = SoundAlert.RANDOM_FROM_DIRECTORY,
            directoryPath = 'yay',
            rewardId = 'def456'
        )

        result = self.jsonParser.parseRedemptions([
            {
                'directoryPath': redemption1.directoryPath,
                'isImmediate': redemption1.isImmediate,
                'rewardId': redemption1.rewardId,
                'soundAlert': self.soundAlertJsonMapper.serializeSoundAlert(redemption1.soundAlert)
            },
            {
                'directoryPath': redemption2.directoryPath,
                'rewardId': redemption2.rewardId,
                'soundAlert': self.soundAlertJsonMapper.serializeSoundAlert(redemption2.soundAlert)
            }
        ])

        assert isinstance(result, frozendict)
        assert len(result) == 2

        redemption = result[redemption1.rewardId]
        assert isinstance(redemption, SoundAlertRedemption)
        assert redemption == redemption1
        assert redemption.directoryPath == redemption1.directoryPath
        assert redemption.isImmediate == redemption1.isImmediate
        assert redemption.rewardId == redemption1.rewardId
        assert redemption.soundAlert == redemption1.soundAlert

        redemption = result[redemption2.rewardId]
        assert isinstance(redemption, SoundAlertRedemption)
        assert redemption == redemption2
        assert redemption.directoryPath == redemption2.directoryPath
        assert redemption.isImmediate == redemption2.isImmediate
        assert redemption.rewardId == redemption2.rewardId
        assert redemption.soundAlert == redemption2.soundAlert

    def test_parseRedemptions_withEmptyList(self):
        result = self.jsonParser.parseRedemptions(list())
        assert result is None

    def test_parseRedemptions_withNone(self):
        result = self.jsonParser.parseRedemptions(None)
        assert result is None

    def test_sanity(self):
        assert self.jsonParser is not None
        assert isinstance(self.jsonParser, SoundAlertRedemptionJsonParser)
        assert isinstance(self.jsonParser, SoundAlertRedemptionJsonParserInterface)
