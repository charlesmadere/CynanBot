from typing import Any

from frozendict import frozendict

from .twitchIrcTags import TwitchIrcTags
from .twitchIrcTagsParserInterface import TwitchIrcTagsParserInterface


class TwitchIrcTagsParser(TwitchIrcTagsParserInterface):

    async def parseTwitchIrcTags(
        self,
        rawIrcTags: dict[Any, Any]
    ) -> TwitchIrcTags:
        if not isinstance(rawIrcTags, dict):
            raise TypeError(f'rawIrcTags argument is malformed: \"{rawIrcTags}\"')

        # TODO
        raise RuntimeError()
