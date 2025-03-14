import math

from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchChatHandler import AbsTwitchChatHandler
from ..api.models.twitchChatMessage import TwitchChatMessage
from ..api.models.twitchCheerMetadata import TwitchCheerMetadata
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ...chatLogger.chatLoggerInterface import ChatLoggerInterface
from ...cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ...trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ...tts.models.ttsCheerDonation import TtsCheerDonation
from ...tts.models.ttsEvent import TtsEvent
from ...tts.models.ttsProvider import TtsProvider
from ...tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ...users.userInterface import UserInterface


class TwitchChatHandler(AbsTwitchChatHandler):

    def __init__(
        self,
        chatLogger: ChatLoggerInterface,
        cheerActionHelper: CheerActionHelperInterface | None,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface | None,
        triviaGameMachine: TriviaGameMachineInterface | None
    ):
        if not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif cheerActionHelper is not None and not isinstance(cheerActionHelper, CheerActionHelperInterface):
            raise TypeError(f'cheerActionHelper argument is malformed: \"{cheerActionHelper}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameBuilder is not None and not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise TypeError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif triviaGameMachine is not None and not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')

        self.__chatLogger: ChatLoggerInterface = chatLogger
        self.__cheerActionHelper: CheerActionHelperInterface | None = cheerActionHelper
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: TriviaGameBuilderInterface | None = triviaGameBuilder
        self.__triviaGameMachine: TriviaGameMachineInterface | None = triviaGameMachine

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __handleCheer(
        self,
        broadcasterUserId: str,
        chatterUserId: str,
        chatterUserLogin: str,
        twitchChatMessageId: str | None,
        chatMessage: TwitchChatMessage,
        cheer: TwitchCheerMetadata | None,
        user: UserInterface
    ):
        if cheer is None or cheer.bits < 1:
            return

        if user.isChatLoggingEnabled:
            self.__chatLogger.logCheer(
                bits = cheer.bits,
                twitchChannel = user.handle,
                twitchChannelId = broadcasterUserId,
                userId = chatterUserId,
                userName = chatterUserLogin
            )

        if user.isSuperTriviaGameEnabled:
            # TODO delete this after doing some debugging
            self.__timber.log('TwitchChatHandler', f'__handleCheer #1: ({broadcasterUserId=}) ({chatterUserId=}) ({chatterUserLogin=}) ({twitchChatMessageId=}) ({cheer=}) ({user=})')

            await self.__processSuperTriviaEvent(
                broadcasterUserId = broadcasterUserId,
                cheer = cheer,
                user = user
            )

            # TODO delete this after doing some debugging
            self.__timber.log('TwitchChatHandler', f'__handleCheer #2: ({broadcasterUserId=}) ({chatterUserId=}) ({chatterUserLogin=}) ({twitchChatMessageId=}) ({cheer=}) ({user=})')
        else:
            # TODO delete this after doing some debugging
            self.__timber.log('TwitchChatHandler', f'__handleCheer #3: ({broadcasterUserId=}) ({chatterUserId=}) ({chatterUserLogin=}) ({twitchChatMessageId=}) ({cheer=}) ({user=})')

        if user.areCheerActionsEnabled:
            # TODO delete this after doing some debugging
            self.__timber.log('TwitchChatHandler', f'__handleCheer #4: ({broadcasterUserId=}) ({chatterUserId=}) ({chatterUserLogin=}) ({twitchChatMessageId=}) ({cheer=}) ({user=})')

            if await self.__processCheerAction(
                broadcasterUserId = broadcasterUserId,
                chatterUserId = chatterUserId,
                chatterUserLogin = chatterUserLogin,
                twitchChatMessageId = twitchChatMessageId,
                chatMessage = chatMessage,
                cheer = cheer,
                user = user
            ):
                return

        if user.isTtsEnabled:
            # TODO delete this after doing some debugging
            self.__timber.log('TwitchChatHandler', f'__handleCheer #5: ({broadcasterUserId=}) ({chatterUserId=}) ({chatterUserLogin=}) ({twitchChatMessageId=}) ({cheer=}) ({user=})')

            await self.__processTtsEvent(
                broadcasterUserId = broadcasterUserId,
                chatMessage = chatMessage,
                chatterUserId = chatterUserId,
                chatterUserLogin = chatterUserLogin,
                cheer = cheer,
                user = user
            )

        # TODO delete this after doing some debugging
        self.__timber.log('TwitchChatHandler', f'__handleCheer #6: ({broadcasterUserId=}) ({chatterUserId=}) ({chatterUserLogin=}) ({twitchChatMessageId=}) ({cheer=}) ({user=})')

    async def onNewChat(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().event

        if event is None:
            self.__timber.log('TwitchChatHandler', f'Received a data bundle that has no event: ({user=}) ({userId=}) ({dataBundle=})')
            return

        chatterUserId = event.chatterUserId
        chatterUserLogin = event.chatterUserLogin
        chatterUserName = event.chatterUserName
        chatMessage = event.chatMessage

        if not utils.isValidStr(chatterUserId) or not utils.isValidStr(chatterUserLogin) or not utils.isValidStr(chatterUserName) or chatMessage is None:
            self.__timber.log('TwitchChatHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({dataBundle=}) ({chatterUserId=}) ({chatterUserLogin=}) ({chatterUserName=}) ({chatMessage=})')
            return

        # TODO delete this after doing some debugging
        self.__timber.log('TwitchChatHandler', f'onNewChat #1: ({user=}) ({dataBundle=}) ({chatterUserId=}) ({chatterUserLogin=}) ({chatterUserName=}) ({chatMessage=}) ({event.cheer=})')

        await self.__handleCheer(
            broadcasterUserId = userId,
            chatterUserId = chatterUserId,
            chatterUserLogin = chatterUserLogin,
            chatMessage = chatMessage,
            twitchChatMessageId = event.messageId,
            cheer = event.cheer,
            user = user
        )

        # TODO delete this after doing some debugging
        self.__timber.log('TwitchChatHandler', f'onNewChat #2: ({user=}) ({dataBundle=}) ({chatterUserId=}) ({chatterUserLogin=}) ({chatterUserName=}) ({chatMessage=}) ({event.cheer=})')

    async def __processCheerAction(
        self,
        broadcasterUserId: str,
        chatterUserId: str,
        chatterUserLogin: str,
        twitchChatMessageId: str | None,
        chatMessage: TwitchChatMessage,
        cheer: TwitchCheerMetadata,
        user: UserInterface
    ) -> bool:
        if not user.areCheerActionsEnabled:
            return False
        elif self.__cheerActionHelper is None:
            return False
        else:
            return await self.__cheerActionHelper.handleCheerAction(
                bits = cheer.bits,
                broadcasterUserId = broadcasterUserId,
                cheerUserId = chatterUserId,
                cheerUserName = chatterUserLogin,
                message = chatMessage.text,
                twitchChatMessageId = twitchChatMessageId,
                user = user
            )

    async def __processSuperTriviaEvent(
        self,
        broadcasterUserId: str,
        cheer: TwitchCheerMetadata,
        user: UserInterface
    ):
        if not user.isSuperTriviaGameEnabled:
            return
        elif self.__triviaGameBuilder is None or self.__triviaGameMachine is None:
            return

        bits = cheer.bits
        superTriviaCheerTriggerAmount = user.superTriviaCheerTriggerAmount
        superTriviaCheerTriggerMaximum = user.superTriviaCheerTriggerMaximum

        # TODO delete this after doing some debugging
        self.__timber.log('TwitchChatHandler', f'__processSuperTriviaEvent #1: ({broadcasterUserId=}) ({cheer=}) ({user=}) ({bits=}) ({superTriviaCheerTriggerAmount=}) ({superTriviaCheerTriggerMaximum=})')

        if superTriviaCheerTriggerAmount is None or superTriviaCheerTriggerAmount < 1 or bits < superTriviaCheerTriggerAmount:
            return

        numberOfGames = int(math.floor(float(bits) / float(superTriviaCheerTriggerAmount)))

        # TODO delete this after doing some debugging
        self.__timber.log('TwitchChatHandler', f'__processSuperTriviaEvent #2: ({broadcasterUserId=}) ({cheer=}) ({user=}) ({bits=}) ({superTriviaCheerTriggerAmount=}) ({superTriviaCheerTriggerMaximum=}) ({numberOfGames=})')

        if numberOfGames < 1:
            return
        elif superTriviaCheerTriggerMaximum is not None and numberOfGames > superTriviaCheerTriggerMaximum:
            numberOfGames = int(min(numberOfGames, superTriviaCheerTriggerMaximum))

        # TODO delete this after doing some debugging
        self.__timber.log('TwitchChatHandler', f'__processSuperTriviaEvent #3: ({broadcasterUserId=}) ({cheer=}) ({user=}) ({bits=}) ({superTriviaCheerTriggerAmount=}) ({superTriviaCheerTriggerMaximum=}) ({numberOfGames=})')

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.handle,
            twitchChannelId = broadcasterUserId,
            numberOfGames = numberOfGames
        )

        # TODO delete this after doing some debugging
        self.__timber.log('TwitchChatHandler', f'__processSuperTriviaEvent #4: ({broadcasterUserId=}) ({cheer=}) ({user=}) ({bits=}) ({superTriviaCheerTriggerAmount=}) ({superTriviaCheerTriggerMaximum=}) ({numberOfGames=}) ({action=})')

        if action is not None:
            self.__triviaGameMachine.submitAction(action)

        # TODO delete this after doing some debugging
        self.__timber.log('TwitchChatHandler', f'__processSuperTriviaEvent #5: ({broadcasterUserId=}) ({cheer=}) ({user=}) ({bits=}) ({superTriviaCheerTriggerAmount=}) ({superTriviaCheerTriggerMaximum=}) ({numberOfGames=}) ({action=})')

    async def __processTtsEvent(
        self,
        broadcasterUserId: str,
        chatterUserId: str,
        chatterUserLogin: str,
        chatMessage: TwitchChatMessage,
        cheer: TwitchCheerMetadata,
        user: UserInterface
    ):
        if not user.isTtsEnabled:
            return

        provider: TtsProvider | None = None
        ttsBoosterPacks = user.ttsBoosterPacks

        if ttsBoosterPacks is None or len(ttsBoosterPacks) == 0:
            return

        for ttsBoosterPack in ttsBoosterPacks:
            if cheer.bits >= ttsBoosterPack.cheerAmount:
                provider = ttsBoosterPack.ttsProvider
                break

        if provider is None:
            return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.CHEER,
            twitchChannel = user.handle,
            twitchChannelId = broadcasterUserId,
            ttsEvent = TtsEvent(
                message = chatMessage.text,
                twitchChannel = user.handle,
                twitchChannelId = broadcasterUserId,
                userId = chatterUserId,
                userName = chatterUserLogin,
                donation = TtsCheerDonation(
                    bits = cheer.bits
                ),
                provider = provider,
                providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
                raidInfo = None
            )
        ))

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
