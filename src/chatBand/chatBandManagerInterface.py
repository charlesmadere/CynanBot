from abc import ABC, abstractmethod

from ..misc.clearable import Clearable


class ChatBandManagerInterface(Clearable, ABC):

    @abstractmethod
    async def playInstrumentForMessage(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        author: str,
        message: str
    ) -> bool:
        pass
