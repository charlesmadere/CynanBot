from datetime import datetime
from typing import Final

from .crowdControlAction import CrowdControlAction
from .crowdControlActionType import CrowdControlActionType
from .crowdControlButton import CrowdControlButton


class ButtonPressCrowdControlAction(CrowdControlAction):

    def __init__(
        self,
        button: CrowdControlButton,
        dateTime: datetime,
        actionId: str,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
    ):
        super().__init__(
            dateTime = dateTime,
            actionId = actionId,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
        )

        if not isinstance(button, CrowdControlButton):
            raise TypeError(f'button argument is malformed: \"{button}\"')

        self.__button: Final[CrowdControlButton] = button

    @property
    def actionType(self) -> CrowdControlActionType:
        return CrowdControlActionType.BUTTON_PRESS

    @property
    def button(self) -> CrowdControlButton:
        return self.__button
