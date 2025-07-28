import re
from re import Pattern
from typing import Any, Collection, Final

from frozendict import frozendict
from frozenlist import FrozenList

from .halfLifeVoiceParserInterface import HalfLifeVoiceParserInterface
from ..models.halfLifeVoice import HalfLifeVoice
from ...misc import utils as utils


class HalfLifeVoiceParser(HalfLifeVoiceParserInterface):

    def __init__(self):
        self.__voiceRegExes: Final[frozendict[HalfLifeVoice, Collection[Pattern]]] = self.__buildVoiceRegExes()

    def __buildVoiceRegExes(self) -> frozendict[HalfLifeVoice, Collection[Pattern]]:
        allVoices: FrozenList[Pattern] = FrozenList()
        allVoices.append(re.compile(r'^\s*all\s*$', re.IGNORECASE))
        allVoices.append(re.compile(r'^\s*all(?:\s+|_|-)?voices?\s*$', re.IGNORECASE))
        allVoices.freeze()

        barney: FrozenList[Pattern] = FrozenList()
        barney.append(re.compile(r'^\s*barney\s*$', re.IGNORECASE))
        barney.freeze()

        hev: FrozenList[Pattern] = FrozenList()
        hev.append(re.compile(r'^\s*hev\s*$', re.IGNORECASE))
        hev.freeze()

        intercom: FrozenList[Pattern] = FrozenList()
        intercom.append(re.compile(r'^\s*intercom\s*$', re.IGNORECASE))
        intercom.freeze()

        police: FrozenList[Pattern] = FrozenList()
        police.append(re.compile(r'^\s*police\s*$', re.IGNORECASE))
        police.freeze()

        scientist: FrozenList[Pattern] = FrozenList()
        scientist.append(re.compile(r'^\s*science\s*$', re.IGNORECASE))
        scientist.append(re.compile(r'^\s*scientist\s*$', re.IGNORECASE))
        scientist.freeze()

        soldier: FrozenList[Pattern] = FrozenList()
        soldier.append(re.compile(r'^\s*soldier\s*$', re.IGNORECASE))
        soldier.freeze()

        return frozendict({
            HalfLifeVoice.ALL: allVoices,
            HalfLifeVoice.BARNEY: barney,
            HalfLifeVoice.HEV: hev,
            HalfLifeVoice.INTERCOM: intercom,
            HalfLifeVoice.POLICE: police,
            HalfLifeVoice.SCIENTIST: scientist,
            HalfLifeVoice.SOLDIER: soldier,
        })

    def parseVoice(self, voiceString: str | Any | None) -> HalfLifeVoice | None:
        if not utils.isValidStr(voiceString):
            return None

        for halfLifeVoice, voiceRegExes in self.__voiceRegExes.items():
            for voiceRegEx in voiceRegExes:
                if voiceRegEx.fullmatch(voiceString) is not None:
                    return halfLifeVoice

        return None

    def requireVoice(self, voiceString: str | Any | None) -> HalfLifeVoice:
        result = self.parseVoice(voiceString)

        if result is None:
            raise ValueError(f'Unable to parse \"{voiceString}\" into HalfLifeVoice value!')

        return result

    def serializeVoice(self, voice: HalfLifeVoice) -> str:
        if not isinstance(voice, HalfLifeVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        return voice.keyName
