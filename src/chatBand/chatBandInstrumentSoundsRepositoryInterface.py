from abc import ABC, abstractmethod

from .chatBandInstrument import ChatBandInstrument
from ..misc.clearable import Clearable


class ChatBandInstrumentSoundsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getRandomSound(self, instrument: ChatBandInstrument) -> str | None:
        pass
