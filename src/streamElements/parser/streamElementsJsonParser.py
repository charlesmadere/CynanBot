import re
from typing import Any, Collection, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from ..models.streamElementsVoice import StreamElementsVoice
from ...misc import utils as utils


class StreamElementsJsonParser(StreamElementsJsonParserInterface):

    def __init__(self):
        self.__voiceRegExes: frozendict[StreamElementsVoice, Collection[Pattern]] = self.__buildVoiceRegExes()

    def __buildVoiceRegExes(self) -> frozendict[StreamElementsVoice, Collection[Pattern]]:
        amy: FrozenList[Pattern] = FrozenList()
        amy.append(re.compile(r'^\s*amy\s*$', re.IGNORECASE))
        amy.freeze()

        brian: FrozenList[Pattern] = FrozenList()
        brian.append(re.compile(r'^\s*brian\s*$', re.IGNORECASE))
        brian.freeze()

        emma: FrozenList[Pattern] = FrozenList()
        emma.append(re.compile(r'^\s*emma\s*$', re.IGNORECASE))
        emma.append(re.compile(r'^\s*ema\s*$', re.IGNORECASE))
        emma.freeze()

        joey: FrozenList[Pattern] = FrozenList()
        joey.append(re.compile(r'^\s*joey\s*$', re.IGNORECASE))
        joey.append(re.compile(r'^\s*joe\s*$', re.IGNORECASE))
        joey.freeze()

        return frozendict({
            StreamElementsVoice.AMY: amy,
            StreamElementsVoice.BRIAN: brian,
            StreamElementsVoice.EMMA: emma,
            StreamElementsVoice.JOEY: joey
        })

    async def parseVoice(
        self,
        string: str | Any | None
    ) -> StreamElementsVoice | None:
        if not utils.isValidStr(string):
            return None

        for streamElementsVoice, voiceRegExes in self.__voiceRegExes.items():
            for voiceRegEx in voiceRegExes:
                if voiceRegEx.fullmatch(string) is not None:
                    return streamElementsVoice

        return None

    async def requireVoice(
        self,
        string: str | Any | None
    ) -> StreamElementsVoice:
        result = await self.parseVoice(string)

        if result is None:
            raise ValueError(f'Unable to parse StreamElementsVoice from string: \"{string}\"')

        return result

    async def serializeVoice(
        self,
        voice: StreamElementsVoice
    ) -> str:
        if not isinstance(voice, StreamElementsVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        match voice:
            case StreamElementsVoice.AMY: return 'amy'
            case StreamElementsVoice.BRIAN: return 'brian'
            case StreamElementsVoice.EMMA: return 'emma'
            case StreamElementsVoice.JOEY: return 'joey'
            case _: raise ValueError(f'Encountered unexpected StreamElementsVoice value: \"{voice}\"')
