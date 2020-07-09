from authHelper import AuthHelper
import json
import requests
from twitchio.ext import commands
from typing import List
from user import User

# https://github.com/TwitchIO/TwitchIO

class CynanBot(commands.Bot):
    def __init__(self, authHelper: AuthHelper):
        super().__init__(
            irc_token = authHelper.getIrcAuthToken(),
            client_id = authHelper.getClientId(),
            nick = 'CynanBot',
            prefix = '!',
            initial_channels = [ user.getHandle() for user in authHelper.getUsers() ]
        )

        self.__authHelper = authHelper

    async def event_message(self, message):
        await self.handle_commands(message)

    async def event_raw_pubsub(self, data):
        if 'error' in data and len(data['error']) >= 1:
            print(f'Received a pub sub error: {data}')

            if data['error'] != 'ERR_BADAUTH':
                return

            print('Validating access tokens...')
            self.__authHelper.validateAccessTokens()

            print('Refreshing access tokens...')
            self.__authHelper.refreshAccessTokens()

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

        for user in self.__authHelper.getUsers():
            if channelId == user.fetchChannelId(self.__authHelper.getClientId()):
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

        for user in self.__authHelper.getUsers():
            channelId = user.fetchChannelId(self.__authHelper.getClientId())

            # we could subscribe to multiple topics, but for now, just channel points
            topics = [ f'channel-points-channel-v1.{channelId}' ]

            # subscribe to pubhub channel points events
            await self.pubsub_subscribe(user.getAccessToken(), *topics)

    @commands.command(name = 'cynanbot')
    async def command_cynanbot(self, ctx):
        await ctx.send(f'Hello @{ctx.author.name}!')
