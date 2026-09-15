import random
import traceback
from typing import Final

from ..exceptions import UnknownTimeoutTargetException
from ..models.actions.grenadeTimeoutAction import GrenadeTimeoutAction
from ..models.timeoutTarget import TimeoutTarget
from ..settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.activeChatters.activeChatter import ActiveChatter
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...twitch.userIds.twitchUserData import TwitchUserData
from ...twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface
from ...users.exceptions import NoSuchUserException


class DetermineGrenadeTargetUseCase:

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        timber: TimberInterface,
        timeoutActionSettings: TimeoutActionSettingsInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionSettings, TimeoutActionSettingsInterface):
            raise TypeError(f'timeoutActionSettings argument is malformed: \"{timeoutActionSettings}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionSettings: Final[TimeoutActionSettingsInterface] = timeoutActionSettings
        self.__timeoutImmuneUserIdsRepository: Final[TimeoutImmuneUserIdsRepositoryInterface] = timeoutImmuneUserIdsRepository
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper

    async def __fetchUserData(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> TwitchUserData:
        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId,
        )

        try:
            return await self.__twitchUserIdsHelper.requireById(
                userId = userId,
                twitchAccessToken = twitchAccessToken,
            )
        except NoSuchUserException as e:
            self.__timber.log('DetermineGrenadeTargetUseCase', f'Failed to fetch timeout target\'s username ({twitchChannelId=}) ({userId=})', e, traceback.format_exc())
            raise UnknownTimeoutTargetException(f'Failed to fetch timeout target\'s username ({twitchChannelId=}) ({userId=})')

    async def invoke(
        self,
        timeoutAction: GrenadeTimeoutAction,
    ) -> TimeoutTarget | None:
        if not isinstance(timeoutAction, GrenadeTimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')

        additionalReverseProbability = await self.__timeoutActionSettings.getGrenadeAdditionalReverseProbability()
        randomReverseNumber = random.random()

        if randomReverseNumber <= additionalReverseProbability:
            targetUserData = await self.__fetchUserData(
                twitchChannelId = timeoutAction.twitchChannelId,
                userId = timeoutAction.instigatorUserId,
            )

            return TimeoutTarget(
                userId = timeoutAction.instigatorUserId,
                userLogin = targetUserData.userLogin,
                userName = targetUserData.userName,
            )

        activeChatters = await self.__activeChattersRepository.get(
            twitchChannelId = timeoutAction.twitchChannelId,
        )

        vulnerableChatters: dict[str, ActiveChatter] = dict(activeChatters)
        vulnerableChatters.pop(timeoutAction.twitchChannelId, None)

        allImmuneUserIds = await self.__timeoutImmuneUserIdsRepository.getAllUserIds()

        for immuneUserId in allImmuneUserIds:
            vulnerableChatters.pop(immuneUserId, None)

        if len(vulnerableChatters) == 0:
            self.__timber.log('DetermineGrenadeTargetUseCase', f'Attempted to timeout random target, but no active chatter(s) were found ({timeoutAction=}) ({additionalReverseProbability=}) ({randomReverseNumber=}) ({activeChatters=}) ({vulnerableChatters=})')
            return None

        randomChatter = random.choice(list(vulnerableChatters.values()))

        await self.__activeChattersRepository.remove(
            chatterUserId = randomChatter.chatterUserId,
            twitchChannelId = timeoutAction.twitchChannelId,
        )

        return TimeoutTarget(
            userId = randomChatter.chatterUserId,
            userLogin = randomChatter.chatterUserLogin,
            userName = randomChatter.chatterUserName,
        )
