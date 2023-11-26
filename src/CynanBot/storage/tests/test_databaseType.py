from typing import Optional

from storage.databaseType import DatabaseType


class TestDatabaseType():

    def test_fromStr_withEmptyString(self):
        result: Optional[DatabaseType] = None
        exception: Optional[Exception] = None

        try:
            result = DatabaseType.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

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
        result: Optional[DatabaseType] = None
        exception: Optional[Exception] = None

        try:
            result = DatabaseType.fromStr(None)
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withWhitespaceString(self):
        result: Optional[DatabaseType] = None
        exception: Optional[Exception] = None

        try:
            result = DatabaseType.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)
