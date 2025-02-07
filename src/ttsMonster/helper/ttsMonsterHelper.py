import traceback
from asyncio import AbstractEventLoop

import aiofiles
import aiofiles.os
import aiofiles.ospath

from .ttsMonsterHelperInterface import TtsMonsterHelperInterface
from .ttsMonsterPrivateApiHelperInterface import TtsMonsterPrivateApiHelperInterface
from ..models.ttsMonsterFileReference import TtsMonsterFileReference
from ..settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from ...glacialTtsStorage.helper.glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.ttsProvider import TtsProvider


class TtsMonsterHelper(TtsMonsterHelperInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface,
        timber: TimberInterface,
        ttsMonsterPrivateApiHelper: TtsMonsterPrivateApiHelperInterface,
        ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(glacialTtsFileRetriever, GlacialTtsFileRetrieverInterface):
            raise TypeError(f'glacialTtsFileRetriever argument is malformed: \"{glacialTtsFileRetriever}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterPrivateApiHelper, TtsMonsterPrivateApiHelperInterface):
            raise TypeError(f'ttsMonsterPrivateApiHelper argument is malformed: \"{ttsMonsterPrivateApiHelper}\"')
        elif not isinstance(ttsMonsterSettingsRepository, TtsMonsterSettingsRepositoryInterface):
            raise TypeError(f'ttsMonsterSettingsRepository argument is malformed: \"{ttsMonsterSettingsRepository}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface = glacialTtsFileRetriever
        self.__timber: TimberInterface = timber
        self.__ttsMonsterPrivateApiHelper: TtsMonsterPrivateApiHelperInterface = ttsMonsterPrivateApiHelper
        self.__ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface = ttsMonsterSettingsRepository

    async def generateTts(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TtsMonsterFileReference | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(message):
            return None

        glacialFile = await self.__glacialTtsFileRetriever.findFile(
            message = message,
            provider = TtsProvider.TTS_MONSTER
        )

        if glacialFile is not None:
            return TtsMonsterFileReference(
                fileName = glacialFile.fileName,
                filePath = glacialFile.filePath
            )

        speechBytes = await self.__ttsMonsterPrivateApiHelper.getSpeech(
            message = message,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if speechBytes is None:
            return None

        glacialFile = await self.__glacialTtsFileRetriever.saveFile(
            fileExtension = await self.__ttsMonsterSettingsRepository.getFileExtension(),
            message = message,
            provider = TtsProvider.TTS_MONSTER
        )

        return TtsMonsterFileReference(
            fileName = glacialFile.fileName,
            filePath = glacialFile.filePath
        )

    async def __saveSpeechBytes(
        self,
        speechBytes: bytes,
        filePath: str
    ):
        if not isinstance(speechBytes, bytes):
            raise TypeError(f'speechBytes argument is malformed: \"{speechBytes}\"')
        elif not utils.isValidStr(filePath):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')

        try:
            async with aiofiles.open(
                file = filePath,
                mode = 'wb',
                loop = self.__eventLoop
            ) as file:
                await file.write(speechBytes)
                await file.flush()
        except Exception as e:
            self.__timber.log('TtsMonsterHelper', f'Encountered exception when trying to write TTS Monster speechBytes to file ({filePath=}): {e}', e, traceback.format_exc())
            raise e
