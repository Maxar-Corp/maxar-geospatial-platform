from MGP_SDK.tasking_service.tasking import Tasking


class Interface:
    """
    The primary interface for interacting with the Orders class.
    Args:
        username (string) = The username of your user
        password (string) = The password associated with your username
        client_id (string) = The client id associated with your user
    """

    def __init__(self, auth):
        self.auth = auth
        self.tasking = Tasking(self.auth)

    def new_tasking(self, start_datetime: str, end_datetime: str, aoi_geojson: dict, recipe: str, order_templates: dict,
                    **kwargs):
        """
        Initiates the creating of a tasking (async) using one of the preconfigured recipes: 50cm_Color, 30cm_Color.
        If a kwarg is null or not provided, default recipe value will be used
        Args:
            start_datetime (string) = ISO-8601 formatted date when the tasking should start
            end_datetime (string) = ISO-8601 formatted date when the tasking should end
            aoi_geojson (dict) = Geojson polygon of area to cover with tasking, e.g.
            {"type":"Polygon","coordinates":[[[...]]]}
            recipe (string) = The name of one of the configured recipes for tasking, e.g. "50cm_Color" or "30cm_Color"
            order_templates (list) = Template for order to be placed. See ordering_service for examples
        Kwargs:
            max_cloud_cover (string) = Maximum cloud cover.
            max_off_nadir_angle (string) = Maximum off nadir angle.
            max_sun_elevation_angle (string) = Maximum sun elevation angle.
        Returns:
            Dictionary of submitted tasking request's details
        Throws:
            ValueError: If start or end times are not in ISO-8601 format
        """

        return self.tasking.create_new_tasking(start_datetime, end_datetime, aoi_geojson, recipe, order_templates,
                                               **kwargs)

    def get_tasking_request(self, tasking_id: str):
        """
        Retrieves a tasking
        Args:
            tasking_id (string) = ID of the requested tasking
        Returns:
            Dictionary of a tasking request and its details
        """

        return self.tasking.tasking_info(tasking_id)

    def cancel_tasking(self, tasking_id: str, reason: str = None):
        """
        Initiates the canceling of a tasking (async)
        Args:
            tasking_id (string) = ID of the requested tasking
            reason (string) = Reason for canceling the tasking
        Returns:
            Dictionary of cancelled tasking request's details
        """

        return self.tasking.cancel_tasking(tasking_id, reason)

    def tasking_list(self, **kwargs):
        """
        Retrieves a page listing of all taskings based upon query parameters. Limited to the authenticated user's group.
        Kwargs:
            limit (int) = How many items to return in the response list. Default 10
            filter (list) = Filter results that match values contained in the given key separated by a colon.
            sort (string) = Indicates sort order, asc (default) for ascending order (alphabetical by name) and desc for
            descending order (reverse alphabetical by name)
        Returns:
            Dictionary of tasking requests and their details
        """

        return self.tasking.get_tasking_list(**kwargs)

