import re
from typing import Pattern

from .streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from .streamElementsMessageVoiceParserInterface import StreamElementsMessageVoiceParserInterface
from ...misc import utils as utils


class StreamElementsMessageVoiceParser(StreamElementsMessageVoiceParserInterface):

    def __init__(
        self,
        streamElementsJsonParser: StreamElementsJsonParserInterface,
    ):
        if not isinstance(streamElementsJsonParser, StreamElementsJsonParserInterface):
            raise TypeError(f'streamElementsJsonParser argument is malformed: \"{streamElementsJsonParser}\"')

        self.__streamElementsJsonParser: StreamElementsJsonParserInterface = streamElementsJsonParser

        self.__voiceRegEx: Pattern = re.compile(r'^(\s*(\w+):\s+)', re.IGNORECASE)

    async def determineVoiceFromMessage(
        self,
        message: str | None,
    ) -> StreamElementsMessageVoiceParserInterface.Result | None:
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

        streamElementsVoice = await self.__streamElementsJsonParser.parseVoice(voiceString)
        if streamElementsVoice is None:
            return None

        fullVoiceString = voiceMatch.group(1)
        messageWithoutVoice = message[len(fullVoiceString):].strip()

        return StreamElementsMessageVoiceParserInterface.Result(
            message = messageWithoutVoice,
            voice = streamElementsVoice,
        )
