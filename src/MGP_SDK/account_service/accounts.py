import requests
import MGP_SDK.process as process


class Info:

    def __init__(self, auth):
        self.auth = auth
        self.base_url = auth.api_base_url
        self.response = None
        self.version = auth.version

    def search(self, search):
        """
        Function searches through all accounts and lists accounts that match the search term
        Args:
            search (string) = Search term. Searches through account numbers, account names, SAP license ids, sold to,
            and licensees
        Returns:
            Dictionary of the found account or accounts
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/account-service/api/v1/accounts?search={}'.format(search)
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        if len(response.json()["accounts"]) < 1:
            raise Exception("No search results for {}. Please try another search term".format(search))
        return response.json()

    def get_accounts(self, account_id=None, account_name=None, id_names=False, types=False, **kwargs):
        """
        Function lists a single account, a list of accounts, or account types and their details
        Args:
            account_id (int) = ID of the desired account. Defaults to None
            account_name (string) = Name of the desired account. Defaults to None
            id_names (bool) = Binary for short list of account IDs and account names. Defaults to False
            types (bool) = Binary for list of all account types. Defaults to False
        Returns:
            Dictionary of account details, list of accounts and their details, or account types and their details
        """

        authorization = process.authorization(self.auth)
        if account_id:
            url = self.base_url + '/account-service/api/v1/accounts/{}'.format(account_id)
        elif account_name:
            url = self.base_url + '/account-service/api/v1/accounts/name/{}'.format(account_name)
        elif id_names:
            url = self.base_url + '/account-service/api/v1/accounts/idnames'
        elif types:
            url = self.base_url + '/account-service/api/v1/accounts/types'
        else:
            url = self.base_url + '/account-service/api/v1/accounts'
        params = {}
        for key, value in kwargs.items():
            params[key] = value
        response = requests.request("GET", url, headers=authorization, params=params, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_roles(self):
        """
        Function lists all roles available for accounts
        Returns:
            Dictionary of all roles available for accounts
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/account-service/api/v1/roles/'
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_comment(self, account_id):
        """
        Function lists all comments and their details for an account
        Args:
            account_id (int) = ID of the desired account
        Returns:
            Dictionary of all comments and their details for a desired account
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/account-service/api/v1/accounts/{}/comments'.format(account_id)
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        if len(response.text) < 1:
            return {
                "id": "0",
                "accountId": account_id,
                "message": "No comments available"
            }
        else:
            return response.json()
