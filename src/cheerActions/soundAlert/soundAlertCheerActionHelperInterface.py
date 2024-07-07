from abc import ABC, abstractmethod

from ..absCheerAction import AbsCheerAction
from ...users.userInterface import UserInterface


class SoundAlertCheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleSoundAlertCheerAction(
        self,
        bits: int,
        actions: list[AbsCheerAction],
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
