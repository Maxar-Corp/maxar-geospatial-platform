import json
import requests
import MGP_SDK.process as process
import warnings
warnings.filterwarnings("ignore")

class Token:

    def __init__(self, auth):
        self.base_url = auth.api_base_url
        self.auth = auth

    def get_user_tokens(self):
        """
        Gets a list of all tokens associated with your user
        Returns:
            Dictionary of all tokens for your user
        """
        process.access_token_refresh(self.auth)
        authorization = process.authorization(self.auth)
        url = "{}/token-service/api/v2/token".format(self.base_url)
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def create_token_record(self, name=None, description=None):
        """
        Creates a new token to utilize in place of an OAuth token
        Args:
            name (string) = Desired name for the new token
            description (string) = Desired description for the new token
        Returns:
            Dictionary of the newly created token and its details
        """
        process.access_token_refresh(self.auth)
        authorization = process.authorization(self.auth)
        url = "{}/token-service/api/v2/token".format(self.base_url)
        payload = {
            "name": name,
            "description": description
        }
        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=authorization, data=payload, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def delete_tokens(self, token):
        """
        Deletes one or more tokens for one or more ids. Pass either a string of a token id to delete a single token or
        pass a list of strings of token ids to delete multiple tokens at once
        Args:
            token (string) | (list(string)) Desired token(s) id
        Return:
            Message of successful deletion
        """
        process.access_token_refresh(self.auth)
        authorization = process.authorization(self.auth)
        if type(token) == str:
            url = "{}/token-service/api/v2/token/id/{}".format(self.base_url, token)
            response = requests.request("DELETE", url, headers=authorization,verify=self.auth.SSL)
        elif type(token) == list:
            url = "{}/token-service/api/v2/token".format(self.base_url)
            payload = json.dumps({"ids": token})
            response = requests.request("DELETE", url, headers=authorization, data=payload,verify=self.auth.SSL)
        else:
            raise Exception('Please pass either a string of the token ID or a list of strings of token ids to delete')
        process._response_handler(response)
        if response.status_code == 200:
            return "Token {} successfully deleted".format(token)
        else:
            return "Token not deleted, response code of {} received".format(response.status_code)
    
