import requests
from datetime import datetime
from MGP_SDK import process
from MGP_SDK.auth.auth import Auth


class Collections:

    def __init__(self, auth: Auth):
        self.auth = auth
        self.version = self.auth.version
        self.api_version = self.auth.api_version
        self.base_url = f'{self.auth.api_base_url}/discovery/{self.api_version}/collections'
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}

    def search_stac_in_collection(self, **kwargs):
        """
        The same query parameters may be used as those in the search endpoint, except for "collections" since the
        collection to search is part of the URL path
        Kwargs:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            datetime (string) = Date range filter in format "start-date/end-date" or "exact-datetime"
            ids (list(string)) = Comma-separated list of STAC item IDs to return
            intersects (dict) = GeoJSON geometry to search by
            where (string) = SQL-style where clause for filtering STAC items by properties
            orderby (string) = SQL-style order by clause
            limit (string) = Desired number of items to return
        Returns:
            Dictionary of STAC item and its information
        """
        process.access_token_refresh(self.auth)
        if 'bbox' and 'intersects' in kwargs.keys():
            raise Exception('When performing a spatial search specify either "bbox" or "intersects" not both.')
        if 'datetime' in kwargs.keys():
            try:
                date1, date2 = kwargs['datetime'].split('/')
                datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
                datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
            except:
                try:
                    datetime.strptime(kwargs["datetime"], '%Y-%m-%dT%H:%M:%SZ')
                except:
                    raise Exception('datetime not in ISO 8601 format or date range not separated by a \'/\'')
        if 'orderby' in kwargs.keys():
            if not (kwargs['orderby'] in ['id', 'datetime']):
                raise Exception('orderby can only be used for id and datetime')
        params_list = ['bbox', 'datetime', 'ids', 'intersects', 'where', 'orderby', 'limit']
        params = {**{k: v for k, v in kwargs.items() if k in params_list}}
        url = f'{self.base_url}/{kwargs["collection_id"]}/items'
        response = requests.get(url, params=params, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        response = response.json()

        # pagination
        # if "links" in response.keys():
        #     is_next = response["links"][0]["rel"] == "next"
        #     while is_next:
        #         sub_response = requests.get(url, params=params, headers=self.authorization,
        #                                     verify=self.auth.SSL)
        #         process._response_handler(sub_response)
        #         sub_response = sub_response.json()
        #         response["features"].append(sub_response["features"])
        #         if "links" in sub_response.keys():
        #             is_next = sub_response["links"][0]["rel"] == "next"
        #             url = sub_response["links"][0]["href"]
        #         else:
        #             is_next = False

        return response

    def return_stac_item(self, collection_id: str, item_id: str):
        """
        Function lists a STAC item and its information
        Args:
            collection_id (string) = Identifier of the desired collection
            item_id (string) = Identifier of the desired item
        Returns:
            Dictionary of a STAC item and its information
        """
        process.access_token_refresh(self.auth)
        url = f'{self.base_url}/{collection_id}/items/{item_id}'
        response = requests.get(url, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def search_stac_by_audit_fields(self, collection_id: str, audit_insert_date: str = None,
                                    audit_update_date: str = None, **kwargs):
        """
        Retrieve items for a given collection ID by audit fields
        Args:
            collection_id (string) = Identifier of the desired collection
            audit_insert_date (string) = Desired insert date in ISO-8601 format. Mutually exclusive with auditUpdateDate
            audit_update_date (string) = Desired update date in ISO-8601 format. Mutually exclusive with auditInsertDate
        Kwargs:
            limit (string) = Desired number of items to return
        Returns:
            List of items for given collection ID
        """
        process.access_token_refresh(self.auth)
        if not ((audit_insert_date is None) ^ (audit_update_date is None)):
            raise Exception('Must provide one of audit_insert_date or audit_update_date')
        else:
            if audit_update_date is None:
                date_time = audit_insert_date
                change = 'auditInsertDate'
            else:
                date_time = audit_update_date
                change = 'auditUpdateDate'
        try:
            date1, date2 = date_time.split('/')
            datetime.strptime(date1, '%Y-%m-%dT%H:%M:%SZ')
            datetime.strptime(date2, '%Y-%m-%dT%H:%M:%SZ')
        except:
            try:
                datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%SZ')
            except:
                raise Exception('datetime not in ISO 8601 format or date range not separated by a \'/\'')
        params = {change: date_time}
        if kwargs['limit']:
            params['limit'] = kwargs['limit']
        url = f'{self.base_url}/{collection_id}/audit'
        response = requests.get(url, params=params, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_collection_definition(self, **kwargs):
        """
        Function retrieves a collection definition of a desired collection
        Kwargs:
            collection_id (string) = Identifier of the desired collection
        Returns:
            Collection definition of a desired collection
        """
        process.access_token_refresh(self.auth)
        # endpoint for both host/collections and host/collections:collectionId
        url = self.base_url
        params = {}
        if 'collection_id' in kwargs.keys():
            url = f'{self.base_url}/{kwargs["collection_id"]}'
        else:
            params_list = ['orderby', 'limit', 'page']
            params = {**{k: v for k, v in kwargs.items() if k in params_list}}
        if "limit" in kwargs.keys():
            if isinstance(kwargs['limit'], int):
                if kwargs['limit'] <= 0:
                    raise ValueError('Limit must be greater than 0')
            else:
                raise ValueError('Limit must be an int')

        response = requests.get(url, params=params, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        response = response.json()
        # pagination
        # if "limit" not in kwargs.keys():
        #     is_next = response["links"][0]["rel"] == "next"
        #     while is_next:
        #         sub_response = requests.get(url, params=params, headers=self.authorization,
        #                                     verify=self.auth.SSL)
        #         process._response_handler(sub_response)
        #         sub_response = sub_response.json()
        #         response["collections"].append(sub_response["collections"])
        #         if "links" in sub_response.keys():
        #             is_next = sub_response["links"][0]["rel"] == "next"
        #             url = sub_response["links"][0]["href"]
        #         else:
        #             is_next = False

        return response
    
