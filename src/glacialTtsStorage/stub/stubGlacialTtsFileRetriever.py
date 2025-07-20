import re
import uuid
from datetime import datetime
from typing import Final, Pattern

from ..fileRetriever.glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from ..models.glacialTtsData import GlacialTtsData
from ..models.glacialTtsFileReference import GlacialTtsFileReference
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...tts.directoryProvider.ttsDirectoryProviderInterface import TtsDirectoryProviderInterface
from ...tts.models.ttsProvider import TtsProvider


class StubGlacialTtsFileRetriever(GlacialTtsFileRetrieverInterface):

    def __init__(
        self,
        timeZoneRepository: TimeZoneRepositoryInterface,
        ttsDirectoryProvider: TtsDirectoryProviderInterface,
        directory: str = '../tts',
    ):
        if not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(ttsDirectoryProvider, TtsDirectoryProviderInterface):
            raise TypeError(f'ttsDirectoryProvider argument is malformed: \"{ttsDirectoryProvider}\"')
        elif not utils.isValidStr(directory):
            raise TypeError(f'directory argument is malformed: \"{directory}\"')

        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__ttsDirectoryProvider: Final[TtsDirectoryProviderInterface] = ttsDirectoryProvider
        self.__directory: Final[str] = directory

        self.__fileNameRegEx: Final[Pattern] = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def findFile(
        self,
        message: str,
        voice: str | None,
        provider: TtsProvider,
    ) -> GlacialTtsFileReference | None:
        # this method is intentionally empty
        return None

    async def __generateRandomId(self) -> str:
        randomUuid = self.__fileNameRegEx.sub('', str(uuid.uuid4()))
        return randomUuid.casefold()

    async def saveFile(
        self,
        fileExtension: str,
        message: str,
        voice: str | None,
        provider: TtsProvider,
    ) -> GlacialTtsFileReference:
        providerFolder = await self.__ttsDirectoryProvider.getFullTtsDirectoryFor(provider)
        glacialId = await self.__generateRandomId()
        filePath = f'{providerFolder}/{glacialId}.{fileExtension}'
        storeDateTime = datetime.now(self.__timeZoneRepository.getDefault())

        return GlacialTtsFileReference(
            glacialTtsData = GlacialTtsData(
                storeDateTime = storeDateTime,
                glacialId = glacialId,
                message = message,
                voice = voice,
                provider = provider,
            ),
            fileName = glacialId,
            filePath = filePath,
        )
