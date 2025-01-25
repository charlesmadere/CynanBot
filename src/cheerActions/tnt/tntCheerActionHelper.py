import random
from dataclasses import dataclass
from typing import Any

from frozendict import frozendict

from .tntCheerAction import TntCheerAction
from .tntCheerActionHelperInterface import TntCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ..timeout.timeoutCheerActionMapper import TimeoutCheerActionMapper
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...timeout.timeoutActionHelperInterface import TimeoutActionHelperInterface
from ...timeout.timeoutActionSettingsRepositoryInterface import TimeoutActionSettingsRepositoryInterface
from ...twitch.activeChatters.activeChatter import ActiveChatter
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface


class TntCheerActionHelper(TntCheerActionHelperInterface):

    @dataclass(frozen = True)
    class TntTarget:
        userId: str
        userName: str

        def __eq__(self, value: Any) -> bool:
            if isinstance(value, TntCheerActionHelper.TntTarget):
                return self.userId == value.userId
            else:
                return False

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        timber: TimberInterface,
        timeoutActionHelper: TimeoutActionHelperInterface,
        timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface,
        timeoutCheerActionMapper: TimeoutCheerActionMapper,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionHelper, TimeoutActionHelperInterface):
            raise TypeError(f'timeoutActionHelper argument is malformed: \"{timeoutActionHelper}\"')
        elif not isinstance(timeoutActionSettingsRepository, TimeoutActionSettingsRepositoryInterface):
            raise TypeError(f'timeoutActionSettingsRepository argument is malformed: \"{timeoutActionSettingsRepository}\"')
        elif not isinstance(timeoutCheerActionMapper, TimeoutCheerActionMapper):
            raise TypeError(f'timeoutCheerActionMapper argument is malformed: \"{timeoutCheerActionMapper}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__activeChattersRepository: ActiveChattersRepositoryInterface = activeChattersRepository
        self.__timber: TimberInterface = timber
        self.__timeoutActionHelper: TimeoutActionHelperInterface = timeoutActionHelper
        self.__timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface = timeoutActionSettingsRepository
        self.__timeoutCheerActionMapper: TimeoutCheerActionMapper = timeoutCheerActionMapper
        self.__timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface = timeoutImmuneUserIdsRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    async def __determineTntTargets(
        self,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        tntAction: TntCheerAction
    ) -> frozenset[TntTarget]:
        tntTargets: set[TntCheerActionHelper.TntTarget] = set()

        additionalReverseProbability = await self.__timeoutActionSettingsRepository.getGrenadeAdditionalReverseProbability()
        randomReverseNumber = random.random()

        if randomReverseNumber <= additionalReverseProbability:
            tntTargets.add(TntCheerActionHelper.TntTarget(
                userId = cheerUserId,
                userName = cheerUserName
            ))

        chatters = await self.__activeChattersRepository.get(
            twitchChannelId = broadcasterUserId
        )

        eligibleChatters: dict[str, ActiveChatter] = dict()

        for chatter in chatters:
            eligibleChatters[chatter.chatterUserId] = chatter

        eligibleChatters.pop(broadcasterUserId, None)
        immuneUserIds = await self.__timeoutImmuneUserIdsRepository.getUserIds()

        for immuneUserId in immuneUserIds:
            eligibleChatters.pop(immuneUserId, None)

        tntTargetCount = random.randint(tntAction.minTimeoutChatters, tntAction.maxTimeoutChatters)
        eligibleChattersList: list[ActiveChatter] = list(eligibleChatters.values())

        while len(tntTargets) < tntTargetCount and len(eligibleChattersList) >= 1:
            randomChatterIndex = random.randint(0, len(eligibleChattersList) - 1)
            randomChatter = eligibleChattersList[randomChatterIndex]
            del eligibleChattersList[randomChatterIndex]

            tntTargets.add(TntCheerActionHelper.TntTarget(
                userId = randomChatter.chatterUserId,
                userName = randomChatter.chatterUserName
            ))

        frozenTntTargets: frozenset[TntCheerActionHelper.TntTarget] = frozenset(tntTargets)

        for tntTarget in frozenTntTargets:
            await self.__activeChattersRepository.remove(
                chatterUserId = tntTarget.userId,
                twitchChannelId = broadcasterUserId
            )

        self.__timber.log('TntCheerActionHelper', f'Selected TNT target(s) ({tntAction=}) ({additionalReverseProbability=}) ({randomReverseNumber=}) ({tntTargetCount=}) ({frozenTntTargets=})')

        return frozenTntTargets

    async def handleTimeoutCheerAction(
        self,
        actions: frozendict[int, AbsCheerAction],
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        twitchChatMessageId: str | None,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        if not isinstance(actions, frozendict):
            raise TypeError(f'actions argument is malformed: \"{actions}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(moderatorTwitchAccessToken):
            raise TypeError(f'moderatorTwitchAccessToken argument is malformed: \"{moderatorTwitchAccessToken}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        action = actions.get(bits, None)

        if not isinstance(action, TntCheerAction):
            return False
        elif not action.isEnabled:
            return False

        tntTargets = await self.__determineTntTargets(
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            tntAction = action
        )

        if len(tntTargets) == 0:
            return True

        streamStatusRequirement = await self.__timeoutCheerActionMapper.toTimeoutActionDataStreamStatusRequirement(
            streamStatusRequirement = action.streamStatusRequirement
        )

        # TODO
        # self.__timeoutActionHelper.submitTimeout(TimeoutActionData(
        #     isRandomChanceEnabled = False,
        #     bits = bits,
        #     durationSeconds = action.durationSeconds,
        #     chatMessage = message,
        #     instigatorUserId = cheerUserId,
        #     instigatorUserName = cheerUserName,
        #     moderatorTwitchAccessToken = moderatorTwitchAccessToken,
        #     moderatorUserId = moderatorUserId,
        #     pointRedemptionEventId = None,
        #     pointRedemptionMessage = None,
        #     pointRedemptionRewardId = None,
        #     timeoutTargetUserId = timeoutTarget.userId,
        #     timeoutTargetUserName = timeoutTarget.userName,
        #     twitchChannelId = broadcasterUserId,
        #     twitchChatMessageId = twitchChatMessageId,
        #     userTwitchAccessToken = userTwitchAccessToken,
        #     actionType = actionType,
        #     streamStatusRequirement = streamStatusRequirement,
        #     user = user
        # ))

        return True
