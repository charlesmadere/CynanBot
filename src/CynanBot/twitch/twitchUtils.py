import asyncio
import queue
import traceback
from datetime import datetime, timedelta, timezone, tzinfo
from queue import SimpleQueue
from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.sentMessageLogger.sentMessageLoggerInterface import \
    SentMessageLoggerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchMessageable import TwitchMessageable
from CynanBot.twitch.outboundMessage import OutboundMessage
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface


class TwitchUtils(TwitchUtilsInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        sentMessageLogger: SentMessageLoggerInterface,
        timber: TimberInterface,
        queueTimeoutSeconds: float = 3,
        sleepBeforeRetryTimeSeconds: float = 1,
        sleepTimeSeconds: float = 0.5,
        maxRetries: int = 3,
        timeZone: tzinfo = timezone.utc
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(sentMessageLogger, SentMessageLoggerInterface):
            raise TypeError(f'sentMessageLogger argument is malformed: \"{sentMessageLogger}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')
        elif not utils.isValidNum(sleepBeforeRetryTimeSeconds):
            raise TypeError(f'sleepBeforeRetryTimeSeconds argument is malformed: \"{sleepBeforeRetryTimeSeconds}\"')
        elif sleepBeforeRetryTimeSeconds < 0.25 or sleepBeforeRetryTimeSeconds > 3:
            raise ValueError(f'sleepBeforeRetryTimeSeconds argument is out of bounds: {sleepBeforeRetryTimeSeconds}')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise TypeError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 0.25 or sleepTimeSeconds > 3:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidInt(maxRetries):
            raise TypeError(f'maxRetries argument is malformed: \"{maxRetries}\"')
        elif maxRetries < 0 or maxRetries > utils.getIntMaxSafeSize():
            raise ValueError(f'maxRetries argument is out of bounds: {maxRetries}')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__sentMessageLogger: SentMessageLoggerInterface = sentMessageLogger
        self.__timber: TimberInterface = timber
        self.__queueTimeoutSeconds: float = queueTimeoutSeconds
        self.__sleepBeforeRetryTimeSeconds: float = sleepBeforeRetryTimeSeconds
        self.__sleepTimeSeconds: float = sleepTimeSeconds
        self.__maxRetries: int = maxRetries
        self.__timeZone: tzinfo = timeZone

        self.__isStarted: bool = False
        self.__messageQueue: SimpleQueue[OutboundMessage] = SimpleQueue()

    def getMaxMessageSize(self) -> int:
        return 494

    async def safeSend(
        self,
        messageable: TwitchMessageable,
        message: Optional[str],
        maxMessages: int = 3,
        perMessageMaxSize: int = 494
    ):
        if not isinstance(messageable, TwitchMessageable):
            raise TypeError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidInt(maxMessages):
            raise TypeError(f'maxMessages argument is malformed: \"{maxMessages}\"')
        elif maxMessages < 1 or maxMessages > 5:
            raise ValueError(f'maxMessages is out of bounds: {maxMessages}')
        elif not utils.isValidInt(perMessageMaxSize):
            raise TypeError(f'perMessageMaxSize argument is malformed: \"{perMessageMaxSize}\"')
        elif perMessageMaxSize < 300:
            raise ValueError(f'perMessageMaxSize is too small: {perMessageMaxSize}')
        elif perMessageMaxSize > self.getMaxMessageSize():
            raise ValueError(f'perMessageMaxSize is too big: {perMessageMaxSize} (max size is {self.getMaxMessageSize()})')

        if not utils.isValidStr(message):
            return

        if len(message) < self.getMaxMessageSize():
            await self.__safeSend(
                messageable = messageable,
                message = message
            )
            return

        messages = utils.splitLongStringIntoMessages(
            maxMessages = maxMessages,
            perMessageMaxSize = perMessageMaxSize,
            message = message
        )

        for m in messages:
            await self.__safeSend(
                messageable = messageable,
                message = m
            )

    async def __safeSend(
        self,
        messageable: TwitchMessageable,
        message: str
    ):
        if not isinstance(messageable, TwitchMessageable):
            raise TypeError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        successfullySent = False
        numberOfRetries = 0
        exceptions: Optional[List[Exception]] = None

        while not successfullySent and numberOfRetries < self.__maxRetries:
            try:
                await messageable.send(message)
                successfullySent = True
            except Exception as e:
                self.__timber.log('TwitchUtils', f'Encountered error when trying to send outbound message (twitchChannel={messageable.getTwitchChannelName()}) (retry={numberOfRetries}) (len={len(message)}) \"{message}\": {e}', e, traceback.format_exc())
                numberOfRetries = numberOfRetries + 1

                if exceptions is None:
                    exceptions = list()

                exceptions.append(e)
                await asyncio.sleep(self.__sleepBeforeRetryTimeSeconds)

        self.__sentMessageLogger.log(
            successfullySent = successfullySent,
            numberOfRetries = numberOfRetries,
            exceptions = exceptions,
            msg = message,
            twitchChannel = messageable.getTwitchChannelName()
        )

        if not successfullySent:
            self.__timber.log('TwitchUtils', f'Failed to send message after {numberOfRetries} retries (twitchChannel={messageable.getTwitchChannelName()}) (len={len(message)}) \"{message}\"')

    async def __sendOutboundMessage(self, outboundMessage: OutboundMessage):
        if not isinstance(outboundMessage, OutboundMessage):
            raise TypeError(f'outboundMessage argument is malformed: \"{outboundMessage}\"')

        try:
            self.__messageQueue.put(outboundMessage, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TwitchUtils', f'Encountered queue.Full when submitting a new outbound message ({outboundMessage}) into the outbound message queue (queue size: {self.__messageQueue.qsize()}): {e}', e)

    def start(self):
        if self.__isStarted:
            self.__timber.log('TwitchUtils', 'Not starting TwitchUtils as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TwitchUtils', 'Starting TwitchUtils...')

        self.__backgroundTaskHelper.createTask(self.__startOutboundMessageLoop())

    async def __startOutboundMessageLoop(self):
        while True:
            outboundMessages: List[OutboundMessage] = list()

            try:
                while not self.__messageQueue.empty():
                    outboundMessages.append(self.__messageQueue.get_nowait())
            except queue.Empty as e:
                self.__timber.log('TwitchUtils', f'Encountered queue.Empty when building up Twitch messages list (queue size: {self.__messageQueue.qsize()}) (actions size: {len(outboundMessages)}): {e}', e)

            now = datetime.now(self.__timeZone)

            for outboundMessage in outboundMessages:
                if now >= outboundMessage.getDelayUntilTime():
                    await self.safeSend(
                        messageable = outboundMessage.getMessageable(),
                        message = outboundMessage.getMessage()
                    )
                else:
                    await self.__sendOutboundMessage(outboundMessage)

            await asyncio.sleep(self.__sleepTimeSeconds)

    async def waitThenSend(
        self,
        messageable: TwitchMessageable,
        delaySeconds: int,
        message: str
    ):
        if not isinstance(messageable, TwitchMessageable):
            raise TypeError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidInt(delaySeconds):
            raise TypeError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif delaySeconds < 1 or delaySeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'delaySeconds argument is out of bounds: {delaySeconds}')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        now = datetime.now(self.__timeZone)
        delayUntilTime = now + timedelta(seconds = delaySeconds)

        await self.__sendOutboundMessage(OutboundMessage(
            delayUntilTime = delayUntilTime,
            message = message,
            messageable = messageable
        ))
