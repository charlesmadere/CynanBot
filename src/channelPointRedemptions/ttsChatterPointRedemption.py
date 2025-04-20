from .absChannelPointRedemption import AbsChannelPointRedemption
from ..timber.timberInterface import TimberInterface
from ..ttsChatter.repository.ttsChatterRepositoryInterface import TtsChatterRepositoryInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface


class TtsChatterPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        timber: TimberInterface,
        ttsChatterRepository: TtsChatterRepositoryInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsChatterRepository, TtsChatterRepositoryInterface):
            raise TypeError(f'ttsChatterRepository argument is malformed: \"{ttsChatterRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__timber: TimberInterface = timber
        self.__ttsChatterRepository: TtsChatterRepositoryInterface = ttsChatterRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.areTtsChattersEnabled:
            return False

        if await self.__ttsChatterRepository.isTtsChatter(
            chatterUserId = twitchChannelPointsMessage.userId,
            twitchChannelId = await twitchChannel.getTwitchChannelId()
        ):
            await self.__twitchUtils.safeSend(
                messageable = twitchChannel,
                message = f'ⓘ @{twitchChannelPointsMessage.userName} you are already a TTS Chatter'
            )
            return True

        await self.__ttsChatterRepository.add(
            chatterUserId = twitchChannelPointsMessage.userId,
            twitchChannelId = await twitchChannel.getTwitchChannelId()
        )

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'ⓘ @{twitchChannelPointsMessage.userName} you are now a TTS Chatter'
        )

        self.__timber.log('TtsChatterPointRedemption', f'Redeemed for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}')
        return True
