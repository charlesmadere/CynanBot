from .absChannelPointRedemption import AbsChannelPointRedemption
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..timeout.timeoutActionData import TimeoutActionData
from ..timeout.timeoutActionHelperInterface import TimeoutActionHelperInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ..twitch.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TimeoutPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        timber: TimberInterface,
        timeoutActionHelper: TimeoutActionHelperInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionHelper, TimeoutActionHelperInterface):
            raise TypeError(f'timeoutActionHelper argument is malformed: \"{timeoutActionHelper}\"')
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

        self.__timber: TimberInterface = timber
        self.__timeoutActionHelper: TimeoutActionHelperInterface = timeoutActionHelper
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchMessageStringUtils: TwitchMessageStringUtilsInterface = twitchMessageStringUtils
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.areTimeoutActionsEnabled:
            return False

        timeoutBoosterPacks = twitchUser.timeoutBoosterPacks
        if timeoutBoosterPacks is None or len(timeoutBoosterPacks) == 0:
            return False

        timeoutBoosterPack = timeoutBoosterPacks.get(twitchChannelPointsMessage.rewardId, None)
        if timeoutBoosterPack is None:
            return False

        moderatorTwitchAccessToken = await self.__twitchTokensRepository.getAccessToken(
            twitchChannelId = await self.__twitchHandleProvider.getTwitchHandle()
        )

        if not utils.isValidStr(moderatorTwitchAccessToken):
            return False

        userTwitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = await twitchChannel.getTwitchChannelId()
        )

        if not utils.isValidStr(userTwitchAccessToken):
            return False

        moderatorUserId = await self.__userIdsRepository.requireUserId(
            userName = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchAccessToken = userTwitchAccessToken
        )

        if not utils.isValidStr(moderatorUserId):
            return False

        timeoutTargetUserName = await self.__twitchMessageStringUtils.getUserNameFromMessage(
            message = twitchChannelPointsMessage.redemptionMessage
        )

        if not utils.isValidStr(timeoutTargetUserName):
            self.__timber.log('TimeoutCheerActionHelper', f'Attempted to timeout \"{timeoutTargetUserName}\" from {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.getHandle()}, but was unable to find a user name: ({twitchChannelPointsMessage=})')

            await self.__twitchUtils.safeSend(
                messageable = twitchChannel,
                message = f'⚠ Sorry @{twitchChannelPointsMessage.userName}, please specify a valid username to be timed out'
            )

            return False

        timeoutTargetUserId = await self.__userIdsRepository.fetchUserId(
            userName = timeoutTargetUserName,
            twitchAccessToken = userTwitchAccessToken
        )

        if not utils.isValidStr(timeoutTargetUserId):
            self.__timber.log('TimeoutPointRedemption', f'Attempted to timeout \"{timeoutTargetUserName}\" from {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.getHandle()}, but was unable to find a user ID: ({twitchChannelPointsMessage=})')

            await self.__twitchUtils.safeSend(
                messageable = twitchChannel,
                message = f'⚠ Sorry @{twitchChannelPointsMessage.userName}, no user ID for \"{timeoutTargetUserName}\" was able to be found'
            )

            return False

        await self.__timeoutActionHelper.timeout(TimeoutActionData(
            bits = None,
            durationSeconds = timeoutBoosterPack.durationSeconds,
            chatMessage = None,
            instigatorUserId = twitchChannelPointsMessage.userId,
            instigatorUserName = twitchChannelPointsMessage.userName,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            pointRedemptionEventId = twitchChannelPointsMessage.eventId,
            pointRedemptionMessage = twitchChannelPointsMessage.redemptionMessage,
            pointRedemptionRewardId = twitchChannelPointsMessage.rewardId,
            timeoutTargetUserId = timeoutTargetUserId,
            timeoutTargetUserName = timeoutTargetUserName,
            twitchChannelId = await twitchChannel.getTwitchChannelId(),
            twitchChatMessageId = None,
            userTwitchAccessToken = userTwitchAccessToken,
            streamStatusRequirement = TimeoutActionData.StreamStatusRequirement.ANY,
            user = twitchUser
        ))

        return True
