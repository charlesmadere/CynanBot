import random
from datetime import datetime, timedelta
from typing import Final

from .absChatAction2 import AbsChatAction2
from .chatActionResult import ChatActionResult
from ..chatterPreferredName.helpers.chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from ..chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..supStreamer.supStreamerHelperInterface import SupStreamerHelperInterface
from ..supStreamer.supStreamerRepositoryInterface import SupStreamerRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProvider import TtsProvider
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..users.supStreamer.supStreamerBoosterPack import SupStreamerBoosterPack


class SupStreamerChatAction(AbsChatAction2):

    def __init__(
        self,
        chatterPreferredNameHelper: ChatterPreferredNameHelperInterface,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        supStreamerHelper: SupStreamerHelperInterface,
        supStreamerRepository: SupStreamerRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        cooldown: timedelta = timedelta(hours = 8),
    ):
        if not isinstance(chatterPreferredNameHelper, ChatterPreferredNameHelperInterface):
            raise TypeError(f'chatterPreferredNameHelper argument is malformed: \"{chatterPreferredNameHelper}\"')
        elif not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
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

        self.__chatterPreferredNameHelper: Final[ChatterPreferredNameHelperInterface] = chatterPreferredNameHelper
        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__supStreamerHelper: Final[SupStreamerHelperInterface] = supStreamerHelper
        self.__supStreamerRepository: Final[SupStreamerRepositoryInterface] = supStreamerRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchFollowingStatusRepository: Final[TwitchFollowingStatusRepositoryInterface] = twitchFollowingStatusRepository
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__cooldown: Final[timedelta] = cooldown

    @property
    def actionName(self) -> str:
        return 'SupStreamerChatAction'

    async def handleChatAction(
        self,
        mostRecentChat: MostRecentChat | None,
        chatMessage: TwitchChatMessage,
    ) -> ChatActionResult:
        if not chatMessage.twitchUser.isSupStreamerEnabled or not chatMessage.twitchUser.isTtsEnabled:
            return ChatActionResult.IGNORED

        now = self.__timeZoneRepository.getNow()
        if mostRecentChat is not None and (mostRecentChat.mostRecentChat + self.__cooldown) > now:
            return ChatActionResult.IGNORED

        cleanedMessage = utils.cleanStr(chatMessage.text)
        if not utils.isValidStr(cleanedMessage):
            return ChatActionResult.IGNORED

        supStreamerBoosterPacks = chatMessage.twitchUser.supStreamerBoosterPacks
        if supStreamerBoosterPacks is None or len(supStreamerBoosterPacks) == 0:
            return ChatActionResult.IGNORED

        shuffledBoosterPacks: list[SupStreamerBoosterPack] = list(supStreamerBoosterPacks)
        random.shuffle(shuffledBoosterPacks)

        for supStreamerBoosterPack in shuffledBoosterPacks:
            if await self.__isSupMessage(
                now = now,
                cleanedMessage = cleanedMessage,
                supStreamerBoosterPack = supStreamerBoosterPack,
                chatMessage = chatMessage,
            ):
                return ChatActionResult.CONSUMED

        return ChatActionResult.IGNORED

    async def __determineAuthorName(self, chatMessage: TwitchChatMessage) -> str:
        preferredNameData = await self.__chatterPreferredNameHelper.get(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if preferredNameData is None:
            return chatMessage.chatterUserName
        else:
            return preferredNameData.preferredName

    async def __isFollowing(self, chatMessage: TwitchChatMessage) -> bool:
        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if not utils.isValidStr(twitchAccessToken):
            return False

        return await self.__twitchFollowingStatusRepository.isFollowing(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = chatMessage.twitchChannelId,
            userId = chatMessage.chatterUserId,
        )

    async def __isSupMessage(
        self,
        now: datetime,
        cleanedMessage: str,
        supStreamerBoosterPack: SupStreamerBoosterPack,
        chatMessage: TwitchChatMessage,
    ) -> bool:
        if not await self.__supStreamerHelper.isSupStreamerMessage(
            chatMessage = cleanedMessage,
            supStreamerMessage = supStreamerBoosterPack.message,
        ):
            return False

        supStreamerChatData = await self.__supStreamerRepository.get(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if supStreamerChatData is not None and (supStreamerChatData.mostRecentSup + self.__cooldown) > now:
            return False

        # only allow sup streamer messages from chatters who are following
        if not await self.__isFollowing(chatMessage):
            return False

        await self.__supStreamerRepository.set(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        authorName = await self.__determineAuthorName(chatMessage)

        providerOverridableStatus: TtsProviderOverridableStatus

        if chatMessage.twitchUser.isChatterPreferredTtsEnabled:
            providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
        else:
            providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

        provider = await self.__determineTtsProvider(
            providerOverridableStatus = providerOverridableStatus,
            chatMessage = chatMessage,
        )

        self.__timber.log(self.actionName, f'Encountered sup streamer chat message ({chatMessage=}) ({supStreamerBoosterPack=}) ({supStreamerChatData=}) ({providerOverridableStatus=}) ({provider=})')

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            ttsEvent = TtsEvent(
                message = f'{authorName} {supStreamerBoosterPack.reply}',
                twitchChannel = chatMessage.twitchChannel,
                twitchChannelId = chatMessage.twitchChannelId,
                userId = chatMessage.chatterUserId,
                userName = chatMessage.chatterUserName,
                donation = None,
                provider = provider,
                providerOverridableStatus = providerOverridableStatus,
                raidInfo = None,
            ),
        ))

        return True

    async def __determineTtsProvider(
        self,
        providerOverridableStatus: TtsProviderOverridableStatus,
        chatMessage: TwitchChatMessage,
    ) -> TtsProvider:
        if providerOverridableStatus is not TtsProviderOverridableStatus.CHATTER_OVERRIDABLE:
            return chatMessage.twitchUser.defaultTtsProvider

        chatterPreferredTts = await self.__chatterPreferredTtsHelper.get(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if chatterPreferredTts is None:
            return chatMessage.twitchUser.defaultTtsProvider
        else:
            return chatterPreferredTts.provider
