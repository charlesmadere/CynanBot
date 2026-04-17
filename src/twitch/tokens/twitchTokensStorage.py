from typing import Final

from .twitchTokensStorageInterface import TwitchTokensStorageInterface
from ..localModels.twitchTokensDetails import TwitchTokensDetails
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...storage.jsonFileReader import JsonFileReader
from ...storage.jsonReaderInterface import JsonReaderInterface
from ...timber.timberInterface import TimberInterface


class TwitchTokensStorage(TwitchTokensStorageInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

        self.__isDatabaseReady: bool = False

    async def __consumeSeedFile(self):
        # TODO
        pass

    async def get(
        self,
        twitchChannelId: str,
    ) -> TwitchTokensDetails | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        # TODO
        return None

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS twitchtokens (
                            expirationtime text DEFAULT NULL,
                            accesstoken text NOT NULL,
                            refreshtoken text NOT NULL,
                            twitchchannelid text NOT NULL PRIMARY KEY
                        )
                    ''',
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS twitchtokens (
                            expirationtime TEXT DEFAULT NULL,
                            accesstoken TEXT NOT NULL,
                            refreshtoken TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL PRIMARY KEY
                        ) STRICT
                    ''',
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()
        await self.__consumeSeedFile()

    async def remove(
        self,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        # TODO
        pass

    async def set(
        self,
        twitchChannelId: str,
        twitchTokensDetails: TwitchTokensDetails | None,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if twitchTokensDetails is None:
            await self.remove(
                twitchChannelId = twitchChannelId,
            )
            return

        # TODO
        pass
