import asyncio
import queue
from asyncio import AbstractEventLoop
from datetime import datetime, timedelta, timezone
from queue import SimpleQueue
from typing import List

from twitchio.abcs import Messageable

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timber import Timber
from twitch.twitchMessage import TwitchMessage


class TwitchUtils():

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        timber: Timber,
        sleepTimeSeconds: float = 0.5,
        queueTimeoutSeconds: int = 3
    ):
        if eventLoop is None:
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise ValueError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 0.25 or sleepTimeSeconds > 2:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise ValueError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__timber: Timber = timber
        self.__sleepTimeSeconds: float = sleepTimeSeconds
        self.__queueTimeoutSeconds: int = queueTimeoutSeconds

        self.__messageQueue: SimpleQueue[TwitchMessage] = SimpleQueue()
        eventLoop.create_task(self.__startTwitchMessageLoop())

    def getMaxMessageSize() -> int:
        return 500

    async def safeSend(
        self,
        messageable: Messageable,
        message: str,
        perMessageMaxSize: int = 475,
        maxMessages: int = 3
    ):
        if messageable is None:
            raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidNum(perMessageMaxSize):
            raise ValueError(f'perMessageMaxSize argument is malformed: \"{perMessageMaxSize}\"')
        elif perMessageMaxSize < 300:
            raise ValueError(f'perMessageMaxSize is too small: {perMessageMaxSize}')
        elif perMessageMaxSize >= self.getMaxMessageSize():
            raise ValueError(f'perMessageMaxSize is too big: {perMessageMaxSize} (max size is {self.getMaxMessageSize()})')
        elif not utils.isValidNum(maxMessages):
            raise ValueError(f'maxMessages argument is malformed: \"{maxMessages}\"')
        elif maxMessages < 1 or maxMessages > 5:
            raise ValueError(f'maxMessages is out of bounds: {maxMessages}')

        if not utils.isValidStr(message):
            return

        if len(message) < self.getMaxMessageSize():
            await messageable.send(message)
            return

        messages: List[str] = list()
        messages.append(message)

        index: int = 0

        while index < len(messages):
            m: str = messages[index]

            if len(m) >= self.getMaxMessageSize():
                spaceIndex = m.rfind(' ')

                while spaceIndex >= perMessageMaxSize:
                    spaceIndex = m[0:spaceIndex].rfind(' ')

                if spaceIndex == -1:
                    raise RuntimeError(f'This message is insane and can\'t be sent (len is {len(message)}):\n{message}')

                messages[index] = m[0:spaceIndex].strip()
                messages.append(m[spaceIndex:len(m)].strip())

            index = index + 1

        if len(messages) > maxMessages:
            raise RuntimeError(f'This message is too long and won\'t be sent (len is {len(message)}):\n{message}')

        for m in messages:
            try:
                await messageable.send(m)
            except Exception as e:
                self.__timber.log('TwitchUtils', f'Encountered error when trying to send message \"{m}\": {e}', e)

    async def __startTwitchMessageLoop(self):
        while True:
            twitchMessages: List[TwitchMessage] = list()

            try:
                while not self.__messageQueue.empty():
                    twitchMessages.append(self.__messageQueue.get_nowait())
            except queue.Empty as e:
                self.__timber.log('TwitchUtils', f'Encountered queue.Empty when building up Twitch messages list (queue size: {self.__messageQueue.qsize()}) (actions size: {len(twitchMessages)}): {e}', e)

            now = datetime.now(timezone.utc)

            for twitchMessage in twitchMessages:
                if now >= twitchMessage.getDelayUntilTime():
                    await self.safeSend(
                        messageable = twitchMessage.getMessageable(),
                        message = twitchMessage.getMessage()
                    )
                else:
                    await self.__submitTwitchMessage(twitchMessage)

            asyncio.sleep(self.__sleepTimeSeconds)

    async def __submitTwitchMessage(self, twitchMessage: TwitchMessage):
        if not isinstance(twitchMessage, TwitchMessage):
            raise ValueError(f'twitchMessage argument is malformed: \"{twitchMessage}\"')

        try:
            self.__messageQueue.put(twitchMessage, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TwitchUtils', f'Encountered queue.Full when submitting a new Twitch Message ({twitchMessage}) into the message queue (queue size: {self.__messageQueue.qsize()}): {e}', e)

    async def waitThenSend(
        self,
        messageable: Messageable,
        delaySeconds: int,
        message: str,
        twitchChannel: str
    ):
        if not isinstance(messageable, Messageable):
            raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidInt(delaySeconds):
            raise ValueError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif delaySeconds < 1 or delaySeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'delaySeconds argument is out of bounds: {delaySeconds}')
        elif not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        now = datetime.now(timezone.utc)
        delayUntilTime = now + timedelta(seconds = delaySeconds)

        await self.__submitTwitchMessage(TwitchMessage(
            delayUntilTime = delayUntilTime,
            messageable = messageable,
            message = message,
            twitchChannel = twitchChannel
        ))
