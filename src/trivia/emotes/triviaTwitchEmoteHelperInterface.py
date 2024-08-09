from abc import abstractmethod

from ...misc.clearable import Clearable


class TriviaTwitchChannelEmoteHelperInterface(Clearable):

    @abstractmethod
    async def getCelebratoryEmote(self) -> str | None:
        pass
