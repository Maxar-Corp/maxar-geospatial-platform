from MGP_SDK.streaming.interface import Interface as streaming_interface
from MGP_SDK.account_service.interface import Interface as account_interface
from MGP_SDK.auth.auth import Auth
from MGP_SDK.token_service.token import Token
from MGP_SDK.three_d.interface import Interface as three_d_interface
from MGP_SDK.basemap_service.interface import Interface as basemap_interface
from MGP_SDK.discovery_service.interface import Interface as discovery_interface
from MGP_SDK.monitor_service.interface import Interface as monitoring_interface
from MGP_SDK.ordering_service.interface import Interface as order_interface
from MGP_SDK.tasking_service.interface import Interface as tasking_interface
from MGP_SDK.usage_service.interface import Interface as usage_interface
from MGP_SDK.analytics_service.interface import Interface as analytics_interface


class Interface:

    def __init__(self, *args):

        if len(args) > 0:
            try:
                username = args[0]
                password = args[1]
                client_id = args[2]
            except:
                raise Exception("MGP-config file not formatted correctly")
            self.auth = Auth(username, password, client_id)
        else:
            self.auth = Auth()

        self.streaming = streaming_interface(self.auth)
        self.account_service = account_interface(self.auth)
        self.token = Token(self.auth)
        self.order_service = order_interface(self.auth)
        self.three_d = three_d_interface(self.auth)
        self.monitoring_service = monitoring_interface(self.auth)
        self.basemap_service = basemap_interface(self.auth)
        self.discovery_service = discovery_interface(self.auth)
        self.tasking_service = tasking_interface(self.auth)
        self.usage_service = usage_interface(self.auth)
        self.analytics = analytics_interface(self.auth)

