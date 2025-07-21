from typing import Final

import aiofiles.ospath
from frozenlist import FrozenList

from .halfLifeTtsServiceInterface import HalfLifeTtsServiceInterface
from ..models.halfLifeVoice import HalfLifeVoice
from ..settings.halfLifeSettingsRepositoryInterface import HalfLifeSettingsRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class HalfLifeTtsService(HalfLifeTtsServiceInterface):

    def __init__(
        self,
        halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface,
        timber: TimberInterface,
    ):
        if not isinstance(halfLifeSettingsRepository, HalfLifeSettingsRepositoryInterface):
            raise TypeError(f'halfLifeSettingsRepository argument is malformed: \"{halfLifeSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__halfLifeSettingsRepository: Final[HalfLifeSettingsRepositoryInterface] = halfLifeSettingsRepository
        self.__timber: Final[TimberInterface] = timber

        self.__cache: Final[dict[str, str | None]] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('HalfLifeTtsService', 'Caches cleared')

    async def __determinePath(
        self,
        voice: HalfLifeVoice,
        directory: str,
        text: str | None,
    ) -> str | None:
        if not utils.isValidStr(text):
            return None

        fileExtension = await self.__halfLifeSettingsRepository.requireFileExtension()
        path = f'{directory}/{voice.keyName}/{text}.{fileExtension}'

        if await aiofiles.ospath.exists(path) and await aiofiles.ospath.isfile(path):
            return path
        else:
            return None

    async def __findFile(
        self,
        voice: HalfLifeVoice,
        directory: str,
        text: str | None,
    ) -> str | None:
        if not utils.isValidStr(text):
            return None

        cachedFile = self.__cache.get(text + voice.keyName, None)
        if utils.isValidStr(cachedFile):
            return cachedFile

        path: str | None = None

        if voice is HalfLifeVoice.ALL:
            for possibleVoice in HalfLifeVoice:
                path = await self.__determinePath(
                    voice = possibleVoice,
                    directory = directory,
                    text = text,
                )

                if utils.isValidStr(path):
                    break
        else:
            path = await self.__determinePath(
                voice = voice,
                directory = directory,
                text = text,
            )

        if utils.isValidStr(path):
            self.__cache[text + voice.keyName] = path
            return path
        else:
            return None

    async def findSoundFiles(
        self,
        voice: HalfLifeVoice | None,
        message: str | None,
    ) -> FrozenList[HalfLifeTtsServiceInterface.SoundFile] | None:
        if voice is not None and not isinstance(voice, HalfLifeVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        # TODO
        return None

    async def getWavs(
        self,
        voice: HalfLifeVoice,
        message: str | None,
    ) -> FrozenList[str] | None:
        if not isinstance(voice, HalfLifeVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if not utils.isValidStr(message):
            return None

        paths: list[str] = list()
        soundsDirectory = await self.__halfLifeSettingsRepository.requireSoundsDirectory()

        # TODO some filenames contain `_` meaning there's 2 words and this is going to miss them.
        for word in utils.getCleanedSplits(message):
            path = await self.__findFile(
                voice = voice,
                directory = soundsDirectory,
                text = word,
            )

            if utils.isValidStr(path):
                paths.append(path)

        frozenPaths: FrozenList[str] = FrozenList(paths)
        frozenPaths.freeze()
        return frozenPaths
