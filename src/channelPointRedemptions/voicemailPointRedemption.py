from dataclasses import dataclass
from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
from ..twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ..twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..voicemail.helpers.voicemailHelperInterface import VoicemailHelperInterface
from ..voicemail.models.addVoicemailResult import AddVoicemailResult
from ..voicemail.settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface


class VoicemailPointRedemption(AbsChannelPointRedemption):

    @dataclass(frozen = True, slots = True)
    class TargetedUserData:
        cleanedMessage: str
        userId: str
        userName: str

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        voicemailHelper: VoicemailHelperInterface,
        voicemailSettingsRepository: VoicemailSettingsRepositoryInterface,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(voicemailHelper, VoicemailHelperInterface):
            raise TypeError(f'voicemailHelper argument is malformed: \"{voicemailHelper}\"')
        elif not isinstance(voicemailSettingsRepository, VoicemailSettingsRepositoryInterface):
            raise TypeError(f'voicemailSettingsRepository argument is malformed: \"{voicemailSettingsRepository}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchFollowingStatusRepository: Final[TwitchFollowingStatusRepositoryInterface] = twitchFollowingStatusRepository
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__voicemailHelper: Final[VoicemailHelperInterface] = voicemailHelper
        self.__voicemailSettingsRepository: Final[VoicemailSettingsRepositoryInterface] = voicemailSettingsRepository

    async def __determineTargetedUser(
        self,
        message: str | None,
        twitchAccessToken: str,
    ) -> TargetedUserData | None:
        if not utils.isValidStr(message):
            return None

        cleanedMessage = utils.cleanStr(message)
        splits = utils.getCleanedSplits(cleanedMessage)
        if len(splits) == 0:
            self.__timber.log('VoicemailPointRedemption', f'Received voicemail channel point redemption event without any message ({message=}) ({cleanedMessage=}) ({splits=})')
            return None

        targetedUserName = utils.removePreceedingAt(splits[0])
        if not utils.isValidStr(targetedUserName):
            self.__timber.log('VoicemailPointRedemption', f'Received voicemail channel point redemption without a valid targeted user name ({message=}) ({cleanedMessage=}) ({splits=}) ({targetedUserName=})')
            return None

        targetedUserId = await self.__userIdsRepository.fetchUserId(
            userName = targetedUserName,
            twitchAccessToken = twitchAccessToken
        )

        if not utils.isValidStr(targetedUserId):
            self.__timber.log('VoicemailPointRedemption', f'Received voicemail channel point redemption but couldn\'t find a valid targeted user ID ({message=}) ({cleanedMessage=}) ({splits=}) ({targetedUserName=}) ({targetedUserId=})')
            return None

        return VoicemailPointRedemption.TargetedUserData(
            cleanedMessage = ' '.join(splits[1:]),
            userId = targetedUserId,
            userName = targetedUserName
        )

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.isVoicemailEnabled:
            return False
        elif not await self.__voicemailSettingsRepository.isEnabled():
            return False

        twitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
        )

        targetedUserData = await self.__determineTargetedUser(
            message = twitchChannelPointsMessage.redemptionMessage,
            twitchAccessToken = twitchAccessToken,
        )

        if targetedUserData is None:
            self.__timber.log('VoicemailPointRedemption', f'Received channel point redemption without a valid targeted user ({twitchChannel=}) ({twitchChannelPointsMessage=}) ({targetedUserData=})')
            return True

        requiresNotActiveInChat = await self.__voicemailSettingsRepository.targetUserMustNotBeActiveInChat()

        if requiresNotActiveInChat and await self.__activeChattersRepository.isActiveIn(
            chatterUserId = targetedUserData.userId,
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
        ):
            self.__timber.log('VoicemailPointRedemption', f'Received voicemail cheer action but the targeted user is active in chat ({twitchChannel=}) ({twitchChannelPointsMessage=}) ({targetedUserData=})')

            self.__twitchChatMessenger.send(
                text = f'⚠ Sorry @{twitchChannelPointsMessage.userName}, you can only send voicemails to users who aren\t active in chat.',
                twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
            )

            return True

        requiresFollowing = await self.__voicemailSettingsRepository.targetUserMustBeFollowing()

        if requiresFollowing and not await self.__twitchFollowingStatusRepository.isFollowing(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
            userId = targetedUserData.userId,
        ):
            self.__timber.log('VoicemailPointRedemption', f'Received channel point redemption but the targeted user is not following the channel ({twitchChannel=}) ({twitchChannelPointsMessage=}) ({targetedUserData=})')

            self.__twitchChatMessenger.send(
                text = f'⚠ Sorry @{twitchChannelPointsMessage.userName}, you can only send voicemails to users who are following the channel.',
                twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
            )

            return True

        addVoicemailResult = await self.__voicemailHelper.addVoicemail(
            message = targetedUserData.cleanedMessage,
            originatingUserId = twitchChannelPointsMessage.userId,
            targetUserId = targetedUserData.userId,
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
        )

        match addVoicemailResult:
            case AddVoicemailResult.FEATURE_DISABLED:
                pass

            case AddVoicemailResult.MAXIMUM_FOR_TARGET_USER:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Sorry @{twitchChannelPointsMessage.userName}, unfortunately @{targetedUserData.userName} has a full voicemail inbox',
                    twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
                )

            case AddVoicemailResult.MESSAGE_MALFORMED:
                self.__timber.log('VoicemailPointRedemption', f'Tried setting a malformed voicemail message ({twitchChannel=}) ({twitchChannelPointsMessage=}) ({targetedUserData=}) ({addVoicemailResult=})')

                self.__twitchChatMessenger.send(
                    text = f'⚠ Sorry @{twitchChannelPointsMessage.userName}, an unknown error occurred when setting your voicemail message for @{targetedUserData.userName}',
                    twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
                )

            case AddVoicemailResult.OK:
                self.__twitchChatMessenger.send(
                    text = f'☎️ @{twitchChannelPointsMessage.userName} your voicemail message for @{targetedUserData.userName} has been sent!',
                    twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
                )

            case AddVoicemailResult.TARGET_USER_IS_ORIGINATING_USER:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Sorry @{twitchChannelPointsMessage.userName}, you can\'t send yourself a voicemail',
                    twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
                )

            case AddVoicemailResult.TARGET_USER_IS_TWITCH_CHANNEL_USER:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Sorry @{twitchChannelPointsMessage.userName}, you can\'t send the streamer a voicemail',
                    twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
                )

        self.__timber.log('VoicemailPointRedemption', f'Redeemed for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}')
        return True
