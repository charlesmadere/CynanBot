import asyncio
import queue
import traceback
from collections import defaultdict
from queue import SimpleQueue
from typing import Final

import aiofiles
import aiofiles.os
import aiofiles.ospath
from frozenlist import FrozenList

from .chatLoggerInterface import ChatLoggerInterface
from .models.absChatLog import AbsChatLog
from .models.cheerChatLog import CheerChatLog
from .models.messageChatLog import MessageChatLog
from .models.raidChatLog import RaidChatLog
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
        sleepTimeSeconds: float = 8,
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
        self.__chatLogQueue: Final[SimpleQueue[AbsChatLog]] = SimpleQueue()

    def __getLogStatement(self, chatLog: AbsChatLog) -> str:
        if not isinstance(chatLog, AbsChatLog):
            raise TypeError(f'chatLog argument is malformed: \"{chatLog}\"')

        logStatement = f'{chatLog.getDateTime().getDateAndTimeStr(True)} —'

        if isinstance(chatLog, CheerChatLog):
            logStatement = f'{logStatement} {chatLog.cheerUserLogin} ({chatLog.cheerUserId}) cheered {chatLog.bitsStr} bit(s)'

        elif isinstance(chatLog, MessageChatLog):
            logStatement = f'{logStatement} {chatLog.chatterUserLogin} ({chatLog.chatterUserId}) — {chatLog.message}'

        elif isinstance(chatLog, RaidChatLog):
            logStatement = f'{logStatement} {chatLog.raidUserLogin} ({chatLog.raidUserId}) raided with {chatLog.viewersStr} viewer(s)'

        else:
            raise RuntimeError(f'AbsChatLog is of an unknown type ({chatLog=})')

        return f'{logStatement.strip()}\n'

    def logCheer(
        self,
        bits: int,
        cheerUserId: str,
        cheerUserLogin: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is malformed: {bits}')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserLogin):
            raise TypeError(f'cheerUserLogin argument is malformed: \"{cheerUserLogin}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        dateTime = SimpleDateTime(
            timeZone = self.__timeZoneRepository.getDefault(),
        )

        self.__chatLogQueue.put(CheerChatLog(
            bits = bits,
            dateTime = dateTime,
            cheerUserId = cheerUserId,
            cheerUserLogin = cheerUserLogin,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        ))

    def logMessage(
        self,
        bits: int | None,
        chatterUserId: str,
        chatterUserLogin: str,
        message: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        if bits is not None and not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits is not None and (bits < 0 or bits > utils.getIntMaxSafeSize()):
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(chatterUserLogin):
            raise TypeError(f'chatterUserLogin argument is malformed: \"{chatterUserLogin}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        dateTime = SimpleDateTime(
            timeZone = self.__timeZoneRepository.getDefault(),
        )

        self.__chatLogQueue.put(MessageChatLog(
            bits = bits,
            dateTime = dateTime,
            chatterUserId = chatterUserId,
            chatterUserLogin = chatterUserLogin,
            message = message,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        ))

    def logRaid(
        self,
        viewers: int,
        raidUserId: str,
        raidUserLogin: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        if not utils.isValidInt(viewers):
            raise TypeError(f'raidSize argument is malformed: \"{viewers}\"')
        elif viewers < 0 or viewers > utils.getIntMaxSafeSize():
            raise ValueError(f'viewers argument is out of bounds: {viewers}')
        elif not utils.isValidStr(raidUserId):
            raise TypeError(f'raidUserId argument is malformed: \"{raidUserId}\"')
        elif not utils.isValidStr(raidUserLogin):
            raise TypeError(f'raidUserLogin argument is malformed: \"{raidUserLogin}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        dateTime = SimpleDateTime(
            timeZone = self.__timeZoneRepository.getDefault(),
        )

        self.__chatLogQueue.put(RaidChatLog(
            viewers = viewers,
            dateTime = dateTime,
            raidUserId = raidUserId,
            raidUserLogin = raidUserLogin,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        ))

    def start(self):
        if self.__isStarted:
            self.__timber.log('ChatLogger', 'Not starting ChatLogger as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('ChatLogger', 'Starting ChatLogger...')
        self.__backgroundTaskHelper.createTask(self.__startChatLogLoop())

    async def __startChatLogLoop(self):
        while True:
            chatLogs: FrozenList[AbsChatLog] = FrozenList()

            try:
                while not self.__chatLogQueue.empty():
                    chatLog = self.__chatLogQueue.get_nowait()
                    chatLogs.append(chatLog)
            except queue.Empty as e:
                self.__timber.log('ChatLogger', f'Encountered queue.Empty when building up chatLogs list (queue size: {self.__chatLogQueue.qsize()}) (chatLogs size: {len(chatLogs)}): {e}', e, traceback.format_exc())

            chatLogs.freeze()
            await self.__writeToLogFiles(chatLogs)
            await asyncio.sleep(self.__sleepTimeSeconds)

    async def __writeToLogFiles(self, chatLogs: FrozenList[AbsChatLog]):
        if len(chatLogs) == 0:
            return

        # The below logic is kind of intense, however, there is a very similar/nearly identical
        # flow within the Timber class. Check that out for more information and context.

        structure: dict[str, dict[str, list[AbsChatLog]]] = defaultdict(lambda: defaultdict(lambda: list()))

        for chatLog in chatLogs:
            twitchChannel = chatLog.getTwitchChannel().lower()
            dateTime = chatLog.getDateTime()
            chatLogDirectory = f'{self.__logRootDirectory}/{twitchChannel}/{dateTime.getYearStr()}/{dateTime.getMonthStr()}'
            chatLogFile = f'{chatLogDirectory}/{dateTime.getDayStr()}.log'
            structure[chatLogDirectory][chatLogFile].append(chatLog)

        for chatLogDirectory, chatLogFileToChatLogsDict in structure.items():
            if not await aiofiles.ospath.exists(
                path = chatLogDirectory,
                loop = self.__backgroundTaskHelper.eventLoop,
            ):
                await aiofiles.os.makedirs(
                    name = chatLogDirectory,
                    loop = self.__backgroundTaskHelper.eventLoop,
                )

            for chatLogFile, chatLogList in chatLogFileToChatLogsDict.items():
                async with aiofiles.open(
                    file = chatLogFile,
                    mode = 'a',
                    encoding = 'utf-8',
                    loop = self.__backgroundTaskHelper.eventLoop,
                ) as file:
                    for chatLog in chatLogList:
                        logStatement = self.__getLogStatement(chatLog)
                        await file.write(logStatement)

                    await file.flush()
