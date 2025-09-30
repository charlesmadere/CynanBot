import random
from dataclasses import dataclass
from typing import Final

from ..exceptions import BananaTimeoutDiceRollFailedException
from ..guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from ..models.absTimeoutTarget import AbsTimeoutTarget
from ..models.actions.bananaTimeoutAction import BananaTimeoutAction
from ..models.bananaTimeoutTarget import BananaTimeoutTarget
from ..models.timeoutDiceRoll import TimeoutDiceRoll
from ..models.timeoutDiceRollFailureData import TimeoutDiceRollFailureData
from ..repositories.chatterTimeoutHistoryRepositoryInterface import ChatterTimeoutHistoryRepositoryInterface
from ..settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface


class DetermineBananaTargetUseCase:

    @dataclass(frozen = True)
    class ResultData:
        timeoutTarget: BananaTimeoutTarget
        isReverse: bool
        diceRoll: TimeoutDiceRoll | None
        diceRollFailureData: TimeoutDiceRollFailureData | None

    def __init__(
        self,
        chatterTimeoutHistoryRepository: ChatterTimeoutHistoryRepositoryInterface,
        guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface,
        timber: TimberInterface,
        timeoutActionSettings: TimeoutActionSettingsInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
    ):
        if not isinstance(chatterTimeoutHistoryRepository, ChatterTimeoutHistoryRepositoryInterface):
            raise TypeError(f'chatterTimeoutHistoryRepository argument is malformed: \"{chatterTimeoutHistoryRepository}\"')
        elif not isinstance(guaranteedTimeoutUsersRepository, GuaranteedTimeoutUsersRepositoryInterface):
            raise TypeError(f'guaranteedTimeoutUsersRepository argument is malformed: \"{guaranteedTimeoutUsersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionSettings, TimeoutActionSettingsInterface):
            raise TypeError(f'timeoutActionSettings argument is malformed: \"{timeoutActionSettings}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')

        self.__chatterTimeoutHistoryRepository: Final[ChatterTimeoutHistoryRepositoryInterface] = chatterTimeoutHistoryRepository
        self.__guaranteedTimeoutUsersRepository: Final[GuaranteedTimeoutUsersRepositoryInterface] = guaranteedTimeoutUsersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionSettings: Final[TimeoutActionSettingsInterface] = timeoutActionSettings
        self.__twitchMessageStringUtils: Final[TwitchMessageStringUtilsInterface] = twitchMessageStringUtils
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils

    async def __fetchBullyOccurrenceCount(
        self,
        targetUserId: str,
        twitchChannelId: str,
    ) -> int:
        if not await self.__timeoutActionSettings.isBullyBasedIncreasedFailureRateEnabled():
            return 0

        chatterTimeoutHistory = await self.__chatterTimeoutHistoryRepository.get(
            chatterUserId = targetUserId,
            twitchChannelId = twitchChannelId,
        )

        return len(chatterTimeoutHistory.entries)

    async def __generateDiceRoll(self) -> TimeoutDiceRoll:
        dieSize = await self.__timeoutActionSettings.getDieSize()
        roll = random.randint(1, dieSize)

        return TimeoutDiceRoll(
            dieSize = dieSize,
            roll = roll,
        )

    async def __generateDiceRollFailureData(
        self,
        timeoutAction: BananaTimeoutAction,
        targetUserId: str,
        diceRoll: TimeoutDiceRoll,
    ) -> TimeoutDiceRollFailureData:
        baseFailureProbability = await self.__timeoutActionSettings.getFailureProbability()
        maxBullyFailureProbability = await self.__timeoutActionSettings.getMaxBullyFailureProbability()
        maxBullyFailureOccurrences = await self.__timeoutActionSettings.getMaxBullyFailureOccurrences()
        perBullyFailureProbabilityIncrease = (maxBullyFailureProbability - baseFailureProbability) / float(maxBullyFailureOccurrences)

        bullyOccurrences = await self.__fetchBullyOccurrenceCount(
            targetUserId = targetUserId,
            twitchChannelId = timeoutAction.twitchChannelId,
        )

        failureProbability = baseFailureProbability + (perBullyFailureProbabilityIncrease * float(bullyOccurrences))
        failureProbability = float(min(failureProbability, maxBullyFailureProbability))
        failureRoll = int(round(failureProbability * float(diceRoll.dieSize)))
        failureRoll = int(min(failureRoll, diceRoll.dieSize))

        reverseProbability = await self.__timeoutActionSettings.getReverseProbability()
        reverseRoll = int(round(reverseProbability * float(diceRoll.dieSize)))
        reverseRoll = int(min(reverseRoll, diceRoll.dieSize))

        return TimeoutDiceRollFailureData(
            baseFailureProbability = baseFailureProbability,
            failureProbability = failureProbability,
            maxBullyFailureProbability = maxBullyFailureProbability,
            perBullyFailureProbabilityIncrease = perBullyFailureProbabilityIncrease,
            reverseProbability = reverseProbability,
            bullyOccurrences = bullyOccurrences,
            failureRoll = failureRoll,
            maxBullyFailureOccurrences = maxBullyFailureOccurrences,
            reverseRoll = reverseRoll,
        )

    async def invoke(
        self,
        timeoutTarget: AbsTimeoutTarget,
        timeoutAction: BananaTimeoutAction,
        instigatorUserName: str,
        diceRoll: TimeoutDiceRoll | None,
    ) -> ResultData:
        if not isinstance(timeoutTarget, AbsTimeoutTarget):
            raise TypeError(f'timeoutTarget argument is malformed: \"{timeoutTarget}\"')
        elif not isinstance(timeoutAction, BananaTimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')
        elif not utils.isValidStr(instigatorUserName):
            raise TypeError(f'instigatorUserName argument is malformed: \"{instigatorUserName}\"')
        elif diceRoll is not None and not isinstance(diceRoll, TimeoutDiceRoll):
            raise TypeError(f'diceRoll argument is malformed: \"{diceRoll}\"')

        isTryingToTimeoutThemselves = timeoutTarget.getTargetUserId() == timeoutAction.instigatorUserId

        isGuaranteedTimeoutTarget = await self.__guaranteedTimeoutUsersRepository.isGuaranteed(
            userId = timeoutTarget.getTargetUserId(),
        )

        if isTryingToTimeoutThemselves or isGuaranteedTimeoutTarget or not timeoutAction.isRandomChanceEnabled:
            return DetermineBananaTargetUseCase.ResultData(
                timeoutTarget = BananaTimeoutTarget(
                    targetUserId = timeoutTarget.getTargetUserId(),
                    targetUserName = timeoutTarget.getTargetUserName(),
                ),
                isReverse = timeoutTarget.getTargetUserId() == timeoutAction.twitchChannelId or isTryingToTimeoutThemselves,
                diceRoll = None,
                diceRollFailureData = None,
            )

        if diceRoll is None:
            diceRoll = await self.__generateDiceRoll()

        diceRollFailureData = await self.__generateDiceRollFailureData(
            timeoutAction = timeoutAction,
            targetUserId = timeoutTarget.getTargetUserId(),
            diceRoll = diceRoll,
        )

        if diceRoll.roll < diceRollFailureData.reverseRoll:
            return DetermineBananaTargetUseCase.ResultData(
                timeoutTarget = BananaTimeoutTarget(
                    targetUserId = timeoutAction.instigatorUserId,
                    targetUserName = instigatorUserName,
                ),
                isReverse = True,
                diceRoll = diceRoll,
                diceRollFailureData = diceRollFailureData,
            )
        elif diceRoll.roll <= diceRollFailureData.failureRoll:
            raise BananaTimeoutDiceRollFailedException(
                timeoutTarget = BananaTimeoutTarget(
                    targetUserId = timeoutTarget.getTargetUserId(),
                    targetUserName = timeoutTarget.getTargetUserName(),
                ),
                diceRoll = diceRoll,
                diceRollFailureData = diceRollFailureData,
            )
        else:
            return DetermineBananaTargetUseCase.ResultData(
                timeoutTarget = BananaTimeoutTarget(
                    targetUserId = timeoutTarget.getTargetUserId(),
                    targetUserName = timeoutTarget.getTargetUserName(),
                ),
                isReverse = False,
                diceRoll = diceRoll,
                diceRollFailureData = diceRollFailureData,
            )
