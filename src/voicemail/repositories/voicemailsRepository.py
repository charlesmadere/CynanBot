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

        # TODO
        raise RuntimeError(f'todo')

    async def getAllForOriginatingUser(
        self,
        originatingUserId: str,
        twitchChannelId: str
    ) -> FrozenList[VoicemailData]:
        if not utils.isValidStr(originatingUserId):
            raise TypeError(f'originatingUserId argument is malformed: \"{originatingUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        # TODO
        raise RuntimeError(f'todo')

    async def __getDatabaseConnection(self):
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

        # TODO
        raise RuntimeError(f'todo')

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
                            PRIMARY KEY (originatinguserid, targetuserid, twitchchannelid)
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
                            PRIMARY KEY (originatinguserid, targetuserid, twitchchannelid)
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

        # TODO
        raise RuntimeError(f'todo')
