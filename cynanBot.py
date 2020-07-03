import json
import requests
from twitchio.ext import commands
from typing import List
from user import User

# https://github.com/TwitchIO/TwitchIO

class CynanBot(commands.Bot):
    def __init__(
        self,
        ircToken: str,
        clientId: str,
        users: List[User]
    ):
        super().__init__(
            irc_token = ircToken,
            client_id = clientId,
            nick = 'CynanBot',
            prefix = '!',
            initial_channels = [ user.twitchHandle for user in users ]
        )

        self.__clientId = clientId
        self.__users = users

    async def event_message(self, message):
        await self.handle_commands(message)

    async def event_raw_pubsub(self, data):
        if 'error' in data and len(data['error']) >= 1:
            print(f'Received a pub sub error: {data}')
            return
        elif 'type' not in data:
            print(f'Received a pub sub response without a type: {data}')
            return
        elif data['type'] == 'PONG' or data['type'] == 'RESPONSE':
            print(f'Received a general pub sub response: {data}')
            return
        elif data['type'] != 'MESSAGE' or 'message' not in data:
            print(f'Received an unexpected pub sub response: {data}')
            return

        jsonResponse = json.loads(data['data']['message'])

        if jsonResponse['type'] != 'reward-redeemed':
            return

        redemptionJson = jsonResponse['data']['redemption']
        channelId = redemptionJson['channel_id']
        twitchUser = None

        for user in self.__users:
            if channelId == user.fetchChannelId(clientId = self.__clientId):
                twitchUser = user
                break

        if twitchUser == None:
            raise RuntimeError(f'Unable to find Twitch User with channel ID: \"{channelId}\"')

        if twitchUser.rewardId == None or len(twitchUser.rewardId) == 0:
            # The runner of this script hasn't yet found their rewardId for POTD. So let's just
            # print out as much helpful data as possible and then return.
            rewardId = redemptionJson['reward']['id']
            print(f'The rewardId is: \"{rewardId}\", and the JSON is: \"{redemptionJson}\"')
            return

        if redemptionJson['reward']['id'] != twitchUser.rewardId:
            # this user has redeemed a non-POTD reward
            return

        userThatRedeemed = redemptionJson['user']['login']
        print(f'Sending POTD for {twitchUser.twitchHandle} to {userThatRedeemed}...')

        twitchChannel = self.get_channel(twitchUser.twitchHandle)

        try:
            picOfTheDay = twitchUser.fetchPicOfTheDay()
            await twitchChannel.send(f'{userThatRedeemed} here\'s the POTD: {picOfTheDay}')
        except FileNotFoundError:
            await twitchChannel.send(f'{twitchUser.twitchHandle} POTD file is missing!')
        except ValueError:
            await twitchChannel.send(f'{twitchUser.twitchHandle} POTD content is malformed!')

    async def event_ready(self):
        print(f'{self.nick} is ready!')

        for user in self.__users:
            channelId = user.fetchChannelId(clientId = self.__clientId)

            # we could subscribe to multiple topics, but for now, just channel points
            topics = [ f'channel-points-channel-v1.{channelId}' ]

            # subscribe to pubhub channel points events
            await self.pubsub_subscribe(user.accessToken, *topics)

    @commands.command(name = 'cynanbot')
    async def command_cynanbot(self, ctx):
        await ctx.send(f'{self.nick} says hello {ctx.author.name}!')
