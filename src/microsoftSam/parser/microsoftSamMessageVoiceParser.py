import re
from typing import Final, Pattern

from .microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from .microsoftSamMessageVoiceParserInterface import MicrosoftSamMessageVoiceParserInterface
from ...misc import utils as utils


class MicrosoftSamMessageVoiceParser(MicrosoftSamMessageVoiceParserInterface):

    def __init__(
        self,
        microsoftSamJsonParser: MicrosoftSamJsonParserInterface,
    ):
        if not isinstance(microsoftSamJsonParser, MicrosoftSamJsonParserInterface):
            raise TypeError(f'microsoftSamJsonParser argument is malformed: \"{microsoftSamJsonParser}\"')

        self.__microsoftSamJsonParser: Final[MicrosoftSamJsonParserInterface] = microsoftSamJsonParser

        self.__voiceRegEx: Final[Pattern] = re.compile(r'^(\s*(\w+):\s+)', re.IGNORECASE)

    async def determineVoiceFromMessage(
        self,
        message: str | None,
    ) -> MicrosoftSamMessageVoiceParserInterface.Result | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        if not utils.isValidStr(message):
            return None

        voiceMatch = self.__voiceRegEx.match(message)
        if voiceMatch is None:
            return None

        voiceString = voiceMatch.group(2)
        if not utils.isValidStr(voiceString):
            return None

        microsoftSamVoice = await self.__microsoftSamJsonParser.parseVoice(voiceString)
        if microsoftSamVoice is None:
            return None

        fullVoiceString = voiceMatch.group(1)
        messageWithoutVoice = message[len(fullVoiceString):].strip()

        return MicrosoftSamMessageVoiceParserInterface.Result(
            voice = microsoftSamVoice,
            message = messageWithoutVoice,
        )
