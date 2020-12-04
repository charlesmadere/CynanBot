import json
import locale
import random
from datetime import datetime, timedelta
from typing import List

import requests
from twitchio.ext import commands

from analogueStoreRepository import AnalogueStoreRepository
from authHelper import AuthHelper
from cutenessRepository import (CutenessRepository, CutenessResult,
                                LeaderboardResult)
from jishoHelper import JishoHelper, JishoResult
from jokesRepository import JokeResponse, JokesRepository
from location import Location
from locationsRepository import LocationsRepository
from nonceRepository import NonceRepository
from timedDict import TimedDict
from user import User
from userIdsRepository import UserIdsRepository
from usersRepository import UsersRepository
from userTokensRepository import UserTokensRepository
from weatherReport import WeatherReport
from weatherRepository import WeatherRepository
from wordOfTheDayRepository import (LanguageEntry, LanguageList,
                                    WordOfTheDayRepository)
from wotd import Wotd


class CynanBot(commands.Bot):

    def __init__(
        self,
        analogueStoreRepository: AnalogueStoreRepository,
        authHelper: AuthHelper,
        cutenessRepository: CutenessRepository,
        jishoHelper: JishoHelper,
        jokesRepository: JokesRepository,
        locationsRepository: LocationsRepository,
        nonceRepository: NonceRepository,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        userTokensRepository: UserTokensRepository,
        weatherRepository: WeatherRepository,
        wordOfTheDayRepository: WordOfTheDayRepository
    ):
        super().__init__(
            irc_token=authHelper.getIrcAuthToken(),
            client_id=authHelper.getClientId(),
            nick='CynanBot',
            prefix='!',
            initial_channels=[user.getHandle()
                              for user in usersRepository.getUsers()]
        )

        if analogueStoreRepository is None:
            raise ValueError(
                f'analogueStoreRepository argument is malformed: \"{analogueStoreRepository}\"')
        elif cutenessRepository is None:
            raise ValueError(
                f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif jishoHelper is None:
            raise ValueError(
                f'jishHelper argument is malformed: \"{jishoHelper}\"')
        elif jokesRepository is None:
            raise ValueError(
                f'jokesRepository argument is malformed: \"{jokesRepository}\"')
        elif locationsRepository is None:
            raise ValueError(
                f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif nonceRepository is None:
            raise ValueError(
                f'nonceRepository argument is malformed: \"{nonceRepository}\"')
        elif userIdsRepository is None:
            raise ValueError(
                f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif userTokensRepository is None:
            raise ValueError(
                f'userTokensRepository argument is malformed: \"{userTokensRepository}\"')
        elif weatherRepository is None:
            raise ValueError(
                f'weatherRepository argument is malformed: \"{weatherRepository}\"')
        elif wordOfTheDayRepository is None:
            raise ValueError(
                f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')

        self.__analogueStoreRepository = analogueStoreRepository
        self.__authHelper = authHelper
        self.__cutenessRepository = cutenessRepository
        self.__jishoHelper = jishoHelper
        self.__jokesRepository = jokesRepository
        self.__locationsRepository = locationsRepository
        self.__nonceRepository = nonceRepository
        self.__userIdsRepository = userIdsRepository
        self.__usersRepository = usersRepository
        self.__userTokensRepository = userTokensRepository
        self.__weatherRepository = weatherRepository
        self.__wordOfTheDayRepository = wordOfTheDayRepository

        self.__cutenessDoubleEndTimes = TimedDict(timedelta(minutes=5))
        self.__lastAnalogueStockMessageTimes = TimedDict(timedelta(minutes=1))
        self.__lastCatJamMessageTimes = TimedDict(timedelta(minutes=20))
        self.__lastCutenessLeaderboardMessageTimes = TimedDict(
            timedelta(seconds=30))
        self.__lastCutenessRedeemedMessageTimes = TimedDict(
            timedelta(seconds=30))
        self.__lastCynanMessageTime = datetime.now() - timedelta(days=1)
        self.__lastDeerForceMessageTimes = TimedDict(timedelta(minutes=20))
        self.__lastJishoMessageTimes = TimedDict(timedelta(seconds=15))
        self.__lastJokeMessageTimes = TimedDict(timedelta(minutes=1))
        self.__lastWeatherMessageTimes = TimedDict(timedelta(minutes=1))
        self.__lastWotdMessageTimes = TimedDict(timedelta(seconds=15))

    async def event_command_error(self, ctx, error):
        # prevents exceptions caused by people using commands for other bots
        pass

    async def event_message(self, message):
        if await self.__handleMessageFromCynan(message):
            return

        if await self.__handleDeerForceMessage(message):
            return

        if await self.__handleCatJamMessage(message):
            return

        await self.handle_commands(message)

    async def event_raw_pubsub(self, data):
        if 'error' in data and len(data['error']) >= 1:
            print(f'Received a pub sub error: {data}')

            if data['error'] == 'ERR_BADAUTH':
                await self.__validateAndRefreshTokensAndResubscribe(nonce=data.get('nonce'))
        elif 'type' not in data:
            print(f'Received a pub sub response without a type: {data}')
        elif data['type'] == 'PONG' or data['type'] == 'RESPONSE':
            print(f'Received a general pub sub response: {data}')
        elif data['type'] != 'MESSAGE' or 'data' not in data or 'message' not in data['data']:
            print(f'Received an unexpected pub sub response: {data}')
        else:
            jsonResponse = json.loads(data['data']['message'])

            if jsonResponse['type'] == 'reward-redeemed':
                await self.__handleRewardRedeemed(jsonResponse)

    async def event_ready(self):
        print(f'{self.nick} is ready!')
        await self.__subscribeToEvents(self.__usersRepository.getUsers())

    async def __handleCatJamMessage(self, message):
        user = self.__usersRepository.getUser(message.channel.name)

        if not user.isCatJamEnabled():
            return False

        splits = message.content.split()

        if 'catJAM' in splits and self.__lastCatJamMessageTimes.isReadyAndUpdate(user.getHandle()):
            await message.channel.send('catJAM')
            return True
        else:
            return False

    async def __handleDeerForceMessage(self, message):
        user = self.__usersRepository.getUser(message.channel.name)

        if message.content.strip().lower() != 'd e e r f o r c e':
            return False
        elif self.__lastDeerForceMessageTimes.isReadyAndUpdate(user.getHandle()):
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
        print(
            f'Enabling double cuteness points in {twitchUser.getHandle()}...')

        self.__cutenessDoubleEndTimes.update(twitchUser.getHandle())

        try:
            result = self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount=3,
                twitchChannel=twitchUser.getHandle(),
                userId=userIdThatRedeemed,
                userName=userNameThatRedeemed
            )

            await twitchChannel.send(f'✨ Double cuteness points enabled for the next 5 minutes! Increase your cuteness now~ ✨ Also, cuteness for {userNameThatRedeemed} has increased to {result.getCutenessStr()} ✨')
        except ValueError:
            print(
                f'Error increasing cuteness for {userNameThatRedeemed} ({userIdThatRedeemed}) in {twitchUser.getHandle()}')
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
                incrementAmount=incrementAmount,
                twitchChannel=twitchUser.getHandle(),
                userId=userIdThatRedeemed,
                userName=userNameThatRedeemed
            )

            if self.__lastCutenessRedeemedMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
                await twitchChannel.send(f'✨ @{userNameThatRedeemed} has increased cuteness~ ✨ Their cuteness has increased to {result.getCutenessStr()} ✨')
        except ValueError:
            print(
                f'Error increasing cuteness for {userNameThatRedeemed} ({userIdThatRedeemed}) in {twitchUser.getHandle()}')
            await twitchChannel.send(f'⚠ Error increasing cuteness for {userNameThatRedeemed}')

    async def __handleMessageFromCynan(self, message):
        if message.author.name.lower() != 'cynanmachae'.lower():
            return False

        now = datetime.now()
        delta = timedelta(hours=4)

        if now > self.__lastCynanMessageTime + delta:
            self.__lastCynanMessageTime = now
            await message.channel.send_me('waves to @CynanMachae 👋')
            return True
        else:
            return False

    async def __handlePotdRewardRedeemed(
        self,
        userNameThatRedeemed: str,
        twitchUser: User,
        twitchChannel
    ):
        print(
            f'Sending POTD to {userNameThatRedeemed} in {twitchUser.getHandle()}...')

        try:
            picOfTheDay = twitchUser.fetchPicOfTheDay()
            await twitchChannel.send(f'@{userNameThatRedeemed} here\'s the POTD: {picOfTheDay}')
        except FileNotFoundError:
            await twitchChannel.send(f'⚠ {twitchUser.getHandle()}\'s POTD file is missing!')
        except ValueError:
            await twitchChannel.send(f'⚠ {twitchUser.getHandle()}\'s POTD content is malformed!')

    async def __handleRewardRedeemed(self, jsonResponse):
        redemptionJson = jsonResponse['data']['redemption']
        twitchUserId = redemptionJson['channel_id']
        twitchUser = None

        for user in self.__usersRepository.getUsers():
            accessToken = self.__userTokensRepository.getAccessToken(
                user.getHandle())

            if accessToken is None:
                continue

            userId = self.__userIdsRepository.fetchUserId(
                userName=user.getHandle(),
                clientId=self.__authHelper.getClientId(),
                accessToken=accessToken
            )

            if twitchUserId.lower() == userId.lower():
                twitchUser = user
                break

        if twitchUser is None:
            raise RuntimeError(
                f'Unable to find User with ID: \"{twitchUserId}\"')

        if not twitchUser.isCutenessEnabled() and not twitchUser.isPicOfTheDayEnabled():
            return

        increaseCutenessDoubleRewardId = twitchUser.getIncreaseCutenessDoubleRewardId()
        increaseCutenessRewardId = twitchUser.getIncreaseCutenessRewardId()
        potdRewardId = twitchUser.getPicOfTheDayRewardId()
        rewardId = redemptionJson['reward']['id']
        userIdThatRedeemed = redemptionJson['user']['id']
        userNameThatRedeemed = redemptionJson['user']['login']
        twitchChannel = self.get_channel(twitchUser.getHandle())

        if twitchUser.isPicOfTheDayEnabled() and rewardId == potdRewardId:
            await self.__handlePotdRewardRedeemed(
                userNameThatRedeemed=userNameThatRedeemed,
                twitchUser=twitchUser,
                twitchChannel=twitchChannel
            )
        elif twitchUser.isCutenessEnabled() and rewardId == increaseCutenessRewardId:
            await self.__handleIncreaseCutenessRewardRedeemed(
                userIdThatRedeemed=userIdThatRedeemed,
                userNameThatRedeemed=userNameThatRedeemed,
                twitchUser=twitchUser,
                twitchChannel=twitchChannel
            )
        elif twitchUser.isCutenessEnabled() and rewardId == increaseCutenessDoubleRewardId:
            await self.__handleIncreaseCutenessDoubleRewardRedeemed(
                userIdThatRedeemed=userIdThatRedeemed,
                userNameThatRedeemed=userNameThatRedeemed,
                twitchUser=twitchUser,
                twitchChannel=twitchChannel
            )
        else:
            print(
                f'The Reward ID for {twitchUser.getHandle()} is \"{rewardId}\"')

    async def __handleWordOfTheDay(self, ctx, wotd: Wotd):
        message = ""

        if wotd is None:
            message = '⚠ Error fetching word of the day'
        elif wotd.hasExamples():
            if wotd.hasTransliteration():
                message = f'({wotd.getLanguage()}) {wotd.getWord()} ({wotd.getTransliteration()}) — {wotd.getDefinition()}. Example: {wotd.getForeignExample()} {wotd.getEnglishExample()}'
            else:
                message = f'({wotd.getLanguage()}) {wotd.getWord()} — {wotd.getDefinition()}. Example: {wotd.getForeignExample()} {wotd.getEnglishExample()}'
        elif wotd.hasTransliteration():
            message = f'({wotd.getLanguage()}) {wotd.getWord()} ({wotd.getTransliteration()}) — {wotd.getDefinition()}'
        else:
            message = f'({wotd.getLanguage()}) {wotd.getWord()} — {wotd.getDefinition()}'

        await ctx.send(message)

    async def __subscribeToEvents(self, users: List[User]):
        if users is None or len(users) == 0:
            print(
                f'Given an empty list of users to subscribe to events for, will not subscribe to any events')
            return

        count = 0

        for user in users:
            accessToken = self.__userTokensRepository.getAccessToken(
                user.getHandle())

            if accessToken is None:
                continue
            else:
                count = count + 1

            userId = self.__userIdsRepository.fetchUserId(
                userName=user.getHandle(),
                clientId=self.__authHelper.getClientId(),
                accessToken=accessToken
            )

            # we could subscribe to multiple topics, but for now, just channel points
            topics = [f'channel-points-channel-v1.{userId}']

            # subscribe to pubhub channel points events
            nonce = await self.pubsub_subscribe(accessToken, *topics)

            # save the nonce, we'll need to use it later if the token used for this user's
            # connection has to be refreshed
            self.__nonceRepository.setNonce(user.getHandle(), nonce)

            print(
                f'Subscribed to events for {user.getHandle()} (nonce: \"{nonce}\")')

        print(f'Finished subscribing to events for {count} user(s)')

    async def __validateAndRefreshTokensAndResubscribe(self, nonce: str):
        print(f'Validating and refreshing tokens... (nonce: \"{nonce}\")')

        users = self.__usersRepository.getUsers()

        self.__authHelper.validateAndRefreshAccessTokens(
            users=users,
            nonce=nonce,
            userTokensRepository=self.__userTokensRepository
        )

        resubscribeUsers = list()

        for user in users:
            if (nonce is None or len(nonce) == 0 or nonce.isspace()) or nonce == self.__nonceRepository.getNonce(user.getHandle()):
                resubscribeUsers.append(user)

        await self.__subscribeToEvents(resubscribeUsers)
        print(
            f'Finished validating and refreshing {len(resubscribeUsers)} token(s) (nonce: \"{nonce}\")')

    @commands.command(name='analogue')
    async def command_analogue(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isAnalogueEnabled():
            return
        elif not self.__lastAnalogueStockMessageTimes.isReady(user.getHandle()):
            return

        storeStock = self.__analogueStoreRepository.fetchStoreStock()
        self.__lastAnalogueStockMessageTimes.update(user.getHandle())

        if storeStock is None:
            await ctx.send('⚠ Error reading products from Analogue store')
        elif len(storeStock) == 0:
            await ctx.send('🍃 Analogue store has nothing in stock')
        else:
            storeStockString = ', '.join(storeStock)
            await ctx.send(f'Analogue products in stock: {storeStockString}')

    @commands.command(name='cuteness')
    async def command_cuteness(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastCutenessLeaderboardMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = ctx.message.content.split()

        userName = None
        if len(splits) == 2:
            userName = splits[1]

        if userName is None or len(userName) == 0 or userName.isspace():
            result = self.__cutenessRepository.fetchLeaderboard(
                user.getHandle())

            if result.hasEntries():
                await ctx.send(f'✨ Cuteness leaderboard — {result.toStr()} ✨')
            else:
                await ctx.send('😿 Unfortunately the cuteness leaderboard is empty 😿')
        else:
            if userName[0] == '@':
                userName = userName[1:len(userName)]

            try:
                result = self.__cutenessRepository.fetchCuteness(
                    twitchChannel=user.getHandle(),
                    userName=userName
                )

                if result.hasCuteness():
                    await ctx.send(f'✨ {userName}\'s cuteness: {result.getCutenessStr()} ✨')
                else:
                    await ctx.send(f'😿 Unfortunately {userName} has no cuteness 😿')
            except ValueError:
                print(
                    f'Unable to find \"{userName}\" in the cuteness database')
                await ctx.send(f'⚠ Unable to find \"{userName}\" in the cuteness database')

    @commands.command(name='cynanbot')
    async def command_cynanbot(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)
        commands = ['!cynanbot', '!cynansource']

        if user.hasDiscord():
            commands.append('!discord')

        if user.hasLocationId():
            commands.append('!weather')

        if user.hasSpeedrunProfile():
            commands.append('!pbs')

        if user.hasTimeZone():
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

        if user.isJishoEnabled():
            commands.append('!jisho')

        if user.isJokesEnabled():
            commands.append('!joke')

        if user.isWordOfTheDayEnabled():
            commands.append('!word')

        commands.sort()
        commandsString = ', '.join(commands)

        await ctx.send(f'My commands: {commandsString}')

    @commands.command(name='cynansource')
    async def command_cynansource(self, ctx):
        await ctx.send('My source code is available here: https://github.com/charlesmadere/cynanbot')

    @commands.command(name='discord')
    async def command_discord(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasDiscord():
            return

        discord = user.getDiscord()
        await ctx.send(f'{user.getHandle()}\'s discord: {discord}')

    @commands.command(name='givecuteness')
    async def command_givecuteness(self, ctx):
        if not ctx.author.is_mod:
            return

        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled() or not user.isGiveCutenessEnabled():
            return

        splits = ctx.message.content.split()

        if len(splits) != 3:
            await ctx.send(f'⚠ Username and amount is necessary for the !givecuteness command. Example: !givecuteness {user.getHandle()} 5')
            return

        userName = splits[1]
        if userName is None or len(userName) == 0 or userName.isspace():
            print(f'Username is malformed: \"{userName}\"')
            await ctx.send(f'⚠ Username argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        incrementAmountStr = splits[2]
        if incrementAmountStr is None or len(incrementAmountStr) == 0 or incrementAmountStr.isspace():
            print(f'Increment amount is malformed: \"{incrementAmountStr}\"')
            await ctx.send(f'⚠ Increment amount argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        try:
            incrementAmount = int(incrementAmountStr)
        except (SyntaxError, ValueError):
            print(
                f'Unable to convert increment amount into an int: \"{incrementAmountStr}\"')
            await ctx.send(f'⚠ Increment amount argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        if userName[0] == '@':
            userName = userName[1:len(userName)]

        try:
            userId = self.__userIdsRepository.fetchUserId(userName=userName)
        except ValueError:
            print(
                f'Attempted to give cuteness to \"{userName}\", but their user ID does not exist in the database')
            await ctx.send(f'⚠ Unable to give cuteness to \"{userName}\", they don\'t currently exist in the database')
            return

        try:
            result = self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount=incrementAmount,
                twitchChannel=user.getHandle(),
                userId=userId,
                userName=userName
            )

            await ctx.send(f'✨ Cuteness for {userName} is now {result.getCutenessStr()} ✨')
        except ValueError:
            print(
                f'Error incrementing cuteness by {incrementAmount} for {userName} ({userId}) in {user.getHandle()}')
            await ctx.send(f'⚠ Error incrementing cuteness for {userName}')

    @commands.command(name='jisho')
    async def command_jisho(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isJishoEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastJishoMessageTimes.isReady(user.getHandle()):
            return

        splits = ctx.message.content.split()

        if len(splits) == 1:
            await ctx.send('⚠ A search term is necessary for the !jisho command. Example: !jisho 食べる')
            return

        query = splits[1]

        try:
            result = self.__jishoHelper.search(query)
            self.__lastJishoMessageTimes.update(user.getHandle())

            if result is None:
                print(
                    f'Failed searching Jisho for \"{query}\" in {user.getHandle()}')
                await ctx.send(f'⚠ Error searching Jisho for \"{query}\"')
            else:
                await ctx.send(f'{result.toStr()}')
        except ValueError:
            print(f'JishoHelper search query is malformed: \"{query}\"')
            await ctx.send(f'⚠ Error searching Jisho for \"{query}\"')

    @commands.command(name='joke')
    async def command_joke(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isJokesEnabled():
            return
        elif not self.__lastJokeMessageTimes.isReady(user.getHandle()):
            return

        try:
            result = self.__jokesRepository.fetchJoke()

            if result is None:
                print(f'Error fetching joke of the day in {user.getHandle()}')
                await ctx.send('⚠ Error fetching joke of the day')
            else:
                await ctx.send(result.toStr())
        except ValueError:
            print(f'Error fetching joke of the day in {user.getHandle()}')
            await ctx.send('⚠ Error fetching joke of the day')

    @commands.command(name='mycuteness')
    async def command_mycuteness(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled():
            return

        userId = str(ctx.author.id)

        try:
            result = self.__cutenessRepository.fetchCutenessAndLocalLeaderboard(
                twitchChannel=user.getHandle(),
                userId=userId,
                userName=ctx.author.name
            )

            if result.hasCuteness() and result.hasLocalLeaderboard():
                await ctx.send(f'✨ {ctx.author.name}\'s cuteness is {result.getCutenessStr()}, and their local leaderboard is: {result.getLocalLeaderboardStr()} ✨')
            elif result.hasCuteness():
                await ctx.send(f'✨ {ctx.author.name}\'s cuteness is {result.getCutenessStr()} ✨')
            else:
                await ctx.send(f'😿 {ctx.author.name} has no cuteness 😿')
        except ValueError:
            print(
                f'Error retrieving cuteness for {ctx.author.name} ({userId}) in {user.getHandle()}')
            await ctx.send(f'⚠ Error retrieving cuteness for {ctx.author.name}')

    @commands.command(name='pbs')
    async def command_pbs(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasSpeedrunProfile():
            return

        speedrunProfile = user.getSpeedrunProfile()
        await ctx.send(f'{user.getHandle()}\'s speedrun profile: {speedrunProfile}')

    @commands.command(name='time')
    async def command_time(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasTimeZone():
            return

        now = datetime.now(user.getTimeZone())
        formattedTime = now.strftime("%A, %b %d, %Y %I:%M%p")
        await ctx.send(f'🕰️ The local time for {user.getHandle()} is {formattedTime}')

    @commands.command(name='twitter')
    async def command_twitter(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasTwitter():
            return

        twitter = user.getTwitter()
        await ctx.send(f'{user.getHandle()}\'s twitter: {twitter}')

    @commands.command(name='weather')
    async def command_weather(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasLocationId():
            return
        elif not self.__lastWeatherMessageTimes.isReady(user.getHandle()):
            return

        location = self.__locationsRepository.getLocation(user.getLocationId())
        weatherReport = self.__weatherRepository.fetchWeather(location)
        self.__lastWeatherMessageTimes.update(user.getHandle())

        if weatherReport is None:
            await ctx.send('⚠ Error fetching weather')
            return

        temperature = f'🌡 Temperature is {weatherReport.getTemperatureStr()}°C ({weatherReport.getTemperatureImperialStr()}°F), '
        humidity = f'humidity is {weatherReport.getHumidity()}%, '

        airQuality = ''
        if weatherReport.hasAirQuality():
            airQuality = f'air quality is {weatherReport.getAirQualityStr()}, '

        pressure = f'and pressure is {weatherReport.getPressureStr()} hPa. '

        conditions = ''
        if weatherReport.hasConditions():
            conditionsJoin = ', '.join(weatherReport.getConditions())
            conditions = f'Current conditions: {conditionsJoin}. '

        tomorrowsTemps = f'Tomorrow has a low of {weatherReport.getTomorrowsLowTemperatureStr()}°C ({weatherReport.getTomorrowsLowTemperatureImperialStr()}°F) and a high of {weatherReport.getTomorrowsHighTemperatureStr()}°C ({weatherReport.getTomorrowsHighTemperatureImperialStr()}°F). '

        tomorrowsConditions = ''
        if weatherReport.hasTomorrowsConditions():
            tomorrowsConditionsJoin = ', '.join(
                weatherReport.getTomorrowsConditions())
            tomorrowsConditions = f'Tomorrow\'s conditions: {tomorrowsConditionsJoin}. '

        alerts = ''
        if weatherReport.hasAlerts():
            alertsJoin = ' '.join(weatherReport.getAlerts())
            alerts = f'🚨 {alertsJoin}'

        await ctx.send(f'{temperature}{humidity}{airQuality}{pressure}{conditions}{tomorrowsTemps}{tomorrowsConditions}{alerts}')

    @commands.command(name='word')
    async def command_word(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isWordOfTheDayEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastWotdMessageTimes.isReady(user.getHandle()):
            return

        splits = ctx.message.content.split()
        languageList = self.__wordOfTheDayRepository.getLanguageList()

        if len(splits) == 1:
            example = languageList.getLanguages()[0].getCommandName()
            languages = languageList.toCommandNameStr()
            await ctx.send(f'⚠ A language code is necessary for the !word command. Example: !word {example}. Available languages: {languages}')
            return

        language = splits[1].strip()
        languageEntry = None

        try:
            languageEntry = languageList.getLanguageForCommand(language)
        except (RuntimeError, ValueError):
            print(f'Error retrieving language entry for \"{language}\"')

        if languageEntry is None:
            languages = languageList.toCommandNameStr()
            await ctx.send(f'⚠ The given language code is not supported by the !word command. Available languages: {languages}')
            return

        wotd = None

        try:
            wotd = self.__wordOfTheDayRepository.fetchWotd(languageEntry)
        except ValueError:
            print(
                f'Error fetching word of the day for \"{languageEntry.getApiName()}\"')

        message = ''

        if wotd is None:
            message = f'⚠ Error fetching word of the day for {languageEntry.getApiName()}'
        elif wotd.hasExamples():
            if wotd.hasTransliteration():
                message = f'({wotd.getLanguage()}) {wotd.getWord()} ({wotd.getTransliteration()}) — {wotd.getDefinition()}. Example: {wotd.getForeignExample()} {wotd.getEnglishExample()}'
            else:
                message = f'({wotd.getLanguage()}) {wotd.getWord()} — {wotd.getDefinition()}. Example: {wotd.getForeignExample()} {wotd.getEnglishExample()}'
        elif wotd.hasTransliteration():
            message = f'({wotd.getLanguage()}) {wotd.getWord()} ({wotd.getTransliteration()}) — {wotd.getDefinition()}'
        else:
            message = f'({wotd.getLanguage()}) {wotd.getWord()} — {wotd.getDefinition()}'

        await ctx.send(message)
