import asyncio
import queue
from collections import defaultdict
from queue import SimpleQueue
from typing import Dict, List

import aiofiles
import aiofiles.os
import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.chatLogger.absChatMessage import AbsChatMessage
from CynanBot.chatLogger.chatEventType import ChatEventType
from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.chatLogger.chatMessage import ChatMessage
from CynanBot.chatLogger.raidMessage import RaidMessage
from CynanBot.timber.timberInterface import TimberInterface


class ChatLogger(ChatLoggerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        timber: TimberInterface,
        sleepTimeSeconds: float = 15,
        logRootDirectory: str = 'logs/chatLogger'
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
        self.__messageQueue: SimpleQueue[AbsChatMessage] = SimpleQueue()

    def __getLogStatement(self, message: AbsChatMessage) -> str:
        assert isinstance(message, AbsChatMessage), f"malformed {message=}"

        logStatement: str = f'{message.getSimpleDateTime().getDateAndTimeStr(True)} —'

        if message.getChatEventType() is ChatEventType.MESSAGE:
            chatMessage: ChatMessage = message
            logStatement = f'{logStatement} {chatMessage.getUserName()} ({chatMessage.getUserId()}) — {chatMessage.getMsg()}'
        elif message.getChatEventType() is ChatEventType.RAID:
            raidMessage: RaidMessage = message
            logStatement = f'{logStatement} Received raid from {raidMessage.getFromWho()} of {raidMessage.getRaidSizeStr()}!'
        else:
            raise RuntimeError(f'AbsChatMessage has unknown ChatEventType: \"{message.getChatEventType()}\"')

        return f'{logStatement.strip()}\n'

    def logMessage(self, msg: str, twitchChannel: str, userId: str, userName: str):
        if not utils.isValidStr(msg):
            raise ValueError(f'msg argument is malformed: \"{msg}\"')
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        chatMessage: AbsChatMessage = ChatMessage(
            msg = msg,
            twitchChannel = twitchChannel,
            userId = userId,
            userName = userName
        )

        self.__messageQueue.put(chatMessage)

    def logRaid(self, raidSize: int, fromWho: str, twitchChannel: str):
        if not utils.isValidInt(raidSize):
            raise ValueError(f'raidSize argument is malformed: \"{raidSize}\"')
        if raidSize < 0 or raidSize > utils.getIntMaxSafeSize():
            raise ValueError(f'raidSize argument is out of bounds: {raidSize}')
        if not utils.isValidStr(fromWho):
            raise ValueError(f'fromWho argument is malformed: \"{fromWho}\"')
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        raidMessage: AbsChatMessage = RaidMessage(
            raidSize = raidSize,
            fromWho = fromWho,
            twitchChannel = twitchChannel
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
            messages: List[AbsChatMessage] = list()

            try:
                while not self.__messageQueue.empty():
                    message = self.__messageQueue.get_nowait()
                    messages.append(message)
            except queue.Empty:
                pass

            await self.__writeToLogFiles(messages)
            await asyncio.sleep(self.__sleepTimeSeconds)

    async def __writeToLogFiles(self, messages: List[AbsChatMessage]):
        if len(messages) == 0:
            return

        # The below logic is kind of intense, however, there is a very similar/nearly identical
        # flow within the Timber class. Check that out for more information and context.

        structure: Dict[str, Dict[str, List[AbsChatMessage]]] = defaultdict(lambda: defaultdict(lambda: list()))

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
