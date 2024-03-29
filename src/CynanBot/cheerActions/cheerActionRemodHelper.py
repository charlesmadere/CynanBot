import asyncio
from typing import Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.cheerActions.cheerActionRemodData import CheerActionRemodData
from CynanBot.cheerActions.cheerActionRemodHelperInterface import \
    CheerActionRemodHelperInterface
from CynanBot.cheerActions.cheerActionRemodRepositoryInterface import \
    CheerActionRemodRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface


class CheerActionRemodHelper(CheerActionRemodHelperInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        cheerActionRemodRepository: CheerActionRemodRepositoryInterface,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        queueSleepTimeSeconds: float = 3
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(cheerActionRemodRepository, CheerActionRemodRepositoryInterface):
            raise TypeError(f'cheerActionRemodRepository argument is malformed: \"{cheerActionRemodRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not utils.isValidInt(queueSleepTimeSeconds):
            raise TypeError(f'queueSleepTimeSeconds argument is malformed: \"{queueSleepTimeSeconds}\"')
        elif queueSleepTimeSeconds < 1 or queueSleepTimeSeconds > 10:
            raise ValueError(f'queueSleepTimeSeconds argument is out of bounds: {queueSleepTimeSeconds}')

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__cheerActionRemodRepository: CheerActionRemodRepositoryInterface = cheerActionRemodRepository
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__queueSleepTimeSeconds: float = queueSleepTimeSeconds

        self.__isStarted: bool = False

    async def __refresh(self):
        remodActions = await self.__cheerActionRemodRepository.getAll()
        if not utils.hasItems(remodActions):
            return

        self.__timber.log('CheerActionRemodHelper', f'Re-applying mod status to {len(remodActions)} user(s)...')
        twitchAccessTokens: Dict[str, Optional[str]] = dict()

        for remodAction in remodActions:
            twitchAccessToken = twitchAccessTokens.get(remodAction.getBroadcasterUserId(), None)

            if not utils.isValidStr(twitchAccessToken):
                await self.__twitchTokensRepository.validateAndRefreshAccessToken(
                    twitchChannel = remodAction.getBroadcasterUserName()
                )

                twitchAccessToken = await self.__twitchTokensRepository.requireAccessToken(
                    twitchChannel = remodAction.getBroadcasterUserName()
                )

                twitchAccessTokens[remodAction.getBroadcasterUserId()] = twitchAccessToken

            if await self.__twitchApiService.addModerator(
                broadcasterId = remodAction.getBroadcasterUserId(),
                twitchAccessToken = twitchAccessToken,
                userId = remodAction.getUserId()
            ):
                await self.__cheerActionRemodRepository.delete(
                    broadcasterUserId = remodAction.getBroadcasterUserId(),
                    userId = remodAction.getUserId()
                )
            else:
                self.__timber.log('CheerActionRemodHelper', f'Failed to re-mod user ({remodAction})')

        self.__timber.log('CheerActionRemodHelper', f'Finished re-applying mod status to {len(remodActions)} user(s)')

    def start(self):
        if self.__isStarted:
            self.__timber.log('CheerActionRemodHelper', 'Not starting CheerActionRemodHelper as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('CheerActionRemodHelper', 'Starting CheerActionRemodHelper...')
        self.__backgroundTaskHelper.createTask(self.__startEventLoop())

    async def __startEventLoop(self):
        while True:
            await self.__refresh()
            await asyncio.sleep(self.__queueSleepTimeSeconds)

    async def submitRemodData(self, data: CheerActionRemodData):
        if not isinstance(data, CheerActionRemodData):
            raise TypeError(f'data argument is malformed: \"{data}\"')

        await self.__cheerActionRemodRepository.add(data)
