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

    def search_vector_layer(self,layers:str, bbox=None, srsname="EPSG:4326", filter=None, shapefile=False, csv=False, **kwargs):
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
        return self.vector.search(layers, bbox, srsname, filter, shapefile, csv)

    def download_vector_analytics(self,layers:str, bbox=None, srsname="EPSG:4326", height=512, width=512, format = "vnd.jpeg-png", outputpath=None,display=False):
        """
        Function downloads the image using the wms method.

        Args:
            bbox: Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            srsname: Desired projection. Defaults to EPSG:4326
            height: The vertical number of pixels to return. Defaults to 512
            width: The horizontal number of pixels to return. Defaults to 512
            img_format: The format of the response image either jpeg, png or geotiff
            identifier: The feature id
            download: User option to download band manipulation file locally. Default True
            outputpath: Output path must include output format. Downloaded path default is user home path.
            display: Display image in IDE (Jupyter Notebooks only). Default False
        Keyword Args:
            legacyid: (string) The duc id to download the browse image
        Returns:
            requests response object or downloaded file path
        """
        return self.vector.get_vector_analytics(bbox=bbox, srsname=srsname, height=height, width=width, format=format, layers=layers,outputpath=outputpath,display=display)


