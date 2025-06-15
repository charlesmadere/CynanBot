import re
from typing import Any, Collection, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from ..models.ttsMonsterDonationPrefixConfig import TtsMonsterDonationPrefixConfig
from ..models.ttsMonsterPrivateApiTtsData import TtsMonsterPrivateApiTtsData
from ..models.ttsMonsterPrivateApiTtsResponse import TtsMonsterPrivateApiTtsResponse
from ..models.ttsMonsterVoice import TtsMonsterVoice
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TtsMonsterPrivateApiJsonMapper(TtsMonsterPrivateApiJsonMapperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        provider: str = 'provider'
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        if not utils.isValidStr(provider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__timber: TimberInterface = timber
        self.__provider: str = provider

        self.__voiceRegExes: frozendict[TtsMonsterVoice, Collection[Pattern]] = self.__buildVoiceRegExes()

    def __buildVoiceRegExes(self) -> frozendict[TtsMonsterVoice, Collection[Pattern]]:
        adam: FrozenList[Pattern] = FrozenList()
        adam.append(re.compile(r'^\s*adam\s*$', re.IGNORECASE))
        adam.freeze()

        announcer: FrozenList[Pattern] = FrozenList()
        announcer.append(re.compile(r'^\s*announcer?\s*$', re.IGNORECASE))
        announcer.freeze()

        asmr: FrozenList[Pattern] = FrozenList()
        asmr.append(re.compile(r'^\s*asmr\s*$', re.IGNORECASE))
        asmr.append(re.compile(r'^\s*a\.s\.m\.r\.\s*$', re.IGNORECASE))
        asmr.freeze()

        brian: FrozenList[Pattern] = FrozenList()
        brian.append(re.compile(r'^\s*brian\s*$', re.IGNORECASE))
        brian.freeze()

        glados: FrozenList[Pattern] = FrozenList()
        glados.append(re.compile(r'^\s*glados\s*$', re.IGNORECASE))
        glados.freeze()

        hikari: FrozenList[Pattern] = FrozenList()
        hikari.append(re.compile(r'^\s*hikari\s*$', re.IGNORECASE))
        hikari.freeze()

        jazz: FrozenList[Pattern] = FrozenList()
        jazz.append(re.compile(r'^\s*jazz\s*$', re.IGNORECASE))
        jazz.freeze()

        johnny: FrozenList[Pattern] = FrozenList()
        johnny.append(re.compile(r'^\s*joh?n\s*$', re.IGNORECASE))
        johnny.append(re.compile(r'^\s*joh?nn?y\s*$', re.IGNORECASE))
        johnny.freeze()

        kkona: FrozenList[Pattern] = FrozenList()
        kkona.append(re.compile(r'^\s*kk?ona\s*$', re.IGNORECASE))
        kkona.freeze()

        narrator: FrozenList[Pattern] = FrozenList()
        narrator.append(re.compile(r'^\s*narrator\s*$', re.IGNORECASE))
        narrator.freeze()

        pirate: FrozenList[Pattern] = FrozenList()
        pirate.append(re.compile(r'^\s*pirate\s*$', re.IGNORECASE))
        pirate.freeze()

        shadow: FrozenList[Pattern] = FrozenList()
        shadow.append(re.compile(r'^\s*shadow\s*$', re.IGNORECASE))
        shadow.freeze()

        sonic: FrozenList[Pattern] = FrozenList()
        sonic.append(re.compile(r'^\s*sonic\s*$', re.IGNORECASE))
        sonic.freeze()

        spongebob: FrozenList[Pattern] = FrozenList()
        spongebob.append(re.compile(r'^\s*sponge(?:\s+|_|-)?bob\s*$', re.IGNORECASE))
        spongebob.freeze()

        vomit: FrozenList[Pattern] = FrozenList()
        vomit.append(re.compile(r'^\s*vomit\s*$', re.IGNORECASE))
        vomit.freeze()

        weeb: FrozenList[Pattern] = FrozenList()
        weeb.append(re.compile(r'^\s*weeb\s*$', re.IGNORECASE))
        weeb.freeze()

        witch: FrozenList[Pattern] = FrozenList()
        witch.append(re.compile(r'^\s*witch\s*$', re.IGNORECASE))
        witch.freeze()

        zeroTwo: FrozenList[Pattern] = FrozenList()
        zeroTwo.append(re.compile(r'^\s*zero(?:\s+|_|-)?two\s*$', re.IGNORECASE))
        zeroTwo.append(re.compile(r'^\s*02\s*$', re.IGNORECASE))
        zeroTwo.freeze()

        zoomer: FrozenList[Pattern] = FrozenList()
        zoomer.append(re.compile(r'^\s*zoome?r\s*$', re.IGNORECASE))
        zoomer.freeze()

        return frozendict({
            TtsMonsterVoice.ADAM: adam,
            TtsMonsterVoice.ANNOUNCER: announcer,
            TtsMonsterVoice.ASMR: asmr,
            TtsMonsterVoice.BRIAN: brian,
            TtsMonsterVoice.GLADOS: glados,
            TtsMonsterVoice.HIKARI: hikari,
            TtsMonsterVoice.JAZZ: jazz,
            TtsMonsterVoice.JOHNNY: johnny,
            TtsMonsterVoice.KKONA: kkona,
            TtsMonsterVoice.NARRATOR: narrator,
            TtsMonsterVoice.PIRATE: pirate,
            TtsMonsterVoice.SHADOW: shadow,
            TtsMonsterVoice.SONIC: sonic,
            TtsMonsterVoice.SPONGEBOB: spongebob,
            TtsMonsterVoice.VOMIT: vomit,
            TtsMonsterVoice.WEEB: weeb,
            TtsMonsterVoice.WITCH: witch,
            TtsMonsterVoice.ZERO_TWO: zeroTwo,
            TtsMonsterVoice.ZOOMER: zoomer,
        })

    async def parseDonationPrefixConfig(
        self,
        string: str | Any | None
    ) -> TtsMonsterDonationPrefixConfig | None:
        if not utils.isValidStr(string):
            return None

        string = string.lower()

        match string:
            case 'disabled': return TtsMonsterDonationPrefixConfig.DISABLED
            case 'enabled': return TtsMonsterDonationPrefixConfig.ENABLED
            case 'if_message_is_blank': return TtsMonsterDonationPrefixConfig.IF_MESSAGE_IS_BLANK
            case _: return None

    async def parseTtsData(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterPrivateApiTtsData | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        link: str | None = None
        if 'link' in jsonContents and utils.isValidStr(jsonContents.get('link')):
            link = utils.getStrFromDict(jsonContents, 'link')

        if not utils.isValidUrl(link):
            self.__timber.log('TtsMonsterPrivateApiJsonMapper', f'\"link\" value in JSON response is missing/malformed ({link=}) ({jsonContents=})')
            return None

        warning: str | None = None
        if 'warning' in jsonContents and utils.isValidStr(jsonContents.get('warning')):
            warning = utils.getStrFromDict(jsonContents, 'warning')

        return TtsMonsterPrivateApiTtsData(
            link = link,
            warning = warning
        )

    async def parseTtsResponse(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterPrivateApiTtsResponse | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        status = utils.getIntFromDict(jsonContents, 'status')
        data = await self.parseTtsData(jsonContents.get('data'))

        if data is None:
            return None

        return TtsMonsterPrivateApiTtsResponse(
            status = status,
            data = data
        )

    async def parseVoice(
        self,
        string: str | Any | None
    ) -> TtsMonsterVoice | None:
        if not utils.isValidStr(string):
            return None

        for ttsMonsterVoice, voiceRegExes in self.__voiceRegExes.items():
            for voiceRegEx in voiceRegExes:
                if voiceRegEx.fullmatch(string) is not None:
                    return ttsMonsterVoice

        return None

    async def requireDonationPrefixConfig(
        self,
        string: str | Any | None
    ) -> TtsMonsterDonationPrefixConfig:
        result = await self.parseDonationPrefixConfig(string)

        if result is None:
            raise ValueError(f'Unable to parse TtsMonsterDonationPrefixConfig from string: \"{string}\"')

        return result

    async def requireVoice(
        self,
        string: str | Any | None
    ) -> TtsMonsterVoice:
        result = await self.parseVoice(string)

        if result is None:
            raise ValueError(f'Unable to parse TtsMonsterVoice from string: \"{string}\"')

        return result

    async def serializeDonationPrefixConfig(
        self,
        donationPrefixConfig: TtsMonsterDonationPrefixConfig
    ) -> str:
        if not isinstance(donationPrefixConfig, TtsMonsterDonationPrefixConfig):
            raise TypeError(f'donationPrefixConfig argument is malformed: \"{donationPrefixConfig}\"')

        match donationPrefixConfig:
            case TtsMonsterDonationPrefixConfig.DISABLED: return 'disabled'
            case TtsMonsterDonationPrefixConfig.ENABLED: return 'enabled'
            case TtsMonsterDonationPrefixConfig.IF_MESSAGE_IS_BLANK: return 'if_message_is_blank'
            case _: raise RuntimeError(f'Encountered unknown TtsMonsterDonationPrefixConfig value: \"{donationPrefixConfig}\"')

    async def serializeGenerateTtsJsonBody(
        self,
        key: str,
        message: str,
        userId: str
    ) -> dict[str, Any]:
        if not utils.isValidStr(key):
            raise TypeError(f'key argument is malformed: \"{key}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        return {
            'data': {
                'ai': True,
                'details': {
                    'provider': self.__provider
                },
                'key': key,
                'message': message,
                'userId': userId
            }
        }

    async def serializeVoice(
        self,
        voice: TtsMonsterVoice
    ) -> str:
        if not isinstance(voice, TtsMonsterVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        match voice:
            case TtsMonsterVoice.ADAM: return 'adam'
            case TtsMonsterVoice.ANNOUNCER: return 'announcer'
            case TtsMonsterVoice.ASMR: return 'asmr'
            case TtsMonsterVoice.BRIAN: return 'brian'
            case TtsMonsterVoice.GLADOS: return 'glados'
            case TtsMonsterVoice.HIKARI: return 'hikari'
            case TtsMonsterVoice.JAZZ: return 'jazz'
            case TtsMonsterVoice.JOHNNY: return 'johnny'
            case TtsMonsterVoice.KKONA: return 'kkona'
            case TtsMonsterVoice.NARRATOR: return 'narrator'
            case TtsMonsterVoice.PIRATE: return 'pirate'
            case TtsMonsterVoice.SHADOW: return 'shadow'
            case TtsMonsterVoice.SONIC: return 'sonic'
            case TtsMonsterVoice.SPONGEBOB: return 'spongebob'
            case TtsMonsterVoice.VOMIT: return 'vomit'
            case TtsMonsterVoice.WEEB: return 'weeb'
            case TtsMonsterVoice.WITCH: return 'witch'
            case TtsMonsterVoice.ZERO_TWO: return 'zero_two'
            case TtsMonsterVoice.ZOOMER: return 'zoomer'
            case _: raise RuntimeError(f'Encountered unknown TtsMonsterVoice value: \"{voice}\"')
