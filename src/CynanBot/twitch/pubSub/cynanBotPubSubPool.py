from typing import List

from twitchio import Client
from twitchio.ext.pubsub import PubSubPool
from twitchio.ext.pubsub.topics import Topic
from twitchio.ext.pubsub.websocket import PubSubWebsocket

from CynanBotCommon.timber.timberInterface import TimberInterface
from twitch.pubSub.pubSubReconnectListener import PubSubReconnectListener


class CynanBotPubSubPool(PubSubPool):

    def __init__(
        self,
        client: Client,
        maxConnectionTopics: int,
        maxPoolSize: int,
        pubSubReconnectListener: PubSubReconnectListener,
        timber: TimberInterface
    ):
        super().__init__(
            client = client,
            max_connection_topics = maxConnectionTopics,
            max_pool_size = maxPoolSize
        )

        if not isinstance(pubSubReconnectListener, PubSubReconnectListener):
            raise ValueError(f'pubSubReconnectListener argument is malformed: \"{pubSubReconnectListener}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__pubSubReconnectListener: PubSubReconnectListener = pubSubReconnectListener
        self.__timber: TimberInterface = timber

    async def auth_fail_hook(self, topics: List[Topic]):
        self.__timber.log('CynanBotPubSubPool', f'auth_fail_hook(): (topics=\"{topics}\")')
        return await super().auth_fail_hook(topics)

    async def reconnect_hook(
        self,
        node: PubSubWebsocket,
        topics: List[Topic]
    ) -> List[Topic]:
        self.__timber.log('CynanBotPubSubPool', f'reconnect_hook(): (node=\"{node}\") (topics=\"{topics}\")')
        return await self.__pubSubReconnectListener.onPubSubReconnect(topics)
