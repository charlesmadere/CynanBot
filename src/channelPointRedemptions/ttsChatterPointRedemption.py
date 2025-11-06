from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..timber.timberInterface import TimberInterface
from ..ttsChatter.repository.ttsChatterRepositoryInterface import TtsChatterRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage


class TtsChatterPointRedemption(AbsChannelPointRedemption):

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
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.areTtsChattersEnabled:
            return False

        if await self.__ttsChatterRepository.isTtsChatter(
            chatterUserId = twitchChannelPointsMessage.userId,
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
        ):
            self.__twitchChatMessenger.send(
                text = f'ⓘ @{twitchChannelPointsMessage.userName} you are already a TTS Chatter',
                twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
            )
            return True

        await self.__ttsChatterRepository.add(
            chatterUserId = twitchChannelPointsMessage.userId,
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
        )

        self.__twitchChatMessenger.send(
            text = f'ⓘ @{twitchChannelPointsMessage.userName} you are now a TTS Chatter',
            twitchChannelId = twitchChannelPointsMessage.twitchChannelId,
        )

        self.__timber.log('TtsChatterPointRedemption', f'Redeemed for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}')
        return True
