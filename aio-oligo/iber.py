from aiohttp import ClientSession


class ResponseException(Exception):
    pass


class LoginException(Exception):
    pass


class SessionException(Exception):
    pass


class NoResponseException(Exception):
    pass


class SelectContractException(Exception):
    pass


class Iber:
    __domain = "https://www.i-de.es"
    __login_url = __domain + "/consumidores/rest/loginNew/login"
    __watthourmeter_url = __domain + "/consumidores/rest/escenarioNew/obtenerMedicionOnline/24"
    __icp_status_url = __domain + "/consumidores/rest/rearmeICP/consultarEstado"
    __contracts_url = __domain + "/consumidores/rest/cto/listaCtos/"
    __contract_detail_url = __domain + "/consumidores/rest/detalleCto/detalle/"
    __contract_selection_url = __domain + "/consumidores/rest/cto/seleccion/"
    __headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/77.0.3865.90 Chrome/77.0.3865.90 Safari/537.36",
        'accept': "application/json; charset=utf-8",
        'content-type': "application/json; charset=utf-8",
        'cache-control': "no-cache"
    }

    def __init__(self):
        self.__session = None

    async def login(self, username, password):
        """
        Login to the I+D platform.

        :param username: I+D login email
        :param password: I+D login password
        """
        self.__session = ClientSession()
        login_data = "[\"{}\",\"{}\",null,\"Linux -\",\"PC\",\"Chrome 77.0.3865.90\",\"0\",\"\",\"s\"]".format(username,
                                                                                                               password)
        async with self.__session.post(self.__login_url, data=login_data) as response:
            if response.status != 200:
                self.__session = None
                raise ResponseException(f'Response error, code: {response.status}')
            json_response = await response.json()
            if not json_response['success']:
                self.__session = None
                raise LoginException('Login error')

    def __check_session(self):
        """
        Checks for the existence of a client session.
        """
        if not self.__session:
            raise SessionException('Please, login first')

    async def __check_response(self, response):
        """
        Checks for valid server responses.

        :param response: :class:`aiohttp.ClientResponse` response object
        """
        if response.status != 200:
            self.__session = None
            raise ResponseException
        json_response = await response.json()
        if not json_response:
            raise NoResponseException
        return json_response

    async def watthourmeter(self):
        """
        Get the current energy reading.

        :return: Current watt/hour reading
        """
        self.__check_session()
        async with self.__session.get(self.__watthourmeter_url, headers=self.__headers) as response:
            json_response = await self.__check_response(response)
            return json_response['valMagnitud']

    async def icpstatus(self):
        """
        Get the current ICP status.

        :return: True if connected, False if disconnected
        """

        self.__check_session()
        async with self.__session.post(self.__icp_status_url, headers=self.__headers) as response:
            json_response = await self.__check_response(response)
            if json_response['icp'] == 'trueConectado':
                return True
            else:
                return False

    async def contracts(self):
        """
        Get user's contracts.

        :return: User's contracts in JSON format
        """
        async with self.__session.get(self.__contracts_url, headers=self.__headers) as response:
            json_response = await self.__check_response(response)
            if json_response['success']:
                return json_response['contratos']

    async def contract_details(self):
        """
        Get current contract details.

        :return: Contract details in JSON format
        """
        async with self.__session.get(self.__contract_detail_url, headers=self.__headers) as response:
            json_response = await self.__check_response(response)
            if json_response['success']:
                return json_response['contratos']

    async def contractselect(self, id):
        """
        Choose current contract by selecting it by contract id (codContrato).

        :param id: Contract code (codContrato)
        """
        async with self.__session.get(self.__contract_selection_url + id, headers=self.__headers) as response:
            json_response = await self.__check_response(response)
            if not json_response['success']:
                raise SelectContractException
