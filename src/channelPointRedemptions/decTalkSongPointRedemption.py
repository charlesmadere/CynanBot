from asyncio import AbstractEventLoop
from typing import Any, Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..storage.jsonFileReader import JsonFileReader
from ..storage.jsonReaderInterface import JsonReaderInterface
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..timber.timberInterface import TimberInterface
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProvider import TtsProvider
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage


class DecTalkSongPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber

        self.__decTalkSongsRepository: Final[JsonReaderInterface] = JsonFileReader(
            eventLoop = eventLoop,
            fileName = 'decTalkSongsRepository.json'
        )

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.isDecTalkSongsEnabled:
            return False

        decTalkSongs = await self.__decTalkSongsRepository.readJsonAsync()
        if decTalkSongs is None or len(decTalkSongs) == 0:
            return False

        decTalkSongBoosterPacks = twitchUser.decTalkSongBoosterPacks
        if decTalkSongBoosterPacks is None or len(decTalkSongBoosterPacks) == 0:
            return False

        decTalkSongBoosterPack = decTalkSongBoosterPacks.get(twitchChannelPointsMessage.rewardId, None)
        if decTalkSongBoosterPack is None:
            return False

        songStrings: list[str] | Any | None = decTalkSongs.get(decTalkSongBoosterPack.song, None)

        if not isinstance(songStrings, list) or len(songStrings) == 0:
            return False

        message = ''.join(songStrings)

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = twitchUser.handle,
            twitchChannelId = await twitchChannel.getTwitchChannelId(),
            ttsEvent = TtsEvent(
                message = message,
                twitchChannel = twitchUser.handle,
                twitchChannelId = await twitchChannel.getTwitchChannelId(),
                userId = twitchChannelPointsMessage.userId,
                userName = twitchChannelPointsMessage.userName,
                donation = None,
                provider = TtsProvider.UNRESTRICTED_DEC_TALK,
                providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
                raidInfo = None
            )
        ))

        self.__timber.log('DecTalkSongPointRedemption', f'Redeemed DecTalk song {decTalkSongBoosterPack} for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}')
        return True
