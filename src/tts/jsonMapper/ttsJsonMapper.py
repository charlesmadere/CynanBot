from typing import Any

from .ttsJsonMapperInterface import TtsJsonMapperInterface
from ..models.ttsProvider import TtsProvider
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TtsJsonMapper(TtsJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def asyncParseProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider | None:
        return self.parseProvider(ttsProvider)

    async def asyncRequireProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider:
        return self.requireProvider(ttsProvider)

    async def asyncSerializeProvider(
        self,
        ttsProvider: TtsProvider
    ) -> str:
        return self.serializeProvider(ttsProvider)

    def parseProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider | None:
        if not utils.isValidStr(ttsProvider):
            return None

        ttsProvider = ttsProvider.lower()

        match ttsProvider:
            case 'commodore_sam': return TtsProvider.COMMODORE_SAM
            case 'dec_talk': return TtsProvider.DEC_TALK
            case 'google': return TtsProvider.GOOGLE
            case 'half_life': return TtsProvider.HALF_LIFE
            case 'microsoft': return TtsProvider.MICROSOFT
            case 'microsoft_sam': return TtsProvider.MICROSOFT_SAM
            case 'singing_dec_talk': return TtsProvider.SINGING_DEC_TALK
            case 'stream_elements': return TtsProvider.STREAM_ELEMENTS
            case 'tts_monster': return TtsProvider.TTS_MONSTER
            case _:
                self.__timber.log('TtsJsonMapper', f'Encountered unknown TtsProvider value: \"{ttsProvider}\"')
                return None

    def requireProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider:
        result = self.parseProvider(ttsProvider)

        if result is None:
            raise ValueError(f'Unable to parse \"{ttsProvider}\" into TtsProvider value!')

        return result

    def serializeProvider(
        self,
        ttsProvider: TtsProvider
    ) -> str:
        if not isinstance(ttsProvider, TtsProvider):
            raise TypeError(f'ttsProvider argument is malformed: \"{ttsProvider}\"')

        match ttsProvider:
            case TtsProvider.COMMODORE_SAM: return 'commodore_sam'
            case TtsProvider.DEC_TALK: return 'dec_talk'
            case TtsProvider.GOOGLE: return 'google'
            case TtsProvider.HALF_LIFE: return 'half_life'
            case TtsProvider.MICROSOFT: return 'microsoft'
            case TtsProvider.MICROSOFT_SAM: return 'microsoft_sam'
            case TtsProvider.SINGING_DEC_TALK: return 'singing_dec_talk'
            case TtsProvider.STREAM_ELEMENTS: return 'stream_elements'
            case TtsProvider.TTS_MONSTER: return 'tts_monster'
            case _: raise ValueError(f'The given TtsProvider value is unknown: \"{ttsProvider}\"')
