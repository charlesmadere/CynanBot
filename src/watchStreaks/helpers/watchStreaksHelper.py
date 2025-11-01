from typing import Final

from .watchStreaksHelperInterface import WatchStreaksHelperInterface
from ..models.watchStreakTtsAnnouncementResult import WatchStreakTtsAnnouncementResult
from ..settings.watchStreakSettingsInterface import WatchStreakSettingsInterface
from ...misc import utils as utils
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...tts.models.ttsEvent import TtsEvent
from ...tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ...users.userInterface import UserInterface


class WatchStreaksHelper(WatchStreaksHelperInterface):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface,
        watchStreakSettings: WatchStreakSettingsInterface,
    ):
        if not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(watchStreakSettings, WatchStreakSettingsInterface):
            raise TypeError(f'watchStreakSettings argument is malformed: \"{watchStreakSettings}\"')

        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__watchStreakSettings: Final[WatchStreakSettingsInterface] = watchStreakSettings

    async def watchStreakTtsAnnounce(
        self,
        watchStreak: int,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannelId: str,
        user: UserInterface,
    ) -> WatchStreakTtsAnnouncementResult:
        if not utils.isValidInt(watchStreak):
            raise TypeError(f'watchStreak argument is malformed: \"{watchStreak}\"')
        elif watchStreak < 0 or watchStreak > utils.getIntMaxSafeSize():
            raise ValueError(f'watchStreak argument is out of bounds: {watchStreak}')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if not user.isWatchStreakTtsAnnounceEnabled or not await self.__watchStreakSettings.isEnabled():
            return WatchStreakTtsAnnouncementResult.NOT_ENABLED
        elif watchStreak < await self.__watchStreakSettings.getMinimumWatchStreakForTts():
            return WatchStreakTtsAnnouncementResult.STREAK_TOO_SHORT

        providerOverridableStatus: TtsProviderOverridableStatus

        if user.isChatterPreferredTtsEnabled:
            providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
        else:
            providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.handle,
            twitchChannelId = twitchChannelId,
            ttsEvent = TtsEvent(
                message = f'Thanks {chatterUserName} for the {watchStreak} watch streak!',
                twitchChannel = user.handle,
                twitchChannelId = twitchChannelId,
                userId = chatterUserId,
                userName = chatterUserName,
                donation = None,
                provider = user.defaultTtsProvider,
                providerOverridableStatus = providerOverridableStatus,
                raidInfo = None,
            ),
        ))

        return WatchStreakTtsAnnouncementResult.OK
