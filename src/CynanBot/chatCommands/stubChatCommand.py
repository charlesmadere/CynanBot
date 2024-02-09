from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.twitch.configuration.twitchContext import TwitchContext


class StubChatCommand(AbsChatCommand):

    async def handleChatCommand(self, ctx: TwitchContext):
        pass
