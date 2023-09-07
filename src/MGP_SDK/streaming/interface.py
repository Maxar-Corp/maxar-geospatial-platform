import warnings
from MGP_SDK.OGC_Spec.interface import OgcInterface


class Interface:
    """
    The primary interface for interacting with the WMS and WFS Streaming classes.
    Args:
        username (string) = The username if your connectId requires Auth
        password (string) = The password associated with your username
    """

    def __init__(self, auth):
        self.auth = auth
        self.ogc = OgcInterface(self.auth, 'streaming')

    def search(self, bbox: str = None, srsname: str = "EPSG:4326", filter: str = None, shapefile: bool = False,
               csv: bool = False, **kwargs):
        """
        Function searches using the wfs method.

        Args:
            bbox: Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            srsname: Desired projection. Defaults to EPSG:4326
            filter: CQL filter used to refine data of search.
            shapefile: (Default False) Binary of whether to return as shapefile format
            csv: (Default False) Binary of whether to return as a csv format
        Keyword Args:
            featureprofile: The desired stacking profile. Defaults to account Default
            typename: The typename of the desired feature type. Defaults to FinishedFeature
        Returns:
            Response is either a list of features or a shapefile of all features and associated metadata.
        """
        return self.ogc.search(bbox, srsname, filter, shapefile, csv, **kwargs)

    def download_image(self, bbox: str = None, srsname: str = "EPSG:4326", height: int = 512, width: int = 512,
                       img_format: str = 'jpeg', zoom_level: int = None, download: bool = True, outputpath: str = None,
                       display: bool = False, **kwargs):
        """
        Function downloads the image using the wms method.

        Args:
            bbox: Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            srsname: Desired projection. Defaults to EPSG:4326
            height: The vertical number of pixels to return. Defaults to 512
            width: The horizontal number of pixels to return. Defaults to 512
            img_format: The format of the response image either jpeg, png or geotiff
            identifier: The feature id
            gridoffsets: The pixel size to be returned in X and Y dimensions
            zoom_level: The zoom level. Used for WMTS
            download: User option to download band manipulation file locally. Default True
            outputpath: Output path must include output format. Downloaded path default is user home path.
            display: Display image in IDE (Jupyter Notebooks only). Default False
        Keyword Args:
            legacyid: (string) The duc id to download the browse image
        Returns:
            requests response object or downloaded file path
        """
        return self.ogc.download_image(bbox, srsname, height, width, img_format, zoom_level, download, outputpath,
                                       display, **kwargs)

    def download_browse_image(self, input_id, img_format='jpeg', outputpath=None, display=False):
        # TODO determine browse image functionality from new MGP Xpress
        return

    def get_tile_list_with_zoom(self, bbox: str, zoom_level: int, srsname: str = "EPSG:4326", **kwargs):
        """
        Function acquires a list of tile calls dependent on the desired bbox and zoom level

        Args:
            bbox: Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            zoom_level: The zoom level
            srsname: Desired projection. Defaults to EPSG:4326
        Returns:
            List of individual tile calls for desired bbox and zoom level
        """

        return self.ogc.get_tile_list_with_zoom(bbox, zoom_level, srsname, **kwargs)

    def download_tiles(self, bbox: str, zoom_level: int, srsname: str = "EPSG:4326", img_format: str = 'jpeg',
                       outputpath: bool = None, display: bool = False, **kwargs):
        """
        Function downloads all tiles within a bbox dependent on zoom level

        Args:
            bbox: Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            zoom_level: The zoom level
            srsname: Desired projection. Defaults to EPSG:4326
            img_format: The format of the response image either jpeg, png or geotiff
            outputpath: Output path must include output format. Downloaded path default is user home path.
            display: Display image in IDE (Jupyter Notebooks only)
        Returns:
            Message displaying success and location of downloaded tiles
        """

        return self.ogc.download_tiles(bbox, zoom_level, srsname, img_format, outputpath, display, **kwargs)

    def download_image_with_feature_id(self, bbox: str, identifier: str, gridoffsets: str, srsname: str = "EPSG:4326",
                                       img_format: str = 'jpeg', display: bool = True, outputpath: str = None):
        """
        Function downloads the image and metadata of desired feature id

        Args:
            bbox: Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            identifier: Desired feature id
            gridoffsets: The pixel size to be returned in X and Y dimensions
            srsname: Desired projection. Defaults to EPSG:4326
            img_format: The format of the response image either jpeg, png or geotiff. Default jpeg
            display: Display image in IDE (Jupyter Notebooks only)
            outputpath: Output path must include output format. Downloaded path default is user home path.
        Returns:
            Downloaded image location of desired feature id in desired format and associated metadata
        """
        # TODO WCS not set up
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

    def download_image_by_pixel_count(self, bbox: str, height: int, width: int, srsname: str = "EPSG:4326",
                                      img_format: str = 'jpeg', outputpath: str = None, display: bool = False,
                                      **kwargs):
        """
        Function downloads the image of desired bbox dependent on pixel height and width

        Args:
            bbox: Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            height: The vertical number of pixels to return
            width: The horizontal number of pixels to return
            srsname: Desired projection. Defaults to EPSG:4326
            img_format: Default=jpeg, The format of the response image either jpeg, png or geotiff
            outputpath: Output path must include output format. Downloaded path default is user home path.
            display: Display image in IDE (Jupyter Notebooks only)
        Keyword Args:
            filter: CQL filter used to refine data of search.
            featureprofile: The desired stacking profile. Defaults to account Default
        Returns:
            Downloaded image location of desired bbox dependent on pixel height and width
        """
        return self.ogc.download_image_by_pixel_count(bbox, height, width, srsname, img_format, outputpath, display,
                                                      **kwargs)

    def get_image_from_csv(self, featureid: str, img_size: int = 1024, **kwargs):
        """
        Function reruns requests for images that previously failed, from a csv file

        Args:
            featureid: Feature id of the image
            img_size: Desired pixel resolution (size x size). Defaults to 1024
        Keyword Args:
            outputdirectory: string, Desired output location for tiles
        Returns:
            None
        """

        return self.ogc.get_image_from_csv(featureid, img_size, **kwargs)

    def get_full_res_image(self, featureid: str, thread_number: int = 100, bbox: str = None, mosaic: bool = False,
                           srsname: str = 'EPSG:4326', **kwargs):
        """
        Function takes in a feature id and breaks the image up into 1024x1024 tiles, then places a number of calls
        based on multithreading percentages to return a full image strip in multiple tiles

        Args:
            featureid: Feature id of the image
            thread_number: Number of threads given to multithread functionality. Default 100
            bbox: Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            mosaic: Flag if image files are mosaiced. Default False
            srsname: Desired projection. Defaults to EPSG:4326
        Keyword Args:
            outputdirectory: string, Desired output location for tiles
            image_format: string, Desired image format (png or jpeg)
            filename: string, filename for output mosaiced image
        Returns:
            None
        """
        return self.ogc.get_full_res_image(featureid, thread_number, bbox, mosaic, srsname, **kwargs)

    def create_mosaic(self, base_dir: str, img_format: str, img_size: int = 1024, **kwargs):
        """
        Function creates a mosaic of downloaded image tiles from full_res_dowload function

        Args:
            base_dir: Root directory containing image files to be mosaiced
            img_format: Image format of files
            img_size: Size of individual image files, defaults to 1024
        Keyword Args:
            outputdirectory: string Directory destination of finished mosaic file
            filename: string, filename of merged image
        Returns:
            None
        """
        # TODO Determine best use case for seamline streaming
        return self.ogc.create_mosaic(base_dir, img_format, img_size, **kwargs)

    def calculate_sqkm(self, bbox: str):
        """
        Function calculates the area in square kilometers of the desired bounding box
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
        Returns:
            Float of bounding box area in square kilometers
        """
        return self.ogc.calculate_sqkm(bbox=bbox)
