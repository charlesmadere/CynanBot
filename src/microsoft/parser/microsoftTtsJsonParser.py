import re
from typing import Any, Collection, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .microsoftTtsJsonParserInterface import MicrosoftTtsJsonParserInterface
from ..models.microsoftTtsVoice import MicrosoftTtsVoice
from ...misc import utils as utils


class MicrosoftTtsJsonParser(MicrosoftTtsJsonParserInterface):

    def __init__(self):
        self.__voiceRegExes: frozendict[MicrosoftTtsVoice, Collection[Pattern]] = self.__buildVoiceRegExes()

    def __buildVoiceRegExes(self) -> frozendict[MicrosoftTtsVoice, Collection[Pattern]]:
        david: FrozenList[Pattern] = FrozenList()
        david.append(re.compile(r'^\s*david\s*$', re.IGNORECASE))
        david.freeze()

        haruka: FrozenList[Pattern] = FrozenList()
        haruka.append(re.compile(r'^\s*haruka\s*$', re.IGNORECASE))
        haruka.freeze()

        zira: FrozenList[Pattern] = FrozenList()
        zira.append(re.compile(r'^\s*zira\s*$', re.IGNORECASE))
        zira.freeze()

        return frozendict({
            MicrosoftTtsVoice.DAVID: david,
            MicrosoftTtsVoice.HARUKA: haruka,
            MicrosoftTtsVoice.ZIRA: zira

        })

    async def parseVoice(
        self,
        string: str | Any | None
    ) -> MicrosoftTtsVoice | None:
        if not utils.isValidStr(string):
            return None

        for microsoftTtsVoice, voiceRegExes in self.__voiceRegExes.items():
            for voiceRegEx in voiceRegExes:
                if voiceRegEx.fullmatch(string) is not None:
                    return microsoftTtsVoice

        return None

    async def requireVoice(
        self,
        string: str | Any | None
    ) -> MicrosoftTtsVoice:
        result = await self.parseVoice(string)

        if result is None:
            raise ValueError(f'Unable to parse \"{string}\" into MicrosoftTtsVoice value!')

        return result

    async def serializeVoice(
        self,
        voice: MicrosoftTtsVoice
    ) -> str:
        if not isinstance(voice, MicrosoftTtsVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        match voice:
            case MicrosoftTtsVoice.DAVID: return 'david'
            case MicrosoftTtsVoice.HARUKA: return 'haruka'
            case MicrosoftTtsVoice.ZIRA: return 'zira'
            case _: raise RuntimeError(f'Encountered unknown MicrosoftTtsVoice value: \"{voice}\"')
