import traceback
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.network.networkHandle import NetworkHandle
from CynanBot.network.networkResponse import NetworkResponse
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.api.twitchBannedUser import TwitchBannedUser
from CynanBot.twitch.api.twitchBannedUserRequest import TwitchBannedUserRequest
from CynanBot.twitch.api.twitchBannedUsersPageResponse import \
    TwitchBannedUsersPageResponse
from CynanBot.twitch.api.twitchBannedUsersResponse import \
    TwitchBannedUsersResponse
from CynanBot.twitch.api.twitchBanRequest import TwitchBanRequest
from CynanBot.twitch.api.twitchBanResponse import TwitchBanResponse
from CynanBot.twitch.api.twitchBroadcasterType import TwitchBroadcasterType
from CynanBot.twitch.api.twitchEmoteDetails import TwitchEmoteDetails
from CynanBot.twitch.api.twitchEmoteImage import TwitchEmoteImage
from CynanBot.twitch.api.twitchEmoteImageScale import TwitchEmoteImageScale
from CynanBot.twitch.api.twitchEmoteType import TwitchEmoteType
from CynanBot.twitch.api.twitchEventSubRequest import TwitchEventSubRequest
from CynanBot.twitch.api.twitchEventSubResponse import TwitchEventSubResponse
from CynanBot.twitch.api.twitchFollower import TwitchFollower
from CynanBot.twitch.api.twitchLiveUserDetails import TwitchLiveUserDetails
from CynanBot.twitch.api.twitchModUser import TwitchModUser
from CynanBot.twitch.api.twitchStreamType import TwitchStreamType
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier
from CynanBot.twitch.api.twitchTokensDetails import TwitchTokensDetails
from CynanBot.twitch.api.twitchUnbanRequest import TwitchUnbanRequest
from CynanBot.twitch.api.twitchUserDetails import TwitchUserDetails
from CynanBot.twitch.api.twitchUserSubscriptionDetails import \
    TwitchUserSubscriptionDetails
from CynanBot.twitch.api.twitchUserType import TwitchUserType
from CynanBot.twitch.api.websocket.twitchWebsocketConnectionStatus import \
    TwitchWebsocketConnectionStatus
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from CynanBot.twitch.api.websocket.twitchWebsocketTransport import \
    TwitchWebsocketTransport
from CynanBot.twitch.api.websocket.twitchWebsocketTransportMethod import \
    TwitchWebsocketTransportMethod
from CynanBot.twitch.exceptions import (TwitchAccessTokenMissingException,
                                        TwitchErrorException,
                                        TwitchJsonException,
                                        TwitchPasswordChangedException,
                                        TwitchRefreshTokenMissingException,
                                        TwitchStatusCodeException,
                                        TwitchTokenIsExpiredException)
from CynanBot.twitch.twitchCredentialsProviderInterface import \
    TwitchCredentialsProviderInterface
from CynanBot.twitch.twitchPaginationResponse import TwitchPaginationResponse
from CynanBot.twitch.websocket.twitchWebsocketJsonMapperInterface import \
    TwitchWebsocketJsonMapperInterface


class TwitchApiService(TwitchApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        twitchCredentialsProvider: TwitchCredentialsProviderInterface,
        twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface,
        timeZone: timezone = timezone.utc
    ):
        assert isinstance(networkClientProvider, NetworkClientProvider), f"malformed {networkClientProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchCredentialsProvider, TwitchCredentialsProviderInterface), f"malformed {twitchCredentialsProvider=}"
        assert isinstance(twitchWebsocketJsonMapper, TwitchWebsocketJsonMapperInterface), f"malformed {twitchWebsocketJsonMapper=}"
        assert isinstance(timeZone, timezone), f"malformed {timeZone=}"

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__twitchCredentialsProvider: TwitchCredentialsProviderInterface = twitchCredentialsProvider
        self.__twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface = twitchWebsocketJsonMapper
        self.__timeZone: timezone = timeZone

    async def addModerator(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str
    ) -> bool:
        if not utils.isValidStr(broadcasterId):
            raise ValueError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        if not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

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
            raise GenericNetworkException(f'TwitchApiService encountered network when adding moderator ({broadcasterId=}) ({userId=}): {e}')

        if response is None:
            self.__timber.log('TwitchApiService', f'Encountered unknown network error when adding moderator ({broadcasterId=}) ({userId=}) ({response=})')
            raise GenericNetworkException(f'TwitchApiService encountered unknown network error when adding moderator ({broadcasterId=}) ({userId=}) ({response=})')

        responseStatusCode = response.getStatusCode()
        await response.close()

        if responseStatusCode == 204:
            return True
        else:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when adding moderator ({broadcasterId=}) ({userId=}) ({responseStatusCode=})')
            return False

    async def banUser(
        self,
        twitchAccessToken: str,
        banRequest: TwitchBanRequest
    ) -> TwitchBanResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        assert isinstance(banRequest, TwitchBanRequest), f"malformed {banRequest=}"

        self.__timber.log('TwitchApiService', f'Banning user... ({twitchAccessToken=}) ({banRequest=})')
        clientSession = await self.__networkClientProvider.get()
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()

        try:
            response = await clientSession.post(
                url = f'https://api.twitch.tv/helix/moderation/bans?broadcaster_id={banRequest.getBroadcasterUserId()}&moderator_id={banRequest.getModeratorUserId()}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                },
                json = banRequest.toJson()
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when banning user ({banRequest=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network when banning user ({banRequest=}): {e}')

        if response is None:
            self.__timber.log('TwitchApiService', f'Encountered unknown network error when banning user ({banRequest=}) ({response=})')
            raise GenericNetworkException(f'TwitchApiService encountered unknown network error when banning user ({banRequest=}) ({response=})')

        responseStatusCode = response.getStatusCode()
        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when banning user ({banRequest=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise GenericNetworkException(f'Encountered non-200 HTTP status code when banning user ({banRequest=}) ({responseStatusCode=}) ({jsonResponse=})')
        if not utils.hasItems(jsonResponse):
            self.__timber.log('TwitchApiService', f'Received a null/empty JSON response when banning user ({banRequest=}) ({jsonResponse=})')
            raise TwitchJsonException(f'Recieved a null/empty JSON response when banning user ({banRequest=}) ({jsonResponse=})')

        data: Optional[List[Dict[str, Any]]] = jsonResponse.get('data')

        if not utils.hasItems(data) or not utils.hasItems(data[0]):
            self.__timber.log('TwitchApiService', f'Received a null/empty \"data\" field in JSON response when banning user ({banRequest=}) ({jsonResponse=})')
            raise TwitchJsonException(f'Received a null/empty \"data\" field in JSON response when banning user ({banRequest=}) ({jsonResponse=})')

        entry = data[0]

        endTime: Optional[SimpleDateTime] = None
        if 'end_time' in entry and utils.isValidStr(entry.get('end_time')):
            endTime = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(entry, 'end_time')))

        return TwitchBanResponse(
            createdAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(entry, 'created_at'))),
            endTime = endTime,
            broadcasterUserId = utils.getStrFromDict(entry, 'broadcaster_id'),
            moderatorUserId = utils.getStrFromDict(entry, 'moderator_id'),
            userId = utils.getStrFromDict(entry, 'user_id')
        )

    async def __calculateExpirationTime(self, expiresInSeconds: Optional[int]) -> datetime:
        nowDateTime = datetime.now(self.__timeZone)

        if utils.isValidInt(expiresInSeconds) and expiresInSeconds > 0:
            return nowDateTime + timedelta(seconds = expiresInSeconds)
        else:
            return nowDateTime - timedelta(weeks = 1)

    async def createEventSubSubscription(
        self,
        twitchAccessToken: str,
        eventSubRequest: TwitchEventSubRequest
    ) -> TwitchEventSubResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        assert isinstance(eventSubRequest, TwitchEventSubRequest), f"malformed {eventSubRequest=}"

        self.__timber.log('TwitchApiService', f'Creating EventSub subscription... ({twitchAccessToken=}) ({eventSubRequest=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = 'https://api.twitch.tv/helix/eventsub/subscriptions',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                },
                json = eventSubRequest.toJson()
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=})): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {e}')

        responseStatusCode = response.getStatusCode()
        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('TwitchApiService', f'Received a null/empty JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
        if responseStatusCode != 202:
            self.__timber.log('TwitchApiService', f'Encountered non-202 HTTP status code ({responseStatusCode}) when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
            raise TwitchStatusCodeException(f'TwitchApiService encountered non-202 HTTP status code ({responseStatusCode}) when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')

        data: Optional[List[Dict[str, Any]]] = jsonResponse.get('data')
        if not utils.hasItems(data):
            self.__timber.log('TwitchApiService', f'Received a null/empty \"data\" field in the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty \"data\" field in the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')

        dataJson: Dict[str, Any] = data[0]
        if not utils.hasItems(dataJson):
            self.__timber.log('TwitchApiService', f'Received a null/empty first \"data\" field element in the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty first \"data\" field element in the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')

        cost = utils.getIntFromDict(dataJson, 'cost')
        createdAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(dataJson, 'created_at')))
        subscriptionId = utils.getStrFromDict(dataJson, 'id')
        version = utils.getStrFromDict(dataJson, 'version')
        subscriptionType = TwitchWebsocketSubscriptionType.fromStr(utils.getStrFromDict(dataJson, 'type'))
        status = TwitchWebsocketConnectionStatus.fromStr(utils.getStrFromDict(dataJson, 'status'))

        conditionJson: Optional[Dict[str, Any]] = dataJson.get('condition')
        if not utils.hasItems(conditionJson):
            self.__timber.log('TwitchApiService', f'Received a null/empty \"condition\" field in the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty \"condition\" field in the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')

        condition = await self.__twitchWebsocketJsonMapper.parseWebsocketCondition(dataJson.get('condition'))

        transportJson: Optional[Dict[str, Any]] = dataJson.get('transport')
        if not utils.hasItems(transportJson):
            self.__timber.log('TwitchApiService', f'Received a null/empty \"transport\" field in the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty \"transport\" field in the JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {jsonResponse}')

        transport = TwitchWebsocketTransport(
            connectedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(transportJson, 'connected_at'))),
            sessionId = utils.getStrFromDict(transportJson, 'session_id'),
            method = TwitchWebsocketTransportMethod.fromStr(utils.getStrFromDict(transportJson, 'method'))
        )

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

    async def fetchBannedUsers(
        self,
        twitchAccessToken: str,
        bannedUserRequest: TwitchBannedUserRequest
    ) -> TwitchBannedUsersResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        assert isinstance(bannedUserRequest, TwitchBannedUserRequest), f"malformed {bannedUserRequest=}"

        self.__timber.log('TwitchApiService', f'Fetching banned users... {bannedUserRequest=}')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        firstFetch = True
        currentPagination: Optional[TwitchPaginationResponse] = None
        pages: List[TwitchBannedUsersPageResponse] = list()

        while firstFetch or currentPagination is not None:
            if firstFetch:
                firstFetch = False

            page = await self.__fetchBannedUsers(
                clientSession = clientSession,
                twitchAccessToken = twitchAccessToken,
                twitchClientId = twitchClientId,
                bannedUserRequest = bannedUserRequest,
                currentPagination = currentPagination
            )

            if page is None:
                currentPagination = None
            else:
                pages.append(page)
                currentPagination = page.getPagination()

        allUsers: List[TwitchBannedUser] = list()

        for page in pages:
            usersPage = page.getUsers()

            if usersPage is not None and len(usersPage) >= 1:
                allUsers.extend(usersPage)

        allUsers.sort(key = lambda user: user.getUserLogin().lower())

        return TwitchBannedUsersResponse(
            users = allUsers,
            broadcasterId = bannedUserRequest.getBroadcasterId(),
            requestedUserId = bannedUserRequest.getRequestedUserId()
        )

    async def __fetchBannedUsers(
        self,
        clientSession: NetworkHandle,
        twitchAccessToken: str,
        twitchClientId: str,
        bannedUserRequest: TwitchBannedUserRequest,
        currentPagination: Optional[TwitchPaginationResponse]
    ) -> TwitchBannedUsersPageResponse:
        assert isinstance(clientSession, NetworkHandle), f"malformed {clientSession=}"
        if not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        if not utils.isValidStr(twitchClientId):
            raise ValueError(f'twitchClientId argument is malformed: \"{twitchClientId}\"')
        assert isinstance(bannedUserRequest, TwitchBannedUserRequest), f"malformed {bannedUserRequest=}"
        assert currentPagination is None or isinstance(currentPagination, TwitchPaginationResponse), f"malformed {currentPagination=}"

        url = f'https://api.twitch.tv/helix/moderation/banned?broadcaster_id={bannedUserRequest.getBroadcasterId()}&first=100'

        if utils.isValidStr(bannedUserRequest.getRequestedUserId()):
            url = f'{url}&user_id={bannedUserRequest.getRequestedUserId()}'

        if currentPagination is not None:
            url = f'{url}&first={currentPagination.getCursor()}'

        try:
            response = await clientSession.get(
                url = url,
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching banned users ({twitchAccessToken=}) ({bannedUserRequest=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching banned users ({twitchAccessToken=}) ({bannedUserRequest=}): {e}')

        responseStatusCode = response.getStatusCode()
        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('TwitchApiService', f'Received a null/empty JSON response when fetching banned users ({twitchAccessToken=}) ({bannedUserRequest=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching banned users ({twitchAccessToken=}) ({bannedUserRequest=}): {jsonResponse}')
        if responseStatusCode == 401 or ('error' in jsonResponse and len(jsonResponse['error']) >= 1):
            self.__timber.log('TwitchApiService', f'Received an error ({responseStatusCode}) when fetching banned users ({twitchAccessToken=}) ({bannedUserRequest=}): {jsonResponse}')
            raise TwitchTokenIsExpiredException(f'TwitchApiService received an error ({responseStatusCode}) when fetching banned users ({twitchAccessToken=}) ({bannedUserRequest=}): {jsonResponse}')
        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching banned users ({twitchAccessToken=}) ({bannedUserRequest=}): {responseStatusCode}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching banned users ({twitchAccessToken=}) ({bannedUserRequest=}): {responseStatusCode}')

        data: Optional[List[Dict[str, Any]]] = jsonResponse.get('data')
        if not utils.hasItems(data):
            return TwitchBannedUsersPageResponse(
                users = None,
                pagination = None
            )

        users: List[TwitchBannedUser] = list()

        for bannedUserJson in data:
            expiresAt: Optional[SimpleDateTime] = None
            if 'expires_at' in bannedUserJson and utils.isValidStr(bannedUserJson.get('expires_at')):
                expiresAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(bannedUserJson, 'expires_at')))

            reason: Optional[str] = None
            if 'reason' in bannedUserJson and utils.isValidStr(bannedUserJson.get('reason')):
                reason = utils.getStrFromDict(bannedUserJson, 'reason')

            users.append(TwitchBannedUser(
                createdAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(bannedUserJson, 'created_at'))),
                expiresAt = expiresAt,
                moderatorId = utils.getStrFromDict(bannedUserJson, 'moderator_id'),
                moderatorLogin = utils.getStrFromDict(bannedUserJson, 'moderator_login'),
                moderatorName = utils.getStrFromDict(bannedUserJson, 'moderator_name'),
                reason = reason,
                userId = utils.getStrFromDict(bannedUserJson, 'user_id'),
                userLogin = utils.getStrFromDict(bannedUserJson, 'user_login'),
                userName = utils.getStrFromDict(bannedUserJson, 'user_name')
            ))

        users.sort(key = lambda user: user.getUserLogin().lower())

        paginationJson: Optional[Dict[str, Any]] = jsonResponse.get('pagination')
        pagination: Optional[TwitchPaginationResponse] = None

        if isinstance(paginationJson, Dict) and utils.isValidStr(paginationJson.get('cursor')):
            pagination = TwitchPaginationResponse(
                cursor = utils.getStrFromDict(paginationJson, 'cursor')
            )

        return TwitchBannedUsersPageResponse(
            users = users,
            pagination = pagination
        )

    async def fetchEmoteDetails(
        self,
        broadcasterId: str,
        twitchAccessToken: str
    ) -> List[TwitchEmoteDetails]:
        if not utils.isValidStr(broadcasterId):
            raise ValueError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        if not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        self.__timber.log('TwitchApiService', f'Fetching emote details... ({broadcasterId=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/emotes?broadcaster_id={broadcasterId}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching emote details (broadcasterId=\"{broadcasterId}\") (twitchAccessToken=\"{twitchAccessToken}\"): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching emote details (broadcasterId=\"{broadcasterId}\") (twitchAccessToken=\"{twitchAccessToken}\"): {e}')

        responseStatusCode = response.getStatusCode()
        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('TwitchApiService', f'Received a null/empty JSON response when fetching emote details (broadcasterId=\"{broadcasterId}\"): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching emote details (broadcasterId=\"{broadcasterId}\"): {jsonResponse}')
        if responseStatusCode == 401 or ('error' in jsonResponse and len(jsonResponse['error']) >= 1):
            self.__timber.log('TwitchApiService', f'Received an error ({responseStatusCode}) when fetching emote details (broadcasterId=\"{broadcasterId}\"): {jsonResponse}')
            raise TwitchTokenIsExpiredException(f'TwitchApiService received an error ({responseStatusCode}) when fetching emote details (broadcasterId=\"{broadcasterId}\"): {jsonResponse}')
        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching emote details (broadcasterId=\"{broadcasterId}\"): {responseStatusCode}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching emote details (broadcasterId=\"{broadcasterId}\"): {responseStatusCode}')

        data: Optional[List[Dict[str, Any]]] = jsonResponse.get('data')
        if not utils.hasItems(data):
            self.__timber.log('TwitchApiService', f'Received a null/empty \"data\" field in the JSON response when fetching emote details (broadcasterId=\"{broadcasterId}\"): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty \"data\" field in the JSON response when fetching emote details (broadcasterId=\"{broadcasterId}\"): {jsonResponse}')

        emoteDetailsList: List[TwitchEmoteDetails] = list()

        for emoteJson in data:
            imagesJson: Dict[str, str] = emoteJson['images']
            emoteImages: List[TwitchEmoteImage] = list()

            for imageJsonKey, imageJsonValue in imagesJson:
                emoteImages.append(TwitchEmoteImage(
                    url = imageJsonKey,
                    imageScale = TwitchEmoteImageScale.fromStr(imageJsonValue)
                ))

            emoteId = utils.getStrFromDict(emoteJson, 'id')
            emoteName = utils.getStrFromDict(emoteJson, 'name')
            emoteType = TwitchEmoteType.fromStr(utils.getStrFromDict(emoteJson, 'emote_type'))
            subscriberTier = TwitchSubscriberTier.fromStr(utils.getStrFromDict(emoteJson, 'tier'))

            emoteDetailsList.append(TwitchEmoteDetails(
                emoteImages = emoteImages,
                emoteId = emoteId,
                emoteName = emoteName,
                emoteType = emoteType,
                subscriberTier = subscriberTier
            ))

        return emoteDetailsList

    async def fetchFollower(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str
    ) -> Optional[TwitchFollower]:
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        if not utils.isValidStr(userId):
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

        responseStatusCode = response.getStatusCode()
        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('TwitchApiService', f'Received a null/empty JSON response when fetching follower ({broadcasterId=}) ({twitchAccessToken=}) ({userId=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching follower ({broadcasterId=}) ({twitchAccessToken=}) ({userId=}): {jsonResponse}')
        if responseStatusCode == 401 or ('error' in jsonResponse and len(jsonResponse['error']) >= 1):
            self.__timber.log('TwitchApiService', f'Received an error ({responseStatusCode}) when fetching follower ({broadcasterId=}) ({twitchAccessToken=}) ({userId=}): {jsonResponse}')
            raise TwitchTokenIsExpiredException(f'TwitchApiService received an error ({responseStatusCode}) when fetching follower ({broadcasterId=}) ({twitchAccessToken=}) ({userId=}): {jsonResponse}')
        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching follower ({broadcasterId=}) ({twitchAccessToken=}) ({userId=}): {responseStatusCode}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching follower ({broadcasterId=}) ({twitchAccessToken=}) ({userId=}): {responseStatusCode}')

        data: Optional[List[Dict[str, Any]]] = jsonResponse.get('data')

        if not isinstance(data, List) or len(data) == 0:
            return None

        for dataEntry in data:
            dataEntryUserId = utils.getStrFromDict(dataEntry, 'user_id')

            if dataEntryUserId == userId:
                return TwitchFollower(
                    followedAt = SimpleDateTime(utils.getDateTimeFromStr(utils.getStrFromDict(dataEntry, 'followed_at'))),
                    userId = dataEntryUserId,
                    userLogin = utils.getStrFromDict(dataEntry, 'user_id'),
                    userName = utils.getStrFromDict(dataEntry, 'user_name')
                )

        return None

    async def fetchLiveUserDetails(
        self,
        twitchAccessToken: str,
        userNames: List[str]
    ) -> List[TwitchLiveUserDetails]:
        if not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        if not utils.areValidStrs(userNames):
            raise ValueError(f'userNames argument is malformed: \"{userNames}\"')
        if len(userNames) > 100:
            raise ValueError(f'userNames argument has too many values (len is {len(userNames)}, max is 100): \"{userNames}\"')

        userNames.sort(key = lambda userName: userName.lower())
        self.__timber.log('TwitchApiService', f'Fetching live user details... (userNames=\"{userNames}\")')

        userNamesStr = '&user_login='.join(userNames)
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/streams?first=100&user_login={userNamesStr}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching live user details (userNames=\"{userNames}\"): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching when fetching user details (userNames=\"{userNames}\"): {e}')

        responseStatusCode = response.getStatusCode()
        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('TwitchApiService', f'Received a null/empty JSON response when fetching live user details (userNames=\"{userNames}\"): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching live user details (userNames=\"{userNames}\"): {jsonResponse}')
        if responseStatusCode == 401 or ('error' in jsonResponse and len(jsonResponse['error']) >= 1):
            self.__timber.log('TwitchApiService', f'Received an error ({responseStatusCode}) when fetching live user details (userNames=\"{userNames}\"): {jsonResponse}')
            raise TwitchTokenIsExpiredException(f'TwitchApiService received an error ({responseStatusCode}) when fetching live user details (userNames=\"{userNames}\"): {jsonResponse}')
        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching live user details (userNames=\"{userNames}\"): {responseStatusCode}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching live user details (userNames=\"{userNames}\"): {responseStatusCode}')

        data: Optional[List[Dict[str, Any]]] = jsonResponse.get('data')
        users: List[TwitchLiveUserDetails] = list()

        if not utils.hasItems(data):
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
                streamType = TwitchStreamType.fromStr(utils.getStrFromDict(dataEntry, 'type', fallback = ''))
            ))

        users.sort(key = lambda user: user.getUserName().lower())
        return users

    async def fetchModerator(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str
    ) -> Optional[TwitchModUser]:
        if not utils.isValidStr(broadcasterId):
            raise ValueError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        if not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

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

        responseStatusCode = response.getStatusCode()
        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('TwitchApiService', f'Received a null/empty JSON response when fetching moderator ({broadcasterId=}) ({userId=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching moderator ({broadcasterId=}) ({userId=}): {jsonResponse}')
        if responseStatusCode == 401 or ('error' in jsonResponse and len(jsonResponse['error']) >= 1):
            self.__timber.log('TwitchApiService', f'Received an error ({responseStatusCode}) when fetching moderator ({broadcasterId=}) ({userId=}): {jsonResponse}')
            raise TwitchTokenIsExpiredException(f'TwitchApiService received an error ({responseStatusCode}) when fetching moderator ({broadcasterId=}) ({userId=}): {jsonResponse}')
        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching moderator ({broadcasterId=}) ({userId=}): {responseStatusCode}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching moderator ({broadcasterId=}) ({userId=}): {responseStatusCode}')

        data: Optional[List[Dict[str, Any]]] = jsonResponse.get('data')
        if not utils.hasItems(data):
            return None

        return TwitchModUser(
            userId = utils.getStrFromDict(data[0], 'user_id'),
            userLogin = utils.getStrFromDict(data[0], 'user_login'),
            userName = utils.getStrFromDict(data[0], 'user_name')
        )

    async def fetchTokens(self, code: str) -> TwitchTokensDetails:
        if not utils.isValidStr(code):
            raise ValueError(f'code argument is malformed: \"{code}\"')

        self.__timber.log('TwitchApiService', f'Fetching tokens... (code=\"{code}\")')

        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        twitchClientSecret = await self.__twitchCredentialsProvider.getTwitchClientSecret()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = f'https://id.twitch.tv/oauth2/token?client_id={twitchClientId}&client_secret={twitchClientSecret}&code={code}&grant_type=authorization_code&redirect_uri=http://localhost'
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching tokens (code=\"{code}\"): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching tokens (code=\"{code}\"): {e}')

        if response.getStatusCode() != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching tokens (code=\"{code}\"): {response.getStatusCode()}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching tokens (code=\"{code}\"): {response.getStatusCode()}')

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('TwitchApiService', f'Received a null/empty JSON response when fetching tokens (code=\"{code}\"): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching tokens (code=\"{code}\"): {jsonResponse}')
        if 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            self.__timber.log('TwitchApiService', f'Received an error of some kind when fetching tokens (code=\"{code}\"): {jsonResponse}')
            raise TwitchErrorException(f'TwitchApiService received an error of some kind when fetching tokens (code=\"{code}\"): {jsonResponse}')

        expirationTime = await self.__calculateExpirationTime(
            expiresInSeconds = utils.getIntFromDict(jsonResponse, 'expires_in', fallback = -1)
        )

        accessToken = utils.getStrFromDict(jsonResponse, 'access_token', fallback = '')
        if not utils.isValidStr(accessToken):
            self.__timber.log('TwitchApiService', f'Received malformed \"access_token\" ({accessToken}) when fetching tokens (code=\"{code}\"): {jsonResponse}')
            raise TwitchAccessTokenMissingException(f'TwitchApiService received malformed \"access_token\" ({accessToken}) when fetching tokens (code=\"{code}\"): {jsonResponse}')

        refreshToken = utils.getStrFromDict(jsonResponse, 'refresh_token', fallback = '')
        if not utils.isValidStr(refreshToken):
            self.__timber.log('TwitchApiService', f'Received malformed \"refresh_token\" ({refreshToken}) when fetching tokens (code=\"{code}\"): {jsonResponse}')
            raise TwitchRefreshTokenMissingException(f'TwitchApiService received malformed \"refresh_token\" ({refreshToken}) when fetching tokens (code=\"{code}\"): {jsonResponse}')

        return TwitchTokensDetails(
            expirationTime = expirationTime,
            accessToken = accessToken,
            refreshToken = refreshToken
        )

    async def fetchUserDetailsWithUserId(
        self,
        twitchAccessToken: str,
        userId: str
    ) -> Optional[TwitchUserDetails]:
        if not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TwitchApiService', f'Fetching user details... ({userId=})')

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

        if response.getStatusCode() != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching user details ({userId=}): {response.getStatusCode()}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching user details ({userId=}): {response.getStatusCode()}')

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('TwitchApiService', f'Received a null/empty JSON response when fetching user details ({userId=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching user details ({userId=}): {jsonResponse}')
        if 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            self.__timber.log('TwitchApiService', f'Received an error of some kind when fetching user details ({userId=}): {jsonResponse}')
            raise TwitchErrorException(f'TwitchApiService received an error of some kind when fetching user details ({userId=}): {jsonResponse}')

        data: Optional[List[Dict[str, Any]]] = jsonResponse.get('data')

        if not utils.hasItems(data):
            self.__timber.log('TwitchApiService', f'Received a null/empty \"data\" field in JSON response when fetching user details ({userId=}): {jsonResponse}')
            return None

        entry: Optional[Dict[str, Any]] = None

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
            broadcasterType = TwitchBroadcasterType.fromStr(utils.getStrFromDict(entry, 'broadcaster_type')),
            userType = TwitchUserType.fromStr(utils.getStrFromDict(entry, 'type'))
        )

    async def fetchUserDetailsWithUserName(
        self,
        twitchAccessToken: str,
        userName: str
    ) -> Optional[TwitchUserDetails]:
        if not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        userName = userName.lower()
        self.__timber.log('TwitchApiService', f'Fetching user details... ({userName=})')

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
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching user details (userName=\"{userName}\"): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching when fetching user details (userName=\"{userName}\"): {e}')

        if response.getStatusCode() != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching user details (userName=\"{userName}\"): {response.getStatusCode()}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching user details (userName=\"{userName}\"): {response.getStatusCode()}')

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('TwitchApiService', f'Received a null/empty JSON response when fetching user details (userName=\"{userName}\"): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching user details (userName=\"{userName}\"): {jsonResponse}')
        if 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            self.__timber.log('TwitchApiService', f'Received an error of some kind when fetching user details (userName=\"{userName}\"): {jsonResponse}')
            raise TwitchErrorException(f'TwitchApiService received an error of some kind when fetching user details (userName=\"{userName}\"): {jsonResponse}')

        data: Optional[List[Dict[str, Any]]] = jsonResponse.get('data')

        if not utils.hasItems(data):
            self.__timber.log('TwitchApiService', f'Received a null/empty \"data\" field in JSON response when fetching user details (userName=\"{userName}\"): {jsonResponse}')
            return None

        entry: Optional[Dict[str, Any]] = None

        for dataEntry in data:
            if utils.getStrFromDict(dataEntry, 'login').lower() == userName:
                entry = dataEntry
                break

        if entry is None:
            self.__timber.log('TwitchApiService', f'Couldn\'t find entry with matching \"login\" field in JSON response when fetching user details (userName=\"{userName}\"): {jsonResponse}')
            return None

        return TwitchUserDetails(
            displayName = utils.getStrFromDict(entry, 'display_name'),
            login = utils.getStrFromDict(entry, 'login'),
            userId = utils.getStrFromDict(entry, 'id'),
            broadcasterType = TwitchBroadcasterType.fromStr(utils.getStrFromDict(entry, 'broadcaster_type')),
            userType = TwitchUserType.fromStr(utils.getStrFromDict(entry, 'type'))
        )

    async def fetchUserSubscriptionDetails(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str
    ) -> Optional[TwitchUserSubscriptionDetails]:
        if not utils.isValidStr(broadcasterId):
            raise ValueError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        if not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        self.__timber.log('TwitchApiService', f'Fetching user subscription details... (broadcasterId=\"{broadcasterId}\") (userId=\"{userId}\")')

        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/subscriptions?broadcaster_id={broadcasterId}&user_id={userId}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching user subscription details (broadcasterId=\"{broadcasterId}\") (userId=\"{userId}\"): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching when fetching user subscription details (broadcasterId=\"{broadcasterId}\") (userId=\"{userId}\"): {e}')

        if response.getStatusCode() != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching user subscription details (broadcasterId=\"{broadcasterId}\") (userId=\"{userId}\"): {response.getStatusCode()}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching user subscription details (broadcasterId=\"{broadcasterId}\") (userId=\"{userId}\"): {response.getStatusCode()}')

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('TwitchApiService', f'Received a null/empty JSON response when fetching user subscription details (broadcasterId=\"{broadcasterId}\") (userId=\"{userId}\"): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when fetching user subscription details (broadcasterId=\"{broadcasterId}\") (userId=\"{userId}\"): {jsonResponse}')
        if 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            self.__timber.log('TwitchApiService', f'Received an error of some kind when fetching user subscription details (broadcasterId=\"{broadcasterId}\") (userId=\"{userId}\"): {jsonResponse}')
            raise TwitchErrorException(f'TwitchApiService received an error of some kind when fetching user subscription details (broadcasterId=\"{broadcasterId}\") (userId=\"{userId}\"): {jsonResponse}')

        data: Optional[List[Dict[str, Any]]] = jsonResponse.get('data')

        if not utils.hasItems(data):
            self.__timber.log('TwitchApiService', f'Received a null/empty \"data\" field in JSON response when fetching user subscription details (broadcasterId=\"{broadcasterId}\") (userId=\"{userId}\"): {jsonResponse}')
            return None

        entry: Optional[Dict[str, Any]] = None

        for dataEntry in data:
            if dataEntry.get('user_id') == userId:
                entry = dataEntry
                break

        if entry is None:
            self.__timber.log('TwitchApiService', f'Couldn\'t find entry with matching \"user_id\" field in JSON response when fetching user subscription details (broadcasterId=\"{broadcasterId}\") (userId=\"{userId}\"): {jsonResponse}')
            return None

        return TwitchUserSubscriptionDetails(
            isGift = utils.getBoolFromDict(entry, 'is_gift', fallback = False),
            userId = utils.getStrFromDict(entry, 'user_id'),
            userName = utils.getStrFromDict(entry, 'user_name'),
            subscriberTier = TwitchSubscriberTier.fromStr(utils.getStrFromDict(entry, 'tier'))
        )

    async def refreshTokens(self, twitchRefreshToken: str) -> TwitchTokensDetails:
        if not utils.isValidStr(twitchRefreshToken):
            raise ValueError(f'twitchRefreshToken argument is malformed: \"{twitchRefreshToken}\"')

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

        if response.getStatusCode() == 400:
            self.__timber.log('TwitchApiService', f'Encountered HTTP 400 status code when refreshing tokens ({twitchRefreshToken=}): {response.getStatusCode()}')
            raise TwitchPasswordChangedException(f'Encountered HTTP 400 status code when refreshing tokens ({twitchRefreshToken=}): {response.getStatusCode()}')
        if response.getStatusCode() != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when refreshing tokens ({twitchRefreshToken=}): {response.getStatusCode()}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when refreshing tokens ({twitchRefreshToken=}): {response.getStatusCode()}')

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('TwitchApiService', f'Received a null/empty JSON response when refreshing tokens ({twitchRefreshToken=}): {jsonResponse}')
            raise TwitchJsonException(f'TwitchApiService received a null/empty JSON response when refreshing tokens ({twitchRefreshToken=}): {jsonResponse}')
        if 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            self.__timber.log('TwitchApiService', f'Received an error of some kind when refreshing tokens ({twitchRefreshToken=}): {jsonResponse}')
            raise TwitchErrorException(f'TwitchApiService received an error of some kind when refreshing tokens ({twitchRefreshToken=}): {jsonResponse}')

        expirationTime = await self.__calculateExpirationTime(
            expiresInSeconds = utils.getIntFromDict(jsonResponse, 'expires_in', fallback = -1)
        )

        accessToken = utils.getStrFromDict(jsonResponse, 'access_token', fallback = '')
        if not utils.isValidStr(accessToken):
            self.__timber.log('TwitchApiService', f'Received malformed \"access_token\" ({accessToken}) when refreshing tokens ({twitchRefreshToken=}): {jsonResponse}')
            raise TwitchAccessTokenMissingException(f'TwitchApiService received malformed \"access_token\" ({accessToken}) when refreshing tokens ({twitchRefreshToken=}): {jsonResponse}')

        refreshToken = utils.getStrFromDict(jsonResponse, 'refresh_token', fallback = '')
        if not utils.isValidStr(refreshToken):
            self.__timber.log('TwitchApiService', f'Received malformed \"refresh_token\" ({refreshToken}) when refreshing tokens ({twitchRefreshToken=}): {jsonResponse}')
            raise TwitchRefreshTokenMissingException(f'TwitchApiService received malformed \"refresh_token\" ({refreshToken}) when refreshing tokens ({twitchRefreshToken=}): {jsonResponse}')

        return TwitchTokensDetails(
            expirationTime = expirationTime,
            accessToken = accessToken,
            refreshToken = refreshToken
        )

    async def unbanUser(
        self,
        twitchAccessToken: str,
        unbanRequest: TwitchUnbanRequest
    ) -> bool:
        if not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        assert isinstance(unbanRequest, TwitchUnbanRequest), f"malformed {unbanRequest=}"

        self.__timber.log('TwitchApiService', f'Unbanning user... ({twitchAccessToken=}) ({unbanRequest=})')

        clientSession = await self.__networkClientProvider.get()
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        response: Optional[NetworkResponse] = None

        try:
            response = await clientSession.delete(
                url = f'https://id.twitch.tv/helix/moderation/bans?broadcaster_id={unbanRequest.getBroadcasterUserId()}&moderator_id={unbanRequest.getModeratorUserId()}&user_id={unbanRequest.getUserIdToBan()}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when unbanning user ({unbanRequest=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when unbanning user ({unbanRequest=}): {e}')

        if response is None:
            self.__timber.log('TwitchApiService', f'Encountered unknown network error when unbanning user ({unbanRequest=}) ({response=})')
            raise GenericNetworkException(f'TwitchApiService encountered unknown network error when unbanning user ({unbanRequest=}) ({response=})')

        responseStatusCode = response.getStatusCode()
        await response.close()

        if responseStatusCode == 204:
            # means that the given user ID had been banned
            return True
        elif responseStatusCode == 400:
            # probably means that the given user ID had not been banned
            return False

        self.__timber.log('TwitchApiService', f'Encountered network error when unbanning user ({unbanRequest=}) ({response=}): {responseStatusCode}')
        raise GenericNetworkException(f'TwitchApiService encountered network error when unbanning user ({unbanRequest=}) ({response=}): {responseStatusCode}')

    async def validateTokens(self, twitchAccessToken: str) -> Optional[datetime]:
        if not utils.isValidStr(twitchAccessToken):
            raise ValueError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        self.__timber.log('TwitchApiService', f'Validating tokens... ({twitchAccessToken=})')

        clientSession = await self.__networkClientProvider.get()
        response: Optional[NetworkResponse] = None

        try:
            response = await clientSession.get(
                url = 'https://id.twitch.tv/oauth2/validate',
                headers = {
                    'Authorization': f'OAuth {twitchAccessToken}'
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when refreshing tokens ({twitchAccessToken=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when refreshing tokens ({twitchAccessToken=}): {e}')

        responseStatusCode = response.getStatusCode()
        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        clientId: Optional[str] = None
        if jsonResponse is not None and utils.isValidStr(jsonResponse.get('client_id')):
            clientId = utils.getStrFromDict(jsonResponse, 'client_id')

        expiresInSeconds: Optional[int] = None
        if jsonResponse is not None and utils.isValidInt(jsonResponse.get('expires_in')):
            expiresInSeconds = utils.getIntFromDict(jsonResponse, 'expires_in')

        if responseStatusCode != 200 or not utils.isValidStr(clientId) or not utils.isValidInt(expiresInSeconds):
            return None

        nowDateTime = datetime.now(self.__timeZone)
        expiresInTimeDelta = timedelta(seconds = expiresInSeconds)
        expirationTime = nowDateTime + expiresInTimeDelta

        return expirationTime
