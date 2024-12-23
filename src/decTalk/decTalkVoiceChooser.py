import random
import re
from typing import Pattern

from .decTalkVoiceChooserInterface import DecTalkVoiceChooserInterface
from .models.decTalkVoice import DecTalkVoice
from ..misc import utils as utils


class DecTalkVoiceChooser(DecTalkVoiceChooserInterface):

    def __init__(
        self,
        probabilityOfDefaultVoice: float = 0.8,
        voices: frozenset[DecTalkVoice] = frozenset({
            DecTalkVoice.DENNIS,
            DecTalkVoice.FRANK,
            DecTalkVoice.HARRY
        })
    ):
        if not utils.isValidNum(probabilityOfDefaultVoice):
            raise TypeError(f'probabilityOfDefaultVoice argument is malformed: \"{probabilityOfDefaultVoice}\"')
        if not isinstance(voices, frozenset):
            raise TypeError(f'voices argument is malformed: \"{voices}\"')

        self.__probabilityOfDefaultVoice: float = probabilityOfDefaultVoice
        self.__voices: frozenset[DecTalkVoice] = voices
        self.__voiceRegEx: Pattern = re.compile(r'\[:n\w]', re.IGNORECASE)

    async def choose(
        self,
        messageText: str | None
    ) -> str | None:
        if messageText is not None and not isinstance(messageText, str):
            raise TypeError(f'messageText argument is malformed: \"{messageText}\"')

        if len(self.__voices) == 0:
            return None
        elif not utils.isValidStr(messageText):
            return None
        elif random.random() <= self.__probabilityOfDefaultVoice:
            return None
        elif await self.__isVoicePatternAlreadyInMessage(messageText):
            return None

        randomVoice = random.choice(list(self.__voices))
        return f'{randomVoice.commandString} {messageText}'

    async def __isVoicePatternAlreadyInMessage(self, messageText: str) -> bool:
        return self.__voiceRegEx.search(messageText) is not None
