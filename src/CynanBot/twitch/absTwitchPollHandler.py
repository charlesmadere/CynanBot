from abc import ABC, abstractmethod

from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.users.userInterface import UserInterface


class AbsTwitchPollHandler(ABC):

    @abstractmethod
    async def onNewPoll(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        pass
