import locale
import math

from frozenlist import FrozenList

from .ttsMonsterFileManagerInterface import TtsMonsterFileManagerInterface
from .ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
from ..ttsEvent import TtsEvent
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface
from ...ttsMonster.helper.ttsMonsterHelperInterface import TtsMonsterHelperInterface
from ...ttsMonster.settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface


class TtsMonsterTtsManager(TtsMonsterTtsManagerInterface):

    def __init__(
        self,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsMonsterFileManager: TtsMonsterFileManagerInterface,
        ttsMonsterHelper: TtsMonsterHelperInterface,
        ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
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
        elif not isinstance(ttsMonsterSettingsRepository, TtsMonsterSettingsRepositoryInterface):
            raise TypeError(f'ttsMonsterSettingsRepository argument is malformed: \"{ttsMonsterSettingsRepository}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsMonsterFileManager: TtsMonsterFileManagerInterface = ttsMonsterFileManager
        self.__ttsMonsterHelper: TtsMonsterHelperInterface = ttsMonsterHelper
        self.__ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface = ttsMonsterSettingsRepository
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__isLoading: bool = False
        self.__playSessionId: str | None = None
        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __executeTts(self, fileNames: FrozenList[str]):
        timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()

        # TODO add logic to kill TTS Monster if it runs too long

        self.__playSessionId = await self.__soundPlayerManager.playPlaylist(
            filePaths = fileNames,
            volume = await self.__ttsMonsterSettingsRepository.getMediaPlayerVolume()
        )


    async def isPlaying(self) -> bool:
        if self.__isLoading:
            return True

        # TODO Technically this method use is incorrect, as it is possible for SoundPlayerManager
        #  to be playing media, but it could be media that is completely unrelated to TTS Monster,
        #  and yet in this scenario, this method would still return true. So for the fix for this
        #  is probably a way to check if SoundPlayerManager is currently playing, AND also a check
        #  to see specifically what media it is currently playing.
        return await self.__soundPlayerManager.isPlaying()

    async def playTtsEvent(self, event: TtsEvent) -> bool:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isEnabled():
            return False
        elif await self.isPlaying():
            self.__timber.log('ttsMonsterTtsManager', f'There is already an ongoing TTS Monster event!')
            return False

        self.__isLoading = True

        ttsMonsterUrls = await self.__ttsMonsterHelper.generateTts(
            message = event.message,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId
        )

        if ttsMonsterUrls is None or len(ttsMonsterUrls.urls) == 0:
            self.__timber.log('ttsMonsterTtsManager', f'Failed to generate any TTS messages ({event=}) ({ttsMonsterUrls=})')
            self.__isLoading = False
            return False

        fileNames = await self.__ttsMonsterFileManager.saveTtsUrlsToNewFiles(ttsMonsterUrls.urls)

        if fileNames is None or len(fileNames) == 0:
            self.__timber.log('ttsMonsterTtsManager', f'Failed to download/save TTS messages ({event=}) ({ttsMonsterUrls=}) ({fileNames=})')
            self.__isLoading = False
            return False

        await self.__reportCharacterUsage(
            characterAllowance = ttsMonsterUrls.characterAllowance,
            characterUsage = ttsMonsterUrls.characterUsage,
            twitchChannel = event.twitchChannel
        )

        self.__timber.log('ttsMonsterTtsManager', f'Playing {len(fileNames)} TTS message(s) in \"{event.twitchChannel}\"...')
        await self.__executeTts(fileNames = fileNames)

        self.__isLoading = False
        return True

    async def __reportCharacterUsage(
        self,
        characterAllowance: int | None,
        characterUsage: int | None,
        twitchChannel: str
    ):
        if not utils.isValidInt(characterUsage):
            return

        twitchChannelProvider = self.__twitchChannelProvider
        if twitchChannelProvider is None:
            return

        remainingCharactersString = ''
        usagePercentString = ''
        if utils.isValidInt(characterAllowance):
            remainingCharacters = locale.format_string("%d", characterAllowance - characterUsage, grouping = True)
            remainingCharactersString = f'(remaining characters: {remainingCharacters})'

            usagePercent = str(int(math.ceil((float(characterUsage) / float(characterAllowance)) * float(100)))) + '%'
            usagePercentString = f'({usagePercent} usage)'

        self.__timber.log('ttsMonsterTtsManager', f'Current TTS Monster character usage stats in \"{twitchChannel}\": ({characterUsage=}) ({characterAllowance=}) ({usagePercentString=})')

        characterUsageString = locale.format_string("%d", characterUsage, grouping = True)
        messageable = await twitchChannelProvider.getTwitchChannel(twitchChannel)

        await self.__twitchUtils.waitThenSend(
            messageable = messageable,
            delaySeconds = 3,
            message = f'ⓘ TTS Monster character usage is currently {characterUsageString} {remainingCharactersString} {usagePercentString}'.strip()
        )

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    async def stopTtsEvent(self):
        playSessionId = self.__playSessionId
        if not utils.isValidStr(playSessionId):
            return

        self.__playSessionId = None
        stopResult = await self.__soundPlayerManager.stopPlaySessionId(
            playSessionId = playSessionId
        )

        self.__timber.log('ttsMonsterTtsManager', f'Stopped TTS event ({playSessionId=}) ({stopResult=})')
