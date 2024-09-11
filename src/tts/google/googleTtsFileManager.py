import base64
import re
import traceback
import uuid
from asyncio import AbstractEventLoop
from typing import Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath

from .googleFileExtensionHelperInterface import GoogleFileExtensionHelperInterface
from .googleTtsFileManagerInterface import GoogleTtsFileManagerInterface
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class GoogleTtsFileManager(GoogleTtsFileManagerInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        googleFileExtensionHelper: GoogleFileExtensionHelperInterface,
        timber: TimberInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        directory: str = 'temp'
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(googleFileExtensionHelper, GoogleFileExtensionHelperInterface):
            raise TypeError(f'googleFileExtensionHelper argument is malformed: \"{googleFileExtensionHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not utils.isValidStr(directory):
            raise TypeError(f'directory argument is malformed: \"{directory}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__googleFileExtensionHelper: GoogleFileExtensionHelperInterface = googleFileExtensionHelper
        self.__timber: TimberInterface = timber
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__directory: str = utils.cleanPath(directory)

        self.__fileNameRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def __decodeBase64Command(self, base64Command: str | None) -> bytes | None:
        if base64Command is None:
            return None
        elif not isinstance(base64Command, str):
            raise TypeError(f'base64Command argument is malformed: \"{base64Command}\"')
        elif not utils.isValidStr(base64Command):
            return None

        decoded = base64.b64decode(
            s = base64Command,
            validate = True
        )

        if decoded is None or len(decoded) == 0:
            self.__timber.log('GoogleTtsFileManager', f'Unable to decode base64Command into bytes ({decoded=})')
            return None

        return decoded

    async def __getGoogleFileExtension(self) -> str:
        audioEncoding = await self.__ttsSettingsRepository.getGoogleVoiceAudioEncoding()
        return await self.__googleFileExtensionHelper.getFileExtension(audioEncoding)

    async def writeBase64CommandToNewFile(self, base64Command: str) -> str | None:
        if not utils.isValidStr(base64Command):
            raise TypeError(f'base64Command argument is malformed: \"{base64Command}\"')

        decoded = await self.__decodeBase64Command(base64Command)

        if decoded is None:
            self.__timber.log('GoogleTtsFileManager', f'Unable to decode base64Command ({base64Command=})')
            return None

        if not await aiofiles.ospath.exists(self.__directory):
            await aiofiles.os.makedirs(self.__directory)

        fileName: str | None = None
        fileExtension = await self.__getGoogleFileExtension()

        while not utils.isValidStr(fileName) or await aiofiles.ospath.exists(fileName):
            randomUuid = self.__fileNameRegEx.sub('', str(uuid.uuid4()))
            fileName = utils.cleanPath(f'{self.__directory}/google-{randomUuid}.{fileExtension}')

        try:
            async with aiofiles.open(
                file = fileName,
                mode = 'wb',
                loop = self.__eventLoop
            ) as file:
                await file.write(decoded)
                await file.flush()
        except Exception as e:
            self.__timber.log('GoogleTtsFileManager', f'Encountered exception when trying to write command to TTS file (\"{fileName}\"): {e}', e, traceback.format_exc())
            fileName = None

        return fileName
