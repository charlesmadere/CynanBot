from typing import Any

from .halfLifeVoiceParserInterface import HalfLifeVoiceParserInterface
from ..models.halfLifeVoice import HalfLifeVoice
from ...misc import utils as utils


class HalfLifeVoiceParser(HalfLifeVoiceParserInterface):

    def parseVoice(self, voiceString: str | Any | None) -> HalfLifeVoice | None:
        if not utils.isValidStr(voiceString):
            return None

        voiceString = voiceString.casefold()

        for currentVoice in HalfLifeVoice:
            if currentVoice.keyName.casefold() == voiceString:
                return currentVoice

        return None

    def requireVoice(self, voiceString: str | Any | None) -> HalfLifeVoice:
        result = self.parseVoice(voiceString)

        if result is None:
            raise ValueError(f'Unable to parse \"{voiceString}\" into HalfLifeVoice value!')

        return result

    def serializeVoice(self, voice: HalfLifeVoice) -> str:
        if not isinstance(voice, HalfLifeVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        return voice.keyName
