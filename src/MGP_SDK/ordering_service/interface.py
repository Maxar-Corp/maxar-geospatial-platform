from MGP_SDK.ordering_service.orders import Orders
from MGP_SDK.ordering_service.pipelines import Pipelines


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
        self.orders = Orders(self.auth)
        self.pipelines = Pipelines(self.auth)

    def place_order(self, namespace: str, name: str, settings: dict, output_config: dict, metadata: dict, **kwargs):
        """
        Places an order for the given group of pipelines and pipeline name
        Args:
            namespace (string) = A group of pipelines (e.g. 'imagery')
            name (string) = Name of the pipeline to order from (e.g. 'analysis-ready')
            output_config (dict) = Delivery configuration. Amazon S3, Google Cloud Storage, Azure Blob storage
            are supported.
            settings (dict) = settings specific to this pipeline. (required if the requested pipeline requires
            user-provided input parameters and has a json_schema attribute)
        Kwargs:
            notifications (list) = Destination(s) where notifications should be sent. Multiple notifications of the same
            type can be created, each having its own notification level.
            metadata (dict) = supplemental information to attach to this order
            validate (bool) = Binary if user requests to validate order before sending. Defaults to False
        Returns:
            JSON response
        """

        return self.pipelines.post_order_or_get_estimate(namespace, name, settings, output_config, metadata, **kwargs)

    def cancel_order(self, order_id: str):
        """
        Cancels an order if pipeline supports canceling
        Args:
            order_id (int) = The ID of the order you want to cancel
        Returns:
            JSON response
        """

        return self.orders.cancel_order_by_id(order_id)

    def cancel_multiple_orders(self, order_ids: list):
        """
        Cancels orders based on a list containing order IDs
        Args:
            order_ids (list) = List containing order IDs
        Returns:
            JSON response
        """

        for order_id in order_ids:
            print(self.orders.cancel_order_by_id(order_id))
        return

    def get_order_details(self, order_id: str):
        """
        Retrieves the details and status of an Order.
        Args:
            order_id (int) = The ID of the order you are trying to get the details of
        Returns:
            JSON response
        """

        return self.orders.get_order_details(order_id=order_id)

    def get_user_orders(self, user_id: str = None, **kwargs):
        """
        Returns a list of a users order by user ID. If no ID is provided, returns a list of the authenticated user's
        orders

        Args:
            user_id (string) = The identifier of the desired user
        Kwargs:
            limit (int) = Limits the number of responses returned
            filter (list) = Filter results that match values contained in the given key separated by a colon
            sort (string) = Indicates sort order, desc (default) for descending order (newest first) and asc for
            ascending order (oldest first)
            start_date (string) = ISO-8601 formatted date after which to query orders (inclusive)
            end_date (string) = ISO-8601 formatted date before which to query orders (inclusive)
        Returns:
            JSON response
        """

        return self.orders.get_orders_by_user_id(user_id, **kwargs)

    def get_usage_estimate(self, namespace: str, name: str, settings: dict, output_config: dict, metadata: dict, **kwargs):
        """
        Get a usage estimate for the order.
        Args:
            namespace (string) = A group of pipelines (e.g. 'imagery')
            name (string) = Name of the pipeline to order from (e.g. 'analysis-ready')
            output_config (dict) = Delivery configuration. Amazon S3, Google Cloud Storage, Azure Blob storage are
            supported.
            settings (dict) = Settings specific to this pipeline. (required if the requested pipeline requires
            user-provided input parameters and has a json_schema attribute)
        Kwargs:
            metadata (dict) = Supplemental information to attach to this order
            notifications (list) = destination(s) where notifications should be sent. Multiple notifications of the same
            type can be created, each having its own notification level.
        Returns:
            JSON response
        """

        return self.pipelines.post_order_or_get_estimate(namespace, name, settings, output_config, metadata, **kwargs)

    def get_order_events(self, order_id: str, **kwargs):
        """
        Gets events for an order by order ID
        Args:
            order_id (int) = ID of the requested order
        Kwargs:
            limit (int) = Limits the number of responses returned
            filter (list) = Filter results that match values contained in the given key separated by a colon
        Returns:
            JSON response
        """

        return self.orders.get_order_events_by_id(order_id, **kwargs)

    def get_all_pipelines(self):
        """
        List out all available pipelines
        Returns:
            Dictionary of all available pipelines and their information
        """

        return self.pipelines.list_all_pipelines()

    def get_pipeline_details(self, namespace: str, name: str):
        """
        Gets the details for a pipeline by namespace and name
        Args:
            namespace (string) = A group of pipelines (e.g. 'imagery')
            name (string) = Name of the pipeline to order from (e.g. 'analysis-ready')
        Returns:
            JSON response
        """

        return self.pipelines.get_pipeline(namespace, name)
