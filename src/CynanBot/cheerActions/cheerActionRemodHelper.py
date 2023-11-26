import asyncio

import CynanBot.misc.utils as utils
from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.cheerActions.cheerActionRemodData import CheerActionRemodData
from CynanBot.cheerActions.cheerActionRemodHelperInterface import \
    CheerActionRemodHelperInterface
from CynanBot.cheerActions.cheerActionRemodRepositoryInterface import \
    CheerActionRemodRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.twitchApiServiceInterface import TwitchApiServiceInterface
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface


class CheerActionRemodHelper(CheerActionRemodHelperInterface):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        backgroundTaskHelper: BackgroundTaskHelper,
        cheerActionRemodRepository: CheerActionRemodRepositoryInterface,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        queueSleepTimeSeconds: float = 3
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise ValueError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(cheerActionRemodRepository, CheerActionRemodRepositoryInterface):
            raise ValueError(f'cheerActionRemodRepository argument is malformed: \"{cheerActionRemodRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise ValueError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not utils.isValidInt(queueSleepTimeSeconds):
            raise ValueError(f'queueSleepTimeSeconds argument is malformed: \"{queueSleepTimeSeconds}\"')
        elif queueSleepTimeSeconds < 1 or queueSleepTimeSeconds > 10:
            raise ValueError(f'queueSleepTimeSeconds argument is out of bounds: {queueSleepTimeSeconds}')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__cheerActionRemodRepository: CheerActionRemodRepositoryInterface = cheerActionRemodRepository
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__queueSleepTimeSeconds: float = queueSleepTimeSeconds

        self.__isStarted: bool = False

    async def __getTwitchAccessToken(self, userName: str) -> str:
        if not isinstance(userName, str):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        if await self.__twitchTokensRepository.hasAccessToken(userName):
            await self.__twitchTokensRepository.validateAndRefreshAccessToken(userName)
            return await self.__twitchTokensRepository.requireAccessToken(userName)
        else:
            administratorUserName = await self.__administratorProvider.getAdministratorUserName()
            await self.__twitchTokensRepository.validateAndRefreshAccessToken(administratorUserName)
            return await self.__twitchTokensRepository.requireAccessToken(administratorUserName)

    async def __refresh(self):
        data = await self.__cheerActionRemodRepository.getAll()

        if not utils.hasItems(data):
            return

        for remodAction in data:
            twitchAccessToken = await self.__getTwitchAccessToken(remodAction.getBroadcasterUserName())

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
            raise ValueError(f'data argument is malformed: \"{data}\"')

        await self.__cheerActionRemodRepository.add(data)
