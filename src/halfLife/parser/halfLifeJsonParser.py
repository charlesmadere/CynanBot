from typing import Any

from .halfLifeJsonParserInterface import HalfLifeJsonParserInterface
from ..models.halfLifeVoice import HalfLifeVoice
from ...misc import utils as utils


class HalfLifeJsonParser(HalfLifeJsonParserInterface):

    def parseVoice(self, jsonString: str | Any | None) -> HalfLifeVoice | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonString = jsonString.lower()

        for currentVoice in HalfLifeVoice:
            if currentVoice.value.casefold() == jsonString.casefold():
                return currentVoice

        return None

    def requireVoice(self, jsonString: str | Any | None) -> HalfLifeVoice:
        result = self.parseVoice(jsonString)

        if result is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into HalfLifeVoice value!')

        return result

    def serializeVoice(self, voice: HalfLifeVoice) -> str:
        if not isinstance(voice, HalfLifeVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        return voice.value
