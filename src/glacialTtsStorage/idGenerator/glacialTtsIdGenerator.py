import hashlib

from .glacialTtsIdGeneratorInterface import GlacialTtsIdGeneratorInterface
from ...misc import utils as utils
from ...tts.models.ttsProvider import TtsProvider


class GlacialTtsIdGenerator(GlacialTtsIdGeneratorInterface):

    async def generateId(
        self,
        message: str,
        voice: str | None,
        provider: TtsProvider,
    ) -> str:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif voice is not None and not isinstance(voice, str):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        string = f'{provider.name}:{message}'

        if utils.isValidStr(voice):
            string = f'{string}:{voice}'

        encodedString = string.encode('utf-8')
        return hashlib.sha256(encodedString).hexdigest()
