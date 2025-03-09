import re
from typing import Pattern

from .halfLifeMessageVoiceParserInterface import HalfLifeMessageVoiceParserInterface
from .halfLifeVoiceParserInterface import HalfLifeVoiceParserInterface
from ...misc import utils as utils


class HalfLifeMessageVoiceParser(HalfLifeMessageVoiceParserInterface):

    def __init__(
        self,
        halfLifeVoiceParser: HalfLifeVoiceParserInterface
    ):
        if not isinstance(halfLifeVoiceParser, HalfLifeVoiceParserInterface):
            raise TypeError(f'halfLifeJsonParser argument is malformed: \"{HalfLifeVoiceParserInterface}\"')

        self.__halfLifeVoiceParser: HalfLifeVoiceParserInterface = halfLifeVoiceParser

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

        halfLifeVoice = self.__halfLifeVoiceParser.parseVoice(voiceString)
        if halfLifeVoice is None:
            return None

        fullVoiceString = voiceMatch.group(1)
        messageWithoutVoice = message[len(fullVoiceString):].strip()

        return HalfLifeMessageVoiceParserInterface.Result(
            message = messageWithoutVoice,
            voice = halfLifeVoice
        )
