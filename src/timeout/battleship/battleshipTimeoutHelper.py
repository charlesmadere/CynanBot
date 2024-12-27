import random
from dataclasses import dataclass

from frozenlist import FrozenList

from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...twitch.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..timeoutActionData import TimeoutActionData
from ..timeoutActionHelperInterface import TimeoutActionHelperInterface
from ...twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ...timber.timberInterface import TimberInterface
from ...users.userInterface import UserInterface
from ...twitch.activeChatters.activeChatter import ActiveChatter
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from .battleshipTimeoutHelperInterface import BattleshipTimeoutHelperInterface
from ...misc import utils


class BattleshipTimeoutHelper(BattleshipTimeoutHelperInterface):

    @dataclass(frozen = True)
    class TimeoutTarget:
        userId: str
        userName: str

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        timber: TimberInterface,
        timeoutActionHelper: TimeoutActionHelperInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        self.__activeChattersRepository: ActiveChattersRepositoryInterface = activeChattersRepository
        self.__timber: TimberInterface = timber
        self.__timeoutActionHelper: TimeoutActionHelperInterface = timeoutActionHelper
        self.__timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface = timeoutImmuneUserIdsRepository
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    async def __determineRandomTimeoutTarget(
        self,
        broadcasterUserId: str,
        originUserId: str,
        originUserName: str,
        user: UserInterface
    ) -> TimeoutTarget | None:
        chatters = await self.__activeChattersRepository.get(
            twitchChannelId = broadcasterUserId
        )

        frozenChatters: FrozenList[ActiveChatter] = FrozenList(chatters)
        frozenChatters.freeze()

        if len(frozenChatters) == 0:
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout from {originUserName}:{originUserId} in {user.handle}, but no active chatter was found ({chatters=})')
            return None

        eligibleChatters: list[ActiveChatter] = list()

        for chatter in frozenChatters:
            if not await self.__timeoutImmuneUserIdsRepository.isImmune(chatter.chatterUserId):
                eligibleChatters.append(chatter)

        if len(eligibleChatters) == 0:
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout from {originUserName}:{originUserId} in {user.handle}, but no active chatter was found ({chatters=})')
            return None

        randomChatter = random.choice(eligibleChatters)

        return BattleshipTimeoutHelper.TimeoutTarget(
            userId = randomChatter.chatterUserId,
            userName = randomChatter.chatterUserName
        )

    async def fire(
        self,
        broadcasterUserId: str,
        originUserId: str,
        originUserName: str,
        user: UserInterface
    ) -> bool:
        timeoutTarget = await self.__determineRandomTimeoutTarget(
            broadcasterUserId = broadcasterUserId,
            originUserId = originUserId,
            originUserName = originUserName,
            user = user
        )

        if timeoutTarget is None:
            return False

        moderatorTwitchAccessToken = await self.__twitchTokensRepository.getAccessToken(
            twitchChannel = await self.__twitchHandleProvider.getTwitchHandle()
        )

        if not utils.isValidStr(moderatorTwitchAccessToken):
            return False

        userTwitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = broadcasterUserId
        )

        if not utils.isValidStr(userTwitchAccessToken):
            return False

        moderatorUserId = await self.__userIdsRepository.requireUserId(
            userName = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchAccessToken = userTwitchAccessToken
        )

        return await self.__timeoutActionHelper.timeout(TimeoutActionData(
            isRandomChanceEnabled = False,
            bits = None,
            durationSeconds = 42,
            chatMessage = None,
            instigatorUserId = originUserId,
            instigatorUserName = originUserName,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            pointRedemptionEventId = None,
            pointRedemptionMessage = None,
            pointRedemptionRewardId = None,
            timeoutTargetUserId = timeoutTarget.userId,
            timeoutTargetUserName = timeoutTarget.userName,
            twitchChannelId = broadcasterUserId,
            twitchChatMessageId = None,
            userTwitchAccessToken = userTwitchAccessToken,
            streamStatusRequirement = TimeoutActionData.StreamStatusRequirement.ONLINE,
            user = user
        ))
