from typing import Dict, List

from twitchio import Channel, Message
from twitchio.ext import commands, pubsub
from twitchio.ext.commands import Bot, Context
from twitchio.ext.commands.errors import CommandNotFound
from twitchio.ext.pubsub import PubSubChannelPointsMessage, PubSubPool
from twitchio.ext.pubsub.topics import Topic

import CynanBotCommon.utils as utils
from authHelper import AuthHelper
from commands import (AbsCommand, AnalogueCommand, AnswerCommand,
                      ChatBandClearCommand, CommandsCommand, CutenessCommand,
                      CynanSourceCommand, DiscordCommand, GiveCutenessCommand,
                      JishoCommand, MyCutenessCommand, PbsCommand,
                      PkMonCommand, PkMoveCommand, RaceCommand, StubCommand,
                      SwQuoteCommand, TamalesCommand, TimeCommand,
                      TranslateCommand, TriviaCommand, TriviaScoreCommand,
                      TwitterCommand, WeatherCommand, WordCommand)
from cuteness.cutenessRepository import CutenessRepository
from cuteness.doubleCutenessHelper import DoubleCutenessHelper
from CynanBotCommon.analogue.analogueStoreRepository import \
    AnalogueStoreRepository
from CynanBotCommon.chatBand.chatBandManager import ChatBandManager
from CynanBotCommon.funtoon.funtoonRepository import FuntoonRepository
from CynanBotCommon.language.jishoHelper import JishoHelper
from CynanBotCommon.language.languagesRepository import LanguagesRepository
from CynanBotCommon.language.translationHelper import TranslationHelper
from CynanBotCommon.language.wordOfTheDayRepository import \
    WordOfTheDayRepository
from CynanBotCommon.location.locationsRepository import LocationsRepository
from CynanBotCommon.lruCache import LruCache
from CynanBotCommon.nonceRepository import NonceRepository
from CynanBotCommon.pkmn.pokepediaRepository import PokepediaRepository
from CynanBotCommon.starWars.starWarsQuotesRepository import \
    StarWarsQuotesRepository
from CynanBotCommon.tamaleGuyRepository import TamaleGuyRepository
from CynanBotCommon.trivia.triviaGameRepository import TriviaGameRepository
from CynanBotCommon.trivia.triviaRepository import TriviaRepository
from CynanBotCommon.trivia.triviaScoreRepository import TriviaScoreRepository
from CynanBotCommon.twitchTokensRepository import (
    TwitchAccessTokenMissingException, TwitchRefreshTokenMissingException,
    TwitchTokensRepository)
from CynanBotCommon.weather.weatherRepository import WeatherRepository
from CynanBotCommon.websocketConnection.websocketConnectionServer import \
    WebsocketConnectionServer
from events import AbsEvent, RaidEvent, SubGiftThankingEvent
from generalSettingsRepository import GeneralSettingsRepository
from messages import (AbsMessage, CatJamMessage, ChatBandMessage, CynanMessage,
                      DeerForceMessage, EyesMessage, ImytSlurpMessage,
                      JamCatMessage, RatJamMessage, StubMessage)
from pointRedemptions import (AbsPointRedemption, CutenessRedemption,
                              DoubleCutenessRedemption, PkmnBattleRedemption,
                              PkmnCatchRedemption, PkmnEvolveRedemption,
                              PkmnShinyRedemption, PotdPointRedemption,
                              StubPointRedemption, TriviaGameRedemption)
from users.user import User
from users.userIdsRepository import UserIdsRepository
from users.usersRepository import UsersRepository


class CynanBot(Bot):

    def __init__(
        self,
        analogueStoreRepository: AnalogueStoreRepository,
        authHelper: AuthHelper,
        chatBandManager: ChatBandManager,
        cutenessRepository: CutenessRepository,
        doubleCutenessHelper: DoubleCutenessHelper,
        funtoonRepository: FuntoonRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        jishoHelper: JishoHelper,
        languagesRepository: LanguagesRepository,
        locationsRepository: LocationsRepository,
        nonceRepository: NonceRepository,
        pokepediaRepository: PokepediaRepository,
        starWarsQuotesRepository: StarWarsQuotesRepository,
        tamaleGuyRepository: TamaleGuyRepository,
        translationHelper: TranslationHelper,
        triviaGameRepository: TriviaGameRepository,
        triviaRepository: TriviaRepository,
        triviaScoreRepository: TriviaScoreRepository,
        twitchTokensRepository: TwitchTokensRepository,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        weatherRepository: WeatherRepository,
        websocketConnectionServer: WebsocketConnectionServer,
        wordOfTheDayRepository: WordOfTheDayRepository
    ):
        super().__init__(
            token = authHelper.requireTwitchIrcAuthToken(),
            client_secret = authHelper.requireTwitchClientSecret(),
            nick = authHelper.requireNick(),
            prefix = '!',
            initial_channels = [ user.getHandle() for user in usersRepository.getUsers() ]
        )

        if authHelper is None:
            raise ValueError(f'authHelper argument is malformed: \"{authHelper}\"')
        elif doubleCutenessHelper is None:
            raise ValueError(f'doubleCutenessHelper argument is malformed: \"{doubleCutenessHelper}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif languagesRepository is None:
            raise ValueError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif nonceRepository is None:
            raise ValueError(f'nonceRepository argument is malformed: \"{nonceRepository}\"')
        elif twitchTokensRepository is None:
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__authHelper: AuthHelper = authHelper
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__twitchTokensRepository: TwitchTokensRepository = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__websocketConnectionServer: WebsocketConnectionServer = websocketConnectionServer

        self.__channelPointsLruCache: LruCache = LruCache(64)

        #######################################
        ## Initialization of command objects ##
        #######################################

        self.__commandsCommand: AbsCommand = CommandsCommand(generalSettingsRepository, usersRepository)
        self.__cynanSourceCommand: AbsCommand = CynanSourceCommand(usersRepository)
        self.__discordCommand: AbsCommand = DiscordCommand(usersRepository)
        self.__pbsCommand: AbsCommand = PbsCommand(usersRepository)
        self.__raceCommand: AbsCommand = RaceCommand(usersRepository)
        self.__timeCommand: AbsCommand = TimeCommand(usersRepository)
        self.__twitterCommand: AbsCommand = TwitterCommand(usersRepository)

        if analogueStoreRepository is None:
            self.__analogueCommand: AbsCommand = StubCommand()
        else:
            self.__analogueCommand: AbsCommand = AnalogueCommand(analogueStoreRepository, generalSettingsRepository, usersRepository)

        if cutenessRepository is None or triviaGameRepository is None or triviaScoreRepository is None:
            self.__answerCommand: AbsCommand = StubCommand()
        else:
            self.__answerCommand: AbsCommand = AnswerCommand(cutenessRepository, doubleCutenessHelper, generalSettingsRepository, triviaGameRepository, triviaScoreRepository, usersRepository)

        if chatBandManager is None:
            self.__chatBandClearCommand: AbsCommand = StubCommand()
        else:
            self.__chatBandClearCommand: AbsCommand = ChatBandClearCommand(chatBandManager, generalSettingsRepository, usersRepository)

        if cutenessRepository is None:
            self.__cutenessCommand: AbsCommand = StubCommand()
            self.__giveCutenessCommand: AbsCommand = StubCommand()
            self.__myCutenessCommand: AbsCommand = StubCommand()
        else:
            self.__cutenessCommand: AbsCommand = CutenessCommand(cutenessRepository, userIdsRepository, usersRepository)
            self.__giveCutenessCommand: AbsCommand = GiveCutenessCommand(cutenessRepository, userIdsRepository, usersRepository)
            self.__myCutenessCommand: AbsCommand = MyCutenessCommand(cutenessRepository, usersRepository)

        if jishoHelper is None:
            self.__jishoCommand: AbsCommand = StubCommand()
        else:
            self.__jishoCommand: AbsCommand = JishoCommand(generalSettingsRepository, jishoHelper, usersRepository)

        if pokepediaRepository is None:
            self.__pkMonCommand: AbsCommand = StubCommand()
            self.__pkMoveCommand: AbsCommand = StubCommand()
        else:
            self.__pkMonCommand: AbsCommand = PkMonCommand(generalSettingsRepository, pokepediaRepository, usersRepository)
            self.__pkMoveCommand: AbsCommand = PkMoveCommand(generalSettingsRepository, pokepediaRepository, usersRepository)

        if starWarsQuotesRepository is None:
            self.__swQuoteCommand: AbsCommand = StubCommand()
        else:
            self.__swQuoteCommand: AbsCommand = SwQuoteCommand(starWarsQuotesRepository, usersRepository)

        if tamaleGuyRepository is None:
            self.__tamalesCommand: AbsCommand = StubCommand()
        else:
            self.__tamalesCommand: AbsCommand = TamalesCommand(generalSettingsRepository, tamaleGuyRepository, usersRepository)

        if translationHelper is None:
            self.__translateCommand: AbsCommand = StubCommand()
        else:
            self.__translateCommand: AbsCommand = TranslateCommand(generalSettingsRepository, languagesRepository, translationHelper, usersRepository)

        if triviaRepository is None:
            self.__triviaCommand: AbsCommand = StubCommand()
        else:
            self.__triviaCommand: AbsCommand = TriviaCommand(generalSettingsRepository, triviaRepository, usersRepository)

        if triviaScoreRepository is None:
            self.__triviaScoreCommand: AbsCommand = StubCommand()
        else:
            self.__triviaScoreCommand: AbsCommand = TriviaScoreCommand(generalSettingsRepository, triviaScoreRepository, userIdsRepository, usersRepository)

        if locationsRepository is None or weatherRepository is None:
            self.__weatherCommand: AbsCommand = StubCommand()
        else:
            self.__weatherCommand: AbsCommand = WeatherCommand(generalSettingsRepository, locationsRepository, usersRepository, weatherRepository)

        if wordOfTheDayRepository is None:
            self.__wordCommand: AbsCommand = StubCommand()
        else:
            self.__wordCommand: AbsCommand = WordCommand(generalSettingsRepository, languagesRepository, usersRepository, wordOfTheDayRepository)

        #############################################
        ## Initialization of event handler objects ##
        #############################################

        self.__raidEvent: AbsEvent = RaidEvent(generalSettingsRepository)
        self.__subGiftThankingEvent: AbsEvent = SubGiftThankingEvent(authHelper, generalSettingsRepository)

        ###############################################
        ## Initialization of message handler objects ##
        ###############################################

        self.__catJamMessage: AbsMessage = CatJamMessage(generalSettingsRepository)

        if chatBandManager is None:
            self.__chatBandMessage: AbsMessage = StubMessage()
        else:
            self.__chatBandMessage: AbsMessage = ChatBandMessage(chatBandManager, generalSettingsRepository)

        self.__cynanMessage: AbsMessage = CynanMessage(generalSettingsRepository)
        self.__deerForceMessage: AbsMessage = DeerForceMessage(generalSettingsRepository)
        self.__eyesMessage: AbsMessage = EyesMessage(generalSettingsRepository)
        self.__imytSlurpMessage: AbsMessage = ImytSlurpMessage(generalSettingsRepository)
        self.__jamCatMessage: AbsMessage = JamCatMessage(generalSettingsRepository)
        self.__ratJamMessage: AbsMessage = RatJamMessage(generalSettingsRepository)

        ########################################################
        ## Initialization of point redemption handler objects ##
        ########################################################

        if cutenessRepository is None or doubleCutenessHelper is None:
            self.__cutenessPointRedemption: AbsPointRedemption = StubPointRedemption()
            self.__doubleCutenessPointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__cutenessPointRedemption: AbsPointRedemption = CutenessRedemption(cutenessRepository, doubleCutenessHelper)
            self.__doubleCutenessPointRedemption: AbsPointRedemption = DoubleCutenessRedemption(cutenessRepository, doubleCutenessHelper)

        if funtoonRepository is None:
            self.__pkmnBattlePointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__pkmnBattlePointRedemption: AbsPointRedemption = PkmnBattleRedemption(funtoonRepository, generalSettingsRepository)

        if funtoonRepository is None:
            self.__pkmnCatchPointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__pkmnCatchPointRedemption: AbsPointRedemption = PkmnCatchRedemption(funtoonRepository, generalSettingsRepository)

        if funtoonRepository is None:
            self.__pkmnEvolvePointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__pkmnEvolvePointRedemption: AbsPointRedemption = PkmnEvolveRedemption(funtoonRepository, generalSettingsRepository)

        if funtoonRepository is None:
            self.__pkmnShinyPointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__pkmnShinyPointRedemption: AbsPointRedemption = PkmnShinyRedemption(funtoonRepository, generalSettingsRepository)

        self.__potdPointRedemption: AbsPointRedemption = PotdPointRedemption()

        if cutenessRepository is None or triviaGameRepository is None or triviaScoreRepository is None:
            self.__triviaGamePointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__triviaGamePointRedemption: AbsPointRedemption = TriviaGameRedemption(cutenessRepository, generalSettingsRepository, triviaGameRepository, triviaScoreRepository)

        ######################################
        ## Initialization of PubSub objects ##
        ######################################

        self.__pubSub = PubSubPool(self)

    async def event_command_error(self, context: Context, error: Exception):
        if isinstance(error, CommandNotFound):
            return
        else:
            raise error

    async def event_message(self, message: Message):
        if message.echo:
            return

        if utils.isValidStr(message.content):
            if self.__generalSettingsRepository.isPersistAllUsersEnabled():
                self.__userIdsRepository.setUser(
                    userId = str(message.author.id),
                    userName = message.author.name
                )

            twitchUser = self.__usersRepository.getUser(message.channel.name)

            if await self.__chatBandMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__cynanMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__deerForceMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__catJamMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__imytSlurpMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__jamCatMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__ratJamMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__eyesMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

        await self.handle_commands(message)

    async def event_pubsub_channel_points(self, event: PubSubChannelPointsMessage):
        twitchUserIdStr = str(event.channel_id)
        twitchUserNameStr = self.__userIdsRepository.fetchUserName(twitchUserIdStr)
        twitchUser = self.__usersRepository.getUser(twitchUserNameStr)
        rewardId = str(event.reward.id)
        userIdThatRedeemed = str(event.user.id)
        userNameThatRedeemed: str = event.user.name
        redemptionMessage: str = event.input
        lruCacheId: str = f'{twitchUserNameStr}:{event.id}'.lower()

        if self.__channelPointsLruCache.contains(lruCacheId):
            print(f'Duplicate reward ID for {twitchUser.getHandle()} ({twitchUserIdStr}) redeemed by \"{userNameThatRedeemed}\" ({userIdThatRedeemed}): \"{event.id}\" ({utils.getNowTimeText(includeSeconds = True)})')
            return

        self.__channelPointsLruCache.put(lruCacheId)
        twitchChannel = self.get_channel(twitchUser.getHandle())

        if self.__generalSettingsRepository.isRewardIdPrintingEnabled() or twitchUser.isRewardIdPrintingEnabled():
            print(f'Reward ID for {twitchUser.getHandle()} ({twitchUserIdStr}) redeemed by \"{userNameThatRedeemed}\" ({userIdThatRedeemed}): \"{rewardId}\" ({utils.getNowTimeText(includeSeconds = True)})')

        if self.__generalSettingsRepository.isPersistAllUsersEnabled():
            self.__userIdsRepository.setUser(
                userId = userIdThatRedeemed,
                userName = userNameThatRedeemed
            )

        if twitchUser.isCutenessEnabled() and twitchUser.hasCutenessBoosterPacks():
            if await self.__cutenessPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchUser = twitchUser,
                redemptionMessage = redemptionMessage,
                rewardId = rewardId,
                userIdThatRedeemed = userIdThatRedeemed,
                userNameThatRedeemed = userNameThatRedeemed
            ):
                if self.__generalSettingsRepository.isDebugLoggingEnabled():
                    print(f'Redeemed cuteness point in {twitchUser.getHandle()} for {userNameThatRedeemed}:{userIdThatRedeemed}')
                return

            if rewardId == twitchUser.getIncreaseCutenessDoubleRewardId():
                if await self.__doubleCutenessPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    rewardId = rewardId,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                ):
                    if self.__generalSettingsRepository.isDebugLoggingEnabled():
                        print(f'Redeemed double cuteness points in {twitchUser.getHandle()} for {userNameThatRedeemed}:{userIdThatRedeemed}')
                return

        if twitchUser.isPicOfTheDayEnabled() and rewardId == twitchUser.getPicOfTheDayRewardId():
            if await self.__potdPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchUser = twitchUser,
                redemptionMessage = redemptionMessage,
                rewardId = rewardId,
                userIdThatRedeemed = userIdThatRedeemed,
                userNameThatRedeemed = userNameThatRedeemed
            ):
                if self.__generalSettingsRepository.isDebugLoggingEnabled():
                    print(f'Redeemed Pic Of The Day in {twitchUser.getHandle()} for {userNameThatRedeemed}:{userIdThatRedeemed}')
            return

        if twitchUser.isPkmnEnabled():
            if rewardId == twitchUser.getPkmnBattleRewardId():
                if await self.__pkmnBattlePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    rewardId = rewardId,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                ):
                    if self.__generalSettingsRepository.isDebugLoggingEnabled():
                        print(f'Redeemed Pkmn Battle in {twitchUser.getHandle()} for {userNameThatRedeemed}:{userIdThatRedeemed}')
                return

            if twitchUser.hasPkmnCatchBoosterPacks():
                if await self.__pkmnCatchPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    rewardId = rewardId,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                ):
                    if self.__generalSettingsRepository.isDebugLoggingEnabled():
                        print(f'Redeemed Pkmn Catch in {twitchUser.getHandle()} for {userNameThatRedeemed}:{userIdThatRedeemed}')
                    return

            if rewardId == twitchUser.getPkmnEvolveRewardId():
                if await self.__pkmnEvolvePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    rewardId = rewardId,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                ):
                    if self.__generalSettingsRepository.isDebugLoggingEnabled():
                        print(f'Redeemed Pkmn Evolve in {twitchUser.getHandle()} for {userNameThatRedeemed}:{userIdThatRedeemed}')
                return

            if rewardId == twitchUser.getPkmnShinyRewardId():
                if await self.__pkmnShinyPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    rewardId = rewardId,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                ):
                    if self.__generalSettingsRepository.isDebugLoggingEnabled():
                        print(f'Redeemed Pkmn Shiny in {twitchUser.getHandle()} for {userNameThatRedeemed}:{userIdThatRedeemed}')
                return

        if twitchUser.isTriviaGameEnabled() and rewardId == twitchUser.getTriviaGameRewardId():
            if await self.__triviaGamePointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchUser = twitchUser,
                redemptionMessage = redemptionMessage,
                rewardId = rewardId,
                userIdThatRedeemed = userIdThatRedeemed,
                userNameThatRedeemed = userNameThatRedeemed
            ):
                if self.__generalSettingsRepository.isDebugLoggingEnabled():
                    print(f'Redeemed trivia game in {twitchUser.getHandle()} for {userNameThatRedeemed}:{userIdThatRedeemed}')
            return

    async def event_pubsub_error(self, tags: Dict):
        print(f'Received PubSub error ({utils.getNowTimeText(includeSeconds = True)}): {tags}')
        await self.__unsubscribeFromPubSubTopics()
        await self.__subscribeToPubSubTopics()

    async def event_pubsub_nonce(self, tags: Dict):
        print(f'Received PubSub nonce ({utils.getNowTimeText(includeSeconds = True)}): {tags}')

    async def event_pubsub_pong(self):
        print(f'Received PubSub pong ({utils.getNowTimeText(includeSeconds = True)})')

    async def event_raw_usernotice(self, channel: Channel, tags: Dict):
        if self.__generalSettingsRepository.isDebugLoggingEnabled():
            print(f'event_raw_usernotice() ({utils.getNowTimeText(includeSeconds = True)}): {tags}')

        if not utils.hasItems(tags):
            return

        msgId = tags.get('msg-id')

        if not utils.isValidStr(msgId):
            return

        twitchUser = self.__usersRepository.getUser(channel.name)

        if msgId == 'raid':
            await self.__raidEvent.handleEvent(
                twitchChannel = channel,
                twitchUser = twitchUser,
                tags = tags
            )
        elif msgId == 'subgift' or msgId == 'anonsubgift':
            await self.__subGiftThankingEvent.handleEvent(
                twitchChannel = channel,
                twitchUser = twitchUser,
                tags = tags
            )

    async def event_ready(self):
        print(f'{self.__authHelper.requireNick()} is ready! ({utils.getNowTimeText(includeSeconds = True)})')
        await self.__startWebsocketConnectionServer()
        await self.__subscribeToPubSubTopics()

    async def __getAllPubSubTopics(self, validateAndRefresh: bool) -> List[Topic]:
        if not utils.isValidBool(validateAndRefresh):
            raise ValueError(f'validateAndRefresh argument is malformed: \"{validateAndRefresh}\"')

        users = self.__usersRepository.getUsers()
        usersAndTwitchTokens: Dict[User, str] = dict()
        pubSubTopics: List[Topic] = list()

        for user in users:
            twitchAccessToken = self.__twitchTokensRepository.getAccessToken(user.getHandle())

            if utils.isValidStr(twitchAccessToken):
                usersAndTwitchTokens[user] = twitchAccessToken

        if not utils.hasItems(usersAndTwitchTokens):
            return pubSubTopics

        usersToRemove: List[User] = list()

        if validateAndRefresh:
            for user in usersAndTwitchTokens:
                try:
                    self.__twitchTokensRepository.validateAndRefreshAccessToken(
                        twitchClientId = self.__authHelper.requireTwitchClientId(),
                        twitchClientSecret = self.__authHelper.requireTwitchClientSecret(),
                        twitchHandle = user.getHandle()
                    )

                    usersAndTwitchTokens[user] = self.__twitchTokensRepository.getAccessToken(user.getHandle())
                except (TwitchAccessTokenMissingException, TwitchRefreshTokenMissingException) as e:
                    # if we run into this error, that most likely means that this user changed
                    # their password
                    usersToRemove.append(user)
                    print(f'Failed to validate and refresh access Twitch token for {user.getHandle()} ({utils.getNowTimeText(includeSeconds = True)}): {e}')

        if utils.hasItems(usersToRemove):
            for user in usersToRemove:
                del usersAndTwitchTokens[user]

        for user in usersAndTwitchTokens:
            twitchAccessToken = usersAndTwitchTokens[user]

            userId = self.__userIdsRepository.fetchUserIdAsInt(
                userName = user.getHandle(),
                twitchAccessToken = twitchAccessToken,
                twitchClientId = self.__authHelper.requireTwitchClientId()
            )

            pubSubTopics.append(pubsub.channel_points(twitchAccessToken)[userId])

        return pubSubTopics

    async def __startWebsocketConnectionServer(self):
        if self.__websocketConnectionServer is None:
            print(f'Will not start websocketConnectionServer, as the instance is None ({utils.getNowTimeText(includeSeconds = True)})')
        else:
            self.__websocketConnectionServer.start(self.loop)

    async def __subscribeToPubSubTopics(self):
        pubSubTopics = await self.__getAllPubSubTopics(validateAndRefresh = True)
        if not utils.hasItems(pubSubTopics):
            print(f'There aren\'t any PubSub topics to subscribe to ({utils.getNowTimeText(includeSeconds = True)})')
            return

        print(f'Subscribing to {len(pubSubTopics)} PubSub topic(s)... ({utils.getNowTimeText(includeSeconds = True)})')
        await self.__pubSub.subscribe_topics(pubSubTopics)
        print(f'Finished subscribing to PubSub topic(s) ({utils.getNowTimeText(includeSeconds = True)})')

    async def __unsubscribeFromPubSubTopics(self):
        pubSubTopics = await self.__getAllPubSubTopics(validateAndRefresh = False)
        if not utils.hasItems(pubSubTopics):
            print(f'There aren\'t any PubSub topics to unsubscribe from ({utils.getNowTimeText(includeSeconds = True)})')
            return

        print(f'Unsubscribing from {len(pubSubTopics)} PubSub topic(s)... ({utils.getNowTimeText(includeSeconds = True)})')
        await self.__pubSub.unsubscribe_topics(pubSubTopics)
        print(f'Finished unsubscribing from PubSub topic(s) ({utils.getNowTimeText(includeSeconds = True)})')

    @commands.command(name = 'analogue')
    async def command_analogue(self, ctx: Context):
        await self.__analogueCommand.handleCommand(ctx)

    @commands.command(name = 'answer')
    async def command_answer(self, ctx: Context):
        await self.__answerCommand.handleCommand(ctx)

    @commands.command(name = 'clearchatband')
    async def command_clearchatband(self, ctx: Context):
        await self.__chatBandClearCommand.handleCommand(ctx)

    @commands.command(name = 'commands')
    async def command_commands(self, ctx: Context):
        await self.__commandsCommand.handleCommand(ctx)

    @commands.command(name = 'cuteness')
    async def command_cuteness(self, ctx: Context):
        await self.__cutenessCommand.handleCommand(ctx)

    @commands.command(name = 'cynansource')
    async def command_cynansource(self, ctx: Context):
        await self.__cynanSourceCommand.handleCommand(ctx)

    @commands.command(name = 'discord')
    async def command_discord(self, ctx: Context):
        await self.__discordCommand.handleCommand(ctx)

    @commands.command(name = 'givecuteness')
    async def command_givecuteness(self, ctx: Context):
        await self.__giveCutenessCommand.handleCommand(ctx)

    @commands.command(name = 'jisho')
    async def command_jisho(self, ctx: Context):
        await self.__jishoCommand.handleCommand(ctx)

    @commands.command(name = 'mycuteness')
    async def command_mycuteness(self, ctx: Context):
        await self.__myCutenessCommand.handleCommand(ctx)

    @commands.command(name = 'pbs')
    async def command_pbs(self, ctx: Context):
        await self.__pbsCommand.handleCommand(ctx)

    @commands.command(name = 'pkmon')
    async def command_pkmon(self, ctx: Context):
        await self.__pkMonCommand.handleCommand(ctx)

    @commands.command(name = 'pkmove')
    async def command_pkmove(self, ctx: Context):
        await self.__pkMoveCommand.handleCommand(ctx)

    @commands.command(name = 'race')
    async def command_race(self, ctx: Context):
        await self.__raceCommand.handleCommand(ctx)

    @commands.command(name = 'swquote')
    async def command_swquote(self, ctx: Context):
        await self.__swQuoteCommand.handleCommand(ctx)

    @commands.command(name = 'tamales')
    async def command_tamales(self, ctx: Context):
        await self.__tamalesCommand.handleCommand(ctx)

    @commands.command(name = 'time')
    async def command_time(self, ctx: Context):
        await self.__timeCommand.handleCommand(ctx)

    @commands.command(name = 'translate')
    async def command_translate(self, ctx: Context):
        await self.__translateCommand.handleCommand(ctx)

    @commands.command(name = 'trivia')
    async def command_trivia(self, ctx: Context):
        await self.__triviaCommand.handleCommand(ctx)

    @commands.command(name = 'triviascore')
    async def command_triviascore(self, ctx: Context):
        await self.__triviaScoreCommand.handleCommand(ctx)

    @commands.command(name = 'twitter')
    async def command_twitter(self, ctx: Context):
        await self.__twitterCommand.handleCommand(ctx)

    @commands.command(name = 'weather')
    async def command_weather(self, ctx: Context):
        await self.__weatherCommand.handleCommand(ctx)

    @commands.command(name = 'word')
    async def command_word(self, ctx: Context):
        await self.__wordCommand.handleCommand(ctx)
