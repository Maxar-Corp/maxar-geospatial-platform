import MGP_SDK.process as process
from MGP_SDK.auth.auth import Auth
import requests


def _combine_bbox_and_filter(querystring, filter, bbox, endpoint):
    geometry = ''
    if endpoint == 'streaming' or endpoint == 'basemaps_ogc':
        geometry = 'featureGeometry'
    elif endpoint == 'basemaps_seamlines':
        geometry = 'seamline_geometry'
    # TODO handle raster / vector
    bbox_geometry = f'BBOX({geometry},{bbox})'
    combined_filter = bbox_geometry + 'AND' + '(' + filter + ')'
    querystring.update({'cql_filter': combined_filter})
    return querystring


class WFS:

    def __init__(self, auth: Auth, endpoint):
        self.auth = auth
        self.version = self.auth.version
        self.api_version = self.auth.api_version
        self.endpoint = endpoint
        if self.endpoint == 'streaming':
            self.base_url = f'{self.auth.api_base_url}/streaming/{self.api_version}/ogc/wfs'
        elif self.endpoint == 'basemaps_seamlines':
            self.base_url = f'{self.auth.api_base_url}/basemaps/{self.api_version}/seamlines/wfs'
        elif self.endpoint == 'basemaps_ogc':
            self.base_url = f'{self.auth.api_base_url}/basemaps/{self.api_version}/ogc/wfs'
        elif self.endpoint == 'vector':
            self.base_url = f'{self.auth.api_base_url}/analytics/{self.api_version}/vector/change-detection/Maxar/ows'
        # TODO Handle raster endpoint
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}

    def search(self, typename=None, srsname='EPSG:4326', **kwargs):
        """
        Function searches using the wfs method.
        Args:
            typename (string) = Desired typename. Defaults to 'FinishedFeature'
        Kwargs:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            filter (string) = CQL filter used to refine data of search.
            outputformat (string) = Desired format of the response object. Defaults to json.
            featureprofile (string) = Desired stacking profile. Defaults to account Default
            typename (string) = Desired typename. Defaults to FinishedFeature
            srsname (string) = Desired projection. Defaults to EPSG:4326
        Returns:
            Response object of the search
        """

        querystring = self._init_querystring(typename)
        keys = list(kwargs.keys())
        if 'filter' in keys and kwargs['filter']:
            process.cql_checker(kwargs['filter'])
            if 'bbox' in keys and kwargs['bbox']:
                if srsname == "EPSG:4326":
                    process._validate_bbox(kwargs['bbox'], srsname=srsname)
                    querystring = _combine_bbox_and_filter(querystring, kwargs['filter'], kwargs['bbox'], self.endpoint)
                    del (kwargs['filter'])
                    del (kwargs['bbox'])
                else:
                    process._validate_bbox(kwargs['bbox'], srsname=srsname)
                    bbox_list = [i for i in kwargs['bbox'].split(',')]
                    querystring['srsname'] = srsname
                    srsname = "'" + srsname + "'"
                    kwargs['bbox'] = ",".join([bbox_list[1], bbox_list[0], bbox_list[3], bbox_list[2], srsname])
                    querystring = _combine_bbox_and_filter(querystring, kwargs['filter'], kwargs['bbox'], self.endpoint)
                    del (kwargs['filter'])
                    del (kwargs['bbox'])
            else:
                if not srsname:
                    querystring['srsname'] = "EPSG:4326"
                else:
                    querystring['srsname'] = srsname
                querystring.update({'cql_filter': kwargs['filter']})
                del (kwargs['filter'])
        elif kwargs['bbox']:
            process._validate_bbox(kwargs['bbox'], srsname=srsname)
            if srsname == "EPSG:4326":
                bbox_list = [i for i in kwargs['bbox'].split(',')]
                kwargs['bbox'] = ",".join([bbox_list[0], bbox_list[1], bbox_list[2], bbox_list[3]])
            else:
                bbox_list = [i for i in kwargs['bbox'].split(',')]
                kwargs['bbox'] = ",".join([bbox_list[1], bbox_list[0], bbox_list[3], bbox_list[2], srsname])
                querystring['srsname'] = srsname
        elif 'request' in keys:
            if kwargs['request'] == 'DescribeFeatureType' or kwargs['request'] == 'GetCapabilities':
                querystring.update({'request': kwargs['request']})
                del (kwargs['filter'])
                del (kwargs['bbox'])
                del (querystring['outputformat'])
        else:
            raise Exception('Search function must have a BBOX or a Filter.')
        for key, value in kwargs.items():
            querystring[key] = value
        query_string = process._remove_cache(querystring)
        response = requests.get(self.base_url, headers=self.authorization, params=query_string, verify=self.auth.SSL)
        return process._response_handler(response)

    def _init_querystring(self, typename):
        if typename is None:
            if self.endpoint == 'streaming' or self.endpoint == 'basemaps_ogc':
                typename = 'Maxar:FinishedFeature'
            elif self.endpoint == 'basemaps_seamlines':
                typename = 'seamline'
            # TODO Handle raster / vector
        querystring = {
            'service': 'WFS',
            'request': 'GetFeature',
            'typeNames': typename,
            'version': '2.0.0',
            'srsname': 'EPSG:4326',
            'outputFormat': 'application/json',
            'SDKversion': '{}'.format(self.version),
        }
        return querystring
