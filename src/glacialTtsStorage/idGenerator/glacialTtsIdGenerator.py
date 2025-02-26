import hashlib

from .glacialTtsIdGeneratorInterface import GlacialTtsIdGeneratorInterface
from ...misc import utils as utils
from ...tts.models.ttsProvider import TtsProvider


class GlacialTtsIdGenerator(GlacialTtsIdGeneratorInterface):

    async def generateId(
        self,
        message: str,
        provider: TtsProvider
    ) -> str:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        string = f'{provider.name}:{message}'
        encodedString = string.encode('utf-8')
        return hashlib.sha256(encodedString).hexdigest()
