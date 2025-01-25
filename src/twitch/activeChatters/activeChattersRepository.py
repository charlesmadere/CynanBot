from collections import defaultdict
from datetime import datetime, timedelta
from typing import Collection

from frozenlist import FrozenList

from .activeChatter import ActiveChatter
from .activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils


class ActiveChattersRepository(ActiveChattersRepositoryInterface):

    def __init__(
        self,
        timeZoneRepository: TimeZoneRepositoryInterface,
        maxActiveChattersSize: int = 200,
        maxActiveChattersTimeToLive: timedelta = timedelta(hours = 1)
    ):
        if not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidInt(maxActiveChattersSize):
            raise TypeError(f'cacheSize argument is malformed: \"{maxActiveChattersSize}\"')
        elif maxActiveChattersSize < 16 or maxActiveChattersSize > 512:
            raise ValueError(f'maxActiveChattersSize argument is out of bounds: {maxActiveChattersSize}')
        elif not isinstance(maxActiveChattersTimeToLive, timedelta):
            raise TypeError(f'maxActiveChattersTimeToLive argument is malformed: \"{maxActiveChattersTimeToLive}\"')

        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__maxActiveChattersSize: int = maxActiveChattersSize
        self.__maxActiveChattersTimeToLive: timedelta = maxActiveChattersTimeToLive

        self.__twitchChannelIdToActiveChatters: dict[str, list[ActiveChatter]] = defaultdict(lambda: list())

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

        activeChatters = self.__twitchChannelIdToActiveChatters[twitchChannelId]
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

        activeChatters = self.__twitchChannelIdToActiveChatters[twitchChannelId]
        now = datetime.now(self.__timeZoneRepository.getDefault())

        await self.__clean(
            now = now,
            activeChatters = activeChatters
        )

        frozenActiveChatters: FrozenList[ActiveChatter] = FrozenList(activeChatters)
        frozenActiveChatters.freeze()

        return frozenActiveChatters

    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ):
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        activeChatters = self.__twitchChannelIdToActiveChatters[twitchChannelId]
        indexToDelete: int | None = None

        for index, activeChatter in enumerate(activeChatters):
            if activeChatter.chatterUserId == chatterUserId:
                indexToDelete = index
                break

        if indexToDelete is not None:
            del activeChatters[indexToDelete]
