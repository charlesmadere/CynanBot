from datetime import datetime, timedelta
from typing import Final

from .twitchTokensStorageInterface import TwitchTokensStorageInterface
from ..api.models.twitchTokensDetails import TwitchTokensDetails
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
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

    async def __createExpiredExpirationTime(self) -> datetime:
        now = self.__timeZoneRepository.getNow()
        return now - timedelta(weeks = 2)

    async def get(
        self,
        twitchChannelId: str,
    ) -> TwitchTokensDetails | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT expirationtime, accesstoken, refreshtoken FROM twitchtokens
                WHERE twitchchannelid = $1
                LIMIT 1
            ''',
            twitchChannelId,
        )

        await connection.close()

        if record is None or len(record) == 0:
            return None

        expirationTimeString: str | None = record[0]
        expirationTime: datetime

        if utils.isValidStr(expirationTimeString):
            expirationTime = datetime.fromisoformat(expirationTimeString)
        else:
            expirationTime = await self.__createExpiredExpirationTime()

        return TwitchTokensDetails(
            expirationTime = expirationTime,
            accessToken = record[1],
            refreshToken = record[2],
        )

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

    async def __insertOrUpdate(
        self,
        twitchChannelId: str,
        tokensDetails: TwitchTokensDetails,
    ):
        expirationTime = tokensDetails.expirationTime

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO twitchtokens (expirationtime, accesstoken, refreshtoken, twitchchannelid)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (twitchchannelid) DO UPDATE SET expirationtime = EXCLUDED.expirationtime, accesstoken = EXCLUDED.accesstoken, refreshtoken = EXCLUDED.refreshtoken
            ''',
            expirationTime.isoformat(), tokensDetails.accessToken, tokensDetails.refreshToken, twitchChannelId,
        )

        await connection.close()
        self.__timber.log('TwitchTokensStorage', f'Inserted or updated Twitch tokens details ({twitchChannelId=}) ({expirationTime=})')

    async def remove(
        self,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM twitchtokens
                WHERE twitchchannelid = $1
            ''',
            twitchChannelId,
        )

        await connection.close()
        self.__timber.log('TwitchTokensStorage', f'Removed Twitch tokens details ({twitchChannelId=})')

    async def set(
        self,
        twitchChannelId: str,
        tokensDetails: TwitchTokensDetails | None,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif tokensDetails is not None and not isinstance(tokensDetails, TwitchTokensDetails):
            raise TypeError(f'tokensDetails argument is malformed: \"{tokensDetails}\"')

        if tokensDetails is None:
            await self.remove(
                twitchChannelId = twitchChannelId,
            )
        else:
            await self.__insertOrUpdate(
                twitchChannelId = twitchChannelId,
                tokensDetails = tokensDetails,
            )

    async def updateExpirationTime(
        self,
        expirationTime: datetime,
        twitchChannelId: str,
    ):
        if not isinstance(expirationTime, datetime):
            raise TypeError(f'expirationTime argument is malformed: \"{expirationTime}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                UPDATE twitchtokens
                SET expirationtime = $1
                WHERE twitchchannelid = $2
            ''',
            expirationTime.isoformat(), twitchChannelId,
        )

        await connection.close()
        self.__timber.log('TwitchTokensStorage', f'Updated Twitch tokens expiration time ({expirationTime=}) ({twitchChannelId=})')
