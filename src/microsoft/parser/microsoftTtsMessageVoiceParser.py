import re
from typing import Pattern

from .microsoftTtsJsonParserInterface import MicrosoftTtsJsonParserInterface
from .microsoftTtsMessageVoiceParserInterface import MicrosoftTtsMessageVoiceParserInterface
from ...misc import utils as utils


class MicrosoftTtsMessageVoiceParser(MicrosoftTtsMessageVoiceParserInterface):

    def __init__(
        self,
        microsoftTtsJsonParser: MicrosoftTtsJsonParserInterface,
    ):
        if not isinstance(microsoftTtsJsonParser, MicrosoftTtsJsonParserInterface):
            raise TypeError(f'microsoftTtsJsonParser argument is malformed: \"{microsoftTtsJsonParser}\"')

        self.__microsoftTtsJsonParser: MicrosoftTtsJsonParserInterface = microsoftTtsJsonParser

        self.__voiceRegEx: Pattern = re.compile(r'(^\s*(\w+):\s+)', re.IGNORECASE)

    async def determineVoiceFromMessage(
        self,
        message: str | None,
    ) -> MicrosoftTtsMessageVoiceParserInterface.Result | None:
        if not utils.isValidStr(message):
            return None

        voiceMatch = self.__voiceRegEx.match(message)
        if voiceMatch is None:
            return None

        voiceString = voiceMatch.group(2)
        if not utils.isValidStr(voiceString):
            return None

        microsoftTtsVoice = await self.__microsoftTtsJsonParser.parseVoice(voiceString)
        if microsoftTtsVoice is None:
            return None

        fullVoiceString = voiceMatch.group(1)
        messageWithoutVoice = message[len(fullVoiceString):].strip()

        return MicrosoftTtsMessageVoiceParserInterface.Result(
            voice = microsoftTtsVoice,
            message = messageWithoutVoice,
        )
