from abc import abstractmethod

from .chatBandInstrument import ChatBandInstrument
from ..misc.clearable import Clearable


class ChatBandInstrumentSoundsRepositoryInterface(Clearable):

    @abstractmethod
    async def getRandomSound(self, instrument: ChatBandInstrument) -> str | None:
        pass
