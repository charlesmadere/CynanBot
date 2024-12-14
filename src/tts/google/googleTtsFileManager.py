import base64
import traceback
from asyncio import AbstractEventLoop

import aiofiles
import aiofiles.os
import aiofiles.ospath

from .googleFileExtensionHelperInterface import GoogleFileExtensionHelperInterface
from .googleTtsFileManagerInterface import GoogleTtsFileManagerInterface
from ...google.settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from ...misc import utils as utils
from ...storage.tempFileHelperInterface import TempFileHelperInterface
from ...timber.timberInterface import TimberInterface


class GoogleTtsFileManager(GoogleTtsFileManagerInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        googleFileExtensionHelper: GoogleFileExtensionHelperInterface,
        googleSettingsRepository: GoogleSettingsRepositoryInterface,
        tempFileHelper: TempFileHelperInterface,
        timber: TimberInterface
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(googleFileExtensionHelper, GoogleFileExtensionHelperInterface):
            raise TypeError(f'googleFileExtensionHelper argument is malformed: \"{googleFileExtensionHelper}\"')
        elif not isinstance(googleSettingsRepository, GoogleSettingsRepositoryInterface):
            raise TypeError(f'googleSettingsRepository argument is malformed: \"{googleSettingsRepository}\"')
        elif not isinstance(tempFileHelper, TempFileHelperInterface):
            raise TypeError(f'tempFileHelper argument is malformed: \"{tempFileHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__googleFileExtensionHelper: GoogleFileExtensionHelperInterface = googleFileExtensionHelper
        self.__googleSettingsRepository: GoogleSettingsRepositoryInterface = googleSettingsRepository
        self.__tempFileHelper: TempFileHelperInterface = tempFileHelper
        self.__timber: TimberInterface = timber

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
        audioEncoding = await self.__googleSettingsRepository.getVoiceAudioEncoding()
        return await self.__googleFileExtensionHelper.getFileExtension(audioEncoding)

    async def writeBase64CommandToNewFile(self, base64Command: str) -> str | None:
        if not utils.isValidStr(base64Command):
            raise TypeError(f'base64Command argument is malformed: \"{base64Command}\"')

        decoded = await self.__decodeBase64Command(base64Command)

        if decoded is None:
            self.__timber.log('GoogleTtsFileManager', f'Unable to decode base64Command ({base64Command=})')
            return None

        fileName = await self.__tempFileHelper.getTempFileName(
            prefix = 'google',
            extension = await self.__getGoogleFileExtension()
        )

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
