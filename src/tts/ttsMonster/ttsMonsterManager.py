import locale
import math
from queue import SimpleQueue

from .ttsMonsterFileManagerInterface import TtsMonsterFileManagerInterface
from .ttsMonsterManagerInterface import TtsMonsterManagerInterface
from ..tempFileHelper.ttsTempFileHelperInterface import TtsTempFileHelperInterface
from ..ttsEvent import TtsEvent
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface
from ...ttsMonster.helper.ttsMonsterHelperInterface import TtsMonsterHelperInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface


class TtsMonsterManager(TtsMonsterManagerInterface):

    def __init__(
        self,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsMonsterFileManager: TtsMonsterFileManagerInterface,
        ttsMonsterHelper: TtsMonsterHelperInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        ttsTempFileHelper: TtsTempFileHelperInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterFileManager, TtsMonsterFileManagerInterface):
            raise TypeError(f'ttsMonsterFileManager argument is malformed: \"{ttsMonsterFileManager}\"')
        elif not isinstance(ttsMonsterHelper, TtsMonsterHelperInterface):
            raise TypeError(f'ttsMonsterHelper argument is malformed: \"{ttsMonsterHelper}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(ttsTempFileHelper, TtsTempFileHelperInterface):
            raise TypeError(f'ttsTempFileHelper argument is malformed: \"{ttsTempFileHelper}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsMonsterFileManager: TtsMonsterFileManagerInterface = ttsMonsterFileManager
        self.__ttsMonsterHelper: TtsMonsterHelperInterface = ttsMonsterHelper
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__ttsTempFileHelper: TtsTempFileHelperInterface = ttsTempFileHelper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__isLoading: bool = False
        self.__currentPlaylist: SimpleQueue[str] = SimpleQueue()
        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def isPlaying(self) -> bool:
        if self.__isLoading:
            return True
        elif not self.__currentPlaylist.empty():
            return True

        # TODO Technically this method use is incorrect, as it is possible for SoundPlayerManager
        #  to be playing media, but it could be media that is completely unrelated to TTS Monster,
        #  and yet in this scenario, this method would still return true. So the fix for this is
        #  to check if SoundPlayerManager is currently playing, AND also a check to see
        #  specifically what media it is currently playing.
        return await self.__soundPlayerManager.isPlaying()

    async def playTtsEvent(self, event: TtsEvent) -> bool:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isEnabled():
            return False
        elif await self.isPlaying():
            self.__timber.log('TtsMonsterManager', f'There is already an ongoing TTS Monster event!')
            return False

        self.__isLoading = True

        ttsMonsterUrls = await self.__ttsMonsterHelper.generateTts(
            message = event.message,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId
        )

        if ttsMonsterUrls is None or len(ttsMonsterUrls.urls) == 0:
            self.__timber.log('TtsMonsterManager', f'Failed to generate any TTS messages ({event=}) ({ttsMonsterUrls=})')
            self.__isLoading = False
            return False

        ttsFileNames = await self.__ttsMonsterFileManager.saveTtsUrlsToNewFiles(ttsMonsterUrls.urls)

        if ttsFileNames is None or len(ttsFileNames) == 0:
            self.__timber.log('TtsMonsterManager', f'Failed to download/save TTS messages ({event=}) ({ttsMonsterUrls=}) ({ttsFileNames=})')
            self.__isLoading = False
            return False

        for ttsFileName in ttsFileNames:
            self.__currentPlaylist.put_nowait(ttsFileName)

        await self.__reportCharacterUsage(
            characterUsage = ttsMonsterUrls.characterUsage,
            twitchChannel = event.twitchChannel
        )

        self.__timber.log('TtsMonsterManager', f'Playing {len(ttsFileNames)} TTS message(s) in \"{event.twitchChannel}\"...')
        # TODO send sound event(s) to the sound player manager
        self.__isLoading = False

        return True

    async def __reportCharacterUsage(self, characterUsage: int | None, twitchChannel: str):
        if not utils.isValidInt(characterUsage) or self.__twitchChannelProvider is None:
            return

        remainingCharacters = 10000 - characterUsage
        usagePercent = str(int(math.ceil((float(characterUsage) / float(10000)) * float(100)))) + '%'
        self.__timber.log('TtsMonsterManager', f'TTS Monster character usage in \"{twitchChannel}\" is currently {characterUsage} ({remainingCharacters=}) ({usagePercent=})')

        twitchChannel = await self.__twitchChannelProvider.getTwitchChannel(twitchChannel)
        characterUsageStr = locale.format_string("%d", characterUsage, grouping = True)
        remainingCharactersStr = locale.format_string("%d", remainingCharacters, grouping = True)

        await self.__twitchUtils.waitThenSend(
            messageable = twitchChannel,
            delaySeconds = 5,
            message = f'TTS Monster character usage is currently {characterUsageStr} (remaining characters: {remainingCharactersStr}) (usage percent: {usagePercent})'
        )

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
