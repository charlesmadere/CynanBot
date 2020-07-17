from authHelper import AuthHelper
from channelIdsRepository import ChannelIdsRepository
from datetime import datetime
from datetime import timedelta
import json
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
        self.__lastCynanMessageTime = datetime.now() - timedelta(hours = 8)

    async def event_command_error(self, ctx, error):
        # prevents exceptions caused by people using commands for other bots
        pass

    async def event_message(self, message):
        await self.handle_commands(message)

    async def event_raw_pubsub(self, data):
        if 'error' in data and len(data['error']) >= 1:
            print(f'Received a pub sub error: {data}')

            if data['error'] != 'ERR_BADAUTH':
                return

            users = self.__usersRepository.getUsers()

            print('Validating access tokens...')
            self.__authHelper.validateAccessTokens(
                users = users,
                userTokensRepository = self.__userTokensRepository
            )

            print('Refreshing access tokens...')
            self.__authHelper.refreshAccessTokens(
                users = users,
                userTokensRepository = self.__userTokensRepository
            )

            print('Finished validating and refreshing tokens')
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
            return

        redemptionJson = jsonResponse['data']['redemption']
        channelId = redemptionJson['channel_id']
        twitchUser = None

        for user in self.__usersRepository.getUsers():
            userChannelId = self.__channelIdsRepository.fetchChannelId(
                handle = user.getHandle(),
                clientId = self.__authHelper.getClientId(),
                accessToken = self.__userTokensRepository.getAccessToken(user.getHandle())
            )

            if channelId == userChannelId:
                twitchUser = user
                break

        if twitchUser == None:
            raise RuntimeError(f'Unable to find User with channel ID: \"{channelId}\"')

        rewardId = twitchUser.getRewardId()

        if rewardId == None or len(rewardId) == 0 or rewardId.isspace():
            # The runner of this script hasn't yet found their rewardId for POTD. So let's just
            # print out as much helpful data as possible and then return.
            newRewardId = redemptionJson['reward']['id']
            print(f'The rewardId is: \"{newRewardId}\", and the JSON is: \"{redemptionJson}\"')
            return

        if redemptionJson['reward']['id'] != twitchUser.getRewardId():
            # this user has redeemed a non-POTD reward
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

    @commands.command(name = 'cynanbot')
    async def command_cynanbot(self, ctx):
        await ctx.send(f'Hello @{ctx.author.name}!')

    @commands.command(name = 'time')
    async def command_time(self, ctx):
        now = datetime.now()
        formattedTime = now.strftime("%B %d, %Y %H:%M")
        await ctx.send(f'The local time is: {formattedTime}')
