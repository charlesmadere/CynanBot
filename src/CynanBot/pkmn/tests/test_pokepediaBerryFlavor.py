from CynanBot.pkmn.pokepediaBerryFlavor import PokepediaBerryFlavor


class TestPokepediaBerryFlavor():

    def test_fromStr_withOne(self):
        result = PokepediaBerryFlavor.fromInt(1)
        assert result is PokepediaBerryFlavor.SPICY

    def test_fromStr_withTwo(self):
        result = PokepediaBerryFlavor.fromInt(2)
        assert result is PokepediaBerryFlavor.DRY

    def test_fromStr_withThree(self):
        result = PokepediaBerryFlavor.fromInt(3)
        assert result is PokepediaBerryFlavor.SWEET

    def test_fromStr_withFour(self):
        result = PokepediaBerryFlavor.fromInt(4)
        assert result is PokepediaBerryFlavor.BITTER

    def test_fromStr_withFive(self):
        result = PokepediaBerryFlavor.fromInt(5)
        assert result is PokepediaBerryFlavor.SOUR
