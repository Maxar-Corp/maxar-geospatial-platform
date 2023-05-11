import requests
import warnings
import MGP_SDK.process as process

warnings.filterwarnings('ignore')


class Usage:

    def __init__(self, auth):
        self.auth = auth
        self.api_version = self.auth.api_version
        self.base_url = f'{self.auth.api_base_url}/account-service/api/{self.api_version}'
        self.token = self.auth.refresh_token()
        self.authorization = {"Authorization": f"Bearer {self.token}"}

    def get_account_usage(self, **kwargs):
        """
        Function lists the usage for an account or accounts
        Kwargs:
            page (int) = Desired starting page. First page is page 0
            pageSize (int) = Desired amount of returned objects
            sortBy (string) = Desired sorting arrangement. Available options are:
                id
                accountNumber
                sapLicenseId
                licensee
                soldTo
                totalCreditsUsed
                numberOfActivations
                numberOfUsers
        Returns:
            Dictionary of account(s) usage
        """

        if 'page' in kwargs.keys():
            try:
                int(kwargs['page'])
                assert kwargs['page'] >= 0
            except:
                raise ValueError("page must be an integer of 0 or greater. Page provided: {}".format(kwargs['page']))
        if 'pageSize' in kwargs.keys():
            try:
                int(kwargs['pageSize'])
                assert kwargs['pageSize'] > 0
            except:
                raise ValueError("pageSize must be an integer greater than 0. Limit provided: {}".format(['pageSize']))
        if 'sortBy' in kwargs.keys():
            sort_list = ['id', 'accountNumber', 'name', 'sapLicenseId', 'licensee', 'soldTo', 'totalCreditsUsed',
                         'numberOfActivations', 'numberOfUsers']
            if kwargs['sortBy'] not in sort_list:
                raise Exception("sortBy must utilize one of the following parameters: {}".format(tuple(sort_list)))
        url = f'{self.base_url}/accounts/usage'
        kwarg_list = ['page', 'pageSize', 'sortBy']
        params = {**{k: v for k, v in kwargs.items() if k in kwarg_list}}
        response = requests.get(url, params=params, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_activation_usage(self, **kwargs):
        """
        Function lists the usage for an activation or activations
        Kwargs:
            page (int) = Desired starting page. First page is page 0
            pageSize (int) = Desired amount of returned objects
            sortBy (string) = Desired sorting arrangement. Available options are:
                id
                activationNumber
                sapContractIdentifier
                sapLineItem
                startDate
                endDate
                creditLimit
                totalCreditsUsed
                creditsUsedPercentage
                numberOfUsers
                totalUsers
                accountTotalUsers
                accountName
                accountNumber
                accountSapLicenseId
                accountLicensee
                accountSoldTo
                userLimit
                dailyCreditLimitTotal
                dailyCreditLimitUsed
                clientContextId
            clientContextId (string) = Desired client ID
        Returns:
            Dictionary of activation(s) usage
        """

        if 'page' in kwargs.keys():
            try:
                int(kwargs['page'])
                assert kwargs['page'] >= 0
            except:
                raise ValueError("page must be an integer of 0 or greater. Page provided: {}".format(kwargs['page']))
        if 'pageSize' in kwargs.keys():
            try:
                int(kwargs['pageSize'])
                assert kwargs['pageSize'] > 0
            except:
                raise ValueError("pageSize must be an integer greater than 0. Limit provided: {}".format(kwargs['pageSize']))
        if 'sortBy' in kwargs.keys():
            sort_list = ['id', 'activationNumber', 'sapContractIdentifier', 'sapLineItem', 'startDate', 'endDate',
                         'creditLimit', 'totalCreditsUsed', 'creditsUsedPercentage', 'numberOfUsers', 'totalUsers',
                         'accountTotalUsers', 'accountName', 'accountNumber', 'accountSapLicenseId', 'accountLicensee',
                         'accountSoldTo', 'userLimit', 'dailyCreditLimitTotal', 'dailyCreditLimitUsed',
                         'clientContextId']
            if kwargs['sortBy'] not in sort_list:
                raise Exception("sortBy must utilize one of the following parameters: {}".format(tuple(sort_list)))
        if 'clientContextId' in kwargs.keys():
            try:
                str(kwargs['clientContextId'])
            except:
                raise ValueError("clientContextId must be an alpha-numeric string. clientContextId provided: {}"
                                 .format(kwargs['clientContextId']))
        url = f"{self.base_url}/activations/usage"
        kwarg_list = ['page', 'pageSize', 'sortBy', 'clientContextId']
        params = {**{k: v for k, v in kwargs.items() if k in kwarg_list}}
        response = requests.get(url, params=params, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def get_user_usage(self, **kwargs):
        """
        Function lists the usage for a user or users
        Kwargs:
            page (int) = Desired starting page. First page is page 0
            pageSize (int) = Desired amount of returned objects
            sortBy (string) = Desired sorting arrangement. Available options are:
                id
                username
                accountId
                activationNumber
                accountNumber
                accountSapLicenseId
                accountLicensee
                accountSoldTo
                totalCreditsUsed
                dailyCreditLimitTotal
                dailyCreditLimitUsed
                userType
                clientContextId
            clientContextId (string) = Desired client ID
        Returns:
            Dictionary of user(s) usage
        :return:
        """

        if 'page' in kwargs.keys():
            try:
                int(kwargs['page'])
                assert kwargs['page'] >= 0
            except:
                raise ValueError("page must be an integer of 0 or greater. Page provided: {}".format(kwargs['page']))
        if 'pageSize' in kwargs.keys():
            try:
                int(kwargs['pageSize'])
                assert kwargs['pageSize'] > 0
            except:
                raise ValueError("pageSize must be an integer greater than 0. Limit provided: {}".format(kwargs['pageSize']))
        if 'sortBy' in kwargs.keys():
            sort_list = ['id', 'username', 'accountId', 'activationNumber', 'accountNumber', 'accountSapLicenseId',
                         'accountLicensee', 'accountSoldTo', 'totalCreditsUsed', 'dailyCreditLimitTotal',
                         'dailyCreditLimitUsed', 'userType', 'clientContextId']
            if kwargs['sortBy'] not in sort_list:
                raise Exception("sortBy must utilize one of the following parameters: {}".format(tuple(sort_list)))
        if 'clientContextId' in kwargs.keys():
            try:
                str(kwargs['clientContextId'])
            except:
                raise ValueError("clientContextId must be an alpha-numeric string. clientContextId provided: {}"
                                 .format(kwargs['clientContextId']))
        url = f"{self.base_url}/users/usage"
        kwarg_list = ['page', 'pageSize', 'sortBy', 'clientContextId']
        params = {**{k: v for k, v in kwargs.items() if k in kwarg_list}}
        response = requests.get(url, params=params, headers=self.authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()
