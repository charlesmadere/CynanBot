from authHelper import AuthHelper
from channelIdsRepository import ChannelIdsRepository
from datetime import datetime, timedelta
import json
import random
import requests
from twitchio.ext import commands
from user import User
from usersRepository import UsersRepository
from userTokensRepository import UserTokensRepository

# https://github.com/TwitchIO/TwitchIO

class CynanBot(commands.Bot):
    def __init__(
        self,
        authHelper: AuthHelper,
        channelIdsRepository: ChannelIdsRepository,
        usersRepository: UsersRepository,
        userTokensRepository: UserTokensRepository
    ):
        super().__init__(
            irc_token = authHelper.getIrcAuthToken(),
            client_id = authHelper.getClientId(),
            nick = 'CynanBot',
            prefix = '!',
            initial_channels = [ user.getHandle() for user in usersRepository.getUsers() ]
        )

        self.__authHelper = authHelper
        self.__channelIdsRepository = channelIdsRepository
        self.__usersRepository = usersRepository
        self.__userTokensRepository = userTokensRepository

        now = datetime.now()
        self.__lastCynanMessageTime = now - timedelta(hours = 8)
        self.__lastDeerForceMessageTimes = dict()

    async def event_command_error(self, ctx, error):
        # prevents exceptions caused by people using commands for other bots
        pass

    async def event_message(self, message):
        if message.content == 'D e e R F o r C e':
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

        if jsonResponse['type'] != 'reward-redeemed':
            await self.__handleRewardRedeemed(jsonResponse)

    async def event_ready(self):
        print(f'{self.nick} is ready!')

        for user in self.__usersRepository.getUsers():
            handle = user.getHandle()
            accessToken = self.__userTokensRepository.getAccessToken(handle)

            channelId = self.__channelIdsRepository.fetchChannelId(
                handle = handle,
                clientId = self.__authHelper.getClientId(),
                accessToken = accessToken
            )

            # we could subscribe to multiple topics, but for now, just channel points
            topics = [ f'channel-points-channel-v1.{channelId}' ]

            # subscribe to pubhub channel points events
            await self.pubsub_subscribe(accessToken, *topics)

    async def __handleDeerForceMessage(self, message):
        now = datetime.now()
        delta = now - timedelta(minutes = 20)
        user = self.__usersRepository.getUser(message.channel.name)

        lastDeerForceMessageTime = None
        if user.getHandle() in self.__lastDeerForceMessageTimes:
            lastDeerForceMessageTime = self.__lastDeerForceMessageTimes[user.getHandle()]

        if lastDeerForceMessageTime == None or delta > lastDeerForceMessageTime:
            self.__lastDeerForceMessageTimes[user.getHandle()] = now
            await message.channel.send('D e e R F o r C e')

    async def __handleMessageFromCynan(self, message):
        now = datetime.now()
        delta = now - timedelta(minutes = 30)

        if delta > self.__lastCynanMessageTime:
            self.__lastCynanMessageTime = now
            await message.channel.send_me('waves to @CynanMachae')
            return True
        else:
            return False

    async def __handleRewardRedeemed(self, jsonResponse):
        redemptionJson = jsonResponse['data']['redemption']
        twitchChannelId = redemptionJson['channel_id']
        twitchUser = None

        for user in self.__usersRepository.getUsers():
            userChannelId = self.__channelIdsRepository.fetchChannelId(
                handle = user.getHandle(),
                clientId = self.__authHelper.getClientId(),
                accessToken = self.__userTokensRepository.getAccessToken(user.getHandle())
            )

            if twitchChannelId.lower() == userChannelId.lower():
                twitchUser = user
                break

        if twitchUser == None:
            raise RuntimeError(f'Unable to find User with channel ID: \"{twitchChannelId}\"')

        rewardId = twitchUser.getRewardId()

        if rewardId == None or len(rewardId) == 0 or rewardId.isspace():
            # The runner of this script hasn't yet found their rewardId for POTD. So let's just
            # print out as much helpful data as possible and then return.
            newRewardId = redemptionJson['reward']['id']
            print(f'The rewardId is: \"{newRewardId}\", and the JSON is: \"{redemptionJson}\"')
            return

        if redemptionJson['reward']['id'] != twitchUser.getRewardId():
            # This user has redeemed a non-POTD reward. Possibly in the future we'll support some
            # different reward redemptions.
            return

        userThatRedeemed = redemptionJson['user']['login']
        print(f'Sending {twitchUser.getHandle()}\'s POTD to {userThatRedeemed}...')

        twitchChannel = self.get_channel(twitchUser.getHandle())

        try:
            picOfTheDay = twitchUser.fetchPicOfTheDay()
            await twitchChannel.send(f'@{userThatRedeemed} here\'s the POTD: {picOfTheDay}')
        except FileNotFoundError:
            await twitchChannel.send(f'@{twitchUser.getHandle()} POTD file is missing!')
        except ValueError:
            await twitchChannel.send(f'@{twitchUser.getHandle()} POTD content is malformed!')

    def __validateAndRefreshTokens(self):
        print('Validating and refreshing tokens...')

        self.__authHelper.validateAndRefreshAccessTokens(
            users = self.__usersRepository.getUsers(),
            userTokensRepository = self.__userTokensRepository
        )

        print('Finished validating and refreshing tokens')

    @commands.command(name = 'cynanbot')
    async def command_cynanbot(self, ctx):
        await ctx.send(f'hello @{ctx.author.name} !')

    @commands.command(name = 'time')
    async def command_time(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)
        now = datetime.now(user.getTimeZone())
        formattedTime = now.strftime("%A, %b %d, %Y %I:%M%p")
        await ctx.send(f'the local time for {user.getHandle()} is {formattedTime}')
