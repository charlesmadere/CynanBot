import CynanBot.misc.utils as utils
from CynanBot.twitch.api.twitchEmoteImage import TwitchEmoteImage
from CynanBot.twitch.api.twitchEmoteImageScale import TwitchEmoteImageScale
from CynanBot.twitch.api.twitchEmoteType import TwitchEmoteType
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier


class TwitchEmoteDetails():

    def __init__(
        self,
        emoteImages: list[TwitchEmoteImage],
        emoteId: str,
        emoteName: str,
        emoteType: TwitchEmoteType,
        subscriberTier: TwitchSubscriberTier
    ):
        if not utils.hasItems(emoteImages):
            raise ValueError(f'emoteImages argument is malformed: \"{emoteImages}\"')
        elif not utils.isValidStr(emoteId):
            raise ValueError(f'emoteId argument is malformed: \"{emoteId}\"')
        elif not utils.isValidStr(emoteName):
            raise ValueError(f'emoteName argument is malformed: \"{emoteName}\"')
        elif not isinstance(emoteType, TwitchEmoteType):
            raise ValueError(f'emoteType argument is malformed: \"{emoteType}\"')
        elif not isinstance(subscriberTier, TwitchSubscriberTier):
            raise ValueError(f'subscriberTier argument is malformed: \"{subscriberTier}\"')

        self.__emoteImages: list[TwitchEmoteImage] = emoteImages
        self.__emoteId: str = emoteId
        self.__emoteName: str = emoteName
        self.__emoteType: TwitchEmoteType = emoteType
        self.__subscriberTier: TwitchSubscriberTier = subscriberTier

    def getEmote(self, imageScale: TwitchEmoteImageScale) -> TwitchEmoteImage | None:
        if not isinstance(imageScale, TwitchEmoteImageScale):
            raise TypeError(f'imageScale argument is malformed: \"{imageScale}\"')

        for emoteImage in self.__emoteImages:
            if emoteImage.getImageScale() is imageScale:
                return emoteImage

        return None

    def getEmotes(self) -> list[TwitchEmoteImage]:
        return self.__emoteImages

    def getEmoteId(self) -> str:
        return self.__emoteId

    def getEmoteName(self) -> str:
        return self.__emoteName

    def getEmoteType(self) -> TwitchEmoteType:
        return self.__emoteType

    def getSubscriberTier(self) -> TwitchSubscriberTier:
        return self.__subscriberTier
