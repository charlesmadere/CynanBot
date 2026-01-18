import traceback
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Final

from frozendict import frozendict

from .activeChatter import ActiveChatter
from .activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ..api.models.twitchChattersRequest import TwitchChattersRequest
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..exceptions import TwitchJsonException, TwitchStatusCodeException
from ..tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class ActiveChattersRepository(ActiveChattersRepositoryInterface):

    class Entry:

        def __init__(self):
            self.__chattersHaveBeenFetched: bool = False
            self.__chatters: Final[list[ActiveChatter]] = list()

        @property
        def chatters(self) -> list[ActiveChatter]:
            return self.__chatters

        @property
        def chattersHaveBeenFetched(self) -> bool:
            return self.__chattersHaveBeenFetched

        def __repr__(self) -> str:
            dictionary = self.toDictionary()
            return str(dictionary)

        def setChattersHaveBeenFetched(self):
            self.__chattersHaveBeenFetched = True

        def toDictionary(self) -> dict[str, Any]:
            return {
                'chatters': self.__chatters,
                'chattersHaveBeenFetched': self.__chattersHaveBeenFetched,
            }

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        maxActiveChattersSize: int = 256,
        maxActiveChattersTimeToLive: timedelta = timedelta(hours = 1),
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
        elif maxActiveChattersSize < 16 or maxActiveChattersSize > 512:
            raise ValueError(f'maxActiveChattersSize argument is out of bounds: {maxActiveChattersSize}')
        elif not isinstance(maxActiveChattersTimeToLive, timedelta):
            raise TypeError(f'maxActiveChattersTimeToLive argument is malformed: \"{maxActiveChattersTimeToLive}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__maxActiveChattersSize: Final[int] = maxActiveChattersSize
        self.__maxActiveChattersTimeToLive: Final[timedelta] = maxActiveChattersTimeToLive

        self.__twitchChannelIdToActiveChatters: Final[dict[str, ActiveChattersRepository.Entry]] = defaultdict(lambda: ActiveChattersRepository.Entry())

    async def add(
        self,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannelId: str,
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
            chatterUserName = chatterUserName,
        )

        activeChatters.insert(0, activeChatter)

        await self.__clean(
            now = now,
            activeChatters = activeChatters,
        )

    async def __clean(
        self,
        now: datetime,
        activeChatters: list[ActiveChatter],
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

    async def clearCaches(self):
        now = datetime.now(self.__timeZoneRepository.getDefault())

        for entry in self.__twitchChannelIdToActiveChatters.values():
            await self.__clean(
                now = now,
                activeChatters = entry.chatters,
            )

        self.__timber.log('ActiveChattersRepository', 'Caches cleared')

    async def __fetchCurrentConnectedChatters(
        self,
        entry: Entry,
        twitchChannelId: str,
    ) -> list[ActiveChatter]:
        entry.setChattersHaveBeenFetched()
        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchId = await self.__userIdsRepository.fetchUserId(twitchHandle)

        if not utils.isValidStr(twitchId):
            # this should be impossible here but let's just be overly careful
            return entry.chatters

        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(twitchId)

        if not utils.isValidStr(twitchAccessToken):
            return entry.chatters

        first = max(round(self.__maxActiveChattersSize * 0.75), 8)
        self.__timber.log('ActiveChattersRepository', f'Fetching currently connected chatters... ({twitchChannelId=}) ({first=})')

        try:
            chatters = await self.__twitchApiService.fetchChatters(
                twitchAccessToken = twitchAccessToken,
                chattersRequest = TwitchChattersRequest(
                    first = first,
                    broadcasterId = twitchChannelId,
                    moderatorId = twitchId,
                ),
            )
        except (GenericNetworkException, TwitchJsonException, TwitchStatusCodeException) as e:
            self.__timber.log('ActiveChattersRepository', f'Failed fetching currently connected chatters ({twitchChannelId=}) ({first=})', e, traceback.format_exc())
            return entry.chatters

        index = 0
        now = datetime.now(self.__timeZoneRepository.getDefault())
        mostRecentChat = now - timedelta(seconds = round(self.__maxActiveChattersTimeToLive.total_seconds() * 0.25))

        while index < len(chatters.data) and index < self.__maxActiveChattersSize:
            chatter = chatters.data[index]

            entry.chatters.append(ActiveChatter(
                mostRecentChat = mostRecentChat,
                chatterUserId = chatter.userId,
                chatterUserName = chatter.userLogin,
            ))

            index += 1

        return entry.chatters

    async def get(
        self,
        twitchChannelId: str,
    ) -> frozendict[str, ActiveChatter]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        activeChatters = await self.__getCurrentActiveChatters(twitchChannelId)
        now = datetime.now(self.__timeZoneRepository.getDefault())

        await self.__clean(
            now = now,
            activeChatters = activeChatters,
        )

        activeChattersDictionary: dict[str, ActiveChatter] = dict()

        for activeChatter in activeChatters:
            activeChattersDictionary[activeChatter.chatterUserId] = activeChatter

        return frozendict(activeChattersDictionary)

    async def __getCurrentActiveChatters(
        self,
        twitchChannelId: str,
    ) -> list[ActiveChatter]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        entry = self.__twitchChannelIdToActiveChatters[twitchChannelId]

        if entry.chattersHaveBeenFetched:
            return entry.chatters
        else:
            # On a Twitch channel's first call into this function, we will end up in this portion of the if statement.
            # From here, we will call the Twitch API and get a list of current connected chatters. This technically
            # doesn't really fulfill what this class is actually supposed to be doing, which is to maintain a list of
            # ACTIVE chatters. People who are just connected to the chat aren't necessarily an active chatter, they
            # might just be lurking after all.
            #
            # But anyway, this code is still helpful for situations where the bot has just now started up, especially
            # if the bot has been started up late, or had to be restarted mid-stream. In those situations, the list of
            # active chatters could end up being incredibly small, maybe just 1 or 2 chatters, if even that many. So
            # this code is meant to help bridge that gap and bring in some of the people who are currently connected
            # to chat, in order to give the active chatters list an initial collection of people.

            return await self.__fetchCurrentConnectedChatters(
                entry = entry,
                twitchChannelId = twitchChannelId,
            )

    async def isActiveIn(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> bool:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        activeChatters = await self.get(twitchChannelId = twitchChannelId)
        return chatterUserId in activeChatters

    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str,
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
