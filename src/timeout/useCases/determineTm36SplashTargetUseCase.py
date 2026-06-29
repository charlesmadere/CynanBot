import random
from typing import Final

from ..models.actions.tm36TimeoutAction import Tm36TimeoutAction
from ..models.timeoutTarget import TimeoutTarget
from ..settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.activeChatters.activeChatter import ActiveChatter
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface


class DetermineTm36SplashTargetUseCase:

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        timber: TimberInterface,
        timeoutActionSettings: TimeoutActionSettingsInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionSettings, TimeoutActionSettingsInterface):
            raise TypeError(f'timeoutActionSettings argument is malformed: \"{timeoutActionSettings}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionSettings: Final[TimeoutActionSettingsInterface] = timeoutActionSettings
        self.__timeoutImmuneUserIdsRepository: Final[TimeoutImmuneUserIdsRepositoryInterface] = timeoutImmuneUserIdsRepository

    async def invoke(
        self,
        timeoutAction: Tm36TimeoutAction,
    ) -> TimeoutTarget | None:
        if not isinstance(timeoutAction, Tm36TimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')

        splashDamageProbability = await self.__timeoutActionSettings.getTm36SplashDamageProbability()
        randomSplashNumber = random.random()

        if randomSplashNumber > splashDamageProbability:
            return None

        activeChatters = await self.__activeChattersRepository.get(
            twitchChannelId = timeoutAction.twitchChannelId,
        )

        vulnerableChatters: dict[str, ActiveChatter] = dict(activeChatters)
        vulnerableChatters.pop(timeoutAction.twitchChannelId, None)

        allImmuneUserIds = await self.__timeoutImmuneUserIdsRepository.getAllUserIds()

        for immuneUserId in allImmuneUserIds:
            vulnerableChatters.pop(immuneUserId, None)

        if len(vulnerableChatters) == 0:
            self.__timber.log('DetermineTm36SplashTargetUseCase', f'Attempted to timeout random target, but no active chatter(s) were found ({timeoutAction=}) ({splashDamageProbability=}) ({randomSplashNumber=}) ({activeChatters=}) ({vulnerableChatters=})')
            return None

        randomChatter = random.choice(list(vulnerableChatters.values()))

        await self.__activeChattersRepository.remove(
            chatterUserId = randomChatter.chatterUserId,
            twitchChannelId = timeoutAction.twitchChannelId,
        )

        return TimeoutTarget(
            userId = randomChatter.chatterUserId,
            userName = randomChatter.chatterUserName,
        )
