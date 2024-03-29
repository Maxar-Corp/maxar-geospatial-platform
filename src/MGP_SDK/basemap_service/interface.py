from MGP_SDK.auth.auth import Auth
from MGP_SDK.OGC_Spec.interface import OgcInterface


class Interface:

    def __init__(self, auth: Auth):
        self.auth = auth
        self.ogc = OgcInterface(self.auth, 'basemaps_ogc')
        self.seamlines = OgcInterface(self.auth, 'basemaps_seamlines')

    def search(self, bbox: str = None, srsname: str = "EPSG:4326", filter: str = None, shapefile: bool = False,
               csv: bool = False, seamlines=False, **kwargs):
        """
        Function searches using the wfs method.
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            srsname (sting) = Desired projection. Defaults to EPSG:4326
            filter (string) = CQL filter used to refine data of search.
            shapefile (bool) = Binary of whether to return as shapefile format. Defaults to False
            csv (bool) = Binary of whether to return as a csv format. Defaults to False
            seamlines (bool) = Binary of whether to return the information utilizing the seamlines layer. Defaults to False
        Kwargs:
            featureprofile (string) = The desired stacking profile. Defaults to account Default
            typename (string) = The typename of the desired feature type. Defaults to FinishedFeature
        Returns:
            Response is either a list of features or a shapefile of all features and associated metadata.
        """

        if seamlines:
            return self.seamlines.search(bbox, srsname, filter, shapefile, csv, **kwargs)
        else:
            return self.ogc.search(bbox, srsname, filter, shapefile, csv, **kwargs)

    def download_image(self, bbox: str = None, srsname: str = "EPSG:4326", height: int = 512, width: int = 512,
                       img_format: str = 'jpeg', zoom_level: int = None, download: bool = True, outputpath: str = None,
                       display: bool = False, seamlines=False, **kwargs):
        """
        Function downloads seamline image using the wms method.
        Kwargs:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            srsname (string) = Desired projection. Defaults to EPSG:4326
            height (int) = The vertical number of pixels to return. Defaults to 512
            width (int) = The horizontal number of pixels to return. Defaults to 512
            img_format (string) = The format of the response image either jpeg, png or geotiff
            zoom_level (int) = The zoom level. Used for WMTS
            download (bool) = User option to download band manipulation file locally. Default True
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
            display (bool) = Display image in IDE (Jupyter Notebooks only). Defaults to False
            seamlines (bool) = Binary of whether to return the information utilizing the seamlines layer. Defaults to False
            legacyid (string) = The duc id to download the browse image
        Returns:
            Requests response object or downloaded file path
        """

        if seamlines:
            return self.seamlines.download_image(bbox, srsname, height, width, img_format, zoom_level, download, outputpath,
                                           display, **kwargs)
        else:
            return self.ogc.download_image(bbox, srsname, height, width, img_format, zoom_level, download, outputpath,
                                           display, **kwargs)

    def get_tile_list_with_zoom(self, bbox: str, zoom_level: int, srsname: str = "EPSG:4326", seamlines=False, **kwargs):
        """
        Function acquires a list of tile calls dependent on the desired bbox and zoom level
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            zoom_level (int) = The zoom level
            srsname (string) = Desired projection. Defaults to EPSG:4326
            seamlines (bool) = Binary of whether to return the information utilizing the seamlines layer. Defaults to False
        Returns:
            List of individual tile calls for desired bbox and zoom level
        """

        if seamlines:
            return self.seamlines.get_tile_list_with_zoom(bbox, zoom_level, srsname, **kwargs)
        else:
            return self.ogc.get_tile_list_with_zoom(bbox, zoom_level, srsname, **kwargs)

    def download_tiles(self, bbox: str, zoom_level: int, srsname: str = "EPSG:4326", img_format: str = 'jpeg',
                       outputpath: bool = None, display: bool = False, seamlines=False, **kwargs):
        """
        Function downloads all tiles within a bbox dependent on zoom level

        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            zoom_level (int) = The zoom level
            srsname (string) = Desired projection. Defaults to EPSG:4326
            img_format (string) = The format of the response image either jpeg, png or geotiff
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
            display (bool) = Display image in IDE (Jupyter Notebooks only). Defaults to False
            seamlines (bool) = Binary of whether to return the information utilizing the seamlines layer. Defaults to False
        Returns:
            Message displaying success and location of downloaded tiles
        """

        if seamlines:
            return self.seamlines.download_tiles(bbox, zoom_level, srsname, img_format, outputpath, display, **kwargs)
        else:
            return self.ogc.download_tiles(bbox, zoom_level, srsname, img_format, outputpath, display, **kwargs)

    def download_image_by_pixel_count(self, bbox: str, height: int, width: int, srsname: str = "EPSG:4326",
                                      img_format: str = 'jpeg', outputpath: str = None, display: bool = False,
                                      seamlines=False, **kwargs):
        """
        Function downloads an image within a given AOI
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            height (int) = The vertical number of pixels to return. Defaults to 512
            width (int) = The horizontal number of pixels to return. Defaults to 512
            srsname (string) = Desired projection. Defaults to EPSG:4326
            img_format (string) = The format of the response image either jpeg, png or geotiff
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
            display (bool) = Display image in IDE (Jupyter Notebooks only). Defaults to False
            seamlines (bool) = Binary of whether to return the information utilizing the seamlines layer. Defaults to False
        Returns:
            Message displaying success and location of downloaded tiles
        """
        if seamlines:
            return self.seamlines.download_image_by_pixel_count(bbox, height, width, srsname, img_format, outputpath,
                                                                display, **kwargs)
        else:
            return self.ogc.download_image_by_pixel_count(bbox, height, width, srsname, img_format, outputpath, display,
                                                          **kwargs)

    def get_image_from_csv(self, featureid: str, img_size: int = 1024, seamlines=False, **kwargs):
        """
        Function reruns requests for images that previously failed from a csv file
        Args:
            featureid (string) = Identifier of the desired feature
            img_size (int) = Desired pixel resolution (size x size). Defaults to 1024
            seamlines (bool) = Binary of whether to return the information utilizing the seamlines layer. Defaults to False
        Kwargs:
            outputdirectory (string) = Desired output location for tiles
        Returns:
            None
        """

        # TODO Determine applicability
        if seamlines:
            return self.seamlines.get_image_from_csv(featureid, img_size, **kwargs)
        else:
            return self.ogc.get_image_from_csv(featureid, img_size, **kwargs)
    # TODO Determine applicability of full res imagery for seamlines
    # def get_full_res_image(self, thread_number: int = 100, bbox: str = None, mosaic: bool = False,
    #                        srsname: str = 'EPSG:4326', **kwargs):
    #     """
    #     Function takes in a feature id and breaks the image up into 1024x1024 tiles, then places a number of calls
    #     based on multithreading percentages to return a full image strip in multiple tiles
    #
    #     Args:
    #         thread_number: Number of threads given to multithread functionality
    #         bbox: Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
    #         mosaic: Flag if image files are mosaiced
    #         srsname: Desired projection. Defaults to EPSG:4326
    #     Keyword Args:
    #         outputdirectory: string, Desired output location for tiles
    #         image_format: string, Desired image format (png or jpeg)
    #         filename: string, filename for output mosaiced image
    #     Returns:
    #         None
    #     """
    #
    #     return self.ogc.get_full_res_image(featureid, thread_number, bbox, mosaic, srsname, **kwargs)
    #
    # def create_mosaic(self, base_dir: str, img_format: str, img_size: int = 1024, **kwargs):
    #     """
    #     Function creates a mosaic of downloaded image tiles from full_res_dowload function
    #
    #     Args:
    #         base_dir: Root directory containing image files to be mosaiced
    #         img_format: Image format of files
    #         img_size: Size of individual image files, defaults to 1024
    #     Keyword Args:
    #         outputdirectory: string Directory destination of finished mosaic file
    #         filename: string, filename of merged image
    #     Returns:
    #         None
    #     """
    #
    #     return self.ogc.create_mosaic(base_dir, img_format, img_size, **kwargs)
