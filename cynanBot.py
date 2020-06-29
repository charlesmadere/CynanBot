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
        clientSecret: str,
        pubSubId: str,
        users: List[User]
    ):
        super().__init__(
            irc_token = ircToken,
            client_id = clientId,
            nick = 'CynanBot',
            prefix = '!',
            initial_channels = [ user.twitchHandle for user in users ]
        )

        self.ircToken = ircToken
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.pubSubId = pubSubId
        self.users = users

    async def event_message(self, message):
        await self.handle_commands(message)

    async def event_raw_pubsub(self, data):
        print(data)

    async def event_ready(self):
        print(f'{self.nick} is ready!')

        # subscribe to pubhub channel points events
        # await self.pubsub_subscribe(
        #     self.clientId,
        #     [ f'channel-points-channel-v1.{self.__fetchChannelIdForUser(user)}' for user in self.users ]
        # )
        self.__fetchPubSubToken()

    def __fetchChannelIdForUser(self, user: User):
        headers = {
            'Client-ID': self.clientId,
            'Authorization': f'Bearer {self.pubSubId}'
        }

        rawResponse = requests.get(
            f'https://api.twitch.tv/helix/users?login={user.twitchHandle}',
            headers = headers
        )

        print(self.clientId)
        print(self.ircToken)
        print(self.pubSubId)
        print(rawResponse.content)

        jsonResponse = json.loads(rawResponse.content)
        return jsonResponse['data'][0]['id']

    def __fetchPubSubToken(self):
        rawResponse = requests.post(
            f'https://id.twitch.tv/oauth2/token?client_id={self.clientId}&client_secret={self.clientSecret}&code={self.pubSubId}&grant_type=authorization_code&redirect_uri=http://localhost'
        )
        print(rawResponse)

    def __getUserForCommand(self, ctx):
        channelName = ctx.channel.name.lower()

        for user in self.users:
            if user.twitchHandle.lower() == channelName:
                return user

        raise RuntimeError(f'Unable to find user for channel \"{channelName}\"')

    @commands.command(name = 'cynanbot')
    async def command_cynanbot(self, ctx):
        await ctx.send(f'{self.nick} says hello {ctx.author.name}!')
