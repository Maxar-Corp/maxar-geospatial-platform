import requests
from MGP_SDK import process
from MGP_SDK.auth.auth import Auth


class Basemaps:

    def __init__(self, auth: Auth):
        self.auth = auth
        self.version = self.auth.version
        self.api_version = self.auth.api_version
        self.base_url = f'{self.auth.api_base_url}/contentservice/api/{self.api_version}/basemaps'
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}

    def get_available_basemaps(self):
        """
        Gets a list of available basemaps that a user is authorized to view.
        Returns:
            JSON response
        """

        response = requests.get(self.base_url, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_basemap_details(self, basemap_id: str):
        """
        Gets the general content detail for authorized content for the given id
        Returns:
            JSON response
        """

        url = f'{self.base_url}/id/{basemap_id}'
        response = requests.get(url, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()
