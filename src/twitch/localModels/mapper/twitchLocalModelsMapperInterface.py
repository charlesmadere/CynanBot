from abc import ABC, abstractmethod
from typing import Collection

from frozenlist import FrozenList

from ..twitchBitsUseType import TwitchBitsUseType as LocalBitsUseType
from ..twitchChatMessageFragment import TwitchChatMessageFragment as LocalChatMessageFragment
from ..twitchChatMessageFragmentCheermote import TwitchChatMessageFragmentCheermote as LocalChatMessageFragmentCheermote
from ..twitchChatMessageFragmentEmote import TwitchChatMessageFragmentEmote as LocalChatMessageFragmentEmote
from ..twitchChatMessageFragmentGif import TwitchChatMessageFragmentGif as LocalChatMessageFragmentGif
from ..twitchChatMessageFragmentMention import TwitchChatMessageFragmentMention as LocalChatMessageFragmentMention
from ..twitchChatMessageFragmentType import TwitchChatMessageFragmentType as LocalChatMessageFragmentType
from ..twitchCheerMetadata import TwitchCheerMetadata as LocalCheerMetadata
from ..twitchCustomPowerUp import TwitchCustomPowerUp as LocalCustomPowerUp
from ..twitchCustomPowerUpData import TwitchCustomPowerUpData as LocalCustomPowerUpData
from ..twitchEmoteImageFormat import TwitchEmoteImageFormat as LocalEmoteImageFormat
from ..twitchResubscriptionMessage import TwitchResubscriptionMessage as LocalResubscriptionMessage
from ..twitchResubscriptionMessageEmote import TwitchResubscriptionMessageEmote as LocalResubscriptionMessageEmote
from ..twitchWatchStreak import TwitchWatchStreak as LocalWatchStreak
from ...api.models.twitchBitsUseType import TwitchBitsUseType as ApiBitsUseType
from ...api.models.twitchChatMessageFragment import TwitchChatMessageFragment as ApiChatMessageFragment
from ...api.models.twitchChatMessageFragmentCheermote import \
    TwitchChatMessageFragmentCheermote as ApiChatMessageFragmentCheermote
from ...api.models.twitchChatMessageFragmentEmote import TwitchChatMessageFragmentEmote as ApiChatMessageFragmentEmote
from ...api.models.twitchChatMessageFragmentGif import TwitchChatMessageFragmentGif as ApiChatMessageFragmentGif
from ...api.models.twitchChatMessageFragmentMention import \
    TwitchChatMessageFragmentMention as ApiChatMessageFragmentMention
from ...api.models.twitchChatMessageFragmentType import TwitchChatMessageFragmentType as ApiChatMessageFragmentType
from ...api.models.twitchCheerMetadata import TwitchCheerMetadata as ApiCheerMetadata
from ...api.models.twitchCustomPowerUp import TwitchCustomPowerUp as ApiCustomPowerUp
from ...api.models.twitchCustomPowerUpData import TwitchCustomPowerUpData as ApiCustomPowerUpData
from ...api.models.twitchEmoteImageFormat import TwitchEmoteImageFormat as ApiEmoteImageFormat
from ...api.models.twitchResubscriptionMessage import TwitchResubscriptionMessage as ApiResubscriptionMessage
from ...api.models.twitchResubscriptionMessageEmote import \
    TwitchResubscriptionMessageEmote as ApiResubscriptionMessageEmote
from ...api.models.twitchWatchStreak import TwitchWatchStreak as ApiWatchStreak


class TwitchLocalModelsMapperInterface(ABC):

    @abstractmethod
    async def mapBitsUseType(
        self,
        bitsUseType: ApiBitsUseType | None,
    ) -> LocalBitsUseType | None:
        pass

    @abstractmethod
    async def mapChatMessageFragment(
        self,
        chatMessageFragment: ApiChatMessageFragment | None,
    ) -> LocalChatMessageFragment | None:
        pass

    @abstractmethod
    async def mapChatMessageFragments(
        self,
        chatMessageFragments: Collection[ApiChatMessageFragment] | None,
    ) -> FrozenList[LocalChatMessageFragment]:
        pass

    @abstractmethod
    async def mapChatMessageFragmentCheermote(
        self,
        chatMessageFragmentCheermote: ApiChatMessageFragmentCheermote | None,
    ) -> LocalChatMessageFragmentCheermote | None:
        pass

    @abstractmethod
    async def mapChatMessageFragmentEmote(
        self,
        chatMessageFragmentEmote: ApiChatMessageFragmentEmote | None,
    ) -> LocalChatMessageFragmentEmote | None:
        pass

    @abstractmethod
    async def mapChatMessageFragmentGif(
        self,
        chatMessageFragmentGif: ApiChatMessageFragmentGif | None,
    ) -> LocalChatMessageFragmentGif | None:
        pass

    @abstractmethod
    async def mapChatMessageFragmentMention(
        self,
        chatMessageFragmentMention: ApiChatMessageFragmentMention | None,
    ) -> LocalChatMessageFragmentMention | None:
        pass

    @abstractmethod
    async def mapChatMessageFragmentType(
        self,
        chatMessageFragmentType: ApiChatMessageFragmentType | None,
    ) -> LocalChatMessageFragmentType | None:
        pass

    @abstractmethod
    async def mapCheerMetadata(
        self,
        cheerMetadata: ApiCheerMetadata | None,
    ) -> LocalCheerMetadata | None:
        pass

    @abstractmethod
    async def mapCustomPowerUp(
        self,
        customPowerUp: ApiCustomPowerUp | None,
    ) -> LocalCustomPowerUp | None:
        pass

    @abstractmethod
    async def mapCustomPowerUpData(
        self,
        customPowerUpData: ApiCustomPowerUpData | None,
    ) -> LocalCustomPowerUpData | None:
        pass

    @abstractmethod
    async def mapEmoteImageFormat(
        self,
        emoteImageFormat: ApiEmoteImageFormat | None,
    ) -> LocalEmoteImageFormat | None:
        pass

    @abstractmethod
    async def mapResubscriptionMessage(
        self,
        resubscriptionMessage: ApiResubscriptionMessage | None,
    ) -> LocalResubscriptionMessage | None:
        pass

    @abstractmethod
    async def mapResubscriptionMessageEmote(
        self,
        resubscriptionMessageEmote: ApiResubscriptionMessageEmote | None,
    ) -> LocalResubscriptionMessageEmote | None:
        pass

    @abstractmethod
    async def mapWatchStreak(
        self,
        watchStreak: ApiWatchStreak | None,
    ) -> LocalWatchStreak | None:
        pass

    @abstractmethod
    async def requireChatMessageFragment(
        self,
        chatMessageFragment: ApiChatMessageFragment | None,
    ) -> LocalChatMessageFragment:
        pass

    @abstractmethod
    async def requireChatMessageFragmentType(
        self,
        chatMessageFragmentType: ApiChatMessageFragmentType | None,
    ) -> LocalChatMessageFragmentType:
        pass

    @abstractmethod
    async def requireEmoteImageFormat(
        self,
        emoteImageFormat: ApiEmoteImageFormat | None,
    ) -> LocalEmoteImageFormat:
        pass

    @abstractmethod
    async def requireResubscriptionMessageEmote(
        self,
        resubscriptionMessageEmote: ApiResubscriptionMessageEmote | None,
    ) -> LocalResubscriptionMessageEmote:
        pass
