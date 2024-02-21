from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.api.twitchEmoteImage import TwitchEmoteImage
from CynanBot.twitch.api.twitchEmoteImageScale import TwitchEmoteImageScale
from CynanBot.twitch.api.twitchEmoteType import TwitchEmoteType
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier


class TwitchEmoteDetails():

    def __init__(
        self,
        emoteImages: List[TwitchEmoteImage],
        emoteId: str,
        emoteName: str,
        emoteType: TwitchEmoteType,
        subscriberTier: TwitchSubscriberTier
    ):
        if not utils.hasItems(emoteImages):
            raise ValueError(f'emoteImages argument is malformed: \"{emoteImages}\"')
        if not utils.isValidStr(emoteId):
            raise ValueError(f'emoteId argument is malformed: \"{emoteId}\"')
        if not utils.isValidStr(emoteName):
            raise ValueError(f'emoteName argument is malformed: \"{emoteName}\"')
        assert isinstance(emoteType, TwitchEmoteType), f"malformed {emoteType=}"
        assert isinstance(subscriberTier, TwitchSubscriberTier), f"malformed {subscriberTier=}"

        self.__emoteImages: List[TwitchEmoteImage] = emoteImages
        self.__emoteId: str = emoteId
        self.__emoteName: str = emoteName
        self.__emoteType: TwitchEmoteType = emoteType
        self.__subscriberTier: TwitchSubscriberTier = subscriberTier

    def getEmote(self, imageScale: TwitchEmoteImageScale) -> Optional[TwitchEmoteImage]:
        assert isinstance(imageScale, TwitchEmoteImageScale), f"malformed {imageScale=}"

        for emoteImage in self.__emoteImages:
            if emoteImage.getImageScale() is imageScale:
                return emoteImage

        return None

    def getEmotes(self) -> List[TwitchEmoteImage]:
        return self.__emoteImages

    def getEmoteId(self) -> str:
        return self.__emoteId

    def getEmoteName(self) -> str:
        return self.__emoteName

    def getEmoteType(self) -> TwitchEmoteType:
        return self.__emoteType

    def getSubscriberTier(self) -> TwitchSubscriberTier:
        return self.__subscriberTier
