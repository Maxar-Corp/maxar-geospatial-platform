import requests
from MGP_SDK import process
from MGP_SDK.auth.auth import Auth
from MGP_SDK.OGC_Spec.interface import OgcInterface
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

class RasterAnalytics:
    def __init__(self, auth: Auth):
        self.auth = auth
        self.version = self.auth.version
        self.api_version = self.auth.api_version
        self.base_url = f'{self.auth.api_base_url}/analytics/{self.api_version}/raster'
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}
        self.token_service_token = self.auth.token_service_token()['apiToken']

    def _gdal_check(self):
        try:
            from osgeo import gdal
            return gdal
        except:
            raise Exception("Gdal not found on this machine")

    def _parameters_formatter(self,params:list):
        return "&".join(["p=" + param for param in params])

    def get_image_metadata(self, function:str, script_id:str, **kwargs):
        """
        Get metadata about an image given an IPE resource ID, function name, and parameters.
        Args:
        :param function: String of The function to process. ex pansharp
        :param script_id: String of Desired script ID

        Kwargs:
        :param function_parameters: list of The function parameters if required. Ex ["catalogID=10400100655F5400","crs=EPSG:4326","ancillaryType=refined"]
        :return: response json object containing the metadata about an image
        """
        if "function_parameters" in kwargs.keys():
            if type(kwargs["function_parameters"] != list):
                raise Exception("function_parameters needs to be a list of the paramaters. EX: ['catalogID=10400100655F5400','crs=EPSG:4326','ancillaryType=refined']")
            formatted_params = self._parameters_formatter(kwargs["function_parameters"])
            url = f"{self.base_url}/{script_id}/metadata?function={function}&{formatted_params}&maxar_api_token={self.token_service_token}"
        else:
            url = f"{self.base_url}/{script_id}/metadata?function={function}&maxar_api_token={self.token_service_token}"
        response = requests.get(url, verify=self.auth.SSL)
        return process._response_handler(response)

    def get_byte_range(self,function:str, script_id:str, prefetch:bool = True, head_request:bool = False, **kwargs):
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
        :param function_parameters: list of The function parameters if required. Ex ["catalogID=10400100655F5400","crs=EPSG:4326","ancillaryType=refined"]
        :return:
        """
        if "function_parameters" in kwargs.keys():
            if type(kwargs["function_parameters"] != list):
                raise Exception("function_parameters needs to be a list of the paramaters. EX: ['catalogID=10400100655F5400','crs=EPSG:4326','ancillaryType=refined']")
            formatted_params = self._parameters_formatter(kwargs["function_parameters"])
            url = f"{self.base_url}/{script_id}/metadata?function={function}&prefetch={prefetch}&{formatted_params}&maxar_api_token={self.token_service_token}"
        else:
            url = f"{self.base_url}/{script_id}/metadata?function={function}&prefetch={prefetch}&maxar_api_token={self.token_service_token}"
        if head_request:
            response = requests.request("HEAD",url,verify=self.auth.SSL)
        else:
            response = requests.get(url, verify=self.auth.SSL)
        return process._response_handler(response)

    def create_raster_url(self, script_id, function, collect_id, api_token, crs='UTM', **kwargs):
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

        if script_id.lower() == 'browse':
            function = 'browse'
            bands = "red,green,blue"
            for item in kwargs.keys():
                if item == 'bands':
                    bands = kwargs['bands']
            vsi_url = f'/vsicurl/https://api.maxar.com/analytics/v1/raster/{script_id}/geotiff?function={function}' \
                      f'&p=collect_identifier=%22{collect_id}%22&p=crs=%22{crs}%22&p=bands=%22{bands}%22&maxar_api_token={api_token}'
        elif script_id.lower() == 'ortho-image':
            dra = "false"
            interp = "MTF"
            bands = "red,green,blue"
            ortho_functions = ["ortho", "pansharp_ortho"]
            if function not in ortho_functions:
                raise Exception("{} is not a valid function".format(function))
            for item in kwargs.keys():
                if item == 'dra':
                    dra = kwargs['dra']
                if item == 'bands':
                    bands = kwargs['bands']
            if function == "ortho":
                for item in kwargs.keys():
                    if item == 'interpolation':
                        interp = kwargs['interpolation']
                vsi_url = f'/vsicurl/https://api.maxar.com/analytics/v1/raster/{script_id}/geotiff?function={function}' \
                          f'&p=collect_identifier=%22{collect_id}%22&p=crs=%22{crs}%22&p=bands=%22{bands}%22&p=interpolation=%22{interp}%22' \
                          f'&p=dra={dra}&maxar_api_token={api_token}'
            else:
                function = 'pansharp_ortho'
                vsi_url = f'/vsicurl/https://api.maxar.com/analytics/v1/raster/{script_id}/geotiff?function={function}' \
                          f'&p=collect_identifier=%22{collect_id}%22&p=crs=%22{crs}%22&p=bands=%22{bands}%22&p=dra={dra}&maxar_api_token={api_token}'
        elif script_id.lower() == 'ndvi-image':
            ndvi_functions = ["ndvi", "ndvi_dra", "ndvi_colorized"]
            if function not in ndvi_functions:
                raise Exception("{} is not a valid function".format(function))
            function = function
            vsi_url = f'/vsicurl/https://api.maxar.com/analytics/v1/raster/{script_id}/geotiff?function={function}' \
                      f'&p=collect_identifier=%22{collect_id}%22&p=crs=%22{crs}%22&maxar_api_token={api_token}'
        else:
            raise Exception(
                'script_id {} not recognized. Please use browse, ortho-image, or ndvi-image'.format(script_id))
        return vsi_url

    def fetch_arrays(self, raster_url, xoff, yoff, width, height):
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

        gdal = self._gdal_check()
        dataset = gdal.Open(raster_url)
        img_arrays = []
        for band_index in range(dataset.RasterCount):
            band = dataset.GetRasterBand(band_index + 1)
            band_as_array = band.ReadAsArray(xoff, yoff, width, height)
            img_arrays.append(band_as_array)
        return img_arrays

    def download_raster_array(self, raster_array, outputpath):
        """
        Download a rasterized image from a raster array
        Args:
            raster_array (list(list)) = Generated raster array
            outputpath (string) = Desired outputpath for the rasterized image including file extension
        Returns:
            Success message
        """

        img = np.dstack((raster_array[0], raster_array[1], raster_array[2]))
        matplotlib.image.imsave(outputpath, img)
        return "Raster image saved in {}".format(outputpath)

class VectorAnalytics:
    def __init__(self, auth: Auth):
        self.auth = auth
        self.version = self.auth.version
        self.api_version = self.auth.api_version
        self.base_url = f'{self.auth.api_base_url}/analytics/{self.api_version}/vector'
        self.ogc = OgcInterface(self.auth, 'vector')
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}

    def search(self, layers:str,bbox=None, srsname="EPSG:3857", filter=None, shapefile=False, csv=False):
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
        return self.ogc.search(bbox,srsname,filter,shapefile,csv,typename=layers)

    def get_vector_analytics(self, layers:str,bbox=None, srsname="EPSG:4326", height=None, width=None,
                             format="vnd.jpeg-png", outputpath=None, display=False, **kwargs):
        """
        Function downloads the image using the wms method.

        Args:
            layers (string) = Desired vector layer
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            srsname (string) = Desired projection. Defaults to EPSG:4326
            height (int) = The vertical number of pixels to return. Defaults to 512
            width (int) = The horizontal number of pixels to return. Defaults to 512
            img_format (string) = The format of the response image either jpeg, png or geotiff
            outputpath (string) = Output path must include output format. Downloaded path default is user home path.
            display (bool) = Display image in IDE (Jupyter Notebooks only). Default False
        Returns:
            Downloaded file path
        """

        return self.ogc.download_image_by_pixel_count(bbox=bbox, height=height, width=width, srsname=srsname,
                                                      img_format=format, outputpath=outputpath, display=display,
                                                      layers=layers, **kwargs)
        #return self.ogc.wms.return_image(bbox=bbox, srsname=srsname, height=height, width=width, format=format, layers=layers)


    def get_vector_tiles(self, layers:str, zoom_level, bbox=None, srsname="EPSG:4326", outputpath=None, display=False):
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

        return self.ogc.download_tiles(bbox=bbox, zoom_level=zoom_level, srsname=srsname, img_format='png',
                                       outputpath=outputpath, display=display, layers=layers)