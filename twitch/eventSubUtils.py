from asyncio import AbstractEventLoop

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timber import Timber
from twitchio import Client
from twitchio.ext.eventsub import EventSubClient


class EventSubUtils():

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        client: Client,
        port: int,
        webhookSecret: str,
        timber: Timber,
        callbackRoute: str = '/callback'
    ):
        if eventLoop is None:
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif client is None:
            raise ValueError(f'client argument is malformed: \"{client}\"')
        elif not utils.isValidNum(port):
            raise ValueError(f'port argument is malformed: \"{port}\"')
        elif port <= 100:
            raise ValueError(f'port argument is out of bounds: {port}')
        elif not utils.isValidStr(webhookSecret):
            raise ValueError(f'webhookSecret argument is malformed: \"{webhookSecret}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(callbackRoute):
            raise ValueError(f'callbackRoute argument is malformed: \"{callbackRoute}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__port: int = port
        self.__timber: Timber = timber

        self.__isStarted: bool = False
        self.__eventSubClient: EventSubClient = EventSubClient(
            client = client,
            webhook_secret = webhookSecret,
            callback_route = callbackRoute
        )

    async def startEventSub(self):
        if self.__isStarted:
            self.__timber.log('EventSubUtils', 'Not starting EventSub as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('EventSubUtils', f'Starting EventSub...')

        # TODO
        pass
