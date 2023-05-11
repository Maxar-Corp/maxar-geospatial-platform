from MGP_SDK.usage_service.usage import Usage


class Interface:

    def __init__(self, auth):
        self.auth = auth
        self.usage = Usage(self.auth)

    def check_usage_is_allowed(self):
        """
        Checks whether usage is allowed for a user

        Returns:
            String API response of whether usage is allowed
        """

        return self.usage.check_usage_is_allowed_by_user()

    def get_usage_overview(self):
        """
        Shows the overview of usage used for the account the user is tied to
        Returns:
            Dictionary of available products and their usage
        """

        return self.usage.check_usage_overview()
