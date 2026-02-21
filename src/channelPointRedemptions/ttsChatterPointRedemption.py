from typing import Final

from .absChannelPointRedemption2 import AbsChannelPointRedemption2
from ..timber.timberInterface import TimberInterface
from ..ttsChatter.repository.ttsChatterRepositoryInterface import TtsChatterRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption


class TtsChatterPointRedemption(AbsChannelPointRedemption2):

    def __init__(
        self,
        timber: TimberInterface,
        ttsChatterRepository: TtsChatterRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsChatterRepository, TtsChatterRepositoryInterface):
            raise TypeError(f'ttsChatterRepository argument is malformed: \"{ttsChatterRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__ttsChatterRepository: Final[TtsChatterRepositoryInterface] = ttsChatterRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

    async def handlePointRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> bool:
        twitchUser = channelPointsRedemption.twitchUser
        if not twitchUser.areTtsChattersEnabled:
            return False

        if await self.__ttsChatterRepository.isTtsChatter(
            chatterUserId = channelPointsRedemption.redemptionUserId,
            twitchChannelId = channelPointsRedemption.twitchChannelId,
        ):
            self.__twitchChatMessenger.send(
                text = f'ⓘ @{channelPointsRedemption.redemptionUserName} you are already a TTS Chatter',
                twitchChannelId = channelPointsRedemption.twitchChannelId,
            )
            return True

        await self.__ttsChatterRepository.add(
            chatterUserId = channelPointsRedemption.redemptionUserId,
            twitchChannelId = channelPointsRedemption.twitchChannelId,
        )

        self.__twitchChatMessenger.send(
            text = f'ⓘ @{channelPointsRedemption.redemptionUserName} you are now a TTS Chatter',
            twitchChannelId = channelPointsRedemption.twitchChannelId,
        )

        self.__timber.log('TtsChatterPointRedemption', f'Redeemed ({channelPointsRedemption=})')
        return True
