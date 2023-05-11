import json

import requests
from MGP_SDK import process
from MGP_SDK.auth.auth import Auth


class Pipelines:

    def __init__(self, auth: Auth):
        self.auth = auth
        self.api_version = self.auth.api_version
        self.base_url = f'{self.auth.api_base_url}/ordering/{self.api_version}/pipelines'
        self.token = self.auth.refresh_token()
        self.authorization = {'Authorization': f'Bearer {self.token}'}

    def get_pipeline(self, namespace: str, name: str):
        """
        Get the schema for a specific pipeline
        Args:
            namespace (string) = A group of pipelines (e.g. 'Imagery')
            name (string) = Name of the pipeline to order from (e.g. 'analysis-ready')
        Returns:
            Dictionary schema of a specific pipeline
        """

        url = f"{self.base_url}/{namespace}/{name}"
        response = requests.get(url, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def post_order_or_get_estimate(self, namespace: str, name: str, settings: dict, output_config: dict, endpoint: str,
                                   metadata: dict, **kwargs):
        """
        Place an order or validate an order request before placing it
        Args:
            namespace (string) =  A group of pipelines (e.g. 'Imagery')
            name (string) = Name of the pipeline to order from (e.g. 'analysis-ready')
            settings (dict) = Settings specific to this pipeline. (required if the requested pipeline requires
            user-provided input parameters and has a json_schema attribute)
            output_config (dict) = Delivery configuration. Amazon S3, Google Cloud Storage, Azure Blob storage
            are supported.
            endpoint (string) = Desired endpoint (order or validate)
            metadata (dict) = Supplemental information to attach to this order
        Kwargs:
            notifications (list(dict)) = Desired notification type (e.g. 'email'), target (e.g. 'email-address'), and
            level (e.g. 'INITIAL_FINAL')
            metadata (dict) = Supplemental information to attch to this order
        :return:
        """

        kwarg_list = ['notifications', 'metadata']
        data = {**{k: v for k, v in kwargs.items() if k in kwarg_list}, **settings, **output_config, **metadata}
        if endpoint == 'order':
            if 'validate' in kwargs.keys() and kwargs['validate']:
                endpoint = 'validate'
            else:
                endpoint = 'order'
        elif endpoint == 'estimate':
            endpoint = 'estimate'
        url = f"{self.base_url}/{namespace}/{name}/{endpoint}"
        response = requests.post(url, data=json.dumps(data), headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()
