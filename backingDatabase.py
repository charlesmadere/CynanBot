import sqlite3

import utils


class BackingDatabase():

    def __init__(self, databaseFile: str = 'database.sqlite'):
        if not utils.isValidStr(databaseFile):
            raise ValueError(f'databaseFile argument is malformed: \"{databaseFile}\"')

        self.__connection = sqlite3.connect(databaseFile)

    def getConnection(self):
        return self.__connection
