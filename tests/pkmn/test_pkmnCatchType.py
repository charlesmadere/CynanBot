from pkmn.pkmnCatchType import PkmnCatchType


class TestPkmnCatchType():

    def test_fromStr_withEmptyString(self):
        catchType: PkmnCatchType = None
        exception: Exception = None

        try:
            catchType = PkmnCatchType.fromStr('')
        except Exception as e:
            exception = e

        assert catchType is None
        assert exception is not None
        assert isinstance(exception, ValueError)

    def test_fromStr_withGreatStrings(self):
        assert PkmnCatchType.GREAT == PkmnCatchType.fromStr('great')
        assert PkmnCatchType.GREAT == PkmnCatchType.fromStr('GREAT')

    def test_fromStr_withNormalStrings(self):
        assert PkmnCatchType.NORMAL == PkmnCatchType.fromStr('normal')
        assert PkmnCatchType.NORMAL == PkmnCatchType.fromStr('NORMAL')

    def test_fromStr_withNone(self):
        catchType: PkmnCatchType = None
        exception: Exception = None

        try:
            catchType = PkmnCatchType.fromStr(None)
        except Exception as e:
            exception = e

        assert catchType is None
        assert exception is not None
        assert isinstance(exception, ValueError)

    def test_fromStr_withUltraStrings(self):
        assert PkmnCatchType.ULTRA == PkmnCatchType.fromStr('ultra')
        assert PkmnCatchType.ULTRA == PkmnCatchType.fromStr('ULTRA')

    def test_getSortOrder_withGreat(self):
        assert PkmnCatchType.GREAT.getSortOrder() == 1

    def test_getSortOrder_withNormal(self):
        assert PkmnCatchType.NORMAL.getSortOrder() == 0

    def test_getSortOrder_withUltra(self):
        assert PkmnCatchType.ULTRA.getSortOrder() == 2

    def test_toStr_withGreat(self):
        assert PkmnCatchType.GREAT.toStr() == 'great'

    def test_toStr_withNormal(self):
        assert PkmnCatchType.NORMAL.toStr() == 'normal'

    def test_toStr_withUltra(self):
        assert PkmnCatchType.ULTRA.toStr() == 'ultra'
