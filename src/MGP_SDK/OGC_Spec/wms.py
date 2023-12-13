import requests
import MGP_SDK.process as process
from MGP_SDK.auth.auth import Auth


class WMS:
    def __init__(self, auth: Auth, endpoint):
        self.auth = auth
        self.version = auth.version
        self.api_version = auth.api_version
        self.endpoint = endpoint
        if self.endpoint == 'streaming':
            self.base_url = f'{self.auth.api_base_url}/streaming/{self.api_version}/ogc/ows'
        elif self.endpoint == 'basemaps_seamlines':
            self.base_url = f'{self.auth.api_base_url}/basemaps/{self.api_version}/seamlines/ows'
        elif self.endpoint == 'basemaps_ogc':
            self.base_url = f'{self.auth.api_base_url}/basemaps/{self.api_version}/ogc/ows'
        elif self.endpoint == 'vector':
            self.base_url = f'{self.auth.api_base_url}/analytics/{self.api_version}/vector/change-detection/Maxar/ows'
        # TODO Handle raster endpoint
        self.querystring = self._init_querystring(None)
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}

    def return_image(self, **kwargs):
        """
        Function finds the imagery matching a bbox or feature id
        Kwargs:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            filter (string) = CQL filter used to refine data of search.
            height (int) = The vertical number of pixels to return
            width (int) = The horizontal number of pixels to return
            layers (string) = The desired layer. Defaults to 'DigitalGlobe:Imagery'
            format (string) = The desired format of the response image either jpeg, png or geotiff
            featureprofile (string) = The desired stacking profile. Defaults to account Default
        Returns:
            requests response object of desired image
        """
        process.access_token_refresh(self.auth)
        layers = kwargs['layers'] if 'layers' in kwargs.items() else None
        querystring = self._init_querystring(layers)
        querystring.update({'format': kwargs['format']})
        keys = list(kwargs.keys())
        if 'bbox' in keys:
            process._validate_bbox(kwargs['bbox'], srsname=kwargs['srsname'])
            if kwargs['srsname'] == "EPSG:4326":
                bbox_list = kwargs['bbox'].split(',')
                kwargs['bbox'] = ",".join([bbox_list[0], bbox_list[1], bbox_list[2], bbox_list[3]])
            else:
                bbox_list = [i for i in kwargs['bbox'].split(',')]
                kwargs['bbox'] = ",".join([bbox_list[1], bbox_list[0], bbox_list[3], bbox_list[2]])
                querystring['crs'] = kwargs['srsname']
            querystring.update({'bbox': kwargs['bbox']})
        else:
            raise Exception('Search function must have a BBOX.')
        if 'filter' in keys:
            process.cql_checker(kwargs['filter'], endpoint=self.endpoint, token=self.token)
            querystring.update({'cql_filter': kwargs['filter']})
            del (kwargs['filter'])
        if 'request' in keys:
            if kwargs['request'] == 'GetCapabilities':
                querystring.update({'request': kwargs['request']})
                for item in kwargs.keys():
                    del kwargs[item]
        for key, value in kwargs.items():
            querystring[key] = value
        request = requests.get(self.base_url, headers=self.authorization, params=querystring, verify=self.auth.SSL)
        return process._response_handler(request)

    def _init_querystring(self, layers):
        if layers is None:
            if self.endpoint == 'streaming' or self.endpoint == 'basemaps_ogc':
                layers = 'Maxar:Imagery'
            elif self.endpoint == 'basemaps_seamlines':
                layers = 'Maxar:seamline'
            # TODO Handle raster / vector
        querystring = {'service': 'WMS',
                       'request': 'GetMap',
                       'version': '1.3.0',
                       'transparent': 'true',
                       'crs': 'EPSG:4326',
                       'height': '512',
                       'width': '512',
                       'layers': layers,
                       'format': 'image/jpeg',
                       'tiled': 'true',
                       'SDKversion': '{}'.format(self.version)
                       }
        return querystring
    