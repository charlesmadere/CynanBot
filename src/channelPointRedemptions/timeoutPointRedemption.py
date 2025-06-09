import random
from dataclasses import dataclass
from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..timeout.timeoutActionData import TimeoutActionData
from ..timeout.timeoutActionHelperInterface import TimeoutActionHelperInterface
from ..timeout.timeoutActionType import TimeoutActionType
from ..timeout.timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ..twitch.activeChatters.activeChatter import ActiveChatter
from ..twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
from ..twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ..twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.timeout.timeoutBoosterPack import TimeoutBoosterPack
from ..users.timeout.timeoutBoosterPackType import TimeoutBoosterPackType
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.userInterface import UserInterface


class TimeoutPointRedemption(AbsChannelPointRedemption):

    @dataclass(frozen = True)
    class TimeoutTarget:
        userId: str
        userName: str
        actionType: TimeoutActionType

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        timber: TimberInterface,
        timeoutActionHelper: TimeoutActionHelperInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionHelper, TimeoutActionHelperInterface):
            raise TypeError(f'timeoutActionHelper argument is malformed: \"{timeoutActionHelper}\"')
        elif not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionHelper: Final[TimeoutActionHelperInterface] = timeoutActionHelper
        self.__timeoutImmuneUserIdsRepository: Final[TimeoutImmuneUserIdsRepositoryInterface] = timeoutImmuneUserIdsRepository
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchMessageStringUtils: Final[TwitchMessageStringUtilsInterface] = twitchMessageStringUtils
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

    async def __determineRandomTimeoutTarget(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
    ) -> TimeoutTarget | None:
        activeChatters = await self.__activeChattersRepository.get(
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId
        )

        vulnerableChatters: dict[str, ActiveChatter] = dict(activeChatters)
        vulnerableChatters.pop(twitchChannelPointsMessage.twitchChannelId, None)

        allImmuneUserIds = await self.__timeoutImmuneUserIdsRepository.getAllUserIds()

        for immuneUserId in allImmuneUserIds:
            vulnerableChatters.pop(immuneUserId, None)

        if len(vulnerableChatters) == 0:
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout from from {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchChannel.getTwitchChannelName()}, but was unable to find an active chatter: ({twitchChannelPointsMessage=}) ({activeChatters=}) ({vulnerableChatters=})')

            await self.__twitchUtils.safeSend(
                messageable = twitchChannel,
                message = f'⚠ Sorry @{twitchChannelPointsMessage.userName}, no chatter was found'
            )

            return None

        randomChatter = random.choice(list(vulnerableChatters.values()))

        return TimeoutPointRedemption.TimeoutTarget(
            userId = randomChatter.chatterUserId,
            userName = randomChatter.chatterUserName,
            actionType = TimeoutActionType.GRENADE
        )

    async def __determineTimeoutTarget(
        self,
        message: str | None,
        userTwitchAccessToken: str,
        timeoutBoosterPack: TimeoutBoosterPack,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
        twitchUser: UserInterface
    ) -> TimeoutTarget | None:
        timeoutType = timeoutBoosterPack.timeoutType

        match timeoutType:
            case TimeoutBoosterPackType.RANDOM_TARGET:
                return await self.__determineRandomTimeoutTarget(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = twitchChannelPointsMessage
                )

            case TimeoutBoosterPackType.USER_TARGET:
                return await self.__determineUserTimeoutTarget(
                    message = message,
                    userTwitchAccessToken = userTwitchAccessToken,
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = twitchChannelPointsMessage,
                    twitchUser = twitchUser
                )

            case _:
                raise RuntimeError(f'Encountered unknown TimeoutBoosterPackType: \"{timeoutType}\"')

    async def __determineUserTimeoutTarget(
        self,
        message: str | None,
        userTwitchAccessToken: str,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
        twitchUser: UserInterface
    ) -> TimeoutTarget | None:
        timeoutTargetUserName = await self.__twitchMessageStringUtils.getUserNameFromMessage(
            message = message
        )

        if not utils.isValidStr(timeoutTargetUserName):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout \"{timeoutTargetUserName}\" from {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}, but was unable to find a user name: ({twitchChannelPointsMessage=})')

            await self.__twitchUtils.safeSend(
                messageable = twitchChannel,
                message = f'⚠ Sorry @{twitchChannelPointsMessage.userName}, please specify a valid username to be timed out'
            )

            return None

        timeoutTargetUserId = await self.__userIdsRepository.fetchUserId(
            userName = timeoutTargetUserName,
            twitchAccessToken = userTwitchAccessToken
        )

        if not utils.isValidStr(timeoutTargetUserId):
            self.__timber.log('TimeoutPointRedemption', f'Attempted to timeout \"{timeoutTargetUserName}\" from {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}, but was unable to find a user ID: ({twitchChannelPointsMessage=})')

            await self.__twitchUtils.safeSend(
                messageable = twitchChannel,
                message = f'⚠ Sorry @{twitchChannelPointsMessage.userName}, no user ID for \"{timeoutTargetUserName}\" was able to be found'
            )

            return None

        return TimeoutPointRedemption.TimeoutTarget(
            userId = timeoutTargetUserId,
            userName = timeoutTargetUserName,
            actionType = TimeoutActionType.TARGETED
        )

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser

        timeoutBoosterPacks = twitchUser.timeoutBoosterPacks
        if timeoutBoosterPacks is None or len(timeoutBoosterPacks) == 0:
            return False

        timeoutBoosterPack = timeoutBoosterPacks.get(twitchChannelPointsMessage.rewardId, None)
        if timeoutBoosterPack is None:
            return False

        moderatorTwitchAccessToken = await self.__twitchTokensRepository.getAccessToken(
            twitchChannel = await self.__twitchHandleProvider.getTwitchHandle()
        )

        if not utils.isValidStr(moderatorTwitchAccessToken):
            return False

        userTwitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId
        )

        if not utils.isValidStr(userTwitchAccessToken):
            return False

        moderatorUserId = await self.__userIdsRepository.fetchUserId(
            userName = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchAccessToken = userTwitchAccessToken
        )

        if not utils.isValidStr(moderatorUserId):
            return False

        timeoutTarget = await self.__determineTimeoutTarget(
            message = twitchChannelPointsMessage.redemptionMessage,
            userTwitchAccessToken = userTwitchAccessToken,
            timeoutBoosterPack = timeoutBoosterPack,
            twitchChannel = twitchChannel,
            twitchChannelPointsMessage = twitchChannelPointsMessage,
            twitchUser = twitchUser
        )

        if timeoutTarget is None:
            return False

        self.__timeoutActionHelper.submitTimeout(TimeoutActionData(
            isRandomChanceEnabled = timeoutBoosterPack.randomChanceEnabled,
            bits = None,
            durationSeconds = timeoutBoosterPack.durationSeconds,
            remainingGrenades = None,
            chatMessage = None,
            instigatorUserId = twitchChannelPointsMessage.userId,
            instigatorUserName = twitchChannelPointsMessage.userName,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            pointRedemptionEventId = twitchChannelPointsMessage.eventId,
            pointRedemptionMessage = twitchChannelPointsMessage.redemptionMessage,
            pointRedemptionRewardId = twitchChannelPointsMessage.rewardId,
            timeoutTargetUserId = timeoutTarget.userId,
            timeoutTargetUserName = timeoutTarget.userName,
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
            twitchChatMessageId = None,
            userTwitchAccessToken = userTwitchAccessToken,
            actionType = timeoutTarget.actionType,
            streamStatusRequirement = TimeoutStreamStatusRequirement.ANY,
            user = twitchUser
        ))

        return True
