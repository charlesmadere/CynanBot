from .glacialTtsDataMapperInterface import GlacialTtsDataMapperInterface
from ...misc import utils as utils
from ...tts.models.ttsProvider import TtsProvider


class GlacialTtsDataMapper(GlacialTtsDataMapperInterface):

    async def fromDatabaseName(self, ttsProvider: str) -> TtsProvider:
        if not utils.isValidStr(ttsProvider):
            raise TypeError(f'ttsProvider argument is malformed: \"{ttsProvider}\"')

        ttsProvider = ttsProvider.lower()

        match ttsProvider:
            case 'commodore_sam': return TtsProvider.COMMODORE_SAM
            case 'dec_talk': return TtsProvider.DEC_TALK
            case 'google': return TtsProvider.GOOGLE
            case 'half_life': return TtsProvider.HALF_LIFE
            case 'microsoft': return TtsProvider.MICROSOFT
            case 'microsoft_sam': return TtsProvider.MICROSOFT_SAM
            case 'rando_tts': return TtsProvider.RANDO_TTS
            case 'shotgun_tts': return TtsProvider.SHOTGUN_TTS
            case 'singing_dec_talk': return TtsProvider.UNRESTRICTED_DEC_TALK
            case 'stream_elements': return TtsProvider.STREAM_ELEMENTS
            case 'tts_monster': return TtsProvider.TTS_MONSTER
            case 'unrestricted_dec_talk': return TtsProvider.UNRESTRICTED_DEC_TALK
            case _: raise ValueError(f'Encountered unknown TtsProvider value: \"{ttsProvider}\"')

    async def toDatabaseName(self, ttsProvider: TtsProvider) -> str:
        if not isinstance(ttsProvider, TtsProvider):
            raise TypeError(f'ttsProvider argument is malformed: \"{ttsProvider}\"')

        match ttsProvider:
            case TtsProvider.COMMODORE_SAM: return 'commodore_sam'
            case TtsProvider.DEC_TALK: return 'dec_talk'
            case TtsProvider.GOOGLE: return 'google'
            case TtsProvider.HALF_LIFE: return 'half_life'
            case TtsProvider.MICROSOFT: return 'microsoft'
            case TtsProvider.MICROSOFT_SAM: return 'microsoft_sam'
            case TtsProvider.RANDO_TTS: return 'rando_tts'
            case TtsProvider.SHOTGUN_TTS: return 'shotgun_tts'
            case TtsProvider.STREAM_ELEMENTS: return 'stream_elements'
            case TtsProvider.TTS_MONSTER: return 'tts_monster'
            case TtsProvider.UNRESTRICTED_DEC_TALK: return 'unrestricted_dec_talk'
            case _: raise ValueError(f'Encountered unknown TtsProvider value: \"{ttsProvider}\"')

    async def toFolderName(self, ttsProvider: TtsProvider) -> str:
        if not isinstance(ttsProvider, TtsProvider):
            raise TypeError(f'ttsProvider argument is malformed: \"{ttsProvider}\"')

        match ttsProvider:
            case TtsProvider.COMMODORE_SAM: return 'commodore_sam'
            case TtsProvider.DEC_TALK: return 'dec_talk'
            case TtsProvider.GOOGLE: return 'google'
            case TtsProvider.HALF_LIFE: return 'half_life'
            case TtsProvider.MICROSOFT: return 'microsoft'
            case TtsProvider.MICROSOFT_SAM: return 'microsoft_sam'
            case TtsProvider.RANDO_TTS: return 'rando_tts'
            case TtsProvider.SHOTGUN_TTS: return 'shotgun_tts'
            case TtsProvider.STREAM_ELEMENTS: return 'stream_elements'
            case TtsProvider.TTS_MONSTER: return 'tts_monster'
            case TtsProvider.UNRESTRICTED_DEC_TALK: return 'unrestricted_dec_talk'
            case _: raise ValueError(f'encountered unknown TtsProvider value: \"{ttsProvider}\"')
