import asyncio
import json
import locale
from datetime import datetime, timedelta
from json.decoder import JSONDecodeError
from typing import Dict, List

from twitchio.ext import commands
from twitchio.ext.commands.errors import CommandNotFound

import CynanBotCommon.utils as utils
from authHelper import AuthHelper
from cutenessRepository import CutenessRepository
from CynanBotCommon.analogueStoreRepository import AnalogueStoreRepository
from CynanBotCommon.enEsDictionary import EnEsDictionary
from CynanBotCommon.funtoonRepository import FuntoonRepository
from CynanBotCommon.jishoHelper import JishoHelper
from CynanBotCommon.jokesRepository import JokesRepository
from CynanBotCommon.locationsRepository import LocationsRepository
from CynanBotCommon.nonceRepository import NonceRepository
from CynanBotCommon.pokepediaRepository import PokepediaRepository
from CynanBotCommon.tamaleGuyRepository import TamaleGuyRepository
from CynanBotCommon.timedDict import TimedDict
from CynanBotCommon.triviaGameRepository import TriviaGameCheckResult, TriviaGameRepository
from CynanBotCommon.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.weatherRepository import WeatherRepository
from CynanBotCommon.wordOfTheDayRepository import WordOfTheDayRepository
from generalSettingsRepository import GeneralSettingsRepository
from user import User
from userIdsRepository import UserIdsRepository
from usersRepository import UsersRepository


class CynanBot(commands.Bot):

    def __init__(
        self,
        analogueStoreRepository: AnalogueStoreRepository,
        authHelper: AuthHelper,
        cutenessRepository: CutenessRepository,
        enEsDictionary: EnEsDictionary,
        funtoonRepository: FuntoonRepository,
        jishoHelper: JishoHelper,
        jokesRepository: JokesRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        locationsRepository: LocationsRepository,
        nonceRepository: NonceRepository,
        pokepediaRepository: PokepediaRepository,
        tamaleGuyRepository: TamaleGuyRepository,
        triviaGameRepository: TriviaGameRepository,
        twitchTokensRepository: TwitchTokensRepository,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        weatherRepository: WeatherRepository,
        wordOfTheDayRepository: WordOfTheDayRepository
    ):
        super().__init__(
            irc_token = authHelper.requireTwitchIrcAuthToken(),
            client_id = authHelper.requireTwitchClientId(),
            nick = 'CynanBot',
            prefix = '!',
            initial_channels = [ user.getHandle() for user in usersRepository.getUsers() ]
        )

        if analogueStoreRepository is None:
            raise ValueError(f'analogueStoreRepository argument is malformed: \"{analogueStoreRepository}\"')
        elif cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif enEsDictionary is None:
            raise ValueError(f'enEsDictionary argument is malformed: \"{enEsDictionary}\"')
        elif funtoonRepository is None:
            raise ValueError(f'funtoonRepository argument is malformed: \"{funtoonRepository}\"')
        elif jishoHelper is None:
            raise ValueError(f'jishHelper argument is malformed: \"{jishoHelper}\"')
        elif jokesRepository is None:
            raise ValueError(f'jokesRepository argument is malformed: \"{jokesRepository}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif locationsRepository is None:
            raise ValueError(f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif nonceRepository is None:
            raise ValueError(f'nonceRepository argument is malformed: \"{nonceRepository}\"')
        elif pokepediaRepository is None:
            raise ValueError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif tamaleGuyRepository is None:
            raise ValueError(f'tamaleGuyRepository argument is malformed: \"{tamaleGuyRepository}\"')
        elif triviaGameRepository is None:
            raise ValueError(f'triviaGameRepository argument is malformed: \"{triviaGameRepository}\"')
        elif twitchTokensRepository is None:
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif weatherRepository is None:
            raise ValueError(f'weatherRepository argument is malformed: \"{weatherRepository}\"')
        elif wordOfTheDayRepository is None:
            raise ValueError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')

        self.__analogueStoreRepository = analogueStoreRepository
        self.__authHelper = authHelper
        self.__cutenessRepository = cutenessRepository
        self.__enEsDictionary = enEsDictionary
        self.__funtoonRepository = funtoonRepository
        self.__jishoHelper = jishoHelper
        self.__jokesRepository = jokesRepository
        self.__generalSettingsRepository = generalSettingsRepository
        self.__locationsRepository = locationsRepository
        self.__nonceRepository = nonceRepository
        self.__pokepediaRepository = pokepediaRepository
        self.__tamaleGuyRepository = tamaleGuyRepository
        self.__triviaGameRepository = triviaGameRepository
        self.__twitchTokensRepository = twitchTokensRepository
        self.__userIdsRepository = userIdsRepository
        self.__usersRepository = usersRepository
        self.__weatherRepository = weatherRepository
        self.__wordOfTheDayRepository = wordOfTheDayRepository

        self.__cutenessDoubleEndTimes = TimedDict(timedelta(seconds = self.__cutenessRepository.getDoubleCutenessTimeSeconds()))
        self.__lastAnalogueStockMessageTimes = TimedDict(timedelta(minutes = 1))
        self.__lastCatJamMessageTimes = TimedDict(timedelta(minutes = 20))
        self.__lastCutenessLeaderboardMessageTimes = TimedDict(timedelta(seconds = 30))
        self.__lastCutenessRedeemedMessageTimes = TimedDict(timedelta(seconds = 30))
        self.__lastCynanMessageTime = datetime.utcnow() - timedelta(days = 1)
        self.__lastDeerForceMessageTimes = TimedDict(timedelta(minutes = 20))
        self.__lastDiccionarioMessageTimes = TimedDict(timedelta(seconds = 15))
        self.__lastJishoMessageTimes = TimedDict(timedelta(seconds = 15))
        self.__lastJokeMessageTimes = TimedDict(timedelta(minutes = 1))
        self.__lastPkMonMessageTimes = TimedDict(timedelta(seconds = 30))
        self.__lastPkMoveMessageTimes = TimedDict(timedelta(seconds = 30))
        self.__lastRaceMessageTimes = TimedDict(timedelta(minutes = 2))
        self.__lastRatJamMessageTimes = TimedDict(timedelta(minutes = 20))
        self.__lastTamalesMessageTimes = TimedDict(timedelta(minutes = 5))
        self.__lastTriviaMessageTimes = TimedDict(timedelta(minutes = 5))
        self.__lastWeatherMessageTimes = TimedDict(timedelta(minutes = 1))
        self.__lastWotdMessageTimes = TimedDict(timedelta(seconds = 15))

    async def event_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        else:
            raise error

    async def event_message(self, message):
        if await self.__handleMessageFromCynan(message):
            return

        if await self.__handleDeerForceMessage(message):
            return

        if await self.__handleCatJamMessage(message):
            return

        if await self.__handleRatJamMessage(message):
            return

        await self.handle_commands(message)

    async def event_raw_pubsub(self, data):
        if 'error' in data and len(data['error']) >= 1:
            print(f'({utils.getNowTimeText(includeSeconds = True)}) Received pub sub error: {data}')

            if data['error'] == 'ERR_BADAUTH':
                await self.__validateAndRefreshTokensAndResubscribe(nonce = data.get('nonce'))
        elif 'type' not in data:
            print(f'({utils.getNowTimeText(includeSeconds = True)}) Received pub sub event without \"type\": {data}')
        elif data['type'] == 'PONG' or data['type'] == 'RESPONSE':
            print(f'({utils.getNowTimeText(includeSeconds = True)}) Received pub sub event: {data}')
        elif data['type'] != 'MESSAGE' or 'data' not in data or 'message' not in data['data']:
            print(f'({utils.getNowTimeText(includeSeconds = True)}) Received unusual pub sub event: {data}')
        else:
            jsonResponse = None

            try:
                jsonResponse = json.loads(data['data']['message'])
            except JSONDecodeError as e:
                print(f'Exception occurred when attempting to decode pub sub message into JSON: {e}')

            if jsonResponse is not None and jsonResponse.get('type') == 'reward-redeemed':
                await self.__handleRewardRedeemed(jsonResponse)

    async def event_raw_usernotice(self, channel, tags: Dict):
        msgId = tags.get('msg-id')

        if not utils.isValidStr(msgId):
            return

        user = self.__usersRepository.getUser(channel.name)

        if msgId == 'raid':
            await self.__handleRaidLinkMessaging(
                tags = tags,
                user = user,
                twitchChannel = channel
            )

    async def event_ready(self):
        print(f'{self.nick} is ready!')
        await self.__subscribeToEvents(self.__usersRepository.getUsers())

    async def __handleCatJamMessage(self, message) -> bool:
        user = self.__usersRepository.getUser(message.channel.name)

        if not user.isCatJamEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if 'catJAM' in splits and self.__lastCatJamMessageTimes.isReadyAndUpdate(user.getHandle()):
            await message.channel.send('catJAM')
            return True
        else:
            return False

    async def __handleDeerForceMessage(self, message) -> bool:
        user = self.__usersRepository.getUser(message.channel.name)
        text = utils.cleanStr(message.content)

        if text.lower() == 'd e e r f o r c e' and self.__lastDeerForceMessageTimes.isReadyAndUpdate(user.getHandle()):
            await message.channel.send('D e e R F o r C e')
            return True
        else:
            return False

    async def __handleIncreaseCutenessDoubleRewardRedeemed(
        self,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str,
        twitchUser: User,
        twitchChannel
    ):
        print(f'Enabling double cuteness points in {twitchUser.getHandle()}...')

        self.__cutenessDoubleEndTimes.update(twitchUser.getHandle())

        try:
            result = self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = 3,
                twitchChannel = twitchUser.getHandle(),
                userId = userIdThatRedeemed,
                userName = userNameThatRedeemed
            )

            await twitchChannel.send(f'✨ Double cuteness points enabled for the next {self.__cutenessRepository.getDoubleCutenessTimeSecondsStr()} seconds! Increase your cuteness now~ ✨ Also, cuteness for {userNameThatRedeemed} has increased to {result.getCutenessStr()} ✨')

            asyncio.create_task(self.__sendDelayedMessage(
                messageable = twitchChannel,
                delaySeconds = self.__cutenessRepository.getDoubleCutenessTimeSeconds(),
                message = 'Double cuteness has ended! 😿'
            ))
        except ValueError:
            print(f'Error increasing cuteness for {userNameThatRedeemed} ({userIdThatRedeemed}) in {twitchUser.getHandle()}')
            await twitchChannel.send(f'⚠ Error increasing cuteness for {userNameThatRedeemed}')

    async def __handleIncreaseCutenessRewardRedeemed(
        self,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str,
        twitchUser: User,
        twitchChannel
    ):
        incrementAmount = 1

        if not self.__cutenessDoubleEndTimes.isReady(twitchUser.getHandle()):
            incrementAmount = 2

        try:
            result = self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = twitchUser.getHandle(),
                userId = userIdThatRedeemed,
                userName = userNameThatRedeemed
            )

            if self.__lastCutenessRedeemedMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
                await twitchChannel.send(f'✨ @{userNameThatRedeemed} has increased cuteness~ ✨ Their cuteness has increased to {result.getCutenessStr()} ✨')
        except ValueError:
            print(f'Error increasing cuteness for {userNameThatRedeemed} ({userIdThatRedeemed}) in {twitchUser.getHandle()}')
            await twitchChannel.send(f'⚠ Error increasing cuteness for {userNameThatRedeemed}')

    async def __handleMessageFromCynan(self, message) -> bool:
        if message.author.name.lower() != 'cynanmachae'.lower():
            return False

        now = datetime.utcnow()

        if now > self.__lastCynanMessageTime + timedelta(hours = 4):
            self.__lastCynanMessageTime = now
            await message.channel.send_me('waves to @CynanMachae 👋')
            return True
        else:
            return False

    async def __handlePkmnBattleRewardRedeemed(
        self,
        redemptionMessage: str,
        userNameThatRedeemed: str,
        twitchUser: User,
        twitchChannel
    ):
        splits = utils.getCleanedSplits(redemptionMessage)
        if not utils.hasItems(splits):
            await twitchChannel.send(f'⚠ @{userNameThatRedeemed} you must specify the exact user name of the person you want to fight')
            return

        opponentUserName = utils.removePreceedingAt(splits[0])

        self.__funtoonRepository.pkmnBattle(
            userThatRedeemed = userNameThatRedeemed,
            userToBattle = opponentUserName,
            twitchChannel = twitchUser.getHandle()
        )

    async def __handlePkmnCatchRewardRedeemed(
        self,
        userNameThatRedeemed: str,
        twitchUser: User,
        twitchChannel
    ):
        if self.__generalSettingsRepository.isFuntoonApiEnabled():
            if self.__funtoonRepository.pkmnCatch(
                userThatRedeemed = userNameThatRedeemed,
                twitchChannel = twitchUser.getHandle()
            ):
                return

        await twitchChannel.send(f'!catch {userNameThatRedeemed}')

    async def __handlePkmnEvolveRewardRedeemed(
        self,
        userNameThatRedeemed: str,
        twitchUser: User,
        twitchChannel
    ):
        if self.__generalSettingsRepository.isFuntoonApiEnabled():
            if self.__funtoonRepository.pkmnGiveEvolve(
                userThatRedeemed = userNameThatRedeemed,
                twitchChannel = twitchUser.getHandle()
            ):
                return

        await twitchChannel.send(f'!freeevolve {userNameThatRedeemed}')

    async def __handlePotdRewardRedeemed(
        self,
        userNameThatRedeemed: str,
        twitchUser: User,
        twitchChannel
    ):
        print(f'Sending POTD to {userNameThatRedeemed} in {twitchUser.getHandle()}...')

        try:
            picOfTheDay = twitchUser.fetchPicOfTheDay()
            await twitchChannel.send(f'@{userNameThatRedeemed} here\'s the POTD: {picOfTheDay}')
        except FileNotFoundError:
            await twitchChannel.send(f'⚠ {twitchUser.getHandle()}\'s POTD file is missing!')
        except ValueError:
            await twitchChannel.send(f'⚠ {twitchUser.getHandle()}\'s POTD content is malformed!')

    async def __handleRaidLinkMessaging(
        self,
        tags: Dict,
        user: User,
        twitchChannel
    ):
        if tags is None:
            raise ValueError(f'tags argument is malformed: \"{tags}\"')
        elif user is None:
            raise ValueError(f'user argument is malformed: \"{user}\"')
        elif twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        if not user.isRaidLinkMessagingEnabled():
            return

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

        asyncio.create_task(self.__sendDelayedMessage(
            messageable = twitchChannel,
            delaySeconds = self.__generalSettingsRepository.getRaidLinkMessagingDelay(),
            message = message
        ))

    async def __handleRatJamMessage(self, message) -> bool:
        user = self.__usersRepository.getUser(message.channel.name)

        if not user.isRatJamEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if 'ratJAM' in splits and self.__lastRatJamMessageTimes.isReadyAndUpdate(user.getHandle()):
            await message.channel.send('ratJAM')
            return True
        else:
            return False

    async def __handleRewardRedeemed(self, jsonResponse):
        if jsonResponse is None:
            raise ValueError(f'jsonResponse argument is malformed: \"{jsonResponse}\"')

        redemptionJson = jsonResponse['data']['redemption']
        twitchUserId = redemptionJson['channel_id']
        twitchUser = None

        for user in self.__usersRepository.getUsers():
            twitchAccessToken = self.__twitchTokensRepository.getAccessToken(user.getHandle())

            if not utils.isValidStr(twitchAccessToken):
                continue

            userId = self.__userIdsRepository.fetchUserId(
                userName = user.getHandle(),
                twitchAccessToken = twitchAccessToken,
                twitchClientId = self.__authHelper.requireTwitchClientId(),
            )

            if twitchUserId.lower() == userId.lower():
                twitchUser = user
                break

        if twitchUser is None:
            raise RuntimeError(f'Unable to find User with ID: \"{twitchUserId}\"')

        # Don't forget to check this if statement if you're having trouble with redemption reward
        # monitoring for specific users!
        if not twitchUser.isCutenessEnabled() and not twitchUser.isPicOfTheDayEnabled() and not twitchUser.isPkmnEnabled() and not twitchUser.isTriviaGameEnabled():
            return

        increaseCutenessDoubleRewardId = twitchUser.getIncreaseCutenessDoubleRewardId()
        increaseCutenessRewardId = twitchUser.getIncreaseCutenessRewardId()
        potdRewardId = twitchUser.getPicOfTheDayRewardId()
        pkmnBattleRewardId = twitchUser.getPkmnBattleRewardId()
        pkmnCatchRewardId = twitchUser.getPkmnCatchRewardId()
        pkmnEvolveRewardId = twitchUser.getPkmnEvolveRewardId()
        pkmnShinyRewardId = twitchUser.getPkmnShinyRewardId()
        triviaGameRewardId = twitchUser.getTriviaGameRewardId()

        rewardId = utils.getStrFromDict(redemptionJson['reward'], 'id')
        userIdThatRedeemed = utils.getStrFromDict(redemptionJson['user'], 'id')
        userNameThatRedeemed = redemptionJson['user']['display_name']
        redemptionMessage = utils.cleanStr(redemptionJson.get('user_input'))
        twitchChannel = self.get_channel(twitchUser.getHandle())

        if twitchUser.isCutenessEnabled() and rewardId == increaseCutenessRewardId:
            await self.__handleIncreaseCutenessRewardRedeemed(
                userIdThatRedeemed = userIdThatRedeemed,
                userNameThatRedeemed = userNameThatRedeemed,
                twitchUser = twitchUser,
                twitchChannel = twitchChannel
            )
        elif twitchUser.isCutenessEnabled() and rewardId == increaseCutenessDoubleRewardId:
            await self.__handleIncreaseCutenessDoubleRewardRedeemed(
                userIdThatRedeemed = userIdThatRedeemed,
                userNameThatRedeemed = userNameThatRedeemed,
                twitchUser = twitchUser,
                twitchChannel = twitchChannel
            )
        elif twitchUser.isPicOfTheDayEnabled() and rewardId == potdRewardId:
            await self.__handlePotdRewardRedeemed(
                userNameThatRedeemed = userNameThatRedeemed,
                twitchUser = twitchUser,
                twitchChannel = twitchChannel
            )
        elif twitchUser.isPkmnEnabled() and rewardId == pkmnBattleRewardId:
            await self.__handlePkmnBattleRewardRedeemed(
                redemptionMessage = redemptionMessage,
                userNameThatRedeemed = userNameThatRedeemed,
                twitchUser = twitchUser,
                twitchChannel = twitchChannel
            )
        elif twitchUser.isPkmnEnabled() and rewardId == pkmnCatchRewardId:
            await self.__handlePkmnCatchRewardRedeemed(
                userNameThatRedeemed = userNameThatRedeemed,
                twitchUser = twitchUser,
                twitchChannel = twitchChannel
            )
        elif twitchUser.isPkmnEnabled() and rewardId == pkmnEvolveRewardId:
            await self.__handlePkmnEvolveRewardRedeemed(
                userNameThatRedeemed = userNameThatRedeemed,
                twitchUser = twitchUser,
                twitchChannel = twitchChannel
            )
        elif twitchUser.isPkmnEnabled() and rewardId == pkmnShinyRewardId:
            await twitchChannel.send(f'!freeshiny {userNameThatRedeemed}')
        elif twitchUser.isTriviaGameEnabled() and rewardId == triviaGameRewardId:
            await self.__handleTriviaGameRewardRedeemed(
                userIdThatRedeemed = userIdThatRedeemed,
                userNameThatRedeemed = userNameThatRedeemed,
                twitchUser = twitchUser,
                twitchChannel = twitchChannel
            )
        else:
            print(f'The Reward ID for {twitchUser.getHandle()} is \"{rewardId}\"')

    async def __handleTriviaGameRewardRedeemed(
        self,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str,
        twitchUser: User,
        twitchChannel
    ):
        try:
            response = self.__triviaGameRepository.fetchTrivia()
            self.__triviaGameRepository.setUserIdThatRedeemed(userIdThatRedeemed)

            points = self.__generalSettingsRepository.getTriviaGamePoints()
            if twitchUser.hasTriviaGamePoints():
                points = twitchUser.getTriviaGamePoints()
            pointsStr = locale.format_string("%d", points, grouping = True)

            seconds = self.__generalSettingsRepository.getWaitForTriviaAnswerDelay()
            if twitchUser.hasWaitForTriviaAnswerDelay():
                seconds = twitchUser.getWaitForTriviaAnswerDelay()
            secondsStr = locale.format_string("%d", seconds, grouping = True)

            await twitchChannel.send(f'🎓 {userNameThatRedeemed} has started the trivia game! The first to use the !answer command to answer this trivia question will win {pointsStr} cuteness points! You have {secondsStr} seconds! 🎓')
            await twitchChannel.send(response.toPromptStr())

            asyncio.create_task(self.__handleTriviaGameAnswer(
                delaySeconds = seconds,
                twitchChannel = twitchChannel
            ))
        except (RuntimeError, ValueError):
            print(f'Error retrieving trivia')
            await twitchChannel.send('⚠ Error retrieving trivia')

    async def __handleTriviaGameAnswer(self, delaySeconds: int, twitchChannel):
        await asyncio.sleep(delaySeconds)

        if self.__triviaGameRepository.isAnswered():
            return

        self.__triviaGameRepository.setAnswered()
        response = self.__triviaGameRepository.fetchTrivia()
        await twitchChannel.send(f'😿 Sorry, there is no winner! The answer was: {response.getCorrectAnswer()}')

    async def __sendDelayedMessage(self, messageable, delaySeconds: int, message: str):
        if messageable is None:
            raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidNum(delaySeconds):
            raise ValueError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif delaySeconds < 1:
            raise ValueError(f'delaySeconds argument is out of bounds: {delaySeconds}')
        elif not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        await asyncio.sleep(delaySeconds)
        await messageable.send(message)

    async def __subscribeToEvents(self, users: List[User]):
        if not utils.hasItems(users):
            print(f'Given an empty list of users to subscribe to events for, will not subscribe to any events')
            return

        subscribeUsers = dict()

        for user in users:
            twitchAccessToken = self.__twitchTokensRepository.getAccessToken(user.getHandle())

            if utils.isValidStr(twitchAccessToken):
                subscribeUsers[user] = twitchAccessToken

        if not utils.hasItems(subscribeUsers):
            print(f'Found no users with a Twitch access token, not subscribing to any events')
            return

        print(f'Subscribing to events for {len(subscribeUsers)} user(s)...')

        for user in subscribeUsers:
            userId = self.__userIdsRepository.fetchUserId(
                userName = user.getHandle(),
                twitchAccessToken = subscribeUsers[user],
                twitchClientId = self.__authHelper.requireTwitchClientId()
            )

            # we could subscribe to multiple topics, but for now, just channel points
            topics = [ f'channel-points-channel-v1.{userId}' ]

            # subscribe to pubhub channel points events
            nonce = await self.pubsub_subscribe(twitchAccessToken, *topics)

            # save the nonce, we'll need to use it later if the token used for this user's
            # connection has to be refreshed
            self.__nonceRepository.setNonce(user.getHandle(), nonce)

            print(f'Subscribed to events for {user.getHandle()} (userId: \"{userId}\", nonce: \"{nonce}\")')

        print(f'Finished subscribing to events for {len(subscribeUsers)} user(s)')

    async def __validateAndRefreshTokensAndResubscribe(self, nonce: str):
        print(f'Validating and refreshing tokens... (nonce: \"{nonce}\")')

        users = self.__usersRepository.getUsers()
        resubscribeUsers = list()

        for user in users:
            if not utils.isValidStr(nonce) or nonce == self.__nonceRepository.getNonce(user.getHandle()):
                resubscribeUsers.append(user)

        if not utils.hasItems(resubscribeUsers):
            print(f'Found no users to validate and refresh tokens for (nonce: \"{nonce}\")')
            return

        for user in resubscribeUsers:
            self.__twitchTokensRepository.validateAndRefreshAccessToken(
                twitchClientId = self.__authHelper.requireTwitchClientId(),
                twitchClientSecret = self.__authHelper.requireTwitchClientSecret(),
                twitchHandle = user.getHandle()
            )

        await self.__subscribeToEvents(resubscribeUsers)
        print(f'Finished validating and refreshing {len(resubscribeUsers)} token(s) (nonce: \"{nonce}\")')

    @commands.command(name = 'analogue')
    async def command_analogue(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isAnalogueEnabled():
            return
        elif not self.__lastAnalogueStockMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        includePrices = 'includePrices' in splits

        try:
            result = self.__analogueStoreRepository.fetchStoreStock()
            await ctx.send(result.toStr(includePrices = includePrices))
        except (RuntimeError, ValueError):
            print(f'Error fetching Analogue stock in {user.getHandle()}')
            await ctx.send('⚠ Error fetching Analogue stock')

    @commands.command(name = 'answer')
    async def command_answer(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isTriviaGameEnabled():
            return
        elif self.__triviaGameRepository.isAnswered():
            return

        seconds = self.__generalSettingsRepository.getWaitForTriviaAnswerDelay()
        if user.hasWaitForTriviaAnswerDelay():
            seconds = user.getWaitForTriviaAnswerDelay()

        if not self.__triviaGameRepository.isWithinAnswerWindow(seconds):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await ctx.send('⚠ You must provide the exact answer with the !answer command.')
            return

        answer = ' '.join(splits[1:])
        userId = str(ctx.author.id)

        checkResult = self.__triviaGameRepository.check(
            answer = answer,
            userId = userId
        )

        if checkResult is TriviaGameCheckResult.INCORRECT:
            answerStr = self.__triviaGameRepository.fetchTrivia().getCorrectAnswer()
            await ctx.send(f'😿 Sorry, that is not the right answer. The correct answer was: {answerStr}')
            return
        elif checkResult is not TriviaGameCheckResult.CORRECT:
            print(f'Encounted a strange TriviaGameCheckResult when checking the answer to a trivia question: \"{checkResult}\"')
            await ctx.send(f'⚠ Sorry, a \"{checkResult}\" error occurred when checking your answer to the trivia question.')
            return

        cutenessPoints = self.__generalSettingsRepository.getTriviaGamePoints()
        if user.hasTriviaGamePoints():
            cutenessPoints = user.getTriviaGamePoints()

        try:
            cutenessResult = self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = cutenessPoints,
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = ctx.author.name
            )

            await ctx.send(f'🎉 Congratulations {ctx.author.name}! 🎉 You are correct! 🎉 Your new cuteness is now {cutenessResult.getCutenessStr()}~ ✨')
        except ValueError:
            print(f'Error increasing cuteness for {ctx.author.name} ({userId}) in {user.getHandle()}')
            await ctx.send(f'⚠ Error increasing cuteness for {ctx.author.name}')

    @commands.command(name = 'commands')
    async def command_commands(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)
        commands = [ '!cynansource' ]

        if user.hasDiscord():
            commands.append('!discord')

        if user.hasSpeedrunProfile():
            commands.append('!pbs')

        if user.hasTimeZones():
            commands.append('!time')

        if user.hasTwitter():
            commands.append('!twitter')

        if user.isAnalogueEnabled():
            commands.append('!analogue')

        if user.isCutenessEnabled():
            commands.append('!cuteness')
            commands.append('!mycuteness')

            if user.isGiveCutenessEnabled() and ctx.author.is_mod:
                commands.append('!givecuteness')

        if user.isDiccionarioEnabled():
            commands.append('!diccionario')

        if user.isJishoEnabled():
            commands.append('!jisho')

        if user.isJokesEnabled():
            commands.append('!joke')

        if user.isPokepediaEnabled():
            commands.append('!pkmon')
            commands.append('!pkmove')

        if user.isTamalesEnabled():
            commands.append('!tamales')

        if user.isTriviaEnabled() and not user.isTriviaGameEnabled():
            commands.append('!trivia')

        if user.isWeatherEnabled():
            commands.append('!weather')

        if user.isWordOfTheDayEnabled():
            commands.append('!word')

        commands.sort()
        commandsString = ', '.join(commands)

        await ctx.send(f'My commands: {commandsString}')

    @commands.command(name = 'cuteness')
    async def command_cuteness(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastCutenessLeaderboardMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)

        userName = None
        if len(splits) >= 2:
            userName = splits[1]

        if not utils.isValidStr(userName):
            result = self.__cutenessRepository.fetchLeaderboard(user.getHandle())

            if result.hasEntries():
                await ctx.send(f'✨ Cuteness leaderboard — {result.toStr()} ✨')
            else:
                await ctx.send('😿 Unfortunately the cuteness leaderboard is empty 😿')
        else:
            userName = utils.removePreceedingAt(userName)

            try:
                result = self.__cutenessRepository.fetchCuteness(
                    twitchChannel = user.getHandle(),
                    userName = userName
                )

                if result.hasCuteness():
                    await ctx.send(f'✨ {userName}\'s cuteness: {result.getCutenessStr()} ✨')
                else:
                    await ctx.send(f'😿 Unfortunately {userName} has no cuteness 😿')
            except ValueError:
                print(f'Unable to find \"{userName}\" in the cuteness database')
                await ctx.send(f'⚠ Unable to find \"{userName}\" in the cuteness database')

    @commands.command(name = 'cynansource')
    async def command_cynansource(self, ctx):
        await ctx.send('My source code is available here: https://github.com/charlesmadere/cynanbot')

    @commands.command(name = 'diccionario')
    async def command_diccionario(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isDiccionarioEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastDiccionarioMessageTimes.isReady(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)

        if len(splits) < 2:
            await ctx.send('⚠ A search term is necessary for the !diccionario command. Example: !diccionario beer')
            return

        query = ' '.join(splits[1:])

        try:
            result = self.__enEsDictionary.search(query)
            self.__lastDiccionarioMessageTimes.update(user.getHandle())
            await ctx.send(result.toStr())
        except (RuntimeError, ValueError):
            print(f'Error searching Spanish-English Dictionary for \"{query}\" in {user.getHandle()}')
            await ctx.send(f'⚠ Error searching Spanish-English Dictionary for \"{query}\"')

    @commands.command(name = 'discord')
    async def command_discord(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasDiscord():
            return

        discord = user.getDiscordUrl()
        await ctx.send(f'{user.getHandle()}\'s discord: {discord}')

    @commands.command(name = 'givecuteness')
    async def command_givecuteness(self, ctx):
        if not ctx.author.is_mod:
            return

        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled() or not user.isGiveCutenessEnabled():
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 3:
            await ctx.send(f'⚠ Username and amount is necessary for the !givecuteness command. Example: !givecuteness {user.getHandle()} 5')
            return

        userName = splits[1]
        if not utils.isValidStr(userName):
            print(f'Username is malformed: \"{userName}\"')
            await ctx.send(f'⚠ Username argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        incrementAmountStr = splits[2]
        if not utils.isValidStr(incrementAmountStr):
            print(f'Increment amount is malformed: \"{incrementAmountStr}\"')
            await ctx.send(f'⚠ Increment amount argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        try:
            incrementAmount = int(incrementAmountStr)
        except (SyntaxError, ValueError):
            print(f'Unable to convert increment amount into an int: \"{incrementAmountStr}\"')
            await ctx.send(f'⚠ Increment amount argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        userName = utils.removePreceedingAt(userName)

        try:
            userId = self.__userIdsRepository.fetchUserId(userName = userName)
        except ValueError:
            print(f'Attempted to give cuteness to \"{userName}\", but their user ID does not exist in the database')
            await ctx.send(f'⚠ Unable to give cuteness to \"{userName}\", they don\'t currently exist in the database')
            return

        try:
            result = self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = userName
            )

            await ctx.send(f'✨ Cuteness for {userName} is now {result.getCutenessStr()} ✨')
        except ValueError:
            print(f'Error incrementing cuteness by {incrementAmount} for {userName} ({userId}) in {user.getHandle()}')
            await ctx.send(f'⚠ Error incrementing cuteness for {userName}')

    @commands.command(name = 'jisho')
    async def command_jisho(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isJishoEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastJishoMessageTimes.isReady(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await ctx.send('⚠ A search term is necessary for the !jisho command. Example: !jisho 食べる')
            return

        query = splits[1]
        self.__lastJishoMessageTimes.update(user.getHandle())

        try:
            result = self.__jishoHelper.search(query)
            await ctx.send(result.toStr())
        except (RuntimeError, ValueError):
            print(f'Error searching Jisho for \"{query}\" in {user.getHandle()}')
            await ctx.send(f'⚠ Error searching Jisho for \"{query}\"')

    @commands.command(name = 'joke')
    async def command_joke(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isJokesEnabled():
            return
        elif not self.__lastJokeMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        try:
            result = self.__jokesRepository.fetchJoke()
            await ctx.send(result.toStr())
        except (RuntimeError, ValueError):
            print(f'Error fetching joke of the day in {user.getHandle()}')
            await ctx.send('⚠ Error fetching joke of the day')

    @commands.command(name = 'mycuteness')
    async def command_mycuteness(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled():
            return

        userId = str(ctx.author.id)

        try:
            result = self.__cutenessRepository.fetchCutenessAndLocalLeaderboard(
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = ctx.author.name
            )

            if result.hasCuteness() and result.hasLocalLeaderboard():
                await ctx.send(f'✨ {ctx.author.name}\'s cuteness is {result.getCutenessStr()}, and their local leaderboard is: {result.getLocalLeaderboardStr()} ✨')
            elif result.hasCuteness():
                await ctx.send(f'✨ {ctx.author.name}\'s cuteness is {result.getCutenessStr()} ✨')
            else:
                await ctx.send(f'😿 {ctx.author.name} has no cuteness 😿')
        except ValueError:
            print(f'Error retrieving cuteness for {ctx.author.name} ({userId}) in {user.getHandle()}')
            await ctx.send(f'⚠ Error retrieving cuteness for {ctx.author.name}')

    @commands.command(name = 'pbs')
    async def command_pbs(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasSpeedrunProfile():
            return

        speedrunProfile = user.getSpeedrunProfile()
        await ctx.send(f'{user.getHandle()}\'s speedrun profile: {speedrunProfile}')

    @commands.command(name = 'pkmon')
    async def command_pkmon(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isPokepediaEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastPkMonMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await ctx.send('⚠ A Pokémon name is necessary for the !pkmon command. Example: !pkmon charizard')
            return

        name = splits[1]

        try:
            mon = self.__pokepediaRepository.searchPokemon(name)
            strList = mon.toStrList()

            for s in strList:
                await ctx.send(s)
        except (RuntimeError, ValueError):
            print(f'Error retrieving Pokemon \"{name}\"')
            await ctx.send(f'⚠ Error retrieving Pokémon \"{name}\"')

    @commands.command(name = 'pkmove')
    async def command_pkmove(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isPokepediaEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastPkMoveMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await ctx.send('⚠ A move name is necessary for the !pkmove command. Example: !pkmove fire spin')
            return

        name = ' '.join(splits[1:])

        try:
            move = self.__pokepediaRepository.searchMoves(name)
            strList = move.toStrList()

            for s in strList:
                await ctx.send(s)
        except (RuntimeError, ValueError):
            print(f'Error retrieving Pokemon move \"{name}\"')
            await ctx.send(f'⚠ Error retrieving Pokémon move \"{name}\"')

    @commands.command(name = 'race')
    async def command_race(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isRaceEnabled() or not ctx.author.is_mod:
            return
        elif not self.__lastRaceMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        await ctx.send('!race')

    @commands.command(name = 'tamales')
    async def command_tamales(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isTamalesEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastTamalesMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        try:
            storeStock = self.__tamaleGuyRepository.fetchStoreStock()
            await ctx.send(storeStock.toStr())
        except (RuntimeError, ValueError):
            print('Error retrieving Tamale Guy store stock')
            await ctx.send('⚠ Error retrieving Tamale Guy store stock')

    @commands.command(name = 'time')
    async def command_time(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasTimeZones():
            return

        timeZones = user.getTimeZones()
        first = True
        text = ''

        for timeZone in timeZones:
            localTime = datetime.now(timeZone)

            if first:
                first = False
                formattedTime = utils.formatTime(localTime)
                text = f'🕰️ The local time for {user.getHandle()} is {formattedTime}.'
            else:
                formattedTime = utils.formatTimeShort(localTime)
                timeZoneName = timeZone.tzname(datetime.utcnow())
                text = f'{text} {timeZoneName} time is {formattedTime}.'

        await ctx.send(text)

    @commands.command(name = 'trivia')
    async def command_trivia(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isTriviaEnabled():
            return
        elif user.isTriviaGameEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastTriviaMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        try:
            response = self.__triviaGameRepository.fetchTrivia()
            await ctx.send(response.toPromptStr())

            asyncio.create_task(self.__sendDelayedMessage(
                messageable = ctx,
                delaySeconds = self.__generalSettingsRepository.getWaitForTriviaAnswerDelay(),
                message = response.toAnswerStr()
            ))
        except (RuntimeError, ValueError):
            print(f'Error retrieving trivia')
            await ctx.send('⚠ Error retrieving trivia')

    @commands.command(name = 'twitter')
    async def command_twitter(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasTwitter():
            return

        twitter = user.getTwitterUrl()
        await ctx.send(f'{user.getHandle()}\'s twitter: {twitter}')

    @commands.command(name = 'weather')
    async def command_weather(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isWeatherEnabled():
            return
        elif not self.__lastWeatherMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        if not user.hasLocationId():
            await ctx.send(f'⚠ Weather for {user.getHandle()} is enabled, but no location ID is available')
            return

        location = self.__locationsRepository.getLocation(user.getLocationId())

        try:
            weatherReport = self.__weatherRepository.fetchWeather(location)
            await ctx.send(weatherReport.toStr())
        except (RuntimeError, ValueError):
            print(f'Error fetching weather for \"{user.getLocationId()}\" in {user.getHandle()}')
            await ctx.send('⚠ Error fetching weather')

    @commands.command(name = 'word')
    async def command_word(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isWordOfTheDayEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastWotdMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        languageList = self.__wordOfTheDayRepository.getLanguageList()

        if len(splits) < 2:
            example = languageList.getLanguages()[0].getPrimaryCommandName()
            languages = languageList.toCommandNamesStr()
            await ctx.send(f'⚠ A language code is necessary for the !word command. Example: !word {example}. Available languages: {languages}')
            return

        language = splits[1]
        languageEntry = None

        try:
            languageEntry = languageList.getLanguageForCommand(language)
        except (RuntimeError, ValueError):
            print(f'Error retrieving language entry for \"{language}\" in {user.getHandle()}')
            await ctx.send(f'⚠ The given language code is not supported by the !word command. Available languages: {languageList.toCommandNamesStr()}')
            return

        try:
            wotd = self.__wordOfTheDayRepository.fetchWotd(languageEntry)
            await ctx.send(wotd.toStr())
        except (RuntimeError, ValueError):
            print(f'Error fetching word of the day for \"{languageEntry.getApiName()}\" in {user.getHandle()}')
            await ctx.send(f'⚠ Error fetching word of the day for \"{languageEntry.getApiName()}\"')
