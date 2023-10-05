import requests
import json
from datetime import datetime
from MGP_SDK import process
from MGP_SDK.auth.auth import Auth


class Search:

    def __init__(self, auth: Auth):
        self.auth = auth
        self.version = self.auth.version
        self.api_version = self.auth.api_version
        self.base_url = f'{self.auth.api_base_url}/discovery/{self.api_version}/search'
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}

    def stac_search_with_filtering(self, **kwargs):
        """
        Retrieve items matching filters
        Kwargs:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            datetime (string) = Date range filter in format "start-date/end-date" or "exact-datetime"
            ids (list(string)) = Comma-separated list of STAC item IDs to return
            intersects (dict) = GeoJSON geometry to search by
            where (string) = SQL-style where clause for filtering STAC items by properties
            orderby (string) = SQL-style order by clause
            limit (string) = Desired number of items to return
        Returns:
            GeoJSON feature collection
        """

        if 'bbox' in kwargs.keys() and 'intersects' in kwargs.keys():
            if kwargs['bbox'] != None and kwargs['intersects'] != None:
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
        params_list = ['bbox', 'datetime', 'ids', 'collections', 'intersects', 'where', 'orderby', 'limit']
        params = {**{k: v for k, v in kwargs.items() if k in params_list}}
        if 'intersects' in params:
            if type(params['intersects']) == bytes:
                pass
            else:
                params['intersects'] = json.dumps(params['intersects']).encode('utf-8')
        url = self.base_url
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
        #             params.clear()
        #             url = sub_response["links"][0]["href"]
        #         else:
        #             is_next = False
        return response
