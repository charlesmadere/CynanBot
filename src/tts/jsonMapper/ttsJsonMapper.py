import re
from typing import Any, Final, Collection, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .ttsJsonMapperInterface import TtsJsonMapperInterface
from ..models.ttsProvider import TtsProvider
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TtsJsonMapper(TtsJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: Final[TimberInterface] = timber

        self.__ttsProviderRegExes: Final[frozendict[TtsProvider, Collection[Pattern]]] = self.__buildTtsProviderRegExes()

    async def asyncParseProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider | None:
        return self.parseProvider(ttsProvider)

    async def asyncRequireProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider:
        return self.requireProvider(ttsProvider)

    async def asyncSerializeProvider(
        self,
        ttsProvider: TtsProvider
    ) -> str:
        if not isinstance(ttsProvider, TtsProvider):
            raise TypeError(f'ttsProvider argument is malformed: \"{ttsProvider}\"')

        return self.serializeProvider(ttsProvider)

    def __buildTtsProviderRegExes(self) -> frozendict[TtsProvider, Collection[Pattern]]:
        commodoreSam: FrozenList[Pattern] = FrozenList()
        commodoreSam.append(re.compile(r'^\s*commodore(?:\s+|_|-)?sam\s*$', re.IGNORECASE))
        commodoreSam.freeze()

        decTalk: FrozenList[Pattern] = FrozenList()
        decTalk.append(re.compile(r'^\s*dec(?:\s+|_|-)?talk\s*$', re.IGNORECASE))
        decTalk.freeze()

        google: FrozenList[Pattern] = FrozenList()
        google.append(re.compile(r'^\s*google\s*$', re.IGNORECASE))
        google.freeze()

        halfLife: FrozenList[Pattern] = FrozenList()
        halfLife.append(re.compile(r'^\s*half(?:\s+|_|-)?life\s*$', re.IGNORECASE))
        halfLife.append(re.compile(r'^\s*hl\s*$', re.IGNORECASE))
        halfLife.freeze()

        microsoft: FrozenList[Pattern] = FrozenList()
        microsoft.append(re.compile(r'^\s*microsoft\s*$', re.IGNORECASE))
        microsoft.append(re.compile(r'^\s*ms\s*$', re.IGNORECASE))
        microsoft.freeze()

        microsoftSam: FrozenList[Pattern] = FrozenList()
        microsoftSam.append(re.compile(r'^\s*microsoft(?:\s+|_|-)?sam\s*$', re.IGNORECASE))
        microsoftSam.append(re.compile(r'^\s*ms(?:\s+|_|-)?sam\s*$', re.IGNORECASE))
        microsoftSam.freeze()

        singingDecTalk: FrozenList[Pattern] = FrozenList()
        singingDecTalk.append(re.compile(r'^\s*singing(?:\s+|_|-)?dec(?:\s+|_|-)?talk\s*$', re.IGNORECASE))
        singingDecTalk.freeze()

        streamElements: FrozenList[Pattern] = FrozenList()
        streamElements.append(re.compile(r'^\s*stream(?:\s+|_|-)?elements\s*$', re.IGNORECASE))
        streamElements.freeze()

        ttsMonster: FrozenList[Pattern] = FrozenList()
        ttsMonster.append(re.compile(r'^\s*tts(?:\s+|_|-)?monster\s*$', re.IGNORECASE))
        ttsMonster.freeze()

        return frozendict({
            TtsProvider.COMMODORE_SAM: commodoreSam,
            TtsProvider.DEC_TALK: decTalk,
            TtsProvider.GOOGLE: google,
            TtsProvider.HALF_LIFE: halfLife,
            TtsProvider.MICROSOFT: microsoft,
            TtsProvider.MICROSOFT_SAM: microsoftSam,
            TtsProvider.SINGING_DEC_TALK: singingDecTalk,
            TtsProvider.STREAM_ELEMENTS: streamElements,
            TtsProvider.TTS_MONSTER: ttsMonster,
        })

    def parseProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider | None:
        if not utils.isValidStr(ttsProvider):
            return None

        for ttsProviderEnum, providerRegExes in self.__ttsProviderRegExes.items():
            for providerRegEx in providerRegExes:
                if providerRegEx.fullmatch(ttsProvider) is not None:
                    return ttsProviderEnum

        return None

    def requireProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider:
        result = self.parseProvider(ttsProvider)

        if result is None:
            raise ValueError(f'Unable to parse \"{ttsProvider}\" into TtsProvider value!')

        return result

    def serializeProvider(
        self,
        ttsProvider: TtsProvider
    ) -> str:
        if not isinstance(ttsProvider, TtsProvider):
            raise TypeError(f'ttsProvider argument is malformed: \"{ttsProvider}\"')

        match ttsProvider:
            case TtsProvider.COMMODORE_SAM: return 'commodore_sam'
            case TtsProvider.DEC_TALK: return 'dec_talk'
            case TtsProvider.GOOGLE: return 'google'
            case TtsProvider.HALF_LIFE: return 'half_life'
            case TtsProvider.MICROSOFT: return 'microsoft'
            case TtsProvider.MICROSOFT_SAM: return 'microsoft_sam'
            case TtsProvider.SINGING_DEC_TALK: return 'singing_dec_talk'
            case TtsProvider.STREAM_ELEMENTS: return 'stream_elements'
            case TtsProvider.TTS_MONSTER: return 'tts_monster'
            case _: raise ValueError(f'The given TtsProvider value is unknown: \"{ttsProvider}\"')
