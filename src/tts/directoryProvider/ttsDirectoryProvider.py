from .ttsDirectoryProviderInterface import TtsDirectoryProviderInterface
from ..models.ttsProvider import TtsProvider
from ...misc import utils as utils


class TtsDirectoryProvider(TtsDirectoryProviderInterface):

    def __init__(self, rootTtsDirectory: str = '../tts'):
        if not utils.isValidStr(rootTtsDirectory):
            raise TypeError(f'rootTtsDirectory argument is malformed: \"{rootTtsDirectory}\"')

        self.__rootTtsDirectory: str = rootTtsDirectory

    async def getFullTtsDirectoryFor(self, provider: TtsProvider) -> str:
        if not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        rootTtsDirectory = await self.getRootTtsDirectory()
        ttsDirectory = await self.getTtsDirectoryFor(provider)
        return f'{rootTtsDirectory}/{ttsDirectory}'

    async def getRootTtsDirectory(self) -> str:
        return self.__rootTtsDirectory

    async def getTtsDirectoryFor(self, provider: TtsProvider) -> str:
        if not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        match provider:
            case TtsProvider.COMMODORE_SAM: return 'commodore_sam'
            case TtsProvider.DEC_TALK: return 'dec_talk'
            case TtsProvider.GOOGLE: return 'google'
            case TtsProvider.HALF_LIFE: return 'half_life'
            case TtsProvider.MICROSOFT: return 'microsoft'
            case TtsProvider.MICROSOFT_SAM: return 'microsoft_sam'
            case TtsProvider.RANDO_TTS: return 'rando_tts'
            case TtsProvider.SHOTGUN_TTS: return 'shotgun_tts'
            case TtsProvider.SINGING_DEC_TALK: return 'singing_dec_talk'
            case TtsProvider.STREAM_ELEMENTS: return 'stream_elements'
            case TtsProvider.TTS_MONSTER: return 'tts_monster'
            case _: raise ValueError(f'encountered unknown TtsProvider value: \"{provider}\"')
