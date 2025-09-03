import random
from typing import Final

from frozendict import frozendict

from .beanChanceCheerAction import BeanChanceCheerAction
from .beanChanceCheerActionHelperInterface import BeanChanceCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ...beanStats.beanStatsRepositoryInterface import BeanStatsRepositoryInterface
from ...beanStats.chatterBeanStats import ChatterBeanStats
from ...misc import utils as utils
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.soundAlert import SoundAlert
from ...timber.timberInterface import TimberInterface
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ...twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ...users.userInterface import UserInterface


class BeanChanceCheerActionHelper(BeanChanceCheerActionHelperInterface):

    def __init__(
        self,
        beanStatsRepository: BeanStatsRepositoryInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        timber: TimberInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(beanStatsRepository, BeanStatsRepositoryInterface):
            raise TypeError(f'beanStatsRepository argument is malformed: \"{beanStatsRepository}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__beanStatsRepository: Final[BeanStatsRepositoryInterface] = beanStatsRepository
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__timber: Final[TimberInterface] = timber
        self.__trollmojiHelper: Final[TrollmojiHelperInterface] = trollmojiHelper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

    async def __beanStatsToString(self, beanStats: ChatterBeanStats) -> str:
        if not isinstance(beanStats, ChatterBeanStats):
            raise TypeError(f'beanStats argument is malformed: \"{beanStats}\"')

        return f'(bean stats: {beanStats.successfulBeansStr}W - {beanStats.failedBeanAttemptsStr}L)'

    async def handleBeanChanceCheerAction(
        self,
        actions: frozendict[int, AbsCheerAction],
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        userTwitchAccessToken: str,
        user: UserInterface,
    ) -> bool:
        if not isinstance(actions, frozendict):
            raise TypeError(f'actions argument is malformed: \"{actions}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(moderatorTwitchAccessToken):
            raise TypeError(f'moderatorTwitchAccessToken argument is malformed: \"{moderatorTwitchAccessToken}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        action = actions.get(bits, None)

        if not isinstance(action, BeanChanceCheerAction):
            return False
        elif not action.isEnabled:
            return False
        else:
            return await self.__rollBeanChance(
                action = action,
                cheerUserId = cheerUserId,
                cheerUserName = cheerUserName,
                twitchChannelId = twitchChannelId,
                twitchChatMessageId = twitchChatMessageId,
                user = user,
            )

    async def __handleFailRoll(
        self,
        action: BeanChanceCheerAction,
        randomNumber: int,
        cheerUserId: str,
        cheerUserName: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface,
    ):
        self.__timber.log('BeanChanceCheerActionHelper', f'Attempt to bean by {cheerUserName}:{cheerUserId} in {user.handle} but got a bad roll ({randomNumber=}) ({action=})')

        newBeanStats = await self.__beanStatsRepository.incrementFails(
            chatterUserId = cheerUserId,
            chatterUserName = cheerUserName,
            twitchChannel = user.handle,
            twitchChannelId = twitchChannelId
        )

        beanStatsMessage = await self.__beanStatsToString(newBeanStats)
        emote = await self.__trollmojiHelper.getThumbsDownEmoteOrBackup()

        self.__twitchChatMessenger.send(
            text = f'{emote} Sorry, no 🫘! (you rolled a 🎲 {randomNumber} 🎲, but you needed a roll greater than or equal to {action.randomChance}) {beanStatsMessage}',
            twitchChannelId = twitchChannelId,
            replyMessageId = twitchChatMessageId,
        )

    async def __handleSuccessRoll(
        self,
        action: BeanChanceCheerAction,
        randomNumber: int,
        cheerUserId: str,
        cheerUserName: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface,
    ):
        self.__timber.log('BeanChanceCheerActionHelper', f'Successful bean by {cheerUserName}:{cheerUserId} in {user.handle} ({randomNumber=}) ({action=})')

        newBeanStats = await self.__beanStatsRepository.incrementSuccesses(
            chatterUserId = cheerUserId,
            chatterUserName = cheerUserName,
            twitchChannel = user.handle,
            twitchChannelId = twitchChannelId
        )

        beanStatsMessage = await self.__beanStatsToString(newBeanStats)
        emote = await self.__trollmojiHelper.getHypeEmoteOrBackup()

        self.__twitchChatMessenger.send(
            text = f'{emote} 🫘 {emote} 🫘 {emote} {beanStatsMessage}',
            twitchChannelId = twitchChannelId,
            replyMessageId = twitchChatMessageId,
        )

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
        await soundPlayerManager.playSoundAlert(SoundAlert.BEAN)

    async def __rollBeanChance(
        self,
        action: BeanChanceCheerAction,
        cheerUserId: str,
        cheerUserName: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface
    ) -> bool:
        randomNumber = int(round(random.random() * float(100)))

        if randomNumber < action.randomChance:
            await self.__handleFailRoll(
                action = action,
                randomNumber = randomNumber,
                cheerUserId = cheerUserId,
                cheerUserName = cheerUserName,
                twitchChannelId = twitchChannelId,
                twitchChatMessageId = twitchChatMessageId,
                user = user,
            )

            return False
        else:
            await self.__handleSuccessRoll(
                action = action,
                randomNumber = randomNumber,
                cheerUserId = cheerUserId,
                cheerUserName = cheerUserName,
                twitchChannelId = twitchChannelId,
                twitchChatMessageId = twitchChatMessageId,
                user = user,
            )

            return True
