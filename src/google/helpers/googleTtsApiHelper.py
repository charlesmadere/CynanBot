import base64
import binascii
import traceback
from typing import Final

from .googleTtsApiHelperInterface import GoogleTtsApiHelperInterface
from ..apiService.googleApiServiceInterface import GoogleApiServiceInterface
from ..exceptions import GoogleCloudProjectIdUnavailableException
from ..models.googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class GoogleTtsApiHelper(GoogleTtsApiHelperInterface):

    def __init__(
        self,
        googleApiService: GoogleApiServiceInterface,
        timber: TimberInterface
    ):
        if not isinstance(googleApiService, GoogleApiServiceInterface):
            raise TypeError(f'googleApiService argument is malformed: \"{googleApiService}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__googleApiService: Final[GoogleApiServiceInterface] = googleApiService
        self.__timber: Final[TimberInterface] = timber

    async def getSpeech(
        self,
        request: GoogleTextSynthesizeRequest
    ) -> bytes | None:
        if not isinstance(request, GoogleTextSynthesizeRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        try:
            response = await self.__googleApiService.textToSpeech(request)
        except (GenericNetworkException, GoogleCloudProjectIdUnavailableException) as e:
            self.__timber.log('GoogleTtsApiHelper', f'Failed to fetch Google text to speech ({request=}): {e}', e, traceback.format_exc())
            return None

        try:
            return base64.b64decode(
                s = response.audioContent,
                validate = True
            )
        except binascii.Error as e:
            self.__timber.log('GoogleTtsApiHelper', f'Unable to decode base64 string into bytes due to bad characters ({request=}) ({response=}): {e}', e, traceback.format_exc())
            return None
