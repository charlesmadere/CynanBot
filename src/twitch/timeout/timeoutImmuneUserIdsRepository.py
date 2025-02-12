from .timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ..friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from ..officialAccounts.officialTwitchAccountUserIdProviderInterface import OfficialTwitchAccountUserIdProviderInterface
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...funtoon.funtoonUserIdProviderInterface import FuntoonUserIdProviderInterface
from ...misc import utils as utils
from ...misc.cynanBotUserIdsProviderInterface import CynanBotUserIdsProviderInterface
from ...nightbot.nightbotUserIdProviderInterface import NightbotUserIdProviderInterface
from ...puptime.puptimeUserIdProviderInterface import PuptimeUserIdProviderInterface
from ...seryBot.seryBotUserIdProviderInterface import SeryBotUserIdProviderInterface
from ...streamElements.streamElementsUserIdProviderInterface import StreamElementsUserIdProviderInterface
from ...streamLabs.streamLabsUserIdProviderInterface import StreamLabsUserIdProviderInterface
from ...tangia.tangiaBotUserIdProviderInterface import TangiaBotUserIdProviderInterface
from ...theRun.theRunBotUserIdProviderInterface import TheRunBotUserIdProviderInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TimeoutImmuneUserIdsRepository(TimeoutImmuneUserIdsRepositoryInterface):

    def __init__(
        self,
        cynanBotUserIdsProvider: CynanBotUserIdsProviderInterface,
        funtoonUserIdProvider: FuntoonUserIdProviderInterface,
        nightbotUserIdProvider: NightbotUserIdProviderInterface,
        officialTwitchAccountUserIdProvider: OfficialTwitchAccountUserIdProviderInterface,
        puptimeUserIdProvider: PuptimeUserIdProviderInterface,
        seryBotUserIdProvider: SeryBotUserIdProviderInterface,
        streamElementsUserIdProvider: StreamElementsUserIdProviderInterface,
        streamLabsUserIdProvider: StreamLabsUserIdProviderInterface,
        tangiaBotUserIdProvider: TangiaBotUserIdProviderInterface,
        theRunBotUserIdProvider: TheRunBotUserIdProviderInterface,
        twitchFriendsUserIdProvider: TwitchFriendsUserIdRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        additionalImmuneUserIds: frozenset[str] | None = None
    ):
        if not isinstance(cynanBotUserIdsProvider, CynanBotUserIdsProviderInterface):
            raise TypeError(f'cynanBotUserIdsProvider argument is malformed: \"{cynanBotUserIdsProvider}\"')
        elif not isinstance(funtoonUserIdProvider, FuntoonUserIdProviderInterface):
            raise TypeError(f'funtoonUserIdProvider argument is malformed: \"{funtoonUserIdProvider}\"')
        elif not isinstance(nightbotUserIdProvider, NightbotUserIdProviderInterface):
            raise TypeError(f'nightbotUserIdProvider argument is malformed: \"{nightbotUserIdProvider}\"')
        elif not isinstance(officialTwitchAccountUserIdProvider, OfficialTwitchAccountUserIdProviderInterface):
            raise TypeError(f'officialTwitchAccountUserIdProvider argument is malformed: \"{officialTwitchAccountUserIdProvider}\"')
        elif not isinstance(puptimeUserIdProvider, PuptimeUserIdProviderInterface):
            raise TypeError(f'puptimeUserIdProvider argument is malformed: \"{puptimeUserIdProvider}\"')
        elif not isinstance(seryBotUserIdProvider, SeryBotUserIdProviderInterface):
            raise TypeError(f'seryBotUserIdProvider argument is malformed: \"{seryBotUserIdProvider}\"')
        elif not isinstance(streamElementsUserIdProvider, StreamElementsUserIdProviderInterface):
            raise TypeError(f'streamElementsUserIdProvider argument is malformed: \"{streamElementsUserIdProvider}\"')
        elif not isinstance(streamLabsUserIdProvider, StreamLabsUserIdProviderInterface):
            raise TypeError(f'streamLabsUserIdProvider argument is malformed: \"{streamLabsUserIdProvider}\"')
        elif not isinstance(tangiaBotUserIdProvider, TangiaBotUserIdProviderInterface):
            raise TypeError(f'tangiaBotUserIdProvider argument is malformed: \"{tangiaBotUserIdProvider}\"')
        elif not isinstance(theRunBotUserIdProvider, TheRunBotUserIdProviderInterface):
            raise TypeError(f'theRunBotUserIdProvider argument is malformed: \"{theRunBotUserIdProvider}\"')
        elif not isinstance(twitchFriendsUserIdProvider, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdProvider argument is malformed: \"{twitchFriendsUserIdProvider}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif additionalImmuneUserIds is not None and not isinstance(additionalImmuneUserIds, frozenset):
            raise TypeError(f'additionalImmuneUserIds argument is malformed: \"{additionalImmuneUserIds}\"')

        self.__cynanBotUserIdsProvider: CynanBotUserIdsProviderInterface = cynanBotUserIdsProvider
        self.__funtoonUserIdProvider: FuntoonUserIdProviderInterface = funtoonUserIdProvider
        self.__nightbotUserIdProvider: NightbotUserIdProviderInterface = nightbotUserIdProvider
        self.__officialTwitchAccountUserIdProvider: OfficialTwitchAccountUserIdProviderInterface = officialTwitchAccountUserIdProvider
        self.__puptimeUserIdProvider: PuptimeUserIdProviderInterface = puptimeUserIdProvider
        self.__seryBotUserIdProvider: SeryBotUserIdProviderInterface = seryBotUserIdProvider
        self.__streamElementsUserIdProvider: StreamElementsUserIdProviderInterface = streamElementsUserIdProvider
        self.__streamLabsUserIdProvider: StreamLabsUserIdProviderInterface = streamLabsUserIdProvider
        self.__tangiaBotUserIdProvider: TangiaBotUserIdProviderInterface = tangiaBotUserIdProvider
        self.__theRunBotUserIdProvider: TheRunBotUserIdProviderInterface = theRunBotUserIdProvider
        self.__twitchFriendsUserIdProvider: TwitchFriendsUserIdRepositoryInterface = twitchFriendsUserIdProvider
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__additionalImmuneUserIds: frozenset[str] | None = additionalImmuneUserIds

        self.__userIds: frozenset[str] | None = None
        self.__twitchUserId: str | None = None

    async def __getTwitchUserId(self) -> str:
        twitchUserId = self.__twitchUserId

        if twitchUserId is None:
            twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
            twitchUserId = await self.__userIdsRepository.requireUserId(twitchHandle)
            self.__twitchUserId = twitchUserId

        return twitchUserId

    async def getUserIds(self) -> frozenset[str]:
        userIds = self.__userIds

        if userIds is not None:
            return userIds

        newUserIds: set[str] = set()
        newUserIds.add(await self.__getTwitchUserId())

        if self.__additionalImmuneUserIds is not None and len(self.__additionalImmuneUserIds) >= 1:
            newUserIds.update(self.__additionalImmuneUserIds)

        cynanBotUserId = await self.__cynanBotUserIdsProvider.getCynanBotUserId()
        if utils.isValidStr(cynanBotUserId):
            newUserIds.add(cynanBotUserId)

        cynanBotTtsUserId = await self.__cynanBotUserIdsProvider.getCynanBotTtsUserId()
        if utils.isValidStr(cynanBotTtsUserId):
            newUserIds.add(cynanBotTtsUserId)

        funtoonUserId = await self.__funtoonUserIdProvider.getFuntoonUserId()
        if utils.isValidStr(funtoonUserId):
            newUserIds.add(funtoonUserId)

        mandooBotUserId = await self.__twitchFriendsUserIdProvider.getMandooBotUserId()
        if utils.isValidStr(mandooBotUserId):
            newUserIds.add(mandooBotUserId)

        nightbotUserId = await self.__nightbotUserIdProvider.getNightbotUserId()
        if utils.isValidStr(nightbotUserId):
            newUserIds.add(nightbotUserId)

        oathyBotUserId = await self.__twitchFriendsUserIdProvider.getOathyBotUserId()
        if utils.isValidStr(oathyBotUserId):
            newUserIds.add(oathyBotUserId)

        puptimeUserId = await self.__puptimeUserIdProvider.getPuptimeUserId()
        if utils.isValidStr(puptimeUserId):
            newUserIds.add(puptimeUserId)

        seryBotUserId = await self.__seryBotUserIdProvider.getSeryBotUserId()
        if utils.isValidStr(seryBotUserId):
            newUserIds.add(seryBotUserId)

        soundAlertsUserId = await self.__officialTwitchAccountUserIdProvider.getSoundAlertsUserId()
        if utils.isValidStr(soundAlertsUserId):
            newUserIds.add(soundAlertsUserId)

        streamElementsUserId = await self.__streamElementsUserIdProvider.getStreamElementsUserId()
        if utils.isValidStr(streamElementsUserId):
            newUserIds.add(streamElementsUserId)

        streamLabsUserId = await self.__streamLabsUserIdProvider.getStreamLabsUserId()
        if utils.isValidStr(streamLabsUserId):
            newUserIds.add(streamLabsUserId)

        tangiaBotUserId = await self.__tangiaBotUserIdProvider.getTangiaBotUserId()
        if utils.isValidStr(tangiaBotUserId):
            newUserIds.add(tangiaBotUserId)

        theRunBotUserId = await self.__theRunBotUserIdProvider.getTheRunBotUserId()
        if utils.isValidStr(theRunBotUserId):
            newUserIds.add(theRunBotUserId)

        twitchAccountUserId = await self.__officialTwitchAccountUserIdProvider.getTwitchAccountUserId()
        if utils.isValidStr(twitchAccountUserId):
            newUserIds.add(twitchAccountUserId)

        twitchAnonymousGifterUserId = await self.__officialTwitchAccountUserIdProvider.getTwitchAnonymousGifterUserId()
        if utils.isValidStr(twitchAnonymousGifterUserId):
            newUserIds.add(twitchAnonymousGifterUserId)

        valorantUserId = await self.__officialTwitchAccountUserIdProvider.getValorantUserId()
        if utils.isValidStr(valorantUserId):
            newUserIds.add(valorantUserId)

        frozenUserIds: frozenset[str] = frozenset(newUserIds)
        self.__userIds = frozenUserIds
        return frozenUserIds

    async def isImmune(self, userId: str) -> bool:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        userIds = await self.getUserIds()
        return userId in userIds
