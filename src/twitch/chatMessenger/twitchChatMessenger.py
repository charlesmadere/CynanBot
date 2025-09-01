import asyncio
import queue
import traceback
from datetime import datetime, timedelta
from queue import SimpleQueue
from typing import Final

from frozenlist import FrozenList

from .chatMessage import ChatMessage
from .twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..api.models.twitchSendChatMessageRequest import TwitchSendChatMessageRequest
from ..api.models.twitchSendChatMessageResponse import TwitchSendChatMessageResponse
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..globalTwitchConstants import GlobalTwitchConstants
from ..tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...sentMessageLogger.messageMethod import MessageMethod
from ...sentMessageLogger.sentMessageLoggerInterface import SentMessageLoggerInterface
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TwitchChatMessenger(TwitchChatMessengerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        globalTwitchConstants: GlobalTwitchConstants,
        sentMessageLogger: SentMessageLoggerInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        sleepTimeSeconds: float = 0.125,
        maxMessageSplits: int = 3,
        queueTimeoutSeconds: int = 3,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(globalTwitchConstants, GlobalTwitchConstants):
            raise TypeError(f'globalTwitchConstants argument is malformed: \"{globalTwitchConstants}\"')
        elif not isinstance(sentMessageLogger, SentMessageLoggerInterface):
            raise TypeError(f'sentMessageLogger argument is malformed: \"{sentMessageLogger}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise TypeError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 0.125 or sleepTimeSeconds > 3:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidInt(maxMessageSplits):
            raise TypeError(f'maxMessageSplits argument is malformed: \"{maxMessageSplits}\"')
        elif maxMessageSplits < 0 or maxMessageSplits > 5:
            raise ValueError(f'maxMessageSplits argument is out of bounds: {maxMessageSplits}')
        elif not utils.isValidInt(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__globalTwitchConstants: Final[GlobalTwitchConstants] = globalTwitchConstants
        self.__sentMessageLogger: Final[SentMessageLoggerInterface] = sentMessageLogger
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__sleepTimeSeconds: Final[float] = sleepTimeSeconds
        self.__maxMessageSplits: Final[int] = maxMessageSplits
        self.__queueTimeoutSeconds: Final[int] = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__messageQueue: Final[SimpleQueue[ChatMessage]] = SimpleQueue()
        self.__selfTwitchUserId: str | None = None

    async def __getSelfTwitchAccessToken(self) -> str:
        selfTwitchUserId = await self.__getSelfTwitchUserId()

        return await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = selfTwitchUserId,
        )

    async def __getSelfTwitchUserId(self) -> str:
        selfTwitchUserId = self.__selfTwitchUserId

        if selfTwitchUserId is None:
            twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
            selfTwitchUserId = await self.__userIdsRepository.requireUserId(twitchHandle)
            self.__selfTwitchUserId = selfTwitchUserId

        return selfTwitchUserId

    async def __handleChatMessage(self, chatMessage: ChatMessage):
        if not isinstance(chatMessage, ChatMessage):
            raise TypeError(f'chatMessage argument is malformed: \"{chatMessage}\"')

        if chatMessage.sendAfter is None:
            await self.__sendChatMessage(chatMessage)
            return

        now = datetime.now(self.__timeZoneRepository.getDefault())

        if now < chatMessage.sendAfter:
            self.__submitChatMessage(chatMessage)
        else:
            await self.__sendChatMessage(chatMessage)

    async def __prepareChatMessageTexts(
        self,
        chatMessage: ChatMessage,
    ) -> FrozenList[str]:
        texts: FrozenList[str] = FrozenList()

        if len(chatMessage.text) < self.__globalTwitchConstants.maxMessageSize:
            texts.append(chatMessage.text)
        else:
            splits = utils.splitLongStringIntoMessages(
                maxMessages = self.__maxMessageSplits,
                perMessageMaxSize = self.__globalTwitchConstants.maxMessageSize,
                message = chatMessage.text,
            )

            texts.extend(splits)

        texts.freeze()
        return texts

    def send(
        self,
        text: str,
        twitchChannelId: str,
        delaySeconds: int | None = None,
        replyMessageId: str | None = None,
    ):
        if not isinstance(text, str):
            raise TypeError(f'text argument is malformed: \"{text}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif delaySeconds is not None and (not utils.isValidInt(delaySeconds) or delaySeconds < 1):
            raise TypeError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif replyMessageId is not None and not isinstance(replyMessageId, str):
            raise TypeError(f'replyMessageId argument is malformed: \"{replyMessageId}\"')

        cleanedText = utils.cleanStr(text)

        if not utils.isValidStr(cleanedText):
            self.__timber.log('TwitchChatMessenger', f'Encountered blank chat message ({cleanedText=}) ({text=}) ({twitchChannelId=}) ({delaySeconds=}) ({replyMessageId=})')
            return

        sendAfter: datetime | None = None
        if delaySeconds is not None and delaySeconds >= 1:
            now = datetime.now(self.__timeZoneRepository.getDefault())
            sendAfter = now + timedelta(seconds = delaySeconds)

        chatMessage = ChatMessage(
            text = cleanedText,
            twitchChannelId = twitchChannelId,
            sendAfter = sendAfter,
            replyMessageId = replyMessageId,
        )

        self.__submitChatMessage(chatMessage)

    async def __sendChatMessage(
        self,
        chatMessage: ChatMessage,
    ):
        texts = await self.__prepareChatMessageTexts(chatMessage)
        selfTwitchAccessToken = await self.__getSelfTwitchAccessToken()
        selfTwitchUserId = await self.__getSelfTwitchUserId()

        twitchChannel = await self.__userIdsRepository.requireUserName(
            userId = chatMessage.twitchChannelId,
            twitchAccessToken = selfTwitchAccessToken,
        )

        for text in texts:
            await self.__sendChatMessageText(
                chatMessage = chatMessage,
                selfTwitchAccessToken = selfTwitchAccessToken,
                selfTwitchUserId = selfTwitchUserId,
                text = text,
                twitchChannel = twitchChannel,
            )

    async def __sendChatMessageText(
        self,
        chatMessage: ChatMessage,
        selfTwitchAccessToken: str,
        selfTwitchUserId: str,
        text: str,
        twitchChannel: str,
    ):
        sendAttempt = 0
        shouldRetry = False
        successfullySent = False

        while not successfullySent and (sendAttempt == 0 or shouldRetry):
            chatRequest: TwitchSendChatMessageRequest

            if sendAttempt == 0 and utils.isValidStr(chatMessage.replyMessageId):
                chatRequest = TwitchSendChatMessageRequest(
                    broadcasterId = chatMessage.twitchChannelId,
                    message = text,
                    replyParentMessageId = chatMessage.replyMessageId,
                    senderId = selfTwitchUserId,
                )
            else:
                chatRequest = TwitchSendChatMessageRequest(
                    broadcasterId = chatMessage.twitchChannelId,
                    message = text,
                    replyParentMessageId = None,
                    senderId = selfTwitchUserId,
                )

            response: TwitchSendChatMessageResponse | None = None

            try:
                response = await self.__twitchApiService.sendChatMessage(
                    twitchAccessToken = selfTwitchAccessToken,
                    chatRequest = chatRequest,
                )
            except Exception as e:
                self.__timber.log('TwitchChatMessenger', f'Failed to send chat message ({chatMessage=}) ({text=}) ({len(text)=}) ({sendAttempt=}) ({response=})', e, traceback.format_exc())

            successfullySent = response is not None and response.isSent

            if not successfullySent:
                shouldRetry = sendAttempt == 0 and utils.isValidStr(chatMessage.replyMessageId)
                self.__timber.log('TwitchChatMessenger', f'Failed to send chat message via ({chatMessage=}) ({text=}) ({len(text)=}) ({sendAttempt=}) ({response=}) ({shouldRetry=})')

            sendAttempt += 1

        self.__sentMessageLogger.log(
            successfullySent = successfullySent,
            exceptions = None,
            numberOfSendAttempts = sendAttempt,
            messageMethod = MessageMethod.TWITCH_API,
            msg = text,
            twitchChannel = twitchChannel,
        )

    def start(self):
        if self.__isStarted:
            self.__timber.log('TwitchChatMessenger', 'Not starting TwitchChatMessenger as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TwitchChatMessenger', 'Starting TwitchChatMessenger...')
        self.__backgroundTaskHelper.createTask(self.__startMessageLoop())

    async def __startMessageLoop(self):
        while True:
            chatMessages: FrozenList[ChatMessage] = FrozenList()

            try:
                while not self.__messageQueue.empty():
                    chatMessage = self.__messageQueue.get_nowait()
                    chatMessages.append(chatMessage)
            except queue.Empty as e:
                self.__timber.log('TwitchChatMessenger', f'Encountered queue.Empty when building up chat messages list (queue size: {self.__messageQueue.qsize()}) ({len(chatMessages)=}): {e}', e, traceback.format_exc())

            chatMessages.freeze()

            for index, chatMessage in enumerate(chatMessages):
                try:
                    await self.__handleChatMessage(chatMessage)
                except Exception as e:
                    self.__timber.log('TwitchChatMessenger', f'Encountered unknown Exception when looping through chat messages (queue size: {self.__messageQueue.qsize()}) ({len(chatMessages)=}) ({index=}) ({chatMessage=}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__sleepTimeSeconds)

    def __submitChatMessage(self, chatMessage: ChatMessage):
        if not isinstance(chatMessage, ChatMessage):
            raise TypeError(f'chatMessage argument is malformed: \"{chatMessage}\"')

        try:
            self.__messageQueue.put(
                item = chatMessage,
                block = True,
                timeout = self.__queueTimeoutSeconds,
            )
        except queue.Full as e:
            self.__timber.log('TwitchChatMessenger', f'Encountered queue.Full when submitting a new chat message ({chatMessage}) into the action queue (queue size: {self.__messageQueue.qsize()}): {e}', e, traceback.format_exc())
