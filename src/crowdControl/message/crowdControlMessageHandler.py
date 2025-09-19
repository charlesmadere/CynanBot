from typing import Final

from .crowdControlMessage import CrowdControlMessage
from .crowdControlMessageListener import CrowdControlMessageListener
from .crowdControlMessagePresenterInterface import CrowdControlMessagePresenterInterface
from ...misc import utils as utils
from ...twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface


class CrowdControlMessageHandler(CrowdControlMessageListener):

    def __init__(
        self,
        crowdControlMessagePresenter: CrowdControlMessagePresenterInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(crowdControlMessagePresenter, CrowdControlMessagePresenterInterface):
            raise TypeError(f'crowdControlMessagePresenter argument is malformed: \"{crowdControlMessagePresenter}\"')
        if not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__crowdControlMessagePresenter: Final[CrowdControlMessagePresenterInterface] = crowdControlMessagePresenter
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

    async def onNewCrowdControlMessage(self, crowdControlMessage: CrowdControlMessage):
        message = await self.__crowdControlMessagePresenter.toString(crowdControlMessage)

        if not utils.isValidStr(message):
            return

        self.__twitchChatMessenger.send(
            text = message,
            twitchChannelId = crowdControlMessage.twitchChannelId,
            replyMessageId = crowdControlMessage.twitchChatMessageId,
        )
