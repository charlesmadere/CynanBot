import traceback
from datetime import datetime, timedelta
from typing import Any

from frozenlist import FrozenList

from .jsonMapper.twitchJsonMapperInterface import TwitchJsonMapperInterface
from .models.twitchBanRequest import TwitchBanRequest
from .models.twitchBanResponse import TwitchBanResponse
from .models.twitchBanResponseEntry import TwitchBanResponseEntry
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
from .models.twitchPaginationResponse import TwitchPaginationResponse
from .models.twitchSendChatAnnouncementRequest import TwitchSendChatAnnouncementRequest
from .models.twitchSendChatMessageRequest import TwitchSendChatMessageRequest
from .models.twitchSendChatMessageResponse import TwitchSendChatMessageResponse
from .models.twitchStartCommercialResponse import TwitchStartCommercialResponse
from .models.twitchTokensDetails import TwitchTokensDetails
from .models.twitchUnbanRequest import TwitchUnbanRequest
from .models.twitchUserDetails import TwitchUserDetails
from .models.twitchUserSubscription import TwitchUserSubscription
from .models.twitchValidationResponse import TwitchValidationResponse
from .models.twitchWebsocketConnectionStatus import TwitchWebsocketConnectionStatus
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
                    'Client-Id': twitchClientId,
                    'Content-Type': 'application/json'
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

            frozenEntries: FrozenList[TwitchBanResponseEntry] = FrozenList()
            frozenEntries.append(TwitchBanResponseEntry(
                createdAt = createdAt,
                endTime = endTime,
                broadcasterId = banRequest.broadcasterUserId,
                moderatorId = banRequest.moderatorUserId,
                userId = banRequest.userIdToBan
            ))

            frozenEntries.freeze()

            return TwitchBanResponse(
                data = frozenEntries
            )
        elif responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when banning user ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when banning user ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})'
            )

        banResponse = await self.__twitchJsonMapper.parseBanResponse(jsonResponse)

        if banResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when banning user ({twitchAccessToken=}) ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({banResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when banning user ({twitchAccessToken=}) ({banRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({banResponse=})')

        return banResponse

    async def createEventSubSubscription(
        self,
        twitchAccessToken: str,
        eventSubRequest: TwitchEventSubRequest,
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
                    'Content-Type': 'application/json',
                },
                json = await self.__twitchJsonMapper.serializeEventSubRequest(eventSubRequest),
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=})): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 202:
            self.__timber.log('TwitchApiService', f'Encountered non-202 HTTP status code ({responseStatusCode}) when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-202 HTTP status code ({responseStatusCode}) when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=})'
            )

        eventSubResponse = await self.__twitchJsonMapper.parseEventSubResponse(jsonResponse)

        if eventSubResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({eventSubResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when creating EventSub subscription ({twitchAccessToken=}) ({eventSubRequest=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({eventSubResponse=})')

        return eventSubResponse

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

    async def fetchChannelEmotes(
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
                    'Client-Id': twitchClientId,
                },
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

    async def fetchEventSubSubscriptions(
        self,
        twitchAccessToken: str,
        userId: str,
        pagination: TwitchPaginationResponse | None = None,
        status: TwitchWebsocketConnectionStatus | None = TwitchWebsocketConnectionStatus.ENABLED,
    ) -> TwitchEventSubResponse:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif pagination is not None and not isinstance(pagination, TwitchPaginationResponse):
            raise TypeError(f'pagination argument is malformed: \"{pagination}\"')
        elif status is not None and not isinstance(status, TwitchWebsocketConnectionStatus):
            raise TypeError(f'status argument is malformed: \"{status}\"')

        self.__timber.log('TwitchApiService', f'Fetching EventSub subscriptions... ({twitchAccessToken=}) ({userId=}) ({pagination=}) ({status=})')
        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        queryString = f'user_id={userId}'

        if pagination is not None:
            queryString = f'{queryString}&after={pagination.cursor}'

        if status is not None:
            statusString = await self.__twitchJsonMapper.serializeWebsocketConnectionStatus(status)
            queryString = f'{queryString}&status={statusString}'

        try:
            response = await clientSession.get(
                url = f'https://api.twitch.tv/helix/eventsub/subscriptions?{queryString}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                },
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when fetching EventSub subscriptions ({twitchAccessToken=}) ({userId=}) ({pagination=}) ({status=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when fetching EventSub subscriptions ({twitchAccessToken=}) ({userId=}) ({pagination=}) ({status=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when fetching EventSub subscriptions ({twitchAccessToken=}) ({userId=}) ({pagination=}) ({status=}) ({response=}): {responseStatusCode}')
            raise GenericNetworkException(f'TwitchApiService encountered non-200 HTTP status code when fetching EventSub subscriptions ({twitchAccessToken=}) ({userId=}) ({pagination=}) ({status=}) ({response=}): {responseStatusCode}')

        eventSubResponse = await self.__twitchJsonMapper.parseEventSubResponse(jsonResponse)

        if eventSubResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when fetching EventSub subscriptions ({twitchAccessToken=}) ({userId=}) ({pagination=}) ({status=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({eventSubResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when fetching EventSub subscriptions ({twitchAccessToken=}) ({userId=}) ({pagination=}) ({status=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({eventSubResponse=})')

        return eventSubResponse

    async def fetchFollower(
        self,
        broadcasterId: str,
        twitchAccessToken: str,
        userId: str,
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
                    'Client-Id': twitchClientId,
                },
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

    async def startCommercial(
        self,
        length: int,
        broadcasterId: str,
        twitchAccessToken: str
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

        self.__timber.log('TwitchApiService', f'Starting commercial... ({length=}) ({broadcasterId=}) ({twitchAccessToken=})')

        twitchClientId = await self.__twitchCredentialsProvider.getTwitchClientId()
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.post(
                url = 'https://api.twitch.tv/helix/channels/commercial',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId,
                    'Content-Type': 'application/json'
                },
                json = {
                    'broadcaster_id': broadcasterId,
                    'length': length
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchApiService', f'Encountered network error when starting commercial ({length=}) ({broadcasterId=}) ({twitchAccessToken=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TwitchApiService encountered network error when starting commercial ({length=}) ({broadcasterId=}) ({twitchAccessToken=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200 and responseStatusCode != 429:
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when starting commercial ({length=}) ({broadcasterId=}) ({twitchAccessToken=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when starting commercial ({length=}) ({broadcasterId=}) ({twitchAccessToken=}) ({responseStatusCode=}) ({jsonResponse=})'
            )

        startCommercialResponse = await self.__twitchJsonMapper.parseStartCommercialResponse(jsonResponse)

        if startCommercialResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when starting commercial ({length=}) ({twitchAccessToken=}) ({responseStatusCode=}) ({jsonResponse=}) ({startCommercialResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when starting commercial ({length=}) ({twitchAccessToken=}) ({responseStatusCode=}) ({jsonResponse=}) ({startCommercialResponse=})')

        return startCommercialResponse

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
            self.__timber.log('TwitchApiService', f'Encountered non-200 HTTP status code when validating token ({twitchAccessToken=}) ({responseStatusCode=}) ({jsonResponse=})')
            raise TwitchStatusCodeException(
                statusCode = responseStatusCode,
                message = f'TwitchApiService encountered non-200 HTTP status code when validating token ({twitchAccessToken=}) ({responseStatusCode=}) ({jsonResponse=})'
            )

        validationResponse = await self.__twitchJsonMapper.parseValidationResponse(jsonResponse)

        if validationResponse is None:
            self.__timber.log('TwitchApiService', f'Unable to parse JSON response when validating token ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({validationResponse=})')
            raise TwitchJsonException(f'TwitchApiService unable to parse JSON response when validating token ({twitchAccessToken=}) ({response=}) ({responseStatusCode=}) ({jsonResponse=}) ({validationResponse=})')

        return validationResponse
