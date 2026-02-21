from asyncio import AbstractEventLoop
from typing import Any, Final

from .absChannelPointRedemption2 import AbsChannelPointRedemption2
from ..storage.jsonFileReader import JsonFileReader
from ..storage.jsonReaderInterface import JsonReaderInterface
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..timber.timberInterface import TimberInterface
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProvider import TtsProvider
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption


class DecTalkSongPointRedemption(AbsChannelPointRedemption2):

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
            fileName = 'decTalkSongsRepository.json',
        )

    async def handlePointRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> bool:
        twitchUser = channelPointsRedemption.twitchUser
        if not twitchUser.isDecTalkSongsEnabled:
            return False

        decTalkSongs = await self.__decTalkSongsRepository.readJsonAsync()
        if decTalkSongs is None or len(decTalkSongs) == 0:
            return False

        decTalkSongBoosterPacks = twitchUser.decTalkSongBoosterPacks
        if decTalkSongBoosterPacks is None or len(decTalkSongBoosterPacks) == 0:
            return False

        decTalkSongBoosterPack = decTalkSongBoosterPacks.get(channelPointsRedemption.rewardId, None)
        if decTalkSongBoosterPack is None:
            return False

        songStrings: list[str] | Any | None = decTalkSongs.get(decTalkSongBoosterPack.song, None)

        if not isinstance(songStrings, list) or len(songStrings) == 0:
            return False

        message = ''.join(songStrings)

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = channelPointsRedemption.twitchChannel,
            twitchChannelId = channelPointsRedemption.twitchChannelId,
            ttsEvent = TtsEvent(
                message = message,
                twitchChannel = channelPointsRedemption.twitchChannel,
                twitchChannelId = channelPointsRedemption.twitchChannelId,
                userId = channelPointsRedemption.redemptionUserId,
                userName = channelPointsRedemption.redemptionUserName,
                donation = None,
                provider = TtsProvider.UNRESTRICTED_DEC_TALK,
                providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
                raidInfo = None,
            ),
        ))

        self.__timber.log('DecTalkSongPointRedemption', f'Redeemed ({channelPointsRedemption=}) ({decTalkSongBoosterPack=})')
        return True
