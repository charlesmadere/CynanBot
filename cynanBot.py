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
        accessToken: str,
        refreshToken: str,
        users: List[User]
    ):
        super().__init__(
            irc_token = ircToken,
            client_id = clientId,
            nick = 'CynanBot',
            prefix = '!',
            initial_channels = [ user.twitchHandle for user in users ]
        )

        self.__ircToken = ircToken
        self.__clientId = clientId
        self.__accessToken = accessToken
        self.__refreshToken = refreshToken
        self.__users = users

    async def event_message(self, message):
        await self.handle_commands(message)

    async def event_raw_pubsub(self, data):
        if 'error' in data and len(data['error']) >= 1:
            print(f'Received an error: {data}')
            return
        elif 'type' not in data:
            print(f'Received a response without a type: {data}')
            return
        elif data['type'] == 'PONG' or data['type'] == 'RESPONSE':
            print(f'Received a general response: {data}')
            return
        elif data['type'] != 'MESSAGE' or 'message' not in data:
            print(f'Received an unexpected response: {data}')
            return

        jsonResponse = json.loads(data['data']['message'])

        if jsonResponse['type'].lower() != 'reward-redeemed':
            return

        redemptionJson = jsonResponse['data']['redemption']
        channelId = redemptionJson['channel_id']
        twitchUser = None

        for user in self.__users:
            if channelId == user.fetchChannelId(
                clientId = self.__clientId,
                accessToken = self.__accessToken
            ):
                twitchUser = user
                break

        if twitchUser == None:
            raise RuntimeError(f'Unable to find channel with ID \"{channelId}\"')

        if redemptionJson['reward']['id'].lower() != twitchUser.rewardId:
            # this user has redeemed a non-POTD reward
            return

        userThatRedeemed = redemptionJson['user']['login']
        print(f'Sending POTD for {twitchUser.twitchHandle} to {userThatRedeemed}')

        twitchChannel = self.get_channel(twitchUser.twitchHandle)

        try:
            picOfTheDay = twitchUser.fetchPicOfTheDay()
            await twitchChannel.send(f'{userThatRedeemed} here\'s the POTD: {picOfTheDay}')
        except ValueError:
            await twitchChannel.send(f'{twitchUser.twitchHandle} POTD is broken!')

    async def event_ready(self):
        print(f'{self.nick} is ready!')

        channelIds = [
            user.fetchChannelId(
                clientId = self.__clientId,
                accessToken = self.__accessToken
            ) for user in self.__users
        ]

        topics = [ f'channel-points-channel-v1.{channelId}' for channelId in channelIds ]

        # subscribe to pubhub channel points events
        await self.pubsub_subscribe(self.__accessToken, *topics)

    @commands.command(name = 'cynanbot')
    async def command_cynanbot(self, ctx):
        await ctx.send(f'{self.nick} says hello {ctx.author.name}!')
