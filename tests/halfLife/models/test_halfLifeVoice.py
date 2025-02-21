from src.halfLife.models.halfLifeVoice import HalfLifeVoice


class TestHalfLifeVoice:

    def test_value_withAll(self):
        result = HalfLifeVoice.ALL.keyName
        assert result == 'all'

    def test_value_withBarney(self):
        result = HalfLifeVoice.BARNEY.keyName
        assert result == 'barney'

    def test_value_withHev(self):
        result = HalfLifeVoice.HEV.keyName
        assert result == 'hev'

    def test_value_withIntercom(self):
        result = HalfLifeVoice.INTERCOM.keyName
        assert result == 'intercom'

    def test_value_withPolice(self):
        result = HalfLifeVoice.POLICE.keyName
        assert result == 'police'

    def test_value_withScientist(self):
        result = HalfLifeVoice.SCIENTIST.keyName
        assert result == 'scientist'

    def test_value_withSoldier(self):
        result = HalfLifeVoice.SOLDIER.keyName
        assert result == 'soldier'
