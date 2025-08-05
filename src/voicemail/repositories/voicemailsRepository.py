from collections import defaultdict
from datetime import datetime
from typing import Final

from frozenlist import FrozenList

from .voicemailsRepositoryInterface import VoicemailsRepositoryInterface
from ..idGenerator.voicemailIdGeneratorInterface import VoicemailIdGeneratorInterface
from ..models.addVoicemailResult import AddVoicemailResult
from ..models.removeVoicemailResult import RemoveVoicemailResult
from ..models.voicemailData import VoicemailData
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class VoicemailsRepository(VoicemailsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        voicemailIdGenerator: VoicemailIdGeneratorInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(voicemailIdGenerator, VoicemailIdGeneratorInterface):
            raise TypeError(f'voicemailIdGenerator argument is malformed: \"{voicemailIdGenerator}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__voicemailIdGenerator: Final[VoicemailIdGeneratorInterface] = voicemailIdGenerator

        self.__isDatabaseReady: bool = False
        self.__cache: dict[str, dict[str, FrozenList[VoicemailData] | None]] = defaultdict(lambda: dict())

    async def addVoicemail(
        self,
        message: str,
        originatingUserId: str,
        targetUserId: str,
        twitchChannelId: str
    ) -> AddVoicemailResult:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(originatingUserId):
            raise TypeError(f'originatingUserId argument is malformed: \"{originatingUserId}\"')
        elif not utils.isValidStr(targetUserId):
            raise TypeError(f'targetUserId argument is malformed: \"{targetUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__cache[twitchChannelId].pop(targetUserId, None)

        connection = await self.__getDatabaseConnection()
        now = datetime.now(self.__timeZoneRepository.getDefault())
        voicemailId = await self.__generateNewVoicemailId(connection)

        await connection.execute(
            '''
                INSERT INTO voicemails (createddatetime, message, originatinguserid, targetuserid, twitchchannelid, voicemailid)
                VALUES ($1, $2, $3, $4, $5, $6)
            ''',
            now.isoformat(), message, originatingUserId, targetUserId, twitchChannelId, voicemailId
        )

        await connection.close()
        self.__timber.log('VoicemailsRepository', f'Added new voicemail ({originatingUserId=}) ({targetUserId=}) ({twitchChannelId=}) ({voicemailId=})')

        return AddVoicemailResult.OK

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('VoicemailsRepository', 'Caches cleared')

    async def __generateNewVoicemailId(self, connection: DatabaseConnection) -> str:
        newVoicemailId: str | None = None

        while not utils.isValidStr(newVoicemailId):
            newVoicemailId = await self.__voicemailIdGenerator.generateVoicemailId()

            record = await connection.fetchRow(
                '''
                    SELECT COUNT(1) FROM voicemails
                    WHERE voicemailid = $1
                    LIMIT 1
                ''',
                newVoicemailId
            )

            count: int | None = None
            if record is not None and len(record) >= 1:
                count = record[0]

            if not utils.isValidInt(count) or count == 1:
                newVoicemailId = None

        return newVoicemailId

    async def getAllForOriginatingUser(
        self,
        originatingUserId: str,
        twitchChannelId: str
    ) -> FrozenList[VoicemailData]:
        if not utils.isValidStr(originatingUserId):
            raise TypeError(f'originatingUserId argument is malformed: \"{originatingUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        cachedVoicemails = self.__cache[twitchChannelId].get(originatingUserId, None)
        if cachedVoicemails is not None:
            return cachedVoicemails

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT createddatetime, message, targetuserid, voicemailid FROM voicemails
                WHERE originatinguserid = $1 AND twitchchannelid = $2
                ORDER BY createddatetime ASC
            ''',
            originatingUserId, twitchChannelId
        )

        await connection.close()
        voicemails: FrozenList[VoicemailData] = FrozenList()
        self.__cache[twitchChannelId][originatingUserId] = voicemails

        if records is None or len(records) == 0:
            voicemails.freeze()
            return voicemails

        for record in records:
            voicemails.append(VoicemailData(
                createdDateTime = datetime.fromisoformat(record[0]),
                message = record[1],
                originatingUserId = originatingUserId,
                targetUserId = record[2],
                twitchChannelId = twitchChannelId,
                voicemailId = record[3]
            ))

        voicemails.freeze()
        return voicemails

    async def getAllForTargetUser(
        self,
        targetUserId: str,
        twitchChannelId: str
    ) -> FrozenList[VoicemailData]:
        if not utils.isValidStr(targetUserId):
            raise TypeError(f'targetUserId argument is malformed: \"{targetUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        cachedVoicemails = self.__cache[twitchChannelId].get(targetUserId, None)
        if cachedVoicemails is not None:
            return cachedVoicemails

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT createddatetime, message, originatinguserid, voicemailid FROM voicemails
                WHERE targetuserid = $1 AND twitchchannelid = $2
                ORDER BY createddatetime ASC
            ''',
            targetUserId, twitchChannelId
        )

        await connection.close()
        voicemails: FrozenList[VoicemailData] = FrozenList()
        self.__cache[twitchChannelId][targetUserId] = voicemails

        if records is None or len(records) == 0:
            voicemails.freeze()
            return voicemails

        for record in records:
            voicemails.append(VoicemailData(
                createdDateTime = datetime.fromisoformat(record[0]),
                message = record[1],
                originatingUserId = record[2],
                targetUserId = targetUserId,
                twitchChannelId = twitchChannelId,
                voicemailId = record[3]
            ))

        voicemails.freeze()
        return voicemails

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getForTargetUser(
        self,
        targetUserId: str,
        twitchChannelId: str
    ) -> VoicemailData | None:
        if not utils.isValidStr(targetUserId):
            raise TypeError(f'targetUserId argument is malformed: \"{targetUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        allForTargetUser = await self.getAllForTargetUser(
            targetUserId = targetUserId,
            twitchChannelId = twitchChannelId
        )

        if len(allForTargetUser) == 0:
            return None
        else:
            return allForTargetUser[0]

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS voicemails (
                            createddatetime text NOT NULL,
                            message text NOT NULL,
                            originatinguserid text NOT NULL,
                            targetuserid text NOT NULL,
                            twitchchannelid text NOT NULL,
                            voicemailid text NOT NULL,
                            PRIMARY KEY (originatinguserid, targetuserid, twitchchannelid, voicemailid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS voicemails (
                            createddatetime TEXT NOT NULL,
                            message TEXT NOT NULL,
                            originatinguserid TEXT NOT NULL,
                            targetuserid TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            voicemailid TEXT NOT NULL,
                            PRIMARY KEY (originatinguserid, targetuserid, twitchchannelid, voicemailid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def removeVoicemail(
        self,
        twitchChannelId: str,
        voicemailId: str
    ) -> RemoveVoicemailResult:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(voicemailId):
            raise TypeError(f'voicemailId argument is malformed: \"{voicemailId}\"')

        self.__cache.pop(twitchChannelId, None)

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT COUNT(1) FROM voicemails
                WHERE twitchchannelid = $1 AND voicemailid = $2
                LIMIT 1
            ''',
            twitchChannelId, voicemailId
        )

        count: int | None = None
        if record is not None and len(record) >= 1:
            count = record[0]

        if not utils.isValidInt(count) or count == 0:
            await connection.close()
            return RemoveVoicemailResult.NOT_FOUND

        await connection.execute(
            '''
                DELETE FROM voicemails
                WHERE twitchchannelid = $1 AND voicemailid = $2
            ''',
            twitchChannelId, voicemailId
        )

        await connection.close()
        self.__timber.log('VoicemailsRepository', f'Deleted voicemail ({twitchChannelId=}) ({voicemailId=})')

        return RemoveVoicemailResult.OK
