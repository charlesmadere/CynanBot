from typing import Optional

from cheerActions.cheerActionType import CheerActionType


class TestCheerActionType():

    def test_fromStr_withEmptyString(self):
        result: Optional[CheerActionType] = None
        exception: Optional[Exception] = None

        try:
            result = CheerActionType.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withNone(self):
        result: Optional[CheerActionType] = None
        exception: Optional[Exception] = None

        try:
            result = CheerActionType.fromStr(None)
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withTimeoutString(self):
        result = CheerActionType.fromStr('timeout')
        assert result is CheerActionType.TIMEOUT

    def test_fromStr_withWhitespaceString(self):
        result: Optional[CheerActionType] = None
        exception: Optional[Exception] = None

        try:
            result = CheerActionType.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_toStr_withTimeout(self):
        result = CheerActionType.TIMEOUT.toStr()
        assert result == 'timeout'
