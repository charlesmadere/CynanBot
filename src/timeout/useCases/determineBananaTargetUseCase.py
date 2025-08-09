from typing import Final

from ..models.bananaTimeoutAction import BananaTimeoutAction
from ..models.bananaTimeoutTarget import BananaTimeoutTarget
from ..settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ..timeoutActionHistoryRepositoryInterface import TimeoutActionHistoryRepositoryInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class DetermineBananaTargetUseCase:

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        timber: TimberInterface,
        timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface,
        timeoutActionSettings: TimeoutActionSettingsInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionHistoryRepository, TimeoutActionHistoryRepositoryInterface):
            raise TypeError(f'timeoutActionHistoryRepository argument is malformed: \"{timeoutActionHistoryRepository}\"')
        elif not isinstance(timeoutActionSettings, TimeoutActionSettingsInterface):
            raise TypeError(f'timeoutActionSettings argument is malformed: \"{timeoutActionSettings}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionHistoryRepository: Final[TimeoutActionHistoryRepositoryInterface] = timeoutActionHistoryRepository
        self.__timeoutActionSettings: Final[TimeoutActionSettingsInterface] = timeoutActionSettings
        self.__timeoutImmuneUserIdsRepository: Final[TimeoutImmuneUserIdsRepositoryInterface] = timeoutImmuneUserIdsRepository
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

    async def __fetchUserName(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> str:
        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId,
        )

        return await self.__userIdsRepository.requireUserName(
            userId = userId,
            twitchAccessToken = twitchAccessToken,
        )

    async def invoke(
        self,
        timeoutAction: BananaTimeoutAction,
    ) -> BananaTimeoutTarget | None:
        if not isinstance(timeoutAction, BananaTimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')

        # TODO
        return None
