from abc import abstractmethod

from ..misc.clearable import Clearable


class ChatBandManagerInterface(Clearable):

    @abstractmethod
    async def playInstrumentForMessage(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        author: str,
        message: str
    ) -> bool:
        pass
