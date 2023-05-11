import requests
from MGP_SDK import process
from MGP_SDK.auth.auth import Auth


class ServerChecks:

    def __init__(self, auth: Auth):
        self.auth = auth
        self.api_version = self.auth.api_version
        self.base_url = self.auth.api_base_url + f'/discovery/{self.api_version}/'
        self.version = self.auth.version
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}

    def send_check(self, **kwargs):
        """
        View the service's status
        Kwargs:
            conformance (string) = Endpoint is conformance
            healthcheck (string) = Endpoint is healthcheck
            status (string) = Endpoint is status
        Returns:
            Dictionary of desired endpoint's details
        """

        param_list = ['conformance', 'healthcheck', 'status']
        endpoint = ''
        if 'endpoint' in kwargs.keys() and kwargs['endpoint'] in param_list:
            endpoint = kwargs['endpoint']
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()
