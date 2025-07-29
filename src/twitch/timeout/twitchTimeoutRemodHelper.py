import asyncio
from datetime import datetime, timedelta

from frozenlist import FrozenList

from .twitchTimeoutRemodData import TwitchTimeoutRemodData
from .twitchTimeoutRemodHelperInterface import TwitchTimeoutRemodHelperInterface
from .twitchTimeoutRemodRepositoryInterface import TwitchTimeoutRemodRepositoryInterface
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TwitchTimeoutRemodHelper(TwitchTimeoutRemodHelperInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTimeoutRemodRepository: TwitchTimeoutRemodRepositoryInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        queueSleepTimeSeconds: float = 3,
        additionalBufferTime: timedelta = timedelta(seconds = 5),
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchTimeoutRemodRepository, TwitchTimeoutRemodRepositoryInterface):
            raise TypeError(f'twitchTimeoutRemodRepository argument is malformed: \"{twitchTimeoutRemodRepository}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidInt(queueSleepTimeSeconds):
            raise TypeError(f'queueSleepTimeSeconds argument is malformed: \"{queueSleepTimeSeconds}\"')
        elif queueSleepTimeSeconds < 1 or queueSleepTimeSeconds > 10:
            raise ValueError(f'queueSleepTimeSeconds argument is out of bounds: {queueSleepTimeSeconds}')
        elif not isinstance(additionalBufferTime, timedelta):
            raise TypeError(f'additionalBufferTime argument is malformed: \"{additionalBufferTime}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchTimeoutRemodRepository: TwitchTimeoutRemodRepositoryInterface = twitchTimeoutRemodRepository
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__queueSleepTimeSeconds: float = queueSleepTimeSeconds
        self.__additionalBufferTime: timedelta = additionalBufferTime

        self.__isStarted: bool = False

    async def __deleteFromRepository(self, remodAction: TwitchTimeoutRemodData):
        if not isinstance(remodAction, TwitchTimeoutRemodData):
            raise TypeError(f'remodAction argument is malformed: \"{remodAction}\"')

        await self.__twitchTimeoutRemodRepository.delete(
            broadcasterUserId = remodAction.broadcasterUserId,
            userId = remodAction.userId
        )

    async def __refresh(self):
        remodActions = await self.__twitchTimeoutRemodRepository.getAll()
        frozenRemodActions: FrozenList[TwitchTimeoutRemodData] = FrozenList(remodActions)
        frozenRemodActions.freeze()

        if len(frozenRemodActions) == 0:
            return

        self.__timber.log('TwitchTimeoutRemodHelper', f'Re-applying mod status to {len(remodActions)} user(s)...')
        twitchAccessTokens: dict[str, str | None] = dict()
        broadcastersWithoutTokens: set[str] = set()

        for remodAction in frozenRemodActions:
            if remodAction.broadcasterUserId in broadcastersWithoutTokens:
                continue

            twitchAccessToken = twitchAccessTokens.get(remodAction.broadcasterUserId, None)

            if not utils.isValidStr(twitchAccessToken):
                twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
                    twitchChannelId = remodAction.broadcasterUserId,
                )

                if not utils.isValidStr(twitchAccessToken):
                    self.__timber.log('TwitchTimeoutRemodHelper', f'Unable to retrieve Twitch access token for {remodAction.broadcasterUserName}:{remodAction.broadcasterUserId}')
                    broadcastersWithoutTokens.add(remodAction.broadcasterUserId)
                    await self.__deleteFromRepository(remodAction)
                    continue

                twitchAccessTokens[remodAction.broadcasterUserId] = twitchAccessToken

            userName = await self.__userIdsRepository.requireUserName(
                userId = remodAction.userId,
                twitchAccessToken = twitchAccessToken,
            )

            if await self.__twitchApiService.addModerator(
                broadcasterId = remodAction.broadcasterUserId,
                twitchAccessToken = twitchAccessToken,
                userId = remodAction.userId,
            ):
                self.__timber.log('TwitchTimeoutRemodHelper', f'Successfully re-modded user ({remodAction=}) ({userName=})')
            else:
                self.__timber.log('TwitchTimeoutRemodHelper', f'Failed to re-mod user ({remodAction=}) ({userName=})')

            await self.__deleteFromRepository(remodAction)

        self.__timber.log('TwitchTimeoutRemodHelper', f'Finished re-applying mod status to {len(frozenRemodActions)} user(s)')

    def start(self):
        if self.__isStarted:
            self.__timber.log('TwitchTimeoutRemodHelper', 'Not starting TwitchTimeoutRemodHelper as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TwitchTimeoutRemodHelper', 'Starting TwitchTimeoutRemodHelper...')
        self.__backgroundTaskHelper.createTask(self.__startEventLoop())

    async def __startEventLoop(self):
        while True:
            await self.__refresh()
            await asyncio.sleep(self.__queueSleepTimeSeconds)

    async def submitRemodData(
        self,
        timeoutDurationSeconds: int,
        broadcasterUserId: str,
        broadcasterUserName: str,
        userId: str,
    ):
        if not utils.isValidInt(timeoutDurationSeconds):
            raise TypeError(f'timeoutDurationSeconds argument is malformed: \"{timeoutDurationSeconds}\"')
        elif timeoutDurationSeconds < 1 or timeoutDurationSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'timeoutDurationSeconds argument is out of bounds: {timeoutDurationSeconds}')
        if not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(broadcasterUserName):
            raise TypeError(f'broadcasterUserName argument is malformed: \"{broadcasterUserName}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        now = datetime.now(self.__timeZoneRepository.getDefault())
        remodDateTime = now + timedelta(seconds = timeoutDurationSeconds) + self.__additionalBufferTime

        await self.__twitchTimeoutRemodRepository.add(TwitchTimeoutRemodData(
            remodDateTime = remodDateTime,
            broadcasterUserId = broadcasterUserId,
            broadcasterUserName = broadcasterUserName,
            userId = userId,
        ))
