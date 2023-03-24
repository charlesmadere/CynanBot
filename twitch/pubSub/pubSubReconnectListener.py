from typing import List, Optional

from twitchio.ext.pubsub.topics import Topic


class PubSubReconnectListener():

    async def onPubSubReconnect(self, topics: Optional[List[Topic]]) -> List[Topic]:
        pass
