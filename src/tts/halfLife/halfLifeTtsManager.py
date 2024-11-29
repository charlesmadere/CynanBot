from frozenlist import FrozenList
from ..ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..ttsEvent import TtsEvent
from ..ttsManagerInterface import TtsManagerInterface
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...halfLife.helper.halfLifeHelperInterface import HalfLifeHelperInterface
from ...halfLife.settings.halfLifeSettingsRepositoryInterface import HalfLifeSettingsRepositoryInterface
from ...messageCleaner.messageCleanerInterface import MessageCleanerInterface
from ...timber.timberInterface import TimberInterface


class HalfLifeTtsManager(TtsManagerInterface):

    def __init__(
        self,
        soundPlayerManager: SoundPlayerManagerInterface,
        halfLifeHelper: HalfLifeHelperInterface,
        messageCleaner: MessageCleanerInterface,
        halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(halfLifeHelper, HalfLifeHelperInterface):
            raise TypeError(f'halfLifeHelper argument is malformed: \"{halfLifeHelper}\"')
        elif not isinstance(messageCleaner, MessageCleanerInterface):
            raise TypeError(f'messageCleaner argument is malformed: \"{messageCleaner}\"')
        elif not isinstance(halfLifeSettingsRepository, HalfLifeSettingsRepositoryInterface):
            raise TypeError(f'halfLifeSettingsRepository argument is malformed: \"{halfLifeSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__halfLifeHelper: HalfLifeHelperInterface = halfLifeHelper
        self.__halfLifeMessageCleaner: MessageCleanerInterface = messageCleaner
        self.__halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface = halfLifeSettingsRepository
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__isLoading: bool = False

    async def isPlaying(self) -> bool:
        if self.__isLoading:
            return True

        # TODO Technically this method use is incorrect, as it is possible for SoundPlayerManager
        #  to be playing media, but it could be media that is completely unrelated to Half Life
        #  TTS, and yet in this scenario, this method would still return true. So for
        #  the fix for this is probably a way to check if SoundPlayerManager is currently playing,
        #  AND also a check to see specifically what media it is currently playing.
        return await self.__soundPlayerManager.isPlaying()

    async def playTtsEvent(self, event: TtsEvent) -> bool:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isEnabled():
            return False
        elif await self.isPlaying():
            self.__timber.log('HalfLifeTtsManager', f'There is already an ongoing Half Life TTS event!')
            return False

        self.__isLoading = True
        fileNames = await self.__processTtsEvent(event)

        if fileNames is None:
            return False
        
        await self.__soundPlayerManager.playPlaylist(
            fileNames, 
            await self.__halfLifeSettingsRepository.getMediaPlayerVolume()
        )
        
        self.__isLoading = False

        return True

    async def __processTtsEvent(self, event: TtsEvent) -> FrozenList[str] | None:
        message = await self.__halfLifeMessageCleaner.clean(event.message)
        donationPrefix = await self.__ttsCommandBuilder.buildDonationPrefix(event)
        fullMessage: str

        if utils.isValidStr(message) and utils.isValidStr(donationPrefix):
            fullMessage = f'{donationPrefix} {message}'
        elif utils.isValidStr(message):
            fullMessage = message
        elif utils.isValidStr(donationPrefix):
            fullMessage = donationPrefix
        else:
            return None

        if not utils.isValidStr(message):
            return None

        speechFiles = await self.__halfLifeHelper.getSpeech(fullMessage)

        if speechFiles is None:
            self.__timber.log('HalfLifeTtsManager', f'Failed to fetch TTS speech in \"{event.twitchChannel}\" ({event=}) ({speechFiles=})')
            return None

        return speechFiles
