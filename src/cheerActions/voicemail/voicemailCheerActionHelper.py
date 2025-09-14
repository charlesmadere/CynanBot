from dataclasses import dataclass
from typing import Final

from frozendict import frozendict

from .voicemailCheerAction import VoicemailCheerAction
from .voicemailCheerActionHelperInterface import VoicemailCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ...chatterInventory.helpers.useChatterItemHelperInterface import UseChatterItemHelperInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ...twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface
from ...voicemail.helpers.voicemailHelperInterface import VoicemailHelperInterface
from ...voicemail.models.addVoicemailResult import AddVoicemailResult
from ...voicemail.settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface


class VoicemailCheerActionHelper(VoicemailCheerActionHelperInterface):

    @dataclass(frozen = True)
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
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        useChatterItemHelper: UseChatterItemHelperInterface,
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
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif not isinstance(useChatterItemHelper, UseChatterItemHelperInterface):
            raise TypeError(f'useChatterItemHelper argument is malformed: \"{useChatterItemHelper}\"')
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
        self.__twitchMessageStringUtils: Final[TwitchMessageStringUtilsInterface] = twitchMessageStringUtils
        self.__useChatterItemHelper: Final[UseChatterItemHelperInterface] = useChatterItemHelper
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__voicemailHelper: Final[VoicemailHelperInterface] = voicemailHelper
        self.__voicemailSettingsRepository: Final[VoicemailSettingsRepositoryInterface] = voicemailSettingsRepository

    async def __determineTargetedUser(
        self,
        message: str,
        userTwitchAccessToken: str,
    ) -> TargetedUserData | None:
        cleanedMessage = await self.__twitchMessageStringUtils.removeCheerStrings(message)
        cleanedMessage = utils.cleanStr(cleanedMessage)

        splits = utils.getCleanedSplits(cleanedMessage)
        if len(splits) == 0:
            self.__timber.log('VoicemailCheerActionHelper', f'Received voicemail cheer action without any message ({message=}) ({cleanedMessage=}) ({splits=})')
            return None

        targetedUserName = utils.removePreceedingAt(splits[0])
        if not utils.isValidStr(targetedUserName):
            self.__timber.log('VoicemailCheerActionHelper', f'Received voicemail cheer action without a valid targeted user name ({message=}) ({cleanedMessage=}) ({splits=}) ({targetedUserName=})')
            return None

        targetedUserId = await self.__userIdsRepository.fetchUserId(
            userName = targetedUserName,
            twitchAccessToken = userTwitchAccessToken,
        )

        if not utils.isValidStr(targetedUserId):
            self.__timber.log('VoicemailCheerActionHelper', f'Received voicemail cheer action but couldn\'t find a valid targeted user ID ({message=}) ({cleanedMessage=}) ({splits=}) ({targetedUserName=}) ({targetedUserId=})')
            return None

        return VoicemailCheerActionHelper.TargetedUserData(
            cleanedMessage = ' '.join(splits[1:]),
            userId = targetedUserId,
            userName = targetedUserName,
        )

    async def handleVoicemailCheerAction(
        self,
        actions: frozendict[int, AbsCheerAction],
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        userTwitchAccessToken: str,
        user: UserInterface,
    ) -> bool:
        action = actions.get(bits, None)

        if not isinstance(action, VoicemailCheerAction) or not action.isEnabled:
            return False

        targetedUserData = await self.__determineTargetedUser(
            message = message,
            userTwitchAccessToken = userTwitchAccessToken,
        )

        if targetedUserData is None:
            self.__timber.log('VoicemailCheerActionHelper', f'Received voicemail cheer action without a valid targeted user ({bits=}) ({twitchChannelId=}) ({cheerUserId=}) ({cheerUserName=}) ({message=}) ({action=}) ({targetedUserData=})')
            return True

        requiresNotActiveInChat = await self.__voicemailSettingsRepository.targetUserMustNotBeActiveInChat()

        if requiresNotActiveInChat and await self.__activeChattersRepository.isActiveIn(
            chatterUserId = targetedUserData.userId,
            twitchChannelId = twitchChannelId,
        ):
            self.__timber.log('VoicemailCheerActionHelper', f'Received voicemail cheer action but the targeted user is active in chat ({bits=}) ({twitchChannelId=}) ({cheerUserId=}) ({cheerUserName=}) ({message=}) ({action=}) ({targetedUserData=})')

            self.__twitchChatMessenger.send(
                text = f'⚠ Sorry @{cheerUserName}, you can only send voicemails to users who aren\t active in chat.',
                twitchChannelId = twitchChannelId,
                replyMessageId = twitchChatMessageId,
            )

            return True

        requiresFollowing = await self.__voicemailSettingsRepository.targetUserMustBeFollowing()

        if requiresFollowing and not await self.__twitchFollowingStatusRepository.isFollowing(
            twitchAccessToken = userTwitchAccessToken,
            twitchChannelId = twitchChannelId,
            userId = targetedUserData.userId
        ):
            self.__timber.log('VoicemailCheerActionHelper', f'Received voicemail cheer action but the targeted user is not following the channel ({bits=}) ({twitchChannelId=}) ({cheerUserId=}) ({cheerUserName=}) ({message=}) ({action=}) ({targetedUserData=})')

            self.__twitchChatMessenger.send(
                text = f'⚠ Sorry @{cheerUserName}, you can only send voicemails to users who are following the channel.',
                twitchChannelId = twitchChannelId,
                replyMessageId = twitchChatMessageId,
            )

            return True

        addVoicemailResult = await self.__voicemailHelper.addVoicemail(
            message = targetedUserData.cleanedMessage,
            originatingUserId = cheerUserId,
            targetUserId = targetedUserData.userId,
            twitchChannelId = twitchChannelId,
        )

        match addVoicemailResult:
            case AddVoicemailResult.FEATURE_DISABLED:
                # this case is intentionally empty
                pass

            case AddVoicemailResult.MAXIMUM_FOR_TARGET_USER:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Sorry @{cheerUserName}, unfortunately @{targetedUserData.userName} has a full voicemail inbox',
                    twitchChannelId = twitchChannelId,
                    replyMessageId = twitchChatMessageId,
                )

            case AddVoicemailResult.MESSAGE_MALFORMED:
                self.__timber.log('VoicemailCheerActionHelper', f'Tried setting a malformed voicemail message ({bits=}) ({twitchChannelId=}) ({cheerUserId=}) ({cheerUserName=}) ({message=}) ({action=}) ({targetedUserData=}) ({addVoicemailResult=})')

                self.__twitchChatMessenger.send(
                    text = f'⚠ Sorry @{cheerUserName}, an unknown error occurred when setting your voicemail message for @{targetedUserData.userName}.',
                    twitchChannelId = twitchChannelId,
                    replyMessageId = twitchChatMessageId,
                )

            case AddVoicemailResult.OK:
                self.__twitchChatMessenger.send(
                    text = f'☎️ @{cheerUserName} your voicemail message for @{targetedUserData.userName} has been sent!',
                    twitchChannelId = twitchChannelId,
                    replyMessageId = twitchChatMessageId,
                )

            case AddVoicemailResult.TARGET_USER_IS_ORIGINATING_USER:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Sorry @{cheerUserName}, you can\'t send yourself a voicemail',
                    twitchChannelId = twitchChannelId,
                    replyMessageId = twitchChatMessageId,
                )

            case AddVoicemailResult.TARGET_USER_IS_TWITCH_CHANNEL_USER:
                self.__twitchChatMessenger.send(
                    text = f'⚠ Sorry @{cheerUserName}, you can\'t send the streamer a voicemail',
                    twitchChannelId = twitchChannelId,
                    replyMessageId = twitchChatMessageId,
                )

        return True
