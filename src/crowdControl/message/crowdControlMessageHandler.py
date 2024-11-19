from .crowdControlMessage import CrowdControlMessage
from .crowdControlMessageListener import CrowdControlMessageListener
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface


class CrowdControlMessageHandler(CrowdControlMessageListener):

    def __init__(
        self,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def onNewCrowdControlMessage(self, crowdControlMessage: CrowdControlMessage):
        twitchChannelProvider = self.__twitchChannelProvider

        if twitchChannelProvider is None:
            return

        twitchChannel = await twitchChannelProvider.getTwitchChannel(crowdControlMessage.twitchChannel)

        # TODO
        pass

    async def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
