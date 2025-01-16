from .crowdControlMessage import CrowdControlMessage
from .crowdControlMessageListener import CrowdControlMessageListener
from .crowdControlMessagePresenterInterface import CrowdControlMessagePresenterInterface
from ...misc import utils as utils
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface


class CrowdControlMessageHandler(CrowdControlMessageListener):

    def __init__(
        self,
        crowdControlMessagePresenter: CrowdControlMessagePresenterInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(crowdControlMessagePresenter, CrowdControlMessagePresenterInterface):
            raise TypeError(f'crowdControlMessagePresenter argument is malformed: \"{crowdControlMessagePresenter}\"')
        if not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__crowdControlMessagePresenter: CrowdControlMessagePresenterInterface = crowdControlMessagePresenter
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def onNewCrowdControlMessage(self, crowdControlMessage: CrowdControlMessage):
        twitchChannelProvider = self.__twitchChannelProvider

        if twitchChannelProvider is None:
            return

        twitchChannel = await twitchChannelProvider.getTwitchChannel(crowdControlMessage.twitchChannel)
        message = await self.__crowdControlMessagePresenter.toString(crowdControlMessage)

        if not utils.isValidStr(message):
            return

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = crowdControlMessage.twitchChatMessageId
        )

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
