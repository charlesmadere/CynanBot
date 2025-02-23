from typing import Any

from .ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from ..models.ttsMonsterPrivateApiTtsData import TtsMonsterPrivateApiTtsData
from ..models.ttsMonsterPrivateApiTtsResponse import TtsMonsterPrivateApiTtsResponse
from ..models.ttsMonsterVoice import TtsMonsterVoice
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TtsMonsterPrivateApiJsonMapper(TtsMonsterPrivateApiJsonMapperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        provider: str = 'provider'
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        if not utils.isValidStr(provider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__timber: TimberInterface = timber
        self.__provider: str = provider

    async def parseTtsData(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterPrivateApiTtsData | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        link: str | None = None
        if 'link' in jsonContents and utils.isValidStr(jsonContents.get('link')):
            link = utils.getStrFromDict(jsonContents, 'link')

        if not utils.isValidUrl(link):
            self.__timber.log('TtsMonsterPrivateApiJsonMapper', f'\"link\" value in JSON response is missing/malformed ({link=}) ({jsonContents=})')
            return None

        warning: str | None = None
        if 'warning' in jsonContents and utils.isValidStr(jsonContents.get('warning')):
            warning = utils.getStrFromDict(jsonContents, 'warning')

        return TtsMonsterPrivateApiTtsData(
            link = link,
            warning = warning
        )

    async def parseTtsResponse(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterPrivateApiTtsResponse | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        status = utils.getIntFromDict(jsonContents, 'status')
        data = await self.parseTtsData(jsonContents.get('data'))

        if data is None:
            return None

        return TtsMonsterPrivateApiTtsResponse(
            status = status,
            data = data
        )

    async def parseVoice(
        self,
        string: str | Any | None
    ) -> TtsMonsterVoice:
        if not utils.isValidStr(string):
            raise TypeError(f'string argument is malformed: \"{string}\"')

        string = string.lower()

        match string:
            case 'brian': return TtsMonsterVoice.BRIAN
            case 'jazz': return TtsMonsterVoice.JAZZ
            case 'kkona': return TtsMonsterVoice.KKONA
            case 'pirate': return TtsMonsterVoice.PIRATE
            case 'shadow': return TtsMonsterVoice.SHADOW
            case 'witch': return TtsMonsterVoice.WITCH
            case 'zero_two': return TtsMonsterVoice.ZERO_TWO
            case _: raise ValueError(f'Encountered unknown TtsMonsterVoice string value: \"{string}\"')

    async def serializeGenerateTtsJsonBody(
        self,
        key: str,
        message: str,
        userId: str
    ) -> dict[str, Any]:
        if not utils.isValidStr(key):
            raise TypeError(f'key argument is malformed: \"{key}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        return {
            'data': {
                'ai': True,
                'details': {
                    'provider': self.__provider
                },
                'key': key,
                'message': message,
                'userId': userId
            }
        }

    async def serializeVoice(
        self,
        voice: TtsMonsterVoice
    ) -> str:
        if not isinstance(voice, TtsMonsterVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        match voice:
            case TtsMonsterVoice.BRIAN: return 'brian'
            case TtsMonsterVoice.JAZZ: return 'jazz'
            case TtsMonsterVoice.KKONA: return 'kkona'
            case TtsMonsterVoice.PIRATE: return 'pirate'
            case TtsMonsterVoice.SHADOW: return 'shadow'
            case TtsMonsterVoice.WITCH: return 'witch'
            case TtsMonsterVoice.ZERO_TWO: return 'zero_two'
            case _: raise ValueError(f'Encountered unknown TtsMonsterVoice value: \"{voice}\"')
