import requests
from datetime import datetime
from MGP_SDK import process
from MGP_SDK.auth.auth import Auth


class Catalogs:

    def __init__(self, auth: Auth):
        self.auth = auth
        self.version = self.auth.version
        self.api_version = self.auth.api_version
        self.base_url = f'{self.auth.api_base_url}/discovery/{self.api_version}'
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}

    def get_top_level_sub_catalog(self, **kwargs):
        """
        View the available Maxar Sub-Catalogs that can be navigated as a self-contained STAC catalog
        Kwargs:
            orderby (string) = SQL-style order by clause
            limit (string) = Desired number of collections to return
        Returns:
            Dictionary of available Sub-Catalogs
        """
        process.access_token_refresh(self.auth)
        url = f'{self.base_url}/catalogs'
        kwargs_list = ['orderby', 'limit']
        if "orderby" in kwargs.keys():
            if kwargs['orderby'] not in ['id', 'id asc', 'id desc', 'datetime', 'datetime asc', 'datetime desc']:
                raise Exception('ordeby must be one of id or datetime with optional asc or desc modifiers. EG: id desc')
        params = {**{k: v for k, v in kwargs.items() if k in kwargs_list}}
        response = requests.get(url, params=params, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_sub_catalog_definition(self, sub_catalog_id: str):
        """
        View the definition of a Maxar Sub-Catalog
        Args:
            sub_catalog_id (string) = Desired identifier (name) of a specific collection
        Returns:
            Dictionary of definitions of a Sub-Catalog
        """
        process.access_token_refresh(self.auth)
        url = f'{self.base_url}/catalogs/{sub_catalog_id}'
        response = requests.get(url, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_sub_catalog_collections(self, sub_catalog_id: str, **kwargs):
        """
        List the collections that belong to a Sub-Catalog
        Args:
            sub_catalog_id (string) = Desired identifier (name) of a specific collection
        Kwargs:
            orderby (string) = SQL-style order by clause
            limit (string) = Desired number of collections to return
        Returns:
            Dictionary of collections that belong to a Sub-Catalog
        """
        process.access_token_refresh(self.auth)
        url = f'{self.base_url}/catalogs/{sub_catalog_id}/collections'
        kwargs_list = ['orderby', 'limit']
        if "orderby" in kwargs.keys():
            if kwargs['orderby'] not in ['id', 'id asc', 'id desc', 'datetime', 'datetime asc', 'datetime desc']:
                raise Exception('orderby must be one of id or datetime with optional asc or desc modifiers. EG: id desc')
        params = {**{k: v for k, v in kwargs.items() if k in kwargs_list}}
        response = requests.get(url, params=params, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_collection_in_sub_catalog(self, sub_catalog_id: str, collection_id: str):
        """
        View the definition of a collections that belongs to a Sub-Catalog
        Args:
            sub_catalog_id (string) = Desired identifier (name) of a specific collection
            collection_id (string) = Identifier of the desired collection
        Returns:
            Dictionary of definitions of desired collection that belongs to a Sub-Catalog
        """
        process.access_token_refresh(self.auth)
        url = f'{self.base_url}/catalogs/{sub_catalog_id}/collections/{collection_id}'
        response = requests.get(url, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_sub_catalog_stac_item(self, sub_catalog_id: str, collection_id: str, item_id: str):
        """
        Get a STAC item in a sub-catalog's collection
        Args:
            sub_catalog_id (string) = Desired identifier (name) of a specific collection
            collection_id: (string) = Identifier of the desired collection
            item_id (string) = Identifier of the desired item
        Returns:
            Dictionary of the desired STAC item in a sub-catalog's collection
        """
        process.access_token_refresh(self.auth)
        url = f'{self.base_url}/catalogs/{sub_catalog_id}/collections/{collection_id}/items/{item_id}'
        response = requests.get(url, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def search_stac_in_sub_catalog_or_collection(self, endpoint: str, **kwargs):
        """
        Retrieve items matching filters in a sub-catalog
        Args:
            endpoint (string) = Desired endpoint (search or items). Defaults to items
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
        url = f'{self.base_url}/catalogs/{kwargs["sub_catalog_id"]}/search' if endpoint == 'search' else \
            f'{self.base_url}/catalogs/{kwargs["sub_catalog_id"]}/collections/{kwargs["collection_id"]}/items'
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
    

