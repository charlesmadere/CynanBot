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

        self.users = users
        self.channelIds = dict()

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    async def event_ready(self):
        print(f'{self.nick} is ready!')

    def __fetchChannelIdForUser(self, user: User):
        # TODO
        raise NotImplementedError()

    def __getChannelIdForUser(self, user: User):
        if user in self.channelIds:
            return self.channelIds[user]

        channelId = self.__fetchChannelIdForUser(user)
        self.channelIds[user] = channelId
        return channelId

    def __getUserForCommand(self, ctx):
        channelName = ctx.channel.name.lower()

        for user in self.users:
            if user.twitchHandle.lower() == channelName:
                return user

        raise RuntimeError(f'Unable to find user for channel \"{channelName}\"')

    @commands.command(name = 'cynanbot')
    async def command_cynanbot(self, ctx):
        await ctx.send(f'{self.nick} says hello {ctx.author.name}!')
