import random
import re
from typing import Pattern

import aiofiles.os
import aiofiles.ospath
from frozendict import frozendict
from frozenlist import FrozenList

from .chatBandInstrument import ChatBandInstrument
from .chatBandInstrumentSoundsRepositoryInterface import ChatBandInstrumentSoundsRepositoryInterface
from ..misc import utils as utils
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..timber.timberInterface import TimberInterface


class ChatBandInstrumentSoundsRepository(ChatBandInstrumentSoundsRepositoryInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__timber: TimberInterface = timber

        self.__cache: frozendict[ChatBandInstrument, FrozenList[str] | None] | None = None
        self.__soundFileRegEx: Pattern = re.compile(r'^\w[\w\s]*\s?(\(shiny\))?\.(mp3|ogg|wav)$', re.IGNORECASE)

    async def clearCaches(self):
        self.__cache = None
        self.__timber.log('ChatBandInstrumentSoundsRepository', f'Caches cleared')

    async def __getInstrumentDirectoryName(self, instrument: ChatBandInstrument) -> str | None:
        if not isinstance(instrument, ChatBandInstrument):
            raise TypeError(f'instrument argument is malformed: \"{instrument}\"')

        match instrument:
            case ChatBandInstrument.BASS: return 'bass'
            case ChatBandInstrument.DRUMS: return 'drums'
            case ChatBandInstrument.GUITAR: return 'guitar'
            case ChatBandInstrument.MAGIC: return 'magic'
            case ChatBandInstrument.PIANO: return 'piano'
            case ChatBandInstrument.SYNTH: return 'synth'
            case ChatBandInstrument.TRUMPET: return 'trumpet'
            case ChatBandInstrument.VIOLIN: return 'violin'
            case ChatBandInstrument.WHISTLE: return 'whistle'
            case _: raise ValueError(f'Encountered unexpected ChatBandInstrument value: \"{instrument}\"')

    async def getRandomSound(self, instrument: ChatBandInstrument) -> str | None:
        if not isinstance(instrument, ChatBandInstrument):
            raise TypeError(f'instrument argument is malformed: \"{instrument}\"')

        cache = self.__cache

        if cache is None:
            cache = await self.__loadInstrumentsCache()
            self.__cache = cache

        filePaths = cache.get(instrument, None)

        if filePaths is None or len(filePaths) == 0:
            return None

        return random.choice(filePaths)

    async def __loadInstrumentsCache(self) -> frozendict[ChatBandInstrument, FrozenList[str] | None]:
        cache: dict[ChatBandInstrument, FrozenList[str] | None] = dict()

        for instrument in ChatBandInstrument:
            directoryName = await self.__getInstrumentDirectoryName(instrument)
            filePaths = await self.__scanDirectoryForSoundFiles(directoryName)
            cache[instrument] = filePaths

        self.__timber.log('SoundPlayerRandomizerHelper', f'Finished loading in {len(cache)} sound alert(s)')
        return frozendict(cache)

    async def __scanDirectoryForSoundFiles(self, directoryName: str | None) -> FrozenList[str] | None:
        if not utils.isValidStr(directoryName):
            return None
        elif not await aiofiles.ospath.exists(directoryName):
            return None
        elif not await aiofiles.ospath.isdir(directoryName):
            return None

        directoryContents = await aiofiles.os.scandir(directoryName)

        if directoryContents is None:
            return None

        soundFilesSet: set[str] = set()

        for entry in directoryContents:
            if not entry.is_file():
                continue

            soundFileMatch = self.__soundFileRegEx.fullmatch(entry.name)

            if soundFileMatch is None:
                continue

            cleanPath = utils.cleanPath(entry.path)

            if utils.isValidStr(cleanPath):
                soundFilesSet.add(cleanPath)

        directoryContents.close()

        soundFilesList: list[str] = list(soundFilesSet)
        soundFilesList.sort(key = lambda path: path.casefold())

        frozenSoundFilesList: FrozenList[str] = FrozenList(soundFilesList)
        frozenSoundFilesList.freeze()
        return frozenSoundFilesList
