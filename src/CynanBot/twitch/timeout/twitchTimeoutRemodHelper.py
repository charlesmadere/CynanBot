import asyncio

import CynanBot.misc.utils as utils
from CynanBot.misc.backgroundTaskHelperInterface import \
    BackgroundTaskHelperInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.timeout.twitchTimeoutRemodData import \
    TwitchTimeoutRemodData
from CynanBot.twitch.timeout.twitchTimeoutRemodHelperInterface import \
    TwitchTimeoutRemodHelperInterface
from CynanBot.twitch.timeout.twitchTimeoutRemodRepositoryInterface import \
    TwitchTimeoutRemodRepositoryInterface
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface


class TwitchTimeoutRemodHelper(TwitchTimeoutRemodHelperInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTimeoutRemodRepository: TwitchTimeoutRemodRepositoryInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        queueSleepTimeSeconds: float = 3
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
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

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchTimeoutRemodRepository: TwitchTimeoutRemodRepositoryInterface = twitchTimeoutRemodRepository
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__queueSleepTimeSeconds: float = queueSleepTimeSeconds

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
        if remodActions is None or len(remodActions) == 0:
            return

        self.__timber.log('TwitchTimeoutRemodHelper', f'Re-applying mod status to {len(remodActions)} user(s)...')
        twitchAccessTokens: dict[str, str | None] = dict()
        broadcastersWithoutTokens: set[str] = set()

        for remodAction in remodActions:
            if remodAction.broadcasterUserId in broadcastersWithoutTokens:
                continue

            twitchAccessToken = twitchAccessTokens.get(remodAction.broadcasterUserId, None)

            if not utils.isValidStr(twitchAccessToken):
                if not await self.__twitchTokensRepository.hasAccessTokenById(
                    twitchChannelId = remodAction.broadcasterUserId
                ):
                    self.__timber.log('TwitchTimeoutRemodHelper', f'There is no Twitch access token available for {remodAction.broadcasterUserName}:{remodAction.broadcasterUserId}')
                    broadcastersWithoutTokens.add(remodAction.broadcasterUserId)
                    await self.__deleteFromRepository(remodAction)
                    continue

                twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
                    twitchChannelId = remodAction.broadcasterUserId
                )

                if not utils.isValidStr(twitchAccessToken):
                    self.__timber.log('TwitchTimeoutRemodHelper', f'Unable to retrieve Twitch access token for {remodAction.broadcasterUserName}:{remodAction.broadcasterUserId}')
                    broadcastersWithoutTokens.add(remodAction.broadcasterUserId)
                    await self.__deleteFromRepository(remodAction)
                    continue

                twitchAccessTokens[remodAction.broadcasterUserId] = twitchAccessToken

            userName = await self.__userIdsRepository.requireUserName(
                userId = remodAction.userId,
                twitchAccessToken = twitchAccessToken
            )

            if await self.__twitchApiService.addModerator(
                broadcasterId = remodAction.broadcasterUserId,
                twitchAccessToken = twitchAccessToken,
                userId = remodAction.userId
            ):
                self.__timber.log('TwitchTimeoutRemodHelper', f'Successfully re-modded user ({remodAction=}) ({userName=})')
                await self.__deleteFromRepository(remodAction)
            else:
                self.__timber.log('TwitchTimeoutRemodHelper', f'Failed to re-mod user ({remodAction=}) ({userName=})')

        self.__timber.log('TwitchTimeoutRemodHelper', f'Finished re-applying mod status to {len(remodActions)} user(s)')

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

    async def submitRemodData(self, data: TwitchTimeoutRemodData):
        if not isinstance(data, TwitchTimeoutRemodData):
            raise TypeError(f'data argument is malformed: \"{data}\"')

        await self.__twitchTimeoutRemodRepository.add(data)
