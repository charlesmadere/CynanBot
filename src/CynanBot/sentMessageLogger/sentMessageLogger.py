import asyncio
import queue
from collections import defaultdict
from queue import SimpleQueue
from typing import Dict, List, Optional

import aiofiles
import aiofiles.os
import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.sentMessageLogger.sentMessage import SentMessage
from CynanBot.sentMessageLogger.sentMessageLoggerInterface import \
    SentMessageLoggerInterface
from CynanBot.timber.timberInterface import TimberInterface


class SentMessageLogger(SentMessageLoggerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        timber: TimberInterface,
        sleepTimeSeconds: float = 15,
        logRootDirectory: str = 'logs/sentMessageLogger'
    ):
        assert isinstance(backgroundTaskHelper, BackgroundTaskHelper), f"malformed {backgroundTaskHelper=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        if not utils.isValidNum(sleepTimeSeconds):
            raise ValueError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        if sleepTimeSeconds < 1 or sleepTimeSeconds > 60:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        if not utils.isValidStr(logRootDirectory):
            raise ValueError(f'logRootDirectory argument is malformed: \"{logRootDirectory}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__timber: TimberInterface = timber
        self.__sleepTimeSeconds: float = sleepTimeSeconds
        self.__logRootDirectory: str = logRootDirectory

        self.__isStarted: bool = False
        self.__messageQueue: SimpleQueue[SentMessage] = SimpleQueue()

    def __getLogStatement(self, message: SentMessage) -> str:
        assert isinstance(message, SentMessage), f"malformed {message=}"

        prefix = f'{message.getSimpleDateTime().getDateAndTimeStr(True)} — '
        error = ''

        if not message.wasSuccessfullySent():
            error = f'message failed to send after {message.getNumberOfRetries()} attempt(s) — '
        elif message.getNumberOfRetries() >= 1:
            error = f'message was sent, but it required {message.getNumberOfRetries()} attempt(s) — '

        suffix = f'{message.getMsg()}'

        logStatement = f'{prefix}{error}{suffix}'.strip()
        return f'{logStatement}\n'

    def log(
        self,
        successfullySent: bool,
        numberOfRetries: int,
        exceptions: Optional[List[Exception]],
        msg: str,
        twitchChannel: str
    ):
        if not utils.isValidBool(successfullySent):
            raise ValueError(f'successfullySent argument is malformed: \"{successfullySent}\"')
        if not utils.isValidInt(numberOfRetries):
            raise ValueError(f'numberOfRetries argument is malformed: \"{numberOfRetries}\"')
        if not utils.isValidStr(msg):
            raise ValueError(f'msg argument is malformed: \"{msg}\"')
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        sentMessage = SentMessage(
            successfullySent = successfullySent,
            numberOfRetries = numberOfRetries,
            exceptions = exceptions,
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
            messages: List[SentMessage] = list()

            try:
                while not self.__messageQueue.empty():
                    message = self.__messageQueue.get_nowait()
                    messages.append(message)
            except queue.Empty:
                pass

            await self.__writeToLogFiles(messages)
            await asyncio.sleep(self.__sleepTimeSeconds)

    async def __writeToLogFiles(self, messages: List[SentMessage]):
        if len(messages) == 0:
            return

        # The below logic is kind of intense, however, there is a very similar/nearly identical
        # flow within the Timber class. Check that out for more information and context.

        structure: Dict[str, Dict[str, List[SentMessage]]] = defaultdict(lambda: defaultdict(lambda: list()))

        for message in messages:
            twitchChannel = message.getTwitchChannel().lower()
            simpleDateTime = message.getSimpleDateTime()
            messageDirectory = f'{self.__logRootDirectory}/{twitchChannel}/{simpleDateTime.getYearStr()}/{simpleDateTime.getMonthStr()}'
            messageFile = f'{messageDirectory}/{simpleDateTime.getDayStr()}.log'
            structure[messageDirectory][messageFile].append(message)

        for messageDirectory, messageFileToMessagesDict in structure.items():
            if not await aiofiles.ospath.exists(messageDirectory):
                await aiofiles.os.makedirs(messageDirectory)

            for messageFile, messagesList in messageFileToMessagesDict.items():
                async with aiofiles.open(messageFile, mode = 'a', encoding = 'utf-8') as file:
                    for message in messagesList:
                        logStatement = self.__getLogStatement(message)
                        await file.write(logStatement)
