import traceback
from datetime import datetime, timedelta
from typing import Collection

from frozenlist import FrozenList

from .activeChatter import ActiveChatter
from .activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ..api.models.twitchChattersRequest import TwitchChattersRequest
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class ActiveChattersRepository(ActiveChattersRepositoryInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        maxActiveChattersSize: int = 200,
        maxActiveChattersTimeToLive: timedelta = timedelta(hours = 1)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidInt(maxActiveChattersSize):
            raise TypeError(f'cacheSize argument is malformed: \"{maxActiveChattersSize}\"')
        elif maxActiveChattersSize < 8 or maxActiveChattersSize > 512:
            raise ValueError(f'maxActiveChattersSize argument is out of bounds: {maxActiveChattersSize}')
        elif not isinstance(maxActiveChattersTimeToLive, timedelta):
            raise TypeError(f'maxActiveChattersTimeToLive argument is malformed: \"{maxActiveChattersTimeToLive}\"')

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__maxActiveChattersSize: int = maxActiveChattersSize
        self.__maxActiveChattersTimeToLive: timedelta = maxActiveChattersTimeToLive

        self.__twitchChannelIdToActiveChatters: dict[str, list[ActiveChatter]] = dict()

    async def add(
        self,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannelId: str
    ):
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        activeChatters = await self.__getCurrentActiveChatters(twitchChannelId)
        indexToDelete: int | None = None

        for index, activeChatter in enumerate(activeChatters):
            if activeChatter.chatterUserId == chatterUserId:
                indexToDelete = index
                break

        if indexToDelete is not None:
            del activeChatters[indexToDelete]

        now = datetime.now(self.__timeZoneRepository.getDefault())

        activeChatter = ActiveChatter(
            mostRecentChat = now,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName
        )

        activeChatters.insert(0, activeChatter)

        await self.__clean(
            now = now,
            activeChatters = activeChatters
        )

    async def __clean(
        self,
        now: datetime,
        activeChatters: list[ActiveChatter]
    ):
        if len(activeChatters) == 0:
            return

        activeChatters.sort(key = lambda element: element.mostRecentChat, reverse = True)

        while len(activeChatters) > self.__maxActiveChattersSize:
            del activeChatters[len(activeChatters) - 1]

        index = len(activeChatters) - 1

        while index >= 0 and activeChatters[index].mostRecentChat + self.__maxActiveChattersTimeToLive < now:
            del activeChatters[index]
            index = index - 1

    async def get(
        self,
        twitchChannelId: str
    ) -> Collection[ActiveChatter]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        activeChatters = await self.__getCurrentActiveChatters(twitchChannelId)
        now = datetime.now(self.__timeZoneRepository.getDefault())

        await self.__clean(
            now = now,
            activeChatters = activeChatters
        )

        frozenActiveChatters: FrozenList[ActiveChatter] = FrozenList(activeChatters)
        frozenActiveChatters.freeze()

        return frozenActiveChatters

    async def __getCurrentActiveChatters(
        self,
        twitchChannelId: str
    ) -> list[ActiveChatter]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        currentActiveChatters: list[ActiveChatter] | None = self.__twitchChannelIdToActiveChatters.get(twitchChannelId, None)

        if currentActiveChatters is not None:
            return currentActiveChatters

        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(twitchChannelId)
        currentActiveChatters = list()

        if not utils.isValidStr(twitchAccessToken):
            self.__twitchChannelIdToActiveChatters[twitchChannelId] = currentActiveChatters
            return currentActiveChatters

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchId = await self.__userIdsRepository.requireUserId(twitchHandle)
        first = round(self.__maxActiveChattersSize / 2)

        self.__timber.log('ActiveChattersRepository', f'Fetching currently connected chatters... ({twitchChannelId=}) ({twitchId=}) ({first=})')

        try:
            chatters = await self.__twitchApiService.fetchChatters(
                twitchAccessToken = twitchAccessToken,
                chattersRequest = TwitchChattersRequest(
                    first = first,
                    broadcasterId = twitchChannelId,
                    moderatorId = twitchId
                )
            )
        except GenericNetworkException as e:
            self.__timber.log('ActiveChattersRepository', f'Failed fetching currently connected chatters ({twitchChannelId=}) ({twitchId=}) ({first=}): {e}', e, traceback.format_exc())
            self.__twitchChannelIdToActiveChatters[twitchChannelId] = currentActiveChatters
            return currentActiveChatters

        index = 0
        now = datetime.now(self.__timeZoneRepository.getDefault())
        mostRecentChat = now - timedelta(seconds = round(self.__maxActiveChattersTimeToLive.total_seconds() / 2))

        while index < len(chatters.data) and index < self.__maxActiveChattersSize:
            chatter = chatters.data[index]
            currentActiveChatters.append(ActiveChatter(
                mostRecentChat = mostRecentChat,
                chatterUserId = chatter.userId,
                chatterUserName = chatter.userLogin
            ))

            index += 1

        self.__twitchChannelIdToActiveChatters[twitchChannelId] = currentActiveChatters
        return currentActiveChatters

    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ):
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        activeChatters = await self.__getCurrentActiveChatters(twitchChannelId)
        indexToDelete: int | None = None

        for index, activeChatter in enumerate(activeChatters):
            if activeChatter.chatterUserId == chatterUserId:
                indexToDelete = index
                break

        if indexToDelete is not None:
            del activeChatters[indexToDelete]
