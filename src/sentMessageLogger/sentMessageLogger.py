import asyncio
import queue
import traceback
from collections import defaultdict
from queue import SimpleQueue
from typing import Collection, Final

import aiofiles
import aiofiles.os
import aiofiles.ospath
from frozenlist import FrozenList

from .messageMethod import MessageMethod
from .sentMessage import SentMessage
from .sentMessageLoggerInterface import SentMessageLoggerInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..misc.simpleDateTime import SimpleDateTime
from ..timber.timberInterface import TimberInterface


class SentMessageLogger(SentMessageLoggerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        sleepTimeSeconds: float = 15,
        logRootDirectory: str = '../logs/sentMessageLogger'
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise TypeError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 1 or sleepTimeSeconds > 60:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidStr(logRootDirectory):
            raise TypeError(f'logRootDirectory argument is malformed: \"{logRootDirectory}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__sleepTimeSeconds: Final[float] = sleepTimeSeconds
        self.__logRootDirectory: Final[str] = logRootDirectory

        self.__isStarted: bool = False
        self.__messageQueue: Final[SimpleQueue[SentMessage]] = SimpleQueue()

    def __getLogStatement(self, message: SentMessage) -> str:
        if not isinstance(message, SentMessage):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        prefix = f'{message.sendTime.getDateAndTimeStr(True)} — {message.messageMethod.toStr()} — '

        error = ''
        if not message.successfullySent:
            error = f'(failed to send after {message.numberOfSendAttempts} attempt(s)) — '
        elif message.numberOfSendAttempts > 1:
            error = f'(successfully sent after {message.numberOfSendAttempts} attempt(s)) — '

        logStatement = f'{prefix}{error}{message.msg}'.strip()
        return f'{logStatement}\n'

    def log(
        self,
        successfullySent: bool,
        exceptions: Collection[Exception] | None,
        numberOfSendAttempts: int,
        messageMethod: MessageMethod,
        msg: str,
        twitchChannel: str
    ):
        if not utils.isValidBool(successfullySent):
            raise TypeError(f'successfullySent argument is malformed: \"{successfullySent}\"')
        elif exceptions is not None and not isinstance(exceptions, Collection):
            raise TypeError(f'exceptions argument is malformed: \"{exceptions}\"')
        elif not utils.isValidInt(numberOfSendAttempts):
            raise TypeError(f'numberOfSendAttempts argument is malformed: \"{numberOfSendAttempts}\"')
        elif numberOfSendAttempts < 1 or numberOfSendAttempts > utils.getIntMaxSafeSize():
            raise ValueError(f'numberOfSendAttempts argument is out of bounds: {numberOfSendAttempts}')
        elif not isinstance(messageMethod, MessageMethod):
            raise TypeError(f'messageMethod argument is malformed: \"{messageMethod}\"')
        elif not utils.isValidStr(msg):
            raise TypeError(f'msg argument is malformed: \"{msg}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        frozenExceptions: FrozenList[Exception] | None = None

        if exceptions is not None:
            frozenExceptions = FrozenList(exceptions)
            frozenExceptions.freeze()

        sendTime = SimpleDateTime(
            timeZone = self.__timeZoneRepository.getDefault()
        )

        sentMessage = SentMessage(
            successfullySent = successfullySent,
            exceptions = frozenExceptions,
            numberOfSendAttempts = numberOfSendAttempts,
            messageMethod = messageMethod,
            sendTime = sendTime,
            msg = msg,
            twitchChannel = twitchChannel
        )

        self.__messageQueue.put(sentMessage)

    def start(self):
        if self.__isStarted:
            self.__timber.log('SentMessageLogger', 'Not starting SentMessageLogger as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('SentMessageLogger', 'Starting SentMessageLogger...')
        self.__backgroundTaskHelper.createTask(self.__startMessageLoop())

    async def __startMessageLoop(self):
        while True:
            messages: list[SentMessage] = list()

            try:
                while not self.__messageQueue.empty():
                    message = self.__messageQueue.get_nowait()
                    messages.append(message)
            except queue.Empty as e:
                self.__timber.log('SentMessageLogger', f'Encountered queue.Empty when building up messages list (queue size: {self.__messageQueue.qsize()}) (messages size: {len(messages)}): {e}', e, traceback.format_exc())

            await self.__writeToLogFiles(messages)
            await asyncio.sleep(self.__sleepTimeSeconds)

    async def __writeToLogFiles(self, messages: list[SentMessage]):
        if len(messages) == 0:
            return

        # The below logic is kind of intense, however, there is a very similar/nearly identical
        # flow within the Timber class. Check that out for more information and context.

        structure: dict[str, dict[str, list[SentMessage]]] = defaultdict(lambda: defaultdict(lambda: list()))

        for message in messages:
            twitchChannel = message.twitchChannel.lower()
            sendTime = message.sendTime
            messageDirectory = f'{self.__logRootDirectory}/{twitchChannel}/{sendTime.getYearStr()}/{sendTime.getMonthStr()}'
            messageFile = f'{messageDirectory}/{sendTime.getDayStr()}.log'
            structure[messageDirectory][messageFile].append(message)

        for messageDirectory, messageFileToMessagesDict in structure.items():
            if not await aiofiles.ospath.exists(
                path = messageDirectory,
                loop = self.__backgroundTaskHelper.eventLoop
            ):
                await aiofiles.os.makedirs(
                    name = messageDirectory,
                    loop = self.__backgroundTaskHelper.eventLoop
                )

            for messageFile, messagesList in messageFileToMessagesDict.items():
                async with aiofiles.open(
                    file = messageFile,
                    mode = 'a',
                    encoding = 'utf-8',
                    loop = self.__backgroundTaskHelper.eventLoop
                ) as file:
                    for message in messagesList:
                        logStatement = self.__getLogStatement(message)
                        await file.write(logStatement)

                    await file.flush()
