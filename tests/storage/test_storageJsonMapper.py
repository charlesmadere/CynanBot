import pytest

from src.storage.databaseType import DatabaseType
from src.storage.storageJsonMapper import StorageJsonMapper
from src.storage.storageJsonMapperInterface import StorageJsonMapperInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestStorageJsonMapper:

    timber: TimberInterface = TimberStub()

    jsonMapper: StorageJsonMapperInterface = StorageJsonMapper(
        timber = timber
    )

    def test_parseDatabaseType_withEmptyString(self):
        result = self.jsonMapper.parseDatabaseType('')
        assert result is None

    def test_parseDatabaseType_withNone(self):
        result = self.jsonMapper.parseDatabaseType(None)
        assert result is None

    def test_parseDatabaseType_withPostgresString(self):
        result = self.jsonMapper.parseDatabaseType('postgres')
        assert result is DatabaseType.POSTGRESQL

    def test_parseDatabaseType_withPostgresqlString(self):
        result = self.jsonMapper.parseDatabaseType('postgresql')
        assert result is DatabaseType.POSTGRESQL

    def test_parseDatabaseType_withSqliteString(self):
        result = self.jsonMapper.parseDatabaseType('sqlite')
        assert result is DatabaseType.SQLITE

    def test_parseDatabaseType_withWhitespaceString(self):
        result = self.jsonMapper.parseDatabaseType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseDatabaseTypeAsync_withEmptyString(self):
        result = await self.jsonMapper.parseDatabaseTypeAsync('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseDatabaseTypeAsync_withNone(self):
        result = await self.jsonMapper.parseDatabaseTypeAsync(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseDatabaseTypeAsync_withPostgresString(self):
        result = await self.jsonMapper.parseDatabaseTypeAsync('postgres')
        assert result is DatabaseType.POSTGRESQL

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
        result = await self.jsonMapper.parseDatabaseTypeAsync(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_requireDatabaseTypeAsync_withEmptyString(self):
        result: DatabaseType | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireDatabaseTypeAsync('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireDatabaseTypeAsync_withNone(self):
        result: DatabaseType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireDatabaseTypeAsync(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireDatabaseTypeAsync_withPostgresString(self):
        result = await self.jsonMapper.requireDatabaseTypeAsync('postgres')
        assert result is DatabaseType.POSTGRESQL

    @pytest.mark.asyncio
    async def test_requireDatabaseTypeAsync_withPostgresqlString(self):
        result = await self.jsonMapper.requireDatabaseTypeAsync('postgresql')
        assert result is DatabaseType.POSTGRESQL

    @pytest.mark.asyncio
    async def test_requireDatabaseTypeAsync_withSqliteString(self):
        result = await self.jsonMapper.requireDatabaseTypeAsync('sqlite')
        assert result is DatabaseType.SQLITE

    @pytest.mark.asyncio
    async def test_requireDatabaseTypeAsync_withWhitespaceString(self):
        result: DatabaseType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireDatabaseTypeAsync(' ')

        assert result is None
