from .models.chatterPrefferedTts import ChatterPreferredTts
from .models.commodoreSam.commodoreSamPreferredTts import CommodoreSamPreferredTts
from .models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from .models.google.googlePreferredTts import GooglePreferredTts
from .models.halfLife.halfLifePreferredTts import HalfLifePreferredTts
from .models.microsoft.microsoftTtsPreferredTts import MicrosoftTtsPreferredTts
from .models.microsoftSam.microsoftSamPreferredTts import MicrosoftSamPreferredTts
from .models.singingDecTalk.singingDecTalkPreferredTts import SingingDecTalkPreferredTts
from .models.streamElements.streamElementsPreferredTts import StreamElementsPreferredTts
from .models.ttsMonster.ttsMonsterPreferredTts import TtsMonsterPreferredTts
from ..misc import utils as utils
from ..tts.models.ttsProvider import TtsProvider


class ChatterPreferredTtsPresenter:

    async def __commodoreSam(self, preferredTts: CommodoreSamPreferredTts) -> str:
        return TtsProvider.COMMODORE_SAM.humanName

    async def __decTalk(self, preferredTts: DecTalkPreferredTts) -> str:
        decTalkVoice = preferredTts.voice

        if decTalkVoice is None:
            return TtsProvider.DEC_TALK.humanName

        return f'{TtsProvider.DEC_TALK.humanName} ({decTalkVoice.humanName})'

    async def __google(self, preferredTts: GooglePreferredTts) -> str:
        languageEntry = preferredTts.languageEntry
        googleHumanName = TtsProvider.GOOGLE.humanName

        if languageEntry is None:
            return googleHumanName

        flag = languageEntry.flag

        if utils.isValidStr(flag):
            return f'{googleHumanName} ({languageEntry.humanName} {flag})'
        else:
            return f'{googleHumanName} ({languageEntry.humanName})'

    async def __halfLife(self, preferredTts: HalfLifePreferredTts) -> str:
        voice = preferredTts.halfLifeVoiceEntry

        if voice is None:
            return TtsProvider.HALF_LIFE.humanName

        return f'{TtsProvider.HALF_LIFE.humanName} ({voice.humanName})'

    async def __microsoftSam(self, preferredTts: MicrosoftSamPreferredTts) -> str:
        voice = preferredTts.voice

        if voice is None:
            return TtsProvider.MICROSOFT_SAM.humanName

        return f'{TtsProvider.MICROSOFT_SAM.humanName} ({voice.humanName})'

    async def __microsoftTts(self, preferredTts: MicrosoftTtsPreferredTts) -> str:
        voice = preferredTts.voice

        if voice is None:
            return TtsProvider.MICROSOFT.humanName

        return f'{TtsProvider.MICROSOFT.humanName} ({voice.humanName})'

    async def __singingDecTalk(self, preferredTts: SingingDecTalkPreferredTts) -> str:
        return TtsProvider.SINGING_DEC_TALK.humanName

    async def __streamElements(self, preferredTts: StreamElementsPreferredTts) -> str:
        voice = preferredTts.voice

        if voice is None:
            return TtsProvider.STREAM_ELEMENTS.humanName

        return f'{TtsProvider.STREAM_ELEMENTS.humanName} ({voice.humanName})'

    async def __ttsMonster(self, preferredTts: TtsMonsterPreferredTts) -> str:
        voice = preferredTts.voice

        if voice is None:
            return TtsProvider.TTS_MONSTER.humanName

        return f'{TtsProvider.TTS_MONSTER.humanName} ({voice.humanName})'

    async def printOut(self, preferredTts: ChatterPreferredTts) -> str:
        if not isinstance(preferredTts, ChatterPreferredTts):
            raise TypeError(f'preferredTts argument is malformed: \"{preferredTts}\"')

        absPreferredTts = preferredTts.preferredTts

        if isinstance(absPreferredTts, CommodoreSamPreferredTts):
            return await self.__commodoreSam(absPreferredTts)

        elif isinstance(absPreferredTts, DecTalkPreferredTts):
            return await self.__decTalk(absPreferredTts)

        elif isinstance(absPreferredTts, GooglePreferredTts):
            return await self.__google(absPreferredTts)

        elif isinstance(absPreferredTts, HalfLifePreferredTts):
            return await self.__halfLife(absPreferredTts)

        elif isinstance(absPreferredTts, MicrosoftSamPreferredTts):
            return await self.__microsoftSam(absPreferredTts)

        elif isinstance(absPreferredTts, MicrosoftTtsPreferredTts):
            return await self.__microsoftTts(absPreferredTts)

        elif isinstance(absPreferredTts, SingingDecTalkPreferredTts):
            return await self.__singingDecTalk(absPreferredTts)

        elif isinstance(absPreferredTts, StreamElementsPreferredTts):
            return await self.__streamElements(absPreferredTts)

        elif isinstance(absPreferredTts, TtsMonsterPreferredTts):
            return await self.__ttsMonster(absPreferredTts)

        else:
            raise ValueError(f'Encountered unknown AbsPreferredTts: \"{preferredTts}\"')
