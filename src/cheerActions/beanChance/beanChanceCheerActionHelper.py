import random
from typing import Collection

from .beanChanceCheerAction import BeanChanceCheerAction
from .beanChanceCheerActionHelperInterface import BeanChanceCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ...beanStats.beanStatsRepositoryInterface import BeanStatsRepositoryInterface
from ...beanStats.chatterBeanStats import ChatterBeanStats
from ...misc import utils as utils
from ...soundPlayerManager.soundAlert import SoundAlert
from ...soundPlayerManager.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...timber.timberInterface import TimberInterface
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.configuration.twitchMessageable import TwitchMessageable
from ...twitch.emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface
from ...users.userInterface import UserInterface


class BeanChanceCheerActionHelper(BeanChanceCheerActionHelperInterface):

    def __init__(
        self,
        beanStatsRepository: BeanStatsRepositoryInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        timber: TimberInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchEmotesHelper: TwitchEmotesHelperInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(beanStatsRepository, BeanStatsRepositoryInterface):
            raise TypeError(f'beanStatsRepository argument is malformed: \"{beanStatsRepository}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchEmotesHelper, TwitchEmotesHelperInterface):
            raise TypeError(f'twitchEmotesHelper argument is malformed: \"{twitchEmotesHelper}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__beanStatsRepository: BeanStatsRepositoryInterface = beanStatsRepository
        self.__soundPlayerManagerProvider: SoundPlayerManagerProviderInterface = soundPlayerManagerProvider
        self.__timber: TimberInterface = timber
        self.__trollmojiHelper: TrollmojiHelperInterface = trollmojiHelper
        self.__twitchEmotesHelper: TwitchEmotesHelperInterface = twitchEmotesHelper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __beanStatsToString(self, beanStats: ChatterBeanStats) -> str:
        if not isinstance(beanStats, ChatterBeanStats):
            raise TypeError(f'beanStats argument is malformed: \"{beanStats}\"')

        return f'(bean stats: {beanStats.successfulBeansStr}W - {beanStats.failedBeanAttemptsStr}L)'

    async def handleBeanChanceCheerAction(
        self,
        actions: Collection[AbsCheerAction],
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        twitchChatMessageId: str | None,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        beanAction: BeanChanceCheerAction | None = None

        for action in actions:
            if isinstance(action, BeanChanceCheerAction) and action.isEnabled and action.bits == bits:
                beanAction = action
                break

        if beanAction is None:
            return False

        twitchChannelProvider = self.__twitchChannelProvider
        if twitchChannelProvider is None:
            return False

        return await self.__rollBeanChance(
            action = beanAction,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            twitchChannelId = broadcasterUserId,
            twitchChatMessageId = twitchChatMessageId,
            twitchChannelProvider = twitchChannelProvider,
            user = user
        )

    async def __handleFailRoll(
        self,
        action: BeanChanceCheerAction,
        randomNumber: int,
        cheerUserId: str,
        cheerUserName: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        twitchChannel: TwitchMessageable,
        user: UserInterface
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

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'{emote} Sorry, no 🫘! (you rolled a 🎲 {randomNumber} 🎲, but you needed a roll greater than or equal to {action.randomChance}) {beanStatsMessage}',
            replyMessageId = twitchChatMessageId
        )

    async def __handleSuccessRoll(
        self,
        action: BeanChanceCheerAction,
        randomNumber: int,
        cheerUserId: str,
        cheerUserName: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        twitchChannel: TwitchMessageable,
        user: UserInterface
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

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'{emote} 🫘 {emote} 🫘 {emote} {beanStatsMessage}',
            replyMessageId = twitchChatMessageId
        )

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewSoundPlayerManagerInstance()
        await soundPlayerManager.playSoundAlert(SoundAlert.BEAN)

    async def __rollBeanChance(
        self,
        action: BeanChanceCheerAction,
        cheerUserId: str,
        cheerUserName: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        twitchChannelProvider: TwitchChannelProvider,
        user: UserInterface
    ) -> bool:
        if not isinstance(action, BeanChanceCheerAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise TypeError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.handle)
        randomNumber = int(round(random.random() * float(100)))

        if randomNumber < action.randomChance:
            await self.__handleFailRoll(
                action = action,
                randomNumber = randomNumber,
                cheerUserId = cheerUserId,
                cheerUserName = cheerUserName,
                twitchChannelId = twitchChannelId,
                twitchChatMessageId = twitchChatMessageId,
                twitchChannel = twitchChannel,
                user = user
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
                twitchChannel = twitchChannel,
                user = user
            )

            return True

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
