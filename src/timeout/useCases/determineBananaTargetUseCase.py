import random
import re
import traceback
from dataclasses import dataclass
from typing import Final, Pattern

from ..exceptions import BananaTimeoutDiceRollFailedException, UnknownTimeoutTargetException
from ..guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from ..models.actions.bananaTimeoutAction import BananaTimeoutAction
from ..models.bananaTimeoutTarget import BananaTimeoutTarget
from ..models.timeoutDiceRoll import TimeoutDiceRoll
from ..models.timeoutDiceRollFailureData import TimeoutDiceRollFailureData
from ..repositories.chatterTimeoutHistoryRepositoryInterface import ChatterTimeoutHistoryRepositoryInterface
from ..settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ...users.exceptions import NoSuchUserException
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


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
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(chatterTimeoutHistoryRepository, ChatterTimeoutHistoryRepositoryInterface):
            raise TypeError(f'chatterTimeoutHistoryRepository argument is malformed: \"{chatterTimeoutHistoryRepository}\"')
        elif not isinstance(guaranteedTimeoutUsersRepository, GuaranteedTimeoutUsersRepositoryInterface):
            raise TypeError(f'guaranteedTimeoutUsersRepository argument is malformed: \"{guaranteedTimeoutUsersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionSettings, TimeoutActionSettingsInterface):
            raise TypeError(f'timeoutActionSettings argument is malformed: \"{timeoutActionSettings}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__chatterTimeoutHistoryRepository: Final[ChatterTimeoutHistoryRepositoryInterface] = chatterTimeoutHistoryRepository
        self.__guaranteedTimeoutUsersRepository: Final[GuaranteedTimeoutUsersRepositoryInterface] = guaranteedTimeoutUsersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionSettings: Final[TimeoutActionSettingsInterface] = timeoutActionSettings
        self.__timeoutImmuneUserIdsRepository: Final[TimeoutImmuneUserIdsRepositoryInterface] = timeoutImmuneUserIdsRepository
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchMessageStringUtils: Final[TwitchMessageStringUtilsInterface] = twitchMessageStringUtils
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__timeoutTargetRegEx: Final[Pattern] = re.compile(r'^\s*@?(\w+)\s*', re.IGNORECASE)

    async def __determineTargetUserName(
        self,
        timeoutAction: BananaTimeoutAction,
    ) -> str:
        messageContainingTarget: str | None = timeoutAction.chatMessage

        if not utils.isValidStr(messageContainingTarget) and timeoutAction.pointRedemption is not None:
            messageContainingTarget = timeoutAction.pointRedemption.message

        if not utils.isValidStr(messageContainingTarget):
            raise UnknownTimeoutTargetException(f'Given empty/blank/malformed timeout target message ({timeoutAction=}) ({messageContainingTarget=})')

        messageContainingTarget = await self.__twitchMessageStringUtils.removeCheerStrings(messageContainingTarget)

        if not utils.isValidStr(messageContainingTarget):
            raise UnknownTimeoutTargetException(f'Given empty/blank/malformed timeout target message ({timeoutAction=}) ({messageContainingTarget=})')

        targetMatch = self.__timeoutTargetRegEx.match(messageContainingTarget)

        if targetMatch is None:
            raise UnknownTimeoutTargetException(f'Given empty/blank/malformed timeout target message ({timeoutAction=}) ({messageContainingTarget=}) ({targetMatch=})')

        targetUserName: str | None = targetMatch.group(1)

        if not utils.isValidStr(targetUserName):
            raise UnknownTimeoutTargetException(f'Given empty/blank/malformed timeout target message ({timeoutAction=}) ({messageContainingTarget=}) ({targetMatch=}) ({targetUserName=})')

        return targetUserName

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

    async def __fetchUserId(
        self,
        twitchChannelId: str,
        userName: str | None,
    ) -> str:
        if not utils.isValidStr(userName):
            raise UnknownTimeoutTargetException(f'Given invalid/unknown timeout target ({twitchChannelId=}) ({userName=})')

        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId,
        )

        try:
            return await self.__userIdsRepository.requireUserId(
                userName = userName,
                twitchAccessToken = twitchAccessToken,
            )
        except NoSuchUserException as e:
            self.__timber.log('DetermineBananaTargetUseCase', f'Failed to fetch user ID to use as a timeout target ({twitchChannelId=}) ({userName=}): {e}', e, traceback.format_exc())
            raise UnknownTimeoutTargetException(f'Failed to fetch user ID to use as a timeout target ({twitchChannelId=}) ({userName=})')

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
        timeoutAction: BananaTimeoutAction,
        instigatorUserName: str,
    ) -> ResultData:
        if not isinstance(timeoutAction, BananaTimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')
        elif not utils.isValidStr(instigatorUserName):
            raise TypeError(f'instigatorUserName argument is malformed: \"{instigatorUserName}\"')

        targetUserName = await self.__determineTargetUserName(
            timeoutAction = timeoutAction,
        )

        targetUserId = await self.__fetchUserId(
            twitchChannelId = timeoutAction.twitchChannelId,
            userName = targetUserName,
        )

        if targetUserId == timeoutAction.twitchChannelId:
            targetUserId = timeoutAction.instigatorUserId

        isTryingToTimeoutThemselves = targetUserId == timeoutAction.instigatorUserId

        isGuaranteedTimeoutTarget = await self.__guaranteedTimeoutUsersRepository.isGuaranteed(
            userId = targetUserId,
        )

        if isTryingToTimeoutThemselves or isGuaranteedTimeoutTarget or not timeoutAction.isRandomChanceEnabled:
            return DetermineBananaTargetUseCase.ResultData(
                timeoutTarget = BananaTimeoutTarget(
                    targetUserId = targetUserId,
                    targetUserName = targetUserName,
                ),
                isReverse = targetUserId == timeoutAction.twitchChannelId or isTryingToTimeoutThemselves,
                diceRoll = None,
                diceRollFailureData = None,
            )

        diceRoll = await self.__generateDiceRoll()

        diceRollFailureData = await self.__generateDiceRollFailureData(
            timeoutAction = timeoutAction,
            targetUserId = targetUserId,
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
                    targetUserId = targetUserId,
                    targetUserName = targetUserName,
                ),
                diceRoll = diceRoll,
                diceRollFailureData = diceRollFailureData,
            )
        else:
            return DetermineBananaTargetUseCase.ResultData(
                timeoutTarget = BananaTimeoutTarget(
                    targetUserId = targetUserId,
                    targetUserName = targetUserName,
                ),
                isReverse = False,
                diceRoll = diceRoll,
                diceRollFailureData = diceRollFailureData,
            )
