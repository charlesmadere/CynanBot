import re
from typing import Pattern

from src.halfLife.parser.halfLifeJsonParserInterface import HalfLifeJsonParserInterface

from .halfLifeMessageVoiceParserInterface import HalfLifeMessageVoiceParserInterface
from ..models.halfLifeVoice import HalfLifeVoice
from ...misc import utils as utils


class HalfLifeMessageVoiceParser(HalfLifeMessageVoiceParserInterface):

    def __init__(
        self, 
        halfLifeJsonParser: HalfLifeJsonParserInterface):

        if not isinstance(halfLifeJsonParser, HalfLifeJsonParserInterface):
            raise TypeError(f'halfLifeJsonParser argument is malformed: \"{HalfLifeJsonParserInterface}\"')

        self.__halfLifeJsonParser: HalfLifeJsonParserInterface = halfLifeJsonParser
        self.__voiceRegEx: Pattern = re.compile(r'(^\s*(\w+):\s+)', re.IGNORECASE)

    async def determineVoiceFromMessage(
        self,
        message: str | None
    ) -> HalfLifeMessageVoiceParserInterface.Result | None:
        if not utils.isValidStr(message):
            return None

        voiceMatch = self.__voiceRegEx.match(message)
        if voiceMatch is None:
            return None

        voiceString = voiceMatch.group(2)
        if not utils.isValidStr(voiceString):
            return None

        halfLifeVoice: HalfLifeVoice | None = None

        halfLifeVoice = self.__halfLifeJsonParser.parseVoice(voiceString)
        
        if halfLifeVoice is None:
            return None

        fullVoiceString = voiceMatch.group(1)
        messageWithoutVoice = message[len(fullVoiceString):].strip()

        return HalfLifeMessageVoiceParserInterface.Result(
            message = messageWithoutVoice,
            voice = halfLifeVoice
        )
