import pytest

from CynanBot.storage.databaseType import DatabaseType


class TestDatabaseType():

    def test_fromStr_withEmptyString(self):
        result: DatabaseType | None = None

        with pytest.raises(TypeError):
            result = DatabaseType.fromStr('')

        assert result is None

    def test_fromStr_withPostgresString(self):
        result = DatabaseType.fromStr('postgres')
        assert result is DatabaseType.POSTGRESQL

    def test_fromStr_withPostgresqlString(self):
        result = DatabaseType.fromStr('postgresql')
        assert result is DatabaseType.POSTGRESQL

    def test_fromStr_withSqliteString(self):
        result = DatabaseType.fromStr('sqlite')
        assert result is DatabaseType.SQLITE

    def test_fromStr_withNone(self):
        result: DatabaseType | None = None

        with pytest.raises(TypeError):
            result = DatabaseType.fromStr(None) # type: ignore

        assert result is None

    def test_fromStr_withWhitespaceString(self):
        result: DatabaseType | None = None

        with pytest.raises(TypeError):
            result = DatabaseType.fromStr(' ')

        assert result is None
