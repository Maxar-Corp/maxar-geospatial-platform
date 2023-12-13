import requests
import MGP_SDK.process as process


class TableInfo:

    def __init__(self, auth):
        self.base_url = auth.api_base_url
        self.response = None
        self.version = auth.version
        self.auth = auth

    def get_table(self, table_id=None):
        """
        Function lists either all rate tables and their details or a single rate table and its details
        Args:
            table_id (int) = Id of the desired rate table. Defaults to None
        Returns:
             Dictionary of all tables and their details or a single table and its details
        """
        process.access_token_refresh(self.auth)
        authorization = process.authorization(self.auth)
        if table_id:
            url = self.base_url + '/account-service/api/v1/ratetables/{}'.format(table_id)
        else:
            url = self.base_url + '/account-service/api/v1/ratetables'
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_activations_for_table(self, table_id):
        """
        Function lists all activations associated with a specific rate table
        Args:
            table_id (int) = Id of the desired rate table
        Returns:
            Dictionary of a list of all activations associated with the given rate table
        """
        process.access_token_refresh(self.auth)
        authorization = process.authorization(self.auth)
        url = self.base_url + '/account-service/api/v1/ratetables/{}/activations'.format(table_id)
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_credit_types(self):
        """
        Function lists all available credit types
        Returns:
            List of dictionaries of available credit types
        """
        process.access_token_refresh(self.auth)
        authorization = process.authorization(self.auth)
        url = self.base_url + '/account-service/api/v1/ratetables/credittypes'
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_rate_amounts(self, table_id):
        """
        Function lists all rate amounts for a desired rate table
        Args:
            table_id (int) = Id of the desired rate table
        Returns:
            List of all rate amounts and their details for the specified rate table
        """
        process.access_token_refresh(self.auth)
        authorization = process.authorization(self.auth)
        url = self.base_url + '/account-service/api/v1/ratetables/{}/productCredits'.format(table_id)
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_rate_tables_and_associated_activations(self):
        """
        Function lists all rate tables and their products and the activations that have access to the tables
        Returns:
            List of dictionaries of rate tables and their associated products
        """
        process.access_token_refresh(self.auth)
        authorization = process.authorization(self.auth)
        url = self.base_url + '/account-service/api/v1/ratetables/activationNumbers'
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()
    
