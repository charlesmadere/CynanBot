from datetime import datetime, timedelta
from typing import Any

from frozendict import frozendict
from frozenlist import FrozenList

from .twitchJsonMapperInterface import TwitchJsonMapperInterface
from ..models.twitchApiScope import TwitchApiScope
from ..models.twitchBanRequest import TwitchBanRequest
from ..models.twitchBannedUser import TwitchBannedUser
from ..models.twitchBannedUserResponse import TwitchBannedUserResponse
from ..models.twitchBroadcasterSubscriptionResponse import TwitchBroadcasterSubscriptionResponse
from ..models.twitchBroadcasterSusbcription import TwitchBroadcasterSubscription
from ..models.twitchBroadcasterType import TwitchBroadcasterType
from ..models.twitchChannelEditor import TwitchChannelEditor
from ..models.twitchChannelEditorsResponse import TwitchChannelEditorsResponse
from ..models.twitchChatAnnouncementColor import TwitchChatAnnouncementColor
from ..models.twitchChatter import TwitchChatter
from ..models.twitchChattersResponse import TwitchChattersResponse
from ..models.twitchCheerMetadata import TwitchCheerMetadata
from ..models.twitchEmoteDetails import TwitchEmoteDetails
from ..models.twitchEmoteImageFormat import TwitchEmoteImageFormat
from ..models.twitchEmoteImageScale import TwitchEmoteImageScale
from ..models.twitchEmoteType import TwitchEmoteType
from ..models.twitchEmotesResponse import TwitchEmotesResponse
from ..models.twitchEventSubRequest import TwitchEventSubRequest
from ..models.twitchOutcomeColor import TwitchOutcomeColor
from ..models.twitchPaginationResponse import TwitchPaginationResponse
from ..models.twitchPollStatus import TwitchPollStatus
from ..models.twitchPredictionStatus import TwitchPredictionStatus
from ..models.twitchReward import TwitchReward
from ..models.twitchRewardRedemptionStatus import TwitchRewardRedemptionStatus
from ..models.twitchSendChatAnnouncementRequest import TwitchSendChatAnnouncementRequest
from ..models.twitchSendChatDropReason import TwitchSendChatDropReason
from ..models.twitchSendChatMessageRequest import TwitchSendChatMessageRequest
from ..models.twitchSendChatMessageResponse import TwitchSendChatMessageResponse
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
from ..models.twitchWebsocketNoticeType import TwitchWebsocketNoticeType
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

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

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
            case 'channel:manage:moderators': return TwitchApiScope.CHANNEL_MANAGE_MODERATORS
            case 'channel:manage:polls': return TwitchApiScope.CHANNEL_MANAGE_POLLS
            case 'channel:manage:predictions': return TwitchApiScope.CHANNEL_MANAGE_PREDICTIONS
            case 'channel:manage:redemptions': return TwitchApiScope.CHANNEL_MANAGE_REDEMPTIONS
            case 'channel:moderate': return TwitchApiScope.CHANNEL_MODERATE
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
            case 'moderator:manage:banned_users': return TwitchApiScope.MODERATOR_MANAGE_BANNED_USERS
            case 'moderator:manage:chat_messages': return TwitchApiScope.MODERATOR_MANAGE_CHAT_MESSAGES
            case 'moderator:read:chatters': return TwitchApiScope.MODERATOR_READ_CHATTERS
            case 'moderator:read:chat_settings': return TwitchApiScope.MODERATOR_READ_CHAT_SETTINGS
            case 'moderator:read:followers': return TwitchApiScope.MODERATOR_READ_FOLLOWERS
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

        isGift = utils.getBoolFromDict(jsonResponse, 'is_gift')

        broadcasterId = utils.getStrFromDict(jsonResponse, 'broadcaster_id')
        broadcasterLogin = utils.getStrFromDict(jsonResponse, 'broadcaster_login')
        broadcasterName = utils.getStrFromDict(jsonResponse, 'broadcaster_name')

        gifterId: str | None = None
        if 'gifter_id' in jsonResponse and utils.isValidStr(jsonResponse.get('gifter_id')):
            gifterId = utils.getStrFromDict(jsonResponse, 'gifter_id')

        gifterLogin: str | None = None
        if 'gifter_login' in jsonResponse and utils.isValidStr(jsonResponse.get('gifter_login')):
            gifterLogin = utils.getStrFromDict(jsonResponse, 'gifter_login')

        gifterName: str | None = None
        if 'gifter_name' in jsonResponse and utils.isValidStr(jsonResponse.get('gifter_name')):
            gifterName = utils.getStrFromDict(jsonResponse, 'gifter_name')

        planName: str | None = None
        if 'plan_name' in jsonResponse and utils.isValidStr(jsonResponse.get('plan_name')):
            planName = utils.getStrFromDict(jsonResponse, 'plan_name')

        userId = utils.getStrFromDict(jsonResponse, 'user_id')
        userLogin = utils.getStrFromDict(jsonResponse, 'user_login')
        userName = utils.getStrFromDict(jsonResponse, 'user_name')

        tier = await self.requireSubscriberTier(utils.getStrFromDict(jsonResponse, 'tier'))

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
        broadcasterType: str | None
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

        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')
        if not isinstance(data, list) or len(data) == 0:
            return None

        channelEditors: list[TwitchChannelEditor] = list()

        for channelEditorJson in data:
            channelEditor = await self.parseChannelEditor(channelEditorJson)
            channelEditors.append(channelEditor)

        channelEditors.sort(key = lambda editor: editor.createdAt)
        frozenChannelEditors: FrozenList[TwitchChannelEditor] = FrozenList(channelEditors)
        frozenChannelEditors.freeze()

        return TwitchChannelEditorsResponse(
            editors = frozenChannelEditors
        )

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

        bits = utils.getIntFromDict(jsonResponse, 'bits')

        return TwitchCheerMetadata(
            bits = bits
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
        emoteImageFormat: str | None
    ) -> TwitchEmoteImageFormat | None:
        if not utils.isValidStr(emoteImageFormat):
            return None

        emoteImageFormat = emoteImageFormat.lower()

        match emoteImageFormat:
            case 'animated': return TwitchEmoteImageFormat.ANIMATED
            case 'static': return TwitchEmoteImageFormat.STATIC
            case _:
                self.__timber.log('TwitchJsonMapper', f'Encountered unknown TwitchEmoteImageFormat value: \"{emoteImageFormat}\"')
                return None

    async def parseEmoteImageScale(
        self,
        emoteImageScale: str | None
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
            case _:
                self.__timber.log('TwitchJsonMapper', f'Encountered unknown TwitchEmoteImageScale value: \"{emoteImageScale}\"')
                return None

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

    async def parseNoticeType(
        self,
        noticeType: str | Any | None
    ) -> TwitchWebsocketNoticeType | None:
        if not utils.isValidStr(noticeType):
            return None

        noticeType = noticeType.lower()

        match noticeType:
            case 'announcement': return TwitchWebsocketNoticeType.ANNOUNCEMENT
            case 'bits_badge_tier': return TwitchWebsocketNoticeType.BITS_BADGE_TIER
            case 'charity_donation': return TwitchWebsocketNoticeType.CHARITY_DONATION
            case 'community_sub_gift': return TwitchWebsocketNoticeType.COMMUNITY_SUB_GIFT
            case 'gift_paid_upgrade':  return TwitchWebsocketNoticeType.GIFT_PAID_UPGRADE
            case 'pay_it_forward': return TwitchWebsocketNoticeType.PAY_IT_FORWARD
            case 'prime_paid_upgrade': return TwitchWebsocketNoticeType.PRIME_PAID_UPGRADE
            case 'raid': return TwitchWebsocketNoticeType.RAID
            case 'resub': return TwitchWebsocketNoticeType.RE_SUB
            case 'sub': return TwitchWebsocketNoticeType.SUB
            case 'sub_gift': return TwitchWebsocketNoticeType.SUB_GIFT
            case 'unraid': return TwitchWebsocketNoticeType.UN_RAID
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
        subscriberTier: str | None
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
            case 'channel.chat.message':
                return TwitchWebsocketSubscriptionType.CHAT_MESSAGE
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
    ) -> TwitchWebsocketNoticeType:
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
        subscriberTier: str | None
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

    async def serializeEventSubRequest(
        self,
        eventSubRequest: TwitchEventSubRequest
    ) -> dict[str, Any]:
        if not isinstance(eventSubRequest, TwitchEventSubRequest):
            raise TypeError(f'eventSubRequest argument is malformed: \"{eventSubRequest}\"')

        condition = await self.serializeCondition(eventSubRequest.condition)
        eventSubType = await self.serializeSubscriptionType(eventSubRequest.subscriptionType)
        transport = await self.serializeTransport(eventSubRequest.transport)

        return {
            'condition': condition,
            'transport': transport,
            'type': eventSubType,
            'version': eventSubRequest.subscriptionType.version
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
            case TwitchWebsocketSubscriptionType.CHAT_MESSAGE:
                return 'channel.chat.message'
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
            'method': transport.method.toStr()
        }

        if utils.isValidStr(transport.sessionId):
            dictionary['session_id'] = transport.sessionId

        return dictionary

    async def requireWebsocketMessageType(
        self,
        messageType: str | Any | None
    ) -> TwitchWebsocketMessageType:
        result = await self.parseWebsocketMessageType(messageType)

        if result is None:
            raise ValueError(f'Unable to parse \"{messageType}\" into TwitchWebsocketMessageType value!')

        return result
