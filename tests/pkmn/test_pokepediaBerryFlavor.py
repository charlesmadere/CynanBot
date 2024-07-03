from src.pkmn.pokepediaBerryFlavor import PokepediaBerryFlavor


class TestPokepediaBerryFlavor():

    def test_getBerryFlavorId_withBitter(self):
        assert PokepediaBerryFlavor.BITTER.getBerryFlavorId() == 4

    def test_getBerryFlavorId_withDry(self):
        assert PokepediaBerryFlavor.DRY.getBerryFlavorId() == 2

    def test_getBerryFlavorId_withSpicy(self):
        assert PokepediaBerryFlavor.SPICY.getBerryFlavorId() == 1

    def test_getBerryFlavorId_withSour(self):
        assert PokepediaBerryFlavor.SOUR.getBerryFlavorId() == 5

    def test_getBerryFlavorId_withSweet(self):
        assert PokepediaBerryFlavor.SWEET.getBerryFlavorId() == 3
