from abc import ABC, abstractmethod

from .cheerActionType import CheerActionType
from .wizards.absWizard import AbsWizard


class CheerActionsWizardInterface(ABC):

    @abstractmethod
    async def complete(self, twitchChannelId: str):
        pass

    @abstractmethod
    async def get(self, twitchChannelId: str) -> AbsWizard | None:
        pass

    @abstractmethod
    async def start(
        self,
        cheerActionType: CheerActionType,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> AbsWizard:
        pass
