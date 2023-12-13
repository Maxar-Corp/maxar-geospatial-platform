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
            dra (string) = Binary of whether or not to apply dra to the raster. String of bool (true, false). Defaults
            to false
            interpolation (string) = Desired resizing or (re)projection from one pixel grid to another
            acomp (string) = Binary of whether or not to apply atmospheric compensation to the output after hd (if
            applied) and before dra. String of bool (true, false). Defaults to false
            hd (string) = Binary of whether or not to apply higher resolution to the output. String of bool (true,
            false). Defaults to false
        Returns:
            URL formatted with desired parameters and /vsicurl/ prefix
        """
        self.auth.check_token_expiration()
        if script_id.lower() == 'browse':
            if function != "browse":
                raise Exception("{} is not a valid function. Please use browse".format(function))
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
            acomp = "false"
            hd = "false"
            ortho_functions = ["ortho", "pansharp_ortho"]
            if function not in ortho_functions:
                raise Exception("{} is not a valid function. Please use ortho or pansharp_ortho".format(function))
            for item in kwargs.keys():
                if item == 'dra':
                    dra = kwargs['dra']
                if item == 'bands':
                    bands = kwargs['bands']
                if item == 'acomp':
                    acomp = kwargs['acomp']
                if item == 'hd':
                    hd = kwargs['hd']
            if function == "ortho":
                for item in kwargs.keys():
                    if item == 'interpolation':
                        interp = kwargs['interpolation']
                vsi_url = f'/vsicurl/https://api.maxar.com/analytics/v1/raster/{script_id}/geotiff?function={function}' \
                          f'&p=collect_identifier=%22{collect_id}%22&p=crs=%22{crs}%22&p=bands=%22{bands}%22&p=interpolation=%22{interp}%22' \
                          f'&p=dra={dra}&p=acomp={acomp}&p=hd={hd}&maxar_api_token={api_token}'
            else:
                vsi_url = f'/vsicurl/https://api.maxar.com/analytics/v1/raster/{script_id}/geotiff?function={function}' \
                          f'&p=collect_identifier=%22{collect_id}%22&p=crs=%22{crs}%22&p=bands=%22{bands}%22&p=dra={dra}' \
                          f'&p=acomp={acomp}&p=hd={hd}&maxar_api_token={api_token}'
        elif script_id.lower() == 'ndvi-image':
            ndvi_functions = ["ndvi", "ndvi_dra", "ndvi_colorized"]
            if function not in ndvi_functions:
                raise Exception("{} is not a valid function. Please use ndvi, ndvi_dra, or ndvi_colorized".format(function))
            vsi_url = f'/vsicurl/https://api.maxar.com/analytics/v1/raster/{script_id}/geotiff?function={function}' \
                      f'&p=collect_identifier=%22{collect_id}%22&p=crs=%22{crs}%22&maxar_api_token={api_token}'
        else:
            raise Exception(
                'script_id {} not recognized. Please use browse, ortho-image, or ndvi-image'.format(script_id))
        return vsi_url

    def get_raster_metadata(self, raster_url):
        """
        Lists out various metadata information of a desired raster
        Args:
            raster_url: (string) = Vsicurl formatted URL of a raster object
        Returns:
             Dictionary of various raster metadata information
        """
        self.auth.check_token_expiration()
        gdal = self._gdal_check()
        dataset = gdal.Open(raster_url)
        metadata = dataset.GetMetadata()
        description = dataset.GetDescription()
        raster_count = dataset.RasterCount
        img_width, img_height = dataset.RasterXSize, dataset.RasterYSize
        geo_transform = dataset.GetGeoTransform()
        projection = dataset.GetProjection()
        metadata_dict = {
            "Metadata": metadata, "Description": description, "Bands Count": raster_count, "Image Width": img_width,
            "Image Height": img_height, "Spatial Reference": geo_transform, "Projection": projection
        }
        return metadata_dict

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
        self.auth.check_token_expiration()
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
        self.auth.check_token_expiration()
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

    def search(self, layers, bbox=None, srsname="EPSG:3857", filter=None, shapefile=False, csv=False):
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
        return self.ogc.search(bbox, srsname, filter, shapefile, csv, typename=layers)

    def get_vector_analytics(self, layers, bbox=None, srsname="EPSG:4326", height=None, width=None,
                             format="vnd.jpeg-png", outputpath=None, display=False, **kwargs):
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
            Downloaded file path
        """

        return self.ogc.download_image_by_pixel_count(bbox=bbox, height=height, width=width, srsname=srsname,
                                                      img_format=format, outputpath=outputpath, display=display,
                                                      layers=layers, **kwargs)

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
