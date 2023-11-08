import os
import warnings

import requests
from pyproj import Transformer
import shapely.ops as ops
from shapely.geometry.polygon import Polygon
import shapely.geometry
import shapely.wkt
import random
import string
import queue
from concurrent.futures import ThreadPoolExecutor
from MGP_SDK.auth import auth
from datetime import datetime
import xml.etree.ElementTree as ET
from shapely.validation import make_valid


def authorization(auth_class=None):
    if auth_class:
        token = auth_class.refresh_token()
        auth_dict = {'Authorization': 'Bearer {}'.format(token), 'content-type': 'application/json'}
    else:
        auth_class = auth.Auth()
        token = auth_class.refresh_token()
        auth_dict = {'Authorization': 'Bearer {}'.format(token), 'content-type': 'application/json'}
    return auth_dict

def _response_handler(response):
    """
    Function takes in the server response code and responds accordingly.
    Returns:
        Requests response object of server status
    """

    if response.status_code == 200 or response.status_code == 201 or response.status_code == 204 or \
            response.status_code == 202:
        return response
    elif 'Exception' in response.text:
        raise Exception(response.url, response.text)
    else:
        raise Exception(
            "Non-200 response {} received for {} \n{}".format(response.status_code, response.url, response.text)
        )
    # if response.status_code != 200:
    #     raise Exception("Non-200 response received for {}.".format(response.url))
    # elif 'Exception' in response.text:
    #     raise Exception(response.url, response.text)
    # else:
    #     return response


def area_sqkm(bbox, srsname="EPSG:4326"):
    """
    Function takes in the bbox and calculates the area in SQKM.
    Args:
        bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
    Returns:
        Float value of area in SQKM
    """

    _validate_bbox(bbox)
    bboxlst = bbox.split(',')
    ymin = float(bboxlst[0])
    ymax = float(bboxlst[2])
    xmin = float(bboxlst[1])
    xmax = float(bboxlst[3])

    if srsname == "EPSG:4326":

        geom = Polygon([(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)])
        transformer = Transformer.from_crs(
                "EPSG:4326",
                f"+proj=aea +lat_1={geom.bounds[1]} +lat_2={geom.bounds[3]}",
                always_xy=True)

        geom_area = ops.transform(
            transformer.transform,
            geom)

    else:

        geom = Polygon([(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin), (xmin, ymin)])
        transformer = Transformer.from_crs(
                srsname,
                f"+proj=aea +lat_1={geom.bounds[1]} +lat_2={geom.bounds[3]}",
                always_xy=True)

        geom_area = ops.transform(
            transformer.transform,
            geom)

    # Print the area in sqkm^2

    geomareasqkm = geom_area.area/(10**6)
    return geomareasqkm


def _display_image(image):
    """
    Function takes in the response object and displays it.
    Args:
        image (response) = response object from wms method
    """

    try:
        import IPython.display as disp
        from IPython.display import Image, display
    except:
        raise Exception('Must have IPython installed to display.')
    display(disp.Image(image.content))

def _validate_bbox(bbox, srsname="EPSG:4326"):
    """
    Function takes in the bbox and validates that it is proper format
    Args:
        bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
        srsname (string) = Desired projection. Defaults to EPSG:4326
    """

    bbox_list = bbox.split(',')
    if len(bbox_list) > 4:
        raise Exception('Bbox must contain exactly 4 coordinates')
    if srsname == "EPSG:4326":
        try:
            bbox_data = {'min_y': float(bbox_list[0]), 'min_x': float(bbox_list[1]), 'max_y': float(bbox_list[2]),
                         'max_x': float(bbox_list[3])}
        except:
            raise Exception('Bbox coordinates must be numeric.')
        if bbox_data['min_y'] >= bbox_data['max_y']:
            raise Exception("Improper order of bbox: min_y is greater than max_y.")
        if bbox_data['min_x'] >= bbox_data['max_x']:
            raise Exception("Improper order of bbox: min_x is greater than max_x.")

        if [bbox_data[i] for i in bbox_data.keys() if '_y' in i if bbox_data[i] > 90 or bbox_data[i] < -90]:
            if [bbox_data[i] for i in bbox_data.keys() if '_x' in i if bbox_data[i] > 180 or bbox_data[i] < -180]:
                raise Exception(
                    "Improper bbox parameter: {} coordinate outside of range -90:90 and {} outside of range -180:180.".format(
                        (bbox_list[0], bbox_list[2]), (bbox_list[1], bbox_list[3])))
            else:
                raise Exception("Improper bbox parameter: {} coordinate outside of range -90:90.".format(
                    (bbox_list[0], bbox_list[2])))
        elif [bbox_data[i] for i in bbox_data.keys() if '_x' in i if bbox_data[i] > 180 or bbox_data[i] < -180]:
            raise Exception("Improper bbox parameter: {} coordinate outside of range -180:180.".format(
                (bbox_list[1], bbox_list[3])))
    else:
        try:
            bbox_data = {'min_y': float(bbox_list[0]), 'min_x': float(bbox_list[1]), 'max_y': float(bbox_list[2]),
                         'max_x': float(bbox_list[3])}
        except:
            raise Exception(
                "Bbox coordinates must be numeric")
        if bbox_data['min_y'] >= bbox_data['max_y']:
            raise Exception("Improper order of bbox: min_y is greater than max_y.")
        if bbox_data['min_x'] >= bbox_data['max_x']:
            raise Exception("Improper order of bbox: min_x is greater than max_x.")

        if [bbox_data[i] for i in bbox_data.keys() if '_y' in i if bbox_data[i] > 20048966.1 or bbox_data[i] <
                                                                   -20048966.1]:
            if [bbox_data[i] for i in bbox_data.keys() if '_x' in i if bbox_data[i] > 20037508.34 or bbox_data[i] <
                                                                       -20037508.34]:
                raise Exception(
                    "Improper bbox parameter: {} coordinate outside of range -20048966.1:20048966.1 and {} outside "
                    "of range -20037508.34:20037508.34.".format((bbox_list[0], bbox_list[2]), (bbox_list[1],
                                                                                               bbox_list[3])))
            else:
                raise Exception("Improper bbox parameter: {} coordinate outside of range "
                                "-20048966.1:20048966.1".format((bbox_list[0], bbox_list[2])))
        elif [bbox_data[i] for i in bbox_data.keys() if '_x' in i if bbox_data[i] > 20037508.34 or bbox_data[i] <
                                                                     -20037508.34]:
            raise Exception("Improper bbox parameter: {} coordinate outside of range "
                            "-20037508.34:20037508.34.".format((bbox_list[1], bbox_list[3])))

def download_file(response, format_response=None, download_path=None):
    """
    Function downloads response to local machine
    Args:
        response (dict) = Response object
        format_response (string) = File type
        download_path (string) = Desired download path location on local machine
    Returns:
        String of download path location on local machine
    """

    if download_path:
        filename = download_path
    else:
        filename = 'Download.' + format_response
        filename = os.path.join(os.getcwd(), filename)
    if os.path.isfile(filename):
        while os.path.isfile(filename):
            filename = os.path.join(os.path.split(filename)[0], os.path.split(filename)[1].split('.')[0] + '_dup.' +
                                    os.path.split(filename)[1].split('.')[1])
    with open(filename, 'wb') as output_file:
        output_file.write(response.content)

    return filename

def _remove_cache(querystring):
    """
    Function assigns random characters to bypass caching
    Args:
        querystring (dict) = The desired query
    Returns:
        Dictionary of updated query string with random characters
    """

    pool_list = string.digits + string.ascii_letters
    random_characters1 = ''.join(i for i in random.choices(pool_list, k=25))
    random_characters2 = ''.join(i for i in random.choices(pool_list, k=25))
    querystring.update({random_characters1:random_characters2})
    return querystring

def aoi_coverage(bbox, response):
    """
    Function adds the percentage of the desired feature that is covered by the AOI
    Args:
        bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
        response (response) = Object from a WFS request call
    Returns:
        Updated dictionary of the json object
    """

    coverage = response.json()
    box_order = bbox.split(',')
    aoi_polygon = shapely.geometry.box(
        *(float(box_order[1]), float(box_order[0]), float(box_order[3]), float(box_order[2])), ccw=True)
    for feature in coverage['features']:
        try:
            if feature['geometry']['type'] == 'Polygon':
                feature_wkt = shapely.wkt.loads("POLYGON (({}))".format(
                    ", ".join([" ".join([str(k) for k in i]) for i in feature['geometry']['coordinates'][0]])))
                feature['coverage'] = aoi_polygon.intersection(feature_wkt).area / feature_wkt.area
                feature['bbox_coverage'] = feature_wkt.intersection(aoi_polygon).area / aoi_polygon.area
            else:
                feature_wkt = shapely.wkt.loads("MULTIPOLYGON ({})".format(", ".join(
                    ["(({}))".format(", ".join([" ".join([str(k) for k in i]) for i in l[0]])) for l in
                     feature['geometry']['coordinates']])))
                feature['coverage'] = aoi_polygon.intersection(feature_wkt).area / feature_wkt.area
                feature['bbox_coverage'] = feature_wkt.intersection(aoi_polygon).area / aoi_polygon.area
        except:
            continue
    return coverage

def _check_image_format(img_format):
    """
    Function checks image format given for each call
    Args:
        img_format (string) = Desired image format
    Returns:
        String of image format with 'image/' preceding to comply with Maxar API calls
    """

    acceptable_format = ['jpeg', 'png', 'geotiff',"geotiff8", "gif","svg+xml", "tiff","tiff8","vnd.jpeg-png","vnd.jpeg-png8"]
    if img_format in acceptable_format:
        return 'image/' + img_format
    else:
        raise Exception('Format not recognized, please use acceptable format for downloading image.')

def _check_typeName(typename):
    acceptable_types = ['FinishedFeature', 'TileMatrixFeature', 'ImageInMosaicFeature', 'MaxarCatalogMosaicProducts',
                        'MaxarCatalogMosaicSeamlines', 'MaxarCatalogMosaicTiles']
    if typename not in acceptable_types:
        raise Exception('{} is not an acceptable TypeName. Please use one of the following {}'.format(typename, acceptable_types))


def cql_checker(cql_filter, endpoint='endpoint', token='token'):
    """
    Function checks for the validity of a passed in cql filter
    Args:
        cql_filter (string) = Representation of cql filter
    """

    # get available filters from DescribeFeatureType
    xsd = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
    valid_filters_dict = {}

    base_url = 'https://api.maxar.com/'
    if endpoint == 'streaming':
        base_url += 'streaming/v1/ogc/ows'
    elif endpoint == 'basemaps_seamlines':
        base_url += 'basemaps/v1/seamlines/wfs'
    elif endpoint == 'basemaps_ogc':
        base_url += 'basemaps/v1/ogc/wfs'
    elif endpoint == 'vector':
        base_url += 'analytics/v1/vector/change-detection/Maxar/ows'

    auth_header = {"Authorization": f"Bearer {token}"}
    query_string = {'service': 'WFS', 'request': 'DescribeFeatureType', 'version': '2.0.0'}

    response = requests.request("GET", base_url, headers=auth_header, params=query_string,
                                verify=True)
    _response_handler(response)
    response = response.text

    feature_type = ET.fromstring(response)
    tag = []

    if endpoint == 'streaming' or endpoint == 'basemaps_ogc':
        tag = feature_type.find(".//xsd:complexType[@name='FinishedFeatureType']//xsd:sequence", xsd)
        tag.append(feature_type.find(".//xsd:complexType[@name='RasterFeatureType']//xsd:sequence", xsd))
    elif endpoint == 'basemaps_seamlines':
        tag = feature_type.find(".//xsd:complexType[@name='seamlineType']//xsd:sequence", xsd)
    elif endpoint == 'vector':
        tag = feature_type.find(".//xsd:complexType[@name='layer_pcm_eo_1985Type']//xsd:sequence", xsd)

    for element in tag.findall('xsd:element', xsd):
        key = element.get('type').split(":")[1]
        value = element.get('name')
        if key in valid_filters_dict:
            valid_filters_dict[key].append(value)
        else:
            valid_filters_dict[key] = [value]

    source_list = ["'WV01'", "'WV02'", "'WV03_VNIR'", "'WV03'", "'WV04'", "'GE01'", "'QB02'", "'KS3'", "'KS3A'",
                   "'WV03_SWIR'", "'KS5'", "'RS2'", "'IK02'", "'LG01'", "'LG02'"]
    _0_360_list = ["sunAzimuth", "sunElevation", "offNadirAngle", "minimumIncidenceAngle", "maximumIncidenceAngle",
                   "incidenceAngleVariation", "ona", "ona_avg", "sunel_avg", "sun_az_avg", "target_az_avg"]
    _0_1_list = ["cloudCover"]
    error_list = []
    if cql_filter is None:
        error_list.append('filter can not be None type')
        raise Exception('CQL Filter Error:', error_list)
    if cql_filter.find(')') < cql_filter.find('(') or cql_filter.count('(') != cql_filter.count(')'):
        error_list.append('Incorrect parenthesis')
    temp_list = [x.split(')AND(') for x in [i for i in cql_filter.split(')OR(')]]
    cql_parse = [item.replace('(', '').replace(')', '') for sublist in temp_list for item in sublist]
    for item in cql_parse:
        if item.find('>=') > 0:
            key, value = item.split('>=')
        elif item.find('<=') > 0:
            key, value = item.split('<=')
        elif item.find('=') > 0:
            key, value = item.split('=')
        elif item.find('<') > 0:
            key, value = item.split('<')
        elif item.find('>') > 0:
            key, value = item.split('>')
        else:
            error_list.append('No comparison operator e.g. < > =')
            raise Exception('CQL Filter Error:', error_list)

        # more stringent checks on certain filters
        if key == 'source' or key == 'sensor':
            if value not in source_list:
                error_list.append(f'{value} should be one of {source_list}')
        elif key in _0_1_list:
            try:
                value = float(value)
            except:
                error_list.append(f'{value} Not a float')
            if not (0 <= value <= 1):
                error_list.append(f'{value} must be between 0 and 1')
        elif key in _0_360_list:
            try:
                value = float(value)
            except:
                error_list.append(f'{value} Not a float')
            if not (0 <= value <= 360):
                error_list.append(f'{value} must be between 0 and 360')
        if ('decimal' in valid_filters_dict.keys() and key in valid_filters_dict['decimal']) or \
                ('double' in valid_filters_dict.keys() and key in valid_filters_dict['double']):
            try:
                float(value)
            except:
                error_list.append(f'{value} Not a float')
        elif 'boolean' in valid_filters_dict.keys() and key in valid_filters_dict['boolean']:
            value = value.replace("'", "")
            if value != 'FALSE' and value != 'TRUE':
                error_list.append(f'{value} should be either TRUE or FALSE')
        elif 'int' in valid_filters_dict.keys() and key in valid_filters_dict['int']:
            try:
                int(value)
            except:
                error_list.append(f'{value} Not an integer')
        elif ('dateTime' in valid_filters_dict.keys() and key in valid_filters_dict['dateTime']) or \
            ('date' in valid_filters_dict.keys() and key in valid_filters_dict['date']):
            if value[0] != "'" or value[-1] != "'":
                error_list.append(f'{value} Need single quotes around dates')
            value = value.replace("'", "")
            try:
                format_data = "%Y-%m-%d %H:%M:%S.%f"
                datetime.strptime(value, format_data)
            except:
                try:
                    format_data = "%Y-%m-%d"
                    datetime.strptime(value, format_data)
                except:
                    error_list.append(f'{value} Not a valid date')
        elif 'string' in valid_filters_dict.keys() and key in valid_filters_dict['string']:
            if value[0] != "'" or value[-1] != "'":
                error_list.append(f'{value} Need single quotes around string values')
            if not isinstance(value, str):
                error_list.append(f'{value} Not a valid string value')
        else:
            error_list.append(f'{key, value} Not a valid parameter')
    if len(error_list) > 0:
        raise Exception('CQL Filter Error:' + ", ".join(error_list))



class BoundedThreadPoolExecutor(ThreadPoolExecutor):

    def __init__(self, *args, **kwargs):
        super(BoundedThreadPoolExecutor, self).__init__(*args, **kwargs)
        self._work_queue = queue.Queue()
