import requests
from MGP_SDK.three_d.three_d import Three_d
import MGP_SDK.process as process

class Interface:
    """
    The primary interface for interacting with the 3D class.
    Args:
        username (string) = The username of your user
        password (string) = The password associated with your username
        client_id (string) = The client id associated with your user
    """

    def __init__(self, auth):
        self.auth = auth
        self.threed = Three_d(self.auth)

    def get_capabilites(self):
        """
        Function lists out all 3D layers and their capabilities
        Returns:
            Dictionary of 3D layers and their information
        """
        return self.threed.get_capabilities_3d()

    def get_coverage(self, bbox, **kwargs):
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
        return self.threed.get_coverage_3d(bbox, **kwargs)

    def get_layer_tileset(self, layer):
        """
        Function provides a tileset.json for the desired 3D layer
        Args:
            layer (string) = The desired 3D layer
        Returns:
            JSON object of the desired 3D layer's information
        """
        return self.threed.get_layer_tileset_3d(layer)

    # def get_feature(self, layer, x, y, z):
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
