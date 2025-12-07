import random
from datetime import datetime, timedelta
from typing import Final

from .absChatAction import AbsChatAction
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..nickName.helpers.nickNameHelperInterface import NickNameHelperInterface
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
        nickNameHelper: NickNameHelperInterface | None,
        streamAlertsManager: StreamAlertsManagerInterface,
        supStreamerHelper: SupStreamerHelperInterface,
        supStreamerRepository: SupStreamerRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        cooldown: timedelta = timedelta(hours = 6),
    ):
        if nickNameHelper is not None and not isinstance(nickNameHelper, NickNameHelperInterface):
            raise TypeError(f'nickNameHelper argument is malformed: \"{nickNameHelper}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
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

        self.__nickNameHelper: Final[NickNameHelperInterface | None] = nickNameHelper
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__supStreamerHelper: Final[SupStreamerHelperInterface] = supStreamerHelper
        self.__supStreamerRepository: Final[SupStreamerRepositoryInterface] = supStreamerRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchFollowingStatusRepository: Final[TwitchFollowingStatusRepositoryInterface] = twitchFollowingStatusRepository
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__cooldown: Final[timedelta] = cooldown

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

        cleanedMessage = utils.cleanStr(message.getContent())
        supStreamerBoosterPacks = user.supStreamerBoosterPacks

        if supStreamerBoosterPacks is not None and len(supStreamerBoosterPacks) >= 1:
            shuffledBoosterPacks = list(supStreamerBoosterPacks)
            random.shuffle(shuffledBoosterPacks)

            for supStreamerBoosterPack in shuffledBoosterPacks:
                if await self.__checkSupMessage(cleanedMessage, message, now, supStreamerBoosterPack.message, supStreamerBoosterPack.reply, user):
                    return True

        if utils.isValidStr(user.supStreamerMessage):
            return await self.__checkSupMessage(cleanedMessage, message, now, user.supStreamerMessage, 'sup', user)

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

        authorName = await self.__determineAuthorName(message)

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
                message = f'{authorName} {reply}',
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

    async def __determineAuthorName(self, message: TwitchMessage) -> str:
        if not isinstance(message, TwitchMessage):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if self.__nickNameHelper is None:
            return message.getAuthorName()

        nickNameData = await self.__nickNameHelper.get(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId(),
        )

        if nickNameData is not None and utils.isValidStr(nickNameData.nickName):
            return nickNameData.nickName
        else:
            return message.getAuthorName()

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
