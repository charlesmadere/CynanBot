from typing import Any

from .microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from ..models.microsoftSamVoice import MicrosoftSamVoice
from ...misc import utils as utils


class MicrosoftSamJsonParser(MicrosoftSamJsonParserInterface):

    def parseVoice(self, jsonString: str | Any | None) -> MicrosoftSamVoice | None:
        if not utils.isValidStr(jsonString):
            return None

        for currentVoice in MicrosoftSamVoice:
            if currentVoice.jsonValue == jsonString:
                return currentVoice

        return None

    def requireVoice(self, jsonString: str | Any | None) -> MicrosoftSamVoice:
        result = self.parseVoice(jsonString)

        if result is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into MicrosoftSamVoice value!')

        return result

    def serializeVoice(self, voice: MicrosoftSamVoice):
        return voice.jsonValue
