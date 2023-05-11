import requests
from MGP_SDK import process
from MGP_SDK.auth.auth import Auth
from MGP_SDK.account_service import users
from datetime import datetime


class Orders:

    def __init__(self, auth: Auth):
        self.auth = auth
        self.api_version = self.auth.api_version
        self.base_url = self.auth.api_base_url + f"/ordering/{self.api_version}/orders"
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}
        self.users = users.Users(self.auth)

    def get_order_details(self, order_id: str):
        """
        Gets the IDs of all Orders that match the search criteria and the user can access.
        Args:
            order_id (string) = The ID of the order you are trying to get the details of
        Returns:
            JSON response
        """

        url = f"{self.base_url}/{order_id}"
        response = requests.get(url, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_order_events_by_id(self, order_id: str, **kwargs):
        """
        Get staus events for an order
        Args:
            order_id (string) = The identifier assigned to the order
        Kwargs:
            limit (int) = Limits the number of responses returned
            filter (list) = Filter results that match values contained in the given key separated by a colon
        Returns:
            Dictionary of order events for a desired order
        """

        if 'limit' in kwargs.keys():
            try:
                int(kwargs['limit'])
                assert kwargs['limit'] > 0
            except:
                raise ValueError("Limit must be an integer greater than 0. Limit provided: " + kwargs['limit'])
        if 'filter' in kwargs.keys():
            for filter in kwargs['filter']:
                try:
                    k, v = filter.split(":")
                except:
                    raise Exception("Filter must be a kev value pair separated by a colon (:) " + filter)
        kwarg_list = ["limit", "filter"]
        params = {**{k: v for k, v in kwargs.items() if k in kwarg_list}}
        url = f"{self.base_url}/{order_id}/events"
        response = requests.get(url, params=params, headers=self.authorization, verify=self.auth.SSL)
        # TODO Handle pagination from response
        process._response_handler(response)
        return response.json()

    def get_orders_by_user_id(self, user_id: str, **kwargs):
        """
        List orders for a specific user
        Args:
            user_id (string) = The identifier of the desired user
        Kwargs:
            limit (int) = Limits the number of responses returned
            filter (list) = Filter results that match values contained in the given key separated by a colon
            sort (string) = Indicates sort order, desc (default) for descending order (newest first) and asc for
            ascending order (oldest first)
            start_date (string) = ISO-8601 formatted date after which to query orders (inclusive)
            end_date (string) = ISO-8601 formatted date before which to query orders (inclusive)
        Returns:
            Dictionary of orders from a desired user
        """

        if 'limit' in kwargs.keys():
            try:
                int(kwargs['limit'])
                assert kwargs['limit'] > 0
            except:
                raise ValueError("Limit must be an integer greater than 0. Limit provided: " + kwargs['limit'])
        if 'filter' in kwargs.keys():
            for filter in kwargs['filter']:
                try:
                    k, v = filter.split(":")
                except:
                    raise Exception("Filter must be a kev value pair separated by a colon (:) " + filter)
        if 'sort' in kwargs.keys():
            if kwargs['sort'] is not 'asc' or kwargs['sort'] is not 'desc':
                raise Exception('sort must be either asc or desc. ' + kwargs['sort'])
        if 'start_date' in kwargs.keys():
            try:
                datetime_string = datetime.fromisoformat(kwargs['start_date'])
            except:
                raise Exception('Date is not properly formatted. eg: 2023-03-03T10:30:00.000Z')
        if 'end_date' in kwargs.keys():
            try:
                datetime_string = datetime.fromisoformat(kwargs['end_date'])
            except:
                raise Exception('Date is not properly formatted. eg: 2023-03-03T10:30:00.000Z')
        if user_id is None:
            user_id = self.users.get_users(username=self.auth.username)['userId']
        url = f"{self.base_url}/user/{user_id}"
        kwarg_list = ["limit", "filter", "sort", "start_date", "end_date"]
        params = {**{k: v for k, v in kwargs.items() if k in kwarg_list}}
        response = requests.get(url, params=params, headers=self.authorization, verify=self.auth.SSL)
        # TODO Handle pagination from response
        process._response_handler(response)
        return response.json()

    def cancel_order_by_id(self, order_id: str):
        """
        Cancel a desired order if the pipeline allows for cencellation
        Args:
            order_id (string) = The identifier given to the order
        Returns:
            Dictionary of desired order's status
        """

        url = f"{self.base_url}/{order_id}/cancel"
        response = requests.post(url, headers=self.authorization, verify=self.auth.SSL)
        error_message = "Pipeline does not support order cancellation"
        if response.status_code == 400 and response.json()['error']['error_messages'][0] == error_message:
            raise Exception(error_message)
        else:
            process._response_handler(response)
            return response.json()
