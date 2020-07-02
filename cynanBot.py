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
        rewardId: str,
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
        self.__rewardId = rewardId
        self.__users = users

    async def event_message(self, message):
        await self.handle_commands(message)

    async def event_raw_pubsub(self, data):
        dirtyJson = json.loads(data)
        messageJson = json.loads(dirtyJson.data['data']['message'])

        if messageJson['type'].lower() != 'reward-redeemed':
            return

        redemptionJson = messageJson['data']['redemption']

        if redemptionJson['reward']['id'].lower() != self.__rewardId:
            return

        channelId = redemptionJson['channel_id']
        twitchChannel = None

        for user in self.__users:
            if channelId == user.fetchChannelId():
                twitchChannel = user.twitchHandle
                break

        if twitchChannel == None:
            raise RuntimeError(f'Unable to find channel with ID \"{channelId}\"')

        userThatRedeemed = redemptionJson['user']['login']
        # TODO

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
