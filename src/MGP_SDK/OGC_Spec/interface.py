import os
import csv
import sys
import requests
import warnings
from concurrent.futures import as_completed
from PIL import Image
from MGP_SDK.OGC_Spec.wms import WMS
from MGP_SDK.OGC_Spec.wfs import WFS
from MGP_SDK.OGC_Spec.wmts import WMTS
import MGP_SDK.process as process

warnings.filterwarnings("ignore")


class OgcInterface:
    """
    The primary interface for interacting with the WMS and WFS Streaming classes.
    Args:
        username (string) = The username if your connectId requires Auth
        password (string) = The password associated with your username
        client_id (string) = The client ID associated with your user
    """

    def __init__(self, auth, endpoint):
        self.auth = auth
        self.wms = WMS(auth, endpoint)
        self.wfs = WFS(auth, endpoint)
        self.wmts = WMTS(auth, endpoint)

    def search(self, bbox=None, srsname="EPSG:4326", filter=None, shapefile=False, csv=False, **kwargs):
        """
        Function searches using the wfs method.
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            srsname (string) = Desired projection. Defaults to EPSG:4326
            filter (string) = CQL filter used to refine data of search.
            shapefile (bool) = Binary of whether to return as shapefile format. Defaults to False
            csv (bool) = Binary of whether to return as a csv format. Defaults to False
        Kwargs:
            featureprofile (string) = The desired stacking profile. Defaults to account Default
            typename (string) = The typename of the desired feature type. Defaults to FinishedFeature
        Returns:
            Response is either a list of features or a shapefile of all features and associated metadata.
        """

        if shapefile:
            result = self.wfs.search(bbox=bbox, filter=filter, srsname=srsname, outputformat='shape-zip', **kwargs)
            if 'download_path' in kwargs.keys():
                return process.download_file(result, format_response='zip', download_path=kwargs['download_path'])
            else:
                return process.download_file(result, format_response='zip')
        elif csv:
            result = self.wfs.search(bbox=bbox, filter=filter, srsname=srsname, outputformat='csv', **kwargs)
            if 'download_path' in kwargs.keys():
                return process.download_file(result, format_response='csv', download_path=kwargs['download_path'])
            else:
                return process.download_file(result, format_response='csv')
        else:
            result = self.wfs.search(bbox=bbox, filter=filter, srsname=srsname, **kwargs)
        if bbox:
            if 'typename' in kwargs.keys():
                if 'MaxarCatalogMosaic' in kwargs['typename']:
                    return result.json()['features']
            result = process.aoi_coverage(bbox, result)
            return result['features']
        elif 'request' in kwargs.keys():
            if kwargs['request'] == 'DescribeFeatureType':
                result = self.wfs.search(bbox=bbox, filter=filter, **kwargs)
                return result.text
        else:
            # return result
            return result.json()['features']

    def download_image(self, bbox=None, srsname="EPSG:4326", height=None, width=None, img_format=None,
                       zoom_level=None, download=True, outputpath=None, display=False,
                       **kwargs):
        """
        Function downloads the image using the wms method.
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            srsname (string) = Desired projection. Defaults to EPSG:4326
            height (int) = The vertical number of pixels to return. Defaults to 512
            width (int) = The horizontal number of pixels to return. Defaults to 512
            img_format (string) = The format of the response image either jpeg, png or geotiff
            zoom_level (int) = The zoom level. Used for WMTS
            download (bool) = User option to download band manipulation file locally. Default True
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
            display (bool) = Display image in IDE (Jupyter Notebooks only). Default False
        Kwargs:
            legacyid (string) = The duc id to download the browse image
        Returns:
            Requests response object or downloaded file path
        """

        acceptable_format = ['jpeg', 'png', 'geotiff']
        if img_format != None:
            if img_format in acceptable_format:
                img_formatted = 'image/' + img_format
            else:
                raise Exception('Format not recognized, please use acceptable format for downloading image.')
        if 'legacyid' in kwargs.keys():
            legacy_id = kwargs['legacyid']
            url = "https://api.discover.digitalglobe.com/show?id={}".format(legacy_id)
            result = requests.request("GET", url, headers={}, data={})
        elif zoom_level:
            if not bbox:
                raise Exception('zoom_level must have a bbox')
            else:
                wmts_download = self.download_tiles(bbox=bbox,zoom_level=zoom_level,srsname=srsname,img_format=img_format,outputpath=outputpath,display=display, **kwargs)
                return wmts_download
        else:
            if not bbox or not img_format or not width or not height:
                raise Exception('height/width must have a bbox and an img_format')
            else:
                process._validate_bbox(bbox, srsname=srsname)
                if width < 0 or width > 8000:
                    raise Exception("Invalid value for width parameter (max 8000)")
                if height < 0 or height > 8000:
                    raise Exception("Invalid value for height parameter (max 8000)")
                result = self.wms.return_image(bbox=bbox, srsname=srsname, format=img_formatted, height=height,
                                               width=width, **kwargs)
        if display:
            process._display_image(result)
        if download:
            if outputpath:
                file_name = process.download_file(result, download_path=outputpath)
            else:
                file_name = process.download_file(result, format_response=img_format)
            return f"Downloaded file {file_name}"
        else:
            return result

    def download_browse_image(self, input_id, img_format='jpeg', outputpath=None, display=False):
        """
        Function downloads the browse image for the desired legacy id
        Args:
            input_id (string) = The desired input id (Can be feature id or catalog id)
            img_format (string) = The format of the response image either jpeg, png or geotiff
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
            display (bool) = Display image in IDE (Jupyter Notebooks only). Defaults to False
        Returns:
            Downloaded image location of desired legacy id in desired format
        """

        # legacyid = self._convert_feature_to_legacy(input_id)
        # process._check_image_format(img_format)
        # url = "https://api.discover.digitalglobe.com/show?id={}".format(legacyid)
        # result = requests.request("GET", url, headers={}, data={})
        # if display:
        #     process._display_image(result)
        # if outputpath:
        #     file_name = process.download_file(result, download_path=outputpath)
        # else:
        #     file_name = process.download_file(result, format_response=img_format)
        # return f"Downloaded file {file_name}"
        # TODO determine browse image functionality from new MGP Xpress
        return

    def get_tile_list_with_zoom(self, bbox, zoom_level, srsname="EPSG:4326", **kwargs):
        """
        Function acquires a list of tile calls dependent on the desired bbox and zoom level
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            zoom_level (int) = The zoom level
            srsname (string) = Desired projection. Defaults to EPSG:4326
        Returns:
            List of individual tile calls for desired bbox and zoom level
        """

        process._validate_bbox(bbox, srsname=srsname)
        wmts_list = self.wmts.wmts_bbox_get_tile_list(zoom_level, bbox, crs=srsname, **kwargs)
        return wmts_list

    def download_tiles(self, bbox, zoom_level, srsname="EPSG:4326", img_format='jpeg', outputpath=None, display=False, **kwargs):
        """
        Function downloads all tiles within a bbox dependent on zoom level
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            zoom_level (int) = The zoom level
            srsname (string) = Desired projection. Defaults to EPSG:4326
            img_format (string) = The format of the response image either jpeg, png or geotiff
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
            display (bool) = Display image in IDE (Jupyter Notebooks only). Defaults to False
        Returns:
            Message displaying success and location of downloaded tiles
        """

        process._check_image_format(img_format)
        wmts = self.get_tile_list_with_zoom(bbox, zoom_level, srsname=srsname, img_format=img_format, **kwargs)[1]
        if outputpath:
            extension = outputpath.split(".")[-1]
            base_file = outputpath.replace("." + extension, "")
        else:
            extension = img_format
            base_file = os.getcwd() + "\\Download"
        for tile in wmts:
            response = self.wmts.wmts_get_tile(tile[0], tile[1], tile[2], **kwargs)
            if display:
                process._display_image(response)
            filename = "{}_{}_{}_{}.{}".format(base_file, tile[0], tile[1], tile[2], extension)
            with open(filename, 'wb+') as f:
                f.write(response.content)
        return "Download complete, files are located in {}".format(base_file)

    def download_image_with_feature_id(self, bbox, identifier, gridoffsets, srsname="EPSG:4326", img_format='jpeg',
                                       display=True, outputpath=None):
        """
        Function downloads the image and metadata of desired feature id
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            identifier (string) = Desired feature id
            gridoffsets (string) = The pixel size to be returned in X and Y dimensions
            srsname (string) = Desired projection. Defaults to EPSG:4326
            img_format (string) = The format of the response image either jpeg, png or geotiff. Default jpeg
            display (bool) = Display image in IDE (Jupyter Notebooks only). Defaults to False
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
        Returns:
            Downloaded image location of desired feature id in desired format and associated metadata
        """
        # WCS Not set up
        # process._check_image_format(img_format)
        # result = self.wcs.return_image(bbox, identifier, gridoffsets, srsname=srsname)
        #
        # if display:
        #     process._display_image(result)
        #
        # if outputpath:
        #     file_name = process.download_file(result, download_path=outputpath)
        # else:
        #     file_name = process.download_file(result, format_response=img_format)
        # return self.wcs.parse_coverage(file_name)

    def download_image_by_pixel_count(self, bbox, height, width, srsname, img_format, outputpath=None, display=False,
                                      **kwargs):
        """
        Function downloads the image of desired bbox dependent on pixel height and width
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            height (int) = The vertical number of pixels to return
            width (int) = The horizontal number of pixels to return
            srsname (string) = Desired projection. Defaults to EPSG:4326
            img_format (string) = The format of the response image either jpeg, png or geotiff
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
            display (bool) = Display image in IDE (Jupyter Notebooks only). Defaults to False
        Kwargs:
            filter (string) = CQL filter used to refine data of search.
            featureprofile (string) = The desired stacking profile. Defaults to account Default
        Returns:
            Downloaded image location of desired bbox dependent on pixel height and width
        """

        # if 'filter' in kwargs:
        #     process.cql_checker(kwargs.get('filter'))
        img_formatted = process._check_image_format(img_format)
        process._validate_bbox(bbox, srsname=srsname)
        if width <= 0 or width > 8000:
            raise Exception("Invalid value for width parameter (max 8000)")
        if height <= 0 or height > 8000:
            raise Exception("Invalid value for height parameter (max 8000)")
        result = self.wms.return_image(bbox=bbox, srsname=srsname, format=img_formatted, height=height, width=width,
                                       **kwargs)
        if display:
            process._display_image(result)

        if outputpath:
            file_name = process.download_file(result, download_path=outputpath)
        else:
            file_name = process.download_file(result, format_response=img_format)
        return "Downloaded file {}".format(file_name)

    # def band_manipulation(self, bbox, featureid, band_combination, height=256, width=256, img_format='jpeg',
    #                       display=True, outputpath=None):
    #     """
    #     Function changes the bands of the feature id passed in.
    #     Args:
    #         bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
    #         featureid (string) = The id of the image
    #         band_combination (list(string)) = The desired band combination of 1-4 items.
    #         height (int) = The vertical number of pixels to return
    #         width (int) = The horizontal number of pixels to return
    #         img_format (string) = The file type that you want downloaded.
    #         display (bool) = Display image in IDE (Jupyter Notebooks only). Defaults To True
    #         outputpath (string) = Output path must include output format. Downloaded path default is user home path.
    #     Returns:
    #         download location for file
    #     """
    #
    #     band_string = self._band_check(featureid, band_combination)
    #     feature_id_filter = "featureId='{}'".format(featureid)
    #     message = self.download_image_by_pixel_count(bbox, height, width, img_format, outputpath=outputpath,
    #                                                  display=display,
    #                                                  filter=feature_id_filter, bands=band_string)
    #     return message

    def get_image_from_csv(self, featureid, img_size=1024, **kwargs):
        """
        Function reruns requests for images that previously failed, from a csv file
        Args:
            featureid (string) = Feature id of the image
            img_size (int) = Desired pixel resolution (size x size). Defaults to 1024
        Keyword Args:
            outputdirectory (string) = Desired output location for tiles
        Returns:
            None
        """

        if 'outputdirectory' not in kwargs.keys():
            outputdirectory = os.path.expanduser('~')
        else:
            outputdirectory = kwargs['outputdirectory']

        # call auth here because using wms.return_image() slows down multithreading anc calls auth for each sub_bbox call
        #
        sub_querystring = self.wms.querystring
        sub_querystring['width'] = 1024
        sub_querystring['height'] = 1024
        sub_querystring['cql_filter'] = "featureId='{}'".format(featureid)
        if 'image_format' in kwargs.keys():
            format = kwargs['image_format']
            sub_querystring['format'] = 'image/{}'.format(format)
        else:
            format = sub_querystring['format'][6:]

        url = self.wms.base_url
        sub_querystring = self.wms.querystring
        sub_querystring['width'] = img_size
        sub_querystring['height'] = img_size
        sub_querystring['cql_filter'] = "featureId='{}'".format(featureid)
        if 'image_format' in kwargs.keys():
            format = kwargs['image_format']
            sub_querystring['format'] = 'image/{}'.format(format)
        else:
             format = sub_querystring['format'][6:]
        failed_reqs = []
        token = self.auth.refresh_token()
        authorization = {'Authorization': 'Bearer {}'.format(token)}
        with open(os.path.join(outputdirectory, 'failed_tiles.csv'), "r") as csvfile:
            request_reader = csv.reader(csvfile, delimiter=',')
            for row in request_reader:
                for r in row:
                    sub_bbox1, sub_bbox2, sub_bbox3, sub_bbox4, sub_grid_cell_location = r.split(", ")
                    sub_bbox = sub_bbox1 + ", " + sub_bbox2 + ", " + sub_bbox3 + ", " + sub_bbox4
                    sub_query = sub_querystring.copy()
                    sub_query['bbox'] = sub_bbox
                    sub_response = requests.request("GET", url, params=sub_query, headers=authorization,
                                                    verify=self.auth.SSL)
                    if sub_response.status_code == 200:
                        sub_output = os.path.join(outputdirectory,
                                                  sub_grid_cell_location + ".{}".format(format))
                        process.download_file(sub_response, download_path=sub_output)
                        print('request from csv succeeded for image ' + sub_grid_cell_location)
                    else:
                        print('request from csv failed for image ' + sub_grid_cell_location)
                        failed_reqs.append(r)
        csvfile.close()
        os.remove(os.path.join(outputdirectory, 'failed_tiles.csv'))
        if len(failed_reqs) > 0:
            with open(os.path.join(outputdirectory, 'failed_tiles.csv'), "w", newline='') as csvfile:
                tile_writer = csv.writer(csvfile, delimiter=',')
                for fr in failed_reqs:
                    tile_writer.writerow([fr])

    def get_full_res_image(self, featureid, thread_number=100, bbox=None, mosaic=False, srsname='EPSG:4326', **kwargs):
        """
        Function takes in a feature id and breaks the image up into 1024x1024 tiles, then places a number of calls
        based on multithreading percentages to return a full image strip in multiple tiles
        Args:
            featureid (string) = Feature id of the image
            thread_number (int) = Number of threads given to multithread functionality. Default 100
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            mosaic (bool) = Binary if image files are mosaiced. Default False
            srsname (string) = Desired projection. Defaults to EPSG:4326
        Kwargs:
            outputdirectory (string) = Desired output location for tiles
            image_format (string) = Desired image format (png or jpeg)
            filename (string) = Filename for output mosaiced image
        Returns:
            Message stating success of download and download location
        """

        if bbox:
            process._validate_bbox(bbox, srsname=srsname)
        filter = "featureId='{}'".format(featureid)
        wfs_request = self.search(filter=filter, srsname=srsname)
        image_bbox = wfs_request[0]['geometry']['coordinates'][0]
        x_coords = [x[0] for x in image_bbox]
        y_coords = [y[1] for y in image_bbox]

        if srsname == "EPSG:4326":
            miny = min(y_coords)
            maxy = max(y_coords) + 0.0042176
            minx = min(x_coords)
            maxx = max(x_coords) + 0.0054932
        else:
            miny = min(y_coords)
            maxy = max(y_coords) + 468.1536
            minx = min(x_coords)
            maxx = max(x_coords) + 468.1536

        if bbox:
            bbox_order = bbox.split(',')
            if srsname == "EPSG:4326":
                miny = max(miny, float(bbox_order[0]))
                maxy = min(maxy, float(bbox_order[2])) + 0.0042176
                minx = max(minx, float(bbox_order[1]))
                maxx = min(maxx, float(bbox_order[3])) + 0.0054932
            else:
                miny = max(miny, float(bbox_order[0]))
                maxy = min(maxy, float(bbox_order[2])) + 468.1536
                minx = max(minx, float(bbox_order[1]))
                maxx = min(maxx, float(bbox_order[3])) + 468.1536

        y_list = []
        x_list = []

        if srsname == "EPSG:4326":
            while miny < maxy:
                y_list.append(miny)
                miny += 0.0042176
            while minx < maxx:
                x_list.append(minx)
                minx += 0.0054932
            tiles = {}

            if len(y_list) == 1:
                if len(x_list) == 1:
                    tiles['c{}_r{}'.format(0, 0)] = '{}, {}, {}, {}'.format(y_list[0], x_list[0],
                                                                            y_list[0] + 0.0042176,
                                                                            x_list[0] + 0.0054932)
                else:
                    for x in range(len(x_list) - 1):
                        tiles['c{}_r{}'.format(x, 0)] = '{}, {}, {}, {}'.format(y_list[0], x_list[x],
                                                                                y_list[0] + 0.0042176,
                                                                                x_list[x + 1])
            elif len(x_list) == 1:
                for y in reversed(range(len(y_list) - 1)):
                    tiles['c{}_r{}'.format(0, len(y_list) - y - 2)] = '{}, {}, {}, {}'.format(y_list[y], x_list[0],
                                                                                              y_list[y + 1],
                                                                                              x_list[0] + 0.0054932)
            else:
                for y in reversed(range(len(y_list) - 1)):
                    for x in range(len(x_list) - 1):
                        tiles['c{}_r{}'.format(x, len(y_list) - y - 2)] = '{}, {}, {}, {}'.format(y_list[y], x_list[x],
                                                                                                  y_list[y + 1],
                                                                                                  x_list[x + 1])

        else:
            while miny < maxy:
                y_list.append(miny)
                # How many decimal degrees being incremented by, converted DD to Meters, which is 111km is 1DD at the equator
                # 111 * 0.0042176 is equal to 0.4681536 km then multiplied by 1000 to get 468.1536 Meters
                miny += 468.1536
            while minx < maxx:
                x_list.append(minx)
                minx += 468.1536
            tiles = {}

            if len(y_list) == 1:
                if len(x_list) == 1:
                    tiles['c{}_r{}'.format(0, 0)] = '{}, {}, {}, {}'.format(x_list[0], y_list[0],
                                                                            x_list[0] + 468.1536, y_list[0] + 468.1536)
                else:
                    for x in range(len(x_list) - 1):
                        tiles['c{}_r{}'.format(x, 0)] = '{}, {}, {}, {}'.format(x_list[x], y_list[0],
                                                                                x_list[x + 1], y_list[0] + 468.1536)
            elif len(x_list) == 1:
                for y in reversed(range(len(y_list) - 1)):
                    tiles['c{}_r{}'.format(0, len(y_list) - y - 2)] = '{}, {}, {}, {}'.format(x_list[0], y_list[y],
                                                                                              x_list[0] + 468.1536,
                                                                                              y_list[y + 1])
            else:
                for y in reversed(range(len(y_list) - 1)):
                    for x in range(len(x_list) - 1):
                        tiles['c{}_r{}'.format(x, len(y_list) - y - 2)] = '{}, {}, {}, {}'.format(x_list[x], y_list[y],
                                                                                                  x_list[x + 1],
                                                                                                  y_list[y + 1])

        print("Started full image download process...")

        # This section deletes bboxes that don't cover the image from Tiles
        wfs_Response = self.wfs.search(filter=filter, srsname=srsname)

        if bbox:
            if process.aoi_coverage(bbox, wfs_Response)['features'][0]['bbox_coverage'] == 0:
                raise Exception("Bounding box is outside of desired feature's AOI")

        keysToDel = []
        for tile, bbox in tiles.items():
            if srsname == "EPSG:4326":
                bbox_coverage = process.aoi_coverage(bbox, wfs_Response)['features'][0]['coverage']
            else:
                bbox_list = [i for i in bbox.split(',')]
                bbox = ",".join([bbox_list[1], bbox_list[0], bbox_list[3], bbox_list[2], srsname])
                bbox_coverage = process.aoi_coverage(bbox + ",{}".format(srsname), wfs_Response)['features'][0][
                    'coverage']
            if bbox_coverage == 0.0:
                keysToDel.append(tile)

        for tileKey in keysToDel:
            del tiles[tileKey]



        url = self.wms.base_url
        # call auth here because using wms.return_image() slows down multithreading anc calls auth for each sub_bbox call

        sub_querystring = self.wms._init_querystring(None)
        sub_querystring['crs'] = srsname
        sub_querystring['width'] = 1024
        sub_querystring['height'] = 1024
        sub_querystring['cql_filter'] = "featureId='{}'".format(featureid)
        if 'image_format' in kwargs.keys():
            format = kwargs['image_format']
            sub_querystring['format'] = 'image/{}'.format(format)
        else:
            format = sub_querystring['format'][6:]

        def response_thread(coord_list: list, authorization: str):
            """
            Function multithreads requests to speed up image return process
            Args:
                coord_list (list) = Coordinates for individual tiles
                authorization (string) = auth header containing bearer token
            Returns:
                List of cell locations and corresponding response objects
            """

            failed_request = []
            sub_bbox, sub_grid_cell_location = coord_list.split("|")
            sub_query = sub_querystring.copy()
            sub_query['bbox'] = sub_bbox
            sub_response = requests.request("GET", url, params=sub_query, headers=authorization, verify=self.auth.SSL)
            if sub_response.status_code != 200:
                failed_request.append(coord_list)
            return [sub_grid_cell_location, sub_response, failed_request]

        def split_array_and_send_requests(array: list, num_attempts: int):
            """

            Function splits the array into chucks and executes the response_thread function using the
            thread pool executor, then downloads the image file if the request is successful. If requests
            fail, the function retries requests for those tiles until they succeed
            Args:
                array (list) = Tiles with corresponding coordinates
                num_attempts (int) = Number of times rerunning the requests has been attempted
            """

            failed_reqs = []
            chunk_size = thread_number * 5
            chunk_count = int(len(array) / chunk_size)
            for i in range(chunk_count + 1):
                # gets auth once per chunk
                token = self.auth.refresh_token()
                authorization = {'Authorization': 'Bearer {}'.format(token)}
                if i == chunk_count:
                    sub_array = array[i * chunk_size:]
                else:
                    sub_array = array[i * chunk_size:(i + 1) * chunk_size]
                with process.BoundedThreadPoolExecutor(max_workers=thread_number) as executor:
                    futures = [executor.submit(response_thread, coords, authorization) for coords in sub_array]
                    for future in as_completed(futures):
                        coord, response, failed_request = future.result()
                        if response.status_code == 200:
                            sub_output = os.path.join(outputdirectory, coord + ".{}".format(format))
                            process.download_file(response, download_path=sub_output)
                        else:
                            for fr in failed_request:
                                failed_reqs.append(fr)
                print('Finished section {} out of {}'.format(i + 1, chunk_count + 1))
                print('\r')
            if len(failed_reqs) > 0:
                if num_attempts < 10:
                    num_attempts += 1
                    print('Some image requests failed, retrying failed requests, retry attempt {}'.format(num_attempts))
                    print('\r')
                    split_array_and_send_requests(failed_reqs, num_attempts)
                else:
                    print('Attempted failed image requests 10 times, will print failed requests to csv and retry')
                    print('\r')
                    with open(os.path.join(outputdirectory, 'failed_tiles.csv'), "w", newline='') as csvfile:
                        failed_tile_writer = csv.writer(csvfile, delimiter=',')
                        for fr in failed_reqs:
                            row_content = fr.replace("|", ", ")
                            failed_tile_writer.writerow([row_content])
                    csvfile.close()
            failed_reqs.clear()
            print('\r')
            print('\n')

        multithreading_array = ["{}|{}".format(k, j) for j, k in list(tiles.items())]

        # assign output directory to home dir if not specified
        if 'outputdirectory' not in kwargs.keys():
            outputdirectory = os.path.expanduser('~')
        else:
            outputdirectory = kwargs['outputdirectory']

        # assign generic filename if not specified
        if 'filename' in kwargs.keys():
            filename = kwargs['filename']
        else:
            filename = 'Maxar_Image'

        # This code takes the output directory and makes a new directory inside of it to put all the images. This is because create_mosaic will break if the folder has other files in it.
        outputdirectory = outputdirectory + r'\{}'.format(filename)
        if not os.path.exists(outputdirectory):
            os.makedirs(outputdirectory)
        else:
            start = 1
            outputdirectory2 = outputdirectory + str(start)
            while os.path.exists(outputdirectory2):
                outputdirectory2 = outputdirectory + str(start)
                start += 1
            outputdirectory = outputdirectory2
            os.makedirs(outputdirectory)

        with open(os.path.join(outputdirectory, 'Grid_cell_coordinates.txt'), 'w') as grid_coords:
            grid_coords.write('grid_cell_name | grid_cell_bbox\n')
            for line in multithreading_array:
                value, key = line.split('|')
                grid_coords.write('{} | {}\n'.format(key, value))

        split_array_and_send_requests(multithreading_array, num_attempts=0)

        if mosaic:
            if 'image_format' in kwargs.keys():
                self.create_mosaic(base_dir=outputdirectory, img_format=kwargs['image_format'], img_size=1024, **kwargs)
                return "Finished full image download process, output directory is: {}. Beginning mosaic process". \
                    format(os.path.split(outputdirectory)[0])
            else:
                self.create_mosaic(base_dir=outputdirectory, img_size=1024, img_format='jpeg', **kwargs)
                return "Finished full image download process, output directory is: {}. Beginning mosaic process". \
                    format(os.path.split(outputdirectory)[0])
        else:
            return "Finished full image download process, output directory is: {}". \
                format(os.path.split(outputdirectory)[0])

    def create_mosaic(self, base_dir, img_format, img_size=1024, **kwargs):
        """
        Function creates a mosaic of downloaded image tiles from full_res_dowload function
        Args:
            base_dir (string) = Root directory containing image files to be mosaiced
            img_format (string) = Image format of files
            img_size (int) = Size of individual image files, defaults to 1024
        Kwargs:
            outputdirectory (string) = string Directory destination of finished mosaic file
            filename (string) = Filename of merged image
        Returns:
            None
        """

        if img_format == 'geotiff':
            try:
                import rasterio
                from rasterio.merge import merge
            except:
                self._pillow_mosaic(base_dir, img_format, img_size=img_size, **kwargs)
                print("GDAL and rasterio are not installed on your machine. The downloaded image will not be georeferenced. "
                      " Please refer to the MGP_SDK documentation for steps on how to install GDAL in "
                      "your environment. To install rasterio use: pip install rasterio")
            else:
                srcs_to_mosaic = []
                for image in os.listdir(base_dir):
                    if image.endswith('.geotiff'):
                        raster = rasterio.open(os.path.join(base_dir, image))
                        srcs_to_mosaic.append(raster)
                        output_data = raster.meta.copy()
                mosaic, output = merge(srcs_to_mosaic)
                output_data.update(
                    {"driver": "GTiff",
                     "height": mosaic.shape[1],
                     "width": mosaic.shape[2],
                     "transform": output
                     }
                )

                if 'outputdirectory' in kwargs.keys():
                    if 'filename' in kwargs.keys():
                        with rasterio.open(os.path.join(
                                kwargs['outputdirectory'], kwargs['filename'] + '.geotiff'), "w", **output_data) as m:
                            m.write(mosaic)
                        print(
                            "Finished image mosaic process, output directory is: {}".format(kwargs['outputdirectory']))
                    else:
                        with rasterio.open(os.path.join(
                                kwargs['outputdirectory'], 'merged_image.geotiff'), "w", **output_data) as m:
                            m.write(mosaic)
                        print(
                            "Finished image mosaic process, output directory is: {}".format(kwargs['outputdirectory']))
                else:
                    if 'filename' in kwargs.keys():
                        with rasterio.open(os.path.join(base_dir, kwargs['filename'] + '.geotiff'), "w",
                                           **output_data) as m:
                            m.write(mosaic)
                    else:
                        with rasterio.open(os.path.join(base_dir, 'merged_image.geotiff'), "w", **output_data) as m:
                            m.write(mosaic)
                    print("Finished image mosaic process, output directory is: {}".format(base_dir))
        else:
            self._pillow_mosaic(base_dir, img_format, img_size=img_size, **kwargs)

    def _pillow_mosaic(self, base_dir: str, img_format: str, img_size: int = 1024, **kwargs):
        """
        Function creates a mosaic of downloaded image tiles from full_res_dowload function
        Args:
            base_dir (string) = Root directory containing image files to be mosaiced
            img_format (string) = Image format of files
            img_size (int) = Size of individual image files, defaults to 1024
        Kwargs:
            outputdirectory (string) = Directory destination of finished mosaic file
            filename (string) = Filename of merged image
        Returns:
            None
        """

        Image.MAX_IMAGE_PIXELS = None
        coord_list = []
        for k in [i for i in os.listdir(base_dir) if ".txt" not in i and os.path.isfile(os.path.join(base_dir, i))]:
            filename = k
            coords = k.replace('c', '').replace('_r', ',').replace('.{}'.format(img_format), '').split(',')
            if "geotiff" in filename:
                pre, ext = os.path.splitext(os.path.join(base_dir, filename))
                os.rename(os.path.join(base_dir, filename), pre + ".tiff")
                filename = filename.replace("geotiff", "tiff")
            coord_list.append([filename, int(coords[0]), int(coords[1])])

        max_row = max([i[2] for i in coord_list]) + 1
        max_col = max([i[1] for i in coord_list]) + 1
        maximum = max(max_col, max_row)
        size = img_size * maximum
        mosaic = Image.new('RGB', (max_col * img_size, max_row * img_size), (size, size, size))

        count = 0
        for i in coord_list:
            column = img_size * i[1]
            row = img_size * i[2]
            mosaic.paste(Image.open(os.path.join(base_dir, i[0])), (column, row))
            count += 1
            if count % 100 == 0:
                sys.stdout.write("Processing {} of {} total".format(count, len(coord_list)))
                sys.stdout.write("\r")

        # must change to tiff because pillow doesnt support geotiff
        if img_format == "geotiff":
            img_format = "tiff"
        # if they specify filename, give it a name. Else, call it merged image
        if 'outputdirectory' in kwargs.keys():
            if 'filename' in kwargs.keys():
                filepath = r"{}\{}.{}".format(kwargs['outputdirectory'], kwargs['filename'], img_format)
                mosaic.save(filepath)
                print("Finished image mosaic process, output directory is: {}".format(kwargs['outputdirectory']))
            else:
                filepath = r"{}\merged_image.{}".format(kwargs['outputdirectory'], img_format)
                mosaic.save(filepath)
                print("Finished image mosaic process, output directory is: {}".format(kwargs['outputdirectory']))
        else:
            if 'filename' in kwargs.keys():
                filepath = r"{}\{}.{}".format(base_dir, kwargs['filename'], img_format)
                mosaic.save(filepath)
            else:
                filepath = r"{}\merged_image.{}".format(base_dir, img_format)
                mosaic.save(filepath)
            print("Finished image mosaic process, output directory is: {}".format(base_dir))

    def _band_check(self, featureid: str, band_combination: list, srsname: str = "EPSG:4326"):
        """
        Function checks bands given against a list of valid bands
        Args:
            featureid (string) = The id of the image
            band_combination (list) = The desired band combination of 1-4 items.
            srsname (string) = Desired projection. Defaults to EPSG:4326
        Returns:
            String of band combination
        """

        band_check = self.search(filter="featureId='{}'".format(featureid), srsname=srsname)
        #        band_check_list = ['MS1_MS2', 'SWIR 8-Band']
        band_check_list = ['WV03_SWIR']
        #        if band_check[0]['properties']['productType'] not in band_check_list:
        if band_check[0]['properties']['source'] not in band_check_list:
            raise Exception('Product Type for the image must be either SWIR 8-band or MS1_MS2.')
        band_options = ['R', 'G', 'B', 'C', 'Y', 'RE', 'N', 'N2', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7']
        if len(band_combination) <= 0 or len(band_combination) > 4:
            raise Exception('The number of bands must be greater than 0 and less than or equal to 4.')

        band_string = ','.join([i if i in band_options else 'z' for i in band_combination])

        if 'z' in band_string:
            raise Exception(band_combination + ' is not a valid option.')
        return band_string

    def _convert_feature_to_legacy(self, input_id: str):
        """
        Function takes in a feature id or legacy id and finds the browse image associated with it.
        Args:
            input_id (string) = The id that you are searching for
        Returns:
            Legacy id of desired feature
        """

        catalog_identifiers = ['101', '102', '103', '104', '105', '106']

        # if the id passed in is a cat id or WVO4 Inv id. Return the browse for that id from discover api
        if input_id[0:3] in catalog_identifiers or '-inv' == input_id[-4:]:
            legacy_id = input_id
        # If the id passed in is a feature id. Use our wfs method to return a json and parse out the legacy id from
        # the metadata
        else:
            json_return = self.search(filter="featureId='{}'".format(input_id))
            legacy_id = json_return[0]['properties']['legacyIdentifier']
        return legacy_id

    @staticmethod
    def calculate_sqkm(bbox: str):
        """
        Function calculates the area in square kilometers of the desired bounding box
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
        Returns:
            Float of bounding box area in square kilometers
        """

        return process.area_sqkm(bbox)
