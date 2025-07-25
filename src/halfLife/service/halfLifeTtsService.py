import random
import re
from asyncio import AbstractEventLoop
from typing import Collection, Final, Pattern

import aiofiles.os
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

        self.__soundFileNameRegEx: Final[Pattern] = re.compile(r'^(.+)\.(mp3)|(wav)$', re.IGNORECASE)
        self.__textNormalizerRegEx: Final[Pattern] = re.compile(r'[^a-z0-9]', re.IGNORECASE)

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

        voices: FrozenList[HalfLifeVoice] = FrozenList()

        if voice is None or voice is HalfLifeVoice.ALL:
            voices.extend(HalfLifeVoice)
            voices.remove(HalfLifeVoice.ALL)
        else:
            voices.append(voice)

        voices.freeze()

        soundsDirectory = await self.__halfLifeSettingsRepository.requireSoundsDirectory()
        soundFiles: FrozenList[HalfLifeSoundFile] = FrozenList()

        for text in utils.getCleanedSplits(message):
            normalizedText = self.__textNormalizerRegEx.sub('', text).casefold()

            if not utils.isValidStr(normalizedText):
                continue

            soundFile = await self.__findSoundFile(
                voices = voices,
                directory = soundsDirectory,
                text = normalizedText,
            )

            if soundFile is not None:
                soundFiles.append(soundFile)

        soundFiles.freeze()
        return soundFiles

    async def __findSoundFile(
        self,
        voices: Collection[HalfLifeVoice],
        directory: str,
        text: str,
    ) -> HalfLifeSoundFile | None:
        # shuffle the voice order to introduce more random/organic/fun voice selections
        shuffledVoices: list[HalfLifeVoice] = list(voices)
        random.shuffle(shuffledVoices)

        for voice in shuffledVoices:
            path = await self.__scanDirectoryForFile(
                directory = f'{directory}/{voice.keyName}',
                text = text,
            )

            if utils.isValidStr(path):
                return HalfLifeSoundFile(
                    voice = voice,
                    path = path,
                    text = text,
                )

        return None

    async def __scanDirectoryForFile(
        self,
        directory: str,
        text: str,
    ) -> str | None:
        if not await aiofiles.ospath.isdir(
            s = directory,
            loop = self.__eventLoop,
        ):
            return None

        directoryContents = await aiofiles.os.scandir(
            path = directory,
            loop = self.__eventLoop,
        )

        matchingFiles: list[str] = list()

        for entry in directoryContents:
            if not entry.is_file():
                continue

            fileNameMatch = self.__soundFileNameRegEx.fullmatch(entry.name)
            if fileNameMatch is None or not utils.isValidStr(fileNameMatch.group(1)):
                continue

            normalizedFileName = self.__textNormalizerRegEx.sub('', fileNameMatch.group(1))
            if not utils.isValidStr(normalizedFileName):
                continue
            elif normalizedFileName.casefold() == text:
                matchingFiles.append(entry.name)

        if len(matchingFiles) == 0:
            return None

        chosenFile = random.choice(matchingFiles)
        return f'{directory}/{chosenFile}'
