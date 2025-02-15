from asyncio import AbstractEventLoop

from frozenlist import FrozenList

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..storage.jsonFileReader import JsonFileReader
from ..storage.jsonReaderInterface import JsonReaderInterface
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..timber.timberInterface import TimberInterface
from ..tts.ttsEvent import TtsEvent
from ..tts.ttsProvider import TtsProvider
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage


class DecTalkSongPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber

        self.__decTalkSongsRepository: JsonReaderInterface = JsonFileReader(
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

        decTalkSongBoosterPacks = twitchUser.decTalkSongBoosterPacks
        if decTalkSongBoosterPacks is None or len(decTalkSongBoosterPacks) == 0:
            return False

        decTalkSongBoosterPack = decTalkSongBoosterPacks.get(twitchChannelPointsMessage.rewardId, None)
        if decTalkSongBoosterPack is None:
            return False

        decTalkSongs = await self.__decTalkSongsRepository.readJsonAsync()
        if decTalkSongs is None or len(decTalkSongs) == 0:
            return False

        songData = FrozenList(decTalkSongs.get(decTalkSongBoosterPack.song, None))
        songData.freeze()

        if len(songData) == 0:
            return False

        songData = ''.join(songData)

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = twitchUser.handle,
            twitchChannelId = await twitchChannel.getTwitchChannelId(),
            ttsEvent = TtsEvent(
                message = songData,
                twitchChannel = twitchUser.handle,
                twitchChannelId = await twitchChannel.getTwitchChannelId(),
                userId = twitchChannelPointsMessage.userId,
                userName = twitchChannelPointsMessage.userName,
                donation = None,
                provider = TtsProvider.SINGING_DEC_TALK,
                raidInfo = None
            )
        ))

        self.__timber.log('DecTalkSongPointRedemption', f'Redeemed DecTalk song {decTalkSongBoosterPack} for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}')
        return True
