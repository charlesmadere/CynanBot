from .models.chatterPrefferedTts import ChatterPreferredTts
from .models.commodoreSam.commodoreSamTtsProperties import CommodoreSamTtsProperties
from .models.decTalk.decTalkTtsProperties import DecTalkTtsProperties
from .models.google.googleTtsProperties import GoogleTtsProperties
from .models.halfLife.halfLifeTtsProperties import HalfLifeTtsProperties
from .models.microsoft.microsoftTtsTtsProperties import MicrosoftTtsTtsProperties
from .models.microsoftSam.microsoftSamTtsProperties import MicrosoftSamTtsProperties
from .models.shotgunTts.shotgunTtsTtsProperties import ShotgunTtsTtsProperties
from .models.streamElements.streamElementsTtsProperties import StreamElementsTtsProperties
from .models.ttsMonster.ttsMonsterTtsProperties import TtsMonsterTtsProperties
from .models.unrestrictedDecTalk.unrestrictedDecTalkTtsProperties import UnrestrictedDecTalkTtsProperties
from ..misc import utils as utils
from ..tts.models.ttsProvider import TtsProvider


class ChatterPreferredTtsPresenter:

    async def __commodoreSam(self, properties: CommodoreSamTtsProperties) -> str:
        return TtsProvider.COMMODORE_SAM.humanName

    async def __decTalk(self, properties: DecTalkTtsProperties) -> str:
        voice = properties.voice

        if voice is None:
            return TtsProvider.DEC_TALK.humanName

        return f'{TtsProvider.DEC_TALK.humanName} ({voice.humanName})'

    async def __google(self, properties: GoogleTtsProperties) -> str:
        languageEntry = properties.languageEntry

        if languageEntry is None:
            return TtsProvider.GOOGLE.humanName

        flag = languageEntry.flag

        if utils.isValidStr(flag):
            return f'{TtsProvider.GOOGLE.humanName} ({languageEntry.humanName} {flag})'

        return f'{TtsProvider.GOOGLE.humanName} ({languageEntry.humanName})'

    async def __halfLife(self, properties: HalfLifeTtsProperties) -> str:
        voice = properties.voice

        if voice is None:
            return TtsProvider.HALF_LIFE.humanName

        return f'{TtsProvider.HALF_LIFE.humanName} ({voice.humanName})'

    async def __microsoftSam(self, properties: MicrosoftSamTtsProperties) -> str:
        voice = properties.voice

        if voice is None:
            return TtsProvider.MICROSOFT_SAM.humanName

        return f'{TtsProvider.MICROSOFT_SAM.humanName} ({voice.humanName})'

    async def __microsoftTts(self, properties: MicrosoftTtsTtsProperties) -> str:
        voice = properties.voice

        if voice is None:
            return TtsProvider.MICROSOFT.humanName

        return f'{TtsProvider.MICROSOFT.humanName} ({voice.humanName})'

    async def __shotgunTts(self, properties: ShotgunTtsTtsProperties) -> str:
        return TtsProvider.SHOTGUN_TTS.humanName

    async def __streamElements(self, properties: StreamElementsTtsProperties) -> str:
        voice = properties.voice

        if voice is None:
            return TtsProvider.STREAM_ELEMENTS.humanName

        return f'{TtsProvider.STREAM_ELEMENTS.humanName} ({voice.humanName})'

    async def __ttsMonster(self, properties: TtsMonsterTtsProperties) -> str:
        voice = properties.voice

        if voice is None:
            return TtsProvider.TTS_MONSTER.humanName

        return f'{TtsProvider.TTS_MONSTER.humanName} ({voice.humanName})'

    async def __unrestrictedDecTalk(self, properties: UnrestrictedDecTalkTtsProperties) -> str:
        return TtsProvider.UNRESTRICTED_DEC_TALK.humanName

    async def printOut(self, preferredTts: ChatterPreferredTts) -> str:
        if not isinstance(preferredTts, ChatterPreferredTts):
            raise TypeError(f'preferredTts argument is malformed: \"{preferredTts}\"')

        properties = preferredTts.properties

        if isinstance(properties, CommodoreSamTtsProperties):
            return await self.__commodoreSam(properties)

        elif isinstance(properties, DecTalkTtsProperties):
            return await self.__decTalk(properties)

        elif isinstance(properties, GoogleTtsProperties):
            return await self.__google(properties)

        elif isinstance(properties, HalfLifeTtsProperties):
            return await self.__halfLife(properties)

        elif isinstance(properties, MicrosoftSamTtsProperties):
            return await self.__microsoftSam(properties)

        elif isinstance(properties, MicrosoftTtsTtsProperties):
            return await self.__microsoftTts(properties)

        elif isinstance(properties, ShotgunTtsTtsProperties):
            return await self.__shotgunTts(properties)

        elif isinstance(properties, StreamElementsTtsProperties):
            return await self.__streamElements(properties)

        elif isinstance(properties, TtsMonsterTtsProperties):
            return await self.__ttsMonster(properties)

        elif isinstance(properties, UnrestrictedDecTalkTtsProperties):
            return await self.__unrestrictedDecTalk(properties)

        else:
            raise ValueError(f'Encountered unknown AbsTtsProperties ({preferredTts=}) ({properties=})')
