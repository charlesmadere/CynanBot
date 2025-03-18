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
        ana: FrozenList[Pattern] = FrozenList()
        ana.append(re.compile(r'^\s*ana\s*$', re.IGNORECASE))
        ana.freeze()

        andrew: FrozenList[Pattern] = FrozenList()
        andrew.append(re.compile(r'^\s*andrew\s*$', re.IGNORECASE))
        andrew.freeze()

        aria: FrozenList[Pattern] = FrozenList()
        aria.append(re.compile(r'^\s*aria\s*$', re.IGNORECASE))
        aria.freeze()

        ava: FrozenList[Pattern] = FrozenList()
        ava.append(re.compile(r'^\s*ava\s*$', re.IGNORECASE))
        ava.freeze()

        brian: FrozenList[Pattern] = FrozenList()
        brian.append(re.compile(r'^\s*brian\s*$', re.IGNORECASE))
        brian.freeze()

        christopher: FrozenList[Pattern] = FrozenList()
        christopher.append(re.compile(r'^\s*christopher\s*$', re.IGNORECASE))
        christopher.freeze()

        clara: FrozenList[Pattern] = FrozenList()
        clara.append(re.compile(r'^\s*clara\s*$', re.IGNORECASE))
        clara.freeze()

        david: FrozenList[Pattern] = FrozenList()
        david.append(re.compile(r'^\s*david\s*$', re.IGNORECASE))
        david.freeze()

        emma: FrozenList[Pattern] = FrozenList()
        emma.append(re.compile(r'^\s*emma\s*$', re.IGNORECASE))
        emma.freeze()

        eric: FrozenList[Pattern] = FrozenList()
        eric.append(re.compile(r'^\s*eric\s*$', re.IGNORECASE))
        eric.freeze()

        guy: FrozenList[Pattern] = FrozenList()
        guy.append(re.compile(r'^\s*guy\s*$', re.IGNORECASE))
        guy.freeze()

        haruka: FrozenList[Pattern] = FrozenList()
        haruka.append(re.compile(r'^\s*haruka\s*$', re.IGNORECASE))
        haruka.freeze()

        hortense: FrozenList[Pattern] = FrozenList()
        hortense.append(re.compile(r'^\s*hortense\s*$', re.IGNORECASE))
        hortense.freeze()

        jenny: FrozenList[Pattern] = FrozenList()
        jenny.append(re.compile(r'^\s*jenny\s*$', re.IGNORECASE))
        jenny.freeze()

        keita: FrozenList[Pattern] = FrozenList()
        keita.append(re.compile(r'^\s*keita\s*$', re.IGNORECASE))
        keita.freeze()

        liam: FrozenList[Pattern] = FrozenList()
        liam.append(re.compile(r'^\s*liam\s*$', re.IGNORECASE))
        liam.freeze()

        michelle: FrozenList[Pattern] = FrozenList()
        michelle.append(re.compile(r'^\s*michelle\s*$', re.IGNORECASE))
        michelle.freeze()

        nanami: FrozenList[Pattern] = FrozenList()
        nanami.append(re.compile(r'^\s*nanami\s*$', re.IGNORECASE))
        nanami.freeze()

        roger: FrozenList[Pattern] = FrozenList()
        roger.append(re.compile(r'^\s*roger\s*$', re.IGNORECASE))
        roger.freeze()

        steffan: FrozenList[Pattern] = FrozenList()
        steffan.append(re.compile(r'^\s*steffan\s*$', re.IGNORECASE))
        steffan.freeze()

        zira: FrozenList[Pattern] = FrozenList()
        zira.append(re.compile(r'^\s*zira\s*$', re.IGNORECASE))
        zira.freeze()

        return frozendict({
            MicrosoftTtsVoice.ANA: ana,
            MicrosoftTtsVoice.ANDREW: andrew,
            MicrosoftTtsVoice.ARIA: aria,
            MicrosoftTtsVoice.AVA: ava,
            MicrosoftTtsVoice.BRIAN: brian,
            MicrosoftTtsVoice.CHRISTOPHER: christopher,
            MicrosoftTtsVoice.CLARA: clara,
            MicrosoftTtsVoice.DAVID: david,
            MicrosoftTtsVoice.EMMA: emma,
            MicrosoftTtsVoice.ERIC: eric,
            MicrosoftTtsVoice.GUY: guy,
            MicrosoftTtsVoice.HARUKA: haruka,
            MicrosoftTtsVoice.HORTENSE: hortense,
            MicrosoftTtsVoice.JENNY: jenny,
            MicrosoftTtsVoice.KEITA: keita,
            MicrosoftTtsVoice.LIAM: liam,
            MicrosoftTtsVoice.MICHELLE: michelle,
            MicrosoftTtsVoice.NANAMI: nanami,
            MicrosoftTtsVoice.ROGER: roger,
            MicrosoftTtsVoice.STEFFAN: steffan,
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
            case MicrosoftTtsVoice.ANA: return 'ana'
            case MicrosoftTtsVoice.ANDREW: return 'andrew'
            case MicrosoftTtsVoice.ARIA: return 'aria'
            case MicrosoftTtsVoice.AVA: return 'ava'
            case MicrosoftTtsVoice.BRIAN: return 'brian'
            case MicrosoftTtsVoice.CHRISTOPHER: return 'christopher'
            case MicrosoftTtsVoice.CLARA: return 'clara'
            case MicrosoftTtsVoice.DAVID: return 'david'
            case MicrosoftTtsVoice.EMMA: return 'emma'
            case MicrosoftTtsVoice.ERIC: return 'eric'
            case MicrosoftTtsVoice.GUY: return 'guy'
            case MicrosoftTtsVoice.HARUKA: return 'haruka'
            case MicrosoftTtsVoice.HORTENSE: return 'hortense'
            case MicrosoftTtsVoice.JENNY: return 'jenny'
            case MicrosoftTtsVoice.KEITA: return 'keita'
            case MicrosoftTtsVoice.LIAM: return 'liam'
            case MicrosoftTtsVoice.MICHELLE: return 'michelle'
            case MicrosoftTtsVoice.NANAMI: return 'nanami'
            case MicrosoftTtsVoice.ROGER: return 'roger'
            case MicrosoftTtsVoice.STEFFAN: return 'steffan'
            case MicrosoftTtsVoice.ZIRA: return 'zira'
            case _: raise RuntimeError(f'Encountered unknown MicrosoftTtsVoice value: \"{voice}\"')
