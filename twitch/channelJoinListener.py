from typing import List


class ChannelJoinListener():

    async def joinChannels(self, channels: List[str]):
        pass

    async def isReadyToJoinChannels(self) -> bool:
        pass
