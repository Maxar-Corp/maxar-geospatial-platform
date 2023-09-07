from MGP_SDK.analytics_service.analytics import RasterAnalytics, VectorAnalytics
class Interface:

    def __init__(self, auth):
        self.auth = auth
        self.raster = RasterAnalytics(self.auth)
        self.vector = VectorAnalytics(self.auth)

    def get_image_metadata_raster(self, function:str, script_id:str, **kwargs):
        """
        Get metadata about an image given an IPE resource ID, function name, and parameters.
        Args:
        :param function: String of The function to process. ex pansharp
        :param script_id: String of Desired script ID

        Kwargs:
        :param function_parameters: String of The function parameters if required. *Note these are always prepended by
            a `p=` query string param since they are dynamic based on the selected `function`*
        :return: response json object containing the metadata about an image
        """
        if kwargs:
            return self.raster.get_image_metadata(function,script_id, function_parameters=kwargs["function_parameters"])
        else:
            return self.raster.get_image_metadata(function,script_id)

    def get_byte_range_raster(self,function:str, script_id:str, prefetch:bool = True, head_request:bool = False,
                              **kwargs):
        """
        Returns a virtual image as GeoTIFF given a script ID, function name, function parameters
        (provided as url query parameters), and a valid byte range.
        Args:
        :param function: String of The function to process. ex pansharp
        :param script_id: String of Desired script ID
        :param prefetch: Prefetching true or false. Default is true
        :param head_request: Boolean of if you would like this to be a HEAD http request instead of a GET to return only
         response headers

        Kwargs:
        :param function_parameters: String of The function parameters if required. *Note these are always prepended by
            a `p=` query string param since they are dynamic based on the selected `function`*
        :return:
        """
        if kwargs:
            return self.raster.get_byte_range(function,script_id,prefetch,head_request,
                                              function_parameters=kwargs["function_paramaters"])
        else:
            return self.raster.get_byte_range(function,script_id,prefetch,head_request)

    def raster_url(self, script_id, function, collect_id, api_token, crs='UTM', **kwargs):
        """
        Formats a vsicurl URL to be utilized with further raster functions
        Args:
            script_id (string) = Desired IPEScript
            function (string) = Desired function of the IPEScript
            collect_id (string) = Desired raster image ID
            api_token (string) = User's maxar_api_token
            crs (string) = Desired projection. Defaults to UTM
        Kwargs:
            bands (string) = Comma separated string of desired bands. Ex: red,green,blue
            dra (string) = Binary of whether or not to apply dra to the raster. String of bool (true, false)
            interpolation (string) = Desired resizing or (re)projection from one pixel grid to another
        Returns:
            URL formatted with desired parameters and /vsicurl/ prefix
        """

        return self.raster.create_raster_url(script_id, function, collect_id, api_token, crs, **kwargs)

    def get_arrays(self, raster_url, xoff, yoff, width, height):
        """
        Lists out the arrays of a raster
        Args:
            raster_url (string) = Vsicurl formatted URL of a raster object
            xoff (int) = Number of pixels to offset on the x axis
            yoff (int) = Number of pixels to offset on the y axis
            width (int) = Number of pixels for the returned raster on the x axis
            height (int) = Number of pixels for the returned raster on the y axis
        Returns:
            List of arrays of the raster's pixels
        """

        return self.raster.fetch_arrays(raster_url, xoff, yoff, width, height)

    def download_raster(self, raster_array, outputpath):
        """
        Download a rasterized image from a raster array
        Args:
            raster_array (list(list)) = Generated raster array
            outputpath (string) = Desired outputpath for the rasterized image including file extension
        Returns:
            Success message
        """

        return self.raster.download_raster_array(raster_array=raster_array, outputpath=outputpath)

    def search_vector_layer(self,layers:str, bbox=None, srsname="EPSG:3857", filter=None, shapefile=False, csv=False):
        """
            Function searches using the wfs method.

            Args:
                layers (string) = Desired vector data layer
                bbox: Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
                srsname: Desired projection. Defaults to EPSG:3857. NOTE:(WFS for vector data currently only supports EPSG:3857)
                filter: CQL filter used to refine data of search.
                shapefile: (Default False) Binary of whether to return as shapefile format
                csv: (Default False) Binary of whether to return as a csv format
            Returns:
                Response is either a list of features or a shapefile of all features and associated metadata.
        """

        return self.vector.search(layers, bbox, srsname, filter, shapefile, csv)

    def download_vector_analytics(self,layers:str, bbox=None, srsname="EPSG:4326", height=512, width=512,
                                  format = "vnd.jpeg-png", outputpath=None,display=False, **kwargs):
        """
        Function downloads the image using the wms method.

        Args:
            layers (string) = Desired vector layer
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            srsname (string) = Desired projection. Defaults to EPSG:4326
            height (int) = The vertical number of pixels to return. Defaults to 512
            width (int) = The horizontal number of pixels to return. Defaults to 512
            format (string) = The format of the response image either jpeg, png or geotiff
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
            display (bool) = Display image in IDE (Jupyter Notebooks only). Default False
        Returns:
            requests response object or downloaded file path
        """

        return self.vector.get_vector_analytics(bbox=bbox, srsname=srsname, height=height, width=width, format=format,
                                                layers=layers,outputpath=outputpath,display=display, **kwargs)

    def download_vector_tiles(self, layers:str, zoom_level, bbox=None, srsname="EPSG:4326", outputpath=None, display=False):
        """
        Function downloads vector imagery using the wmts method

        Args:
            layers (string) = Desired vector layer
            zoom_level (int) = The desired zoom level
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            srsname (string) = Desired projection. Defaults to EPSG:4326
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
            display (bool) = Display image in IDE (Jupyter Notebooks only). Default False
        Returns:
            Downloaded file path
        """
        return self.vector.get_vector_tiles(layers=layers, zoom_level=zoom_level, bbox=bbox, srsname=srsname,
                                            outputpath=outputpath, display=display)
