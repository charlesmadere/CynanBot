import traceback
import urllib.parse
from datetime import datetime, timedelta
from typing import Any, Final

from frozenlist import FrozenList

from .jsonMapper.twitchJsonMapperInterface import TwitchJsonMapperInterface
from .models.twitchBanRequest import TwitchBanRequest
from .models.twitchBanResponse import TwitchBanResponse
from .models.twitchBanResponseEntry import TwitchBanResponseEntry
from .models.twitchBannedUsersReponse import TwitchBannedUsersResponse
from .models.twitchBroadcasterSubscriptionsResponse import TwitchBroadcasterSubscriptionsResponse
from .models.twitchChannelEditorsResponse import TwitchChannelEditorsResponse
from .models.twitchChattersRequest import TwitchChattersRequest
from .models.twitchChattersResponse import TwitchChattersResponse
from .models.twitchEmotesResponse import TwitchEmotesResponse
from .models.twitchEventSubRequest import TwitchEventSubRequest
from .models.twitchEventSubResponse import TwitchEventSubResponse
from .models.twitchFetchStreamsRequest import TwitchFetchStreamsRequest
from .models.twitchFetchStreamsWithIdsRequest import TwitchFetchStreamsWithIdsRequest
from .models.twitchFetchStreamsWithLoginsRequest import TwitchFetchStreamsWithLoginsRequest
from .models.twitchFetchUserRequest import TwitchFetchUserRequest
from .models.twitchFetchUserWithIdRequest import TwitchFetchUserWithIdRequest
from .models.twitchFetchUserWithLoginRequest import TwitchFetchUserWithLoginRequest
from .models.twitchFollowersResponse import TwitchFollowersResponse
from .models.twitchLiveUserDetails import TwitchLiveUserDetails
from .models.twitchModeratorsResponse import TwitchModeratorsResponse
from .models.twitchPaginationResponse import TwitchPaginationResponse
from .models.twitchSendChatAnnouncementRequest import TwitchSendChatAnnouncementRequest
from .models.twitchSendChatMessageRequest import TwitchSendChatMessageRequest
from .models.twitchSendChatMessageResponse import TwitchSendChatMessageResponse
from .models.twitchStartCommercialResponse import TwitchStartCommercialResponse
from .models.twitchStreamsResponse import TwitchStreamsResponse
from .models.twitchTokensDetails import TwitchTokensDetails
from .models.twitchUnbanRequest import TwitchUnbanRequest
from .models.twitchUserSubscriptionsResponse import TwitchUserSubscriptionsResponse
from .models.twitchUsersResponse import TwitchUsersResponse
from .models.twitchValidationResponse import TwitchValidationResponse
from .twitchApiServiceInterface import TwitchApiServiceInterface
from ..exceptions import (TwitchErrorException, TwitchJsonException,
                          TwitchPasswordChangedException, TwitchStatusCodeException,
                          TwitchTokenIsExpiredException)
from ..twitchCredentialsProviderInterface import TwitchCredentialsProviderInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class TwitchApiService(TwitchApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchCredentialsProvider: TwitchCredentialsProviderInterface,
        twitchJsonMapper: TwitchJsonMapperInterface,
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchCredentialsProvider, TwitchCredentialsProviderInterface):
            raise TypeError(f'twitchCredentialsProvider argument is malformed: \"{twitchCredentialsProvider}\"')
        elif not isinstance(twitchJsonMapper, TwitchJsonMapperInterface):
            raise TypeError(f'twitchJsonMapper argument is malformed: \"{twitchJsonMapper}\"')

        self.__networkClientProvider: Final[NetworkClientProvider] = networkClientProvider
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchCredentialsProvider: Final[TwitchCredentialsProviderInterface] = twitchCredentialsProvider
        self.__twitchJsonMapper: Final[TwitchJsonMapperInterface] = twitchJsonMapper

    async def addModerator(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str,
    ) -> bool:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TwitchApiService', f'Adding moderator... ({broadcasterId=}) ({userId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'broadcaster_id': broadcasterId,
            'user_id': userId,
        })

        try:
            response = await clientSession.post(
                url = f'https://api.twitch.tv/helix/moderation/moderators?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when adding moderator ({broadcasterId=}) ({userId=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when adding moderator ({broadcasterId=}) ({userId=}): {e}')

        responseStatusCode = response.statusCode
        await response.close()

        if responseStatusCode == 204:
            return True
        else:
            self.__timber.log('TwitchApiService', f'Encountered non-204 HTTP status code when adding moderator ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=})')
            return False

    async def banUser(
        self,
        twitchAccessToken: str,
        banRequest: TwitchBanRequest,
    ) -> TwitchBanResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(banRequest, TwitchBanRequest):
            raise TypeError(f'banRequest argument is malformed: \"{banRequest}\"')

        self.__timber.log('TwitchApiService', f'Banning user... ({banRequest=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'broadcaster_id': banRequest.broadcasterUserId,
            'moderator_id': banRequest.moderatorUserId,
        })

        try:
            response = await clientSession.post(
                url = f'https://api.twitch.tv/helix/moderation/bans?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                    'Content-Type': 'application/json',
                },
                json = await self.__twitchJsonMapper.serializeBanRequest(banRequest),
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when banning user ({banRequest=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when banning user ({banRequest=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode == 500 and utils.isValidInt(banRequest.duration):
            # DUMB EDGE CASE ALERT
            # Sometimes Twitch seems to successfully time a user out, but still fails in some
            # way internally. So the user becomes timed out, we just unfortunately don't receive
            # a proper API response of this actually happening, and instead just receive notice
            # that the server internally ran into an issue (error code 500). So let's make an
            # assumption that whenever we are notified of error 500, that the timeout did
            # actually successfully complete.
            # DUMB EDGE CASE ALERT

            self.__timber.log('TwitchApiService', f'Encountered 500 HTTP status code when timing out user; assuming a timeout successfully happened in order to recover ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')

            # Make up this timeout's createdAt and endTime. These are just educated guesses
            # and are probably off by a few seconds.
            createdAt = datetime.now(self.__timeZoneRepository.getDefault()) - timedelta(seconds = 3)
            endTime = createdAt + timedelta(seconds = banRequest.duration)

            frozenEntries: FrozenList[TwitchBanResponseEntry] = FrozenList()
            frozenEntries.append(TwitchBanResponseEntry(
                createdAt = createdAt,
                endTime = endTime,
                broadcasterId = banRequest.broadcasterUserId,
                moderatorId = banRequest.moderatorUserId,
                userId = banRequest.userIdToBan,
            ))

            frozenEntries.freeze()

            return TwitchBanResponse(
                data = frozenEntries,
            )
        elif responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when banning user ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when banning user ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})',
            )

        banResponse = await self.__twitchJsonMapper.parseBanResponse(jsonResponse)

        if banResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when banning user ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({banResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when banning user ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({banResponse=})')

        return banResponse

    async def checkUserSubscription(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str,
    ) -> TwitchUserSubscriptionsResponse:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TwitchApiService', f'Checking user subscription... ({broadcasterId=}) ({userId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'broadcaster_id': broadcasterId,
            'user_id': userId,
        })

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/subscriptions/user?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when checking user subscription ({broadcasterId=}) ({userId=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when checking user subscription ({broadcasterId=}) ({userId=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when checking user subscription ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when checking user subscription ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})',
            )

        userSubscriptionsResponse = await self.__twitchJsonMapper.parseUserSubscriptionsResponse(jsonResponse)

        if userSubscriptionsResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when checking user subscription ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when checking user subscription ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')

        return userSubscriptionsResponse

    async def createEventSubSubscription(
        self,
        twitchAccessToken: str,
        eventSubRequest: TwitchEventSubRequest,
    ) -> TwitchEventSubResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(eventSubRequest, TwitchEventSubRequest):
            raise TypeError(f'eventSubRequest argument is malformed: \"{eventSubRequest}\"')

        self.__timber.log('TwitchApiService', f'Creating EventSub subscription... ({eventSubRequest=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = 'https://api.twitch.tv/helix/eventsub/subscriptions',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                    'Content-Type': 'application/json',
                },
                json = await self.__twitchJsonMapper.serializeEventSubRequest(eventSubRequest),
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when creating EventSub subscription ({eventSubRequest=}))', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when creating EventSub subscription ({eventSubRequest=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 202:
            self.__timber.log('TwitchApiService', f'Encountered non-202 HTTP status code ({responseStatusCode}) when creating EventSub subscription ({eventSubRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-202 HTTP status code ({responseStatusCode}) when creating EventSub subscription ({eventSubRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})',
            )

        eventSubResponse = await self.__twitchJsonMapper.parseEventSubResponse(jsonResponse)

        if eventSubResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when creating EventSub subscription ({eventSubRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({eventSubResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when creating EventSub subscription ({eventSubRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({eventSubResponse=})')

        return eventSubResponse

    async def fetchBannedUsers(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str,
    ) -> TwitchBannedUsersResponse:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TwitchApiService', f'Fetching banned user... ({broadcasterId=}) ({userId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'broadcaster_id': broadcasterId,
            'user_id': userId,
        })

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/moderation/banned?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching banned user ({broadcasterId=}) ({userId=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching banned user ({broadcasterId=}) ({userId=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching banned user ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching banned user ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})',
            )

        bannedUsersResponse = await self.__twitchJsonMapper.parseBannedUsersResponse(jsonResponse)

        if bannedUsersResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching banned user ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({bannedUsersResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching banned user ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({bannedUsersResponse=})')

        return bannedUsersResponse

    async def fetchBroadcasterSubscriptions(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str,
    ) -> TwitchBroadcasterSubscriptionsResponse:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TwitchApiService', f'Fetching broadcaster subscriptions... ({broadcasterId=}) ({userId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'broadcaster_id': broadcasterId,
            'user_id': userId,
        })

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/subscriptions?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching broadcaster subscriptions ({broadcasterId=}) ({userId=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching broadcaster subscriptions ({broadcasterId=}) ({userId=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching broadcaster subscriptions ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching broadcaster subscriptions ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})',
            )

        broadcasterSubscriptionsResponse = await self.__twitchJsonMapper.parseBroadcasterSubscriptionsResponse(jsonResponse)

        if broadcasterSubscriptionsResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching broadcaster subscriptions ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching broadcaster subscriptions ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')

        return broadcasterSubscriptionsResponse

    async def fetchChannelEditors(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
    ) -> TwitchChannelEditorsResponse:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        self.__timber.log('TwitchApiService', f'Fetching channel editors... ({broadcasterId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'broadcaster_id': broadcasterId,
        })

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/channels/editors?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching channel editors ({broadcasterId=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching channel editors ({broadcasterId=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching channel editors ({broadcasterId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching channel editors ({broadcasterId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})',
            )

        channelEditorsResponse = await self.__twitchJsonMapper.parseChannelEditorsResponse(jsonResponse)

        if channelEditorsResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching channel editors ({broadcasterId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({channelEditorsResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching channel editors ({broadcasterId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({channelEditorsResponse=})')

        return channelEditorsResponse

    async def fetchChatters(
        self,
        twitchAccessToken: str,
        chattersRequest: TwitchChattersRequest,
    ) -> TwitchChattersResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(chattersRequest, TwitchChattersRequest):
            raise TypeError(f'chattersRequest argument is malformed: \"{chattersRequest}\"')

        first = chattersRequest.first

        if first is None or first < 1 or first > 1000:
            first = 100

        self.__timber.log('TwitchApiService', f'Fetching chatters... ({chattersRequest=}) ({first=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'broadcaster_id': chattersRequest.broadcasterId,
            'first': first,
            'moderator_id': chattersRequest.moderatorId,
        })

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/chat/chatters?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching chatters ({chattersRequest=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching chatters ({chattersRequest=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching chatters ({chattersRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching chatters ({chattersRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})',
            )

        chattersResponse = await self.__twitchJsonMapper.parseChattersResponse(jsonResponse)

        if chattersResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching chatters ({chattersRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({chattersResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching chatters ({chattersRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({chattersResponse=})')

        return chattersResponse

    async def fetchChannelEmotes(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
    ) -> TwitchEmotesResponse:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        self.__timber.log('TwitchApiService', f'Fetching emotes... ({broadcasterId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'broadcaster_id': broadcasterId,
        })

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/chat/emotes?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching emotes ({broadcasterId=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching emotes ({broadcasterId=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching emotes ({broadcasterId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching emotes ({broadcasterId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse})',
            )

        emotesResponse = await self.__twitchJsonMapper.parseEmotesResponse(jsonResponse)

        if emotesResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching emotes ({broadcasterId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({emotesResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching emotes ({broadcasterId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({emotesResponse=})')

        return emotesResponse

    async def fetchEventSubSubscriptions(
        self,
        twitchAccessToken: str,
        userId: str,
    ) -> TwitchEventSubResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TwitchApiService', f'Fetching EventSub subscriptions... ({userId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        isFirstRun = True
        pagination: TwitchPaginationResponse | None = None
        finalEventSubResponse: TwitchEventSubResponse | None = None

        while isFirstRun or pagination is not None:
            if isFirstRun:
                isFirstRun = False

            queryString = f'user_id={userId}'

            if pagination is not None:
                queryString = f'{queryString}&after={pagination.cursor}'

            try:
                response = await clientSession.get(
                    url = f'https://api.twitch.tv/helix/eventsub/subscriptions?{queryString}',
                    headers = {
                        'Authorization': f'Bearer {twitchAccessToken}',
                        'Client-Id': twitchClientId,
                    },
                )
            except GenericNetworkException as e:
                self.__timber.log('TwitchApiService', f'Encountered network error when fetching EventSub subscriptions ({userId=}) ({pagination=})', e, traceback.format_exc())
                raise GenericNetworkException(f'TwitchApiService encountered network error when fetching EventSub subscriptions ({userId=}) ({pagination=}): {e}')

            responseStatusCode = response.statusCode
            jsonResponse = await response.json()
            await response.close()

            if responseStatusCode != 200:
                self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching EventSub subscriptions ({userId=}) ({pagination=}) ({response=}): {responseStatusCode}')
                raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching EventSub subscriptions ({userId=}) ({pagination=}) ({response=}): {responseStatusCode}')

            newEventSubResponse = await self.__twitchJsonMapper.parseEventSubResponse(jsonResponse)

            if newEventSubResponse is None:
                self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching EventSub subscriptions ({userId=}) ({pagination=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({newEventSubResponse=})')
                raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching EventSub subscriptions ({userId=}) ({pagination=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({newEventSubResponse=})')

            finalEventSubResponse = await self.__twitchJsonMapper.mergeEventSubResponses(
                first = finalEventSubResponse,
                second = newEventSubResponse,
            )

            if finalEventSubResponse is None:
                pagination = None
            else:
                pagination = finalEventSubResponse.pagination

        if finalEventSubResponse is None:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching EventSub subscriptions ({userId=}) ({pagination=})')
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching EventSub subscriptions ({userId=}) ({pagination=})')

        return finalEventSubResponse

    async def fetchFollower(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str,
    ) -> TwitchFollowersResponse | None:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TwitchApiService', f'Fetching follower... ({broadcasterId=}) ({userId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'broadcaster_id': broadcasterId,
            'user_id': userId,
        })

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/channels/followers?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching follower ({broadcasterId=}) ({userId=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching follower ({broadcasterId=}) ({userId=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching follower ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching follower ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=})',
            )

        followersResponse = await self.__twitchJsonMapper.parseFollowersResponse(jsonResponse)

        if followersResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching follower ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({followersResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching follower ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({followersResponse=})')

        return followersResponse

    async def fetchLiveUserDetails(
        self,
        twitchAccessToken: str,
        twitchChannelIds: list[str]
    ) -> list[TwitchLiveUserDetails]:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(twitchChannelIds, list):
            raise TypeError(f'twitchChannelIds argument is malformed: \"{twitchChannelIds}\"')
        elif len(twitchChannelIds) > 100:
            raise ValueError(f'twitchChannelIds argument has too many values (len is {len(twitchChannelIds)}, max is 100): \"{twitchChannelIds}\"')

        self.__timber.log('TwitchApiService', f'Fetching live user details... ({twitchChannelIds=})')

        userIdsStr = '&user_id='.join(twitchChannelIds)
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/streams?first=100&user_id={userIdsStr}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching live user details ({twitchChannelIds=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching live user details ({twitchChannelIds=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse: dict[str, Any] | Any | None = await response.json()
        await response.close()

        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty/invalid JSON response when fetching live user details ({twitchChannelIds=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching live user details ({twitchChannelIds=}): {jsonResponse}')
        elif responseStatusCode == 401 or ('error' in jsonResponse and len(jsonResponse['error']) >= 1):
            self.__timber.log('TwitchApiService', f'Received an error ({responseStatusCode}) when fetching live user details ({twitchChannelIds=}): {jsonResponse}')
            raise TwitchTokenIsExpiredException(f'TwitchApiService received an error ({responseStatusCode}) when fetching live user details ({twitchChannelIds=}): {jsonResponse}')
        elif responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching live user details ({twitchChannelIds=}): {responseStatusCode}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching live user details ({twitchChannelIds=}): {responseStatusCode}')

        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')
        users: list[TwitchLiveUserDetails] = list()

        if not isinstance(data, list) or len(data) == 0:
            return users

        for dataEntry in data:
            users.append(TwitchLiveUserDetails(
                isMature = utils.getBoolFromDict(dataEntry, 'is_mature', fallback = False),
                streamId = utils.getStrFromDict(dataEntry, 'id'),
                userId = utils.getStrFromDict(dataEntry, 'user_id'),
                userLogin = utils.getStrFromDict(dataEntry, 'user_login'),
                userName = utils.getStrFromDict(dataEntry, 'user_name'),
                viewerCount = utils.getIntFromDict(dataEntry, 'viewer_count', fallback = 0),
                gameId = utils.getStrFromDict(dataEntry, 'game_id', fallback = ''),
                gameName = utils.getStrFromDict(dataEntry, 'game_name', fallback = ''),
                language = utils.getStrFromDict(dataEntry, 'language', fallback = ''),
                thumbnailUrl = utils.getStrFromDict(dataEntry, 'thumbnail_url', fallback = ''),
                title = utils.getStrFromDict(dataEntry, 'title', fallback = ''),
                streamType = await self.__twitchJsonMapper.parseStreamType(utils.getStrFromDict(dataEntry, 'type'))
            ))

        users.sort(key = lambda user: user.userName.casefold())
        return users

    async def fetchModerator(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str,
    ) -> TwitchModeratorsResponse:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TwitchApiService', f'Fetching moderator... ({broadcasterId=}) ({userId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'broadcaster_id': broadcasterId,
            'user_id': userId,
        })

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/moderation/moderators?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching moderator ({broadcasterId=}) ({userId=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching moderator ({broadcasterId=}) ({userId=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching moderator ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching moderator ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode}) ({jsonResponse=})',
            )

        moderatorsResponse = await self.__twitchJsonMapper.parseModeratorsResponse(jsonResponse)

        if moderatorsResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching moderator ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({moderatorsResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching moderator ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({moderatorsResponse=})')

        return moderatorsResponse

    async def fetchStreams(
        self,
        twitchAccessToken: str,
        fetchStreamsRequest: TwitchFetchStreamsRequest,
    ) -> TwitchStreamsResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(fetchStreamsRequest, TwitchFetchStreamsRequest):
            raise TypeError(f'fetchStreamsRequest argument is malformed: \"{fetchStreamsRequest}\"')

        queryString: str

        if isinstance(fetchStreamsRequest, TwitchFetchStreamsWithIdsRequest):
            queryString = urllib.parse.urlencode(
                query = {
                    'user_id': fetchStreamsRequest.userIds,
                },
                doseq = True,
            )

        elif isinstance(fetchStreamsRequest, TwitchFetchStreamsWithLoginsRequest):
            queryString = urllib.parse.urlencode(
                query = {
                    'user_login': fetchStreamsRequest.userLogins,
                },
                doseq = True,
            )

        else:
            raise RuntimeError(f'unknown TwitchFetchStreamsRequest: \"{fetchStreamsRequest}\"')

        self.__timber.log('TwitchApiService', f'Fetching streams... ({fetchStreamsRequest=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/streams?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching streams ({fetchStreamsRequest=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching streams ({fetchStreamsRequest=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching streams ({fetchStreamsRequest=}) ({response=}) ({responseStatusCode=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching streams ({fetchStreamsRequest=}) ({response=}) ({responseStatusCode=})',
            )

        streamsResponse = await self.__twitchJsonMapper.parseStreamsResponse(jsonResponse)

        if streamsResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching streams ({fetchStreamsRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({streamsResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching streams ({fetchStreamsRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({streamsResponse=})')

        return streamsResponse

    async def fetchTokens(self, code: str) -> TwitchTokensDetails:
        if not utils.isValidStr(code):
            raise TypeError(f'code argument is malformed: \"{code}\"')

        self.__timber.log('TwitchApiService', f'Fetching tokens... ({code=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        twitchClientSecret = await self.__twitchCredentialsProvider.getTwitchClientSecret()
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'client_id': twitchClientId,
            'client_secret': twitchClientSecret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost',
        })

        try:
            response = await clientSession.post(
                url = f'https://id.twitch.tv/oauth2/token?{queryString}',
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching tokens ({code=}) ({twitchClientId=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching tokens ({code=}) ({twitchClientId=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching tokens ({code=}) ({twitchClientId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching tokens ({code=}) ({twitchClientId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})',
            )
        elif not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty JSON response when fetching tokens ({code=}) ({twitchClientId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching tokens ({code=}) ({twitchClientId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
        elif 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            self.__timber.log('TwitchApiService', f'Received an error of some kind when fetching tokens ({code=}) ({twitchClientId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchErrorException(f'TwitchApiService received an error of some kind when fetching tokens ({code=}) ({twitchClientId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')

        tokensDetails = await self.__twitchJsonMapper.parseTokensDetails(jsonResponse)

        if tokensDetails is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching tokens ({code=}) ({twitchClientId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching tokens ({code=}) ({twitchClientId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')

        return tokensDetails

    async def fetchUser(
        self,
        twitchAccessToken: str,
        fetchUserRequest: TwitchFetchUserRequest,
    ) -> TwitchUsersResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(fetchUserRequest, TwitchFetchUserRequest):
            raise TypeError(f'fetchUserRequest argument is malformed: \"{fetchUserRequest}\"')

        queryString: str

        if isinstance(fetchUserRequest, TwitchFetchUserWithIdRequest):
            queryString = urllib.parse.urlencode({
                'id': fetchUserRequest.userId,
            })

        elif isinstance(fetchUserRequest, TwitchFetchUserWithLoginRequest):
            queryString = urllib.parse.urlencode({
                'login': fetchUserRequest.userLogin,
            })

        else:
            raise RuntimeError(f'unknown TwitchFetchUserRequest: \"{fetchUserRequest}\"')

        self.__timber.log('TwitchApiService', f'Fetching user... ({fetchUserRequest=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/users?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching user ({fetchUserRequest=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching user ({fetchUserRequest=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching user ({fetchUserRequest=}) ({response=}) ({responseStatusCode=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching user ({fetchUserRequest=}) ({response=}) ({responseStatusCode=})',
            )

        usersResponse = await self.__twitchJsonMapper.parseUsersResponse(jsonResponse)

        if usersResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching user ({fetchUserRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({usersResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching user ({fetchUserRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({usersResponse=})')

        return usersResponse

    async def refreshTokens(self, twitchRefreshToken: str) -> TwitchTokensDetails:
        if not utils.isValidStr(twitchRefreshToken):
            raise TypeError(f'twitchRefreshToken argument is malformed: \"{twitchRefreshToken}\"')

        self.__timber.log('TwitchApiService', f'Refreshing tokens... ({twitchRefreshToken=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        twitchClientSecret = await self.__twitchCredentialsProvider.getTwitchClientSecret()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = 'https://id.twitch.tv/oauth2/token',
                json = {
                    'client_id': twitchClientId,
                    'client_secret': twitchClientSecret,
                    'grant_type': 'refresh_token',
                    'refresh_token': twitchRefreshToken,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when refreshing tokens ({twitchRefreshToken=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when refreshing tokens ({twitchRefreshToken=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode == 400:
            self.__timber.log('TwitchApiService', f'Encountered HTTP 400 status code when refreshing tokens ({twitchRefreshToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchPasswordChangedException(f'TwitchApiService encountered HTTP 400 status code when refreshing tokens ({twitchRefreshToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
        elif responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when refreshing tokens ({twitchRefreshToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when refreshing tokens ({twitchRefreshToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})',
            )
        elif not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty/invalid JSON response when refreshing tokens ({twitchRefreshToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when refreshing tokens ({twitchRefreshToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
        elif 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            self.__timber.log('TwitchApiService', f'Received an error of some kind when refreshing tokens ({twitchRefreshToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchErrorException(f'TwitchApiService received an error of some kind when refreshing tokens ({twitchRefreshToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')

        tokensDetails = await self.__twitchJsonMapper.parseTokensDetails(jsonResponse)

        if tokensDetails is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when refreshing tokens ({twitchRefreshToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({tokensDetails=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when refreshing tokens ({twitchRefreshToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({tokensDetails=})')

        return tokensDetails

    async def removeModerator(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str,
    ) -> bool:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TwitchApiService', f'Removing moderator... ({broadcasterId=}) ({userId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'broadcaster_id': broadcasterId,
            'user_id': userId,
        })

        try:
            response = await clientSession.delete(
                url = f'https://api.twitch.tv/helix/moderation/moderators?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when removing moderator ({broadcasterId=}) ({userId=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when removing moderator ({broadcasterId=}) ({userId=}): {e}')

        responseStatusCode = response.statusCode
        await response.close()

        match responseStatusCode:
            case 204:
                # means that the given user ID has had their moderator status removed
                return True

            case 400:
                # probably means that the given user ID was not a moderator
                return False

            case _:
                self.__timber.log('TwitchApiService', f'Encountered network error when removing moderator ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=})')
                raise TwitchStatusCodeException(
                    statusCode = responseStatusCode,
                    message = f'TwitchApiService encountered network error when removing moderator ({broadcasterId=}) ({userId=}) ({response=}) ({responseStatusCode=})',
                )

    async def sendChatAnnouncement(
        self,
        twitchAccessToken: str,
        announcementRequest: TwitchSendChatAnnouncementRequest,
    ) -> bool:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(announcementRequest, TwitchSendChatAnnouncementRequest):
            raise TypeError(f'announcementRequest argument is malformed: \"{announcementRequest}\"')

        self.__timber.log('TwitchApiService', f'Sending chat announcement... ({announcementRequest=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        queryString = urllib.parse.urlencode({
            'broadcaster_id': announcementRequest.broadcasterId,
            'moderator_id': announcementRequest.moderatorId,
        })

        try:
            response = await clientSession.delete(
                url = f'https://api.twitch.tv/helix/chat/announcements?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                    'Content-Type': 'application/json',
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when sending chat announcement ({announcementRequest=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when sending chat announcement ({announcementRequest=}): {e}')

        responseStatusCode = response.statusCode
        await response.close()

        match responseStatusCode:
            case 204:
                # means that the announcement was successfully sent
                return True

            case _:
                self.__timber.log('TwitchApiService', f'Encountered network error when sending chat announcement ({announcementRequest=}) ({response=}) ({responseStatusCode=})')
                raise TwitchStatusCodeException(
                    statusCode = responseStatusCode,
                    message = f'TwitchApiService encountered network error when sending chat announcement ({announcementRequest=}) ({response=}) ({responseStatusCode=})',
                )

    async def sendChatMessage(
        self,
        twitchAccessToken: str,
        chatRequest: TwitchSendChatMessageRequest,
    ) -> TwitchSendChatMessageResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(chatRequest, TwitchSendChatMessageRequest):
            raise TypeError(f'chatRequest argument is malformed: \"{chatRequest}\"')

        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = 'https://api.twitch.tv/helix/chat/messages',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                    'Content-Type': 'application/json',
                },
                json = await self.__twitchJsonMapper.serializeSendChatMessageRequest(chatRequest),
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when sending chat message ({chatRequest=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when sending chat message ({chatRequest=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when sending chat message ({chatRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when sending chat message ({chatRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse})',
            )

        sendChatMessageResponse = await self.__twitchJsonMapper.parseSendChatMessageResponse(jsonResponse)

        if sendChatMessageResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when sending chat message ({chatRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({sendChatMessageResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when sending chat message ({chatRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({sendChatMessageResponse=})')

        return sendChatMessageResponse

    async def startCommercial(
        self,
        length: int,
        broadcasterId: str,
        twitchAccessToken: str,
    ) -> TwitchStartCommercialResponse:
        if not utils.isValidInt(length):
            raise TypeError(f'length argument is malformed: \"{length}\"')
        elif not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        if length < 30:
            length = 30
        elif length > 180:
            length = 180

        self.__timber.log('TwitchApiService', f'Starting commercial... ({length=}) ({broadcasterId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = 'https://api.twitch.tv/helix/channels/commercial',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                    'Content-Type': 'application/json',
                },
                json = {
                    'broadcaster_id': broadcasterId,
                    'length': length,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when starting commercial ({length=}) ({broadcasterId=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when starting commercial ({length=}) ({broadcasterId=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200 and responseStatusCode != 429:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when starting commercial ({length=}) ({broadcasterId=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when starting commercial ({length=}) ({broadcasterId=}) ({responseStatusCode=}) ({jsonResponse=})',
            )

        startCommercialResponse = await self.__twitchJsonMapper.parseStartCommercialResponse(jsonResponse)

        if startCommercialResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when starting commercial ({length=}) ({broadcasterId=}) ({responseStatusCode=}) ({jsonResponse=}) ({startCommercialResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when starting commercial ({length=}) ({broadcasterId=}) ({responseStatusCode=}) ({jsonResponse=}) ({startCommercialResponse=})')

        return startCommercialResponse

    async def unbanUser(
        self,
        twitchAccessToken: str,
        unbanRequest: TwitchUnbanRequest,
    ) -> bool:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(unbanRequest, TwitchUnbanRequest):
            raise TypeError(f'unbanRequest argument is malformed: \"{unbanRequest}\"')

        self.__timber.log('TwitchApiService', f'Unbanning user... ({unbanRequest=})')
        clientSession = await self.__networkClientProvider.get()
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()

        queryString = urllib.parse.urlencode({
            'broadcaster_id': unbanRequest.broadcasterUserId,
            'moderator_id': unbanRequest.moderatorUserId,
            'user_id': unbanRequest.userIdToBan,
        })

        try:
            response = await clientSession.delete(
                url = f'https://id.twitch.tv/helix/moderation/bans?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                    'Content-Type': 'application/json',
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when unbanning user ({unbanRequest=})', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when unbanning user ({unbanRequest=}): {e}')

        responseStatusCode = response.statusCode
        await response.close()

        match responseStatusCode:
            case 204:
                # means that the given user ID had been banned, and has now been unbanned
                return True

            case 400:
                # probably means that the given user ID had not been banned
                return False

            case _:
                self.__timber.log('TwitchApiService', f'Encountered network error when unbanning user ({unbanRequest=}) ({response=}) ({responseStatusCode=})')
                raise TwitchStatusCodeException(
                    statusCode = responseStatusCode,
                    message = f'TwitchApiService encountered network error when unbanning user ({unbanRequest=}) ({response=}) ({responseStatusCode=})',
                )

    async def validate(self, twitchAccessToken: str) -> TwitchValidationResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        self.__timber.log('TwitchApiService', f'Validating token...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = 'https://id.twitch.tv/oauth2/validate',
                headers = {
                    'Authorization': f'OAuth {twitchAccessToken}',
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when validating token', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when validating token: {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when validating token ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when validating token ({response=}) ({responseStatusCode=}) ({jsonResponse=})',
            )

        validationResponse = await self.__twitchJsonMapper.parseValidationResponse(jsonResponse)

        if validationResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when validating token ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({validationResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when validating token ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({validationResponse=})')

        return validationResponse
