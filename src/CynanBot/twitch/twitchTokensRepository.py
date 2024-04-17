import traceback
from datetime import datetime, timedelta, timezone, tzinfo
from typing import Any

import CynanBot.misc.utils as utils
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
from CynanBot.twitch.twitchTokensRepositoryListener import \
    TwitchTokensRepositoryListener


class TwitchTokensRepository(TwitchTokensRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        seedFileReader: JsonReaderInterface | None = None,
        tokensExpirationBuffer: timedelta = timedelta(minutes = 10),
        timeZone: tzinfo = timezone.utc
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif seedFileReader is not None and not isinstance(seedFileReader, JsonReaderInterface):
            raise TypeError(f'seedFileReader argument is malformed: \"{seedFileReader}\"')
        elif not isinstance(tokensExpirationBuffer, timedelta):
            raise TypeError(f'tokensExpirationBuffer argument is malformed: \"{tokensExpirationBuffer}\"')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__seedFileReader: JsonReaderInterface | None = seedFileReader
        self.__tokensExpirationBuffer: timedelta = tokensExpirationBuffer
        self.__timeZone: tzinfo = timeZone

        self.__isDatabaseReady: bool = False
        self.__cache: dict[str, TwitchTokensDetails] = dict()
        self.__twitchTokensRepositoryListener: TwitchTokensRepositoryListener | None = None

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
            tokensDetails = tokensDetails,
            twitchChannel = twitchChannel
        )

        twitchTokensRepositoryListener = self.__twitchTokensRepositoryListener

        if twitchTokensRepositoryListener is not None:
            if tokensDetails is None:
                await twitchTokensRepositoryListener.onUserRemoved(
                    twitchChannel = twitchChannel
                )
            else:
                await twitchTokensRepositoryListener.onUserAdded(
                    tokensDetails = tokensDetails,
                    twitchChannel = twitchChannel
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
                    tokensDetails = tokensDetails,
                    twitchChannel = twitchChannel
                )

        self.__timber.log('TwitchTokensRepository', f'Finished reading in seed file \"{seedFileReader}\"')

    async def __createExpiredExpirationTime(self) -> datetime:
        nowDateTime = datetime.now(self.__timeZone)
        return nowDateTime - timedelta(weeks = 1)

    async def getAccessToken(self, twitchChannel: str) -> str | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        tokensDetails = await self.getTokensDetails(twitchChannel)

        if tokensDetails is None:
            return None

        return tokensDetails.getAccessToken()

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getRefreshToken(self, twitchChannel: str) -> str | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        tokensDetails = await self.getTokensDetails(twitchChannel)

        if tokensDetails is None:
            return None

        return tokensDetails.getRefreshToken()

    async def getTokensDetails(self, twitchChannel: str) -> TwitchTokensDetails | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        if twitchChannel.lower() in self.__cache:
            return self.__cache[twitchChannel.lower()]

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

        if not utils.hasItems(record):
            self.__cache.pop(twitchChannel.lower(), None)
            return None

        expirationTime = utils.getDateTimeFromStr(record[0])

        if expirationTime is None:
            expirationTime = await self.__createExpiredExpirationTime()

        tokensDetails = TwitchTokensDetails(
            expirationTime = expirationTime,
            accessToken = record[1],
            refreshToken = record[2]
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

    async def __refreshTokensDetails(
        self,
        twitchChannel: str,
        tokensDetails: TwitchTokensDetails
    ):
        if not isinstance(tokensDetails, TwitchTokensDetails):
            raise TypeError(f'tokenDetails argument is malformed: \"{tokensDetails}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__timber.log('TwitchTokensRepository', f'Refreshing Twitch tokens for \"{twitchChannel}\"...')

        try:
            newTokensDetails = await self.__twitchApiService.refreshTokens(
                twitchRefreshToken = tokensDetails.getRefreshToken()
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchTokensRepository', f'Encountered network error when trying to refresh Twitch tokens for \"{twitchChannel}\": {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchTokensRepository encountered network error when trying to refresh Twitch tokens for \"{twitchChannel}\": {e}')
        except TwitchPasswordChangedException as e:
            self.__timber.log('TwitchTokensRepository', f'Encountered network error caused by password change when trying to refresh Twitch tokens for \"{twitchChannel}\": {e}', e, traceback.format_exc())
            await self.removeUser(twitchChannel)
            raise TwitchPasswordChangedException(f'TwitchTokensRepository encountered network error caused by password change when trying to refresh Twitch tokens for \"{twitchChannel}\": {e}')

        await self.__setTokensDetails(
            tokensDetails = newTokensDetails,
            twitchChannel = twitchChannel
        )

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

        twitchTokensRepositoryListener = self.__twitchTokensRepositoryListener

        if twitchTokensRepositoryListener is not None:
            await twitchTokensRepositoryListener.onUserRemoved(
                twitchChannel = twitchChannel
            )

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

    def setListener(self, listener: TwitchTokensRepositoryListener | None):
        if listener is not None and not isinstance(listener, TwitchTokensRepositoryListener):
            raise TypeError(f'listener argument is malformed: \"{listener}\"')

        self.__twitchTokensRepositoryListener = listener

    async def __setTokensDetails(
        self,
        tokensDetails: TwitchTokensDetails | None,
        twitchChannel: str
    ):
        if tokensDetails is not None and not isinstance(tokensDetails, TwitchTokensDetails):
            raise TypeError(f'tokenDetails argument is malformed: \"{tokensDetails}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

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
            self.__timber.log('TwitchTokensRepository', f'Twitch tokens details for \"{twitchChannel}\" has been deleted')
        else:
            expirationTime = tokensDetails.getExpirationTime()

            await connection.execute(
                '''
                    INSERT INTO twitchtokens (expirationtime, accesstoken, refreshtoken, twitchchannel)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (twitchchannel) DO UPDATE SET expirationtime = EXCLUDED.expirationtime, accesstoken = EXCLUDED.accesstoken, refreshtoken = EXCLUDED.refreshtoken
                ''',
                expirationTime.isoformat(), tokensDetails.getAccessToken(), tokensDetails.getRefreshToken(), twitchChannel
            )

            self.__cache[twitchChannel.lower()] = tokensDetails
            self.__timber.log('TwitchTokensRepository', f'Twitch tokens details for \"{twitchChannel}\" has been updated ({tokensDetails})')

        await connection.close()

    async def validateAndRefreshAccessToken(self, twitchChannel: str):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        tokensDetails = await self.getTokensDetails(twitchChannel)
        if tokensDetails is None:
            self.__timber.log('TwitchTokensRepository', f'Attempted to validate Twitch tokens for \"{twitchChannel}\", but tokens details are missing/unavailable')
            return

        nowDateTime = datetime.now(self.__timeZone)

        if tokensDetails.getExpirationTime() + self.__tokensExpirationBuffer <= nowDateTime:
            self.__timber.log('TwitchTokensRepository', f'Validated Twitch tokens for \"{twitchChannel}\", they don\'t need to be refreshed yet ({tokensDetails.getExpirationTime()=})')
            return

        self.__timber.log('TwitchTokensRepository', f'Validating Twitch tokens for \"{twitchChannel}\"...')

        expirationTime: datetime | None = None
        try:
            expirationTime = await self.__twitchApiService.validateTokens(
                twitchAccessToken = tokensDetails.getAccessToken()
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchTokensRepository', f'Encountered network error when trying to validate Twitch tokens for \"{twitchChannel}\": {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchTokensRepository encountered network error when trying to validate Twitch tokens for \"{twitchChannel}\": {e}')

        if expirationTime is not None and expirationTime > nowDateTime + self.__tokensExpirationBuffer:
            await self.__setExpirationTime(
                expirationTime = expirationTime,
                twitchChannel = twitchChannel
            )
        else:
            await self.__refreshTokensDetails(
                twitchChannel = twitchChannel,
                tokensDetails = tokensDetails
            )
