from .models.chatterPrefferedTts import ChatterPreferredTts
from .models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from .models.google.googlePreferredTts import GooglePreferredTts
from .models.microsoftSam.microsoftSamPreferredTts import MicrosoftSamPreferredTts
from ..misc import utils as utils


class ChatterPreferredTtsPresenter:

    async def __decTalk(self, preferredTts: DecTalkPreferredTts) -> str:
        return 'DECtalk'

    async def __google(self, preferredTts: GooglePreferredTts) -> str:
        languageEntry = preferredTts.languageEntry

        if languageEntry is None:
            return 'Google'

        flag = languageEntry.flag

        if utils.isValidStr(flag):
            return f'Google ({languageEntry.name} {flag})'
        else:
            return f'Google ({languageEntry.name})'

    async def __microsoftSam(self, preferredTts: MicrosoftSamPreferredTts) -> str:
        return 'Microsoft Sam'

    async def printOut(self, preferredTts: ChatterPreferredTts) -> str:
        if not isinstance(preferredTts, ChatterPreferredTts):
            raise TypeError(f'preferredTts argument is malformed: \"{preferredTts}\"')

        absPreferredTts = preferredTts.preferredTts

        if isinstance(absPreferredTts, DecTalkPreferredTts):
            return await self.__decTalk(absPreferredTts)

        elif isinstance(absPreferredTts, GooglePreferredTts):
            return await self.__google(absPreferredTts)

        elif isinstance(absPreferredTts, MicrosoftSamPreferredTts):
            return await self.__microsoftSam(absPreferredTts)
