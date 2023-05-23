import json

import requests
import os


class Auth:
    """
    This class handles authentication for the MGP SDK. When a config file is not present the user must pass the args below.
    Please create .MGP-config in home directory. For example: "C:/Users/<user>/.MGP-config"
    MGP-config contents:        [mgp]
                                user_name=username
                                user_password=password
                                client_id=clientID
    """

    def __init__(self, username=None, password=None, client_id=None):
        """
        Function initializes the MGP environment and generates an access and refresh token
        Args:
            username (string) = Username
            password (string) = Password
            client_id (string) = Client ID
        """

        self.base_url = "https://account.maxar.com"
        self.api_base_url = "https://api.maxar.com"
        self.username = username
        self.password = password
        self.client_id = client_id
        self.access = None
        self.refresh = None
        self.version = "Python1.1.1"
        self.api_version = 'v1'
        self.SSL = True

        if not self.username: #checks if username is provided as argument to class. If not, look for .MGP-config
            dir_path = os.path.expanduser('~')
            file = '.MGP-config'
            full_path = os.path.join(dir_path, file)
            if os.path.isfile(full_path):
                self.username, self.password, self.client_id = self._get_environment(full_path)
            else:
                raise ValueError("Please create .MGP-config in home dir.")
        # else:
        #     acceptable_urls = ['https://marianas-test.dev.gcsdev.com']
        #     if self.base_url not in acceptable_urls:
        #         raise ValueError("Base_url must match acceptable SecureWatch 3 URL.")

        #checks for auth when the class is instantiated and assigns tokens to the self.access and self.refresh
        self.refresh_token()

    @staticmethod
    def _get_environment(file):
        """
        Determines tenant and data from config file, passes data into init
        """

        with open(file) as config_file:
            cred_dict = {}
            for line in config_file.readlines():
                if '=' in line:
                    key, value = line.split('=')
                    key = key.strip()
                    value = value.strip()
                    if '\n' in value:
                        value = value.replace('\n', '')
                    cred_dict.update({key: value})
        if 'user_name' not in cred_dict.keys() or 'user_password' not in cred_dict.keys() or 'client_id' not in cred_dict.keys():
            raise Exception('.MGP-config not formatted properly')
        else:
            user_name = cred_dict['user_name']
            password = cred_dict['user_password']
            client_id = cred_dict['client_id']
            return user_name, password, client_id



    def get_auth(self):
        """
        Function generates an access token and refresh token based on a username and password combination
        """

        url = "{}/auth/realms/mds/protocol/openid-connect/token".format(self.base_url)
        payload = 'client_id={}&username={}&password={}&grant_type=password&scope=openid'.format(self.client_id, self.username, self.password)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=self.SSL)
        if response.status_code != 200:
            raise Exception('Unable to connect. Status code equals {}'.format(response.status_code))
        else:
            self.access = response.json()['access_token']
            self.refresh = response.json()['refresh_token']
            return self.access

    def refresh_token(self):
        """
        Function takes in refresh token and generates a new access token and refresh token
        """

        if self.refresh:
            url = "{}/auth/realms/mds/protocol/openid-connect/token".format(self.base_url)

            payload = 'grant_type=refresh_token&refresh_token={}&client_id={}&scope=openid'.format(self.refresh, self.client_id)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.request("POST", url, headers=headers, data=payload, verify=self.SSL)
            if response.status_code == 400 and response.json()['error_description'] == 'Token is not active':
                self.get_auth()
            elif response.status_code != 200:
                raise Exception('Error. Status code = {}'.format(response.status_code))
            else:
                self.access = response.json()['access_token']
                self.refresh = response.json()['refresh_token']
                return self.access
        else:
            self.get_auth()


    def token_service_token(self):
        """
        creates a token service token.
        :return: A dictionary of the token details. If using subset return of this function to ['apiToken'] to authenticate with token.
        """
        url = f"{self.base_url}/token-service/api/{self.api_version}/token"
        headers = {"Authorization": f"Bearer {self.access}",'Content-Type': 'application/json'}
        existing_tokens = requests.request("GET", url, headers=headers)

        def create_token_service_token():
            payload = {
                "name": f"{self.username}_SDK_token",
                "description": "Token service token auto generated for using MGP SDK functionality"
            }
            create_token = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            token = create_token.json()
            return token
        if len(existing_tokens.json()) == 0:
            token = create_token_service_token()
        else:
            tokens = [i for i in existing_tokens.json() if i["name"] is not None and "SDK_token" in i["name"]]
            if len(tokens) == 0:
                token = create_token_service_token()
            else:
                token = existing_tokens.json()[0]
        return token
