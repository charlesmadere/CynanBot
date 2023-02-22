import asyncio
import queue
from datetime import datetime, timedelta, timezone
from queue import SimpleQueue
from typing import List

from twitchio.abcs import Messageable

import CynanBotCommon.utils as utils
from CynanBotCommon.backgroundTaskHelper import BackgroundTaskHelper
from CynanBotCommon.timber.timber import Timber
from twitch.twitchMessage import TwitchMessage


class TwitchUtils():

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        timber: Timber,
        sleepTimeSeconds: float = 0.5,
        maxRetries: int = 3,
        queueTimeoutSeconds: int = 3,
        timeZone: timezone = timezone.utc
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise ValueError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise ValueError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 0.25 or sleepTimeSeconds > 3:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidInt(maxRetries):
            raise ValueError(f'maxRetries argument is malformed: \"{maxRetries}\"')
        elif maxRetries < 0 or maxRetries > utils.getIntMaxSafeSize():
            raise ValueError(f'maxRetries argument is out of bounds: {maxRetries}')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise ValueError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')
        elif not isinstance(timeZone, timezone):
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__timber: Timber = timber
        self.__sleepTimeSeconds: float = sleepTimeSeconds
        self.__maxRetries: int = maxRetries
        self.__queueTimeoutSeconds: int = queueTimeoutSeconds
        self.__timeZone: timezone = timeZone

        self.__messageQueue: SimpleQueue[TwitchMessage] = SimpleQueue()
        backgroundTaskHelper.createTask(self.__startTwitchMessageLoop())

    def getMaxMessageSize(self) -> int:
        return 488

    async def safeSend(
        self,
        messageable: Messageable,
        message: str,
        maxMessages: int = 3,
        perMessageMaxSize: int = 488
    ):
        if not isinstance(messageable, Messageable):
            raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidInt(maxMessages):
            raise ValueError(f'maxMessages argument is malformed: \"{maxMessages}\"')
        elif maxMessages < 1 or maxMessages > 5:
            raise ValueError(f'maxMessages is out of bounds: {maxMessages}')
        elif not utils.isValidInt(perMessageMaxSize):
            raise ValueError(f'perMessageMaxSize argument is malformed: \"{perMessageMaxSize}\"')
        elif perMessageMaxSize < 300:
            raise ValueError(f'perMessageMaxSize is too small: {perMessageMaxSize}')
        elif perMessageMaxSize > self.getMaxMessageSize():
            raise ValueError(f'perMessageMaxSize is too big: {perMessageMaxSize} (max size is {self.getMaxMessageSize()})')

        if not utils.isValidStr(message):
            return

        if len(message) < self.getMaxMessageSize():
            await self.__safeSend(messageable, message)
            return

        messages = utils.splitLongStringIntoMessages(
            maxMessages = maxMessages,
            perMessageMaxSize = perMessageMaxSize,
            message = message
        )

        for m in messages:
            await self.__safeSend(messageable, m)

    async def __safeSend(self, messageable: Messageable, message: str):
        if not isinstance(messageable, Messageable):
            raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        for index in range(self.__maxRetries):
            try:
                await messageable.send(message)
                return
            except Exception as e:
                self.__timber.log('TwitchUtils', f'Encountered error when trying to send message (retry #{index}) (len: {len(message)}) \"{message}\": {e}', e)

        self.__timber.log('TwitchUtils', f'Failed to send message after {self.__maxRetries} retries (len: {len(message)} \"{message}\"')

    async def __startTwitchMessageLoop(self):
        while True:
            twitchMessages: List[TwitchMessage] = list()

            try:
                while not self.__messageQueue.empty():
                    twitchMessages.append(self.__messageQueue.get_nowait())
            except queue.Empty as e:
                self.__timber.log('TwitchUtils', f'Encountered queue.Empty when building up Twitch messages list (queue size: {self.__messageQueue.qsize()}) (actions size: {len(twitchMessages)}): {e}', e)

            now = datetime.now(self.__timeZone)

            for twitchMessage in twitchMessages:
                if now >= twitchMessage.getDelayUntilTime():
                    await self.safeSend(
                        messageable = twitchMessage.getMessageable(),
                        message = twitchMessage.getMessage()
                    )
                else:
                    await self.__submitTwitchMessage(twitchMessage)

            await asyncio.sleep(self.__sleepTimeSeconds)

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

        now = datetime.now(self.__timeZone)
        delayUntilTime = now + timedelta(seconds = delaySeconds)

        await self.__submitTwitchMessage(TwitchMessage(
            delayUntilTime = delayUntilTime,
            messageable = messageable,
            message = message,
            twitchChannel = twitchChannel
        ))
