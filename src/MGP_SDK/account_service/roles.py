import requests
import MGP_SDK.process as process


class Roles:

    def __init__(self, auth):
        self.base_url = auth.api_base_url
        self.response = None
        self.version = auth.version
        self.auth = auth

    def get_roles(self, **kwargs):
        """
        Function lists all roles
        Returns:
            List of dictionaries of roles and their details
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + "/account-service/api/v1/roles"
        params = {}
        for key, value in kwargs.items():
            params[key] = value
        response = requests.request("GET", url, headers=authorization, params=params, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_user_types(self):
        """
        Function lists all available user types
        Returns:
            List of available user types
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + "/account-service/api/v1/roles/usertypes"
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()
