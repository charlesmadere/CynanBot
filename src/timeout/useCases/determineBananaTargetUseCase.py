import random
from dataclasses import dataclass
from typing import Final

from ..exceptions import BananaTimeoutDiceRollFailedException
from ..guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from ..models.actions.bananaTimeoutAction import BananaTimeoutAction
from ..models.timeoutDiceRoll import TimeoutDiceRoll
from ..models.timeoutDiceRollFailureData import TimeoutDiceRollFailureData
from ..models.timeoutTarget import TimeoutTarget
from ..settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class DetermineBananaTargetUseCase:

    @dataclass(frozen = True, slots = True)
    class ResultData:
        isReverse: bool
        diceRoll: TimeoutDiceRoll | None
        diceRollFailureData: TimeoutDiceRollFailureData | None
        timeoutTarget: TimeoutTarget

    def __init__(
        self,
        guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface,
        timber: TimberInterface,
        timeoutActionSettings: TimeoutActionSettingsInterface,
    ):
        if not isinstance(guaranteedTimeoutUsersRepository, GuaranteedTimeoutUsersRepositoryInterface):
            raise TypeError(f'guaranteedTimeoutUsersRepository argument is malformed: \"{guaranteedTimeoutUsersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionSettings, TimeoutActionSettingsInterface):
            raise TypeError(f'timeoutActionSettings argument is malformed: \"{timeoutActionSettings}\"')

        self.__guaranteedTimeoutUsersRepository: Final[GuaranteedTimeoutUsersRepositoryInterface] = guaranteedTimeoutUsersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionSettings: Final[TimeoutActionSettingsInterface] = timeoutActionSettings

    async def __generateDiceRoll(self) -> TimeoutDiceRoll:
        dieSize = await self.__timeoutActionSettings.getDieSize()
        roll = random.randint(1, dieSize)

        return TimeoutDiceRoll(
            dieSize = dieSize,
            roll = roll,
        )

    async def __generateDiceRollFailureData(
        self,
        diceRoll: TimeoutDiceRoll,
    ) -> TimeoutDiceRollFailureData:
        failureProbability = await self.__timeoutActionSettings.getFailureProbability()
        failureRoll = int(round(failureProbability * float(diceRoll.dieSize)))
        failureRoll = int(min(failureRoll, diceRoll.dieSize))

        reverseProbability = await self.__timeoutActionSettings.getReverseProbability()
        reverseRoll = int(round(reverseProbability * float(diceRoll.dieSize)))
        reverseRoll = int(min(reverseRoll, diceRoll.dieSize))

        return TimeoutDiceRollFailureData(
            failureProbability = failureProbability,
            reverseProbability = reverseProbability,
            failureRoll = failureRoll,
            reverseRoll = reverseRoll,
        )

    async def invoke(
        self,
        timeoutAction: BananaTimeoutAction,
        instigatorUserName: str,
        diceRoll: TimeoutDiceRoll | None,
        timeoutTarget: TimeoutTarget,
    ) -> ResultData:
        if not isinstance(timeoutAction, BananaTimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')
        elif not utils.isValidStr(instigatorUserName):
            raise TypeError(f'instigatorUserName argument is malformed: \"{instigatorUserName}\"')
        elif diceRoll is not None and not isinstance(diceRoll, TimeoutDiceRoll):
            raise TypeError(f'diceRoll argument is malformed: \"{diceRoll}\"')
        elif not isinstance(timeoutTarget, TimeoutTarget):
            raise TypeError(f'timeoutTarget argument is malformed: \"{timeoutTarget}\"')

        isGuaranteedTimeoutTarget = await self.__guaranteedTimeoutUsersRepository.isGuaranteed(
            userId = timeoutTarget.userId,
        )

        isTryingToTimeoutThemselves = timeoutTarget.userId == timeoutAction.instigatorUserId
        isTryingToTimeoutStreamer = timeoutTarget.userId == timeoutAction.twitchChannelId

        if isGuaranteedTimeoutTarget or isTryingToTimeoutThemselves or isTryingToTimeoutStreamer or not timeoutAction.isRandomChanceEnabled:
            return DetermineBananaTargetUseCase.ResultData(
                timeoutTarget = timeoutTarget,
                isReverse = isTryingToTimeoutStreamer,
                diceRoll = None,
                diceRollFailureData = None,
            )

        if diceRoll is None:
            diceRoll = await self.__generateDiceRoll()

        diceRollFailureData = await self.__generateDiceRollFailureData(
            diceRoll = diceRoll,
        )

        self.__timber.log('DetermineBananaTargetUseCase', f'Generated dice roll failure data ({timeoutAction=}) ({instigatorUserName=}) ({timeoutTarget=}) ({diceRoll=}) ({diceRollFailureData=})')

        if diceRoll.roll <= diceRollFailureData.reverseRoll:
            return DetermineBananaTargetUseCase.ResultData(
                timeoutTarget = TimeoutTarget(
                    userId = timeoutAction.instigatorUserId,
                    userName = instigatorUserName,
                ),
                isReverse = True,
                diceRoll = diceRoll,
                diceRollFailureData = diceRollFailureData,
            )

        elif diceRoll.roll <= diceRollFailureData.failureRoll:
            raise BananaTimeoutDiceRollFailedException(
                timeoutTarget = timeoutTarget,
                diceRoll = diceRoll,
                diceRollFailureData = diceRollFailureData,
            )

        else:
            return DetermineBananaTargetUseCase.ResultData(
                timeoutTarget = timeoutTarget,
                isReverse = False,
                diceRoll = diceRoll,
                diceRollFailureData = diceRollFailureData,
            )
