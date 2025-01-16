import pytest

from src.storage.databaseType import DatabaseType
from src.storage.storageJsonMapper import StorageJsonMapper
from src.storage.storageJsonMapperInterface import StorageJsonMapperInterface


class TestStorageJsonMapper:

    jsonMapper: StorageJsonMapperInterface = StorageJsonMapper()

    def test_parseDatabaseType_withEmptyString(self):
        result: DatabaseType | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.parseDatabaseType('')

        assert result is None

    def test_parseDatabaseType_withNone(self):
        result: DatabaseType | None = None

        with pytest.raises(TypeError):
            result = self.jsonMapper.parseDatabaseType(None)

        assert result is None

    def test_parseDatabaseType_withPostgresqlString(self):
        result = self.jsonMapper.parseDatabaseType('postgresql')
        assert result is DatabaseType.POSTGRESQL

    def test_parseDatabaseType_withSqliteString(self):
        result = self.jsonMapper.parseDatabaseType('sqlite')
        assert result is DatabaseType.SQLITE

    def test_parseDatabaseType_withWhitespaceString(self):
        result: DatabaseType | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.parseDatabaseType(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_parseDatabaseTypeAsync_withEmptyString(self):
        result: DatabaseType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.parseDatabaseTypeAsync('')

        assert result is None

    @pytest.mark.asyncio
    async def test_parseDatabaseTypeAsync_withNone(self):
        result: DatabaseType | None = None

        with pytest.raises(TypeError):
            result = await self.jsonMapper.parseDatabaseTypeAsync(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_parseDatabaseTypeAsync_withPostgresqlString(self):
        result = await self.jsonMapper.parseDatabaseTypeAsync('postgresql')
        assert result is DatabaseType.POSTGRESQL

    @pytest.mark.asyncio
    async def test_parseDatabaseTypeAsync_withSqliteString(self):
        result = await self.jsonMapper.parseDatabaseTypeAsync('sqlite')
        assert result is DatabaseType.SQLITE

    @pytest.mark.asyncio
    async def test_parseDatabaseTypeAsync_withWhitespaceString(self):
        result: DatabaseType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.parseDatabaseTypeAsync(' ')

        assert result is None
