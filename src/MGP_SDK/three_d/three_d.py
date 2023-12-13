import requests
import MGP_SDK.process as process


class Three_d:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = auth.api_base_url + "/proxy/terracotta/3dtiles"

    def get_capabilities_3d(self):
        """
        Function lists out all 3D layers and their capabilities
        Returns:
            Dictionary of 3D layers and their information
        """
        self.auth.check_token_expiration()
        authorization = process.authorization(self.auth)
        url = "{}/capabilities".format(self.base_url)
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_coverage_3d(self, bbox, **kwargs):
        """
        Function lists the 3Dtiles layers that overlap a requested area
        Args:
            bbox (string) = Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
        Kwargs:
            srs (string) = Spatial Reference system for the return coverage polygons (default EPSG:4326)
            bbox_srs (string) = Spatial Reference system of the bounding box srs (default EPSG:4326)
        Returns:
            Dictionary of 3Dtiles layers that overlap the requested area and their information
        """
        self.auth.check_token_expiration()
        authorization = process.authorization(self.auth)
        keys = list(kwargs.keys())
        if 'srs' in keys and kwargs['srs']:
            if 'bbox_srs' in keys and kwargs['bbox_srs']:
                url = "{}/coverage?bbox={}&srs={}&bbox_srs={}".format(self.base_url, bbox, kwargs['srs'], kwargs['bbox_srs'])
            else:
                url = "{}/coverage?bbox={}&srs={}".format(self.base_url, bbox, kwargs['srs'])
        elif 'bbox_srs' in keys and kwargs['bbox_srs']:
            url = "{}/coverage?bbox={}&bbox_srs={}".format(self.base_url, bbox, kwargs['bbox_srs'])
        else:
            url = "{}/coverage?bbox={}".format(self.base_url, bbox)
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_layer_tileset_3d(self, layer):
        """
        Function provides a tileset.json for the desired 3D layer
        Args:
            layer (string) = The desired 3D layer
        Returns:
            JSON object of the desired 3D layer's information
        """
        self.auth.check_token_expiration()
        authorization = process.authorization(self.auth)
        get_cap = self.get_capabilities_3d()
        uri = [i['uri'] for i in get_cap['layers'] if layer.lower() == i['name']][0]
        if len(uri) == 0:
            raise Exception("{} is not a valid layer name. Please enter a valid layer name".format(layer))
        url = uri.replace("https://api.maxar.com/", "https://api.maxar.com/proxy/terracotta/")
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    # def get_feature_3d(self, layer, x, y, z):
    # Functionality for get feature call is still not fully understood (2/23/2023). Will update function as knowledge
    # and functionality are increased
    #     """
    #
    #     :param layer:
    #     :param x:
    #     :param y:
    #     :param z:
    #     :return:
    #     """
    #
    #     authorization = process.authorization(self.auth)
