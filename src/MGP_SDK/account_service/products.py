import requests
import warnings
import MGP_SDK.process as process

warnings.filterwarnings("ignore")


class Products:

    def __init__(self, auth):
        self.base_url = auth.api_base_url
        self.response = None
        self.version = auth.version
        self.auth = auth

    def get_products(self):
        """
        Gets a list of all products
        Returns:
             A list of dictionaries of products and their detials
        """

        authorization = process.authorization(self.auth)
        url = "{}/account-service/api/v1/products".format(self.base_url)
        response = requests.request("GET", url, headers=authorization, verify=self.auth.SSL)
        process._response_handler(response)
        return response.json()

    def filter_products(self, product_category=None, usage_type=None, age=None, catalog_type=None):
        """
        Filters products based on args passed in
        Args:
            product_category (string) = The desired product category
            usage_type (string) = Desired usage type (Download or Streaming)
            age (string) = Desired age of the product. ex [3,91)
            catalog_type (string) = Desired catalog type (Archive or Online)
        Returns:
            List of dictionaries of the products that you are filtering for
        """

        all_products = self.get_products()
        self._paramater_checker(product_category, usage_type, catalog_type)
        filtered_products = [i for i in all_products if
                             (i['productCategory'].lower() == str(product_category).lower() or not product_category)
                             and (i['usageType'] == str(usage_type) or not usage_type)
                             and (i['age'] == str(age) or not age)
                             and (i['catalogType'] == str(catalog_type).lower() or not catalog_type)]
        return filtered_products

    def _paramater_checker(self, product_category, usage_type, catalog_type):
        all_products = self.get_products()
        if product_category:
            acceptable_product_category = [i['productCategory'] for i in all_products]
            if product_category not in acceptable_product_category:
                raise Exception('Please input correct Product category. {}'.format(acceptable_product_category))
        if usage_type:
            usage_types = ['Streaming', 'Download']
            if usage_type not in usage_types:
                raise Exception('Please enter acceptable UsageType. {}'.format(usage_types))
        if catalog_type:
            catalog_types = ['Online', 'Archive']
            if catalog_type not in catalog_types:
                raise Exception('Please enter acceptable UsageType. {}'.format(catalog_types))
