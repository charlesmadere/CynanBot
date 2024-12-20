from typing import Any

from src.misc import utils
from .models.microsoftSamVoice import MicrosoftSamVoice
from .microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface


class MicrosoftSamJsonParser(MicrosoftSamJsonParserInterface):

    def parseVoice(self, jsonString: str | Any | None) -> MicrosoftSamVoice | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonString = jsonString.lower()

        for currentVoice in MicrosoftSamVoice:
            if currentVoice.value == jsonString.casefold():
                return currentVoice

        return None

    def requireVoice(self, jsonString: str | Any | None) -> MicrosoftSamVoice:
        result = self.parseVoice(jsonString)

        if result is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into MicrosoftSamVoice value!')

        return result

    def serializeVoice(self, voice: MicrosoftSamVoice):
        return voice.value.casefold()
