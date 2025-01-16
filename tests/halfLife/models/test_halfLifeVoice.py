from src.halfLife.models.halfLifeVoice import HalfLifeVoice


class TestHalfLifeVoice:

    def test_value_withAll(self):
        result = HalfLifeVoice.ALL.value
        assert result == 'all'

    def test_value_withBarney(self):
        result = HalfLifeVoice.BARNEY.value
        assert result == 'barney'

    def test_value_withFemale(self):
        result = HalfLifeVoice.FEMALE.value
        assert result == 'female'

    def test_value_withMale(self):
        result = HalfLifeVoice.MALE.value
        assert result == 'male'

    def test_value_withPolice(self):
        result = HalfLifeVoice.POLICE.value
        assert result == 'police'

    def test_value_withScientist(self):
        result = HalfLifeVoice.SCIENTIST.value
        assert result == 'scientist'

    def test_value_withSoldier(self):
        result = HalfLifeVoice.SOLDIER.value
        assert result == 'soldier'

