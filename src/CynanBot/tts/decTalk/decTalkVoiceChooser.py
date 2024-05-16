import random
import re
from typing import Pattern

import CynanBot.misc.utils as utils
from CynanBot.tts.decTalk.decTalkVoice import DecTalkVoice
from CynanBot.tts.decTalk.decTalkVoiceChooserInterface import \
    DecTalkVoiceChooserInterface
from CynanBot.tts.decTalk.decTalkVoiceMapperInterface import \
    DecTalkVoiceMapperInterface


class DecTalkVoiceChooser(DecTalkVoiceChooserInterface):

    def __init__(
        self,
        decTalkVoiceMapper: DecTalkVoiceMapperInterface,
        oddsOfDefaultVoice: float = 0.8,
        voices: set[DecTalkVoice] = {
            DecTalkVoice.BETTY,
            DecTalkVoice.DENNIS,
            DecTalkVoice.FRANK,
            DecTalkVoice.HARRY,
            DecTalkVoice.RITA,
            DecTalkVoice.URSULA,
            DecTalkVoice.WENDY
        }
    ):
        if not isinstance(decTalkVoiceMapper, DecTalkVoiceMapperInterface):
            raise TypeError(f'decTalkVoiceMapper argument is malformed: \"{decTalkVoiceMapper}\"')
        if not utils.isValidNum(oddsOfDefaultVoice):
            raise TypeError(f'oddsOfDefaultVoice argument is malformed: \"{oddsOfDefaultVoice}\"')
        if not isinstance(voices, set):
            raise TypeError(f'voices argument is malformed: \"{voices}\"')
        elif len(voices) == 0:
            raise ValueError(f'voices argument is empty: \"{voices}\"')

        self.__decTalkVoiceMapper: DecTalkVoiceMapperInterface = decTalkVoiceMapper
        self.__oddsOfDefaultVoice: float = oddsOfDefaultVoice
        self.__voices: set[DecTalkVoice] = voices
        self.__voiceRegEx: Pattern = re.compile(r'\[:n\w\]', re.IGNORECASE)

    async def choose(
        self,
        messageText: str | None
    ) -> str | None:
        if messageText is not None and not isinstance(messageText, str):
            raise TypeError(f'messageText argument is malformed: \"{messageText}\"')

        if not utils.isValidStr(messageText):
            return None
        elif random.random() <= self.__oddsOfDefaultVoice:
            return None
        elif await self.__isVoicePatternAlreadyInMessage(messageText):
            return None

        randomVoice = random.choice(list(self.__voices))
        randomVoiceString = await self.__decTalkVoiceMapper.toString(randomVoice)
        return f'{randomVoiceString} {messageText}'

    async def __isVoicePatternAlreadyInMessage(self, messageText: str) -> bool:
        return self.__voiceRegEx.search(messageText) is not None
