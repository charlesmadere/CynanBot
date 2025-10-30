from typing import Final

from .adge.adgeCheerActionHelperInterface import AdgeCheerActionHelperInterface
from .beanChance.beanChanceCheerActionHelperInterface import BeanChanceCheerActionHelperInterface
from .cheerActionHelperInterface import CheerActionHelperInterface
from .cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from .crowdControl.crowdControlCheerActionHelperInterface import CrowdControlCheerActionHelperInterface
from .itemUse.itemUseCheerActionHelperInterface import ItemUseCheerActionHelperInterface
from .soundAlert.soundAlertCheerActionHelperInterface import SoundAlertCheerActionHelperInterface
from ..misc import utils as utils
from ..twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.userInterface import UserInterface


class CheerActionHelper(CheerActionHelperInterface):

    def __init__(
        self,
        adgeCheerActionHelper: AdgeCheerActionHelperInterface | None,
        beanChanceCheerActionHelper: BeanChanceCheerActionHelperInterface | None,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        crowdControlCheerActionHelper: CrowdControlCheerActionHelperInterface | None,
        itemUseCheerActionHelper: ItemUseCheerActionHelperInterface | None,
        soundAlertCheerActionHelper: SoundAlertCheerActionHelperInterface | None,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if adgeCheerActionHelper is not None and not isinstance(adgeCheerActionHelper, AdgeCheerActionHelperInterface):
            raise TypeError(f'adgeCheerActionHelper argument is malformed: \"{adgeCheerActionHelper}\"')
        elif beanChanceCheerActionHelper is not None and not isinstance(beanChanceCheerActionHelper, BeanChanceCheerActionHelperInterface):
            raise TypeError(f'beanChanceCheerActionHelper argument is malformed: \"{beanChanceCheerActionHelper}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif crowdControlCheerActionHelper is not None and not isinstance(crowdControlCheerActionHelper, CrowdControlCheerActionHelperInterface):
            raise TypeError(f'crowdControlCheerActionHelper argument is malformed: \"{crowdControlCheerActionHelper}\"')
        elif itemUseCheerActionHelper is not None and not isinstance(itemUseCheerActionHelper, ItemUseCheerActionHelperInterface):
            raise TypeError(f'itemUseCheerActionHelper argument is malformed: \"{itemUseCheerActionHelper}\"')
        elif soundAlertCheerActionHelper is not None and not isinstance(soundAlertCheerActionHelper, SoundAlertCheerActionHelperInterface):
            raise TypeError(f'soundAlertCheerActionHelper argument is malformed: \"{soundAlertCheerActionHelper}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__adgeCheerActionHelper: Final[AdgeCheerActionHelperInterface | None] = adgeCheerActionHelper
        self.__beanChanceCheerActionHelper: Final[BeanChanceCheerActionHelperInterface | None] = beanChanceCheerActionHelper
        self.__cheerActionsRepository: Final[CheerActionsRepositoryInterface] = cheerActionsRepository
        self.__crowdControlCheerActionHelper: Final[CrowdControlCheerActionHelperInterface | None] = crowdControlCheerActionHelper
        self.__itemUseCheerActionHelper: Final[ItemUseCheerActionHelperInterface | None] = itemUseCheerActionHelper
        self.__soundAlertCheerActionHelper: Final[SoundAlertCheerActionHelperInterface | None] = soundAlertCheerActionHelper
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

    async def handleCheerAction(
        self,
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface,
    ) -> bool:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if not user.areCheerActionsEnabled:
            return False

        userTwitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

        moderatorUserId = await self.__userIdsRepository.requireUserId(
            userName = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchAccessToken = userTwitchAccessToken,
        )

        moderatorTwitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = moderatorUserId,
        )

        actions = await self.__cheerActionsRepository.getActions(
            twitchChannelId = twitchChannelId,
        )

        if actions is None or len(actions) == 0:
            return False

        elif self.__adgeCheerActionHelper is not None and await self.__adgeCheerActionHelper.handleAdgeCheerAction(
            actions = actions,
            bits = bits,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            message = message,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
            userTwitchAccessToken = userTwitchAccessToken,
            user = user,
        ):
            return True

        elif self.__beanChanceCheerActionHelper is not None and await self.__beanChanceCheerActionHelper.handleBeanChanceCheerAction(
            actions = actions,
            bits = bits,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            message = message,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
            userTwitchAccessToken = userTwitchAccessToken,
            user = user,
        ):
            return True

        elif self.__crowdControlCheerActionHelper is not None and await self.__crowdControlCheerActionHelper.handleCrowdControlCheerAction(
            actions = actions,
            bits = bits,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            message = message,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
            userTwitchAccessToken = userTwitchAccessToken,
            user = user,
        ):
            return True

        elif self.__itemUseCheerActionHelper is not None and await self.__itemUseCheerActionHelper.handleItemUseCheerAction(
            actions = actions,
            bits = bits,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            message = message,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
            userTwitchAccessToken = userTwitchAccessToken,
            user = user,
        ):
            return True

        elif self.__soundAlertCheerActionHelper is not None and await self.__soundAlertCheerActionHelper.handleSoundAlertCheerAction(
            actions = actions,
            bits = bits,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            message = message,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            twitchChannelId = twitchChannelId,
            userTwitchAccessToken = userTwitchAccessToken,
            user = user,
        ):
            return True

        # if and/or when we add more cheer actions in the future, those would go here

        else:
            return False
