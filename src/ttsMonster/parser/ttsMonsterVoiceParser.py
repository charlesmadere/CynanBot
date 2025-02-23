from typing import Any

from .ttsMonsterVoiceParserInterface import TtsMonsterVoiceParserInterface
from ..models.ttsMonsterVoice import TtsMonsterVoice
from ...misc import utils as utils


class TtsMonsterVoiceParser(TtsMonsterVoiceParserInterface):

    def parseVoice(self, jsonString: str | Any | None) -> TtsMonsterVoice | None:
        if not utils.isValidStr(jsonString):
            return None

        for currentVoice in TtsMonsterVoice:
            if currentVoice.inMessageName == jsonString:
                return currentVoice

        return None

    def requireVoice(self, jsonString: str | Any | None) -> TtsMonsterVoice:
        result = self.parseVoice(jsonString)

        if result is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into TtsMonsterVoice value!')

        return result

    def serializeVoice(self, voice: TtsMonsterVoice):
        return voice.inMessageName
