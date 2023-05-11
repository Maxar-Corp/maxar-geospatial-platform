import requests
from MGP_SDK import process
from MGP_SDK.auth.auth import Auth


class Usage:

    def __init__(self, auth: Auth):
        self.auth = auth
        self.api_version = self.auth.api_version
        self.base_url = f'{self.auth.api_base_url}/usage/{self.api_version}'
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}

    def check_usage_is_allowed_by_user(self):
        """
        Function determines if usage is allowed for your user
        Returns:
            Message stating if usage is allowed or not
        """

        url = f'{self.base_url}/allowed'
        response = requests.get(url, headers=self.authorization, verify=self.auth.SSL)
        if response.status_code == 200:
            return 'Usage is allowed, credit limit has not been met'
        elif response.status_code == 402:
            return 'Usage is not allowed, credit limit has been met or exceeded'
        else:
            raise Exception("Non-200 response {} received for {}".format(response.status_code, response.url))

    def check_usage_overview(self):
        """
        Shows the overview of usage used for the account the user is tied to
        Returns:
            Dictionary of available products and their usage
        """

        url = f'{self.base_url}/activation/overview'
        response = requests.get(url, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()
