import random
from typing import Final

from frozenlist import FrozenList

from ..models.airStrikeTargetData import AirStrikeTargetData
from ..models.airStrikeTimeoutAction import AirStrikeTimeoutAction
from ..settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.activeChatters.activeChatter import ActiveChatter
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
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

        return await self.__userIdsRepository.requireUserName(
            userId = userId,
            twitchAccessToken = twitchAccessToken,
        )

    async def invoke(
        self,
        timeoutAction: AirStrikeTimeoutAction,
    ) -> FrozenList[AirStrikeTargetData]:
        if not isinstance(timeoutAction, AirStrikeTimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')

        airStrikeTargets: set[AirStrikeTargetData] = set()

        additionalReverseProbability = await self.__timeoutActionSettings.getGrenadeAdditionalReverseProbability()
        randomReverseNumber = random.random()

        if randomReverseNumber <= additionalReverseProbability:
            airStrikeTargets.add(AirStrikeTargetData(
                targetUserId = timeoutAction.instigatorUserId,
                targetUserName = await self.__fetchUserName(
                    twitchChannelId = timeoutAction.twitchChannelId,
                    userId = timeoutAction.instigatorUserId,
                ),
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

        while len(airStrikeTargets) < airStrikeTargetCount and len(vulnerableChattersList) >= 1:
            randomChatterIndex = random.randint(0, len(vulnerableChattersList) - 1)
            randomChatter = vulnerableChattersList[randomChatterIndex]
            del vulnerableChattersList[randomChatterIndex]

            airStrikeTargets.add(AirStrikeTargetData(
                targetUserId = randomChatter.chatterUserId,
                targetUserName = randomChatter.chatterUserName,
            ))

            await self.__activeChattersRepository.remove(
                chatterUserId = randomChatter.chatterUserId,
                twitchChannelId = timeoutAction.twitchChannelId,
            )

        airStrikeTargetsList: list[AirStrikeTargetData] = list(airStrikeTargets)
        airStrikeTargetsList.sort(key = lambda target: target.targetUserName.casefold())

        frozenAirStrikeTargetsList: FrozenList[AirStrikeTargetData] = FrozenList(airStrikeTargetsList)
        frozenAirStrikeTargetsList.freeze()

        return frozenAirStrikeTargetsList
