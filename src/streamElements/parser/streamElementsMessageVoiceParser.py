import re
from typing import Pattern

from .streamElementsMessageVoiceParserInterface import StreamElementsMessageVoiceParserInterface
from ..models.streamElementsVoice import StreamElementsVoice
from ...misc import utils as utils


class StreamElementsMessageVoiceParser(StreamElementsMessageVoiceParserInterface):

    def __init__(self):
        self.__voiceRegEx: Pattern = re.compile(r'^\s*(\w+):\s+', re.IGNORECASE)

    async def determineVoiceFromMessage(self, message: str) -> StreamElementsVoice | None:
        if not utils.isValidStr(message):
            return None

        voiceMatch = self.__voiceRegEx.match(message)
        if voiceMatch is None:
            return None

        voice = voiceMatch.group(1)
        if not utils.isValidStr(voice):
            return None

        for streamElementsVoice in StreamElementsVoice:
            if streamElementsVoice.humanName.casefold() == voice.casefold():
                return streamElementsVoice

        return None
