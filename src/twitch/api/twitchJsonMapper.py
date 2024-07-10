from datetime import datetime, timedelta
from typing import Any

from .twitchApiScope import TwitchApiScope
from .twitchBanRequest import TwitchBanRequest
from .twitchBroadcasterType import TwitchBroadcasterType
from .twitchEmoteDetails import TwitchEmoteDetails
from .twitchEmoteImageFormat import TwitchEmoteImageFormat
from .twitchEmoteImageScale import TwitchEmoteImageScale
from .twitchEmoteType import TwitchEmoteType
from .twitchEmotesResponse import TwitchEmotesResponse
from .twitchJsonMapperInterface import TwitchJsonMapperInterface
from .twitchSendChatDropReason import TwitchSendChatDropReason
from .twitchSendChatMessageResponse import TwitchSendChatMessageResponse
from .twitchStreamType import TwitchStreamType
from .twitchSubscriberTier import TwitchSubscriberTier
from .twitchThemeMode import TwitchThemeMode
from .twitchTokensDetails import TwitchTokensDetails
from .twitchValidationResponse import TwitchValidationResponse
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


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
            case 'channel:read:polls': return TwitchApiScope.CHANNEL_READ_POLLS
            case 'channel:read:predictions': return TwitchApiScope.CHANNEL_READ_PREDICTIONS
            case 'channel:read:redemptions': return TwitchApiScope.CHANNEL_READ_REDEMPTIONS
            case 'channel:read:subscriptions': return TwitchApiScope.CHANNEL_READ_SUBSCRIPTIONS
            case 'channel_editor': return TwitchApiScope.CHANNEL_EDITOR
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
            case 'whispers:edit': return TwitchApiScope.WHISPERS_EDIT
            case 'whispers:read': return TwitchApiScope.WHISPERS_READ
            case _:
                self.__timber.log('TwitchJsonMapper', f'Encountered unknown TwitchApiScope value: \"{apiScope}\"')
                return None

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
                format = await self.parseEmoteImageFormat(formatString)

                if format is None:
                    self.__timber.log('TwitchJsonMapper', f'Unable to parse value at index {index} for \"format\" data ({jsonResponse=})')
                else:
                    formats.add(format)

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

        tier = await self.parseSubscriberTier(jsonResponse.get('tier'))
        if tier is None:
            self.__timber.log('TwitchJsonMapper', f'Unable to parse value for \"tier\" data ({jsonResponse=})')
            return None

        return TwitchEmoteDetails(
            images = images,
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

        emoteData: list[TwitchEmoteDetails] = list()
        for index, emoteDetailsJson in enumerate(data):
            emoteDetails = await self.parseEmoteDetails(emoteDetailsJson)

            if emoteDetails is None:
                self.__timber.log('TwitchJsonMapper', f'Unable to parse value at index {index} for \"data\" data ({emoteDetailsJson=}) ({jsonResponse=})')
            else:
                emoteData.append(emoteDetails)

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
            case _:
                self.__timber.log('TwitchJsonMapper', f'Encountered unknown TwitchEmoteType value: \"{emoteType}\"')
                return None

    async def parseSendChatDropReason(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchSendChatDropReason | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        code = utils.getStrFromDict(jsonResponse, 'code')

        message: str | None
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

    async def parseStreamStype(
        self,
        streamType: str | None
    ) -> TwitchStreamType | None:
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

        if not 'access_token' in jsonResponse or not utils.isValidStr(jsonResponse.get('access_token')):
            self.__timber.log('TwitchJsonMapper', f'Tokens details JSON data does not include valid \"access_token\" value ({jsonResponse=})')
            return None

        accessToken = utils.getStrFromDict(jsonResponse, 'access_token')

        if not 'refresh_token' in jsonResponse or not utils.isValidStr(jsonResponse.get('refresh_token')):
            self.__timber.log('TwitchJsonMapper', f'Tokens details JSON data does not include valid \"refresh_token\" value ({jsonResponse=})')
            return None

        refreshToken = utils.getStrFromDict(jsonResponse, 'refresh_token')

        return TwitchTokensDetails(
            expirationTime = expirationTime,
            accessToken = accessToken,
            refreshToken = refreshToken
        )

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

    async def requireBroadcasterType(
        self,
        broadcasterType: str | None
    ) -> TwitchBroadcasterType:
        result = await self.parseBroadcasterType(broadcasterType)

        if result is None:
            raise ValueError(f'Unable to parse \"{broadcasterType}\" into TwitchBroadcasterType value!')

        return result

    async def requireSubscriberTier(
        self,
        subscriberTier: str | None
    ) -> TwitchSubscriberTier:
        result = await self.parseSubscriberTier(subscriberTier)

        if result is None:
            raise ValueError(f'Unable to parse \"{subscriberTier}\" into TwitchSubscriberTier value!')

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
