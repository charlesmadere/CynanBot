import asyncio
import traceback
from datetime import datetime, timedelta
from typing import Any, Final

from .twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from .twitchTokensStorageInterface import TwitchTokensStorageInterface
from ..api.models.twitchTokensDetails import TwitchTokensDetails
from ..api.models.twitchValidationResponse import TwitchValidationResponse
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..exceptions import TwitchAccessTokenMissingException, TwitchPasswordChangedException, TwitchStatusCodeException
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...network.exceptions import GenericNetworkException
from ...storage.jsonReaderInterface import JsonReaderInterface
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TwitchTokensRepository(TwitchTokensRepositoryInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensStorage: TwitchTokensStorageInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        seedFileReader: JsonReaderInterface | None = None,
        sleepTime: timedelta = timedelta(minutes = 55),
        tokensExpirationBuffer: timedelta = timedelta(minutes = 10),
        validationExpirationBuffer: timedelta = timedelta(minutes = 10),
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchTokensStorage, TwitchTokensStorageInterface):
            raise TypeError(f'twitchTokensStorage argument is malformed: \"{twitchTokensStorage}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif seedFileReader is not None and not isinstance(seedFileReader, JsonReaderInterface):
            raise TypeError(f'seedFileReader argument is malformed: \"{seedFileReader}\"')
        elif not isinstance(sleepTime, timedelta):
            raise TypeError(f'sleepTime argument is malformed: \"{sleepTime}\"')
        elif not isinstance(tokensExpirationBuffer, timedelta):
            raise TypeError(f'tokensExpirationBuffer argument is malformed: \"{tokensExpirationBuffer}\"')
        elif not isinstance(validationExpirationBuffer, timedelta):
            raise TypeError(f'validationExpirationBuffer argument is malformed: \"{validationExpirationBuffer}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchTokensStorage: Final[TwitchTokensStorageInterface] = twitchTokensStorage
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__seedFileReader: JsonReaderInterface | None = seedFileReader
        self.__sleepTime: Final[timedelta] = sleepTime
        self.__tokensExpirationBuffer: Final[timedelta] = tokensExpirationBuffer
        self.__validationExpirationBuffer: Final[timedelta] = validationExpirationBuffer

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
            self.__timber.log('TwitchTokensRepository', f'Encountered network error when trying to add user ({twitchChannel=}) ({twitchChannelId=}) ({code=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchTokensRepository encountered network error when trying to add user ({twitchChannel=}) ({twitchChannelId=}) ({code=})')

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

        nowDateTime = self.__timeZoneRepository.getNow()
        if nowDateTime + self.__tokensExpirationBuffer > tokensDetails.expirationTime:
            return False

        validationTime = self.__twitchChannelIdToValidationTime.get(twitchChannelId, None)
        if validationTime is None:
            return False

        return nowDateTime + self.__validationExpirationBuffer <= validationTime

    async def __checkAndValidateTokensAsNecessary(self):
        self.__timber.log('TwitchTokensRepository', f'Checking if any Twitch tokens require validation...')

        nowDateTime = self.__timeZoneRepository.getNow()
        twitchChannelIds = frozenset(self.__twitchChannelIdToValidationTime.keys())
        twitchChannelIdsToValidate: set[str] = set()

        for twitchChannelId in twitchChannelIds:
            validationTime = self.__twitchChannelIdToValidationTime.get(twitchChannelId, None)

            if validationTime is None or nowDateTime + self.__validationExpirationBuffer > validationTime:
                twitchChannelIdsToValidate.add(twitchChannelId)

        if len(twitchChannelIdsToValidate) == 0:
            return

        self.__timber.log('TwitchTokensRepository', f'Discovered {len(twitchChannelIdsToValidate)} Twitch token(s) that require validation...')

        for twitchChannelId in twitchChannelIds:
            tokensDetails = await self.getTokensDetailsById(
                twitchChannelId = twitchChannelId,
            )

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

        self.__timber.log('TwitchTokensRepository', f'Reading in seed file... ({seedFileReader=})')
        jsonContents: dict[str, dict[str, Any]] | Any | None = await seedFileReader.readJsonAsync()
        await seedFileReader.deleteFileAsync()

        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            self.__timber.log('TwitchTokensRepository', f'Seed file is empty ({seedFileReader=}) ({jsonContents=})')
            return

        for twitchChannel, tokensDetailsJson in jsonContents.items():
            if not utils.isValidStr(twitchChannel) or not isinstance(tokensDetailsJson, dict):
                self.__timber.log('TwitchTokensRepository', f'Encountered malformed data structure within seed file ({seedFileReader=}) ({twitchChannel=}) ({tokensDetailsJson=})')
                continue

            tokensDetails: TwitchTokensDetails | None = None

            if utils.isValidStr(tokensDetailsJson.get('code')):
                code = utils.getStrFromDict(tokensDetailsJson, 'code')

                try:
                    tokensDetails = await self.__twitchApiService.fetchTokens(code = code)
                except GenericNetworkException as e:
                    self.__timber.log('TwitchTokensRepository', f'Unable to fetch tokens ({twitchChannel=}) ({code=})', e, traceback.format_exc())
            else:
                tokensDetails = TwitchTokensDetails(
                    expirationTime = await self.__createExpiredExpirationTime(),
                    accessToken = utils.getStrFromDict(tokensDetailsJson, 'accessToken'),
                    refreshToken = utils.getStrFromDict(tokensDetailsJson, 'refreshToken'),
                )

            if tokensDetails is not None:
                twitchChannelId = await self.__userIdsRepository.requireUserId(
                    userName = twitchChannel,
                )

                await self.__setTokensDetails(
                    twitchChannelId = twitchChannelId,
                    tokensDetails = tokensDetails,
                )

        self.__timber.log('TwitchTokensRepository', f'Finished reading in seed file ({seedFileReader=})')

    async def __createExpiredExpirationTime(self) -> datetime:
        nowDateTime = self.__timeZoneRepository.getNow()
        return nowDateTime - timedelta(weeks = 2)

    async def getAccessToken(
        self,
        twitchChannel: str,
    ) -> str | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        twitchChannelId = await self.__userIdsRepository.fetchUserId(
            userName = twitchChannel,
        )

        if not utils.isValidStr(twitchChannelId):
            return None

        return await self.getAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

    async def getAccessTokenById(
        self,
        twitchChannelId: str,
    ) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        tokensDetails = await self.getTokensDetailsById(
            twitchChannelId = twitchChannelId,
        )

        if tokensDetails is None:
            return None

        return tokensDetails.accessToken

    async def getTokensDetails(
        self,
        twitchChannel: str,
    ) -> TwitchTokensDetails | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        twitchChannelId = await self.__userIdsRepository.fetchUserId(
            userName = twitchChannel,
        )

        if not utils.isValidStr(twitchChannelId):
            return None

        return await self.getTokensDetailsById(
            twitchChannelId = twitchChannelId,
        )

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
            tokensDetails = await self.__twitchTokensStorage.get(
                twitchChannelId = twitchChannelId,
            )

        if tokensDetails is None:
            return None

        tokensDetails = await self.__validateAndRefreshAccessToken(
            twitchChannelId = twitchChannelId,
            tokensDetails = tokensDetails,
        )

        self.__cache[twitchChannelId] = tokensDetails
        return tokensDetails

    async def removeUser(
        self,
        twitchChannel: str,
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        twitchChannelId = await self.__userIdsRepository.requireUserId(
            userName = twitchChannel,
        )

        await self.removeUserById(
            twitchChannelId = twitchChannelId,
        )

    async def removeUserById(
        self,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        await self.__twitchTokensStorage.remove(
            twitchChannelId = twitchChannelId,
        )

        self.__cache.pop(twitchChannelId, None)

    async def requireAccessToken(
        self,
        twitchChannel: str,
    ) -> str:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        accessToken = await self.getAccessToken(
            twitchChannel = twitchChannel,
        )

        if not utils.isValidStr(accessToken):
            raise TwitchAccessTokenMissingException(f'Twitch access token is missing ({twitchChannel=}) ({accessToken=})')

        return accessToken

    async def requireAccessTokenById(
        self,
        twitchChannelId: str,
    ) -> str:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        accessToken = await self.getAccessTokenById(
            twitchChannelId  = twitchChannelId,
        )

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

        await self.__twitchTokensStorage.updateExpirationTime(
            expirationTime = expirationTime,
            twitchChannelId = twitchChannelId,
        )

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

        if tokensDetails is None:
            await self.__twitchTokensStorage.remove(
                twitchChannelId = twitchChannelId,
            )

            self.__cache.pop(twitchChannelId, None)
        else:
            await self.__twitchTokensStorage.setTokensDetails(
                twitchChannelId = twitchChannelId,
                tokensDetails = tokensDetails,
            )

            self.__cache[twitchChannelId] = tokensDetails

    def start(self):
        if self.__isStarted:
            self.__timber.log('TwitchTokensRepository', 'Not starting TwitchTokensRepository as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TwitchTokensRepository', 'Starting TwitchTokensRepository...')
        self.__backgroundTaskHelper.createTask(self.__startValidationLoop())

    async def __startValidationLoop(self):
        await self.__consumeSeedFile()

        while True:
            await self.__checkAndValidateTokensAsNecessary()
            await asyncio.sleep(self.__sleepTime.total_seconds())

    async def __validateAndRefreshAccessToken(
        self,
        twitchChannelId: str,
        tokensDetails: TwitchTokensDetails,
    ) -> TwitchTokensDetails:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(tokensDetails, TwitchTokensDetails):
            raise TypeError(f'tokensDetails argument is malformed: \"{tokensDetails}\"')

        nowDateTime = self.__timeZoneRepository.getNow()

        if await self.__areTokensDetailsCurrentlyValid(
            twitchChannelId = twitchChannelId,
            tokensDetails = tokensDetails,
        ):
            return tokensDetails

        self.__timber.log('TwitchTokensRepository', f'Validating Twitch tokens ({twitchChannelId=})...')
        self.__twitchChannelIdToValidationTime.pop(twitchChannelId, None)
        validationResponse: TwitchValidationResponse | None = None

        try:
            validationResponse = await self.__twitchApiService.validate(
                twitchAccessToken = tokensDetails.accessToken
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchTokensRepository', f'Encountered network error when trying to validate Twitch tokens ({twitchChannelId=}) ({tokensDetails=})', e, traceback.format_exc())
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
                self.__timber.log('TwitchTokensRepository', f'Encountered network error when trying to refresh Twitch tokens ({twitchChannelId=})', e, traceback.format_exc())
                raise GenericNetworkException(f'TwitchTokensRepository encountered network error when trying to refresh Twitch tokens ({twitchChannelId=})')
            except TwitchPasswordChangedException as e:
                self.__timber.log('TwitchTokensRepository', f'Encountered network error caused by password change when trying to refresh Twitch tokens ({twitchChannelId=})', e, traceback.format_exc())
                await self.removeUserById(twitchChannelId)
                raise TwitchPasswordChangedException(f'TwitchTokensRepository encountered network error caused by password change when trying to refresh Twitch tokens ({twitchChannelId=})')

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
