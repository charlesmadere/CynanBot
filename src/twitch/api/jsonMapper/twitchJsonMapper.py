from datetime import datetime, timedelta
from typing import Any, Final

from frozendict import frozendict
from frozenlist import FrozenList

from .twitchJsonMapperInterface import TwitchJsonMapperInterface
from ..models.twitchApiScope import TwitchApiScope
from ..models.twitchBanRequest import TwitchBanRequest
from ..models.twitchBanResponse import TwitchBanResponse
from ..models.twitchBanResponseEntry import TwitchBanResponseEntry
from ..models.twitchBannedUser import TwitchBannedUser
from ..models.twitchBannedUserResponse import TwitchBannedUserResponse
from ..models.twitchBroadcasterSubscription import TwitchBroadcasterSubscription
from ..models.twitchBroadcasterSubscriptionResponse import TwitchBroadcasterSubscriptionResponse
from ..models.twitchBroadcasterType import TwitchBroadcasterType
from ..models.twitchChannelEditor import TwitchChannelEditor
from ..models.twitchChannelEditorsResponse import TwitchChannelEditorsResponse
from ..models.twitchChatAnnouncementColor import TwitchChatAnnouncementColor
from ..models.twitchChatBadge import TwitchChatBadge
from ..models.twitchChatMessage import TwitchChatMessage
from ..models.twitchChatMessageFragment import TwitchChatMessageFragment
from ..models.twitchChatMessageFragmentCheermote import TwitchChatMessageFragmentCheermote
from ..models.twitchChatMessageFragmentEmote import TwitchChatMessageFragmentEmote
from ..models.twitchChatMessageFragmentMention import TwitchChatMessageFragmentMention
from ..models.twitchChatMessageFragmentType import TwitchChatMessageFragmentType
from ..models.twitchChatMessageType import TwitchChatMessageType
from ..models.twitchChatter import TwitchChatter
from ..models.twitchChattersResponse import TwitchChattersResponse
from ..models.twitchCheerMetadata import TwitchCheerMetadata
from ..models.twitchCommunitySubGift import TwitchCommunitySubGift
from ..models.twitchConduitRequest import TwitchConduitRequest
from ..models.twitchConduitResponseEntry import TwitchConduitResponseEntry
from ..models.twitchConduitShard import TwitchConduitShard
from ..models.twitchEmoteDetails import TwitchEmoteDetails
from ..models.twitchEmoteImageFormat import TwitchEmoteImageFormat
from ..models.twitchEmoteImageScale import TwitchEmoteImageScale
from ..models.twitchEmoteType import TwitchEmoteType
from ..models.twitchEmotesResponse import TwitchEmotesResponse
from ..models.twitchEventSubDetails import TwitchEventSubDetails
from ..models.twitchEventSubRequest import TwitchEventSubRequest
from ..models.twitchEventSubResponse import TwitchEventSubResponse
from ..models.twitchFollower import TwitchFollower
from ..models.twitchFollowersResponse import TwitchFollowersResponse
from ..models.twitchNoticeType import TwitchNoticeType
from ..models.twitchOutcomeColor import TwitchOutcomeColor
from ..models.twitchOutcomePredictor import TwitchOutcomePredictor
from ..models.twitchPaginationResponse import TwitchPaginationResponse
from ..models.twitchPollChoice import TwitchPollChoice
from ..models.twitchPollStatus import TwitchPollStatus
from ..models.twitchPredictionStatus import TwitchPredictionStatus
from ..models.twitchRaid import TwitchRaid
from ..models.twitchResub import TwitchResub
from ..models.twitchReward import TwitchReward
from ..models.twitchRewardRedemptionStatus import TwitchRewardRedemptionStatus
from ..models.twitchSendChatAnnouncementRequest import TwitchSendChatAnnouncementRequest
from ..models.twitchSendChatDropReason import TwitchSendChatDropReason
from ..models.twitchSendChatMessageRequest import TwitchSendChatMessageRequest
from ..models.twitchSendChatMessageResponse import TwitchSendChatMessageResponse
from ..models.twitchStartCommercialDetails import TwitchStartCommercialDetails
from ..models.twitchStartCommercialResponse import TwitchStartCommercialResponse
from ..models.twitchStreamType import TwitchStreamType
from ..models.twitchSubscriberTier import TwitchSubscriberTier
from ..models.twitchThemeMode import TwitchThemeMode
from ..models.twitchTokensDetails import TwitchTokensDetails
from ..models.twitchUserSubscription import TwitchUserSubscription
from ..models.twitchUserType import TwitchUserType
from ..models.twitchValidationResponse import TwitchValidationResponse
from ..models.twitchWebsocketChannelPointsVoting import TwitchWebsocketChannelPointsVoting
from ..models.twitchWebsocketCondition import TwitchWebsocketCondition
from ..models.twitchWebsocketConnectionStatus import TwitchWebsocketConnectionStatus
from ..models.twitchWebsocketMessageType import TwitchWebsocketMessageType
from ..models.twitchWebsocketMetadata import TwitchWebsocketMetadata
from ..models.twitchWebsocketSub import TwitchWebsocketSub
from ..models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..models.twitchWebsocketTransport import TwitchWebsocketTransport
from ..models.twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod
from ....location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ....misc import utils as utils
from ....timber.timberInterface import TimberInterface


class TwitchJsonMapper(TwitchJsonMapperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

    async def __calculateExpirationTime(self, expiresInSeconds: int | None) -> datetime:
        now = datetime.now(self.__timeZoneRepository.getDefault())

        if utils.isValidInt(expiresInSeconds) and expiresInSeconds > 0:
            return now + timedelta(seconds = expiresInSeconds)
        else:
            return now - timedelta(weeks = 1)

    async def parseApiScope(
        self,
        apiScope: str | None
    ) -> TwitchApiScope | None:
        if not utils.isValidStr(apiScope):
            return None

        apiScope = apiScope.lower()

        match apiScope:
            case 'bits:read': return TwitchApiScope.BITS_READ
            case 'channel:bot': return TwitchApiScope.CHANNEL_BOT
            case 'channel:edit:commercial': return TwitchApiScope.CHANNEL_EDIT_COMMERCIAL
            case 'channel:manage:ads': return TwitchApiScope.CHANNEL_MANAGE_ADS
            case 'channel:manage:moderators': return TwitchApiScope.CHANNEL_MANAGE_MODERATORS
            case 'channel:manage:polls': return TwitchApiScope.CHANNEL_MANAGE_POLLS
            case 'channel:manage:predictions': return TwitchApiScope.CHANNEL_MANAGE_PREDICTIONS
            case 'channel:manage:redemptions': return TwitchApiScope.CHANNEL_MANAGE_REDEMPTIONS
            case 'channel:moderate': return TwitchApiScope.CHANNEL_MODERATE
            case 'channel:read:ads': return TwitchApiScope.CHANNEL_READ_ADS
            case 'channel:read:editors': return TwitchApiScope.CHANNEL_READ_EDITORS
            case 'channel:read:polls': return TwitchApiScope.CHANNEL_READ_POLLS
            case 'channel:read:predictions': return TwitchApiScope.CHANNEL_READ_PREDICTIONS
            case 'channel:read:redemptions': return TwitchApiScope.CHANNEL_READ_REDEMPTIONS
            case 'channel:read:subscriptions': return TwitchApiScope.CHANNEL_READ_SUBSCRIPTIONS
            case 'channel_editor': return TwitchApiScope.CHANNEL_EDITOR
            case 'channel_subscriptions': return TwitchApiScope.CHANNEL_SUBSCRIPTIONS
            case 'chat:edit': return TwitchApiScope.CHAT_EDIT
            case 'chat:read': return TwitchApiScope.CHAT_READ
            case 'moderation:read': return TwitchApiScope.MODERATION_READ
            case 'moderator:manage:announcements': return TwitchApiScope.MODERATOR_MANAGE_ANNOUNCEMENTS
            case 'moderator:manage:banned_users': return TwitchApiScope.MODERATOR_MANAGE_BANNED_USERS
            case 'moderator:manage:chat_messages': return TwitchApiScope.MODERATOR_MANAGE_CHAT_MESSAGES
            case 'moderator:read:chatters': return TwitchApiScope.MODERATOR_READ_CHATTERS
            case 'moderator:read:chat_settings': return TwitchApiScope.MODERATOR_READ_CHAT_SETTINGS
            case 'moderator:read:followers': return TwitchApiScope.MODERATOR_READ_FOLLOWERS
            case 'moderator:read:moderators': return TwitchApiScope.MODERATOR_READ_MODERATORS
            case 'user:bot': return TwitchApiScope.USER_BOT
            case 'user:read:broadcast': return TwitchApiScope.USER_READ_BROADCAST
            case 'user:read:chat': return TwitchApiScope.USER_READ_CHAT
            case 'user:read:emotes': return TwitchApiScope.USER_READ_EMOTES
            case 'user:read:follows': return TwitchApiScope.USER_READ_FOLLOWS
            case 'user:read:subscriptions': return TwitchApiScope.USER_READ_SUBSCRIPTIONS
            case 'user:write:chat': return TwitchApiScope.USER_WRITE_CHAT
            case 'user_subscriptions': return TwitchApiScope.USER_SUBSCRIPTIONS
            case 'whispers:edit': return TwitchApiScope.WHISPERS_EDIT
            case 'whispers:read': return TwitchApiScope.WHISPERS_READ
            case _:
                self.__timber.log('TwitchJsonMapper', f'Encountered unknown TwitchApiScope value: \"{apiScope}\"')
                return None

    async def parseBanResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchBanResponse | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')

        if not isinstance(data, list) or len(data) == 0:
            return None

        entries: list[TwitchBanResponseEntry] = list()

        for dataEntry in data:
            entry = await self.parseBanResponseEntry(dataEntry)
            entries.append(entry)

        entries.sort(key = lambda entry: entry.createdAt, reverse = True)
        frozenEntries: FrozenList[TwitchBanResponseEntry] = FrozenList(entries)
        frozenEntries.freeze()

        return TwitchBanResponse(
            data = frozenEntries
        )

    async def parseBanResponseEntry(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchBanResponseEntry:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            raise TypeError(f'jsonResponse argument is malformed: \"{jsonResponse}\"')

        createdAt = utils.getDateTimeFromDict(jsonResponse, 'created_at')

        endTime: datetime | None = None
        if 'end_time' in jsonResponse and utils.isValidStr(jsonResponse.get('end_time')):
            endTime = utils.getDateTimeFromDict(jsonResponse, 'end_time')

        broadcasterId = utils.getStrFromDict(jsonResponse, 'broadcaster_id')
        moderatorId = utils.getStrFromDict(jsonResponse, 'moderator_id')
        userId = utils.getStrFromDict(jsonResponse, 'user_id')

        return TwitchBanResponseEntry(
            createdAt = createdAt,
            endTime = endTime,
            broadcasterId = broadcasterId,
            moderatorId = moderatorId,
            userId = userId
        )

    async def parseBannedUserResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchBannedUserResponse | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')

        if not isinstance(data, list):
            return None
        elif len(data) == 0:
            return TwitchBannedUserResponse()

        dataEntry: dict[str, Any] | Any | None = data[0]
        if not isinstance(dataEntry, dict) or len(dataEntry) == 0:
            return None

        createdAt = utils.getDateTimeFromDict(dataEntry, 'created_at')

        expiresAt: datetime | None = None
        if 'expires_at' in dataEntry and utils.isValidStr(dataEntry.get('expires_at')):
            expiresAt = utils.getDateTimeFromDict(dataEntry, 'expires_at')

        moderatorId = utils.getStrFromDict(dataEntry, 'moderator_id')
        moderatorLogin = utils.getStrFromDict(dataEntry, 'moderator_login')
        moderatorName = utils.getStrFromDict(dataEntry, 'moderator_name')

        reason: str | None = None
        if 'reason' in dataEntry and utils.isValidStr(dataEntry.get('reason')):
            reason = utils.getStrFromDict(dataEntry, 'reason')

        userId = utils.getStrFromDict(dataEntry, 'user_id')
        userLogin = utils.getStrFromDict(dataEntry, 'user_login')
        userName = utils.getStrFromDict(dataEntry, 'user_name')

        bannedUser = TwitchBannedUser(
            createdAt = createdAt,
            expiresAt = expiresAt,
            moderatorId = moderatorId,
            moderatorLogin = moderatorLogin,
            moderatorName = moderatorName,
            reason = reason,
            userId = userId,
            userLogin = userLogin,
            userName = userName
        )

        return TwitchBannedUserResponse(
            bannedUser = bannedUser
        )

    async def parseBroadcasterSubscription(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchBroadcasterSubscription | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')

        if not isinstance(data, list) or len(data) == 0:
            return None

        dataEntry: dict[str, Any] | Any | None = data[0]
        if not isinstance(dataEntry, dict) or len(dataEntry) == 0:
            return None

        isGift = utils.getBoolFromDict(dataEntry, 'is_gift')

        broadcasterId = utils.getStrFromDict(dataEntry, 'broadcaster_id')
        broadcasterLogin = utils.getStrFromDict(dataEntry, 'broadcaster_login')
        broadcasterName = utils.getStrFromDict(dataEntry, 'broadcaster_name')

        gifterId: str | None = None
        if 'gifter_id' in dataEntry and utils.isValidStr(dataEntry.get('gifter_id')):
            gifterId = utils.getStrFromDict(dataEntry, 'gifter_id')

        gifterLogin: str | None = None
        if 'gifter_login' in dataEntry and utils.isValidStr(dataEntry.get('gifter_login')):
            gifterLogin = utils.getStrFromDict(dataEntry, 'gifter_login')

        gifterName: str | None = None
        if 'gifter_name' in dataEntry and utils.isValidStr(dataEntry.get('gifter_name')):
            gifterName = utils.getStrFromDict(dataEntry, 'gifter_name')

        planName: str | None = None
        if 'plan_name' in dataEntry and utils.isValidStr(dataEntry.get('plan_name')):
            planName = utils.getStrFromDict(dataEntry, 'plan_name')

        userId = utils.getStrFromDict(dataEntry, 'user_id')
        userLogin = utils.getStrFromDict(dataEntry, 'user_login')
        userName = utils.getStrFromDict(dataEntry, 'user_name')

        tier = await self.requireSubscriberTier(utils.getStrFromDict(dataEntry, 'tier'))

        return TwitchBroadcasterSubscription(
            isGift = isGift,
            broadcasterId = broadcasterId,
            broadcasterLogin = broadcasterLogin,
            broadcasterName = broadcasterName,
            gifterId = gifterId,
            gifterLogin = gifterLogin,
            gifterName = gifterName,
            planName = planName,
            userId = userId,
            userLogin = userLogin,
            userName = userName,
            tier = tier
        )

    async def parseBroadcasterSubscriptionResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchBroadcasterSubscriptionResponse | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')
        subscription: TwitchBroadcasterSubscription | None = None

        if isinstance(data, list) and len(data) >= 1:
            subscription = await self.parseBroadcasterSubscription(data[0])

        points = utils.getIntFromDict(jsonResponse, 'points', fallback = 0)
        total = utils.getIntFromDict(jsonResponse, 'total', fallback = 0)

        return TwitchBroadcasterSubscriptionResponse(
            points = points,
            total = total,
            subscription = subscription
        )

    async def parseBroadcasterType(
        self,
        broadcasterType: str | Any | None
    ) -> TwitchBroadcasterType:
        if not utils.isValidStr(broadcasterType):
            return TwitchBroadcasterType.NORMAL

        broadcasterType = broadcasterType.lower()

        match broadcasterType:
            case 'affiliate': return TwitchBroadcasterType.AFFILIATE
            case 'partner': return TwitchBroadcasterType.PARTNER
            case _:
                self.__timber.log('TwitchJsonMapper', f'Encountered unknown TwitchBroadcasterType value: \"{broadcasterType}\"')
                return TwitchBroadcasterType.NORMAL

    async def parseChannelEditor(
        self,
        jsonResponse: dict[str, Any]
    ) -> TwitchChannelEditor:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            raise TypeError(f'jsonResponse argument is malformed: \"{jsonResponse}\"')

        createdAt = utils.getDateTimeFromDict(jsonResponse, 'created_at')
        userId = utils.getStrFromDict(jsonResponse, 'user_id')
        userName = utils.getStrFromDict(jsonResponse, 'user_name')

        return TwitchChannelEditor(
            createdAt = createdAt,
            userId = userId,
            userName = userName
        )

    async def parseChannelEditorsResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChannelEditorsResponse | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        channelEditors: list[TwitchChannelEditor] = list()
        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')

        if isinstance(data, list) and len(data) >= 1:
            for channelEditorJson in data:
                channelEditor = await self.parseChannelEditor(channelEditorJson)
                channelEditors.append(channelEditor)

            channelEditors.sort(key = lambda editor: editor.createdAt, reverse = True)

        frozenChannelEditors: FrozenList[TwitchChannelEditor] = FrozenList(channelEditors)
        frozenChannelEditors.freeze()

        return TwitchChannelEditorsResponse(
            editors = frozenChannelEditors
        )

    async def parseChatBadge(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChatBadge | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        badgeId = utils.getStrFromDict(jsonResponse, 'id')

        info: str | None = None
        if 'info' in jsonResponse and utils.isValidStr(jsonResponse.get('info')):
            info = utils.getStrFromDict(jsonResponse, 'info')

        setId = utils.getStrFromDict(jsonResponse, 'set_id')

        return TwitchChatBadge(
            badgeId = badgeId,
            info = info,
            setId = setId
        )

    async def parseChatMessage(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChatMessage | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        text: str | None = None
        if 'text' in jsonResponse and utils.isValidStr(jsonResponse.get('text')):
            text = utils.getStrFromDict(jsonResponse, 'text', clean = True)

        if not utils.isValidStr(text):
            return None

        fragments: FrozenList[TwitchChatMessageFragment] | None = None
        fragmentsList: list[dict[str, Any]] | Any | None = jsonResponse.get('fragments')

        if isinstance(fragmentsList, list) and len(fragmentsList) >= 1:
            fragments = FrozenList()

            for index, fragmentJson in enumerate(fragmentsList):
                fragment = await self.parseChatMessageFragment(fragmentJson)

                if fragment is None:
                    self.__timber.log('TwitchJsonMapper', f'Unable to parse value at index {index} for \"fragments\" data ({jsonResponse=})')
                else:
                    fragments.append(fragment)

            fragments.freeze()

        return TwitchChatMessage(
            fragments = fragments,
            text = text
        )

    async def parseChatMessageFragment(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChatMessageFragment | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        text = utils.getStrFromDict(jsonResponse, 'text', clean = True)

        cheermote: TwitchChatMessageFragmentCheermote | None = None
        if 'cheermote' in jsonResponse:
            cheermote = await self.parseChatMessageFragmentCheermote(jsonResponse.get('cheermote'))

        emote: TwitchChatMessageFragmentEmote | None = None
        if 'emote' in jsonResponse:
            emote = await self.parseChatMessageFragmentEmote(jsonResponse.get('emote'))

        mention: TwitchChatMessageFragmentMention | None = None
        if 'mention' in jsonResponse:
            mention = await self.parseChatMessageFragmentMention(jsonResponse.get('mention'))

        fragmentTypeString = utils.getStrFromDict(jsonResponse, 'type')
        fragmentType = await self.requireChatMessageFragmentType(fragmentTypeString)

        return TwitchChatMessageFragment(
            text = text,
            cheermote = cheermote,
            emote = emote,
            mention = mention,
            fragmentType = fragmentType
        )

    async def parseChatMessageFragmentCheermote(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChatMessageFragmentCheermote | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        bits = utils.getIntFromDict(jsonResponse, 'bits')
        tier = utils.getIntFromDict(jsonResponse, 'tier')
        prefix = utils.getStrFromDict(jsonResponse, 'prefix')

        return TwitchChatMessageFragmentCheermote(
            bits = bits,
            tier = tier,
            prefix = prefix
        )

    async def parseChatMessageFragmentEmote(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChatMessageFragmentEmote | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        frozenFormats: frozenset[TwitchEmoteImageFormat] | None = None
        formatsList: list[str] | Any | None = jsonResponse.get('format')

        if isinstance(formatsList, list) and len(formatsList) >= 1:
            formats: set[TwitchEmoteImageFormat] = set()

            for index, formatString in enumerate(formatsList):
                emoteImageFormat = await self.parseEmoteImageFormat(formatString)

                if emoteImageFormat is None:
                    self.__timber.log('TwitchJsonMapper', f'Unable to parse value at index {index} for \"format\" data ({jsonResponse=})')
                else:
                    formats.add(emoteImageFormat)

            frozenFormats = frozenset(formats)

        emoteId = utils.getStrFromDict(jsonResponse, 'id')
        emoteSetId = utils.getStrFromDict(jsonResponse, 'emote_set_id')
        ownerId = utils.getStrFromDict(jsonResponse, 'owner_id')

        return TwitchChatMessageFragmentEmote(
            formats = frozenFormats,
            emoteId = emoteId,
            emoteSetId = emoteSetId,
            ownerId = ownerId
        )

    async def parseChatMessageFragmentMention(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChatMessageFragmentMention | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        userId = utils.getStrFromDict(jsonResponse, 'user_id')
        userLogin = utils.getStrFromDict(jsonResponse, 'user_login')
        userName = utils.getStrFromDict(jsonResponse, 'user_name')

        return TwitchChatMessageFragmentMention(
            userId = userId,
            userLogin = userLogin,
            userName = userName
        )

    async def parseChatMessageFragmentType(
        self,
        fragmentType: str | Any | None
    ) -> TwitchChatMessageFragmentType | None:
        if not utils.isValidStr(fragmentType):
            return None

        fragmentType = fragmentType.lower()

        match fragmentType:
            case 'cheermote': return TwitchChatMessageFragmentType.CHEERMOTE
            case 'emote': return TwitchChatMessageFragmentType.EMOTE
            case 'mention': return TwitchChatMessageFragmentType.MENTION
            case 'text': return TwitchChatMessageFragmentType.TEXT
            case _: return None

    async def parseChatMessageType(
        self,
        messageType: str | Any | None
    ) -> TwitchChatMessageType | None:
        if not utils.isValidStr(messageType):
            return None

        messageType = messageType.lower()

        match messageType:
            case 'channel_points_highlighted': return TwitchChatMessageType.CHANNEL_POINTS_HIGHLIGHTED
            case 'channel_points_sub_only': return TwitchChatMessageType.CHANNEL_POINTS_SUB_ONLY
            case 'power_ups_gigantified_emote': return TwitchChatMessageType.POWER_UPS_GIGANTIFIED_EMOTE
            case 'power_ups_message_effect': return TwitchChatMessageType.POWER_UPS_MESSAGE_EFFECT
            case 'user_intro': return TwitchChatMessageType.USER_INTRO
            case _: return None

    async def parseChatter(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChatter:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            raise TypeError(f'jsonResponse argument is malformed: \"{jsonResponse}\"')

        userId = utils.getStrFromDict(jsonResponse, 'user_id')
        userLogin = utils.getStrFromDict(jsonResponse, 'user_login')
        userName = utils.getStrFromDict(jsonResponse, 'user_name')

        return TwitchChatter(
            userId = userId,
            userLogin = userLogin,
            userName = userName
        )

    async def parseChattersResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchChattersResponse | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        total = utils.getIntFromDict(jsonResponse, 'total', fallback = 0)
        pagination = await self.parsePaginationResponse(jsonResponse.get('pagination'))

        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')
        frozenChatters: FrozenList[TwitchChatter]

        if isinstance(data, list) and len(data) >= 1:
            chatters: list[TwitchChatter] = list()

            for chatterJson in data:
                chatter = await self.parseChatter(chatterJson)
                chatters.append(chatter)

            chatters.sort(key = lambda chatter: chatter.userName.casefold())
            frozenChatters = FrozenList(chatters)
        else:
            frozenChatters = FrozenList()

        frozenChatters.freeze()

        return TwitchChattersResponse(
            data = frozenChatters,
            total = total,
            pagination = pagination
        )

    async def parseCheerMetadata(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchCheerMetadata | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        bits = utils.getIntFromDict(jsonResponse, 'bits', fallback = 0)

        return TwitchCheerMetadata(
            bits = bits
        )

    async def parseCommunitySubGift(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchCommunitySubGift | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        cumulativeTotal: int | None = None
        if 'cumulative_total' in jsonResponse and utils.isValidInt(jsonResponse.get('cumulative_total')):
            cumulativeTotal = utils.getIntFromDict(jsonResponse, 'cumulative_total')

        total = utils.getIntFromDict(jsonResponse, 'total')
        communitySubGiftId = utils.getStrFromDict(jsonResponse, 'id')
        subTier = await self.requireSubscriberTier(utils.getStrFromDict(jsonResponse, 'sub_tier'))

        return TwitchCommunitySubGift(
            cumulativeTotal = cumulativeTotal,
            total = total,
            communitySubGiftId = communitySubGiftId,
            subTier = subTier
        )

    async def parseCondition(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchWebsocketCondition | None:
        if not isinstance(jsonResponse, dict):
            return None

        broadcasterUserId: str | None = None
        if 'broadcaster_user_id' in jsonResponse and utils.isValidStr(jsonResponse.get('broadcaster_user_id')):
            broadcasterUserId = utils.getStrFromDict(jsonResponse, 'broadcaster_user_id')

        broadcasterUserLogin: str | None = None
        if 'broadcaster_user_login' in jsonResponse and utils.isValidStr(jsonResponse.get('broadcaster_user_login')):
            broadcasterUserLogin = utils.getStrFromDict(jsonResponse, 'broadcaster_user_login')

        broadcasterUserName: str | None = None
        if 'broadcaster_user_name' in jsonResponse and utils.isValidStr(jsonResponse.get('broadcaster_user_name')):
            broadcasterUserName = utils.getStrFromDict(jsonResponse, 'broadcaster_user_name')

        clientId: str | None = None
        if 'client_id' in jsonResponse and utils.isValidStr(jsonResponse.get('client_id')):
            clientId = utils.getStrFromDict(jsonResponse, 'client_id')

        fromBroadcasterUserId: str | None = None
        if 'from_broadcaster_user_id' in jsonResponse and utils.isValidStr(jsonResponse.get('from_broadcaster_user_id')):
            fromBroadcasterUserId = utils.getStrFromDict(jsonResponse, 'from_broadcaster_user_id')

        fromBroadcasterUserLogin: str | None = None
        if 'from_broadcaster_user_login' in jsonResponse and utils.isValidStr(jsonResponse.get('from_broadcaster_user_login')):
            fromBroadcasterUserLogin = utils.getStrFromDict(jsonResponse, 'from_broadcaster_user_login')

        fromBroadcasterUserName: str | None = None
        if 'from_broadcaster_user_name' in jsonResponse and utils.isValidStr(jsonResponse.get('from_broadcaster_user_name')):
            fromBroadcasterUserName = utils.getStrFromDict(jsonResponse, 'from_broadcaster_user_name')

        moderatorUserId: str | None = None
        if 'moderator_user_id' in jsonResponse and utils.isValidStr(jsonResponse.get('moderator_user_id')):
            moderatorUserId = utils.getStrFromDict(jsonResponse, 'moderator_user_id')

        moderatorUserLogin: str | None = None
        if 'moderator_user_login' in jsonResponse and utils.isValidStr(jsonResponse.get('moderator_user_login')):
            moderatorUserLogin = utils.getStrFromDict(jsonResponse, 'moderator_user_login')

        moderatorUserName: str | None = None
        if 'moderator_user_name' in jsonResponse and utils.isValidStr(jsonResponse.get('moderator_user_name')):
            moderatorUserName = utils.getStrFromDict(jsonResponse, 'moderator_user_name')

        rewardId: str | None = None
        if 'reward_id' in jsonResponse and utils.isValidStr(jsonResponse.get('reward_id')):
            rewardId = utils.getStrFromDict(jsonResponse, 'reward_id')

        toBroadcasterUserId: str | None = None
        if 'to_broadcaster_user_id' in jsonResponse and utils.isValidStr(jsonResponse.get('to_broadcaster_user_id')):
            toBroadcasterUserId = utils.getStrFromDict(jsonResponse, 'to_broadcaster_user_id')

        toBroadcasterUserLogin: str | None = None
        if 'to_broadcaster_user_login' in jsonResponse and utils.isValidStr(jsonResponse.get('to_broadcaster_user_login')):
            toBroadcasterUserLogin = utils.getStrFromDict(jsonResponse, 'to_broadcaster_user_login')

        toBroadcasterUserName: str | None = None
        if 'to_broadcaster_user_name' in jsonResponse and utils.isValidStr(jsonResponse.get('to_broadcaster_user_name')):
            toBroadcasterUserName = utils.getStrFromDict(jsonResponse, 'to_broadcaster_user_name')

        userId: str | None = None
        if 'user_id' in jsonResponse and utils.isValidStr(jsonResponse.get('user_id')):
            userId = utils.getStrFromDict(jsonResponse, 'user_id')

        userLogin: str | None = None
        if 'user_login' in jsonResponse and utils.isValidStr(jsonResponse.get('user_login')):
            userLogin = utils.getStrFromDict(jsonResponse, 'user_login')

        userName: str | None = None
        if 'user_name' in jsonResponse and utils.isValidStr(jsonResponse.get('user_name')):
            userName = utils.getStrFromDict(jsonResponse, 'user_name')

        return TwitchWebsocketCondition(
            broadcasterUserId = broadcasterUserId,
            broadcasterUserLogin = broadcasterUserLogin,
            broadcasterUserName = broadcasterUserName,
            clientId = clientId,
            fromBroadcasterUserId = fromBroadcasterUserId,
            fromBroadcasterUserLogin = fromBroadcasterUserLogin,
            fromBroadcasterUserName = fromBroadcasterUserName,
            moderatorUserId = moderatorUserId,
            moderatorUserLogin = moderatorUserLogin,
            moderatorUserName = moderatorUserName,
            rewardId = rewardId,
            toBroadcasterUserId = toBroadcasterUserId,
            toBroadcasterUserLogin = toBroadcasterUserLogin,
            toBroadcasterUserName = toBroadcasterUserName,
            userId = userId,
            userLogin = userLogin,
            userName = userName
        )

    async def parseConduitResponseEntry(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchConduitResponseEntry | None:
        if not isinstance(jsonResponse, dict):
            return None

        shardCount = utils.getIntFromDict(jsonResponse, 'shard_count')
        shardId = utils.getStrFromDict(jsonResponse, 'id')

        return TwitchConduitResponseEntry(
            shardCount = shardCount,
            shardId = shardId,
        )

    async def parseConduitShard(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchConduitShard | None:
        if not isinstance(jsonResponse, dict):
            return None

        conduitId = utils.getStrFromDict(jsonResponse, 'conduit_id')
        shard = utils.getStrFromDict(jsonResponse, 'shard')

        return TwitchConduitShard(
            conduitId = conduitId,
            shard = shard,
        )

    async def parseConnectionStatus(
        self,
        connectionStatus: str | Any | None
    ) -> TwitchWebsocketConnectionStatus | None:
        if not utils.isValidStr(connectionStatus):
            return None

        connectionStatus = connectionStatus.lower()

        match connectionStatus:
            case 'connected': return TwitchWebsocketConnectionStatus.CONNECTED
            case 'enabled': return TwitchWebsocketConnectionStatus.ENABLED
            case 'reconnecting': return TwitchWebsocketConnectionStatus.RECONNECTING
            case 'authorization_revoked': return TwitchWebsocketConnectionStatus.REVOKED
            case 'user_removed': return TwitchWebsocketConnectionStatus.USER_REMOVED
            case 'version_removed': return TwitchWebsocketConnectionStatus.VERSION_REMOVED
            case 'webhook_callback_verification_pending': return TwitchWebsocketConnectionStatus.WEBHOOK_CALLBACK_VERIFICATION_PENDING
            case _: return None

    async def parseEmoteDetails(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchEmoteDetails | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        imagesDictionary: dict[str, str] | Any | None = jsonResponse.get('images')
        images: dict[TwitchEmoteImageScale, str] = dict()
        if isinstance(imagesDictionary, dict) and len(imagesDictionary) >= 1:
            for imageScaleString, imageUrl in imagesDictionary.items():
                imageScale = await self.parseEmoteImageScale(imageScaleString)

                if imageScale is not None and utils.isValidUrl(imageUrl):
                    images[imageScale] = imageUrl
                else:
                    self.__timber.log('TwitchJsonMapper', f'Unable to parse value at key \"{imageScaleString}\" for \"images\" data ({jsonResponse=})')

        if len(images) == 0:
            self.__timber.log('TwitchJsonMapper', f'Encountered missing/invalid \"images\" field in JSON data: ({jsonResponse=})')
            return None

        formatsList: list[str] | Any | None = jsonResponse.get('format')
        formats: set[TwitchEmoteImageFormat] = set()
        if isinstance(formatsList, list) and len(formatsList) >= 1:
            for index, formatString in enumerate(formatsList):
                emoteImageFormat = await self.parseEmoteImageFormat(formatString)

                if emoteImageFormat is None:
                    self.__timber.log('TwitchJsonMapper', f'Unable to parse value at index {index} for \"format\" data ({jsonResponse=})')
                else:
                    formats.add(emoteImageFormat)

        if len(formats) == 0:
            self.__timber.log('TwitchJsonMapper', f'Encountered missing/invalid \"format\" field in JSON data: ({jsonResponse=})')
            return None

        scalesList: list[str] | Any | None = jsonResponse.get('scale')
        scales: set[TwitchEmoteImageScale] = set()
        if isinstance(scalesList, list) and len(scalesList) >= 1:
            for index, scaleString in enumerate(scalesList):
                scale = await self.parseEmoteImageScale(scaleString)

                if scale is None:
                    self.__timber.log('TwitchJsonMapper', f'Unable to parse value at index {index} for \"scale\" data ({jsonResponse=})')
                else:
                    scales.add(scale)

        if len(scales) == 0:
            self.__timber.log('TwitchJsonMapper', f'Encountered missing/invalid \"scale\" field in JSON data: ({jsonResponse=})')
            return None

        themeModesArray: list[str] | Any | None = jsonResponse.get('theme_mode')
        themeModes: set[TwitchThemeMode] = set()
        if isinstance(themeModesArray, list) and len(themeModesArray) >= 1:
            for index, themeModeString in enumerate(themeModesArray):
                themeMode = await self.parseThemeMode(themeModeString)

                if themeMode is None:
                    self.__timber.log('TwitchJsonMapper', f'Unable to parse value at index {index} for \"theme_mode\" data ({jsonResponse})')
                else:
                    themeModes.add(themeMode)

        if len(themeModes) == 0:
            self.__timber.log('TwitchJsonMapper', f'Encountered missing/invalid \"theme_mode\" field in JSON data: ({jsonResponse=})')
            return None

        emoteId = utils.getStrFromDict(jsonResponse, 'id')
        emoteSetId = utils.getStrFromDict(jsonResponse, 'emote_set_id')
        name = utils.getStrFromDict(jsonResponse, 'name')

        emoteType = await self.parseEmoteType(jsonResponse.get('emote_type'))
        if emoteType is None:
            self.__timber.log('TwitchJsonMapper', f'Unable to parse value for \"emote_type\" data ({jsonResponse=})')
            return None

        tier: TwitchSubscriberTier | None = None
        if 'tier' in jsonResponse and utils.isValidStr(jsonResponse.get('tier')):
            tier = await self.parseSubscriberTier(utils.getStrFromDict(jsonResponse, 'tier'))

        return TwitchEmoteDetails(
            images = frozendict(images),
            formats = frozenset(formats),
            scales = frozenset(scales),
            themeModes = frozenset(themeModes),
            emoteId = emoteId,
            emoteSetId = emoteSetId,
            name = name,
            emoteType = emoteType,
            tier = tier
        )

    async def parseEmoteImageFormat(
        self,
        emoteImageFormat: str | Any | None
    ) -> TwitchEmoteImageFormat | None:
        if not utils.isValidStr(emoteImageFormat):
            return None

        emoteImageFormat = emoteImageFormat.lower()

        match emoteImageFormat:
            case 'animated': return TwitchEmoteImageFormat.ANIMATED
            case 'static': return TwitchEmoteImageFormat.STATIC
            case _: return None

    async def parseEmoteImageScale(
        self,
        emoteImageScale: str | Any | None
    ) -> TwitchEmoteImageScale | None:
        if not utils.isValidStr(emoteImageScale):
            return None

        emoteImageScale = emoteImageScale.lower()

        match emoteImageScale:
            case 'url_1x': return TwitchEmoteImageScale.SMALL
            case 'url_2x': return TwitchEmoteImageScale.MEDIUM
            case 'url_4x': return TwitchEmoteImageScale.LARGE
            case '1.0': return TwitchEmoteImageScale.SMALL
            case '2.0': return TwitchEmoteImageScale.MEDIUM
            case '3.0': return TwitchEmoteImageScale.LARGE
            case _: return None

    async def parseEmotesResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchEmotesResponse | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')
        if not isinstance(data, list) or len(data) == 0:
            self.__timber.log('TwitchJsonMapper', f'Encountered missing/invalid \"data\" field in JSON data: ({jsonResponse=})')
            return None

        emoteData: FrozenList[TwitchEmoteDetails] = FrozenList()
        for index, emoteDetailsJson in enumerate(data):
            emoteDetails = await self.parseEmoteDetails(emoteDetailsJson)

            if emoteDetails is None:
                self.__timber.log('TwitchJsonMapper', f'Unable to parse value at index {index} for \"data\" data ({emoteDetailsJson=}) ({jsonResponse=})')
            else:
                emoteData.append(emoteDetails)

        emoteData.freeze()

        if len(emoteData) == 0:
            self.__timber.log('TwitchJsonMapper', f'Encountered missing/invalid \"data\" field in JSON data: ({jsonResponse=})')
            return None

        template = utils.getStrFromDict(jsonResponse, 'template')

        return TwitchEmotesResponse(
            emoteData = emoteData,
            template = template
        )

    async def parseEmoteType(
        self,
        emoteType: str | None
    ) -> TwitchEmoteType | None:
        if not utils.isValidStr(emoteType):
            return None

        emoteType = emoteType.lower()

        match emoteType:
            case 'bitstier': return TwitchEmoteType.BITS
            case 'follower': return TwitchEmoteType.FOLLOWER
            case 'subscriptions': return TwitchEmoteType.SUBSCRIPTIONS
            case _: return None

    async def parseEventSubDetails(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchEventSubDetails:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            raise TypeError(f'jsonResponse argument is malformed: \"{jsonResponse}\"')

        createdAt = utils.getDateTimeFromDict(jsonResponse, 'created_at')
        cost = utils.getIntFromDict(jsonResponse, 'cost')
        detailsId = utils.getStrFromDict(jsonResponse, 'id')
        version = utils.getStrFromDict(jsonResponse, 'version')
        condition = await self.requireCondition(jsonResponse.get('condition'))
        connectionStatus = await self.requireConnectionStatus(utils.getStrFromDict(jsonResponse, 'status'))
        connectionType = await self.requireSubscriptionType(utils.getStrFromDict(jsonResponse, 'type'))
        transport = await self.requireTransport(jsonResponse.get('transport'))

        return TwitchEventSubDetails(
            createdAt = createdAt,
            cost = cost,
            detailsId = detailsId,
            version = version,
            condition = condition,
            connectionStatus = connectionStatus,
            connectionType = connectionType,
            transport = transport
        )

    async def parseEventSubResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchEventSubResponse | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        eventSubDetails: list[TwitchEventSubDetails] = list()
        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')

        if isinstance(data, list) and len(data) >= 1:
            for eventSubDetailsJson in data:
                details = await self.parseEventSubDetails(eventSubDetailsJson)
                eventSubDetails.append(details)

        frozenEventSubDetails: FrozenList[TwitchEventSubDetails] = FrozenList(eventSubDetails)
        frozenEventSubDetails.freeze()

        maxTotalCost = utils.getIntFromDict(jsonResponse, 'max_total_cost')
        total = utils.getIntFromDict(jsonResponse, 'total')
        totalCost = utils.getIntFromDict(jsonResponse, 'total_cost')

        return TwitchEventSubResponse(
            data = frozenEventSubDetails,
            maxTotalCost = maxTotalCost,
            total = total,
            totalCost = totalCost
        )

    async def parseFollower(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchFollower:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            raise TypeError(f'jsonResponse argument is malformed: \"{jsonResponse}\"')

        followedAt = utils.getDateTimeFromDict(jsonResponse, 'followed_at')
        userId = utils.getStrFromDict(jsonResponse, 'user_id')
        userLogin = utils.getStrFromDict(jsonResponse, 'user_login')
        userName = utils.getStrFromDict(jsonResponse, 'user_name')

        return TwitchFollower(
            followedAt = followedAt,
            userId = userId,
            userLogin = userLogin,
            userName = userName
        )

    async def parseFollowersResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchFollowersResponse | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        followers: list[TwitchFollower] = list()
        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')

        if isinstance(data, list) and len(data) >= 1:
            for followerJson in data:
                follower = await self.parseFollower(followerJson)
                followers.append(follower)

            followers.sort(key = lambda follower: follower.followedAt, reverse = True)

        frozenFollowers: FrozenList[TwitchFollower] = FrozenList(followers)
        frozenFollowers.freeze()

        total = utils.getIntFromDict(jsonResponse, 'total', fallback = 0)
        pagination = await self.parsePaginationResponse(jsonResponse.get('pagination'))

        return TwitchFollowersResponse(
            followers = frozenFollowers,
            total = total,
            pagination = pagination
        )

    async def parseNoticeType(
        self,
        noticeType: str | Any | None
    ) -> TwitchNoticeType | None:
        if not utils.isValidStr(noticeType):
            return None

        noticeType = noticeType.lower()

        match noticeType:
            case 'announcement': return TwitchNoticeType.ANNOUNCEMENT
            case 'bits_badge_tier': return TwitchNoticeType.BITS_BADGE_TIER
            case 'charity_donation': return TwitchNoticeType.CHARITY_DONATION
            case 'community_sub_gift': return TwitchNoticeType.COMMUNITY_SUB_GIFT
            case 'gift_paid_upgrade':  return TwitchNoticeType.GIFT_PAID_UPGRADE
            case 'pay_it_forward': return TwitchNoticeType.PAY_IT_FORWARD
            case 'prime_paid_upgrade': return TwitchNoticeType.PRIME_PAID_UPGRADE
            case 'raid': return TwitchNoticeType.RAID
            case 'resub': return TwitchNoticeType.RE_SUB
            case 'sub': return TwitchNoticeType.SUB
            case 'sub_gift': return TwitchNoticeType.SUB_GIFT
            case 'unraid': return TwitchNoticeType.UN_RAID
            case _: return None

    async def parseOutcomeColor(
        self,
        outcomeColor: str | Any | None
    ) -> TwitchOutcomeColor | None:
        if not utils.isValidStr(outcomeColor):
            return None

        outcomeColor = outcomeColor.lower()

        match outcomeColor:
            case 'blue': return TwitchOutcomeColor.BLUE
            case 'pink': return TwitchOutcomeColor.PINK
            case _: return None

    async def parseOutcomePredictor(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchOutcomePredictor | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        channelPointsUsed = utils.getIntFromDict(jsonResponse, 'channel_points_used')

        channelPointsWon: int | None = None
        if 'channel_points_won' in jsonResponse and utils.isValidInt(jsonResponse.get('channel_points_won')):
            channelPointsWon = utils.getIntFromDict(jsonResponse, 'channel_points_won')

        userId = utils.getStrFromDict(jsonResponse, 'user_id')
        userLogin = utils.getStrFromDict(jsonResponse, 'user_login')
        userName = utils.getStrFromDict(jsonResponse, 'user_name')

        return TwitchOutcomePredictor(
            channelPointsUsed = channelPointsUsed,
            channelPointsWon = channelPointsWon,
            userId = userId,
            userLogin = userLogin,
            userName = userName
        )

    async def parsePaginationResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchPaginationResponse | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None
        elif 'cursor' not in jsonResponse or not utils.isValidStr(jsonResponse.get('cursor')):
            return None

        cursor = utils.getStrFromDict(jsonResponse, 'cursor')

        return TwitchPaginationResponse(
            cursor = cursor
        )

    async def parsePollChoice(
        self,
        jsonResponse: dict[str, Any] | None
    ) -> TwitchPollChoice | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        channelPointsVotes = utils.getIntFromDict(jsonResponse, 'channel_points_votes', 0)
        votes = utils.getIntFromDict(jsonResponse, 'votes', 0)
        choiceId = utils.getStrFromDict(jsonResponse, 'id')
        title = utils.getStrFromDict(jsonResponse, 'title')

        return TwitchPollChoice(
            channelPointsVotes = channelPointsVotes,
            votes = votes,
            choiceId = choiceId,
            title = title
        )

    async def parsePollStatus(
        self,
        pollStatus: str | Any | None
    ) -> TwitchPollStatus | None:
        if not utils.isValidStr(pollStatus):
            return None

        pollStatus = pollStatus.lower()

        match pollStatus:
            case 'active': return TwitchPollStatus.ACTIVE
            case 'archived': return TwitchPollStatus.ARCHIVED
            case 'completed': return TwitchPollStatus.COMPLETED
            case 'invalid': return TwitchPollStatus.INVALID
            case 'moderated': return TwitchPollStatus.MODERATED
            case 'terminated': return TwitchPollStatus.TERMINATED
            case _: return None

    async def parsePredictionStatus(
        self,
        predictionStatus: str | Any | None
    ) -> TwitchPredictionStatus | None:
        if not utils.isValidStr(predictionStatus):
            return None

        predictionStatus = predictionStatus.lower()

        match predictionStatus:
            case 'active': return TwitchPredictionStatus.ACTIVE
            case 'canceled': return TwitchPredictionStatus.CANCELED
            case 'locked': return TwitchPredictionStatus.LOCKED
            case 'resolved': return TwitchPredictionStatus.RESOLVED
            case _: return None

    async def parseRaid(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchRaid | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        viewerCount = utils.getIntFromDict(jsonResponse, 'viewer_count', fallback = 0)

        profileImageUrl: str | None = None
        if 'profile_image_url' in jsonResponse and utils.isValidUrl(jsonResponse.get('profile_image_url')):
            profileImageUrl = utils.getStrFromDict(jsonResponse, 'profile_image_url')

        userId = utils.getStrFromDict(jsonResponse, 'user_id')
        userLogin = utils.getStrFromDict(jsonResponse, 'user_login')
        userName = utils.getStrFromDict(jsonResponse, 'user_name')

        return TwitchRaid(
            viewerCount = viewerCount,
            profileImageUrl = profileImageUrl,
            userId = userId,
            userLogin = userLogin,
            userName = userName
        )

    async def parseResub(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchResub | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        gifterIsAnonymous: bool | None = None
        if 'gifter_is_anonymous' in jsonResponse and utils.isValidBool(jsonResponse.get('gifter_is_anonymous')):
            gifterIsAnonymous = utils.getBoolFromDict(jsonResponse, 'gifter_is_anonymous')

        isGift = utils.getBoolFromDict(jsonResponse, 'is_gift', fallback = False)
        isPrime = utils.getBoolFromDict(jsonResponse, 'is_prime', fallback = False)
        cumulativeMonths = utils.getIntFromDict(jsonResponse, 'cumulative_months')
        durationMonths = utils.getIntFromDict(jsonResponse, 'duration_months')
        streakMonths = utils.getIntFromDict(jsonResponse, 'streak_months')

        gifterUserId: str | None = None
        if 'gifter_user_id' in jsonResponse and utils.isValidStr(jsonResponse.get('gifter_user_id')):
            gifterUserId = utils.getStrFromDict(jsonResponse, 'gifter_user_id')

        gifterUserLogin: str | None = None
        if 'gifter_user_login' in jsonResponse and utils.isValidStr(jsonResponse.get('gifter_user_login')):
            gifterUserLogin = utils.getStrFromDict(jsonResponse, 'gifter_user_login')

        gifterUserName: str | None = None
        if 'gifter_user_name' in jsonResponse and utils.isValidStr(jsonResponse.get('gifter_user_name')):
            gifterUserName = utils.getStrFromDict(jsonResponse, 'gifter_user_name')

        subTierString = utils.getStrFromDict(jsonResponse, 'sub_tier')
        subTier = await self.requireSubscriberTier(subTierString)

        return TwitchResub(
            gifterIsAnonymous = gifterIsAnonymous,
            isGift = isGift,
            isPrime = isPrime,
            cumulativeMonths = cumulativeMonths,
            durationMonths = durationMonths,
            streakMonths = streakMonths,
            gifterUserId = gifterUserId,
            gifterUserLogin = gifterUserLogin,
            gifterUserName = gifterUserName,
            subTier = subTier
        )

    async def parseReward(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchReward | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        cost = utils.getIntFromDict(jsonResponse, 'cost')

        prompt: str | None = None
        if 'prompt' in jsonResponse and utils.isValidStr(jsonResponse.get('prompt')):
            prompt = utils.getStrFromDict(jsonResponse, 'prompt')

        rewardId = utils.getStrFromDict(jsonResponse, 'id')
        title = utils.getStrFromDict(jsonResponse, 'title')

        return TwitchReward(
            cost = cost,
            prompt = prompt,
            rewardId = rewardId,
            title = title
        )

    async def parseRewardRedemptionStatus(
        self,
        rewardRedemptionStatus: str | Any | None
    ) -> TwitchRewardRedemptionStatus | None:
        if not utils.isValidStr(rewardRedemptionStatus):
            return None

        rewardRedemptionStatus = rewardRedemptionStatus.lower()

        match rewardRedemptionStatus:
            case 'canceled': return TwitchRewardRedemptionStatus.CANCELED
            case 'fulfilled': return TwitchRewardRedemptionStatus.FULFILLED
            case 'unfulfilled': return TwitchRewardRedemptionStatus.UNFULFILLED
            case 'unknown': return TwitchRewardRedemptionStatus.UNKNOWN
            case _: return None

    async def parseSendChatDropReason(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchSendChatDropReason | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        code = utils.getStrFromDict(jsonResponse, 'code')

        message: str | None = None
        if 'message' in jsonResponse and utils.isValidStr(jsonResponse.get('message')):
            message = utils.getStrFromDict(jsonResponse, 'message')

        return TwitchSendChatDropReason(
            code = code,
            message = message
        )

    async def parseSendChatMessageResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchSendChatMessageResponse | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')
        if not isinstance(data, list) or len(data) == 0:
            return None

        dataEntry: dict[str, Any] | Any | None = data[0]
        if not isinstance(dataEntry, dict) or len(dataEntry) == 0:
            return None

        isSent = utils.getBoolFromDict(dataEntry, 'is_sent', fallback = False)
        messageId = utils.getStrFromDict(dataEntry, 'message_id')
        dropReason = await self.parseSendChatDropReason(dataEntry.get('drop_reason'))

        return TwitchSendChatMessageResponse(
            isSent = isSent,
            messageId = messageId,
            dropReason = dropReason
        )

    async def parseStartCommercialDetails(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchStartCommercialDetails | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        length = utils.getIntFromDict(jsonResponse, 'length')

        retryAfter: int | None = None
        if 'retry_after' in jsonResponse and utils.isValidInt(jsonResponse.get('retry_after')):
            retryAfter = utils.getIntFromDict(jsonResponse, 'retry_after')

        message: str | None = None
        if 'message' in jsonResponse and utils.isValidStr(jsonResponse.get('message')):
            message = utils.getStrFromDict(jsonResponse, 'message')

        return TwitchStartCommercialDetails(
            length = length,
            retryAfter = retryAfter,
            message = message
        )

    async def parseStartCommercialResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchStartCommercialResponse | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        dataArray: list[dict[str, Any]] | Any | None = jsonResponse.get('data')
        if not isinstance(dataArray, list) or len(dataArray) == 0:
            return None

        data: FrozenList[TwitchStartCommercialDetails] = FrozenList()

        for index, dataJson in enumerate(dataArray):
            commercialDetails = await self.parseStartCommercialDetails(dataJson)

            if commercialDetails is None:
                self.__timber.log('TwitchJsonMapper', f'Unable to parse value at index {index} ({commercialDetails=}) ({jsonResponse=})')
            else:
                data.append(commercialDetails)

        if len(data) == 0:
            return None

        data.freeze()

        return TwitchStartCommercialResponse(
            data = data
        )

    async def parseStreamType(
        self,
        streamType: str | None
    ) -> TwitchStreamType:
        if not utils.isValidStr(streamType):
            return TwitchStreamType.UNKNOWN

        streamType = streamType.lower()

        match streamType:
            case 'live': return TwitchStreamType.LIVE
            case _: return TwitchStreamType.UNKNOWN

    async def parseSubscriberTier(
        self,
        subscriberTier: str | Any | None
    ) -> TwitchSubscriberTier | None:
        if not utils.isValidStr(subscriberTier):
            return None

        subscriberTier = subscriberTier.lower()

        match subscriberTier:
            case 'prime': return TwitchSubscriberTier.PRIME
            case '1000': return TwitchSubscriberTier.TIER_ONE
            case '2000': return TwitchSubscriberTier.TIER_TWO
            case '3000': return TwitchSubscriberTier.TIER_THREE
            case _:
                self.__timber.log('TwitchJsonMapper', f'Encountered unknown TwitchSubscriberTier value: \"{subscriberTier}\"')
                return None

    async def parseSubscriptionType(
        self,
        subscriptionType: str | Any | None
    ) -> TwitchWebsocketSubscriptionType | None:
        if not utils.isValidStr(subscriptionType):
            return None

        subscriptionType = subscriptionType.lower()

        match subscriptionType:
            case 'channel.chat.message':
                return TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE
            case 'channel.channel_points_custom_reward_redemption.add':
                return TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION
            case 'channel.poll.begin':
                return TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN
            case 'channel.poll.end':
                return TwitchWebsocketSubscriptionType.CHANNEL_POLL_END
            case 'channel.poll.progress':
                return TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS
            case 'channel.prediction.begin':
                return TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN
            case 'channel.prediction.end':
                return TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END
            case 'channel.prediction.lock':
                return TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK
            case 'channel.prediction.progress':
                return TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS
            case 'channel.update':
                return TwitchWebsocketSubscriptionType.CHANNEL_UPDATE
            case 'channel.cheer':
                return TwitchWebsocketSubscriptionType.CHEER
            case 'channel.follow':
                return TwitchWebsocketSubscriptionType.FOLLOW
            case 'channel.raid':
                return TwitchWebsocketSubscriptionType.RAID
            case 'stream.offline':
                return TwitchWebsocketSubscriptionType.STREAM_OFFLINE
            case 'stream.online':
                return TwitchWebsocketSubscriptionType.STREAM_ONLINE
            case 'channel.subscribe':
                return TwitchWebsocketSubscriptionType.SUBSCRIBE
            case 'channel.subscription.gift':
                return TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT
            case 'channel.subscription.message':
                return TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE
            case 'user.update':
                return TwitchWebsocketSubscriptionType.USER_UPDATE
            case _:
                return None

    async def parseThemeMode(
        self,
        themeMode: str | None
    ) -> TwitchThemeMode | None:
        if not utils.isValidStr(themeMode):
            return None

        themeMode = themeMode.lower()

        match themeMode:
            case 'dark': return TwitchThemeMode.DARK
            case 'light': return TwitchThemeMode.LIGHT
            case _:
                self.__timber.log('TwitchJsonMapper', f'Encountered unknown TwitchThemeMode value: \"{themeMode}\"')
                return None

    async def parseTokensDetails(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchTokensDetails | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        expirationTime = await self.__calculateExpirationTime(
            expiresInSeconds = utils.getIntFromDict(jsonResponse, 'expires_in', fallback = -1)
        )

        if 'access_token' not in jsonResponse or not utils.isValidStr(jsonResponse.get('access_token', None)):
            self.__timber.log('TwitchJsonMapper', f'Tokens details JSON data does not include valid \"access_token\" value ({jsonResponse=})')
            return None

        accessToken = utils.getStrFromDict(jsonResponse, 'access_token')

        if 'refresh_token' not in jsonResponse or not utils.isValidStr(jsonResponse.get('refresh_token', None)):
            self.__timber.log('TwitchJsonMapper', f'Tokens details JSON data does not include valid \"refresh_token\" value ({jsonResponse=})')
            return None

        refreshToken = utils.getStrFromDict(jsonResponse, 'refresh_token')

        return TwitchTokensDetails(
            expirationTime = expirationTime,
            accessToken = accessToken,
            refreshToken = refreshToken
        )

    async def parseTransport(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchWebsocketTransport | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        connectedAt: datetime | None = None
        if 'connected_at' in jsonResponse and utils.isValidStr(jsonResponse.get('connected_at')):
            connectedAt = utils.getDateTimeFromDict(jsonResponse, 'connected_at')

        disconnectedAt: datetime | None = None
        if 'disconnected_at' in jsonResponse and utils.isValidStr(jsonResponse.get('disconnected_at')):
            disconnectedAt = utils.getDateTimeFromDict(jsonResponse, 'disconnected_at')

        callbackUrl: str | None = None
        if 'callback' in jsonResponse and utils.isValidUrl(jsonResponse.get('callback')):
            callbackUrl = utils.getStrFromDict(jsonResponse, 'callback')

        conduitId: str | None = None
        if 'conduit_id' in jsonResponse and utils.isValidStr(jsonResponse.get('conduit_id')):
            conduitId = utils.getStrFromDict(jsonResponse, 'conduit_id')

        secret: str | None = None
        if 'secret' in jsonResponse and utils.isValidStr(jsonResponse.get('secret')):
            secret = utils.getStrFromDict(jsonResponse, 'secret')

        sessionId: str | None = None
        if 'session_id' in jsonResponse and utils.isValidBool(jsonResponse.get('session_id')):
            sessionId = utils.getStrFromDict(jsonResponse, 'session_id')

        method = await self.requireTransportMethod(utils.getStrFromDict(jsonResponse, 'method'))

        return TwitchWebsocketTransport(
            connectedAt = connectedAt,
            disconnectedAt = disconnectedAt,
            callbackUrl = callbackUrl,
            conduitId = conduitId,
            secret = secret,
            sessionId = sessionId,
            method = method
        )

    async def parseTransportMethod(
        self,
        transportMethod: str | Any | None
    ) -> TwitchWebsocketTransportMethod | None:
        if not utils.isValidStr(transportMethod):
            return None

        transportMethod = transportMethod.lower()

        match transportMethod:
            case 'conduit': return TwitchWebsocketTransportMethod.CONDUIT
            case 'webhook': return TwitchWebsocketTransportMethod.WEBHOOK
            case 'websocket': return TwitchWebsocketTransportMethod.WEBSOCKET
            case _: return None

    async def parseUserSubscription(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchUserSubscription | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')
        if not isinstance(data, list) or len(data) == 0:
            return None

        dataEntry: dict[str, Any] | Any | None = data[0]
        if not isinstance(dataEntry, dict) or len(dataEntry) == 0:
            return None

        isGift = utils.getBoolFromDict(dataEntry, 'is_gift', fallback = False)
        broadcasterId = utils.getStrFromDict(dataEntry, 'broadcaster_id')
        broadcasterLogin = utils.getStrFromDict(dataEntry, 'broadcaster_login')
        broadcasterName = utils.getStrFromDict(dataEntry, 'broadcaster_name')

        gifterId: str | None = None
        if 'gifter_id' in dataEntry and utils.isValidStr(dataEntry.get('gifter_id')):
            gifterId = utils.getStrFromDict(dataEntry, 'gifter_id')

        gifterLogin: str | None = None
        if 'gifter_login' in dataEntry and utils.isValidStr(dataEntry.get('gifter_login')):
            gifterLogin = utils.getStrFromDict(dataEntry, 'gifter_login')

        gifterName: str | None = None
        if 'gifter_name' in dataEntry and utils.isValidStr(dataEntry.get('gifter_name')):
            gifterName = utils.getStrFromDict(dataEntry, 'gifter_name')

        tier = await self.requireSubscriberTier(utils.getStrFromDict(dataEntry, 'tier'))

        return TwitchUserSubscription(
            isGift = isGift,
            broadcasterId = broadcasterId,
            broadcasterLogin = broadcasterLogin,
            broadcasterName = broadcasterName,
            gifterId = gifterId,
            gifterLogin = gifterLogin,
            gifterName = gifterName,
            tier = tier
        )

    async def parseUserType(
        self,
        userType: str | Any | None
    ) -> TwitchUserType:
        if not utils.isValidStr(userType):
            return TwitchUserType.NORMAL

        userType = userType.lower()

        match userType:
            case 'admin': return TwitchUserType.ADMIN
            case 'global_mod': return TwitchUserType.GLOBAL_MOD
            case 'staff': return TwitchUserType.STAFF
            case _: return TwitchUserType.NORMAL

    async def parseValidationResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchValidationResponse | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        expiresInSeconds = utils.getIntFromDict(jsonResponse, 'expires_in')
        clientId = utils.getStrFromDict(jsonResponse, 'client_id')
        login = utils.getStrFromDict(jsonResponse, 'login')
        userId = utils.getStrFromDict(jsonResponse, 'user_id')

        now = datetime.now(self.__timeZoneRepository.getDefault())
        expiresAt = now + timedelta(seconds = expiresInSeconds)

        scopesArray: list[str] | None = jsonResponse.get('scopes')
        scopes: set[TwitchApiScope] = set()

        if isinstance(scopesArray, list) and len(scopesArray) >= 1:
            for index, scopeString in enumerate(scopesArray):
                scope = await self.parseApiScope(scopeString)

                if scope is None:
                    self.__timber.log('TwitchJsonMapper', f'Unable to parse value at index {index} for \"scopes\" data ({scopeString=}) ({jsonResponse=})')
                else:
                    scopes.add(scope)

        return TwitchValidationResponse(
            expiresAt = expiresAt,
            scopes = frozenset(scopes),
            expiresInSeconds = expiresInSeconds,
            clientId = clientId,
            login = login,
            userId = userId
        )

    async def parseWebsocketChannelPointsVoting(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchWebsocketChannelPointsVoting | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        isEnabled = utils.getBoolFromDict(jsonResponse, 'is_enabled')
        amountPerVote = utils.getIntFromDict(jsonResponse, 'amount_per_vote')

        return TwitchWebsocketChannelPointsVoting(
            isEnabled = isEnabled,
            amountPerVote = amountPerVote
        )

    async def parseWebsocketMessageType(
        self,
        messageType: str | Any | None
    ) -> TwitchWebsocketMessageType | None:
        if not utils.isValidStr(messageType):
            return None

        messageType = messageType.lower()

        match messageType:
            case 'session_keepalive': return TwitchWebsocketMessageType.KEEP_ALIVE
            case 'notification': return TwitchWebsocketMessageType.NOTIFICATION
            case 'session_reconnect': return TwitchWebsocketMessageType.RECONNECT
            case 'revocation': return TwitchWebsocketMessageType.REVOCATION
            case 'session_welcome': return TwitchWebsocketMessageType.WELCOME
            case _: return None

    async def parseWebsocketMetadata(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchWebsocketMetadata | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        messageTimestamp = utils.getDateTimeFromDict(jsonResponse, 'message_timestamp')
        messageId = utils.getStrFromDict(jsonResponse, 'message_id')

        subscriptionVersion: str | None = None
        if 'subscription_version' in jsonResponse and utils.isValidStr(jsonResponse.get('subscription_version')):
            subscriptionVersion = utils.getStrFromDict(jsonResponse, 'subscription_version')

        messageType = await self.requireWebsocketMessageType(utils.getStrFromDict(jsonResponse, 'message_type'))

        subscriptionType: TwitchWebsocketSubscriptionType | None = None
        if 'subscription_type' in jsonResponse and utils.isValidStr(jsonResponse.get('subscription_type')):
            subscriptionType = await self.parseSubscriptionType(utils.getStrFromDict(jsonResponse, 'subscription_type'))

        return TwitchWebsocketMetadata(
            messageTimestamp = messageTimestamp,
            messageId = messageId,
            subscriptionVersion = subscriptionVersion,
            messageType = messageType,
            subscriptionType = subscriptionType
        )

    async def parseWebsocketSub(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchWebsocketSub | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        isPrime = utils.getBoolFromDict(jsonResponse, 'is_prime', fallback = False)
        durationMonths = utils.getIntFromDict(jsonResponse, 'duration_months')
        subTier = await self.requireSubscriberTier(utils.getStrFromDict(jsonResponse, 'sub_tier'))

        return TwitchWebsocketSub(
            isPrime = isPrime,
            durationMonths = durationMonths,
            subTier = subTier
        )

    async def requireChatMessageFragmentType(
        self,
        fragmentType: str | Any | None
    ) -> TwitchChatMessageFragmentType:
        result = await self.parseChatMessageFragmentType(fragmentType)

        if result is None:
            raise ValueError(f'Unable to parse \"{fragmentType}\" into TwitchChatMessageFragmentType value!')

        return result

    async def requireCondition(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchWebsocketCondition:
        result = await self.parseCondition(jsonResponse)

        if result is None:
            raise ValueError(f'Unable to parse \"{jsonResponse}\" into TwitchWebsocketCondition value!')

        return result

    async def requireConnectionStatus(
        self,
        connectionStatus: str | Any | None
    ) -> TwitchWebsocketConnectionStatus:
        result = await self.parseConnectionStatus(connectionStatus)

        if result is None:
            raise ValueError(f'Unable to parse \"{connectionStatus}\" into TwitchWebsocketConnectionStatus value!')

        return result

    async def requireNoticeType(
        self,
        noticeType: str | Any | None
    ) -> TwitchNoticeType:
        result = await self.parseNoticeType(noticeType)

        if result is None:
            raise ValueError(f'Unable to parse \"{noticeType}\" into TwitchWebsocketNoticeType value!')

        return result

    async def requireOutcomeColor(
        self,
        outcomeColor: str | Any | None
    ) -> TwitchOutcomeColor:
        result = await self.parseOutcomeColor(outcomeColor)

        if result is None:
            raise ValueError(f'Unable to parse \"{outcomeColor}\" into TwitchOutcomeColor value!')

        return result

    async def requireSubscriberTier(
        self,
        subscriberTier: str | Any | None
    ) -> TwitchSubscriberTier:
        result = await self.parseSubscriberTier(subscriberTier)

        if result is None:
            raise ValueError(f'Unable to parse \"{subscriberTier}\" into TwitchSubscriberTier value!')

        return result

    async def requireSubscriptionType(
        self,
        subscriptionType: str | Any | None
    ) -> TwitchWebsocketSubscriptionType:
        result = await self.parseSubscriptionType(subscriptionType)

        if result is None:
            raise ValueError(f'Unable to parse \"{subscriptionType}\" into TwitchWebsocketSubscriptionType value!')

        return result

    async def requireTransport(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchWebsocketTransport:
        result = await self.parseTransport(jsonResponse)

        if result is None:
            raise ValueError(f'Unable to parse \"{jsonResponse}\" into TwitchWebsocketTransport value!')

        return result

    async def requireTransportMethod(
        self,
        transportMethod: str | Any | None
    ) -> TwitchWebsocketTransportMethod:
        result = await self.parseTransportMethod(transportMethod)

        if result is None:
            raise ValueError(f'Unable to parse \"{transportMethod}\" into TwitchWebsocketTransportMethod value!')

        return result

    async def requireWebsocketMessageType(
        self,
        messageType: str | Any | None
    ) -> TwitchWebsocketMessageType:
        result = await self.parseWebsocketMessageType(messageType)

        if result is None:
            raise ValueError(f'Unable to parse \"{messageType}\" into TwitchWebsocketMessageType value!')

        return result

    async def serializeBanRequest(
        self,
        banRequest: TwitchBanRequest
    ) -> dict[str, Any]:
        if not isinstance(banRequest, TwitchBanRequest):
            raise TypeError(f'banRequest argument is malformed: \"{banRequest}\"')

        data: dict[str, Any] = {
            'user_id': banRequest.userIdToBan
        }

        if utils.isValidInt(banRequest.duration):
            data['duration'] = banRequest.duration

        if utils.isValidStr(banRequest.reason):
            data['reason'] = banRequest.reason

        return {
            'data': data
        }

    async def serializeChatAnnouncementColor(
        self,
        announcementColor: TwitchChatAnnouncementColor
    ) -> str:
        if not isinstance(announcementColor, TwitchChatAnnouncementColor):
            raise TypeError(f'announcementColor argument is malformed: \"{announcementColor}\"')

        match announcementColor:
            case TwitchChatAnnouncementColor.BLUE: return 'blue'
            case TwitchChatAnnouncementColor.GREEN: return 'green'
            case TwitchChatAnnouncementColor.ORANGE: return 'orange'
            case TwitchChatAnnouncementColor.PRIMARY: return 'primary'
            case TwitchChatAnnouncementColor.PURPLE: return 'purple'
            case _: raise ValueError(f'Unknown TwitchChatAnnouncementColor value: \"{announcementColor}\"')

    async def serializeCondition(
        self,
        condition: TwitchWebsocketCondition
    ) -> dict[str, Any]:
        if not isinstance(condition, TwitchWebsocketCondition):
            raise TypeError(f'condition argument is malformed: \"{condition}\"')

        dictionary: dict[str, Any] = dict()

        if utils.isValidStr(condition.broadcasterUserId):
            dictionary['broadcaster_user_id'] = condition.broadcasterUserId

        if utils.isValidStr(condition.clientId):
            dictionary['client_id'] = condition.clientId

        if utils.isValidStr(condition.fromBroadcasterUserId):
            dictionary['from_broadcaster_user_id'] = condition.fromBroadcasterUserId

        if utils.isValidStr(condition.moderatorUserId):
            dictionary['moderator_user_id'] = condition.moderatorUserId

        if utils.isValidStr(condition.rewardId):
            dictionary['reward_id'] = condition.rewardId

        if utils.isValidStr(condition.toBroadcasterUserId):
            dictionary['to_broadcaster_user_id'] = condition.toBroadcasterUserId

        if utils.isValidStr(condition.userId):
            dictionary['user_id'] = condition.userId

        return dictionary

    async def serializeConduitRequest(
        self,
        conduitRequest: TwitchConduitRequest
    ) -> dict[str, Any]:
        if not isinstance(conduitRequest, TwitchConduitRequest):
            raise TypeError(f'conduitRequest argument is malformed: \"{conduitRequest}\"')

        return {
            'shard_count': conduitRequest.shardCount,
        }

    async def serializeEventSubRequest(
        self,
        eventSubRequest: TwitchEventSubRequest
    ) -> dict[str, Any]:
        if not isinstance(eventSubRequest, TwitchEventSubRequest):
            raise TypeError(f'eventSubRequest argument is malformed: \"{eventSubRequest}\"')

        condition = await self.serializeCondition(eventSubRequest.condition)
        transport = await self.serializeTransport(eventSubRequest.transport)
        eventSubType = await self.serializeSubscriptionType(eventSubRequest.subscriptionType)
        version = eventSubRequest.subscriptionType.version

        return {
            'condition': condition,
            'transport': transport,
            'type': eventSubType,
            'version': version,
        }

    async def serializeSendChatAnnouncementRequest(
        self,
        announcementRequest: TwitchSendChatAnnouncementRequest
    ) -> dict[str, Any]:
        if not isinstance(announcementRequest, TwitchSendChatAnnouncementRequest):
            raise TypeError(f'announcementRequest argument is malformed: \"{announcementRequest}\"')

        dictionary: dict[str, Any] = {
            'message': announcementRequest.message
        }

        if announcementRequest.color is not None:
            color = await self.serializeChatAnnouncementColor(announcementRequest.color)
            dictionary['color'] = color

        return dictionary

    async def serializeSendChatMessageRequest(
        self,
        chatRequest: TwitchSendChatMessageRequest
    ) -> dict[str, Any]:
        if not isinstance(chatRequest, TwitchSendChatMessageRequest):
            raise TypeError(f'chatRequest argument is malformed: \"{chatRequest}\"')

        dictionary: dict[str, Any] = {
            'broadcaster_id': chatRequest.broadcasterId,
            'message': chatRequest.message,
            'sender_id': chatRequest.senderId
        }

        if utils.isValidStr(chatRequest.replyParentMessageId):
            dictionary['reply_parent_message_id'] = chatRequest.replyParentMessageId

        return dictionary

    async def serializeSubscriptionType(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType
    ) -> str:
        if not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

        match subscriptionType:
            case TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE:
                return 'channel.chat.message'
            case TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION:
                return 'channel.channel_points_custom_reward_redemption.add'
            case TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN:
                return 'channel.poll.begin'
            case TwitchWebsocketSubscriptionType.CHANNEL_POLL_END:
                return 'channel.poll.end'
            case TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS:
                return 'channel.poll.progress'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
                return 'channel.prediction.begin'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END:
                return 'channel.prediction.end'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK:
                return 'channel.prediction.lock'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS:
                return 'channel.prediction.progress'
            case TwitchWebsocketSubscriptionType.CHANNEL_UPDATE:
                return 'channel.update'
            case TwitchWebsocketSubscriptionType.CHEER:
                return 'channel.cheer'
            case TwitchWebsocketSubscriptionType.FOLLOW:
                return 'channel.follow'
            case TwitchWebsocketSubscriptionType.RAID:
                return 'channel.raid'
            case TwitchWebsocketSubscriptionType.STREAM_OFFLINE:
                return 'stream.offline'
            case TwitchWebsocketSubscriptionType.STREAM_ONLINE:
                return 'stream.online'
            case TwitchWebsocketSubscriptionType.SUBSCRIBE:
                return 'channel.subscribe'
            case TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT:
                return 'channel.subscription.gift'
            case TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE:
                return 'channel.subscription.message'
            case TwitchWebsocketSubscriptionType.USER_UPDATE:
                return 'user.update'
            case _:
                raise RuntimeError(f'unknown TwitchWebsocketSubscriptionType: \"{self}\"')

    async def serializeTransport(
        self,
        transport: TwitchWebsocketTransport
    ) -> dict[str, Any]:
        if not isinstance(transport, TwitchWebsocketTransport):
            raise TypeError(f'transport argument is malformed: \"{transport}\"')

        dictionary: dict[str, Any] = {
            'method': await self.serializeTransportMethod(transport.method)
        }

        match transport.method:
            case TwitchWebsocketTransportMethod.CONDUIT:
                dictionary['conduit_id'] = transport.requireConduitId()

            case TwitchWebsocketTransportMethod.WEBHOOK:
                dictionary['callback'] = transport.requireCallbackUrl()
                dictionary['secret'] = transport.requireSecret()

            case TwitchWebsocketTransportMethod.WEBSOCKET:
                dictionary['session_id'] = transport.requireSessionId()

            case _:
                raise ValueError(f'Unknown TwitchWebsocketTransportMethod value: \"{transport}\"')

        return dictionary

    async def serializeTransportMethod(
        self,
        transportMethod: TwitchWebsocketTransportMethod
    ) -> str:
        if not isinstance(transportMethod, TwitchWebsocketTransportMethod):
            raise TypeError(f'transportMethod argument is malformed: \"{transportMethod}\"')

        match transportMethod:
            case TwitchWebsocketTransportMethod.CONDUIT: return 'conduit'
            case TwitchWebsocketTransportMethod.WEBHOOK: return 'webhook'
            case TwitchWebsocketTransportMethod.WEBSOCKET: return 'websocket'
            case _: raise ValueError(f'Unknown TwitchWebsocketTransportMethod value: \"{transportMethod}\"')
