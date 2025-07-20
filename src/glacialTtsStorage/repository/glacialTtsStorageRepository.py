from datetime import datetime
from typing import Final

import aiosqlite
from aiosqlite import Connection

from .glacialTtsStorageRepositoryInterface import GlacialTtsStorageRepositoryInterface
from ..idGenerator.glacialTtsIdGeneratorInterface import GlacialTtsIdGeneratorInterface
from ..mapper.glacialTtsDataMapperInterface import GlacialTtsDataMapperInterface
from ..models.glacialTtsData import GlacialTtsData
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.models.ttsProvider import TtsProvider


class GlacialTtsStorageRepository(GlacialTtsStorageRepositoryInterface):

    def __init__(
        self,
        glacialTtsDataMapper: GlacialTtsDataMapperInterface,
        glacialTtsIdGenerator: GlacialTtsIdGeneratorInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        databaseFile: str = '../db/glacialTtsStorageDatabase.sqlite',
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

        self.__glacialTtsDataMapper: Final[GlacialTtsDataMapperInterface] = glacialTtsDataMapper
        self.__glacialTtsIdGenerator: Final[GlacialTtsIdGeneratorInterface] = glacialTtsIdGenerator
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__databaseFile: Final[str] = databaseFile

        self.__isDatabaseReady: bool = False

    async def add(
        self,
        message: str,
        voice: str | None,
        provider: TtsProvider,
    ) -> GlacialTtsData:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif voice is not None and not isinstance(voice, str):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        glacialTtsData = await self.get(
            message = message,
            voice = voice,
            provider = provider,
        )

        if glacialTtsData is not None:
            self.__timber.log('GlacialTtsStorageRepository', f'Went to add a new TTS, but it\'s already been added ({glacialTtsData=})')
            return glacialTtsData

        storeDateTime = datetime.now(self.__timeZoneRepository.getDefault())

        glacialId = await self.__glacialTtsIdGenerator.generateId(
            message = message,
            voice = voice,
            provider = provider,
        )

        providerString = await self.__glacialTtsDataMapper.toDatabaseName(provider)
        connection = await self.__getDatabaseConnection()

        await connection.execute_insert(
            '''
                INSERT INTO glacialTtsStorage
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (glacialId, provider) DO NOTHING
            ''',
            ( storeDateTime.isoformat(), glacialId, message, providerString, voice, )
        )

        await connection.commit()
        await connection.close()

        glacialTtsData = GlacialTtsData(
            storeDateTime = storeDateTime,
            glacialId = glacialId,
            message = message,
            voice = voice,
            provider = provider,
        )

        return glacialTtsData

    async def get(
        self,
        message: str,
        voice: str | None,
        provider: TtsProvider,
    ) -> GlacialTtsData | None:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif voice is not None and not isinstance(voice, str):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        connection = await self.__getDatabaseConnection()
        providerString = await self.__glacialTtsDataMapper.toDatabaseName(provider)

        if utils.isValidStr(voice):
            cursor = await connection.execute(
                '''
                    SELECT storeDateTime, glacialId FROM glacialTtsStorage
                    WHERE message = $1 AND provider = $2 AND voice = $3
                    LIMIT 1
                ''',
                ( message, providerString, voice, )
            )
        else:
            cursor = await connection.execute(
                '''
                    SELECT storeDateTime, glacialId FROM glacialTtsStorage
                    WHERE message = $1 AND provider = $2 AND voice is NULL
                    LIMIT 1
                ''',
                ( message, providerString, )
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
                voice = voice,
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
                    voice TEXT DEFAULT NULL COLLATE NOCASE,
                    PRIMARY KEY (glacialId, provider)
                ) STRICT
            '''
        )

        await cursor.close()
        await connection.commit()
        return connection

    async def remove(
        self,
        glacialId: str,
        provider: TtsProvider,
    ) -> GlacialTtsData | None:
        if not utils.isValidStr(glacialId):
            raise TypeError(f'glacialId argument is malformed: \"{glacialId}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        providerString = await self.__glacialTtsDataMapper.toDatabaseName(provider)
        connection = await self.__getDatabaseConnection()

        cursor = await connection.execute(
            '''
                SELECT storeDateTime, message, voice FROM glacialTtsStorage
                WHERE glacialId = $1 AND provider = $2
                LIMIT 1
            ''',
            ( glacialId, providerString, )
        )

        row = await cursor.fetchone()
        await cursor.close()

        glacialTtsData: GlacialTtsData | None = None

        if row is not None and len(row) >= 1:
            storeDateTime = datetime.fromisoformat(row[0])

            glacialTtsData = GlacialTtsData(
                storeDateTime = storeDateTime,
                glacialId = glacialId,
                message = row[1],
                voice = row[2],
                provider = provider
            )

            await connection.execute(
                '''
                    DELETE FROM glacialTtsStorage
                    WHERE glacialId = $1 AND provider = $2
                ''',
                ( glacialId, providerString, )
            )

            await connection.commit()

        await connection.close()
        return glacialTtsData
