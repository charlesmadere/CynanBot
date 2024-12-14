import asyncio
import locale
import math
from dataclasses import dataclass

from frozenlist import FrozenList

from .ttsMonsterFileManagerInterface import TtsMonsterFileManagerInterface
from .ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
from ..ttsEvent import TtsEvent
from ..ttsProvider import TtsProvider
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface
from ...ttsMonster.helper.ttsMonsterHelperInterface import TtsMonsterHelperInterface
from ...ttsMonster.settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from ...ttsMonster.ttsMonsterMessageCleanerInterface import TtsMonsterMessageCleanerInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface


class TtsMonsterTtsManager(TtsMonsterTtsManagerInterface):

    @dataclass(frozen = True)
    class TtsMonsterTtsEvent:
        fileNames: FrozenList[str]
        characterAllowance: int | None
        characterUsage: int | None

    def __init__(
        self,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsMonsterFileManager: TtsMonsterFileManagerInterface,
        ttsMonsterHelper: TtsMonsterHelperInterface,
        ttsMonsterMessageCleaner: TtsMonsterMessageCleanerInterface,
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
        elif not isinstance(ttsMonsterMessageCleaner, TtsMonsterMessageCleanerInterface):
            raise TypeError(f'ttsMonsterMessageCleaner argument is malformed: \"{ttsMonsterMessageCleaner}\"')
        elif not isinstance(ttsMonsterSettingsRepository, TtsMonsterSettingsRepositoryInterface):
            raise TypeError(f'ttsMonsterSettingsRepository argument is malformed: \"{ttsMonsterSettingsRepository}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsMonsterFileManager: TtsMonsterFileManagerInterface = ttsMonsterFileManager
        self.__ttsMonsterMessageCleaner: TtsMonsterMessageCleanerInterface = ttsMonsterMessageCleaner
        self.__ttsMonsterHelper: TtsMonsterHelperInterface = ttsMonsterHelper
        self.__ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface = ttsMonsterSettingsRepository
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__isLoadingOrPlaying: bool = False
        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __executeTts(self, fileNames: FrozenList[str]):
        volume = await self.__ttsMonsterSettingsRepository.getMediaPlayerVolume()
        timeoutSeconds = await self.__ttsSettingsRepository.getTtsTimeoutSeconds()

        async def playPlaylist():
            await self.__soundPlayerManager.playPlaylist(
                filePaths = fileNames,
                volume = volume
            )

            self.__isLoadingOrPlaying = False

        try:
            await asyncio.wait_for(playPlaylist(), timeout = timeoutSeconds)
        except TimeoutError as e:
            self.__timber.log('TtsMonsterTtsManager', f'Stopping TTS Monster TTS event due to timeout ({fileNames=}) ({timeoutSeconds=}): {e}', e)
            await self.stopTtsEvent()

    @property
    def isLoadingOrPlaying(self) -> bool:
        return self.__isLoadingOrPlaying

    async def playTtsEvent(self, event: TtsEvent):
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isEnabled():
            return
        elif self.isLoadingOrPlaying:
            self.__timber.log('TtsMonsterTtsManager', f'There is already an ongoing TTS Monster event!')
            return

        self.__isLoadingOrPlaying = True
        ttsMonsterTtsEvent = await self.__processTtsEvent(event)

        if ttsMonsterTtsEvent is None or len(ttsMonsterTtsEvent.fileNames) == 0:
            self.__timber.log('TtsMonsterTtsManager', f'Failed to generate any TTS messages ({event=}) ({ttsMonsterTtsEvent=})')
            self.__isLoadingOrPlaying = False
            return

        await self.__reportCharacterUsage(
            characterAllowance = ttsMonsterTtsEvent.characterAllowance,
            characterUsage = ttsMonsterTtsEvent.characterUsage,
            twitchChannel = event.twitchChannel
        )

        self.__timber.log('TtsMonsterTtsManager', f'Playing {len(ttsMonsterTtsEvent.fileNames)} TTS message(s) in \"{event.twitchChannel}\"...')
        await self.__executeTts(ttsMonsterTtsEvent.fileNames)

    async def __processTtsEvent(self, event: TtsEvent) -> TtsMonsterTtsEvent | None:
        message = await self.__ttsMonsterMessageCleaner.clean(event.message)

        ttsMonsterUrls = await self.__ttsMonsterHelper.generateTts(
            message = message,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId
        )

        if ttsMonsterUrls is None or len(ttsMonsterUrls.urls) == 0:
            self.__timber.log('TtsMonsterTtsManager', f'Failed to generate any TTS URLs ({event=}) ({ttsMonsterUrls=})')
            self.__isLoadingOrPlaying = False
            return

        fileNames = await self.__ttsMonsterFileManager.saveTtsUrlsToNewFiles(
            ttsUrls = ttsMonsterUrls.urls
        )

        if fileNames is None or len(fileNames) == 0:
            self.__timber.log('TtsMonsterTtsManager', f'Failed to download/save TTS messages ({event=}) ({ttsMonsterUrls=}) ({fileNames=})')
            self.__isLoadingOrPlaying = False
            return

        return TtsMonsterTtsManager.TtsMonsterTtsEvent(
            fileNames = fileNames,
            characterAllowance = ttsMonsterUrls.characterAllowance,
            characterUsage = ttsMonsterUrls.characterUsage
        )

    async def __reportCharacterUsage(
        self,
        characterAllowance: int | None,
        characterUsage: int | None,
        twitchChannel: str
    ):
        twitchChannelProvider = self.__twitchChannelProvider

        if twitchChannelProvider is None or not utils.isValidInt(characterUsage):
            return

        remainingCharactersString = ''
        usagePercentString = ''
        if utils.isValidInt(characterAllowance):
            remainingCharacters = locale.format_string("%d", characterAllowance - characterUsage, grouping = True)
            remainingCharactersString = f'(remaining characters: {remainingCharacters})'

            usagePercent = str(int(math.ceil((float(characterUsage) / float(characterAllowance)) * float(100)))) + '%'
            usagePercentString = f'({usagePercent} usage)'

        self.__timber.log('TtsMonsterTtsManager', f'Current TTS Monster character usage stats in \"{twitchChannel}\": ({characterUsage=}) ({characterAllowance=}) ({usagePercentString=})')

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
        if not self.isLoadingOrPlaying:
            return

        await self.__soundPlayerManager.stop()
        self.__timber.log('TtsMonsterTtsManager', f'Stopped TTS event')
        self.__isLoadingOrPlaying = False

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.TTS_MONSTER
