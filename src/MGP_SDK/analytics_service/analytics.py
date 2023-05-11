import requests
from MGP_SDK import process
from MGP_SDK.auth.auth import Auth
from MGP_SDK.OGC_Spec.interface import OgcInterface

class RasterAnalytics:
    def __init__(self, auth: Auth):
        self.auth = auth
        self.version = self.auth.version
        self.api_version = self.auth.api_version
        self.base_url = f'{self.auth.api_base_url}/analytics/{self.api_version}/raster'
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}
        self.token_service_token = self.auth.token_service_token()['apiToken']
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




class VectorAnalytics:
    def __init__(self, auth: Auth):
        self.auth = auth
        self.version = self.auth.version
        self.api_version = self.auth.api_version
        self.base_url = f'{self.auth.api_base_url}/analytics/{self.api_version}/vector'
        self.ogc = OgcInterface(self.auth, 'vector')
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}

    def search(self, layers:str,bbox=None, srsname="EPSG:4326", filter=None, shapefile=False, csv=False, ):
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
        return self.ogc.search(bbox,srsname,filter,shapefile,csv,typename=layers)

    def get_vector_analytics(self, layers:str,bbox=None, srsname="EPSG:4326", height=None, width=None, format = "vnd.jpeg-png",outputpath=None,display=False):
        """
        Function downloads the image using the wms method.

        Args:
            bbox: Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
            srsname: Desired projection. Defaults to EPSG:4326
            height: The vertical number of pixels to return. Defaults to 512
            width: The horizontal number of pixels to return. Defaults to 512
            img_format: The format of the response image either jpeg, png or geotiff
            download: User option to download band manipulation file locally. Default True
            outputpath: Output path must include output format. Downloaded path default is user home path.
            display: Display image in IDE (Jupyter Notebooks only). Default False
        Returns:
            requests response object or downloaded file path
        """
        return self.ogc.download_image_by_pixel_count(bbox=bbox,height=height,width=width,srsname=srsname,img_format=format,outputpath=outputpath,display=display, layers=layers)
        #return self.ogc.wms.return_image(bbox=bbox, srsname=srsname, height=height, width=width, format=format, layers=layers)