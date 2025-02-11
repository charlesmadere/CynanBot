from datetime import datetime

import aiosqlite
from aiosqlite import Connection

from .glacialTtsStorageRepositoryInterface import GlacialTtsStorageRepositoryInterface
from ..idGenerator.glacialTtsIdGeneratorInterface import GlacialTtsIdGeneratorInterface
from ..mapper.glacialTtsDataMapperInterface import GlacialTtsDataMapperInterface
from ..models.glacialTtsData import GlacialTtsData
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.ttsProvider import TtsProvider


class GlacialTtsStorageRepository(GlacialTtsStorageRepositoryInterface):

    def __init__(
        self,
        glacialTtsDataMapper: GlacialTtsDataMapperInterface,
        glacialTtsIdGenerator: GlacialTtsIdGeneratorInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        databaseFile: str = '../db/glacialTtsStorageDatabase.sqlite'
    ):
        if not isinstance(glacialTtsDataMapper, GlacialTtsDataMapperInterface):
            raise TypeError(f'glacialTtsDataMapper argument is malformed: \"{glacialTtsDataMapper}\"')
        elif not isinstance(glacialTtsIdGenerator, GlacialTtsIdGeneratorInterface):
            raise TypeError(f'glacialTtsIdGenerator argument is malformed: \"{glacialTtsIdGenerator}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidStr(databaseFile):
            raise TypeError(f'databaseFile argument is malformed: \"{databaseFile}\"')

        self.__glacialTtsDataMapper: GlacialTtsDataMapperInterface = glacialTtsDataMapper
        self.__glacialTtsIdGenerator: GlacialTtsIdGeneratorInterface = glacialTtsIdGenerator
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__databaseFile: str = databaseFile

        self.__isDatabaseReady: bool = False

    async def add(
        self,
        message: str,
        provider: TtsProvider
    ) -> GlacialTtsData:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        glacialTtsData = await self.get(
            message = message,
            provider = provider
        )

        if glacialTtsData is not None:
            self.__timber.log('GlacialTtsStorageRepository', f'Went to add a new TTS, but it\'s already been added ({glacialTtsData=})')
            return glacialTtsData

        storeDateTime = datetime.now(self.__timeZoneRepository.getDefault())

        glacialId = await self.__glacialTtsIdGenerator.generateId(
            message = message,
            provider = provider
        )

        providerString = await self.__glacialTtsDataMapper.toDatabaseName(provider)
        connection = await self.__getDatabaseConnection()

        cursor = await connection.execute(
            '''
                INSERT INTO glacialTtsStorage
                VALUES ($1, $2, $3, $4)
            ''',
            ( storeDateTime.isoformat(), glacialId, message, providerString  )
        )

        await cursor.close()
        await connection.close()

        glacialTtsData = GlacialTtsData(
            storeDateTime = storeDateTime,
            glacialId = glacialId,
            message = message,
            provider = provider
        )

        return glacialTtsData

    async def get(
        self,
        message: str,
        provider: TtsProvider
    ) -> GlacialTtsData | None:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        connection = await self.__getDatabaseConnection()
        providerString = await self.__glacialTtsDataMapper.toDatabaseName(provider)

        cursor = await connection.execute(
            '''
                SELECT storeDateTime, glacialId FROM glacialTtsStorage
                WHERE message = $1 AND provider = $2
                LIMIT 1
            ''',
            ( message, providerString )
        )

        row = await cursor.fetchone()
        await cursor.close()

        glacialTtsData: GlacialTtsData | None = None

        if row is not None and len(row) >= 1:
            storeDateTime = datetime.fromisoformat(row[0])

            glacialTtsData = GlacialTtsData(
                storeDateTime = storeDateTime,
                glacialId = row[1],
                message = message,
                provider = provider
            )

        await connection.close()
        return glacialTtsData

    async def __getDatabaseConnection(self) -> Connection:
        connection = await aiosqlite.connect(self.__databaseFile)

        if self.__isDatabaseReady:
            return connection

        self.__isDatabaseReady = True

        cursor = await connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS glacialTtsStorage (
                    storeDateTime TEXT NOT NULL,
                    glacialId TEXT NOT NULL,
                    message TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    PRIMARY KEY (glacialId)
                )
            '''
        )

        await cursor.close()
        return connection

    async def remove(
        self,
        glacialId: str
    ) -> GlacialTtsData | None:
        if not utils.isValidStr(glacialId):
            raise TypeError(f'glacialId argument is malformed: \"{glacialId}\"')

        connection = await self.__getDatabaseConnection()

        cursor = await connection.execute(
            '''
                SELECT storeDateTime, message, provider FROM glacialTtsStorage
                WHERE glacialId = $2
                LIMIT 1
            ''',
            ( glacialId, )
        )

        row = await cursor.fetchone()
        await cursor.close()

        glacialTtsData: GlacialTtsData | None = None

        if row is not None and len(row) >= 1:
            storeDateTime = datetime.fromisoformat(row[0])
            provider = await self.__glacialTtsDataMapper.fromDatabaseName(row[2])

            glacialTtsData = GlacialTtsData(
                storeDateTime = storeDateTime,
                glacialId = glacialId,
                message = row[1],
                provider = provider
            )

            await connection.execute(
                '''
                    DELETE FROM glacialTtsStorage
                    WHERE glacialId = $1
                ''',
                ( glacialId, )
            )

        await connection.close()
        return glacialTtsData
