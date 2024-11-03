from .timeoutActionHelperInterface import TimeoutActionHelperInterface
from ..misc import utils as utils
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ..twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ..twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ..twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from ..twitch.twitchConstantsInterface import TwitchConstantsInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userInterface import UserInterface


class TimeoutActionHelper(TimeoutActionHelperInterface):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchConstants: TwitchConstantsInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchConstants, TwitchConstantsInterface):
            raise TypeError(f'twitchConstants argument is malformed: \"{twitchConstants}\"')
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__trollmojiHelper: TrollmojiHelperInterface = trollmojiHelper
        self.__twitchConstants: TwitchConstantsInterface = twitchConstants
        self.__twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface = twitchFollowingStatusRepository
        self.__twitchTimeoutHelper: TwitchTimeoutHelperInterface = twitchTimeoutHelper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    async def timeout(
        self,
        bits: int | None,
        durationSeconds: int,
        broadcasterUserId: str,
        chatMessage: str | None,
        instigatorUserId: str,
        instigatorUserName: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        pointRedemptionEventId: str | None,
        pointRedemptionMessage: str | None,
        pointRedemptionRewardId: str | None,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        userIdToTimeout: str,
        userNameToTimeout: str,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits is not None and (bits < 0 or bits > utils.getIntMaxSafeSize()):
            raise ValueError(f'bits argument is out of bounds: \"{bits}\"')
        elif not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > self.__twitchConstants.maxTimeoutSeconds:
            raise ValueError(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif chatMessage is not None and not isinstance(chatMessage, str):
            raise TypeError(f'chatMessage argument is malformed: \"{chatMessage}\"')
        elif not utils.isValidStr(instigatorUserId):
            raise TypeError(f'instigatorUserId argument is malformed: \"{instigatorUserId}\"')
        elif not utils.isValidStr(instigatorUserName):
            raise TypeError(f'instigatorUserName argument is malformed: \"{instigatorUserName}\"')
        elif not utils.isValidStr(moderatorTwitchAccessToken):
            raise TypeError(f'moderatorTwitchAccessToken argument is malformed: \"{moderatorTwitchAccessToken}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif pointRedemptionEventId is not None and not isinstance(pointRedemptionEventId, str):
            raise TypeError(f'pointRedemptionEventId argument is malformed: \"{pointRedemptionEventId}\"')
        elif pointRedemptionMessage is not None and not isinstance(pointRedemptionMessage, str):
            raise TypeError(f'pointRedemptionMessage argument is malformed: \"{pointRedemptionMessage}\"')
        elif pointRedemptionRewardId is not None and not isinstance(pointRedemptionRewardId, str):
            raise TypeError(f'pointRedemptionRewardId argument is malformed: \"{pointRedemptionRewardId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')
        elif not utils.isValidStr(userNameToTimeout):
            raise TypeError(f'userNameToTimeout argument is malformed: \"{userNameToTimeout}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        return False
