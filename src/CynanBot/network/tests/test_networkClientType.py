from CynanBot.network.networkClientType import NetworkClientType


class TestNetworkClientType():

    def test_fromStr_withEmptyString(self):
        result: NetworkClientType = None
        exception: Exception = None

        try:
            result = NetworkClientType.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert exception is not None
        assert isinstance(exception, ValueError)

    def test_fromStr_withPostgresString(self):
        result = NetworkClientType.fromStr('aiohttp')
        assert result is NetworkClientType.AIOHTTP

    def test_fromStr_withSqliteString(self):
        result = NetworkClientType.fromStr('requests')
        assert result is NetworkClientType.REQUESTS

    def test_fromStr_withNone(self):
        result: NetworkClientType = None
        exception: Exception = None

        try:
            result = NetworkClientType.fromStr(None)
        except Exception as e:
            exception = e

        assert result is None
        assert exception is not None
        assert isinstance(exception, ValueError)

    def test_fromStr_withWhitespaceString(self):
        result: NetworkClientType = None
        exception: Exception = None

        try:
            result = NetworkClientType.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert exception is not None
        assert isinstance(exception, ValueError)
