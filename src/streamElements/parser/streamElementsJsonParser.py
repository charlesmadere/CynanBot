from typing import Any

from .streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from ..models.streamElementsVoice import StreamElementsVoice
from ...misc import utils as utils


class StreamElementsJsonParser(StreamElementsJsonParserInterface):

    async def parseVoice(self, jsonString: str | Any | None) -> StreamElementsVoice | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonString = jsonString.lower()

        match jsonString:
            case 'amy': return StreamElementsVoice.AMY
            case 'brian': return StreamElementsVoice.BRIAN
            case 'joey': return StreamElementsVoice.JOEY
            case _: return None

    async def requireVoice(self, jsonString: str | Any | None) -> StreamElementsVoice:
        result = await self.parseVoice(jsonString)

        if result is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into StreamElementsVoice value!')

        return result

    async def serializeVoice(self, voice: StreamElementsVoice) -> str:
        if not isinstance(voice, StreamElementsVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        match voice:
            case StreamElementsVoice.AMY: return 'amy'
            case StreamElementsVoice.BRIAN: return 'brian'
            case StreamElementsVoice.JOEY: return 'joey'
            case _: raise ValueError(f'Encountered unexpected StreamElementsVoice value: \"{voice}\"')
