from typing import Any

from .microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from ..models.microsoftSamVoice import MicrosoftSamVoice
from ...misc import utils as utils


class MicrosoftSamJsonParser(MicrosoftSamJsonParserInterface):

    async def parseVoice(self, jsonString: str | Any | None) -> MicrosoftSamVoice | None:
        if not utils.isValidStr(jsonString):
            return None

        for currentVoice in MicrosoftSamVoice:
            if currentVoice.jsonValue == jsonString:
                return currentVoice

        return None

    async def requireVoice(self, jsonString: str | Any | None) -> MicrosoftSamVoice:
        result = await self.parseVoice(jsonString)

        if result is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into MicrosoftSamVoice value!')

        return result

    async def serializeVoice(self, voice: MicrosoftSamVoice) -> str:
        if not isinstance(voice, MicrosoftSamVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        return voice.jsonValue
