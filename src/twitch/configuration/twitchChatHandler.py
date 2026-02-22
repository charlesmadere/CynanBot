import math
from typing import Collection, Final

from frozenlist import FrozenList

from ..absTwitchChatHandler import AbsTwitchChatHandler
from ..api.models.twitchChatMessageFragment import TwitchChatMessageFragment as ApiTwitchChatMessageFragment
from ..api.models.twitchChatMessageFragmentCheermote import \
    TwitchChatMessageFragmentCheermote as ApiTwitchChatMessageFragmentCheermote
from ..api.models.twitchChatMessageFragmentEmote import \
    TwitchChatMessageFragmentEmote as ApiTwitchChatMessageFragmentEmote
from ..api.models.twitchChatMessageFragmentMention import \
    TwitchChatMessageFragmentMention as ApiTwitchChatMessageFragmentMention
from ..api.models.twitchChatMessageFragmentType import TwitchChatMessageFragmentType as ApiTwitchChatMessageFragmentType
from ..api.models.twitchCheerMetadata import TwitchCheerMetadata as ApiTwitchCheerMetadata
from ..api.models.twitchEmoteImageFormat import TwitchEmoteImageFormat as ApiTwitchEmoteImageFormat
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..localModels.twitchChatMessage import TwitchChatMessage
from ..localModels.twitchChatMessageFragment import TwitchChatMessageFragment
from ..localModels.twitchChatMessageFragmentCheermote import TwitchChatMessageFragmentCheermote
from ..localModels.twitchChatMessageFragmentEmote import TwitchChatMessageFragmentEmote
from ..localModels.twitchChatMessageFragmentMention import TwitchChatMessageFragmentMention
from ..localModels.twitchChatMessageFragmentType import TwitchChatMessageFragmentType
from ..localModels.twitchCheer import TwitchCheer
from ..localModels.twitchEmoteImageFormat import TwitchEmoteImageFormat
from ...chatLogger.chatLoggerInterface import ChatLoggerInterface
from ...cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
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
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        chatLogger: ChatLoggerInterface,
        cheerActionHelper: CheerActionHelperInterface | None,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface | None,
        triviaGameMachine: TriviaGameMachineInterface | None,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(chatLogger, ChatLoggerInterface):
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

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__chatLogger: Final[ChatLoggerInterface] = chatLogger
        self.__cheerActionHelper: Final[CheerActionHelperInterface | None] = cheerActionHelper
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameBuilder: Final[TriviaGameBuilderInterface | None] = triviaGameBuilder
        self.__triviaGameMachine: Final[TriviaGameMachineInterface | None] = triviaGameMachine

    async def __logCheer(self, chatMessage: TwitchChatMessage):
        if chatMessage.cheer is None or chatMessage.cheer.bits < 1:
            return

        self.__chatLogger.logCheer(
            bits = chatMessage.cheer.bits,
            cheerUserId = chatMessage.chatterUserId,
            cheerUserLogin = chatMessage.chatterUserLogin,
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
        )

    async def onNewChat(self, chatMessage: TwitchChatMessage):
        if not isinstance(chatMessage, TwitchChatMessage):
            raise TypeError(f'chatMessage argument is malformed: \"{chatMessage}\"')

        if utils.isValidStr(chatMessage.sourceMessageId):
            # This is a chat message that originated from a shared chat/stream. As such, let's not
            # even bother to process it or work with it at all. In the future, we may have a reason
            # to change this. But for now, it's better to just ignore these messages completely.
            return

        if chatMessage.twitchUser.isChatLoggingEnabled:
            await self.__logCheer(chatMessage)

        if chatMessage.twitchUser.areCheerActionsEnabled and await self.__processCheerAction(chatMessage):
            return

        if chatMessage.twitchUser.isSuperTriviaGameEnabled:
            await self.__processSuperTriviaEvent(chatMessage)

        if chatMessage.twitchUser.isTtsEnabled:
            await self.__processTtsEvent(chatMessage)

    async def onNewChatDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().event

        if event is None:
            self.__timber.log('TwitchChatHandler', f'Received a data bundle that has no event: ({user=}) ({twitchChannelId=}) ({dataBundle=})')
            return

        eventId = dataBundle.metadata.messageId
        chatterUserId = event.chatterUserId
        chatterUserLogin = event.chatterUserLogin
        chatterUserName = event.chatterUserName
        chatMessage = event.chatMessage

        if not utils.isValidStr(eventId) or not utils.isValidStr(chatterUserId) or not utils.isValidStr(chatterUserLogin) or not utils.isValidStr(chatterUserName) or chatMessage is None:
            self.__timber.log('TwitchChatHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({twitchChannelId=}) ({dataBundle=}) ({chatterUserId=}) ({chatterUserLogin=}) ({chatterUserName=}) ({chatMessage=})')
            return

        messageFragments = await self.__mapApiMessageFragments(chatMessage.fragments)
        cheer = await self.__mapApiCheer(event.cheer)

        chatMessage = TwitchChatMessage(
            messageFragments = messageFragments,
            chatterUserId = chatterUserId,
            chatterUserLogin = chatterUserLogin,
            chatterUserName = chatterUserName,
            eventId = eventId,
            sourceMessageId = event.sourceMessageId,
            text = chatMessage.text,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = event.messageId,
            cheer = cheer,
            twitchUser = user,
        )

        await self.onNewChat(
            chatMessage = chatMessage,
        )

    async def __processCheerAction(self, chatMessage: TwitchChatMessage) -> bool:
        user = chatMessage.twitchUser

        if not user.areCheerActionsEnabled:
            return False
        elif self.__cheerActionHelper is None:
            return False

        cheer = chatMessage.cheer
        if cheer is None or cheer.bits < 1:
            return False

        messageWithoutCheerText = await self.__purgeChatMessageOfCheers(chatMessage)
        self.__timber.log('TwitchChatHandler', f'Purged message of cheers ({messageWithoutCheerText=}) ({chatMessage=})')

        return await self.__cheerActionHelper.handleCheerAction(
            bits = cheer.bits,
            cheerUserId = chatMessage.chatterUserId,
            cheerUserName = chatMessage.chatterUserLogin,
            message = chatMessage.text,
            twitchChannelId = chatMessage.twitchChannelId,
            twitchChatMessageId = chatMessage.twitchChatMessageId,
            user = user,
        )

    async def __processSuperTriviaEvent(self, chatMessage: TwitchChatMessage):
        user = chatMessage.twitchUser

        if not user.isSuperTriviaGameEnabled:
            return
        elif self.__triviaGameBuilder is None or self.__triviaGameMachine is None:
            return

        cheer = chatMessage.cheer
        if cheer is None or cheer.bits < 1:
            return

        superTriviaCheerTriggerAmount = user.superTriviaCheerTriggerAmount
        superTriviaCheerTriggerMaximum = user.superTriviaCheerTriggerMaximum

        if superTriviaCheerTriggerAmount is None or superTriviaCheerTriggerAmount < 1 or cheer.bits < superTriviaCheerTriggerAmount:
            return

        numberOfGames = int(math.floor(float(cheer.bits) / float(superTriviaCheerTriggerAmount)))

        if numberOfGames < 1:
            return
        elif superTriviaCheerTriggerMaximum is not None and numberOfGames > superTriviaCheerTriggerMaximum:
            numberOfGames = int(min(numberOfGames, superTriviaCheerTriggerMaximum))

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            numberOfGames = numberOfGames,
        )

        if action is not None:
            self.__triviaGameMachine.submitAction(action)

    async def __processTtsEvent(self, chatMessage: TwitchChatMessage):
        user = chatMessage.twitchUser
        if not user.isTtsEnabled:
            return

        cheer = chatMessage.cheer
        if cheer is None or cheer.bits < 1:
            return

        provider: TtsProvider | None = None
        ttsBoosterPacks = user.ttsBoosterPacks

        if ttsBoosterPacks is None or len(ttsBoosterPacks) == 0:
            return

        for ttsBoosterPack in ttsBoosterPacks:
            if ttsBoosterPack.isEnabled and cheer.bits >= ttsBoosterPack.cheerAmount:
                provider = ttsBoosterPack.ttsProvider
                break

        if provider is None:
            return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.CHEER,
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            ttsEvent = TtsEvent(
                message = chatMessage.text,
                twitchChannel = chatMessage.twitchChannel,
                twitchChannelId = chatMessage.twitchChannelId,
                userId = chatMessage.chatterUserId,
                userName = chatMessage.chatterUserLogin,
                donation = TtsCheerDonation(
                    bits = cheer.bits,
                ),
                provider = provider,
                providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
                raidInfo = None,
            ),
        ))

    async def __purgeChatMessageOfCheers(self, message: TwitchChatMessage) -> str:
        chunks: list[str] = list()

        for messageFragment in message.messageFragments:
            if messageFragment.fragmentType is not TwitchChatMessageFragmentType.CHEERMOTE:
                chunks.append(messageFragment.text)

        purgedMessage = ' '.join(chunks)
        return utils.cleanStr(purgedMessage)

    async def __mapApiCheer(
        self,
        apiCheer: ApiTwitchCheerMetadata | None,
    ) -> TwitchCheer | None:
        if apiCheer is None or apiCheer.bits < 1:
            return None

        return TwitchCheer(
            bits = apiCheer.bits,
        )

    async def __mapApiMessageFragments(
        self,
        apiMessageFragments: Collection[ApiTwitchChatMessageFragment],
    ) -> FrozenList[TwitchChatMessageFragment]:
        messageFragments: FrozenList[TwitchChatMessageFragment] = FrozenList()

        for apiMessageFragment in apiMessageFragments:
            messageFragment = await self.__mapApiMessageFragment(apiMessageFragment)
            messageFragments.append(messageFragment)

        messageFragments.freeze()
        return messageFragments

    async def __mapApiMessageFragment(
        self,
        apiMessageFragment: ApiTwitchChatMessageFragment,
    ) -> TwitchChatMessageFragment:
        cheermote = await self.__mapApiMessageFragmentCheermote(apiMessageFragment.cheermote)
        emote = await self.__mapApiMessageFragmentEmote(apiMessageFragment.emote)
        mention = await self.__mapApiMessageFragmentMention(apiMessageFragment.mention)
        fragmentType = await self.__mapApiMessageFragmentType(apiMessageFragment.fragmentType)

        return TwitchChatMessageFragment(
            text = apiMessageFragment.text,
            cheermote = cheermote,
            emote = emote,
            mention = mention,
            fragmentType = fragmentType,
        )

    async def __mapApiMessageFragmentCheermote(
        self,
        apiCheermote: ApiTwitchChatMessageFragmentCheermote | None,
    ) -> TwitchChatMessageFragmentCheermote | None:
        if apiCheermote is None:
            return None

        return TwitchChatMessageFragmentCheermote(
            bits = apiCheermote.bits,
            tier = apiCheermote.tier,
            prefix = apiCheermote.prefix,
        )

    async def __mapApiMessageFragmentEmote(
        self,
        apiEmote: ApiTwitchChatMessageFragmentEmote | None,
    ) -> TwitchChatMessageFragmentEmote | None:
        if apiEmote is None:
            return None

        frozenImageFormats: frozenset[TwitchEmoteImageFormat] | None = None

        if apiEmote.formats is not None and len(apiEmote.formats) >= 1:
            imageFormats: set[TwitchEmoteImageFormat] = set()

            for apiImageFormat in apiEmote.formats:
                imageFormat = await self.__mapApiEmoteImageFormat(apiImageFormat)
                imageFormats.add(imageFormat)

            frozenImageFormats = frozenset(imageFormats)

        return TwitchChatMessageFragmentEmote(
            imageFormats = frozenImageFormats,
            emoteId = apiEmote.emoteId,
            emoteSetId = apiEmote.emoteSetId,
            ownerId = apiEmote.ownerId,
        )

    async def __mapApiEmoteImageFormat(
        self,
        apiImageFormat: ApiTwitchEmoteImageFormat,
    ) -> TwitchEmoteImageFormat:
        match apiImageFormat:
            case ApiTwitchEmoteImageFormat.ANIMATED: return TwitchEmoteImageFormat.ANIMATED
            case ApiTwitchEmoteImageFormat.DEFAULT: return TwitchEmoteImageFormat.DEFAULT
            case ApiTwitchEmoteImageFormat.STATIC: return TwitchEmoteImageFormat.STATIC
            case _: raise ValueError(f'Encountered unknown ApiTwitchEmoteImageFormat: \"{apiImageFormat}\"')

    async def __mapApiMessageFragmentMention(
        self,
        apiMention: ApiTwitchChatMessageFragmentMention | None,
    ) -> TwitchChatMessageFragmentMention | None:
        if apiMention is None:
            return None

        return TwitchChatMessageFragmentMention(
            userId = apiMention.userId,
            userLogin = apiMention.userLogin,
            userName = apiMention.userName,
        )

    async def __mapApiMessageFragmentType(
        self,
        apiFragmentType: ApiTwitchChatMessageFragmentType,
    ) -> TwitchChatMessageFragmentType:
        match apiFragmentType:
            case ApiTwitchChatMessageFragmentType.CHEERMOTE: return TwitchChatMessageFragmentType.CHEERMOTE
            case ApiTwitchChatMessageFragmentType.EMOTE: return TwitchChatMessageFragmentType.EMOTE
            case ApiTwitchChatMessageFragmentType.MENTION: return TwitchChatMessageFragmentType.MENTION
            case ApiTwitchChatMessageFragmentType.TEXT: return TwitchChatMessageFragmentType.TEXT
            case _: raise ValueError(f'Encountered unknown ApiTwitchChatMessageFragmentType: \"{apiFragmentType}\"')
