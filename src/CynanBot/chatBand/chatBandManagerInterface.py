from abc import abstractmethod

from CynanBot.misc.clearable import Clearable


class ChatBandManagerInterface(Clearable):

    @abstractmethod
    async def playInstrumentForMessage(self, twitchChannel: str, author: str, message: str) -> bool:
        pass
