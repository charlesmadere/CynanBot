import traceback
from datetime import datetime, timedelta
from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.api.twitchTokensDetails import TwitchTokensDetails
from CynanBot.twitch.exceptions import (NoTwitchTokenDetailsException,
                                        TwitchPasswordChangedException)
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface


class TwitchTokensRepository(TwitchTokensRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        seedFileReader: JsonReaderInterface | None = None,
        tokensExpirationBuffer: timedelta = timedelta(minutes = 10)
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif seedFileReader is not None and not isinstance(seedFileReader, JsonReaderInterface):
            raise TypeError(f'seedFileReader argument is malformed: \"{seedFileReader}\"')
        elif not isinstance(tokensExpirationBuffer, timedelta):
            raise TypeError(f'tokensExpirationBuffer argument is malformed: \"{tokensExpirationBuffer}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__seedFileReader: JsonReaderInterface | None = seedFileReader
        self.__tokensExpirationBuffer: timedelta = tokensExpirationBuffer

        self.__isDatabaseReady: bool = False
        self.__cache: dict[str, TwitchTokensDetails | None] = dict()

    async def addUser(self, code: str, twitchChannel: str):
        if not utils.isValidStr(code):
            raise TypeError(f'code argument is malformed: \"{code}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__timber.log('TwitchTokensRepository', f'Adding user \"{twitchChannel}\"...')

        try:
            tokensDetails = await self.__twitchApiService.fetchTokens(code = code)
        except GenericNetworkException as e:
            self.__timber.log('TwitchTokensRepository', f'Encountered network error when trying to add user \"{twitchChannel}\": {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchTokensRepository encountered network error when trying to add user \"{twitchChannel}\": {e}')

        await self.__setTokensDetails(
            twitchChannel = twitchChannel,
            tokensDetails = tokensDetails
        )

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TwitchTokensRepository', 'Caches cleared')

    async def __consumeSeedFile(self):
        seedFileReader = self.__seedFileReader

        if seedFileReader is None:
            return

        self.__seedFileReader = None

        if not await seedFileReader.fileExistsAsync():
            self.__timber.log('TwitchTokensRepository', f'Seed file (\"{seedFileReader}\") does not exist')
            return

        jsonContents: dict[str, dict[str, Any]] | None = await seedFileReader.readJsonAsync()
        await seedFileReader.deleteFileAsync()

        if jsonContents is None or len(jsonContents) == 0:
            self.__timber.log('TwitchTokensRepository', f'Seed file (\"{seedFileReader}\") is empty')
            return

        self.__timber.log('TwitchTokensRepository', f'Reading in seed file \"{seedFileReader}\"...')

        for twitchChannel, tokensDetailsJson in jsonContents.items():
            tokensDetails: TwitchTokensDetails | None = None

            if utils.isValidStr(tokensDetailsJson.get('code')):
                code = utils.getStrFromDict(tokensDetailsJson, 'code')

                try:
                    tokensDetails = await self.__twitchApiService.fetchTokens(code)
                except GenericNetworkException as e:
                    self.__timber.log('TwitchTokensRepository', f'Unable to fetch tokens for \"{twitchChannel}\" with code \"{code}\": {e}', e, traceback.format_exc())
            else:
                tokensDetails = TwitchTokensDetails(
                    expirationTime = await self.__createExpiredExpirationTime(),
                    accessToken = utils.getStrFromDict(tokensDetailsJson, 'accessToken'),
                    refreshToken = utils.getStrFromDict(tokensDetailsJson, 'refreshToken')
                )

            if tokensDetails is not None:
                await self.__setTokensDetails(
                    twitchChannel = twitchChannel,
                    tokensDetails = tokensDetails
                )

        self.__timber.log('TwitchTokensRepository', f'Finished reading in seed file \"{seedFileReader}\"')

    async def __createExpiredExpirationTime(self) -> datetime:
        nowDateTime = datetime.now(self.__timeZoneRepository.getDefault())
        return nowDateTime - timedelta(weeks = 1)

    async def __fetchTokensDetailsFromDatabase(self, twitchChannel: str) -> TwitchTokensDetails | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT expirationtime, accesstoken, refreshtoken FROM twitchtokens
                WHERE twitchchannel = $1
                LIMIT 1
            ''',
            twitchChannel
        )

        await connection.close()

        if record is None or len(record) == 0:
            return None

        expirationTime = datetime.fromisoformat(record[0])

        if expirationTime is None:
            expirationTime = await self.__createExpiredExpirationTime()

        return TwitchTokensDetails(
            expirationTime = expirationTime,
            accessToken = record[1],
            refreshToken = record[2]
        )

    async def getAccessToken(self, twitchChannel: str) -> str | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        tokensDetails = await self.getTokensDetails(twitchChannel)

        if tokensDetails is None:
            return None

        return tokensDetails.accessToken

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getRefreshToken(self, twitchChannel: str) -> str | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        tokensDetails = await self.getTokensDetails(twitchChannel)

        if tokensDetails is None:
            return None

        return tokensDetails.refreshToken

    async def getTokensDetails(self, twitchChannel: str) -> TwitchTokensDetails | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        tokensDetails: TwitchTokensDetails | None = None

        if twitchChannel.lower() in self.__cache:
            tokensDetails = self.__cache.get(twitchChannel.lower(), None)
        else:
            tokensDetails = await self.__fetchTokensDetailsFromDatabase(
                twitchChannel = twitchChannel
            )

        if tokensDetails is None:
            self.__cache[twitchChannel.lower()] = None
            return None

        tokensDetails = await self.__validateAndRefreshAccessToken(
            twitchChannel = twitchChannel,
            tokensDetails = tokensDetails
        )

        self.__cache[twitchChannel.lower()] = tokensDetails
        return tokensDetails

    async def hasAccessToken(self, twitchChannel: str) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        accessToken = await self.getAccessToken(twitchChannel)
        return utils.isValidStr(accessToken)

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS twitchtokens (
                        expirationtime text DEFAULT NULL,
                        accesstoken text NOT NULL,
                        refreshtoken text NOT NULL,
                        twitchchannel public.citext NOT NULL PRIMARY KEY
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS twitchtokens (
                        expirationtime TEXT DEFAULT NULL,
                        accesstoken TEXT NOT NULL,
                        refreshtoken TEXT NOT NULL,
                        twitchchannel TEXT NOT NULL PRIMARY KEY COLLATE NOCASE
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()
        await self.__consumeSeedFile()

    async def removeUser(self, twitchChannel: str):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__timber.log('TwitchTokensRepository', f'Removing user \"{twitchChannel}\"...')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM twitchtokens
                WHERE twitchchannel = $1
            ''',
            twitchChannel
        )

        await connection.close()
        self.__cache.pop(twitchChannel.lower(), None)

    async def requireAccessToken(self, twitchChannel: str) -> str:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        accessToken = await self.getAccessToken(twitchChannel)

        if not utils.isValidStr(accessToken):
            raise ValueError(f'\"accessToken\" value for \"{twitchChannel}\" is malformed: \"{accessToken}\"')

        return accessToken

    async def requireRefreshToken(self, twitchChannel: str) -> str:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        refreshToken = await self.getRefreshToken(twitchChannel)

        if not utils.isValidStr(refreshToken):
            raise ValueError(f'\"refreshToken\" value for \"{twitchChannel}\" is malformed: \"{refreshToken}\"')

        return refreshToken

    async def requireTokensDetails(self, twitchChannel: str) -> TwitchTokensDetails:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        tokensDetails = await self.getTokensDetails(twitchChannel)

        if tokensDetails is None:
            raise NoTwitchTokenDetailsException(f'Twitch tokens details for \"{twitchChannel}\" is missing/unavailable')

        return tokensDetails

    async def __setExpirationTime(
        self,
        expirationTime: datetime,
        twitchChannel: str
    ):
        if not isinstance(expirationTime, datetime):
            raise TypeError(f'expirationTime argument is malformed: \"{expirationTime}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                UPDATE twitchtokens
                SET expirationtime = $1
                WHERE twitchchannel = $2
            ''',
            expirationTime.isoformat(), twitchChannel
        )

        await connection.close()
        self.__cache.pop(twitchChannel.lower(), None)

    async def __setTokensDetails(
        self,
        twitchChannel: str,
        tokensDetails: TwitchTokensDetails | None,
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif tokensDetails is not None and not isinstance(tokensDetails, TwitchTokensDetails):
            raise TypeError(f'tokenDetails argument is malformed: \"{tokensDetails}\"')

        connection = await self.__getDatabaseConnection()

        if tokensDetails is None:
            await connection.execute(
                '''
                    DELETE FROM twitchtokens
                    WHERE twitchchannel = $1
                ''',
                twitchChannel
            )

            self.__cache.pop(twitchChannel.lower(), None)
            self.__timber.log('TwitchTokensRepository', f'Twitch tokens details have been deleted ({twitchChannel=}) ({tokensDetails=})')
        else:
            expirationTime = tokensDetails.expirationTime

            await connection.execute(
                '''
                    INSERT INTO twitchtokens (expirationtime, accesstoken, refreshtoken, twitchchannel)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (twitchchannel) DO UPDATE SET expirationtime = EXCLUDED.expirationtime, accesstoken = EXCLUDED.accesstoken, refreshtoken = EXCLUDED.refreshtoken
                ''',
                expirationTime.isoformat(), tokensDetails.accessToken, tokensDetails.refreshToken, twitchChannel
            )

            self.__cache[twitchChannel.lower()] = tokensDetails
            self.__timber.log('TwitchTokensRepository', f'Twitch tokens details have been updated ({twitchChannel=}) ({tokensDetails=})')

        await connection.close()

    async def __validateAndRefreshAccessToken(
        self,
        twitchChannel: str,
        tokensDetails: TwitchTokensDetails
    ) -> TwitchTokensDetails:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not isinstance(tokensDetails, TwitchTokensDetails):
            raise TypeError(f'tokensDetails argument is malformed: \"{tokensDetails}\"')

        nowDateTime = datetime.now(self.__timeZoneRepository.getDefault())

        if nowDateTime + self.__tokensExpirationBuffer <= tokensDetails.expirationTime:
            self.__timber.log('TwitchTokensRepository', f'Twitch tokens for \"{twitchChannel}\" don\'t need to be validated and refreshed yet ({tokensDetails.expirationTime=})')
            return tokensDetails

        self.__timber.log('TwitchTokensRepository', f'Validating Twitch tokens for \"{twitchChannel}\"...')
        expirationTime: datetime | None = None

        try:
            expirationTime = await self.__twitchApiService.validateTokens(
                twitchAccessToken = tokensDetails.accessToken
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchTokensRepository', f'Encountered network error when trying to validate Twitch tokens for \"{twitchChannel}\" ({tokensDetails=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchTokensRepository encountered network error when trying to validate Twitch tokens for \"{twitchChannel}\" ({tokensDetails=}): {e}')

        if expirationTime is None or expirationTime + self.__tokensExpirationBuffer > nowDateTime:
            try:
                newTokensDetails = await self.__twitchApiService.refreshTokens(
                    twitchRefreshToken = tokensDetails.refreshToken
                )
            except GenericNetworkException as e:
                self.__timber.log('TwitchTokensRepository', f'Encountered network error when trying to refresh Twitch tokens for \"{twitchChannel}\": {e}', e, traceback.format_exc())
                raise GenericNetworkException(f'TwitchTokensRepository encountered network error when trying to refresh Twitch tokens for \"{twitchChannel}\": {e}')
            except TwitchPasswordChangedException as e:
                self.__timber.log('TwitchTokensRepository', f'Encountered network error caused by password change when trying to refresh Twitch tokens for \"{twitchChannel}\": {e}', e, traceback.format_exc())
                await self.removeUser(twitchChannel)
                raise TwitchPasswordChangedException(f'TwitchTokensRepository encountered network error caused by password change when trying to refresh Twitch tokens for \"{twitchChannel}\": {e}')

            await self.__setTokensDetails(
                twitchChannel = twitchChannel,
                tokensDetails = newTokensDetails
            )

            return newTokensDetails

        await self.__setExpirationTime(
            expirationTime = expirationTime,
            twitchChannel = twitchChannel
        )

        return TwitchTokensDetails(
            expirationTime = expirationTime,
            accessToken = tokensDetails.accessToken,
            refreshToken = tokensDetails.refreshToken
        )
