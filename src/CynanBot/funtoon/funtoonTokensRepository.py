from typing import Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.funtoon.exceptions import NoFuntoonTokenException
from CynanBot.funtoon.funtoonTokensRepositoryInterface import \
    FuntoonTokensRepositoryInterface
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface
from CynanBot.timber.timberInterface import TimberInterface


class FuntoonTokensRepository(FuntoonTokensRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        seedFileReader: Optional[JsonReaderInterface] = None
    ):
        assert isinstance(backingDatabase, BackingDatabase), f"malformed {backingDatabase=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert seedFileReader is None or isinstance(seedFileReader, JsonReaderInterface), f"malformed {seedFileReader=}"

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__seedFileReader: Optional[JsonReaderInterface] = seedFileReader

        self.__isDatabaseReady: bool = False
        self.__cache: Dict[str, Optional[str]] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('FuntoonTokensRepository', 'Caches cleared')

    async def __consumeSeedFile(self):
        seedFileReader = self.__seedFileReader

        if seedFileReader is None:
            return

        self.__seedFileReader = None

        if not await seedFileReader.fileExistsAsync():
            self.__timber.log('FuntoonTokensRepository', f'Seed file (\"{seedFileReader}\") does not exist')
            return

        jsonContents: Optional[Dict[str, str]] = await seedFileReader.readJsonAsync()
        await seedFileReader.deleteFileAsync()

        if not utils.hasItems(jsonContents):
            self.__timber.log('FuntoonTokensRepository', f'Seed file (\"{seedFileReader}\") is empty')
            return

        self.__timber.log('FuntoonTokensRepository', f'Reading in seed file \"{seedFileReader}\"...')

        for twitchChannel, token in jsonContents.items():
            await self.setToken(
                token = token,
                twitchChannel = twitchChannel
            )

        self.__timber.log('FuntoonTokensRepository', f'Finished reading in seed file \"{seedFileReader}\"')

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getToken(self, twitchChannel: str) -> Optional[str]:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        if twitchChannel.lower() in self.__cache:
            return self.__cache[twitchChannel.lower()]

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT token FROM funtoontokens
                WHERE twitchchannel = $1
                LIMIT 1
            ''',
            twitchChannel
        )

        await connection.close()
        token: Optional[str] = None

        if utils.hasItems(record):
            token = record[0]

        self.__cache[twitchChannel.lower()] = token

        return token

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS funtoontokens (
                        token text DEFAULT NULL,
                        twitchchannel public.citext NOT NULL PRIMARY KEY
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS funtoontokens (
                        token TEXT DEFAULT NULL,
                        twitchchannel TEXT NOT NULL PRIMARY KEY COLLATE NOCASE
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()
        await self.__consumeSeedFile()

    async def requireToken(self, twitchChannel: str) -> str:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        token = await self.getToken(twitchChannel)

        if not utils.isValidStr(token):
            raise NoFuntoonTokenException(f'token for twitchChannel \"{twitchChannel}\" is missing/unavailable')

        return token

    async def setToken(self, token: Optional[str], twitchChannel: str):
        assert token is None or isinstance(token, str), f"malformed {token=}"
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        connection = await self.__getDatabaseConnection()

        if utils.isValidStr(token):
            await connection.execute(
                '''
                    INSERT INTO funtoontokens (token, twitchchannel)
                    VALUES ($1, $2)
                    ON CONFLICT (twitchchannel) DO UPDATE SET token = EXCLUDED.token
                ''',
                token, twitchChannel
            )

            self.__cache[twitchChannel.lower()] = token
            self.__timber.log('FuntoonTokensRepository', f'Funtoon token for \"{twitchChannel}\" has been updated (\"{token}\")')
        else:
            await connection.execute(
                '''
                    DELETE FROM funtoontokens
                    WHERE twitchchannel = $1
                ''',
                twitchChannel
            )

            self.__cache[twitchChannel.lower()] = None
            self.__timber.log('FuntoonTokensRepository', f'Funtoon token for \"{twitchChannel}\" has been deleted')

        await connection.close()
