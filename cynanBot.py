import asyncio
import locale
from typing import Dict, List

import CynanBotCommon.utils as utils
import twitchUtils
from authHelper import AuthHelper
from commands import (AbsCommand, AnalogueCommand, AnswerCommand,
                      CommandsCommand, CutenessCommand, DiccionarioCommand,
                      DiscordCommand, GiveCutenessCommand, JishoCommand,
                      JokeCommand, MyCutenessCommand, PbsCommand, PkMonCommand,
                      PkMoveCommand, RaceCommand, StubCommand, SwQuoteCommand,
                      TamalesCommand, TimeCommand, TranslateCommand,
                      TriviaCommand, TwitterCommand, WeatherCommand,
                      WordCommand)
from cutenessBoosterPack import CutenessBoosterPack
from cutenessRepository import CutenessRepository
from CynanBotCommon.analogueStoreRepository import AnalogueStoreRepository
from CynanBotCommon.chatBandManager import ChatBandManager
from CynanBotCommon.enEsDictionary import EnEsDictionary
from CynanBotCommon.funtoonRepository import FuntoonRepository
from CynanBotCommon.jishoHelper import JishoHelper
from CynanBotCommon.jokesRepository import JokesRepository
from CynanBotCommon.languagesRepository import LanguagesRepository
from CynanBotCommon.locationsRepository import LocationsRepository
from CynanBotCommon.nonceRepository import NonceRepository
from CynanBotCommon.pokepediaRepository import PokepediaRepository
from CynanBotCommon.starWarsQuotesRepository import StarWarsQuotesRepository
from CynanBotCommon.tamaleGuyRepository import TamaleGuyRepository
from CynanBotCommon.translationHelper import TranslationHelper
from CynanBotCommon.triviaGameRepository import TriviaGameRepository
from CynanBotCommon.triviaRepository import TriviaRepository
from CynanBotCommon.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.weatherRepository import WeatherRepository
from CynanBotCommon.websocketConnectionServer import WebsocketConnectionServer
from CynanBotCommon.wordOfTheDayRepository import WordOfTheDayRepository
from doubleCutenessHelper import DoubleCutenessHelper
from generalSettingsRepository import GeneralSettingsRepository
from messages import (AbsMessage, CatJamMessage, ChatBandMessage, CynanMessage,
                      DeerForceMessage, RatJamMessage, StubMessage)
from pointRedemptions import (AbsPointRedemption, PkmnBattleRedemption,
                              PkmnCatchRedemption, PkmnEvolveRedemption,
                              PkmnShinyRedemption, PotdPointRedemption,
                              StubPointRedemption, TriviaGameRedemption)
from TwitchIO.twitchio import Channel, Message
from TwitchIO.twitchio.ext import commands, pubsub
from TwitchIO.twitchio.ext.commands import Bot, Context
from TwitchIO.twitchio.ext.commands.errors import CommandNotFound
from TwitchIO.twitchio.ext.pubsub import PubSubChannelPointsMessage, PubSubPool
from TwitchIO.twitchio.ext.pubsub.topics import Topic
from user import User
from userIdsRepository import UserIdsRepository
from usersRepository import UsersRepository


class CynanBot(Bot):

    def __init__(
        self,
        analogueStoreRepository: AnalogueStoreRepository,
        authHelper: AuthHelper,
        chatBandManager: ChatBandManager,
        cutenessRepository: CutenessRepository,
        doubleCutenessHelper: DoubleCutenessHelper,
        enEsDictionary: EnEsDictionary,
        funtoonRepository: FuntoonRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        jishoHelper: JishoHelper,
        jokesRepository: JokesRepository,
        languagesRepository: LanguagesRepository,
        locationsRepository: LocationsRepository,
        nonceRepository: NonceRepository,
        pokepediaRepository: PokepediaRepository,
        starWarsQuotesRepository: StarWarsQuotesRepository,
        tamaleGuyRepository: TamaleGuyRepository,
        translationHelper: TranslationHelper,
        triviaGameRepository: TriviaGameRepository,
        triviaRepository: TriviaRepository,
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
            nick = 'CynanBot',
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
        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__doubleCutenessHelper: DoubleCutenessHelper = doubleCutenessHelper
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__twitchTokensRepository: TwitchTokensRepository = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__websocketConnectionServer: WebsocketConnectionServer = websocketConnectionServer

        #######################################
        ## Initialization of command objects ##
        #######################################

        self.__commandsCommand: AbsCommand = CommandsCommand(usersRepository)
        self.__discordCommand: AbsCommand = DiscordCommand(usersRepository)
        self.__pbsCommand: AbsCommand = PbsCommand(usersRepository)
        self.__raceCommand: AbsCommand = RaceCommand(usersRepository)
        self.__timeCommand: AbsCommand = TimeCommand(usersRepository)
        self.__twitterCommand: AbsCommand = TwitterCommand(usersRepository)

        if analogueStoreRepository is None:
            self.__analogueCommand: AbsCommand = StubCommand()
        else:
            self.__analogueCommand: AbsCommand = AnalogueCommand(analogueStoreRepository, usersRepository)

        if cutenessRepository is None or triviaGameRepository is None:
            self.__answerCommand: AbsCommand = StubCommand()
        else:
            self.__answerCommand: AbsCommand = AnswerCommand(cutenessRepository, doubleCutenessHelper, generalSettingsRepository, triviaGameRepository, usersRepository)

        if cutenessRepository is None:
            self.__cutenessCommand: AbsCommand = StubCommand()
            self.__giveCutenessCommand: AbsCommand = StubCommand()
            self.__myCutenessCommand: AbsCommand = StubCommand()
        else:
            self.__cutenessCommand: AbsCommand = CutenessCommand(cutenessRepository, userIdsRepository, usersRepository)
            self.__giveCutenessCommand: AbsCommand = GiveCutenessCommand(cutenessRepository, userIdsRepository, usersRepository)
            self.__myCutenessCommand: AbsCommand = MyCutenessCommand(cutenessRepository, usersRepository)

        if enEsDictionary is None:
            self.__diccionarioCommand: AbsCommand = StubCommand()
        else:
            self.__diccionarioCommand: AbsCommand = DiccionarioCommand(enEsDictionary, usersRepository)

        if jishoHelper is None:
            self.__jishoCommand: AbsCommand = StubCommand()
        else:
            self.__jishoCommand: AbsCommand = JishoCommand(jishoHelper, usersRepository)

        if jokesRepository is None:
            self.__jokeCommand: AbsCommand = StubCommand()
        else:
            self.__jokeCommand: AbsCommand = JokeCommand(jokesRepository, usersRepository)

        if pokepediaRepository is None:
            self.__pkMonCommand: AbsCommand = StubCommand()
            self.__pkMoveCommand: AbsCommand = StubCommand()
        else:
            self.__pkMonCommand: AbsCommand = PkMonCommand(pokepediaRepository, usersRepository)
            self.__pkMoveCommand: AbsCommand = PkMoveCommand(pokepediaRepository, usersRepository)

        if starWarsQuotesRepository is None:
            self.__swQuoteCommand: AbsCommand = StubCommand()
        else:
            self.__swQuoteCommand: AbsCommand = SwQuoteCommand(starWarsQuotesRepository, usersRepository)

        if tamaleGuyRepository is None:
            self.__tamalesCommand: AbsCommand = StubCommand()
        else:
            self.__tamalesCommand: AbsCommand = TamalesCommand(tamaleGuyRepository, usersRepository)

        if translationHelper is None:
            self.__translateCommand: AbsCommand = StubCommand()
        else:
            self.__translateCommand: AbsCommand = TranslateCommand(languagesRepository, translationHelper, usersRepository)

        if triviaRepository is None:
            self.__triviaCommand: AbsCommand = StubCommand()
        else:
            self.__triviaCommand: AbsCommand = TriviaCommand(generalSettingsRepository, triviaRepository, usersRepository)

        if locationsRepository is None or weatherRepository is None:
            self.__weatherCommand: AbsCommand = StubCommand()
        else:
            self.__weatherCommand: AbsCommand = WeatherCommand(locationsRepository, usersRepository, weatherRepository)

        if wordOfTheDayRepository is None:
            self.__wordCommand: AbsCommand = StubCommand()
        else:
            self.__wordCommand: AbsCommand = WordCommand(languagesRepository, usersRepository, wordOfTheDayRepository)

        ###############################################
        ## Initialization of message handler objects ##
        ###############################################

        self.__catJamMessage: AbsMessage = CatJamMessage(generalSettingsRepository, usersRepository)

        if chatBandManager is None:
            self.__chatBandMessage: AbsMessage = StubMessage()
        else:
            self.__chatBandMessage: AbsMessage = ChatBandMessage(chatBandManager, usersRepository)

        self.__cynanMessage: AbsMessage = CynanMessage(generalSettingsRepository, usersRepository)
        self.__deerForceMessage: AbsMessage = DeerForceMessage(generalSettingsRepository, usersRepository)
        self.__ratJamMessage: AbsMessage = RatJamMessage(generalSettingsRepository, usersRepository)

        ########################################################
        ## Initialization of point redemption handler objects ##
        ########################################################

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

        if triviaGameRepository is None:
            self.__triviaGamePointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__triviaGamePointRedemption: AbsPointRedemption = TriviaGameRedemption(generalSettingsRepository, triviaGameRepository)

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
            await self.__chatBandMessage.handleMessage(message)

            if await self.__cynanMessage.handleMessage(message):
                return

            if await self.__deerForceMessage.handleMessage(message):
                return

            if await self.__catJamMessage.handleMessage(message):
                return

            if await self.__ratJamMessage.handleMessage(message):
                return

        await self.handle_commands(message)

    async def event_pubsub_channel_points(self, event: PubSubChannelPointsMessage):
        twitchUserIdStr = str(event.channel_id)
        twitchUserNameStr = self.__userIdsRepository.fetchUserName(twitchUserIdStr)
        twitchUser = self.__usersRepository.getUser(twitchUserNameStr)
        twitchChannel = self.get_channel(twitchUser.getHandle())

        rewardId = event.reward.id
        userIdThatRedeemed = str(event.user.id)
        userNameThatRedeemed = event.user.name
        redemptionMessage = event.input

        if self.__generalSettingsRepository.isRewardIdPrintingEnabled() or twitchUser.isRewardIdPrintingEnabled():
            print(f'The Reward ID for {twitchUser.getHandle()} (userId \"{twitchUserIdStr}\") is \"{rewardId}\"')

        if twitchUser.isCutenessEnabled() and twitchUser.hasCutenessBoosterPacks():
            for cutenessBoosterPack in twitchUser.getCutenessBoosterPacks():
                if rewardId == cutenessBoosterPack.getRewardId():
                    await self.__handleIncreaseCutenessRewardRedeemed(
                        twitchChannel = twitchChannel,
                        cutenessBoosterPack = cutenessBoosterPack,
                        userIdThatRedeemed = userIdThatRedeemed,
                        userNameThatRedeemed = userNameThatRedeemed,
                        twitchUser = twitchUser
                    )
                    return

            if rewardId == twitchUser.getIncreaseCutenessDoubleRewardId():
                await self.__handleIncreaseCutenessDoubleRewardRedeemed(
                    twitchChannel = twitchChannel,
                    cutenessBoosterPacks = twitchUser.getCutenessBoosterPacks(),
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed,
                    twitchUser = twitchUser
                )
                return

        if twitchUser.isPicOfTheDayEnabled() and rewardId == twitchUser.getPicOfTheDayRewardId():
            await self.__potdPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchUser = twitchUser,
                redemptionMessage = redemptionMessage,
                userIdThatRedeemed = userIdThatRedeemed,
                userNameThatRedeemed = userNameThatRedeemed
            )
            return

        if twitchUser.isPkmnEnabled():
            if rewardId == twitchUser.getPkmnBattleRewardId():
                await self.__pkmnBattlePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                )
                return

            if rewardId == twitchUser.getPkmnCatchRewardId():
                await self.__pkmnCatchPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                )
                return

            if rewardId == twitchUser.getPkmnEvolveRewardId():
                await self.__pkmnEvolvePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    userIdThatRedemeed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                )
                return

            if rewardId == twitchUser.getPkmnShinyRewardId():
                await self.__pkmnShinyPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    userIdThatRedemeed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                )
                return

        if twitchUser.isTriviaGameEnabled() and rewardId == twitchUser.getTriviaGameRewardId():
            await self.__triviaGamePointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchUser = twitchUser,
                redemptionMessage = redemptionMessage,
                userIdThatRedemeed = userIdThatRedeemed,
                userNameThatRedeemed = userNameThatRedeemed
            )
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
        msgId = tags.get('msg-id')

        if not utils.isValidStr(msgId):
            return

        user = self.__usersRepository.getUser(channel.name)

        if user.isRaidLinkMessagingEnabled() and msgId == 'raid':
            await self.__handleRaidLinkMessaging(
                twitchChannel = channel,
                tags = tags,
                user = user
            )

    async def event_ready(self):
        print(f'{self.nick} is ready! ({utils.getNowTimeText(includeSeconds = True)})')
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

        if validateAndRefresh:
            for user in usersAndTwitchTokens:
                self.__twitchTokensRepository.validateAndRefreshAccessToken(
                    twitchClientId = self.__authHelper.requireTwitchClientId(),
                    twitchClientSecret = self.__authHelper.requireTwitchClientSecret(),
                    twitchHandle = user.getHandle()
                )

                usersAndTwitchTokens[user] = self.__twitchTokensRepository.getAccessToken(user.getHandle())

        for user in usersAndTwitchTokens:
            twitchAccessToken = usersAndTwitchTokens[user]

            userId = self.__userIdsRepository.fetchUserIdAsInt(
                userName = user.getHandle(),
                twitchAccessToken = twitchAccessToken,
                twitchClientId = self.__authHelper.requireTwitchClientId()
            )

            pubSubTopics.append(pubsub.channel_points(twitchAccessToken)[userId])

        return pubSubTopics

    async def __handleIncreaseCutenessDoubleRewardRedeemed(
        self,
        twitchChannel: Channel,
        cutenessBoosterPacks: List[CutenessBoosterPack],
        userIdThatRedeemed: str,
        userNameThatRedeemed: str,
        twitchUser: User
    ):
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.hasItems(cutenessBoosterPacks):
            raise ValueError(f'cutenessBoosterPacks argument is malformed: \"{cutenessBoosterPacks}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')

        print(f'Enabling double cuteness points in {twitchUser.getHandle()}...')
        self.__doubleCutenessHelper.beginDoubleCuteness(twitchUser.getHandle())

        # It's sort of not obvious what's going on here, but so what I'm trying to do is not
        # penalize the given user for redeeming double cuteness. Double cuteness should just cost
        # the user the same number of channel points that the baseline cuteness redemption is, and
        # so let's go ahead and multiply that by 2.
        incrementAmount = cutenessBoosterPacks[0].getAmount() * 2

        try:
            result = self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = twitchUser.getHandle(),
                userId = userIdThatRedeemed,
                userName = userNameThatRedeemed
            )

            await twitchUtils.safeSend(twitchChannel, f'✨ Double cuteness points enabled for the next {self.__cutenessRepository.getDoubleCutenessTimeSecondsStr()} seconds! Increase your cuteness now~ ✨ Also, cuteness for {userNameThatRedeemed} has increased to {result.getCutenessStr()} ✨')

            asyncio.create_task(twitchUtils.waitThenSend(
                messageable = twitchChannel,
                delaySeconds = self.__cutenessRepository.getDoubleCutenessTimeSeconds(),
                message = 'Double cuteness has ended! 😿'
            ))
        except ValueError:
            print(f'Error increasing cuteness for {userNameThatRedeemed} ({userIdThatRedeemed}) in {twitchUser.getHandle()}')
            await twitchUtils.safeSend(twitchChannel, f'⚠ Error increasing cuteness for {userNameThatRedeemed}')

    async def __handleIncreaseCutenessRewardRedeemed(
        self,
        twitchChannel: Channel,
        cutenessBoosterPack: CutenessBoosterPack,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str,
        twitchUser: User
    ):
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif cutenessBoosterPack is None:
            raise ValueError(f'cutenessBoosterPack argument is malformed: \"{cutenessBoosterPack}\"')
        elif not utils.isValidStr(userIdThatRedeemed):
            raise ValueError(f'userIdThatRedeemed argument is malformed: \"{userIdThatRedeemed}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')

        incrementAmount = cutenessBoosterPack.getAmount()

        if self.__doubleCutenessHelper.isWithinDoubleCuteness(twitchUser.getHandle()):
            incrementAmount = cutenessBoosterPack.getAmount() * 2

        try:
            self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = twitchUser.getHandle(),
                userId = userIdThatRedeemed,
                userName = userNameThatRedeemed
            )
        except ValueError:
            print(f'Error increasing cuteness for {userNameThatRedeemed} ({userIdThatRedeemed}) in {twitchUser.getHandle()}')
            await twitchUtils.safeSend(twitchChannel, f'⚠ Error increasing cuteness for {userNameThatRedeemed}')

    async def __handleRaidLinkMessaging(
        self,
        twitchChannel: Channel,
        tags: Dict,
        user: User
    ):
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif tags is None:
            raise ValueError(f'tags argument is malformed: \"{tags}\"')
        elif user is None:
            raise ValueError(f'user argument is malformed: \"{user}\"')

        raidedByName = tags.get('msg-param-displayName')
        if not utils.isValidStr(raidedByName):
            raidedByName = tags.get('display-name')
        if not utils.isValidStr(raidedByName):
            raidedByName = tags['login']

        raidSize = tags.get('msg-param-viewerCount')
        messageSuffix = f'😻 Raiders, if you could, I\'d really appreciate you clicking this link to watch the stream. It helps me on my path to partner. {user.getTwitchUrl()} Thank you! ✨'

        message = None
        if utils.isValidNum(raidSize) and raidSize >= 5:
            raidSizeStr = locale.format_string("%d", raidSize, grouping = True)
            message = f'Thank you for the raid of {raidSizeStr} {raidedByName}! {messageSuffix}'
        else:
            message = f'Thank you for the raid {raidedByName}! {messageSuffix}'

        print(f'{user.getHandle()} was raided by {raidedByName} ({utils.getNowTimeText()})')

        asyncio.create_task(twitchUtils.waitThenSend(
            messageable = twitchChannel,
            delaySeconds = self.__generalSettingsRepository.getRaidLinkMessagingDelay(),
            message = message
        ))

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

    @commands.command(name = 'commands')
    async def command_commands(self, ctx: Context):
        await self.__commandsCommand.handleCommand(ctx)

    @commands.command(name = 'cuteness')
    async def command_cuteness(self, ctx: Context):
        await self.__cutenessCommand.handleCommand(ctx)

    @commands.command(name = 'cynansource')
    async def command_cynansource(self, ctx: Context):
        await twitchUtils.safeSend(ctx, 'My source code is available here: https://github.com/charlesmadere/cynanbot')

    @commands.command(name = 'diccionario')
    async def command_diccionario(self, ctx: Context):
        await self.__diccionarioCommand.handleCommand(ctx)

    @commands.command(name = 'discord')
    async def command_discord(self, ctx: Context):
        await self.__discordCommand.handleCommand(ctx)

    @commands.command(name = 'givecuteness')
    async def command_givecuteness(self, ctx: Context):
        await self.__giveCutenessCommand.handleCommand(ctx)

    @commands.command(name = 'jisho')
    async def command_jisho(self, ctx: Context):
        await self.__jishoCommand.handleCommand(ctx)

    @commands.command(name = 'joke')
    async def command_joke(self, ctx: Context):
        await self.__jokeCommand.handleCommand(ctx)

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

    @commands.command(name = 'twitter')
    async def command_twitter(self, ctx: Context):
        await self.__twitterCommand.handleCommand(ctx)

    @commands.command(name = 'weather')
    async def command_weather(self, ctx: Context):
        await self.__weatherCommand.handleCommand(ctx)

    @commands.command(name = 'word')
    async def command_word(self, ctx: Context):
        await self.__wordCommand.handleCommand(ctx)
