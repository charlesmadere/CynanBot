import re
from typing import Pattern

from src.microsoftSam.parser.microsoftSamMessageVoiceParserInterface import MicrosoftSamMessageVoiceParserInterface
from ..models.microsoftSamVoice import MicrosoftSamVoice
from ...misc import utils as utils


class MicrosoftSamMessageVoiceParser(MicrosoftSamMessageVoiceParserInterface):

    def __init__(self):
        self.__voiceRegEx: Pattern = re.compile(r'(^\s*(\w+):\s+)', re.IGNORECASE)

    async def determineVoiceFromMessage(
        self,
        message: str | None
    ) -> MicrosoftSamMessageVoiceParserInterface.Result | None:
        if not utils.isValidStr(message):
            return None

        voiceMatch = self.__voiceRegEx.match(message)
        if voiceMatch is None:
            return None

        voiceString = voiceMatch.group(2)
        if not utils.isValidStr(voiceString):
            return None

        microsoftSamVoice: MicrosoftSamVoice | None = None

        for currentVoice in MicrosoftSamVoice:
            if currentVoice.value.casefold() == voiceString.casefold():
                microsoftSamVoice = currentVoice
                break

        if microsoftSamVoice is None:
            return None

        fullVoiceString = voiceMatch.group(1)
        messageWithoutVoice = message[len(fullVoiceString):].strip()

        return MicrosoftSamMessageVoiceParserInterface.Result(
            message = messageWithoutVoice,
            voice = microsoftSamVoice
        )
