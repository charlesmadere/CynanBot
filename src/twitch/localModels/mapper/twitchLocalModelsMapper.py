from .twitchLocalModelsMapperInterface import TwitchLocalModelsMapperInterface
from ..twitchChatMessageFragmentType import TwitchChatMessageFragmentType as LocalChatMessageFragmentType
from ...api.models.twitchChatMessageFragmentType import TwitchChatMessageFragmentType as ApiChatMessageFragmentType


class TwitchLocalModelsMapper(TwitchLocalModelsMapperInterface):

    async def mapChatMessageFragmentType(
        self,
        chatMessageFragmentType: ApiChatMessageFragmentType | None,
    ) -> LocalChatMessageFragmentType | None:
        if chatMessageFragmentType is None:
            return None

        match chatMessageFragmentType:
            case ApiChatMessageFragmentType.CHEERMOTE: return LocalChatMessageFragmentType.CHEERMOTE
            case ApiChatMessageFragmentType.EMOTE: return LocalChatMessageFragmentType.EMOTE
            case ApiChatMessageFragmentType.GIF: return LocalChatMessageFragmentType.GIF
            case ApiChatMessageFragmentType.MENTION: return LocalChatMessageFragmentType.MENTION
            case ApiChatMessageFragmentType.TEXT: return LocalChatMessageFragmentType.TEXT
