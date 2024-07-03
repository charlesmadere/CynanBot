import traceback

from .jishoHelperInterface import JishoHelperInterface
from ..jisho.jishoApiServiceInterface import JishoApiServiceInterface
from ..jisho.jishoPresenterInterface import JishoPresenterInterface
from ..misc import utils as utils
from ..network.exceptions import GenericNetworkException
from ..timber.timberInterface import TimberInterface


class JishoHelper(JishoHelperInterface):

    def __init__(
        self,
        jishoApiService: JishoApiServiceInterface,
        jishoPresenter: JishoPresenterInterface,
        timber: TimberInterface
    ):
        if not isinstance(jishoApiService, JishoApiServiceInterface):
            raise TypeError(f'jishoApiService argument is malformed: \"{jishoApiService}\"')
        elif not isinstance(jishoPresenter, JishoPresenterInterface):
            raise TypeError(f'jishoPresenter argument is malformed: \"{jishoPresenter}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__jishoApiService: JishoApiServiceInterface = jishoApiService
        self.__jishoPresenter: JishoPresenterInterface = jishoPresenter
        self.__timber: TimberInterface = timber

    async def search(self, query: str) -> list[str]:
        if not utils.isValidStr(query):
            raise TypeError(f'query argument is malformed: \"{query}\"')

        try:
            response = await self.__jishoApiService.search(query)
        except GenericNetworkException as e:
            self.__timber.log('JishoHelper', f'Encountered network error when searching Jisho ({query=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'JishoHelper encountered network error when searching Jisho ({query=}): {e}')

        return await self.__jishoPresenter.toStrings(
            includeRomaji = False,
            jishoResponse = response
        )
