import aiofiles.ospath
from frozenlist import FrozenList

from .halfLifeServiceInterface import HalfLifeServiceInterface
from ..models.halfLifeVoice import HalfLifeVoice
from ...misc import utils as utils


class HalfLifeService(HalfLifeServiceInterface):

    async def getWavs(
        self,
        directory: str,
        text: str,
        voice: HalfLifeVoice
    ) -> FrozenList[str]:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')
        elif not isinstance(voice, HalfLifeVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        #TODO some filenames contain `_` meaning there's 2 words and this is going to miss them.
        paths: list[str] = []
        for word in text.split(' '):
            path = await self.getWav(directory, word, voice)
            if path is not None:
                paths.append(path)

        return FrozenList(paths)

    async def getWav(
        self,
        directory: str,
        text: str,
        voice: HalfLifeVoice
    ) -> str | None:
        if voice.value == HalfLifeVoice.ALL.value:
            for possibleVoice in HalfLifeVoice:
                path = await self.getPath(directory, text, possibleVoice)
                if path is not None:
                    return path
        else:
            path = await self.getPath(directory, text, voice)
            if path is not None:
                return path

        return None

    async def getPath(
        self,
        directory: str,
        file: str | None,
        voice: HalfLifeVoice
    ) -> str | None:
        if not utils.isValidStr(file):
            return None

        path = f'{directory}/{voice.value}/{file}.wav'
        if await aiofiles.ospath.exists(path) and await aiofiles.ospath.isfile(path):
            return path
        else:
            return None