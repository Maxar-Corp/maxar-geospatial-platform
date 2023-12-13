import requests
import MGP_SDK.process as process
from pathlib import Path


class WCS:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = auth.api_base_url + "/deliveryservice/wcsaccess"
        self.response = None
        self.version = auth.version
        self.querystring = self._init_querystring()

    def return_image(self, bbox, identifier, gridoffsets, srsname="EPSG:4326", **kwargs):
        """
        Function finds the imagery matching a bbox or feature id
        Kwargs:
            bbox = String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            filter = CQL filter used to refine data of search.
            gridcrs = String of the Coordinate reference system used. Crs is EPSG:4326.
            gridoffsets = Integer value representing the vertical number of pixels to return
            identifier = String of the feature id to be returned.
            format = String of the format of the response image either jpeg, png or geotiff
            featureprofile = String of the desired stacking profile. Defaults to account Default
        Returns:
            requests response object of desired image
        """
        self.auth.check_token_expiration()
        token = self.auth.refresh_token()
        authorization = {'Authorization': 'Bearer {}'.format(token)}

        self.querystring = self._init_querystring()
        keys = list(kwargs.keys())
        process._validate_bbox(bbox)
        self.querystring.update({'boundingbox': bbox})
        self.querystring.update({'identifier': identifier})
        self.querystring.update({'gridoffsets': gridoffsets})
        if srsname != "EPSG:4326":
            self.querystring['gridcrs'] = "urn:ogc:def:crs:EPSG::{}".format(srsname[5:])
            self.querystring.update({'gridbasecrs': 'urn:ogc:def:crs:EPSG::{}'.format(srsname[5:])})
            bbox_list = [i for i in bbox.split(',')]
            bbox = ",".join([bbox_list[1], bbox_list[0], bbox_list[3], bbox_list[2], bbox_list[4]])
            self.querystring.update({'boundingbox': bbox})
        if 'filter' in keys:
            # process.cql_checker(kwargs['filter'])
            self.querystring.update({'coverage_cql_filter': kwargs['filter']})
            del (kwargs['filter'])
        for key, value in kwargs.items():
            if key in self.querystring.keys():
                self.querystring[key] = value
            else:
                self.querystring.update({key: value})
        request = requests.get(self.base_url, headers=authorization, params=self.querystring, verify=self.auth.SSL)
        self.response = request
        return process._response_handler(self.response)

    def _init_querystring(self):
        querystring = {
                       'service': 'WCS',
                       'request': 'GetCoverage',
                       'version': '1.3.0',
                       'gridcrs': 'urn:ogc:def:crs:EPSG::4326',
                       'format': 'image/jpeg',
                       'SDKversion': '{}'.format(self.version)
                       }
        return querystring

    def parse_coverage(self, coverage):
        writelist = []
        filename = Path(coverage)
        filename_replace_ext = filename.with_suffix('.txt')
        with open(coverage, 'rb') as open_file:
            for line in open_file:
                writelist.append(line)
        writelist1 = writelist[:21]
        writelist2 = writelist[21:]
        with open(filename_replace_ext, 'wb') as write_file:
            for item in writelist1:
                write_file.write(item)
        with open(coverage, 'wb') as write_file:
            for item in writelist2:
                write_file.write(item)
        return (str(filename_replace_ext) + " and " + str(coverage) + " have been downloaded")
