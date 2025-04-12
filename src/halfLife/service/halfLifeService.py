import aiofiles.ospath
from frozenlist import FrozenList

from .halfLifeServiceInterface import HalfLifeServiceInterface
from ..models.halfLifeVoice import HalfLifeVoice
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class HalfLifeService(HalfLifeServiceInterface):

    def __init__(
        self,
        timber: TimberInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

        self.__cache: dict[str, str | None] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('HalfLifeService', 'Caches cleared')

    async def __getPath(
        self,
        directory: str,
        file: str | None,
        voice: HalfLifeVoice
    ) -> str | None:
        if not utils.isValidStr(file):
            return None

        path = f'{directory}/{voice.keyName}/{file}.wav'

        if await aiofiles.ospath.exists(path) and await aiofiles.ospath.isfile(path):
            self.__cache[file + voice.keyName] = path
            return path
        else:
            return None

    async def __getWav(
        self,
        directory: str,
        text: str,
        voice: HalfLifeVoice
    ) -> str | None:
        cachedWav: str | None = self.__cache.get(text + voice.keyName, None)

        if utils.isValidStr(cachedWav):
            return cachedWav

        if voice is HalfLifeVoice.ALL:
            for possibleVoice in HalfLifeVoice:
                path = await self.__getPath(directory, text, possibleVoice)
                if path is not None:
                    return path
        else:
            path = await self.__getPath(directory, text, voice)
            if path is not None:
                return path

        return None

    async def getWavs(
        self,
        directory: str,
        text: str,
        voice: HalfLifeVoice
    ) -> FrozenList[str]:
        if not utils.isValidStr(directory):
            raise TypeError(f'directory argument is malformed: \"{directory}\"')
        elif not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')
        elif not isinstance(voice, HalfLifeVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        #TODO some filenames contain `_` meaning there's 2 words and this is going to miss them.
        paths: list[str] = []
        for word in text.split(' '):
            path = await self.__getWav(directory, word, voice)
            if path is not None:
                paths.append(path)

        frozenPaths: FrozenList[str] = FrozenList(paths)
        frozenPaths.freeze()

        return frozenPaths
