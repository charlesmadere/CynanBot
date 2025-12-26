import pytest

from src.network.networkClientType import NetworkClientType
from src.network.networkJsonMapper import NetworkJsonMapper
from src.network.networkJsonMapperInterface import NetworkJsonMapperInterface


class TestNetworkJsonMapper:

    jsonMapper: NetworkJsonMapperInterface = NetworkJsonMapper()

    def test_parseClientType_withEmptyString(self):
        result: NetworkClientType | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.parseClientType('')

        assert result is None

    def test_parseClientType_withNone(self):
        result: NetworkClientType | None = None

        with pytest.raises(TypeError):
            result = self.jsonMapper.parseClientType(None)

        assert result is None

    def test_parseClientType_withAiohttpString(self):
        result = self.jsonMapper.parseClientType('aiohttp')
        assert result is NetworkClientType.AIOHTTP

    def test_parseClientType_withRequestsString(self):
        result = self.jsonMapper.parseClientType('requests')
        assert result is NetworkClientType.REQUESTS

    def test_parseClientType_withWhitespaceString(self):
        result: NetworkClientType | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.parseClientType(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_parseClientTypeAsync_withEmptyString(self):
        result: NetworkClientType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.parseClientTypeAsync('')

        assert result is None

    @pytest.mark.asyncio
    async def test_parseDatabaseTypeAsync_withNone(self):
        result: NetworkClientType | None = None

        with pytest.raises(TypeError):
            result = await self.jsonMapper.parseClientTypeAsync(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_parseDatabaseTypeAsync_withAiohttpString(self):
        result = await self.jsonMapper.parseClientTypeAsync('aiohttp')
        assert result is NetworkClientType.AIOHTTP

    @pytest.mark.asyncio
    async def test_parseDatabaseTypeAsync_withSqliteString(self):
        result = await self.jsonMapper.parseClientTypeAsync('requests')
        assert result is NetworkClientType.REQUESTS

    @pytest.mark.asyncio
    async def test_parseDatabaseTypeAsync_withWhitespaceString(self):
        result: NetworkClientType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.parseClientTypeAsync(' ')

        assert result is None

    def test_serializeClientType_withAioHttp(self):
        result = self.jsonMapper.serializeClientType(NetworkClientType.AIOHTTP)
        assert result == 'aiohttp'

    def test_serializeClientType_withAll(self):
        results: set[str] = set()

        for clientType in NetworkClientType:
            result = self.jsonMapper.serializeClientType(clientType)
            results.add(result)

        assert len(results) == len(NetworkClientType)

    def test_serializeClientType_withRequests(self):
        result = self.jsonMapper.serializeClientType(NetworkClientType.REQUESTS)
        assert result == 'requests'
