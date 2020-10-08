from analogueStoreRepository import AnalogueStoreRepository
from authHelper import AuthHelper
from cutenessRepository import CutenessRepository
from datetime import datetime, timedelta
from jishoHelper import JishoHelper
from jishoResult import JishoResult
import json
from location import Location
from locationsRepository import LocationsRepository
import random
import requests
from twitchio.ext import commands
from user import User
from userIdsRepository import UserIdsRepository
from usersRepository import UsersRepository
from userTokensRepository import UserTokensRepository
from weatherReport import WeatherReport
from weatherRepository import WeatherRepository
from wordOfTheDayRepository import WordOfTheDayRepository
from wotd import Wotd

# https://github.com/TwitchIO/TwitchIO

class CynanBot(commands.Bot):

    def __init__(
        self,
        analogueStoreRepository: AnalogueStoreRepository,
        authHelper: AuthHelper,
        cutenessRepository: CutenessRepository,
        jishoHelper: JishoHelper,
        locationsRepository: LocationsRepository,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        userTokensRepository: UserTokensRepository,
        weatherRepository: WeatherRepository,
        wordOfTheDayRepository: WordOfTheDayRepository
    ):
        super().__init__(
            irc_token = authHelper.getIrcAuthToken(),
            client_id = authHelper.getClientId(),
            nick = 'CynanBot',
            prefix = '!',
            initial_channels = [ user.getHandle() for user in usersRepository.getUsers() ]
        )

        if analogueStoreRepository == None:
            raise ValueError(f'analogueStoreRepository argument is malformed: \"{analogueStoreRepository}\"')
        elif cutenessRepository == None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif locationsRepository == None:
            raise ValueError(f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif userIdsRepository == None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif userTokensRepository == None:
            raise ValueError(f'userTokensRepository argument is malformed: \"{userTokensRepository}\"')
        elif weatherRepository == None:
            raise ValueError(f'weatherRepository argument is malformed: \"{weatherRepository}\"')
        elif wordOfTheDayRepository == None:
            raise ValueError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')

        self.__analogueStoreRepository = analogueStoreRepository
        self.__authHelper = authHelper
        self.__cutenessRepository = cutenessRepository
        self.__jishoHelper = jishoHelper
        self.__locationsRepository = locationsRepository
        self.__userIdsRepository = userIdsRepository
        self.__usersRepository = usersRepository
        self.__userTokensRepository = userTokensRepository
        self.__weatherRepository = weatherRepository
        self.__wordOfTheDayRepository = wordOfTheDayRepository

        self.__cutenessDoubleEndTimes = dict()
        self.__lastAnalogueStockMessageTimes = dict()
        self.__lastCutenessLeaderboardMessageTimes = dict()
        self.__lastCutenessRedeemedMessageTimes = dict()
        self.__lastCynanMessageTime = datetime.now() - timedelta(days = 1)
        self.__lastDeerForceMessageTimes = dict()
        self.__lastJishoMessageTimes = dict()
        self.__lastWeatherMessageTimes = dict()
        self.__lastWotdMessageTimes = dict()

    def __canSendWordOfTheDay(self, user: User):
        if user == None:
            raise ValueError(f'user argument is malformed: \"{user}\"')

        now = datetime.now()
        delta = timedelta(seconds = 15)
        lastWotdMessageTime = self.__lastWotdMessageTimes.get(user.getHandle())

        if lastWotdMessageTime == None or now > lastWotdMessageTime + delta:
            self.__lastWotdMessageTimes[user.getHandle()] = now
            return True
        else:
            return False

    async def event_command_error(self, ctx, error):
        # prevents exceptions caused by people using commands for other bots
        pass

    async def event_message(self, message):
        if message.content.lower() == 'd e e r f o r c e':
            await self.__handleDeerForceMessage(message)
            return

        if message.author.name.lower() == 'CynanMachae'.lower():
            if await self.__handleMessageFromCynan(message):
                return

        await self.handle_commands(message)

    async def event_raw_pubsub(self, data):
        if 'error' in data and len(data['error']) >= 1:
            print(f'Received a pub sub error: {data}')

            if data['error'] == 'ERR_BADAUTH':
                self.__validateAndRefreshTokens()

            return
        elif 'type' not in data:
            print(f'Received a pub sub response without a type: {data}')
            return
        elif data['type'] == 'PONG' or data['type'] == 'RESPONSE':
            print(f'Received a general pub sub response: {data}')
            return
        elif data['type'] != 'MESSAGE' or 'data' not in data or 'message' not in data['data']:
            print(f'Received an unexpected pub sub response: {data}')
            return

        jsonResponse = json.loads(data['data']['message'])

        if jsonResponse['type'] == 'reward-redeemed':
            await self.__handleRewardRedeemed(jsonResponse)

    async def event_ready(self):
        print(f'{self.nick} is ready!')

        for user in self.__usersRepository.getUsers():
            accessToken = self.__userTokensRepository.getAccessToken(user.getHandle())

            if accessToken == None:
                continue

            userId = self.__userIdsRepository.fetchUserId(
                userName = user.getHandle(),
                clientId = self.__authHelper.getClientId(),
                accessToken = accessToken
            )

            print(f'Subscribing to events for {user.getHandle()}...')

            # we could subscribe to multiple topics, but for now, just channel points
            topics = [ f'channel-points-channel-v1.{userId}' ]

            # subscribe to pubhub channel points events
            await self.pubsub_subscribe(accessToken, *topics)

        print('Finished subscribing to events')

    async def __handleDeerForceMessage(self, message):
        user = self.__usersRepository.getUser(message.channel.name)

        now = datetime.now()
        delta = timedelta(minutes = 20)
        lastDeerForceMessageTime = self.__lastDeerForceMessageTimes.get(user.getHandle())

        if lastDeerForceMessageTime == None or now > lastDeerForceMessageTime + delta:
            self.__lastDeerForceMessageTimes[user.getHandle()] = now
            await message.channel.send('D e e R F o r C e')

    async def __handleIncreaseCutenessDoubleRewardRedeemed(
        self,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str,
        twitchUser: User,
        twitchChannel
    ):
        print(f'Enabling double cuteness points in {twitchUser.getHandle()}...')

        now = datetime.now()
        delta = timedelta(minutes = 5)
        self.__cutenessDoubleEndTimes[twitchUser.getHandle()] = now + delta

        try:
            cuteness = self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = 3,
                twitchChannel = twitchUser.getHandle(),
                userId = userIdThatRedeemed,
                userName = userNameThatRedeemed
            )

            await twitchChannel.send(f'✨ Double cuteness points enabled for the next 5 minutes! Increase your cuteness now~ ✨ Also, cuteness for {userNameThatRedeemed} has increased to {cuteness} ✨')
        except ValueError:
            print(f'Error increasing cuteness for {userNameThatRedeemed} ({userIdThatRedeemed}) in {twitchUser.getHandle()}')
            await twitchChannel.send(f'Error increasing cuteness for {userNameThatRedeemed}')

    async def __handleIncreaseCutenessRewardRedeemed(
        self,
        userIdThatRedeemed: str,
        userNameThatRedeemed: str,
        twitchUser: User,
        twitchChannel
    ):
        now = datetime.now()
        delta = timedelta(seconds = 20)
        lastCutenessRedeemedMessageTime = self.__lastCutenessRedeemedMessageTimes.get(twitchUser.getHandle())

        incrementAmount = 1
        if twitchUser.getHandle() in self.__cutenessDoubleEndTimes and now <= self.__cutenessDoubleEndTimes[twitchUser.getHandle()]:
            incrementAmount = 2

        try:
            cuteness = self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = twitchUser.getHandle(),
                userId = userIdThatRedeemed,
                userName = userNameThatRedeemed
            )

            if lastCutenessRedeemedMessageTime == None or now > lastCutenessRedeemedMessageTime + delta:
                self.__lastCutenessRedeemedMessageTimes[twitchUser.getHandle()] = now
                await twitchChannel.send(f'✨ @{userNameThatRedeemed} has increased cuteness~ ✨ Their cuteness has increased to {cuteness} ✨')
        except ValueError:
            print(f'Error increasing cuteness for {userNameThatRedeemed} ({userIdThatRedeemed}) in {twitchUser.getHandle()}')
            await twitchChannel.send(f'Error increasing cuteness for {userNameThatRedeemed}')

    async def __handleMessageFromCynan(self, message):
        now = datetime.now()
        delta = timedelta(hours = 3)

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
        print(f'Sending POTD to {userNameThatRedeemed} in {twitchUser.getHandle()}...')

        try:
            picOfTheDay = twitchUser.fetchPicOfTheDay()
            await twitchChannel.send(f'@{userNameThatRedeemed} here\'s the POTD: {picOfTheDay}')
        except FileNotFoundError:
            await twitchChannel.send(f'@{twitchUser.getHandle()} POTD file is missing!')
        except ValueError:
            await twitchChannel.send(f'@{twitchUser.getHandle()} POTD content is malformed!')

    async def __handleRewardRedeemed(self, jsonResponse):
        redemptionJson = jsonResponse['data']['redemption']
        twitchUserId = redemptionJson['channel_id']
        twitchUser = None

        for user in self.__usersRepository.getUsers():
            accessToken = self.__userTokensRepository.getAccessToken(user.getHandle())

            if accessToken == None:
                continue

            userId = self.__userIdsRepository.fetchUserId(
                userName = user.getHandle(),
                clientId = self.__authHelper.getClientId(),
                accessToken = accessToken
            )

            if twitchUserId.lower() == userId.lower():
                twitchUser = user
                break

        if twitchUser == None:
            raise RuntimeError(f'Unable to find User with ID: \"{twitchUserId}\"')

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
                userNameThatRedeemed = userNameThatRedeemed,
                twitchUser = twitchUser,
                twitchChannel = twitchChannel
            )
        elif twitchUser.isCutenessEnabled() and rewardId == increaseCutenessRewardId:
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
        else:
            print(f'The Reward ID for {twitchUser.getHandle()} is \"{rewardId}\"')

    async def __handleWordOfTheDay(self, ctx, wotd: Wotd):
        message = ""

        if wotd == None:
            message = 'Error fetching word of the day'
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

    def __validateAndRefreshTokens(self):
        print('Validating and refreshing tokens...')

        self.__authHelper.validateAndRefreshAccessTokens(
            users = self.__usersRepository.getUsers(),
            userTokensRepository = self.__userTokensRepository
        )

        print('Finished validating and refreshing tokens')

    @commands.command(name = 'analogue')
    async def command_analogue(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isAnalogueEnabled():
            return

        now = datetime.now()
        delta = timedelta(minutes = 1)
        lastAnalogueStockMessageTime = self.__lastAnalogueStockMessageTimes.get(user.getHandle())

        if lastAnalogueStockMessageTime == None or now > lastAnalogueStockMessageTime + delta:
            self.__lastAnalogueStockMessageTimes[user.getHandle()] = now
            storeStock = self.__analogueStoreRepository.fetchStoreStock()

            if storeStock == None:
                await ctx.send('Error reading products from Analogue store')
            elif len(storeStock) == 0:
                await ctx.send('Analogue store has nothing in stock')
            else:
                storeStockString = ', '.join(storeStock)
                await ctx.send(f'Analogue products in stock: {storeStockString}')

    @commands.command(name = 'cuteness')
    async def command_cuteness(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled():
            return

        now = datetime.now()
        delta = timedelta(seconds = 30)
        lastCutenessLeaderboardMessageTime = self.__lastCutenessLeaderboardMessageTimes.get(user.getHandle())

        if lastCutenessLeaderboardMessageTime == None or now > lastCutenessLeaderboardMessageTime + delta:
            self.__lastCutenessLeaderboardMessageTimes[user.getHandle()] = now

            leaderboard = self.__cutenessRepository.fetchLeaderboard(
                twitchChannel = user.getHandle()
            )

            if len(leaderboard) == 0:
                await ctx.send('😿 Unfortunately the cuteness leaderboard is empty 😿')
            else:
                leaderboardString = ', '.join(leaderboard)
                await ctx.send(f'✨ Cuteness leaderboard — {leaderboardString} ✨')

    @commands.command(name = 'cynanbot')
    async def command_cynanbot(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)
        commands = [ '!cynanbot', '!cynansource' ]

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

        if user.isDeWordOfTheDayEnabled():
            commands.append('!deword')

        if user.isEnEsWordOfTheDayEnabled():
            commands.append('!engword')

        if user.isEnPtWordOfTheDayEnabled():
            commands.append('!enptword')

        if user.isEsWordOfTheDayEnabled():
            commands.append('!esword')

        if user.isFrWordOfTheDayEnabled():
            commands.append('!frword')

        if user.isItWordOfTheDayEnabled():
            commands.append('!itword')

        if user.isJaWordOfTheDayEnabled():
            commands.append('!jaword')

        if user.isJishoEnabled():
            commands.append('!jisho')

        if user.isKoWordOfTheDayEnabled():
            commands.append('!koword')

        if user.isNoWordOfTheDayEnabled():
            commands.append('!noword')

        if user.isPtWordOfTheDayEnabled():
            commands.append('!ptword')

        if user.isRuWordOfTheDayEnabled():
            commands.append('!ruword')

        if user.isSvWordOfTheDayEnabled():
            commands.append('!svword')

        if user.isZhWordOfTheDayEnabled():
            commands.append('!zhword')

        commands.sort()
        commandsString = ', '.join(commands)

        await ctx.send(f'My commands: {commandsString}')

    @commands.command(name = 'cynansource')
    async def command_cynansource(self, ctx):
        await ctx.send('My source code is available here: https://github.com/charlesmadere/cynanbot')

    @commands.command(name = 'deword')
    async def command_deword(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isDeWordOfTheDayEnabled():
            return
        elif not self.__canSendWordOfTheDay(user):
            return

        wotd = self.__wordOfTheDayRepository.fetchDeWotd()
        await self.__handleWordOfTheDay(ctx, wotd)

    @commands.command(name = 'discord')
    async def command_discord(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasDiscord():
            return

        discord = user.getDiscord()
        await ctx.send(f'{user.getHandle()}\'s discord: {discord}')

    @commands.command(name = 'engword')
    async def command_engword(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isEnEsWordOfTheDayEnabled():
            return
        elif not self.__canSendWordOfTheDay(user):
            return

        wotd = self.__wordOfTheDayRepository.fetchEnEsWotd()
        await self.__handleWordOfTheDay(ctx, wotd)

    @commands.command(name = 'enptword')
    async def command_enptword(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isEnPtWordOfTheDayEnabled():
            return
        elif not self.__canSendWordOfTheDay(user):
            return

        wotd = self.__wordOfTheDayRepository.fetchEnPtWotd()
        await self.__handleWordOfTheDay(ctx, wotd)

    @commands.command(name = 'esword')
    async def command_esword(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isEsWordOfTheDayEnabled():
            return
        elif not self.__canSendWordOfTheDay(user):
            return

        wotd = self.__wordOfTheDayRepository.fetchEsWotd()
        await self.__handleWordOfTheDay(ctx, wotd)

    @commands.command(name = 'frword')
    async def command_frword(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isFrWordOfTheDayEnabled():
            return
        elif not self.__canSendWordOfTheDay(user):
            return

        wotd = self.__wordOfTheDayRepository.fetchFrWotd()
        await self.__handleWordOfTheDay(ctx, wotd)

    @commands.command(name = 'itword')
    async def command_itword(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isItWordOfTheDayEnabled():
            return
        elif not self.__canSendWordOfTheDay(user):
            return

        wotd = self.__wordOfTheDayRepository.fetchItWotd()
        await self.__handleWordOfTheDay(ctx, wotd)

    @commands.command(name = 'jaword')
    async def command_jaword(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isJaWordOfTheDayEnabled():
            return
        elif not self.__canSendWordOfTheDay(user):
            return

        wotd = self.__wordOfTheDayRepository.fetchJaWotd()
        await self.__handleWordOfTheDay(ctx, wotd)

    @commands.command(name = 'jisho')
    async def command_jisho(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isJishoEnabled():
            return

        now = datetime.now()
        delta = timedelta(seconds = 15)
        lastJishoMessageTime = self.__lastJishoMessageTimes.get(user.getHandle())

        if lastJishoMessageTime != None and now <= lastJishoMessageTime + delta:
            return

        self.__lastJishoMessageTimes[user.getHandle()] = now
        splits = ctx.message.content.split()

        if len(splits) == 1:
            await ctx.send('A search term is necessary for the !jisho command')
            return

        query = splits[1]

        try:
            result = self.__jishoHelper.search(query)

            if result == None:
                await ctx.send(f'Error searching Jisho for \"{query}\"')
            else:
                definitions = ' '.join(result.getDefinitions())

                if result.hasFurigana():
                    await ctx.send(f'({result.getFurigana()}) {result.getWord()} — {definitions}')
                else:
                    await ctx.send(f'{result.getWord()} — {definitions}')
        except ValueError:
            print(f'JishoHelper search query is malformed: \"{query}\"')

    @commands.command(name = 'koword')
    async def command_koword(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isKoWordOfTheDayEnabled():
            return
        elif not self.__canSendWordOfTheDay(user):
            return

        wotd = self.__wordOfTheDayRepository.fetchKoWotd()
        await self.__handleWordOfTheDay(ctx, wotd)

    @commands.command(name = 'mycuteness')
    async def command_mycuteness(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled():
            return

        userId = str(ctx.author.id)

        try:
            cuteness = self.__cutenessRepository.fetchCuteness(
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = ctx.author.name
            )

            if cuteness == 0:
                await ctx.send(f'😿 {ctx.author.name}\'s cuteness is {cuteness} 😿')
            else:
                await ctx.send(f'✨ {ctx.author.name}\'s cuteness is {cuteness} ✨')
        except ValueError:
            print(f'Error retrieving cuteness for {ctx.author.name} ({userId}) in {ctx.channel.id}')

    @commands.command(name = 'noword')
    async def command_noword(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isNoWordOfTheDayEnabled():
            return
        elif not self.__canSendWordOfTheDay(user):
            return

        wotd = self.__wordOfTheDayRepository.fetchNoWotd()
        await self.__handleWordOfTheDay(ctx, wotd)

    @commands.command(name = 'pbs')
    async def command_pbs(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasSpeedrunProfile():
            return

        speedrunProfile = user.getSpeedrunProfile()
        await ctx.send(f'{user.getHandle()}\'s speedrun profile: {speedrunProfile}')

    @commands.command(name = 'ptword')
    async def command_ptword(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isPtWordOfTheDayEnabled():
            return
        elif not self.__canSendWordOfTheDay(user):
            return

        wotd = self.__wordOfTheDayRepository.fetchPtWotd()
        await self.__handleWordOfTheDay(ctx, wotd)

    @commands.command(name = 'ruword')
    async def command_ruword(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isRuWordOfTheDayEnabled():
            return
        elif not self.__canSendWordOfTheDay(user):
            return

        wotd = self.__wordOfTheDayRepository.fetchRuWotd()
        await self.__handleWordOfTheDay(ctx, wotd)

    @commands.command(name = 'svword')
    async def command_svword(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isSvWordOfTheDayEnabled():
            return
        elif not self.__canSendWordOfTheDay(user):
            return

        wotd = self.__wordOfTheDayRepository.fetchSvWotd()
        await self.__handleWordOfTheDay(ctx, wotd)

    @commands.command(name = 'time')
    async def command_time(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasTimeZone():
            return

        now = datetime.now(user.getTimeZone())
        formattedTime = now.strftime("%A, %b %d, %Y %I:%M%p")
        await ctx.send(f'the local time for {user.getHandle()} is {formattedTime}')

    @commands.command(name = 'twitter')
    async def command_twitter(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasTwitter():
            return

        twitter = user.getTwitter()
        await ctx.send(f'{user.getHandle()}\'s twitter: {twitter}')

    @commands.command(name = 'weather')
    async def command_weather(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasLocationId():
            return

        now = datetime.now()
        delta = timedelta(minutes = 1)
        lastWeatherMessageTime = self.__lastWeatherMessageTimes.get(user.getHandle())

        if lastWeatherMessageTime != None and now <= lastWeatherMessageTime + delta:
            return

        self.__lastWeatherMessageTimes[user.getHandle()] = now
        location = self.__locationsRepository.getLocation(user.getLocationId())
        weatherReport = self.__weatherRepository.fetchWeather(location)

        if weatherReport == None:
            await ctx.send('Error fetching weather')
            return

        temperature = f'🌡 Temperature is {weatherReport.getTemperature()}°C ({weatherReport.getTemperatureImperial()}°F), '
        humidity = f'humidity is {weatherReport.getHumidity()}%, '

        airQuality = ''
        if weatherReport.hasAirQuality():
            airQuality = f'air quality is {weatherReport.getAirQuality()}, '

        pressure = f'and pressure is {weatherReport.getPressure()}hPa. '

        conditions = ''
        if weatherReport.hasConditions():
            conditionsJoin = ', '.join(weatherReport.getConditions())
            conditions = f'Current conditions: {conditionsJoin}. '

        tomorrowsTemps = f'Tomorrow has a low of {weatherReport.getTomorrowsLowTemperature()}°C ({weatherReport.getTomorrowsLowTemperatureImperial()}°F) and a high of {weatherReport.getTomorrowsHighTemperature()}°C ({weatherReport.getTomorrowsHighTemperatureImperial()}°F). '

        tomorrowsConditions = ''
        if weatherReport.hasTomorrowsConditions():
            tomorrowsConditionsJoin = ', '.join(weatherReport.getTomorrowsConditions())
            tomorrowsConditions = f'Tomorrow\'s conditions: {tomorrowsConditionsJoin}. '

        alerts = ''
        if weatherReport.hasAlerts():
            alertsJoin = ' '.join(weatherReport.getAlerts())
            alerts = f'🚨 {alertsJoin}'

        await ctx.send(f'{temperature}{humidity}{airQuality}{pressure}{conditions}{tomorrowsTemps}{tomorrowsConditions}{alerts}')

    @commands.command(name = 'zhword')
    async def command_zhword(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isZhWordOfTheDayEnabled():
            return
        elif not self.__canSendWordOfTheDay(user):
            return

        wotd = self.__wordOfTheDayRepository.fetchZhWotd()
        await self.__handleWordOfTheDay(ctx, wotd)
