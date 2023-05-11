import json
import requests

from MGP_SDK import process
from MGP_SDK.account_service.users import Users
from MGP_SDK.account_service.roles import Roles
from MGP_SDK.account_service.accounts import Info
from MGP_SDK.account_service.activations import Activations
from MGP_SDK.account_service.rate_tables import TableInfo
from MGP_SDK.account_service.addresses import Address
from MGP_SDK.account_service.products import Products
from MGP_SDK.account_service.usage import Usage


import warnings
warnings.filterwarnings("ignore")


class Interface:
    """
    The primary interface for interacting with the Account Services classes.
    Args:
        username (string) = The username if your connectId requires Auth
        password (string) = The password associated with your username
        client_id (string) = The client ID associated with your user
    """

    def __init__(self, auth):
        self.auth = auth
        self.account_info = Info(self.auth)
        self.users = Users(self.auth)
        self.roles = Roles(self.auth)
        self.rate_table_info = TableInfo(self.auth)
        self.address = Address(self.auth)
        self.activations = Activations(self.auth)
        self.products = Products(self.auth)
        self.usage = Usage(self.auth)

    def search(self, search_type, search_term):
        """
        Function searches through the desired search type (ex. account) and lists the details of the search type that
        match the search term
        Args:
            search_type (string) = Desired level to search through. Options are:
                account
                activation
                user
            search_term (string) = Desired search term that searchers through one of the following categories:
                account:
                    account numbers
                    account names
                    SAP license ids
                    sold to
                    licensees
                activation:
                    activation numbers
                    SAP contract identifiers
                    SAP line items
                    start dates
                    end dates
                    account numbers
                    account ids
                user:
                    usernames
                    roles
                    activation numbers
                    account numbers
        Returns:
            Dictionary of the found account(s), activation(s), or user(s)
        """

        if search_type.lower() == "account":
            results = self.account_info.search(search_term)
        elif search_type.lower() == "activation":
            results = self.activations.search(search_term)
        elif search_type.lower() == "user":
            results = self.users.search(search_term)
        else:
            raise Exception("{} is not a valid search type. Please enter a valid search type".format(search_type))
        return results

    def get_self(self):
        """
        Returns information from the account service API about the currently authenticated user

        Returns:
            Dict containing a users account information
        """

        username = self.auth.username
        return self.users.get_users(username=username)

    def toggle_role(self, client_id: str, role: str, action: str):
        """
        Turns all permissions either on or off (action) for every user that is tied to an activation under a given client ID
        if a permission does not exist on that client or if the user is already actioned, it will be skipped

        Args:
            client_id (string) = ID of the client
            role (string) = snake case name of permission
            action (string) = enable or disable
        Returns:
            Dictionary of all of the users under the client activation and their role's status
        """

        all_roles = self.roles.get_roles()
        search_role = role
        client = client_id
        if not (action == 'enable' or action == 'disable'):
            raise Exception('Action must be one of enable or disable')
        found = False
        payload = {}
        for role in all_roles:
            if role['name'] == search_role and role['clientContextId'] == client:
                payload = role
                found = True
                break
        if not found:
            raise Exception("Role not found. Please try again")
        payload['actionToExecute'] = "ADD" if action == 'enable' else 'REMOVE'
        endpoint = 'assignroles' if action == 'enable' else 'removeroles'
        authorization = process.authorization(self.auth)
        all_users = self.users.get_users(pageSize=1000)["users"]
        user_list = {}
        for user in all_users:
            if len(user['activations']) > 0:
                for activation in user["activations"]:
                    if activation["clientContextId"] == client:
                        try:
                            user_id = user['userId']
                            url = f'{self.auth.base_url}/account-service/api/v1/users/{user_id}/{endpoint}'
                            inner_payload = json.dumps([payload])
                            response = requests.request("POST", url, headers=authorization, data=inner_payload,
                                                        verify=self.auth.SSL)
                            process._response_handler(response)
                            user_list[user['username']] = action
                        except:
                            user_list[user['username']] = f'Already {action}d'

        return user_list
