from .beanChance.beanChanceCheerActionHelperInterface import BeanChanceCheerActionHelperInterface
from .cheerActionHelperInterface import CheerActionHelperInterface
from .cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from .crowdControl.crowdControlCheerActionHelperInterface import CrowdControlCheerActionHelperInterface
from .soundAlert.soundAlertCheerActionHelperInterface import SoundAlertCheerActionHelperInterface
from .timeout.timeoutCheerActionHelperInterface import TimeoutCheerActionHelperInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.userInterface import UserInterface


class CheerActionHelper(CheerActionHelperInterface):

    def __init__(
        self,
        beanChanceCheerActionHelper: BeanChanceCheerActionHelperInterface | None,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        crowdControlCheerActionHelper: CrowdControlCheerActionHelperInterface | None,
        soundAlertCheerActionHelper: SoundAlertCheerActionHelperInterface | None,
        timber: TimberInterface,
        timeoutCheerActionHelper: TimeoutCheerActionHelperInterface | None,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if beanChanceCheerActionHelper is not None and not isinstance(beanChanceCheerActionHelper, BeanChanceCheerActionHelperInterface):
            raise TypeError(f'beanChanceCheerActionHelper argument is malformed: \"{beanChanceCheerActionHelper}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif crowdControlCheerActionHelper is not None and not isinstance(crowdControlCheerActionHelper, CrowdControlCheerActionHelperInterface):
            raise TypeError(f'crowdControlCheerActionHelper argument is malformed: \"{crowdControlCheerActionHelper}\"')
        elif soundAlertCheerActionHelper is not None and not isinstance(soundAlertCheerActionHelper, SoundAlertCheerActionHelperInterface):
            raise TypeError(f'soundAlertCheerActionHelper argument is malformed: \"{soundAlertCheerActionHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif timeoutCheerActionHelper is not None and not isinstance(timeoutCheerActionHelper, TimeoutCheerActionHelperInterface):
            raise TypeError(f'timeoutCheerActionHelper argument is malformed: \"{timeoutCheerActionHelper}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__beanChanceCheerActionHelper: BeanChanceCheerActionHelperInterface | None = beanChanceCheerActionHelper
        self.__cheerActionsRepository: CheerActionsRepositoryInterface = cheerActionsRepository
        self.__crowdControlCheerActionHelper: CrowdControlCheerActionHelperInterface | None = crowdControlCheerActionHelper
        self.__soundAlertCheerActionHelper: SoundAlertCheerActionHelperInterface | None = soundAlertCheerActionHelper
        self.__timber: TimberInterface = timber
        self.__timeoutCheerActionHelper: TimeoutCheerActionHelperInterface | None = timeoutCheerActionHelper
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    async def handleCheerAction(
        self,
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        twitchChatMessageId: str | None,
        user: UserInterface
    ) -> bool:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'userId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if not user.areCheerActionsEnabled:
            return False

        moderatorTwitchAccessToken = await self.__twitchTokensRepository.requireAccessToken(
            twitchChannel = await self.__twitchHandleProvider.getTwitchHandle()
        )

        userTwitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = broadcasterUserId
        )

        moderatorUserId = await self.__userIdsRepository.requireUserId(
            userName = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchAccessToken = userTwitchAccessToken
        )

        actions = await self.__cheerActionsRepository.getActions(broadcasterUserId)

        if actions is None or len(actions) == 0:
            return False

        if self.__beanChanceCheerActionHelper is not None and await self.__beanChanceCheerActionHelper.handleBeanChanceCheerAction(
            actions = actions,
            bits = bits,
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            message = message,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            twitchChatMessageId = twitchChatMessageId,
            userTwitchAccessToken = userTwitchAccessToken,
            user = user
        ):
            return True

        if self.__crowdControlCheerActionHelper is not None and await self.__crowdControlCheerActionHelper.handleCrowdControlCheerAction(
            actions = actions,
            bits = bits,
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            message = message,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            userTwitchAccessToken = userTwitchAccessToken,
            user = user
        ):
            return True

        if self.__soundAlertCheerActionHelper is not None and await self.__soundAlertCheerActionHelper.handleSoundAlertCheerAction(
            actions = actions,
            bits = bits,
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            message = message,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            userTwitchAccessToken = userTwitchAccessToken,
            user = user
        ):
            return True

        if self.__timeoutCheerActionHelper is not None and await self.__timeoutCheerActionHelper.handleTimeoutCheerAction(
            actions = actions,
            bits = bits,
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            message = message,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            twitchChatMessageId = twitchChatMessageId,
            userTwitchAccessToken = userTwitchAccessToken,
            user = user
        ):
            return True

        # if we have more cheer actions in the future, those would go here
        return False
