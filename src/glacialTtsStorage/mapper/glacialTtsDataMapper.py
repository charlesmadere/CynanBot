from .glacialTtsDataMapperInterface import GlacialTtsDataMapperInterface
from ...misc import utils as utils
from ...tts.ttsProvider import TtsProvider


class GlacialTtsDataMapper(GlacialTtsDataMapperInterface):

    async def fromDatabaseName(self, ttsProvider: str) -> TtsProvider:
        if not utils.isValidStr(ttsProvider):
            raise TypeError(f'ttsProvider argument is malformed: \"{ttsProvider}\"')

        ttsProvider = ttsProvider.lower()

        match ttsProvider:
            case 'dec_talk': return TtsProvider.DEC_TALK
            case 'google': return TtsProvider.GOOGLE
            case 'half_life': return TtsProvider.HALF_LIFE
            case 'microsoft_sam': return TtsProvider.MICROSOFT_SAM
            case 'singing_dec_talk': return TtsProvider.SINGING_DEC_TALK
            case 'stream_elements': return TtsProvider.STREAM_ELEMENTS
            case 'tts_monster': return TtsProvider.TTS_MONSTER
            case _: raise ValueError(f'Encountered unknown TtsProvider value: \"{ttsProvider}\"')

    async def toDatabaseName(self, ttsProvider: TtsProvider) -> str:
        match ttsProvider:
            case TtsProvider.DEC_TALK: return 'dec_talk'
            case TtsProvider.GOOGLE: return 'google'
            case TtsProvider.HALF_LIFE: return 'half_life'
            case TtsProvider.MICROSOFT_SAM: return 'microsoft_sam'
            case TtsProvider.SINGING_DEC_TALK: return 'singing_dec_talk'
            case TtsProvider.STREAM_ELEMENTS: return 'stream_elements'
            case TtsProvider.TTS_MONSTER: return 'tts_monster'
            case _: raise ValueError(f'Encountered unknown TtsProvider value: \"{ttsProvider}\"')
