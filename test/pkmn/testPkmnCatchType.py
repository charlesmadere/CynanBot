import unittest

from pkmn.pkmnCatchType import PkmnCatchType


class TestPkmnCatchType(unittest.TestCase):

    def test_fromStr(self):
        self.assertEqual(PkmnCatchType.NORMAL, PkmnCatchType.fromStr("normal"))
        self.assertEqual(PkmnCatchType.NORMAL, PkmnCatchType.fromStr("NORMAL"))

        self.assertEqual(PkmnCatchType.GREAT, PkmnCatchType.fromStr("great"))
        self.assertEqual(PkmnCatchType.GREAT, PkmnCatchType.fromStr("GREAT"))

        self.assertEqual(PkmnCatchType.ULTRA, PkmnCatchType.fromStr("ultra"))
        self.assertEqual(PkmnCatchType.ULTRA, PkmnCatchType.fromStr("ULTRA"))

    def test_getSortOrder(self):
        self.assertEqual(PkmnCatchType.NORMAL.getSortOrder(), 0)
        self.assertEqual(PkmnCatchType.GREAT.getSortOrder(), 1)
        self.assertEqual(PkmnCatchType.ULTRA.getSortOrder(), 2)

    def test_toStr(self):
        self.assertEqual(PkmnCatchType.NORMAL.toStr(), "normal")
        self.assertEqual(PkmnCatchType.GREAT.toStr(), "great")
        self.assertEqual(PkmnCatchType.ULTRA.toStr(), "ultra")
