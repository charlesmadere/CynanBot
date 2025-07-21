import asyncio
import queue
import traceback
from collections import defaultdict
from queue import SimpleQueue
from typing import Final

import aiofiles
import aiofiles.os
import aiofiles.ospath

from .absChatMessage import AbsChatMessage
from .chatLoggerInterface import ChatLoggerInterface
from .chatMessage import ChatMessage
from .cheerMessage import CheerMessage
from .raidMessage import RaidMessage
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..misc.simpleDateTime import SimpleDateTime
from ..timber.timberInterface import TimberInterface


class ChatLogger(ChatLoggerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        sleepTimeSeconds: float = 15,
        logRootDirectory: str = '../logs/chatLogger',
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
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
        self.__messageQueue: Final[SimpleQueue[AbsChatMessage]] = SimpleQueue()

    def __getLogStatement(self, message: AbsChatMessage) -> str:
        if not isinstance(message, AbsChatMessage):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        logStatement = f'{message.dateTime.getDateAndTimeStr(True)} —'

        if isinstance(message, ChatMessage):
            logStatement = f'{logStatement} {message.userName} ({message.userId}) — {message.msg}'

        elif isinstance(message, CheerMessage):
            logStatement = f'{logStatement} {message.userName} ({message.userId}) cheered {message.bitsStr} bit(s)'

        elif isinstance(message, RaidMessage):
            logStatement = f'{logStatement} Received raid from {message.fromWho} of {message.raidSizeStr}!'

        else:
            raise RuntimeError(f'AbsChatMessage is of an unknown type ({message=})')

        return f'{logStatement.strip()}\n'

    def logCheer(
        self,
        bits: int,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str,
    ):
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is malformed: {bits}')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        cheerMessage: AbsChatMessage = CheerMessage(
            bits = bits,
            dateTime = SimpleDateTime(timeZone = self.__timeZoneRepository.getDefault()),
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            userId = userId,
            userName = userName,
        )

        self.__messageQueue.put(cheerMessage)

    def logMessage(
        self,
        msg: str,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str,
    ):
        if not utils.isValidStr(msg):
            raise TypeError(f'msg argument is malformed: \"{msg}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        chatMessage: AbsChatMessage = ChatMessage(
            dateTime = SimpleDateTime(timeZone = self.__timeZoneRepository.getDefault()),
            msg = msg,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            userId = userId,
            userName = userName,
        )

        self.__messageQueue.put(chatMessage)

    def logRaid(
        self,
        raidSize: int,
        fromWho: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        if not utils.isValidInt(raidSize):
            raise TypeError(f'raidSize argument is malformed: \"{raidSize}\"')
        elif raidSize < 0 or raidSize > utils.getIntMaxSafeSize():
            raise ValueError(f'raidSize argument is out of bounds: {raidSize}')
        elif not utils.isValidStr(fromWho):
            raise TypeError(f'fromWho argument is malformed: \"{fromWho}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        raidMessage: AbsChatMessage = RaidMessage(
            raidSize = raidSize,
            dateTime = SimpleDateTime(timeZone = self.__timeZoneRepository.getDefault()),
            fromWho = fromWho,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__messageQueue.put(raidMessage)

    def start(self):
        if self.__isStarted:
            self.__timber.log('ChatLogger', 'Not starting ChatLogger as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('ChatLogger', 'Starting ChatLogger...')
        self.__backgroundTaskHelper.createTask(self.__startMessageLoop())

    async def __startMessageLoop(self):
        while True:
            messages: list[AbsChatMessage] = list()

            try:
                while not self.__messageQueue.empty():
                    message = self.__messageQueue.get_nowait()
                    messages.append(message)
            except queue.Empty as e:
                self.__timber.log('ChatLogger', f'Encountered queue.Empty when building up messages list (queue size: {self.__messageQueue.qsize()}) (messages size: {len(messages)}): {e}', e, traceback.format_exc())

            await self.__writeToLogFiles(messages)
            await asyncio.sleep(self.__sleepTimeSeconds)

    async def __writeToLogFiles(self, messages: list[AbsChatMessage]):
        if len(messages) == 0:
            return

        # The below logic is kind of intense, however, there is a very similar/nearly identical
        # flow within the Timber class. Check that out for more information and context.

        structure: dict[str, dict[str, list[AbsChatMessage]]] = defaultdict(lambda: defaultdict(lambda: list()))

        for message in messages:
            twitchChannel = message.twitchChannel.lower()
            dateTime = message.dateTime
            messageDirectory = f'{self.__logRootDirectory}/{twitchChannel}/{dateTime.getYearStr()}/{dateTime.getMonthStr()}'
            messageFile = f'{messageDirectory}/{dateTime.getDayStr()}.log'
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
