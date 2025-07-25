import traceback

from .timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ..friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from ..officialAccounts.officialTwitchAccountUserIdProviderInterface import OfficialTwitchAccountUserIdProviderInterface
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...funtoon.funtoonUserIdProviderInterface import FuntoonUserIdProviderInterface
from ...misc import utils as utils
from ...misc.cynanBotUserIdsProviderInterface import CynanBotUserIdsProviderInterface
from ...storage.linesReaderInterface import LinesReaderInterface
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TimeoutImmuneUserIdsRepository(TimeoutImmuneUserIdsRepositoryInterface):

    def __init__(
        self,
        cynanBotUserIdsProvider: CynanBotUserIdsProviderInterface,
        funtoonUserIdProvider: FuntoonUserIdProviderInterface,
        officialTwitchAccountUserIdProvider: OfficialTwitchAccountUserIdProviderInterface,
        timber: TimberInterface,
        twitchFriendsUserIdProvider: TwitchFriendsUserIdRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        otherImmuneUserIdsLinesReader: LinesReaderInterface | None = None,
    ):
        if not isinstance(cynanBotUserIdsProvider, CynanBotUserIdsProviderInterface):
            raise TypeError(f'cynanBotUserIdsProvider argument is malformed: \"{cynanBotUserIdsProvider}\"')
        elif not isinstance(funtoonUserIdProvider, FuntoonUserIdProviderInterface):
            raise TypeError(f'funtoonUserIdProvider argument is malformed: \"{funtoonUserIdProvider}\"')
        elif not isinstance(officialTwitchAccountUserIdProvider, OfficialTwitchAccountUserIdProviderInterface):
            raise TypeError(f'officialTwitchAccountUserIdProvider argument is malformed: \"{officialTwitchAccountUserIdProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchFriendsUserIdProvider, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdProvider argument is malformed: \"{twitchFriendsUserIdProvider}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif otherImmuneUserIdsLinesReader is not None and not isinstance(otherImmuneUserIdsLinesReader, LinesReaderInterface):
            raise TypeError(f'immuneUserIdsLinesReader argument is malformed: \"{otherImmuneUserIdsLinesReader}\"')

        self.__cynanBotUserIdsProvider: CynanBotUserIdsProviderInterface = cynanBotUserIdsProvider
        self.__funtoonUserIdProvider: FuntoonUserIdProviderInterface = funtoonUserIdProvider
        self.__officialTwitchAccountUserIdProvider: OfficialTwitchAccountUserIdProviderInterface = officialTwitchAccountUserIdProvider
        self.__timber: TimberInterface = timber
        self.__twitchFriendsUserIdProvider: TwitchFriendsUserIdRepositoryInterface = twitchFriendsUserIdProvider
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__otherImmuneUserIdsLinesReader: LinesReaderInterface | None = otherImmuneUserIdsLinesReader

        self.__immuneUserIds: frozenset[str] | None = None
        self.__otherImmuneUserIds: frozenset[str] | None = None
        self.__twitchUserId: str | None = None

    async def clearCaches(self):
        self.__immuneUserIds = None
        self.__otherImmuneUserIds = None
        self.__twitchUserId = None
        self.__timber.log('TimeoutImmuneUserIdsRepository', 'Caches cleared')

    async def getAllUserIds(self) -> frozenset[str]:
        allUserIds: set[str] = set()
        allUserIds.update(await self.getOtherUserIds())
        allUserIds.update(await self.getUserIds())
        return frozenset(allUserIds)

    async def getOtherUserIds(self) -> frozenset[str]:
        userIds = self.__otherImmuneUserIds

        if userIds is not None:
            return userIds

        newUserIds: set[str] = set()

        if self.__otherImmuneUserIdsLinesReader is not None:
            lines: list[str] | None = None

            try:
                lines = await self.__otherImmuneUserIdsLinesReader.readLinesAsync()
            except Exception as e:
                self.__timber.log('TimeoutImmuneUserIdsRepository', f'Encountered an exception when trying to read in other immune user IDs ({self.__otherImmuneUserIdsLinesReader=}): {e}', e, traceback.format_exc())

            if lines is not None and len(lines) >= 1:
                for index, line in enumerate(lines):
                    cleanedLine = utils.cleanStr(line)

                    if utils.isValidStr(cleanedLine):
                        newUserIds.add(cleanedLine)
                    else:
                        self.__timber.log('TimeoutImmuneUserIdsRepository', f'Found invalid other immune user ID at line #{index} ({cleanedLine=}) ({self.__otherImmuneUserIdsLinesReader=})')

                self.__timber.log('TimeoutImmuneUserIdsRepository', f'Read in {len(lines)} other immune user ID(s) ({self.__otherImmuneUserIdsLinesReader=})')

        frozenUserIds: frozenset[str] = frozenset(newUserIds)
        self.__otherImmuneUserIds = frozenUserIds
        return frozenUserIds

    async def __getTwitchUserId(self) -> str:
        twitchUserId = self.__twitchUserId

        if twitchUserId is None:
            twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
            twitchUserId = await self.__userIdsRepository.requireUserId(twitchHandle)
            self.__twitchUserId = twitchUserId

        return twitchUserId

    async def getUserIds(self) -> frozenset[str]:
        userIds = self.__immuneUserIds

        if userIds is not None:
            return userIds

        newUserIds: set[str] = set()
        newUserIds.add(await self.__getTwitchUserId())

        cynanBotUserId = await self.__cynanBotUserIdsProvider.getCynanBotUserId()
        if utils.isValidStr(cynanBotUserId):
            newUserIds.add(cynanBotUserId)

        cynanBotTtsUserId = await self.__cynanBotUserIdsProvider.getCynanBotTtsUserId()
        if utils.isValidStr(cynanBotTtsUserId):
            newUserIds.add(cynanBotTtsUserId)

        funtoonUserId = await self.__funtoonUserIdProvider.getFuntoonUserId()
        if utils.isValidStr(funtoonUserId):
            newUserIds.add(funtoonUserId)

        kiawaBotUserId = await self.__twitchFriendsUserIdProvider.getKiawaBotUserId()
        if utils.isValidStr(kiawaBotUserId):
            newUserIds.add(kiawaBotUserId)

        mandooBotUserId = await self.__twitchFriendsUserIdProvider.getMandooBotUserId()
        if utils.isValidStr(mandooBotUserId):
            newUserIds.add(mandooBotUserId)

        oathyBotUserId = await self.__twitchFriendsUserIdProvider.getOathyBotUserId()
        if utils.isValidStr(oathyBotUserId):
            newUserIds.add(oathyBotUserId)

        officialTwitchAccountUserIds = await self.__officialTwitchAccountUserIdProvider.getAllUserIds()
        newUserIds.update(officialTwitchAccountUserIds)

        frozenUserIds: frozenset[str] = frozenset(newUserIds)
        self.__immuneUserIds = frozenUserIds
        return frozenUserIds

    async def isImmune(self, userId: str) -> bool:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        userIds = await self.getUserIds()
        return userId in userIds
