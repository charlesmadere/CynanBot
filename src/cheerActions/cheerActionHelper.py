from typing import Final

from .airStrike.airStrikeCheerActionHelperInterface import AirStrikeCheerActionHelperInterface
from .beanChance.beanChanceCheerActionHelperInterface import BeanChanceCheerActionHelperInterface
from .cheerActionHelperInterface import CheerActionHelperInterface
from .cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from .crowdControl.crowdControlCheerActionHelperInterface import CrowdControlCheerActionHelperInterface
from .soundAlert.soundAlertCheerActionHelperInterface import SoundAlertCheerActionHelperInterface
from .timeout.timeoutCheerActionHelperInterface import TimeoutCheerActionHelperInterface
from .voicemail.voicemailCheerActionHelperInterface import VoicemailCheerActionHelperInterface
from ..misc import utils as utils
from ..twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.userInterface import UserInterface


class CheerActionHelper(CheerActionHelperInterface):

    def __init__(
        self,
        airStrikeCheerActionHelper: AirStrikeCheerActionHelperInterface | None,
        beanChanceCheerActionHelper: BeanChanceCheerActionHelperInterface | None,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        crowdControlCheerActionHelper: CrowdControlCheerActionHelperInterface | None,
        soundAlertCheerActionHelper: SoundAlertCheerActionHelperInterface | None,
        timeoutCheerActionHelper: TimeoutCheerActionHelperInterface | None,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        voicemailCheerActionHelper: VoicemailCheerActionHelperInterface | None
    ):
        if airStrikeCheerActionHelper is not None and not isinstance(airStrikeCheerActionHelper, AirStrikeCheerActionHelperInterface):
            raise TypeError(f'airStrikeCheerActionHelper argument is malformed: \"{airStrikeCheerActionHelper}\"')
        elif beanChanceCheerActionHelper is not None and not isinstance(beanChanceCheerActionHelper, BeanChanceCheerActionHelperInterface):
            raise TypeError(f'beanChanceCheerActionHelper argument is malformed: \"{beanChanceCheerActionHelper}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif crowdControlCheerActionHelper is not None and not isinstance(crowdControlCheerActionHelper, CrowdControlCheerActionHelperInterface):
            raise TypeError(f'crowdControlCheerActionHelper argument is malformed: \"{crowdControlCheerActionHelper}\"')
        elif soundAlertCheerActionHelper is not None and not isinstance(soundAlertCheerActionHelper, SoundAlertCheerActionHelperInterface):
            raise TypeError(f'soundAlertCheerActionHelper argument is malformed: \"{soundAlertCheerActionHelper}\"')
        elif timeoutCheerActionHelper is not None and not isinstance(timeoutCheerActionHelper, TimeoutCheerActionHelperInterface):
            raise TypeError(f'timeoutCheerActionHelper argument is malformed: \"{timeoutCheerActionHelper}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif voicemailCheerActionHelper is not None and not isinstance(voicemailCheerActionHelper, VoicemailCheerActionHelperInterface):
            raise TypeError(f'voicemailCheerActionHelper argument is malformed: \"{voicemailCheerActionHelper}\"')

        self.__airStrikeCheerActionHelper: Final[AirStrikeCheerActionHelperInterface | None] = airStrikeCheerActionHelper
        self.__beanChanceCheerActionHelper: Final[BeanChanceCheerActionHelperInterface | None] = beanChanceCheerActionHelper
        self.__cheerActionsRepository: Final[CheerActionsRepositoryInterface] = cheerActionsRepository
        self.__crowdControlCheerActionHelper: Final[CrowdControlCheerActionHelperInterface | None] = crowdControlCheerActionHelper
        self.__soundAlertCheerActionHelper: Final[SoundAlertCheerActionHelperInterface | None] = soundAlertCheerActionHelper
        self.__timeoutCheerActionHelper: Final[TimeoutCheerActionHelperInterface | None] = timeoutCheerActionHelper
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__voicemailCheerActionHelper: Final[VoicemailCheerActionHelperInterface | None] = voicemailCheerActionHelper

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

        actions = await self.__cheerActionsRepository.getActions(
            twitchChannelId = broadcasterUserId
        )

        if actions is None or len(actions) == 0:
            return False

        elif self.__airStrikeCheerActionHelper is not None and await self.__airStrikeCheerActionHelper.handleAirStrikeCheerAction(
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

        elif self.__beanChanceCheerActionHelper is not None and await self.__beanChanceCheerActionHelper.handleBeanChanceCheerAction(
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

        elif self.__crowdControlCheerActionHelper is not None and await self.__crowdControlCheerActionHelper.handleCrowdControlCheerAction(
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

        elif self.__soundAlertCheerActionHelper is not None and await self.__soundAlertCheerActionHelper.handleSoundAlertCheerAction(
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

        elif self.__timeoutCheerActionHelper is not None and await self.__timeoutCheerActionHelper.handleTimeoutCheerAction(
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

        elif self.__voicemailCheerActionHelper is not None and await self.__voicemailCheerActionHelper.handleVoicemailCheerAction(
            actions = actions,
            bits = bits,
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            message = message,
            twitchChatMessageId = twitchChatMessageId,
            userTwitchAccessToken = userTwitchAccessToken,
            user = user
        ):
            return True

        # if and/or when we add more cheer actions in the future, those would go here

        else:
            return False
