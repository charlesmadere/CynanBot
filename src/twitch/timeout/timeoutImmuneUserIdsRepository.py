from .timeoutImmuneUserIdsRepositoryInterface import \
    TimeoutImmuneUserIdsRepositoryInterface
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TimeoutImmuneUserIdsRepository(TimeoutImmuneUserIdsRepositoryInterface):

    def __init__(
        self,
        twitchHandleProvider: TwitchHandleProviderInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        immuneUserIds: set[str] = {
            '546457893', # CynanBot
            '977636741', # CynanBotTTS
            '477393386', # FUNtoon
        }
    ):
        if not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(immuneUserIds, set):
            raise TypeError(f'immuneUserIds argument is malformed: \"{immuneUserIds}\"')

        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__immuneUserIds: set[str] = immuneUserIds

        self.__twitchUserId: str | None = None

    async def __getTwitchUserId(self) -> str:
        twitchUserId = self.__twitchUserId

        if twitchUserId is None:
            twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
            twitchUserId = await self.__userIdsRepository.requireUserId(twitchHandle)
            self.__twitchUserId = twitchUserId

        return twitchUserId

    async def isImmune(self, userId: str) -> bool:
        twitchUserId = await self.__getTwitchUserId()
        return userId == twitchUserId or userId in self.__immuneUserIds
