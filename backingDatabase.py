import sqlite3


class BackingDatabase():

    def __init__(self, databaseFile: str = 'database.sqlite'):
        if databaseFile is None or len(databaseFile) == 0 or databaseFile.isspace():
            raise ValueError(
                f'databaseFile argument is malformed: \"{databaseFile}\"')

        self.__connection = sqlite3.connect(databaseFile)

    def getConnection(self):
        return self.__connection
