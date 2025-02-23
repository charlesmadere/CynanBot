from .models.chatterPrefferedTts import ChatterPreferredTts
from .models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from .models.google.googlePreferredTts import GooglePreferredTts
from .models.halfLife.halfLifePreferredTts import HalfLifePreferredTts
from .models.microsoftSam.microsoftSamPreferredTts import MicrosoftSamPreferredTts
from .models.singingDecTalk.singingDecTalkPreferredTts import SingingDecTalkPreferredTts
from .models.streamElements.streamElementsPreferredTts import StreamElementsPreferredTts
from .models.ttsMonster.ttsMonsterPreferredTts import TtsMonsterPreferredTts
from ..misc import utils as utils
from ..tts.ttsProvider import TtsProvider


class ChatterPreferredTtsPresenter:

    async def __decTalk(self, preferredTts: DecTalkPreferredTts) -> str:
        return TtsProvider.DEC_TALK.humanName

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
        halfLifeVoiceEntry = preferredTts.halfLifeVoiceEntry
        halfLifeHumanName = TtsProvider.HALF_LIFE.humanName

        if halfLifeVoiceEntry is None:
            return halfLifeHumanName

        return f'{halfLifeHumanName} ({halfLifeVoiceEntry.humanName})'

    async def __microsoftSam(self, preferredTts: MicrosoftSamPreferredTts) -> str:
        microsoftSamVoiceEntry = preferredTts.microsoftSamVoiceEntry
        microsoftSamHumanName = TtsProvider.MICROSOFT_SAM.humanName

        if microsoftSamVoiceEntry is None:
            return microsoftSamHumanName

        return f'{microsoftSamHumanName} ({microsoftSamVoiceEntry.humanName})'

    async def __singingDecTalk(self, preferredTts: SingingDecTalkPreferredTts) -> str:
        return TtsProvider.SINGING_DEC_TALK.humanName

    async def __streamElements(self, preferredTts: StreamElementsPreferredTts) -> str:
        return TtsProvider.STREAM_ELEMENTS.humanName

    async def __ttsMonster(self, preferredTts: TtsMonsterPreferredTts) -> str:
        ttsMonsterVoiceEntry = preferredTts.ttsMonsterVoiceEntry
        ttsMonsterHumanName = TtsProvider.TTS_MONSTER.humanName

        if ttsMonsterVoiceEntry is None:
            return ttsMonsterHumanName

        return f'{ttsMonsterHumanName} ({ttsMonsterVoiceEntry.humanName})'

    async def printOut(self, preferredTts: ChatterPreferredTts) -> str:
        if not isinstance(preferredTts, ChatterPreferredTts):
            raise TypeError(f'preferredTts argument is malformed: \"{preferredTts}\"')

        absPreferredTts = preferredTts.preferredTts

        if isinstance(absPreferredTts, DecTalkPreferredTts):
            return await self.__decTalk(absPreferredTts)

        elif isinstance(absPreferredTts, GooglePreferredTts):
            return await self.__google(absPreferredTts)

        elif isinstance(absPreferredTts, HalfLifePreferredTts):
            return await self.__halfLife(absPreferredTts)

        elif isinstance(absPreferredTts, MicrosoftSamPreferredTts):
            return await self.__microsoftSam(absPreferredTts)

        elif isinstance(absPreferredTts, SingingDecTalkPreferredTts):
            return await self.__singingDecTalk(absPreferredTts)

        elif isinstance(absPreferredTts, StreamElementsPreferredTts):
            return await self.__streamElements(absPreferredTts)

        elif isinstance(absPreferredTts, TtsMonsterPreferredTts):
            return await self.__ttsMonster(absPreferredTts)
        else:
            raise ValueError(f'Encountered unknown AbsPreferredTts: \"{preferredTts}\"')
