import asyncio
import traceback
from datetime import datetime, timedelta
from typing import Any, Final

from .twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..api.models.twitchTokensDetails import TwitchTokensDetails
from ..api.models.twitchValidationResponse import TwitchValidationResponse
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..exceptions import (TwitchAccessTokenMissingException,
                          TwitchPasswordChangedException,
                          TwitchStatusCodeException)
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...network.exceptions import GenericNetworkException
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...storage.jsonReaderInterface import JsonReaderInterface
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TwitchTokensRepository(TwitchTokensRepositoryInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        seedFileReader: JsonReaderInterface | None = None,
        sleepTimeSeconds: float = 3300,
        tokensExpirationBuffer: timedelta = timedelta(minutes = 10),
        validationExpirationBuffer: timedelta = timedelta(minutes = 10),
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif seedFileReader is not None and not isinstance(seedFileReader, JsonReaderInterface):
            raise TypeError(f'seedFileReader argument is malformed: \"{seedFileReader}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise TypeError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 300 or sleepTimeSeconds > 3600:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not isinstance(tokensExpirationBuffer, timedelta):
            raise TypeError(f'tokensExpirationBuffer argument is malformed: \"{tokensExpirationBuffer}\"')
        elif not isinstance(validationExpirationBuffer, timedelta):
            raise TypeError(f'validationExpirationBuffer argument is malformed: \"{validationExpirationBuffer}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__seedFileReader: JsonReaderInterface | None = seedFileReader
        self.__sleepTimeSeconds: Final[float] = sleepTimeSeconds
        self.__tokensExpirationBuffer: Final[timedelta] = tokensExpirationBuffer
        self.__validationExpirationBuffer: Final[timedelta] = validationExpirationBuffer

        self.__isDatabaseReady: bool = False
        self.__isStarted: bool = False
        self.__cache: Final[dict[str, TwitchTokensDetails | None]] = dict()
        self.__twitchChannelIdToValidationTime: Final[dict[str, datetime | None]] = dict()

    async def addUser(
        self,
        code: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(code):
            raise TypeError(f'code argument is malformed: \"{code}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__timber.log('TwitchTokensRepository', f'Adding user ({twitchChannel=}) ({twitchChannelId=})...')

        try:
            tokensDetails = await self.__twitchApiService.fetchTokens(code = code)
        except GenericNetworkException as e:
            self.__timber.log('TwitchTokensRepository', f'Encountered network error when trying to add user ({twitchChannel=}) ({twitchChannelId=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchTokensRepository encountered network error when trying to add user ({twitchChannel=}) ({twitchChannelId=}): {e}')

        twitchChannelId = await self.__userIdsRepository.requireUserId(twitchChannel)

        await self.__setTokensDetails(
            twitchChannelId = twitchChannelId,
            tokensDetails = tokensDetails,
        )

    async def __areTokensDetailsCurrentlyValid(
        self,
        twitchChannelId: str,
        tokensDetails: TwitchTokensDetails | None,
    ) -> bool:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif tokensDetails is not None and not isinstance(tokensDetails, TwitchTokensDetails):
            raise TypeError(f'tokensDetails argument is malformed: \"{tokensDetails}\"')

        if tokensDetails is None:
            return False

        now = datetime.now(self.__timeZoneRepository.getDefault())
        if now + self.__tokensExpirationBuffer > tokensDetails.expirationTime:
            return False

        validationTime = self.__twitchChannelIdToValidationTime.get(twitchChannelId, None)
        if validationTime is None:
            return False

        return now + self.__validationExpirationBuffer <= validationTime

    async def __checkAndValidateTokensAsNecessary(self):
        self.__timber.log('TwitchTokensRepository', f'Checking if any Twitch tokens require validation...')

        now = datetime.now(self.__timeZoneRepository.getDefault())
        twitchChannelIds = frozenset(self.__twitchChannelIdToValidationTime.keys())
        twitchChannelIdsToValidate: set[str] = set()

        for twitchChannelId in twitchChannelIds:
            validationTime = self.__twitchChannelIdToValidationTime.get(twitchChannelId, None)

            if validationTime is None or now + self.__validationExpirationBuffer > validationTime:
                twitchChannelIdsToValidate.add(twitchChannelId)

        if len(twitchChannelIdsToValidate) == 0:
            return

        self.__timber.log('TwitchTokensRepository', f'Discovered {len(twitchChannelIdsToValidate)} Twitch token(s) that require validation...')

        for twitchChannelId in twitchChannelIds:
            tokensDetails = await self.getTokensDetailsById(twitchChannelId)

            if tokensDetails is None:
                self.__timber.log('TwitchTokensRepository', f'Twitch tokens details for \"{twitchChannelId}\" require validation, but unable to find any existing tokens details')
                continue

            await self.__validateAndRefreshAccessToken(
                twitchChannelId = twitchChannelId,
                tokensDetails = tokensDetails,
            )

        self.__timber.log('TwitchTokensRepository', f'Finished validation of {len(twitchChannelIdsToValidate)} Twitch token(s)')

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TwitchTokensRepository', 'Caches cleared')

    async def __consumeSeedFile(self):
        seedFileReader = self.__seedFileReader

        if seedFileReader is None:
            return

        self.__seedFileReader = None

        if not await seedFileReader.fileExistsAsync():
            self.__timber.log('TwitchTokensRepository', f'Seed file does not exist ({seedFileReader=})')
            return

        jsonContents: dict[str, dict[str, Any]] | Any | None = await seedFileReader.readJsonAsync()
        await seedFileReader.deleteFileAsync()

        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            self.__timber.log('TwitchTokensRepository', f'Seed file is empty ({seedFileReader=})')
            return

        self.__timber.log('TwitchTokensRepository', f'Reading in seed file... ({seedFileReader=})')

        for twitchChannel, tokensDetailsJson in jsonContents.items():
            if not utils.isValidStr(twitchChannel) or not isinstance(tokensDetailsJson, dict):
                self.__timber.log('TwitchTokensRepository', f'Encountered malformed data structure within seed file ({seedFileReader=}) ({twitchChannel=}) ({tokensDetailsJson=})')
                continue

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
                    refreshToken = utils.getStrFromDict(tokensDetailsJson, 'refreshToken'),
                )

            if tokensDetails is not None:
                twitchChannelId = await self.__userIdsRepository.requireUserId(twitchChannel)

                await self.__setTokensDetails(
                    twitchChannelId = twitchChannelId,
                    tokensDetails = tokensDetails,
                )

        self.__timber.log('TwitchTokensRepository', f'Finished reading in seed file ({seedFileReader=})')

    async def __createExpiredExpirationTime(self) -> datetime:
        nowDateTime = datetime.now(self.__timeZoneRepository.getDefault())
        return nowDateTime - timedelta(weeks = 1)

    async def __fetchTokensDetailsFromDatabase(
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
            twitchChannelId
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
            refreshToken = record[2],
        )

    async def getAccessToken(
        self,
        twitchChannel: str,
    ) -> str | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        twitchChannelId = await self.__userIdsRepository.fetchUserId(twitchChannel)

        if not utils.isValidStr(twitchChannelId):
            return None

        return await self.getAccessTokenById(twitchChannelId)

    async def getAccessTokenById(
        self,
        twitchChannelId: str,
    ) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        tokensDetails = await self.getTokensDetailsById(twitchChannelId)

        if tokensDetails is None:
            return None

        return tokensDetails.accessToken

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getTokensDetails(
        self,
        twitchChannel: str,
    ) -> TwitchTokensDetails | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        twitchChannelId = await self.__userIdsRepository.fetchUserId(twitchChannel)

        if not utils.isValidStr(twitchChannelId):
            return None

        return await self.getTokensDetailsById(twitchChannelId)

    async def getTokensDetailsById(
        self,
        twitchChannelId: str,
    ) -> TwitchTokensDetails | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        tokensDetails: TwitchTokensDetails | None

        if twitchChannelId in self.__cache:
            tokensDetails = self.__cache.get(twitchChannelId, None)

            if tokensDetails is None:
                self.__cache.pop(twitchChannelId, None)
        else:
            tokensDetails = await self.__fetchTokensDetailsFromDatabase(twitchChannelId)

        if tokensDetails is None:
            return None

        tokensDetails = await self.__validateAndRefreshAccessToken(
            twitchChannelId = twitchChannelId,
            tokensDetails = tokensDetails,
        )

        self.__cache[twitchChannelId] = tokensDetails
        return tokensDetails

    async def hasAccessToken(
        self,
        twitchChannel: str,
    ) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        twitchChannelId = await self.__userIdsRepository.fetchUserId(twitchChannel)

        if not utils.isValidStr(twitchChannelId):
            return False

        return await self.hasAccessTokenById(twitchChannelId)

    async def hasAccessTokenById(
        self,
        twitchChannelId: str,
    ) -> bool:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        accessToken = await self.getAccessTokenById(twitchChannelId)
        return utils.isValidStr(accessToken)

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
                    '''
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
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()
        await self.__consumeSeedFile()

    async def removeUser(
        self,
        twitchChannel: str,
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        twitchChannelId = await self.__userIdsRepository.requireUserId(twitchChannel)
        await self.removeUserById(twitchChannelId)

    async def removeUserById(
        self,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__timber.log('TwitchTokensRepository', f'Removing user \"{twitchChannelId}\"...')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM twitchtokens
                WHERE twitchchannelid = $1
            ''',
            twitchChannelId
        )

        await connection.close()
        self.__cache.pop(twitchChannelId, None)

    async def requireAccessToken(
        self,
        twitchChannel: str,
    ) -> str:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        accessToken = await self.getAccessToken(twitchChannel)

        if not utils.isValidStr(accessToken):
            raise TwitchAccessTokenMissingException(f'Twitch access token is missing ({twitchChannel=}) ({accessToken=})')

        return accessToken

    async def requireAccessTokenById(
        self,
        twitchChannelId: str,
    ) -> str:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        accessToken = await self.getAccessTokenById(twitchChannelId)

        if not utils.isValidStr(accessToken):
            raise TwitchAccessTokenMissingException(f'Twitch access token is missing ({twitchChannelId=}) ({accessToken=})')

        return accessToken

    async def __setExpirationTime(
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
            expirationTime.isoformat(), twitchChannelId
        )

        await connection.close()
        self.__cache.pop(twitchChannelId, None)

    async def __setTokensDetails(
        self,
        twitchChannelId: str,
        tokensDetails: TwitchTokensDetails | None,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif tokensDetails is not None and not isinstance(tokensDetails, TwitchTokensDetails):
            raise TypeError(f'tokenDetails argument is malformed: \"{tokensDetails}\"')

        connection = await self.__getDatabaseConnection()

        if tokensDetails is None:
            await connection.execute(
                '''
                    DELETE FROM twitchtokens
                    WHERE twitchchannelid = $1
                ''',
                twitchChannelId
            )

            self.__cache.pop(twitchChannelId, None)
            self.__timber.log('TwitchTokensRepository', f'Twitch tokens details have been deleted ({twitchChannelId=}) ({tokensDetails=})')
        else:
            expirationTime = tokensDetails.expirationTime

            await connection.execute(
                '''
                    INSERT INTO twitchtokens (expirationtime, accesstoken, refreshtoken, twitchchannelid)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (twitchchannelid) DO UPDATE SET expirationtime = EXCLUDED.expirationtime, accesstoken = EXCLUDED.accesstoken, refreshtoken = EXCLUDED.refreshtoken
                ''',
                expirationTime.isoformat(), tokensDetails.accessToken, tokensDetails.refreshToken, twitchChannelId
            )

            self.__cache[twitchChannelId] = tokensDetails
            self.__timber.log('TwitchTokensRepository', f'Twitch tokens details have been updated ({twitchChannelId=}) ({tokensDetails=})')

        await connection.close()

    def start(self):
        if self.__isStarted:
            self.__timber.log('TwitchTokensRepository', 'Not starting TwitchTokensRepository as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TwitchTokensRepository', 'Starting TwitchTokensRepository...')
        self.__backgroundTaskHelper.createTask(self.__startValidationLoop())

    async def __startValidationLoop(self):
        while True:
            await self.__checkAndValidateTokensAsNecessary()
            await asyncio.sleep(self.__sleepTimeSeconds)

    async def __validateAndRefreshAccessToken(
        self,
        twitchChannelId: str,
        tokensDetails: TwitchTokensDetails,
    ) -> TwitchTokensDetails:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(tokensDetails, TwitchTokensDetails):
            raise TypeError(f'tokensDetails argument is malformed: \"{tokensDetails}\"')

        nowDateTime = datetime.now(self.__timeZoneRepository.getDefault())

        if await self.__areTokensDetailsCurrentlyValid(
            twitchChannelId = twitchChannelId,
            tokensDetails = tokensDetails,
        ):
            return tokensDetails

        self.__timber.log('TwitchTokensRepository', f'Validating Twitch tokens for \"{twitchChannelId}\"...')
        self.__twitchChannelIdToValidationTime.pop(twitchChannelId, None)
        validationResponse: TwitchValidationResponse | None = None

        try:
            validationResponse = await self.__twitchApiService.validate(
                twitchAccessToken = tokensDetails.accessToken
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchTokensRepository', f'Encountered network error when trying to validate Twitch tokens ({twitchChannelId=}) ({tokensDetails=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchTokensRepository encountered network error when trying to validate Twitch tokens ({twitchChannelId=}) ({tokensDetails=}): {e}')
        except TwitchStatusCodeException:
            # this is an expected error
            pass

        if validationResponse is not None:
            self.__twitchChannelIdToValidationTime[twitchChannelId] = validationResponse.expiresAt

        if validationResponse is None or validationResponse.expiresAt + self.__tokensExpirationBuffer > nowDateTime:
            try:
                newTokensDetails = await self.__twitchApiService.refreshTokens(
                    twitchRefreshToken = tokensDetails.refreshToken,
                )
            except GenericNetworkException as e:
                self.__timber.log('TwitchTokensRepository', f'Encountered network error when trying to refresh Twitch tokens ({twitchChannelId=}): {e}', e, traceback.format_exc())
                raise GenericNetworkException(f'TwitchTokensRepository encountered network error when trying to refresh Twitch tokens ({twitchChannelId=}): {e}')
            except TwitchPasswordChangedException as e:
                self.__timber.log('TwitchTokensRepository', f'Encountered network error caused by password change when trying to refresh Twitch tokens ({twitchChannelId=}): {e}', e, traceback.format_exc())
                await self.removeUserById(twitchChannelId)
                raise TwitchPasswordChangedException(f'TwitchTokensRepository encountered network error caused by password change when trying to refresh Twitch tokens ({twitchChannelId=}): {e}')

            await self.__setTokensDetails(
                twitchChannelId = twitchChannelId,
                tokensDetails = newTokensDetails,
            )

            return newTokensDetails

        await self.__setExpirationTime(
            expirationTime = validationResponse.expiresAt,
            twitchChannelId = twitchChannelId,
        )

        return TwitchTokensDetails(
            expirationTime = validationResponse.expiresAt,
            accessToken = tokensDetails.accessToken,
            refreshToken = tokensDetails.refreshToken,
        )
