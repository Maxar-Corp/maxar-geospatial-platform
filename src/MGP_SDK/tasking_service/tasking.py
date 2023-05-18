import json

import requests
from datetime import datetime
from MGP_SDK import process
from MGP_SDK.auth.auth import Auth


class Tasking:

    def __init__(self, auth: Auth):
        self.auth = auth
        self.api_version = self.auth.api_version
        self.base_url = f'{self.auth.api_base_url}/tasking/{self.api_version}/tasking'
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}

    def create_new_tasking(self, start_datetime: str, end_datetime: str, aoi_geojson: dict, recipe: str,
                           order_templates: dict, validate=False, **kwargs):
        """
        Make a tasking request based on imagery recipes
        Args:
            start_datetime (string) = ISO-8601 formatted date when the tasking should start
            end_datetime (string) = ISO-8601 formatted date when the tasking should end
            aoi_geojson (dict) = Geojson polygon of area to cover with tasking, e.g.
            {"type":"Polygon","coordinates":[[[...]]]}
            recipe (string) = The name of one of the configured recipes for tasking, e.g. "50cm_Color" or "30cm_Color"
            order_templates (dict) = Template for order to be placed. See ordering_service for examples
            validate (bool) = Binary whether to validate tasking request. Defaults to False
        Kwargs:
            max_cloud_cover (string) = Maximum cloud cover.
            max_off_nadir_angle (string) = Maximum off nadir angle.
            max_sun_elevation_angle (string) = Maximum sun elevation angle.
        Returns:
            Dictionary of submitted tasking request's details
        """

        time_check = [start_datetime, end_datetime]
        for time in time_check:
            try:
                datetime.fromisoformat(time.replace('Z', '+00:00'))
            except:
                raise ValueError(f'{time} is not in a proper format. Example: 2020-07-10T15:00:00+00:00')
        if recipe is not '50cm_Color':
            if recipe is not '30cm_color':
                raise Exception('Recipe must be one of 50cm_Color or 30cm_Color')
        else:
            payload = {
                'start_datetime': start_datetime,
                'end_datetime': end_datetime,
                'aoi_geojson': aoi_geojson,
                'recipe': recipe,
                'order_templates': order_templates
            }
            optional_parameters = ['max_cloud_cover', 'max_off_nadir_angle', 'min_sun_elevation_angle']
            data = {**{k: v for k, v in kwargs.items() if k in optional_parameters}, **payload}
            if validate:
                url = self.base_url + "?validation_only=true"
            else:
                url = self.base_url
            response = requests.post(url, data=json.dumps(data), headers=self.authorization,
                                     verify=self.auth.SSL)
            process._response_handler(response)
            return response.json()

    def cancel_tasking(self, tasking_id: str, reason: str = None):
        """
        Cancels a tasking request
        args:
            tasking_id (string) = ID of the requested tasking
            reason (string) = Reason for canceling the tasking
        Returns:
            Dictionary of cancelled tasking request's details
        """

        payload = {}
        if reason:
            payload['reason'] = reason
        url = f'{self.base_url}/{tasking_id}/cancel'
        response = requests.post(url, json=payload, headers=self.authorization,
                                 verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_tasking_list(self, **kwargs):
        """
        List all tasking requests
        Kwargs:
            limit (int) = How many items to return in the response list. Default 10
            filter (list) = Filter results that match values contained in the given key separated by a colon.
            sort (string) = Indicates sort order, asc (default) for ascending order (alphabetical by name) and desc for
            descending order (reverse alphabetical by name)
        Returns:
            Dictionary of tasking requests and their details
        """

        optional_parameters = ['limit', 'filter', 'sort']
        params = {**{k: v for k, v in kwargs.items() if k in optional_parameters}}
        response = requests.get(self.base_url, headers=self.authorization, params=params, verify=self.auth.SSL)
        # TODO handle pagination
        process._response_handler(response)
        return response.json()

    def tasking_info(self, tasking_id: str):
        """
        Retrieves the details of a tasking request
        Args:
            tasking_id (string) = ID of the requested tasking
        Returns:
            Dictionary of a tasking request and its details
        """

        url = self.base_url + '/' + tasking_id
        response = requests.get(url, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()



