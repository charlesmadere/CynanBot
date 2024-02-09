from typing import Optional

from CynanBot.cheerActions.cheerActionBitRequirement import \
    CheerActionBitRequirement


class TestCheerBitActionRequirement():

    def test_fromStr_withEmptyString(self):
        result: Optional[CheerActionBitRequirement] = None
        exception: Optional[Exception] = None

        try:
            result = CheerActionBitRequirement.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withNone(self):
        result: Optional[CheerActionBitRequirement] = None
        exception: Optional[Exception] = None

        try:
            result = CheerActionBitRequirement.fromStr(None)
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withExactString(self):
        result = CheerActionBitRequirement.fromStr('exact')
        assert result is CheerActionBitRequirement.EXACT

    def test_fromStr_withGreaterThanOrEqualToString(self):
        result = CheerActionBitRequirement.fromStr('greater_than_or_equal_to')
        assert result is CheerActionBitRequirement.GREATER_THAN_OR_EQUAL_TO

    def test_fromStr_withWhitespaceString(self):
        result: Optional[CheerActionBitRequirement] = None
        exception: Optional[Exception] = None

        try:
            result = CheerActionBitRequirement.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_toStr_withExact(self):
        result = CheerActionBitRequirement.EXACT.toStr()
        assert result == 'exact'

    def test_toStr_withGreaterThanOrEqualTo(self):
        result = CheerActionBitRequirement.GREATER_THAN_OR_EQUAL_TO.toStr()
        assert result == 'greater_than_or_equal_to'
