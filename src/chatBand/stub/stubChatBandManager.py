from ..chatBandManagerInterface import ChatBandManagerInterface


class StubChatBandManager(ChatBandManagerInterface):

    async def playInstrumentForMessage(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        author: str,
        message: str
    ) -> bool:
        # this method is intentionally empty
        return False
