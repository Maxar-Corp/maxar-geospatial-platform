import json

import requests
from MGP_SDK import process
from MGP_SDK.auth.auth import Auth
from datetime import datetime


class Monitoring:

    def __init__(self, auth: Auth):
        self.auth = auth
        self.api_version = self.auth.api_version
        self.base_url = f'{self.auth.api_base_url}/monitoring/{self.api_version}/monitors'
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}

    def create_new_monitor(self, source: str, validate=False, **kwargs):
        """
        Creates a new monitor
        Args:
            source (string) = The ID of the event source to listen to
            validate (bool) = Binary whether to validate tasking request. Defaults to False
        Kwargs:
            start_datetime (string) = ISO-8601-formatted datetime string indicating when the monitor should start
            end_datetime (string) = ISO-8601-formatted datetime string indicating when the monitor should end
            description (string) = A human-friendly description of the monitor
            intersects (dict) = A GeoJSON geometry indicating the area of interest for the monitor
            match_criteria (dict) = the fields and values to match against; criteria are specified using a JSON object
            monitor_notifications (list) = Destination(s) where notifications should be sent
            order_templates (list) = Orders to be placed automatically when an event matches the monitor's criteria
        Returns:
            JSON response
        """

        parameter_list = ['start_datetime', 'end_datetime', 'description', 'aoi_geojson', 'match_criteria',
                          'monitor_notifications', 'order_templates']
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
        data = {**{k: v for k, v in kwargs.items() if k in parameter_list}}
        data.update({"source": source})
        if validate:
            url = self.base_url + "?validation_only=true"
        else:
            url = self.base_url
        response = requests.post(url, data=json.dumps(data), headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_monitor_by_id(self, monitor_id: str):
        """
        Retrieve a monitor configuration for a desired monitor
        Args:
            monitor_id (string) = Identifier assigned to a desired monitor
        Returns:
            Dictionary of the desired monitor's configuration
        """

        url = self.base_url + '/' + monitor_id
        response = requests.get(url, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def toggle_monitor(self, monitor_id: str, status: str):
        """
        Enable or disable a desired monitor
        Args:
            monitor_id (string) = Identifier assigned to a desired monitor
            status (string) = Value to enable or disable a monitor (enable or disable)
        Returns:
            Dictionary of the desired monitor's status
        """

        url = f'{self.base_url}/{monitor_id}/{status}'
        response = requests.post(url, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        if response.status_code == 200:
            return 'Status change accepted'

    def monitor_list(self, **kwargs):
        """
        Retrieves a list of monitor configurations
        Kwargs:
            limit (int) = Number of monitors to return, defaults to 10
            filter (string) |  (string(list)) = Filter results that match values contained in the given key separated by
             a colon. If multiple filters are needed, provide as a list of filters
            sort (string) = asc (default) or desc
        Returns:
            Dictionary of monitor configurations
        Throws:
            ValueError: if limit is not an int and greater than 0.
            Exception: If filter and sort are not formatted properly.
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
                    raise Exception("Filter must be a key value pair separated by a colon (:) " + filter)
        if 'sort' in kwargs.keys():
            if kwargs['sort'] != 'asc' and kwargs['sort'] != 'desc':
                raise Exception('sort must be either asc or desc. ' + kwargs['sort'])
        params = {}
        kwarg_list = ["limit", "filter", "sort"]
        for k, v in kwargs.items():
            if k in kwarg_list:
                params[k] = v
        response = requests.get(self.base_url, params=params, headers=self.authorization, verify=self.auth.SSL)
        # TODO Handle pagination from response
        process._response_handler(response)
        return response.json()

    def monitor_events_list(self, monitor_id: str, **kwargs):
        """
        Retrieves a list of events for a monitor
        Args:
            monitor_id (string) = The ID of the monitor
        Kwargs:
            filter (string) | (string(list)) = Filter results that match values contained in the given key separated by
            a colon. If multiple filters are needed, provide as a list of filters
            sort (string) = asc (default) or desc
        Returns:
            Dictionary of monitors and their events
        Throws:
            Exception: If filter and sort are not formatted properly.
        """

        if 'filter' in kwargs.keys():
            for filter in kwargs['filter']:
                try:
                    k, v = filter.split(":")
                except:
                    raise Exception("Filter must be a kev value pair separated by a colon (:) " + filter)
        if 'sort' in kwargs.keys():
            if kwargs['sort'] != 'asc' and kwargs['sort'] != 'desc':
                raise Exception('sort must be either asc or desc. ' + kwargs['sort'])
        params = {}
        if 'filter' in kwargs.keys():
            params['filter'] = kwargs['filter']
        if 'sort' in kwargs.keys():
            params['sort'] = kwargs['sort']
        if 'limit' in kwargs.keys():
            params['limit'] = kwargs['limit']
        url = f'{self.base_url}/{monitor_id}/events'
        response = requests.get(url, params=params, headers=self.authorization, verify=self.auth.SSL)
        # TODO Handle pagination from response
        process._response_handler(response)
        return response.json()
