from abc import ABC, abstractmethod

from CynanBot.cheerActions.cheerAction import CheerAction
from CynanBot.users.userInterface import UserInterface


class SoundAlertCheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleSoundAlertCheerAction(
        self,
        bits: int,
        actions: list[CheerAction],
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
