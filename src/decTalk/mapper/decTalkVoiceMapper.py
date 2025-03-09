import re
from typing import Any, Collection, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from ..models.decTalkVoice import DecTalkVoice
from ...misc import utils as utils


class DecTalkVoiceMapper(DecTalkVoiceMapperInterface):

    def __init__(self):
        self.__voiceRegExes: frozendict[DecTalkVoice, Collection[Pattern]] = self.__buildVoiceRegExes()

    def __buildVoiceRegExes(self) -> frozendict[DecTalkVoice, Collection[Pattern]]:
        betty: FrozenList[Pattern] = FrozenList()
        betty.append(re.compile(r'^\s*\[?:?nb\]?\s*$', re.IGNORECASE))
        betty.append(re.compile(r'^\s*betty\s*$', re.IGNORECASE))
        betty.freeze()

        dennis: FrozenList[Pattern] = FrozenList()
        dennis.append(re.compile(r'^\s*\[?:?nd\]?\s*$', re.IGNORECASE))
        dennis.append(re.compile(r'^\s*dennis\s*$', re.IGNORECASE))
        dennis.freeze()

        frank: FrozenList[Pattern] = FrozenList()
        frank.append(re.compile(r'^\s*\[?:?nf\]?\s*$', re.IGNORECASE))
        frank.append(re.compile(r'^\s*frank\s*$', re.IGNORECASE))
        frank.freeze()

        harry: FrozenList[Pattern] = FrozenList()
        harry.append(re.compile(r'^\s*\[?:?nh\]?\s*$', re.IGNORECASE))
        harry.append(re.compile(r'^\s*harry\s*$', re.IGNORECASE))
        harry.freeze()

        kit: FrozenList[Pattern] = FrozenList()
        kit.append(re.compile(r'^\s*\[?:?nk\]?\s*$', re.IGNORECASE))
        kit.append(re.compile(r'^\s*kit\s*$', re.IGNORECASE))
        kit.freeze()

        paul: FrozenList[Pattern] = FrozenList()
        paul.append(re.compile(r'^\s*\[?:?np\]?\s*$', re.IGNORECASE))
        paul.append(re.compile(r'^\s*paul\s*$', re.IGNORECASE))
        paul.freeze()

        rita: FrozenList[Pattern] = FrozenList()
        rita.append(re.compile(r'^\s*\[?:?nr\]?\s*$', re.IGNORECASE))
        rita.append(re.compile(r'^\s*rita\s*$', re.IGNORECASE))
        rita.freeze()

        ursula: FrozenList[Pattern] = FrozenList()
        ursula.append(re.compile(r'^\s*\[?:?nu\]?\s*$', re.IGNORECASE))
        ursula.append(re.compile(r'^\s*ursula\s*$', re.IGNORECASE))
        ursula.freeze()

        wendy: FrozenList[Pattern] = FrozenList()
        wendy.append(re.compile(r'^\s*\[?:?nw\]?\s*$', re.IGNORECASE))
        wendy.append(re.compile(r'^\s*wendy\s*$', re.IGNORECASE))
        wendy.freeze()

        return frozendict({
            DecTalkVoice.BETTY: betty,
            DecTalkVoice.DENNIS: dennis,
            DecTalkVoice.FRANK: frank,
            DecTalkVoice.HARRY: harry,
            DecTalkVoice.KIT: kit,
            DecTalkVoice.PAUL: paul,
            DecTalkVoice.RITA: rita,
            DecTalkVoice.URSULA: ursula,
            DecTalkVoice.WENDY: wendy
        })

    async def parseVoice(
        self,
        string: str | Any | None
    ) -> DecTalkVoice | None:
        if not utils.isValidStr(string):
            return None

        for decTalkVoice, voiceRegExes in self.__voiceRegExes.items():
            for voiceRegEx in voiceRegExes:
                if voiceRegEx.fullmatch(string) is not None:
                    return decTalkVoice

        return None

    async def requireVoice(
        self,
        voice: str | Any | None
    ) -> DecTalkVoice:
        result = await self.parseVoice(voice)

        if result is None:
            raise ValueError(f'Unable to parse DecTalkVoice from string: \"{voice}\"')

        return result

    async def serializeVoice(
        self,
        voice: DecTalkVoice
    ) -> str:
        if not isinstance(voice, DecTalkVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        match voice:
            case DecTalkVoice.BETTY: return 'betty'
            case DecTalkVoice.DENNIS: return 'dennis'
            case DecTalkVoice.FRANK: return 'frank'
            case DecTalkVoice.HARRY: return 'harry'
            case DecTalkVoice.KIT: return 'kit'
            case DecTalkVoice.PAUL: return 'paul'
            case DecTalkVoice.RITA: return 'rita'
            case DecTalkVoice.URSULA: return 'ursula'
            case DecTalkVoice.WENDY: return 'wendy'
            case _: raise RuntimeError(f'voice is an unknown DecTalkVoice value: \"{voice}\"')
