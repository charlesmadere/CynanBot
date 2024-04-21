import pytest

from CynanBot.network.networkClientType import NetworkClientType


class TestNetworkClientType():

    def test_fromStr_withEmptyString(self):
        result: NetworkClientType | None = None

        with pytest.raises(ValueError):
            result = NetworkClientType.fromStr('')

        assert result is None

    def test_fromStr_withPostgresString(self):
        result = NetworkClientType.fromStr('aiohttp')
        assert result is NetworkClientType.AIOHTTP

    def test_fromStr_withSqliteString(self):
        result = NetworkClientType.fromStr('requests')
        assert result is NetworkClientType.REQUESTS

    def test_fromStr_withNone(self):
        result: NetworkClientType | None = None

        with pytest.raises(ValueError):
            result = NetworkClientType.fromStr(None)  # type: ignore

        assert result is None

    def test_fromStr_withWhitespaceString(self):
        result: NetworkClientType | None = None

        with pytest.raises(ValueError):
            result = NetworkClientType.fromStr(' ')

        assert result is None
