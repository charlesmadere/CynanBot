from typing import Any

from .ttsJsonMapperInterface import TtsJsonMapperInterface
from .ttsProvider import TtsProvider
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class TtsJsonMapper(TtsJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def parseProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider | None:
        if not utils.isValidStr(ttsProvider):
            return None

        ttsProvider = ttsProvider.lower()

        match ttsProvider:
            case 'dec_talk': return TtsProvider.DEC_TALK
            case 'google': return TtsProvider.GOOGLE
            case 'tts_monster': return TtsProvider.TTS_MONSTER
            case _:
                self.__timber.log('TtsJsonMapper', f'Encountered unknown TtsProvider value: \"{ttsProvider}\"')
                return None

    async def requireProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider:
        result = await self.parseProvider(ttsProvider)

        if result is None:
            raise ValueError(f'Unable to parse \"{ttsProvider}\" into TtsProvider value!')

        return result

    async def serializeProvider(
        self,
        ttsProvider: TtsProvider
    ) -> str:
        if not isinstance(ttsProvider, TtsProvider):
            raise TypeError(f'ttsProvider argument is malformed: \"{ttsProvider}\"')

        match ttsProvider:
            case TtsProvider.DEC_TALK: return 'dec_talk'
            case TtsProvider.GOOGLE: return 'google'
            case TtsProvider.TTS_MONSTER: return 'tts_monster'
            case _:
                raise ValueError(f'The given TtsProvider value is unknown: \"{ttsProvider}\"')
