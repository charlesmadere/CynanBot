from .timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...funtoon.funtoonUserIdProviderInterface import FuntoonUserIdProviderInterface
from ...misc import utils as utils
from ...misc.cynanBotUserIdsProviderInterface import CynanBotUserIdsProviderInterface
from ...nightbot.nightbotUserIdProviderInterface import NightbotUserIdProviderInterface
from ...streamElements.streamElementsUserIdProviderInterface import StreamElementsUserIdProviderInterface
from ...streamLabs.streamLabsUserIdProviderInterface import StreamLabsUserIdProviderInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TimeoutImmuneUserIdsRepository(TimeoutImmuneUserIdsRepositoryInterface):

    def __init__(
        self,
        cynanBotUserIdsProvider: CynanBotUserIdsProviderInterface,
        funtoonUserIdProvider: FuntoonUserIdProviderInterface,
        nightbotUserIdProvider: NightbotUserIdProviderInterface,
        streamElementsUserIdProvider: StreamElementsUserIdProviderInterface,
        streamLabsUserIdProvider: StreamLabsUserIdProviderInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        additionalImmuneUserIds: set[str] | None = None
    ):
        if not isinstance(cynanBotUserIdsProvider, CynanBotUserIdsProviderInterface):
            raise TypeError(f'cynanBotUserIdsProvider argument is malformed: \"{cynanBotUserIdsProvider}\"')
        elif not isinstance(funtoonUserIdProvider, FuntoonUserIdProviderInterface):
            raise TypeError(f'funtoonUserIdProvider argument is malformed: \"{funtoonUserIdProvider}\"')
        elif not isinstance(nightbotUserIdProvider, NightbotUserIdProviderInterface):
            raise TypeError(f'nightbotUserIdProvider argument is malformed: \"{nightbotUserIdProvider}\"')
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

        self.__cynanBotUserIdsProvider: CynanBotUserIdsProviderInterface = cynanBotUserIdsProvider
        self.__funtoonUserIdProvider: FuntoonUserIdProviderInterface = funtoonUserIdProvider
        self.__nightbotUserIdProvider: NightbotUserIdProviderInterface = nightbotUserIdProvider
        self.__streamElementsUserIdProvider: StreamElementsUserIdProviderInterface = streamElementsUserIdProvider
        self.__streamLabsUserIdProvider: StreamLabsUserIdProviderInterface = streamLabsUserIdProvider
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__additionalImmuneUserIds: set[str] | None = additionalImmuneUserIds

        self.__cachedImmuneUserIds: frozenset[str] | None = None
        self.__twitchUserId: str | None = None

    async def __getImmuneUserIds(self) -> frozenset[str]:
        cachedImmuneUserIds = self.__cachedImmuneUserIds

        if cachedImmuneUserIds is not None:
            return cachedImmuneUserIds

        immuneUserIds: set[str] = set()
        immuneUserIds.add(await self.__getTwitchUserId())

        if self.__additionalImmuneUserIds is not None and len(self.__additionalImmuneUserIds) >= 1:
            immuneUserIds.update(self.__additionalImmuneUserIds)

        cynanBotUserId = await self.__cynanBotUserIdsProvider.getCynanBotUserId()
        if utils.isValidStr(cynanBotUserId):
            immuneUserIds.add(cynanBotUserId)

        cynanBotTtsUserId = await self.__cynanBotUserIdsProvider.getCynanBotTtsUserId()
        if utils.isValidStr(cynanBotTtsUserId):
            immuneUserIds.add(cynanBotTtsUserId)

        funtoonUserId = await self.__funtoonUserIdProvider.getFuntoonUserId()
        if utils.isValidStr(funtoonUserId):
            immuneUserIds.add(funtoonUserId)

        nightbotUserId = await self.__nightbotUserIdProvider.getNightbotUserId()
        if utils.isValidStr(nightbotUserId):
            immuneUserIds.add(nightbotUserId)

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
