from src.halfLife.models.halfLifeVoice import HalfLifeVoice


class TestHalfLifeVoice:

    def test_keyName(self):
        results: set[str] = set()

        for voice in HalfLifeVoice:
            results.add(voice.keyName)

        assert len(results) == len(HalfLifeVoice)

    def test_keyName_withAll(self):
        result = HalfLifeVoice.ALL.keyName
        assert result == 'all'

    def test_keyName_withBarney(self):
        result = HalfLifeVoice.BARNEY.keyName
        assert result == 'barney'

    def test_keyName_withHev(self):
        result = HalfLifeVoice.HEV.keyName
        assert result == 'hev'

    def test_keyName_withIntercom(self):
        result = HalfLifeVoice.INTERCOM.keyName
        assert result == 'intercom'

    def test_keyName_withPolice(self):
        result = HalfLifeVoice.POLICE.keyName
        assert result == 'police'

    def test_keyName_withScientist(self):
        result = HalfLifeVoice.SCIENTIST.keyName
        assert result == 'scientist'

    def test_keyName_withSoldier(self):
        result = HalfLifeVoice.SOLDIER.keyName
        assert result == 'soldier'

    def test_humanName(self):
        results: set[str] = set()

        for voice in HalfLifeVoice:
            results.add(voice.humanName)

        assert len(results) == len(HalfLifeVoice)

    def test_humanName_withAll(self):
        result = HalfLifeVoice.ALL.humanName
        assert result == 'All'

    def test_humanName_withBarney(self):
        result = HalfLifeVoice.BARNEY.humanName
        assert result == 'Barney'

    def test_humanName_withHev(self):
        result = HalfLifeVoice.HEV.humanName
        assert result == 'Hazardous EnVironment suit (HEV)'

    def test_humanName_withIntercom(self):
        result = HalfLifeVoice.INTERCOM.humanName
        assert result == 'Intercom'

    def test_humanName_withPolice(self):
        result = HalfLifeVoice.POLICE.humanName
        assert result == 'Police'

    def test_humanName_withScientist(self):
        result = HalfLifeVoice.SCIENTIST.humanName
        assert result == 'Scientist'

    def test_humanName_withSoldier(self):
        result = HalfLifeVoice.SOLDIER.humanName
        assert result == 'Soldier'
