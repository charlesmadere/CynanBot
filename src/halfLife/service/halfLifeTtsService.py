import random
from asyncio import AbstractEventLoop
from typing import Collection, Final

import aiofiles.ospath
from frozenlist import FrozenList

from .halfLifeTtsServiceInterface import HalfLifeTtsServiceInterface
from ..models.halfLifeSoundFile import HalfLifeSoundFile
from ..models.halfLifeVoice import HalfLifeVoice
from ..settings.halfLifeSettingsRepositoryInterface import HalfLifeSettingsRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class HalfLifeTtsService(HalfLifeTtsServiceInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface,
        timber: TimberInterface,
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(halfLifeSettingsRepository, HalfLifeSettingsRepositoryInterface):
            raise TypeError(f'halfLifeSettingsRepository argument is malformed: \"{halfLifeSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__halfLifeSettingsRepository: Final[HalfLifeSettingsRepositoryInterface] = halfLifeSettingsRepository
        self.__timber: Final[TimberInterface] = timber

    async def __determineFilePath(
        self,
        voice: HalfLifeVoice,
        directory: str,
        text: str | None,
    ) -> str | None:
        if not utils.isValidStr(text):
            return None

        fileExtension = await self.__halfLifeSettingsRepository.requireFileExtension()
        filePath = f'{directory}/{voice.keyName}/{text}.{fileExtension}'

        if await aiofiles.ospath.isfile(
            path = filePath,
            loop = self.__eventLoop,
        ):
            return filePath
        else:
            return None

    async def findSoundFiles(
        self,
        voice: HalfLifeVoice | None,
        message: str | None,
    ) -> FrozenList[HalfLifeSoundFile] | None:
        if voice is not None and not isinstance(voice, HalfLifeVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if not utils.isValidStr(message):
            return None

        voices: FrozenList[HalfLifeVoice]

        if voice is None or voice is HalfLifeVoice.ALL:
            voices = FrozenList(HalfLifeVoice)
            voices.remove(HalfLifeVoice.ALL)
        else:
            voices = FrozenList()
            voices.append(voice)

        voices.freeze()

        message = message.lower()
        soundsDirectory = await self.__halfLifeSettingsRepository.requireSoundsDirectory()
        soundFiles: FrozenList[HalfLifeSoundFile] = FrozenList()

        for text in utils.getCleanedSplits(message):
            soundFile = await self.__findSoundFile(
                voices = voices,
                directory = soundsDirectory,
                text = text,
            )

            if soundFile is not None:
                soundFiles.append(soundFile)

        soundFiles.freeze()
        return soundFiles

    async def __findSoundFile(
        self,
        voices: Collection[HalfLifeVoice],
        directory: str,
        text: str | None,
    ) -> HalfLifeSoundFile | None:
        if not utils.isValidStr(text):
            return None

        # shuffle the voice order to introduce more random/organic/fun voice selections
        shuffledVoices: list[HalfLifeVoice] = list(voices)
        random.shuffle(shuffledVoices)

        for voice in shuffledVoices:
            filePath = await self.__determineFilePath(
                voice = voice,
                directory = directory,
                text = text,
            )

            if utils.isValidStr(filePath):
                return HalfLifeSoundFile(
                    voice = voice,
                    path = filePath,
                    text = text,
                )

        return None
