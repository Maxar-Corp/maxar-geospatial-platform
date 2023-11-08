import requests
import json
import MGP_SDK.process as process
import MGP_SDK.account_service.roles as account_roles


class Users:

    def __init__(self, auth):
        self.base_url = auth.api_base_url
        self.response = None
        self.version = auth.version
        self.auth = auth

    def search(self, search):
        """
        Function searches through all users and lists users that match the search term
        Args:
            search (string) = Search term. Searches through usernames, roles, activation numbers, and account numbers
        Returns:
            Dictionary of the found user or users
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + '/account-service/api/v1/users?search={}'.format(search)
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        if len(response.json()["users"]) < 1:
            raise Exception("No search results for {}. Please try another search term".format(search))
        return response.json()

    def get_users(self, user_id=None, username=None, **kwargs):
        """
        Function lists a users details
        Args:
            user_id (string) = Identifier of the desired user. Defaults to None
            username (string) = Username of the desired user. Defaults to None
        Kwargs:
            pageSize (int) = Desired number of users returned
            page (int) = Desired starting page for pagination (0 is first page)
        Returns:
            Dictionary of the desired user's details
        """

        authorization = process.authorization(self.auth)
        if user_id:
            url = self.base_url + "/account-service/api/v1/users/{}".format(user_id)
        elif username:
            url = self.base_url + "/account-service/api/v1/users/username/{}".format(username)
        else:
            url = self.base_url + "/account-service/api/v1/users"
        params = {}
        for key, value in kwargs.items():
            params[key] = value
        response = requests.request("GET", url, headers=authorization, params=params, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def update_user(self, user_id, **kwargs):
        """
        Function updates requested user based on payload. Payload can be retrieved using GetUsers function and then edited.
        Args:
            user_id (string) = Identifier of the desired user
        Kwargs:
            username (string) = Desired username for the updated user
            firstName (string) = Desired first name for the updated user
            lastName (string) = Desired last name for the updated user
            phone (string) = Desired phone number for the updated user
        Returns:
            Dictionary of the updated user's details
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + "/account-service/api/v1/users"
        payload = self.get_users(user_id)
        for item in kwargs.keys():
            payload.update({item: kwargs[item]})
        payload = json.dumps(payload)
        response = requests.request("PUT", url, headers=authorization, data=payload, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def create_user(self, user_type, account_id, activation_id, email_address, first_name, last_name, country,
                    client_id='mgp', **kwargs):
        """
        Function accepts payload for new user and returns response JSON of created user.
        Args:
            user_type (string) = Desired user level
            account_id (int) = Identifier of the desired account
            activation_id (int) = Identifier of the desired activation
            email_address (string) = Desired email address for the new user
            first_name (string) = Desired first name for the new user
            last_name (string) = Desired last name for the new user
            country (string) = Desired country of origin for the new user
            client_id (string) = Name of the associated client. Defaults to mgp
        Returns:
            Dictionary of the created user's details
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + "/account-service/api/v1/users/{}".format(client_id)

        payload = {"notifySuspension": False,
                   "userType": user_type,
                   "accountId": account_id,
                   "activations": [{"id": activation_id}],
                   "emailAddress": email_address,
                   "firstName": first_name,
                   "lastName": last_name,
                   "country": country,
                   "phone": '',
                   "isActive": True}

        for item in kwargs.keys():
            payload.update({item: kwargs[item]})

        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=authorization, data=payload, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def update_user_roles(self, user_id, roles_to_update, client_id="b4e8d573-56ee-4e79-abcd-7b161f93ea17", delete=False):
        """
        Args:
            user_id (string) = Identifier of the desired user
            roles_to_update (list(string)) = Desired roles to update
            client_id (string) = Desired client id
            delete (bool) = Binary value for deletion. Defaults to False
        Returns:
            Dictionary of the updated user roles or response object of the deleted role(s)
        """

        authorization = process.authorization(self.auth)
        if type(roles_to_update) != list:
            raise Exception('rolesToUpdate must be a list')

        #use the roles class to create list of all roles
        # role_list = account_roles.Roles.get_roles(self)
        role_list = self.get_user_available_roles(user_id, client_id)
        # roleList = roleClass.GetRoles()
        role_array = []
        if delete:
            action = "REMOVE"
        else:
            action = "ADD"

        #loop through roles you want to add
        for i in range(len(roles_to_update)):
            #loop through all available roles
            for role in role_list:
                if role['name'] == roles_to_update[i]:
                    id = role['id']
                    role_array.append(
                        {"id": id, "name": role['name'], "clientContextId": client_id, "actionToExecute": action}
                    )

        #Check if it found all the roles you wanted to add
        # if len(roles_to_update) != len(role_array):
        #     raise Exception('One or more selected roles not available for this user.')
        payload = json.dumps(role_array)

        if not delete:
            url = self.base_url + "/account-service/api/v1/users/{}/assignroles".format(user_id)
            response = requests.request("POST", url, headers=authorization, data=payload, verify=self.auth.SSL)
            process._response_handler(response)
            return response.json()
        else:
            url = self.base_url + "/account-service/api/v1/users/{}/removeroles".format(user_id)
            response = requests.request("POST", url, headers=authorization, data=payload, verify=self.auth.SSL)
            process._response_handler(response)
            return response


    def get_user_roles(self, user_id, **kwargs):
        """
        Finds the roles a user has.
        Args:
            user_id (string) = Identifier of the desired user
        Returns:
            Dictionary of the roles and their details assigned to a specified user
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + "/account-service/api/v1/users/roles/assigned/{}".format(user_id)
        params = {}
        for key, value in kwargs.items():
            params[key] = value
        response = requests.request("GET", url, headers=authorization, params=params, verify=self.auth.SSL)
        process._response_handler(response)
        if response.status_code == 204:
            return {}
        else:
            return response.json()

    def get_user_available_roles(self, user_id, client_id="b4e8d573-56ee-4e79-abcd-7b161f93ea17"):
        """
        Finds the roles available for a user to have.
        Args:
            user_id (string) = Identifier of the desired user
            client_id (string) = Desired client id
        Returns:
            Dictionary of the roles and their details that a user has the ability to be assigned
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + "/account-service/api/v1/users/roles/assigned-available/{}?clientContextId={}".format(
            user_id, client_id)
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def delete_user(self, user_id):
        """
        Deletes a user
        Args:
            user_id (string) = Identifier of the desired user
        Returns:
            Message of successful deletion
        """

        authorization = process.authorization(self.auth)
        url = self.base_url + "/account-service/api/v1/users?userId={}".format(user_id)
        response = requests.request("DELETE", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return "User {} successfully deleted".format(user_id)
