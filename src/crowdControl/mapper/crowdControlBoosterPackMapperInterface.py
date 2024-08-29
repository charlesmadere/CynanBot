from abc import ABC, abstractmethod

from ..actions.crowdControlAction import CrowdControlAction
from ..actions.crowdControlButton import CrowdControlButton
from ...users.crowdControl.crowdControlBoosterPack import CrowdControlBoosterPack
from ...users.crowdControl.crowdControlInputType import CrowdControlInputType


class CrowdControlBoosterPackMapperInterface(ABC):

    @abstractmethod
    async def toAction(
        self,
        boosterPack: CrowdControlBoosterPack,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> CrowdControlAction:
        pass

    @abstractmethod
    async def toButton(
        self,
        inputType: CrowdControlInputType
    ) -> CrowdControlButton:
        pass
