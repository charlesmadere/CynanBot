from datetime import datetime, timedelta

from .absChatAction import AbsChatAction
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..supStreamer.supStreamerHelperInterface import SupStreamerHelperInterface
from ..supStreamer.supStreamerRepositoryInterface import SupStreamerRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ..twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..users.userInterface import UserInterface


class SupStreamerChatAction(AbsChatAction):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface,
        supStreamerHelper: SupStreamerHelperInterface,
        supStreamerRepository: SupStreamerRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        cooldown: timedelta = timedelta(hours = 6)
    ):
        if not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(supStreamerHelper, SupStreamerHelperInterface):
            raise TypeError(f'supStreamerHelper argument is malformed: \"{supStreamerHelper}\"')
        elif not isinstance(supStreamerRepository, SupStreamerRepositoryInterface):
            raise TypeError(f'supStreamerRepository argument is malformed: \"{supStreamerRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__supStreamerHelper: SupStreamerHelperInterface = supStreamerHelper
        self.__supStreamerRepository: SupStreamerRepositoryInterface = supStreamerRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface = twitchFollowingStatusRepository
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__cooldown: timedelta = cooldown

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface,
    ) -> bool:
        if not user.isSupStreamerEnabled or not user.isTtsEnabled:
            return False

        now = datetime.now(self.__timeZoneRepository.getDefault())

        if mostRecentChat is not None and (mostRecentChat.mostRecentChat + self.__cooldown) > now:
            return False

        chatMessage = message.getContent()
        supStreamerBoosterPacks = user.supStreamerBoosterPacks

        if supStreamerBoosterPacks is not None and len(supStreamerBoosterPacks) >= 1:
            for supStreamerBoosterPack in supStreamerBoosterPacks:
                success = await self.__checkSupMessage(chatMessage, message, now, supStreamerBoosterPack.message, supStreamerBoosterPack.reply, user)
                if success:
                    return success

        if utils.isValidStr(user.supStreamerMessage):
            return await self.__checkSupMessage(chatMessage, message, now, user.supStreamerMessage, "sup", user)

        return False

    async def __checkSupMessage(
        self,
        chatMessage: str | None,
        message: TwitchMessage,
        now: datetime,
        supStreamerMessage: str,
        reply: str,
        user: UserInterface,
    ) -> bool:
        if not utils.isValidStr(chatMessage) or not utils.isValidStr(supStreamerMessage):
            return False
        elif not await self.__supStreamerHelper.isSupStreamerMessage(
            chatMessage = chatMessage,
            supStreamerMessage = supStreamerMessage,
        ):
            return False

        supStreamerChatData = await self.__supStreamerRepository.get(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId(),
        )

        if supStreamerChatData is not None and (supStreamerChatData.mostRecentSup + self.__cooldown) > now:
            return False

        # only allow sup streamer messages from chatters who are following
        if not await self.__isFollowing(message):
            return False

        await self.__supStreamerRepository.set(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId(),
        )

        self.__timber.log('SupStreamerChatAction', f'Encountered sup streamer chat message from {message.getAuthorName()}:{message.getAuthorId()} in {user.handle}')

        providerOverridableStatus: TtsProviderOverridableStatus

        if user.isChatterPreferredTtsEnabled:
            providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
        else:
            providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.handle,
            twitchChannelId = await message.getTwitchChannelId(),
            ttsEvent = TtsEvent(
                message = f'{message.getAuthorName()} {reply}',
                twitchChannel = user.handle,
                twitchChannelId = await message.getTwitchChannelId(),
                userId = message.getAuthorId(),
                userName = message.getAuthorName(),
                donation = None,
                provider = user.defaultTtsProvider,
                providerOverridableStatus = providerOverridableStatus,
                raidInfo = None,
            ),
        ))

        return True

    async def __isFollowing(self, message: TwitchMessage) -> bool:
        if not isinstance(message, TwitchMessage):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = await message.getTwitchChannelId(),
        )

        if not utils.isValidStr(twitchAccessToken):
            return False

        return await self.__twitchFollowingStatusRepository.isFollowing(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = await message.getTwitchChannelId(),
            userId = message.getAuthorId(),
        )
