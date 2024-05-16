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
        if not isinstance(emoteImages, list):
            raise TypeError(f'emoteImages argument is malformed: \"{emoteImages}\"')
        elif len(emoteImages) == 0:
            raise ValueError(f'emoteImages argument is empty: {emoteImages}')
        elif not utils.isValidStr(emoteId):
            raise TypeError(f'emoteId argument is malformed: \"{emoteId}\"')
        elif not utils.isValidStr(emoteName):
            raise TypeError(f'emoteName argument is malformed: \"{emoteName}\"')
        elif not isinstance(emoteType, TwitchEmoteType):
            raise TypeError(f'emoteType argument is malformed: \"{emoteType}\"')
        elif not isinstance(subscriberTier, TwitchSubscriberTier):
            raise TypeError(f'subscriberTier argument is malformed: \"{subscriberTier}\"')

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
