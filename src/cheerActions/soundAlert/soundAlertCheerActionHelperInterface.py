from abc import ABC, abstractmethod
from typing import Collection

from ..absCheerAction import AbsCheerAction
from ...users.userInterface import UserInterface


class SoundAlertCheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleSoundAlertCheerAction(
        self,
        actions: Collection[AbsCheerAction],
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        pass
