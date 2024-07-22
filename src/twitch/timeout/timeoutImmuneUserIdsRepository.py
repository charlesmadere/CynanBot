from .timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...funtoon.funtoonUserIdProviderInterface import FuntoonUserIdProviderInterface
from ...misc import utils as utils
from ...streamElements.streamElementsUserIdProviderInterface import StreamElementsUserIdProviderInterface
from ...streamLabs.streamLabsUserIdProviderInterface import StreamLabsUserIdProviderInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TimeoutImmuneUserIdsRepository(TimeoutImmuneUserIdsRepositoryInterface):

    def __init__(
        self,
        funtoonUserIdProvider: FuntoonUserIdProviderInterface,
        streamElementsUserIdProvider: StreamElementsUserIdProviderInterface,
        streamLabsUserIdProvider: StreamLabsUserIdProviderInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        additionalImmuneUserIds: set[str] = {
            '546457893', # CynanBot
            '977636741', # CynanBotTTS
        }
    ):
        if not isinstance(funtoonUserIdProvider, FuntoonUserIdProviderInterface):
            raise TypeError(f'funtoonUserIdProvider argument is malformed: \"{funtoonUserIdProvider}\"')
        elif not isinstance(streamElementsUserIdProvider, StreamElementsUserIdProviderInterface):
            raise TypeError(f'streamElementsUserIdProvider argument is malformed: \"{streamElementsUserIdProvider}\"')
        elif not isinstance(streamLabsUserIdProvider, StreamLabsUserIdProviderInterface):
            raise TypeError(f'streamLabsUserIdProvider argument is malformed: \"{streamLabsUserIdProvider}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(additionalImmuneUserIds, set):
            raise TypeError(f'additionalImmuneUserIds argument is malformed: \"{additionalImmuneUserIds}\"')

        self.__funtoonUserIdProvider: FuntoonUserIdProviderInterface = funtoonUserIdProvider
        self.__streamElementsUserIdProvider: StreamElementsUserIdProviderInterface = streamElementsUserIdProvider
        self.__streamLabsUserIdProvider: StreamLabsUserIdProviderInterface = streamLabsUserIdProvider
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__additionalImmuneUserIds: frozenset[str] = frozenset(additionalImmuneUserIds)

        self.__cachedImmuneUserIds: frozenset[str] | None = None
        self.__twitchUserId: str | None = None

    async def __getImmuneUserIds(self) -> frozenset[str]:
        cachedImmuneUserIds = self.__cachedImmuneUserIds

        if cachedImmuneUserIds is not None:
            return cachedImmuneUserIds

        immuneUserIds: set[str] = set()
        immuneUserIds.update(self.__additionalImmuneUserIds)
        immuneUserIds.add(await self.__getTwitchUserId())

        funtoonUserId = await self.__funtoonUserIdProvider.getFuntoonUserId()
        if utils.isValidStr(funtoonUserId):
            immuneUserIds.add(funtoonUserId)

        streamElementsUserId = await self.__streamElementsUserIdProvider.getStreamElementsUserId()
        if utils.isValidStr(streamElementsUserId):
            immuneUserIds.add(streamElementsUserId)

        streamLabsUserId = await self.__streamLabsUserIdProvider.getStreamLabsUserId()
        if utils.isValidStr(streamLabsUserId):
            immuneUserIds.add(streamLabsUserId)

        cachedImmuneUserIds = frozenset(immuneUserIds)
        self.__cachedImmuneUserIds = cachedImmuneUserIds
        return cachedImmuneUserIds

    async def __getTwitchUserId(self) -> str:
        twitchUserId = self.__twitchUserId

        if twitchUserId is None:
            twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
            twitchUserId = await self.__userIdsRepository.requireUserId(twitchHandle)
            self.__twitchUserId = twitchUserId

        return twitchUserId

    async def isImmune(self, userId: str) -> bool:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        immuneUserIds = await self.__getImmuneUserIds()
        return userId in immuneUserIds
