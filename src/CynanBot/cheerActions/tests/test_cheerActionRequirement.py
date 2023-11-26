from typing import Optional

from CynanBot.cheerActions.cheerActionRequirement import CheerActionRequirement


class TestCheerActionRequirement():

    def test_fromStr_withEmptyString(self):
        result: Optional[CheerActionRequirement] = None
        exception: Optional[Exception] = None

        try:
            result = CheerActionRequirement.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withNone(self):
        result: Optional[CheerActionRequirement] = None
        exception: Optional[Exception] = None

        try:
            result = CheerActionRequirement.fromStr(None)
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withExactString(self):
        result = CheerActionRequirement.fromStr('exact')
        assert result is CheerActionRequirement.EXACT

    def test_fromStr_withGreaterThanOrEqualToString(self):
        result = CheerActionRequirement.fromStr('greater_than_or_equal_to')
        assert result is CheerActionRequirement.GREATER_THAN_OR_EQUAL_TO

    def test_fromStr_withWhitespaceString(self):
        result: Optional[CheerActionRequirement] = None
        exception: Optional[Exception] = None

        try:
            result = CheerActionRequirement.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_toStr_withExact(self):
        result = CheerActionRequirement.EXACT.toStr()
        assert result == 'exact'

    def test_toStr_withGreaterThanOrEqualTo(self):
        result = CheerActionRequirement.GREATER_THAN_OR_EQUAL_TO.toStr()
        assert result == 'greater_than_or_equal_to'
