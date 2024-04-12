import pytest

from CynanBot.cheerActions.cheerActionBitRequirement import \
    CheerActionBitRequirement


class TestCheerBitActionRequirement():

    def test_fromStr_withEmptyString(self):
        result: CheerActionBitRequirement | None = None

        with pytest.raises(ValueError):
            result = CheerActionBitRequirement.fromStr('')

        assert result is None

    def test_fromStr_withNone(self):
        result: CheerActionBitRequirement | None = None

        with pytest.raises(ValueError):
            result = CheerActionBitRequirement.fromStr(None)

        assert result is None

    def test_fromStr_withExactString(self):
        result = CheerActionBitRequirement.fromStr('exact')
        assert result is CheerActionBitRequirement.EXACT

    def test_fromStr_withGreaterThanOrEqualToString(self):
        result = CheerActionBitRequirement.fromStr('greater_than_or_equal_to')
        assert result is CheerActionBitRequirement.GREATER_THAN_OR_EQUAL_TO

    def test_fromStr_withWhitespaceString(self):
        result: CheerActionBitRequirement | None = None

        with pytest.raises(ValueError):
            result = CheerActionBitRequirement.fromStr(' ')

        assert result is None

    def test_toStr_withExact(self):
        result = CheerActionBitRequirement.EXACT.toStr()
        assert result == 'exact'

    def test_toStr_withGreaterThanOrEqualTo(self):
        result = CheerActionBitRequirement.GREATER_THAN_OR_EQUAL_TO.toStr()
        assert result == 'greater_than_or_equal_to'
