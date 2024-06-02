from CynanBot.pkmn.pokepediaBerryFlavor import PokepediaBerryFlavor


class TestPokepediaBerryFlavor():

    def test_getId_withBitter(self):
        assert PokepediaBerryFlavor.BITTER.getId() == 4

    def test_getId_withDry(self):
        assert PokepediaBerryFlavor.DRY.getId() == 2

    def test_getId_withSpicy(self):
        assert PokepediaBerryFlavor.SPICY.getId() == 1

    def test_getId_withSour(self):
        assert PokepediaBerryFlavor.SOUR.getId() == 5

    def test_getId_withSweet(self):
        assert PokepediaBerryFlavor.SWEET.getId() == 3
