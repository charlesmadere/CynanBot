import re
from typing import Pattern

from frozendict import frozendict

from .streamElementsMessageVoiceParserInterface import StreamElementsMessageVoiceParserInterface
from ..models.streamElementsVoice import StreamElementsVoice
from ...misc import utils as utils


class StreamElementsMessageVoiceParser(StreamElementsMessageVoiceParserInterface):

    def __init__(self):
        self.__voiceRegEx: Pattern = re.compile(r'(^\s*(\w+):\s+)', re.IGNORECASE)

    async def __buildVoiceNamesToVoiceDictionary(self) -> frozendict[str, StreamElementsVoice]:
        voiceNamesToVoiceDictionary: dict[str, StreamElementsVoice] = dict()

        for voice in StreamElementsVoice:
            voiceNamesToVoiceDictionary[voice.humanName] = voice

        return frozendict(voiceNamesToVoiceDictionary)

    async def determineVoiceFromMessage(
        self,
        message: str | None
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

        streamElementsVoice: StreamElementsVoice | None = None

        for currentVoice in StreamElementsVoice:
            if currentVoice.humanName.casefold() == voiceString.casefold():
                streamElementsVoice = currentVoice
                break

        if streamElementsVoice is None:
            return None

        fullVoiceString = voiceMatch.group(1)
        messageWithoutVoice = message[len(fullVoiceString):].strip()

        return StreamElementsMessageVoiceParserInterface.Result(
            message = messageWithoutVoice,
            voice = streamElementsVoice
        )
