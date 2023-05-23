from MGP_SDK.monitor_service.monitoring import Monitoring


class Interface:
    """
    The primary interface for interacting with the Monitoring class.
    Args:
        username (string) = The username of your user
        password (string) = The password associated with your username
        client_id (string) = The client id associated with your user
    """

    def __init__(self, auth):
        self.auth = auth
        self.monitoring = Monitoring(self.auth)

    def new_monitor(self, source: str, validate=False, **kwargs):
        """
        Creates a new monitor
        Args:
            source (string) = the ID of the event source to listen to
            validate (bool) = Binary whether to validate tasking request. Defaults to False
        Kwargs:
            start_datetime (string) = ISO-8601-formatted datetime string indicating when the monitor should start
            end_datetime (string) = ISO-8601-formatted datetime string indicating when the monitor should end
            description (string) = A human-friendly description of the monitor
            intersects (dict) = A GeoJSON geometry indicating the area of interest for the monitor
            match_criteria (dict) = The fields and values to match against; criteria are specified using a JSON object
            monitor_notifications (list) = Destination(s) where notifications should be sent
            order_templates (list) = Orders to be placed automatically when an event matches the monitor's criteria
        Returns:
            JSON response
        """

        return self.monitoring.create_new_monitor(source, validate, **kwargs)

    def toggle_monitor_status(self, monitor_id: str, status: str):
        """
        Toggles the 'enabled' status of a monitor
        Args:
            monitor_id (string) = the ID of the monitor
            status (string) = enable or disable
        Returns:
            Whether the status change has been accepted
        Throws:
            Exception: If the status provided is already applied to the monitor
        """

        current_status = self.get_monitor(monitor_id)['data']['enabled']
        if (status == 'enable' and current_status is True) or (status == 'disable' and current_status is False):
            raise Exception(f'Monitor {monitor_id} is already {status}d.')
        return self.monitoring.toggle_monitor(monitor_id, status)

    def get_monitor(self, monitor_id: str):
        """
        Retrieves a monitor configuration
        Args:
            monitor_id (string) = the ID of the monitor
        Returns:
            JSON response
        """

        return self.monitoring.get_monitor_by_id(monitor_id)

    def get_monitor_list(self, **kwargs):
        """
        Retrieves a list of monitor configurations
        Kwargs:
            limit (int) = number of monitors to return, defaults to 10
            filter (string) | (string(list)) =  filter results that match values contained in the given key separated by
            a colon
            sort (string) = asc (default) or desc
        Returns:
            JSON response
        Throws:
            ValueError: If limit is not an int and greater than 0.
            Exception: If filter and sort are not formatted properly.
        """

        return self.monitoring.monitor_list(**kwargs)

    def get_monitor_events(self, monitor_id: str, **kwargs):
        """
        Retrieves a list of events for a monitor
        Args:
            monitor_id (string) = the ID of the monitor
        Kwargs:
            filter (string) | (string(list)) = filter results that match values contained in the given key separated by
            a colon. If multiple filters are needed, provide as a list of filters
            sort (string) = asc (default) or desc
        Returns:
            JSON Response
        Throws:
            Exception: If filter and sort are not formatted properly.
        """

        return self.monitoring.monitor_events_list(monitor_id, **kwargs)
