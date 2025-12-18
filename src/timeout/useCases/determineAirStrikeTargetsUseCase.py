import random
import traceback
from typing import Final

from frozenlist import FrozenList

from ..exceptions import UnknownTimeoutTargetException
from ..models.actions.airStrikeTimeoutAction import AirStrikeTimeoutAction
from ..models.timeoutTarget import TimeoutTarget
from ..settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.activeChatters.activeChatter import ActiveChatter
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...users.exceptions import NoSuchUserException
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class DetermineAirStrikeTargetsUseCase:

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        timber: TimberInterface,
        timeoutActionSettings: TimeoutActionSettingsInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
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
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__timber: Final[TimberInterface] = timber
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

        try:
            return await self.__userIdsRepository.requireUserName(
                userId = userId,
                twitchAccessToken = twitchAccessToken,
            )
        except NoSuchUserException as e:
            self.__timber.log('DetermineAirStrikeTargetsUseCase', f'Failed to fetch timeout target\'s username ({twitchChannelId=}) ({userId=}): {e}', e, traceback.format_exc())
            raise UnknownTimeoutTargetException(f'Failed to fetch timeout target\'s username ({twitchChannelId=}) ({userId=})')

    async def invoke(
        self,
        timeoutAction: AirStrikeTimeoutAction,
    ) -> FrozenList[TimeoutTarget]:
        if not isinstance(timeoutAction, AirStrikeTimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')

        timeoutTargets: set[TimeoutTarget] = set()

        additionalReverseProbability = await self.__timeoutActionSettings.getGrenadeAdditionalReverseProbability()
        randomReverseNumber = random.random()

        if randomReverseNumber <= additionalReverseProbability:
            targetUserName = await self.__fetchUserName(
                twitchChannelId = timeoutAction.twitchChannelId,
                userId = timeoutAction.instigatorUserId,
            )

            timeoutTargets.add(TimeoutTarget(
                userId = timeoutAction.instigatorUserId,
                userName = targetUserName,
            ))

        activeChatters = await self.__activeChattersRepository.get(
            twitchChannelId = timeoutAction.twitchChannelId,
        )

        vulnerableChatters: dict[str, ActiveChatter] = dict(activeChatters)
        vulnerableChatters.pop(timeoutAction.twitchChannelId, None)

        allImmuneUserIds = await self.__timeoutImmuneUserIdsRepository.getAllUserIds()

        for immuneUserId in allImmuneUserIds:
            vulnerableChatters.pop(immuneUserId, None)

        airStrikeTargetCount = random.randint(timeoutAction.minTimeoutTargets, timeoutAction.maxTimeoutTargets)
        vulnerableChattersList: list[ActiveChatter] = list(vulnerableChatters.values())

        while len(timeoutTargets) < airStrikeTargetCount and len(vulnerableChattersList) >= 1:
            randomChatterIndex = random.randint(0, len(vulnerableChattersList) - 1)
            randomChatter = vulnerableChattersList[randomChatterIndex]
            del vulnerableChattersList[randomChatterIndex]

            timeoutTargets.add(TimeoutTarget(
                userId = randomChatter.chatterUserId,
                userName = randomChatter.chatterUserName,
            ))

            await self.__activeChattersRepository.remove(
                chatterUserId = randomChatter.chatterUserId,
                twitchChannelId = timeoutAction.twitchChannelId,
            )

        timeoutTargetsList: list[TimeoutTarget] = list(timeoutTargets)
        timeoutTargetsList.sort(key = lambda target: target.userName.casefold())

        frozenTimeoutTargetsList: FrozenList[TimeoutTarget] = FrozenList(timeoutTargetsList)
        frozenTimeoutTargetsList.freeze()

        return frozenTimeoutTargetsList
