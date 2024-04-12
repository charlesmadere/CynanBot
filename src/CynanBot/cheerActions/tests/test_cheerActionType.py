import pytest

from CynanBot.cheerActions.cheerActionType import CheerActionType


class TestCheerActionType():

    def test_fromStr_withEmptyString(self):
        result: CheerActionType | None = None

        with pytest.raises(ValueError):
            result = CheerActionType.fromStr('')

        assert result is None

    def test_fromStr_withNone(self):
        result: CheerActionType | None = None

        with pytest.raises(ValueError):
            result = CheerActionType.fromStr(None)

        assert result is None

    def test_fromStr_withTimeoutString(self):
        result = CheerActionType.fromStr('timeout')
        assert result is CheerActionType.TIMEOUT

    def test_fromStr_withWhitespaceString(self):
        result: CheerActionType | None = None

        with pytest.raises(ValueError):
            result = CheerActionType.fromStr(' ')

        assert result is None

    def test_toStr_withTimeout(self):
        result = CheerActionType.TIMEOUT.toStr()
        assert result == 'timeout'
