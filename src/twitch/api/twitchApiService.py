import traceback
from datetime import datetime, timedelta
from typing import Any

from .jsonMapper.twitchJsonMapperInterface import TwitchJsonMapperInterface
from .models.twitchBanRequest import TwitchBanRequest
from .models.twitchBanResponse import TwitchBanResponse
from .models.twitchBannedUserResponse import TwitchBannedUserResponse
from .models.twitchBroadcasterSubscription import TwitchBroadcasterSubscription
from .models.twitchChannelEditorsResponse import TwitchChannelEditorsResponse
from .models.twitchChattersRequest import TwitchChattersRequest
from .models.twitchChattersResponse import TwitchChattersResponse
from .models.twitchEmotesResponse import TwitchEmotesResponse
from .models.twitchEventSubRequest import TwitchEventSubRequest
from .models.twitchEventSubResponse import TwitchEventSubResponse
from .models.twitchFollower import TwitchFollower
from .models.twitchLiveUserDetails import TwitchLiveUserDetails
from .models.twitchModUser import TwitchModUser
from .models.twitchSendChatAnnouncementRequest import TwitchSendChatAnnouncementRequest
from .models.twitchSendChatMessageRequest import TwitchSendChatMessageRequest
from .models.twitchSendChatMessageResponse import TwitchSendChatMessageResponse
from .models.twitchTokensDetails import TwitchTokensDetails
from .models.twitchUnbanRequest import TwitchUnbanRequest
from .models.twitchUserDetails import TwitchUserDetails
from .models.twitchUserSubscription import TwitchUserSubscription
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
        twitchJsonMapper: TwitchJsonMapperInterface
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

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchCredentialsProvider: TwitchCredentialsProviderInterface = twitchCredentialsProvider
        self.__twitchJsonMapper: TwitchJsonMapperInterface = twitchJsonMapper

    async def addModerator(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str
    ) -> bool:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TwitchApiService', f'Adding moderator... ({broadcasterId=}) ({twitchAccessToken=}) ({userId=})')
        clientSession = await self.__networkClientProvider.get()
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()

        try:
            response = await clientSession.post(
                url = f'https://api.twitch.tv/helix/moderation/moderators?broadcaster_id={broadcasterId}&user_id={userId}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when adding moderator ({broadcasterId=}) ({userId=}): {e}', e, traceback.format_exc())
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
        banRequest: TwitchBanRequest
    ) -> TwitchBanResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(banRequest, TwitchBanRequest):
            raise TypeError(f'banRequest argument is malformed: \"{banRequest}\"')

        self.__timber.log('TwitchApiService', f'Banning user... ({twitchAccessToken=}) ({banRequest=})')
        clientSession = await self.__networkClientProvider.get()
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()

        try:
            response = await clientSession.post(
                url = f'https://api.twitch.tv/helix/moderation/bans?broadcaster_id={banRequest.broadcasterUserId}&moderator_id={banRequest.moderatorUserId}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                },
                json = await self.__twitchJsonMapper.serializeBanRequest(banRequest)
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when banning user ({banRequest=}): {e}', e, traceback.format_exc())
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

            return TwitchBanResponse(
                createdAt = createdAt,
                endTime = endTime,
                broadcasterUserId = banRequest.broadcasterUserId,
                moderatorUserId = banRequest.moderatorUserId,
                userId = banRequest.userIdToBan
            )
        elif responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when banning user ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise GenericNetworkException(f'Encountered non-200 HTTP status code when banning user ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
        elif not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty/invalid JSON response when banning user ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchJsonException(f'Received a null/empty JSON response when banning user ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')

        data: list[dict[str, Any]] | None = jsonResponse.get('data')
        if not isinstance(data, list) or len(data) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty/malformed \"data\" field in JSON response when banning user ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchJsonException(f'Received a null/empty \"data\" field in JSON response when banning user ({banRequest=}) ({response=}) ({responseStatusCode=})({jsonResponse=})')

        entry: dict[str, Any] | None = data[0]
        if not isinstance(entry, dict) or len(entry) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty/malformed data entry value in JSON response when banning user ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchJsonException(f'Received a null/empty/malformed data entry value in JSON response when banning user ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')

        endTime: datetime | None = None
        if 'end_time' in entry and utils.isValidStr(entry.get('end_time')):
            endTime = utils.getDateTimeFromDict(entry, 'end_time')

        return TwitchBanResponse(
            createdAt = utils.getDateTimeFromDict(entry, 'created_at'),
            endTime = endTime,
            broadcasterUserId = utils.getStrFromDict(entry, 'broadcaster_id'),
            moderatorUserId = utils.getStrFromDict(entry, 'moderator_id'),
            userId = utils.getStrFromDict(entry, 'user_id')
        )

    async def createEventSubSubscription(
        self,
        twitchAccessToken: str,
        eventSubRequest: TwitchEventSubRequest
    ) -> TwitchEventSubResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(eventSubRequest, TwitchEventSubRequest):
            raise TypeError(f'eventSubRequest argument is malformed: \"{eventSubRequest}\"')

        self.__timber.log('TwitchApiService', f'Creating EventSub subscription... ({twitchAccessToken=}) ({eventSubRequest=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = 'https://api.twitch.tv/helix/eventsub/subscriptions',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                    'Content-Type': 'application/json'
                },
                json = await self.__twitchJsonMapper.serializeEventSubRequest(eventSubRequest)
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=})): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse: dict[str, Any] | Any | None = await response.json()
        await response.close()

        if responseStatusCode != 202:
            self.__timber.log('TwitchApiService', f'Encountered non-202 HTTP status code ({responseStatusCode}) when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-202 HTTP status code ({responseStatusCode}) when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}'
            )
        elif not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty/invalid JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')

        data: list[dict[str, Any] | Any | None] | None = jsonResponse.get('data')
        if not isinstance(data, list) or len(data) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty \"data\" field in the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty \"data\" field in the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')

        dataJson: dict[str, Any] | None = data[0]
        if not isinstance(dataJson, dict) or len(dataJson) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty first \"data\" field element in the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty first \"data\" field element in the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')

        cost = utils.getIntFromDict(dataJson, 'cost')
        createdAt = utils.getDateTimeFromDict(dataJson, 'created_at')
        subscriptionId = utils.getStrFromDict(dataJson, 'id')
        version = utils.getStrFromDict(dataJson, 'version')

        subscriptionType = await self.__twitchJsonMapper.parseSubscriptionType(utils.getStrFromDict(dataJson, 'type'))
        if subscriptionType is None:
            self.__timber.log('TwitchApiService', f'Unable to parse TwitchWebsocketSubscriptionType instance from the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService was unable to parse TwitchWebsocketSubscriptionType instance from the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')

        status = await self.__twitchJsonMapper.parseConnectionStatus(utils.getStrFromDict(dataJson, 'status'))
        if status is None:
            self.__timber.log('TwitchApiService', f'Unable to parse TwitchWebsocketConnectionStatus instance from the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService was unable to parse TwitchWebsocketConnectionStatus instance from the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')

        condition = await self.__twitchJsonMapper.parseCondition(dataJson.get('condition'))
        if condition is None:
            self.__timber.log('TwitchApiService', f'Unable to parse TwitchWebsocketCondition instance from the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService was unable to parse TwitchWebsocketCondition instance from the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')

        transportJson: dict[str, Any] | None = dataJson.get('transport')
        if not isinstance(transportJson, dict) or len(transportJson) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty \"transport\" field in the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty \"transport\" field in the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')

        transport = await self.__twitchJsonMapper.requireTransport(transportJson)

        return TwitchEventSubResponse(
            cost = cost,
            maxTotalCost = utils.getIntFromDict(jsonResponse, 'max_total_cost'),
            total = utils.getIntFromDict(jsonResponse, 'total'),
            totalCost = utils.getIntFromDict(jsonResponse, 'total_cost'),
            createdAt = createdAt,
            subscriptionId = subscriptionId,
            version = version,
            condition = condition,
            subscriptionType = subscriptionType,
            status = status,
            transport = transport
        )

    async def fetchBannedUser(
        self,
        broadcasterId: str,
        chatterUserId: str,
        twitchAccessToken: str
    ) -> TwitchBannedUserResponse:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        self.__timber.log('TwitchApiService', f'Fetching banned user... ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/moderation/banned?broadcaster_id={broadcasterId}&user_id={chatterUserId}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching banned user ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching banned user ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching banned user ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching banned user ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})'
            )

        twitchBannedUserResponse = await self.__twitchJsonMapper.parseBannedUserResponse(jsonResponse)

        if twitchBannedUserResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching banned user ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({twitchBannedUserResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching banned user ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({twitchBannedUserResponse=})')

        return twitchBannedUserResponse

    async def fetchBroadcasterSubscription(
        self,
        broadcasterId: str,
        chatterUserId: str,
        twitchAccessToken: str
    ) -> TwitchBroadcasterSubscription:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        self.__timber.log('TwitchApiService', f'Fetching self subscription details... ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/subscriptions?broadcaster_id={broadcasterId}&user_id={chatterUserId}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching broadcaster subscription ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching broadcaster subscription ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}): {e}')

        jsonResponse = await response.json()
        responseStatusCode = response.statusCode
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching broadcaster subscription ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching broadcaster subscription ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})'
            )

        broadcasterSubscription = await self.__twitchJsonMapper.parseBroadcasterSubscription(jsonResponse)

        if broadcasterSubscription is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching broadcaster subscription ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching broadcaster subscription ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')

        return broadcasterSubscription

    async def fetchChannelEditors(
        self,
        broadcasterId: str,
        twitchAccessToken: str
    ) -> TwitchChannelEditorsResponse:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        self.__timber.log('TwitchApiService', f'Fetching channel editors... ({broadcasterId=}) ({twitchAccessToken=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/channels/editors?broadcaster_id={broadcasterId}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching channel editors ({broadcasterId=}) ({twitchAccessToken=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching channel editors ({broadcasterId=}) ({twitchAccessToken=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching channel editors ({broadcasterId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching channel editors ({broadcasterId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})'
            )

        twitchChannelEditorsResponse = await self.__twitchJsonMapper.parseChannelEditorsResponse(jsonResponse)

        if twitchChannelEditorsResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching channel editors ({broadcasterId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({twitchChannelEditorsResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching channel editors ({broadcasterId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({twitchChannelEditorsResponse=})')

        return twitchChannelEditorsResponse

    async def fetchChatters(
        self,
        twitchAccessToken: str,
        chattersRequest: TwitchChattersRequest
    ) -> TwitchChattersResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(chattersRequest, TwitchChattersRequest):
            raise TypeError(f'chattersRequest argument is malformed: \"{chattersRequest}\"')

        first = chattersRequest.first

        if first is None or first < 1 or first > 1000:
            first = 100

        self.__timber.log('TwitchApiService', f'Fetching chatters... ({twitchAccessToken=}) ({chattersRequest=}) ({first=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/chat/chatters?broadcaster_id={chattersRequest.broadcasterId}&moderator_id={chattersRequest.moderatorId}&first={first}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching chatters ({twitchAccessToken=}) ({chattersRequest=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching chatters ({twitchAccessToken=}) ({chattersRequest=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching chatters ({twitchAccessToken=}) ({chattersRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching chatters ({twitchAccessToken=}) ({chattersRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})'
            )

        twitchChattersResponse = await self.__twitchJsonMapper.parseChattersResponse(jsonResponse)

        if twitchChattersResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching chatters ({twitchAccessToken=}) ({chattersRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({twitchChattersResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching chatters ({twitchAccessToken=}) ({chattersRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({twitchChattersResponse=})')

        return twitchChattersResponse

    async def fetchEmotes(
        self,
        broadcasterId: str,
        twitchAccessToken: str
    ) -> TwitchEmotesResponse:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        self.__timber.log('TwitchApiService', f'Fetching emotes... ({broadcasterId=}) ({twitchAccessToken=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/chat/emotes?broadcaster_id={broadcasterId}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching emotes ({broadcasterId=}) ({twitchAccessToken=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching fetching emotes ({broadcasterId=}) ({twitchAccessToken=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching emotes ({broadcasterId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching emotes ({broadcasterId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse})'
            )

        emotesResponse = await self.__twitchJsonMapper.parseEmotesResponse(jsonResponse)

        if emotesResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching emotes ({broadcasterId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({emotesResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching emotes ({broadcasterId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({emotesResponse=})')

        return emotesResponse

    async def fetchFollower(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str
    ) -> TwitchFollower | None:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TwitchApiService', f'Fetching follower... ({broadcasterId=}) ({twitchAccessToken=}) ({userId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/channels/followers?broadcaster_id={broadcasterId}&user_id={userId}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching follower ({broadcasterId=}) ({twitchAccessToken=}) ({userId=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching when fetching follower ({broadcasterId=}) ({twitchAccessToken=}) ({userId=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching follower ({broadcasterId=}) ({twitchAccessToken=}) ({userId=}) ({response=}): {responseStatusCode}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching follower ({broadcasterId=}) ({twitchAccessToken=}) ({userId=}) ({response=}): {responseStatusCode}')

        twitchFollowersResponse = await self.__twitchJsonMapper.parseFollowersResponse(jsonResponse)

        if twitchFollowersResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching follower ({broadcasterId=}) ({twitchAccessToken=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({twitchFollowersResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching follower ({broadcasterId=}) ({twitchAccessToken=}) ({userId=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({twitchFollowersResponse=})')

        for follower in twitchFollowersResponse.followers:
            if follower.userId == userId:
                return follower

        # the requested user is not following
        return None

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

        self.__timber.log('TwitchApiService', f'Fetching live user details... ({twitchAccessToken=}) ({twitchChannelIds=})')

        userIdsStr = '&user_id='.join(twitchChannelIds)
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/streams?first=100&user_id={userIdsStr}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching live user details ({twitchAccessToken=}) ({twitchChannelIds=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching when fetching user details ({twitchAccessToken=}) ({twitchChannelIds=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse: dict[str, Any] | Any | None = await response.json()
        await response.close()

        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty/invalid JSON response when fetching live user details ({twitchAccessToken=}) ({twitchChannelIds=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching live user details ({twitchAccessToken=}) ({twitchChannelIds=}): {jsonResponse}')
        elif responseStatusCode == 401 or ('error' in jsonResponse and len(jsonResponse['error']) >= 1):
            self.__timber.log('TwitchApiService', f'Received an error ({responseStatusCode}) when fetching live user details ({twitchAccessToken=}) ({twitchChannelIds=}): {jsonResponse}')
            raise TwitchTokenIsExpiredException(f'TwitchApiService received an error ({responseStatusCode}) when fetching live user details ({twitchAccessToken=}) ({twitchChannelIds=}): {jsonResponse}')
        elif responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching live user details ({twitchAccessToken=}) ({twitchChannelIds=}): {responseStatusCode}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching live user details ({twitchAccessToken=}) ({twitchChannelIds=}): {responseStatusCode}')

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
        userId: str
    ) -> TwitchModUser | None:
        if not utils.isValidStr(broadcasterId):
            raise ValueError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TwitchApiService', f'Fetching moderator... ({broadcasterId=}) ({twitchAccessToken=}) ({userId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/moderation/moderators?first=100&broadcaster_id={broadcasterId}&user_id={userId}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching moderator ({broadcasterId=}) ({userId=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching when fetching moderator ({broadcasterId=}) ({userId=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse: dict[str, Any] | Any | None = await response.json()
        await response.close()

        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty/invalid JSON response when fetching moderator ({broadcasterId=}) ({userId=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching moderator ({broadcasterId=}) ({userId=}): {jsonResponse}')
        elif responseStatusCode == 401 or ('error' in jsonResponse and len(jsonResponse['error']) >= 1):
            self.__timber.log('TwitchApiService', f'Received an error ({responseStatusCode}) when fetching moderator ({broadcasterId=}) ({userId=}): {jsonResponse}')
            raise TwitchTokenIsExpiredException(f'TwitchApiService received an error ({responseStatusCode}) when fetching moderator ({broadcasterId=}) ({userId=}): {jsonResponse}')
        elif responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching moderator ({broadcasterId=}) ({userId=}): {responseStatusCode}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching moderator ({broadcasterId=}) ({userId=}): {responseStatusCode}')

        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')

        if not isinstance(data, list) or len(data) == 0:
            return None

        return TwitchModUser(
            userId = utils.getStrFromDict(data[0], 'user_id'),
            userLogin = utils.getStrFromDict(data[0], 'user_login'),
            userName = utils.getStrFromDict(data[0], 'user_name')
        )

    async def fetchTokens(self, code: str) -> TwitchTokensDetails:
        if not utils.isValidStr(code):
            raise TypeError(f'code argument is malformed: \"{code}\"')

        self.__timber.log('TwitchApiService', f'Fetching tokens... ({code=})')

        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        twitchClientSecret = await self.__twitchCredentialsProvider.getTwitchClientSecret()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = f'https://id.twitch.tv/oauth2/token?client_id={twitchClientId}&client_secret={twitchClientSecret}&code={code}&grant_type=authorization_code&redirect_uri=http://localhost'
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching tokens ({code=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching tokens ({code=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching tokens ({code=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching tokens ({code=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
        elif not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty JSON response when fetching tokens ({code=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching tokens ({code=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
        elif 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            self.__timber.log('TwitchApiService', f'Received an error of some kind when fetching tokens ({code=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchErrorException(f'TwitchApiService received an error of some kind when fetching tokens ({code=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')

        tokensDetails = await self.__twitchJsonMapper.parseTokensDetails(jsonResponse)

        if tokensDetails is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching tokens ({code=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching tokens ({code=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')

        return tokensDetails

    async def fetchUserDetailsWithUserId(
        self,
        twitchAccessToken: str,
        userId: str
    ) -> TwitchUserDetails | None:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TwitchApiService', f'Fetching user details with user ID... ({twitchAccessToken=}) ({userId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/users?id={userId}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching user details ({userId=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching when fetching user details ({userId=}): {e}')

        if response.statusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching user details ({userId=}): {response.statusCode}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching user details ({userId=}): {response.statusCode}')

        jsonResponse: dict[str, Any] | Any | None = await response.json()
        await response.close()

        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty/invalid JSON response when fetching user details ({userId=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching user details ({userId=}): {jsonResponse}')
        elif 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            self.__timber.log('TwitchApiService', f'Received an error of some kind when fetching user details ({userId=}): {jsonResponse}')
            raise TwitchErrorException(f'TwitchApiService received an error of some kind when fetching user details ({userId=}): {jsonResponse}')

        data: list[dict[str, Any]] | None = jsonResponse.get('data')

        if not isinstance(data, list) or len(data) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty \"data\" field in JSON response when fetching user details ({userId=}): {jsonResponse}')
            return None

        entry: dict[str, Any] | None = None

        for dataEntry in data:
            if utils.getStrFromDict(dataEntry, 'id').lower() == userId:
                entry = dataEntry
                break

        if entry is None:
            self.__timber.log('TwitchApiService', f'Couldn\'t find entry with matching \"id\" field in JSON response when fetching user details ({userId=}): {jsonResponse}')
            return None

        return TwitchUserDetails(
            displayName = utils.getStrFromDict(entry, 'display_name'),
            login = utils.getStrFromDict(entry, 'login'),
            userId = utils.getStrFromDict(entry, 'id'),
            broadcasterType = await self.__twitchJsonMapper.parseBroadcasterType(utils.getStrFromDict(entry, 'broadcaster_type')),
            userType = await self.__twitchJsonMapper.parseUserType(utils.getStrFromDict(entry, 'type'))
        )

    async def fetchUserDetailsWithUserName(
        self,
        twitchAccessToken: str,
        userName: str
    ) -> TwitchUserDetails | None:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__timber.log('TwitchApiService', f'Fetching user details with username... ({twitchAccessToken=}) ({userName=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/users?login={userName}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching user details ({userName=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching when fetching user details ({userName=}): {e}')

        if response.statusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching user details ({userName=}): {response.statusCode}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching user details ({userName=}): {response.statusCode}')

        jsonResponse: dict[str, Any] | Any | None = await response.json()
        await response.close()

        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty/invalid JSON response when fetching user details ({userName=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching user details ({userName=}): {jsonResponse}')
        elif 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            self.__timber.log('TwitchApiService', f'Received an error of some kind when fetching user details ({userName=}): {jsonResponse}')
            raise TwitchErrorException(f'TwitchApiService received an error of some kind when fetching user details ({userName=}): {jsonResponse}')

        data: list[dict[str, Any]] | None = jsonResponse.get('data')

        if not isinstance(data, list) or len(data) == 0:
            self.__timber.log('TwitchApiService', f'Received a null/empty \"data\" field in JSON response when fetching user details ({userName=}): {jsonResponse}')
            return None

        entry: dict[str, Any] | None = None

        for dataEntry in data:
            if utils.getStrFromDict(dataEntry, 'login').casefold() == userName:
                entry = dataEntry
                break

        if entry is None:
            self.__timber.log('TwitchApiService', f'Couldn\'t find entry with matching \"login\" field in JSON response when fetching user details ({userName=}): {jsonResponse}')
            return None

        return TwitchUserDetails(
            displayName = utils.getStrFromDict(entry, 'display_name'),
            login = utils.getStrFromDict(entry, 'login'),
            userId = utils.getStrFromDict(entry, 'id'),
            broadcasterType = await self.__twitchJsonMapper.parseBroadcasterType(utils.getStrFromDict(entry, 'broadcaster_type')),
            userType = await self.__twitchJsonMapper.parseUserType(utils.getStrFromDict(entry, 'type'))
        )

    async def fetchUserSubscription(
        self,
        broadcasterId: str,
        chatterUserId: str,
        twitchAccessToken: str
    ) -> TwitchUserSubscription:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        self.__timber.log('TwitchApiService', f'Fetching user subscription details... ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/subscriptions/user?broadcaster_id={broadcasterId}&user_id={chatterUserId}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching user subscription ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching user subscription ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}): {e}')

        jsonResponse = await response.json()
        responseStatusCode = response.statusCode
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching user subscription ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when fetching user subscription ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})'
            )

        userSubscription = await self.__twitchJsonMapper.parseUserSubscription(jsonResponse)

        if userSubscription is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching user subscription ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching user subscription ({broadcasterId=}) ({chatterUserId=}) ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')

        return userSubscription

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
                    'refresh_token': twitchRefreshToken
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when refreshing tokens ({twitchRefreshToken=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when refreshing tokens ({twitchRefreshToken=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode == 400:
            self.__timber.log('TwitchApiService', f'Encountered HTTP 400 status code when refreshing tokens ({twitchRefreshToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchPasswordChangedException(f'TwitchApiService encountered HTTP 400 status code when refreshing tokens ({twitchRefreshToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
        elif responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when refreshing tokens ({twitchRefreshToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when refreshing tokens ({twitchRefreshToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
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
        moderatorId: str,
        twitchAccessToken: str
    ) -> bool:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(moderatorId):
            raise TypeError(f'moderatorId argument is malformed: \"{moderatorId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        self.__timber.log('TwitchApiService', f'Removing moderator... ({broadcasterId=}) ({moderatorId=}) ({twitchAccessToken=})')

        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.delete(
                url = f'https://api.twitch.tv/helix/moderation/moderators?broadcaster_id={broadcasterId}&user_id={moderatorId}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when removing moderator ({broadcasterId=}) ({moderatorId=}) ({twitchAccessToken=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when removing moderator ({broadcasterId=}) ({moderatorId=}) ({twitchAccessToken=}): {e}')

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
                self.__timber.log('TwitchApiService', f'Encountered network error when removing moderator ({broadcasterId=}) ({moderatorId=}) ({twitchAccessToken=}) ({response=}): {responseStatusCode}')
                raise GenericNetworkException(f'TwitchApiService encountered network error when removing moderator ({broadcasterId=}) ({moderatorId=}) ({twitchAccessToken=}) ({response=}): {responseStatusCode}')

    async def sendChatAnnouncement(
        self,
        twitchAccessToken: str,
        announcementRequest: TwitchSendChatAnnouncementRequest
    ) -> bool:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(announcementRequest, TwitchSendChatAnnouncementRequest):
            raise TypeError(f'announcementRequest argument is malformed: \"{announcementRequest}\"')

        self.__timber.log('TwitchApiService', f'Sending chat announcement... ({twitchAccessToken=}) ({announcementRequest=})')

        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.delete(
                url = f'https://api.twitch.tv/helix/chat/announcements?broadcaster_id={announcementRequest.broadcasterId}&moderator_id={announcementRequest.moderatorId}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                    'Content-Type': 'application/json'
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when sending chat announcement ({twitchAccessToken=}) ({announcementRequest=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when sending chat announcement ({twitchAccessToken=}) ({announcementRequest=}): {e}')

        responseStatusCode = response.statusCode
        await response.close()

        match responseStatusCode:
            case 204:
                # means that the announcement was successfully sent
                return True

            case _:
                self.__timber.log('TwitchApiService', f'Encountered network error when sending chat announcement ({twitchAccessToken=}) ({announcementRequest=}) ({response=}): {responseStatusCode}')
                raise GenericNetworkException(f'TwitchApiService encountered network error when sending chat announcement ({twitchAccessToken=}) ({announcementRequest=}) ({response=}): {responseStatusCode}')

    async def sendChatMessage(
        self,
        twitchAccessToken: str,
        chatRequest: TwitchSendChatMessageRequest
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
                    'Content-Type': 'application/json'
                },
                json = await self.__twitchJsonMapper.serializeSendChatMessageRequest(chatRequest)
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when sending chat message ({chatRequest=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when sending chat message ({chatRequest=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when sending chat message ({chatRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when sending chat message ({chatRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse})'
            )

        sendChatMessageResponse = await self.__twitchJsonMapper.parseSendChatMessageResponse(jsonResponse)

        if sendChatMessageResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when sending chat message ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({sendChatMessageResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when sending chat message ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({sendChatMessageResponse=})')

        return sendChatMessageResponse

    async def unbanUser(
        self,
        twitchAccessToken: str,
        unbanRequest: TwitchUnbanRequest
    ) -> bool:
        if not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not isinstance(unbanRequest, TwitchUnbanRequest):
            raise ValueError(f'unbanRequest argument is malformed: \"{unbanRequest}\"')

        self.__timber.log('TwitchApiService', f'Unbanning user... ({twitchAccessToken=}) ({unbanRequest=})')

        clientSession = await self.__networkClientProvider.get()
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()

        try:
            response = await clientSession.delete(
                url = f'https://id.twitch.tv/helix/moderation/bans?broadcaster_id={unbanRequest.broadcasterUserId}&moderator_id={unbanRequest.moderatorUserId}&user_id={unbanRequest.userIdToBan}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                    'Content-Type': 'application/json'
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when unbanning user ({twitchAccessToken=}) ({unbanRequest=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when unbanning user ({twitchAccessToken=}) ({unbanRequest=}): {e}')

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
                self.__timber.log('TwitchApiService', f'Encountered network error when unbanning user ({twitchAccessToken=}) ({unbanRequest=}) ({response=}): {responseStatusCode}')
                raise GenericNetworkException(f'TwitchApiService encountered network error when unbanning user ({twitchAccessToken=}) ({unbanRequest=}) ({response=}): {responseStatusCode}')

    async def validate(self, twitchAccessToken: str) -> TwitchValidationResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        self.__timber.log('TwitchApiService', f'Validating token... ({twitchAccessToken=})')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = 'https://id.twitch.tv/oauth2/validate',
                headers = {
                    'Authorization': f'OAuth {twitchAccessToken}'
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when validating token ({twitchAccessToken=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when validating token ({twitchAccessToken=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when validating token ({twitchAccessToken=}) ({responseStatusCode=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when validating token ({twitchAccessToken=}) ({responseStatusCode=})'
            )

        validationResponse = await self.__twitchJsonMapper.parseValidationResponse(jsonResponse)

        if validationResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when validating token ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({validationResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when validating token ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({validationResponse=})')

        return validationResponse
