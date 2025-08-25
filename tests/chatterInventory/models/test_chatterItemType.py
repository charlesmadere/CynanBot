from src.chatterInventory.models.chatterItemType import ChatterItemType


class TestChatterItemType:

    def test_humanName_withAll(self):
        results: set[str] = set()

        for itemType in ChatterItemType:
            results.add(itemType.humanName)

        assert len(results) == len(ChatterItemType)

    def test_humanName_withAirStrike(self):
        result = ChatterItemType.AIR_STRIKE.humanName
        assert result == 'Air Strike'

    def test_humanName_withBanana(self):
        result = ChatterItemType.BANANA.humanName
        assert result == 'Banana'

    def test_humanName_withCassetteTape(self):
        result = ChatterItemType.CASSETTE_TAPE.humanName
        assert result == 'Cassette Tape'

    def test_humanName_withGrenade(self):
        result = ChatterItemType.GRENADE.humanName
        assert result == 'Grenade'

    def test_pluralHumanName_withAll(self):
        results: set[str] = set()

        for itemType in ChatterItemType:
            results.add(itemType.pluralHumanName)

        assert len(results) == len(ChatterItemType)

    def test_pluralHumanName_withAirStrike(self):
        result = ChatterItemType.AIR_STRIKE.pluralHumanName
        assert result == 'Air Strikes'

    def test_pluralHumanName_withBanana(self):
        result = ChatterItemType.BANANA.pluralHumanName
        assert result == 'Bananas'

    def test_pluralHumanName_withCassetteTape(self):
        result = ChatterItemType.CASSETTE_TAPE.pluralHumanName
        assert result == 'Cassette Tapes'

    def test_pluralHumanName_withGrenade(self):
        result = ChatterItemType.GRENADE.pluralHumanName
        assert result == 'Grenades'
