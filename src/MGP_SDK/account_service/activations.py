import requests
import MGP_SDK.process as process


class Activations:

    def __init__(self, auth):
        self.base_url = auth.api_base_url
        self.response = None
        self.version = auth.version
        self.auth = auth

    def search(self, search):
        """
        Function searches through all activations and lists activations that match the search term
        Args:
            search (string) = Search term. Searches through activation numbers, SAP contract identifiers, SAP line items,
            start dates, end dates, account numbers, and account ids
        Returns:
            Dictionary of the found activation or activations
        """
        process.access_token_refresh(self.auth)
        authorization = process.authorization(self.auth)
        url = self.base_url + '/account-service/api/v1/activations?search={}'.format(search)
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        if len(response.json()["activations"]) < 1:
            raise Exception("No search results for {}. Please try another search term".format(search))
        return response.json()

    def get_activations(self, activation_id=None, activation_number=None, **kwargs):
        """
        Get all activations or activation by Id.
        Args:
            activation_id (int): Desired activation ID
            activation_number (string): Desired activation number
        Returns:
            Dictionary of all or desired activation(s) and their details
        """
        process.access_token_refresh(self.auth)
        authorization = process.authorization(self.auth)
        if activation_id:
            url = self.base_url + '/account-service/api/v1/activations/{}'.format(activation_id)
        elif activation_number:
            url = self.base_url + '/account-service/api/v1/activations/number/{}'.format(activation_number)
        else:
            url = self.base_url + '/account-service/api/v1/activations'
        params = {}
        for key, value in kwargs.items():
            params[key] = value
        response = requests.request("GET", url, headers=authorization, params=params, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_activations_for_account(self, account_id):
        """
        Gets activations for an account
        Args:
            account_id (int): Desired account ID
        Returns:
            Dictionary of desired activation and its details
        """
        process.access_token_refresh(self.auth)
        authorization = process.authorization(self.auth)
        url = self.base_url + '/account-service/api/v1/activations/available?accountId={}'.format(account_id)
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_activation_credit_limit(self, activation_number):
        """
        Gets the credit limit for a desired activation
        Args:
            activation_number (string) = Desired activation number
        Returns:
            Dictionary of the desired activation's credit details
        """
        process.access_token_refresh(self.auth)
        authorization = process.authorization(self.auth)
        url = self.base_url + '/account-service/api/v1/activations/number/{}/credit'.format(activation_number)
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_activation_types(self):
        """
        Gets all activation types
        Returns:
            Dictionary of all activation types
        """
        process.access_token_refresh(self.auth)
        authorization = process.authorization(self.auth)
        url = self.base_url + '/account-service/api/v1/activations/types'
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()
    
