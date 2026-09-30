from typing import Collection, Final

from frozenlist import FrozenList

from .determineTm36SplashTargetsUseCaseInterface import DetermineTm36SplashTargetsUseCaseInterface
from ..models.actions.tm36TimeoutAction import Tm36TimeoutAction
from ..models.timeoutTarget import TimeoutTarget
from ..settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ...misc.randomUtilsInterface import RandomUtilsInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.activeChatters.activeChatter import ActiveChatter
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface


class DetermineTm36SplashTargetsUseCase(DetermineTm36SplashTargetsUseCaseInterface):

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        randomUtils: RandomUtilsInterface,
        timber: TimberInterface,
        timeoutActionSettings: TimeoutActionSettingsInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(randomUtils, RandomUtilsInterface):
            raise TypeError(f'randomUtils argument is malformed: \"{randomUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionSettings, TimeoutActionSettingsInterface):
            raise TypeError(f'timeoutActionSettings argument is malformed: \"{timeoutActionSettings}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__randomUtils: Final[RandomUtilsInterface] = randomUtils
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionSettings: Final[TimeoutActionSettingsInterface] = timeoutActionSettings
        self.__timeoutImmuneUserIdsRepository: Final[TimeoutImmuneUserIdsRepositoryInterface] = timeoutImmuneUserIdsRepository

    async def invoke(
        self,
        timeoutAction: Tm36TimeoutAction,
    ) -> Collection[TimeoutTarget]:
        if not isinstance(timeoutAction, Tm36TimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')

        splashDamageProbability = await self.__timeoutActionSettings.getTm36SplashDamageProbability()
        randomSplashNumber = self.__randomUtils.float()
        successfulSplash = randomSplashNumber < splashDamageProbability

        self.__timber.log('DetermineTm36SplashTargetsUseCase', f'Rolled for splash damage ({successfulSplash=}) ({splashDamageProbability=}) ({randomSplashNumber=}) ({timeoutAction=})')

        splashTargets: FrozenList[TimeoutTarget] = FrozenList()

        if not successfulSplash:
            splashTargets.freeze()
            return splashTargets

        activeChatters = await self.__activeChattersRepository.get(
            twitchChannelId = timeoutAction.twitchChannelId,
        )

        vulnerableChatters: dict[str, ActiveChatter] = dict(activeChatters)
        vulnerableChatters.pop(timeoutAction.targetUserId, None)
        vulnerableChatters.pop(timeoutAction.twitchChannelId, None)

        allImmuneUserIds = await self.__timeoutImmuneUserIdsRepository.getAllUserIds()

        for immuneUserId in allImmuneUserIds:
            vulnerableChatters.pop(immuneUserId, None)

        if len(vulnerableChatters) == 0:
            self.__timber.log('DetermineTm36SplashTargetsUseCase', f'Attempted to timeout random target, but no active chatter(s) were found ({successfulSplash=}) ({splashDamageProbability=}) ({randomSplashNumber=}) ({timeoutAction=}) ({activeChatters=}) ({vulnerableChatters=})')
            splashTargets.freeze()
            return splashTargets

        randomlySortedChatters: list[ActiveChatter] = list(vulnerableChatters.values())
        self.__randomUtils.shuffle(randomlySortedChatters)

        rollAgain = True
        maxTargets = await self.__timeoutActionSettings.getTm36MaxSplashDamageTargets()

        while rollAgain and len(randomlySortedChatters) >= 1 and len(splashTargets) < maxTargets:
            randomChatter = randomlySortedChatters.pop()

            splashTargets.append(TimeoutTarget(
                userId = randomChatter.chatterUserId,
                userLogin = randomChatter.chatterUserLogin,
                userName = randomChatter.chatterUserName,
            ))

            rollAgain = self.__randomUtils.bool()

        splashTargets.freeze()
        return splashTargets
