from MGP_SDK.discovery_service.collections import Collections
from MGP_SDK.discovery_service.search import Search
from MGP_SDK.discovery_service.server_checks import ServerChecks
from MGP_SDK.discovery_service.catalogs import Catalogs


class Interface:

    def __init__(self, auth):
        self.auth = auth
        self.collections = Collections(self.auth)
        self.search = Search(self.auth)
        self.server_checks = ServerChecks(self.auth)
        self.catalogs = Catalogs(self.auth)

    def stac_search(self, **kwargs):
        """
        Returns a list of STAC items
        Keyword Args:
            collections (string) = Comma-separated list of collections to search in. Use str format not a Python list
            sub_catalog_id (string) = Name of the subCatalogId to search in
            sub_catalog_collection (string) = Used to denote collections inside of sub catalogs
            bbox (string) = Bounding box in format "west,south,east,north" in WGS84 decimal degrees
            datetime (string) = Date range filter in ISO 8601 format "start-date/end-date" or exact datetime
            stac_id (string) = Comma-separated list of STAC item IDs to return. Use str format not a Python list
            intersects (string) = GeoJSON geometry to search by
            where (string) = SQL-style WHERE clause for filtering STAC items by properties
            orderby (string) = SQL-style ORDER BY clause. Only for id and datetime e.g. 'orderby=id'
            limit (int) = Maximum number of items to return
        Returns:
            JSON response
        """

        return self.search.stac_search_with_filtering(**kwargs)

    def search_by_audit_fields(self, collection_id: str, **kwargs):
        """
        Retrieve items for a given collectionId by audit fields
        Args:
            collection_id (string) = Name of the collection to search e.g. wv01
        Kwargs:
            audit_insert_date (string) = Date range filter in ISO 8601 format "start-date/end-date" or exact datetime
            audit_update_date (string) = Date range filter in ISO 8601 format "start-date/end-date" or exact datetime
            limit (int) = Maximum number of items to return
        Returns:
            List of STAC ids
        """

        return self.collections.search_stac_by_audit_fields(collection_id, **kwargs)

    def get_root_catalog(self):
        """
        Returns the root STAC Catalog or STAC Collection that is the entry point for users to browse
        Returns:
            JSON response
        """

        return self.server_checks.send_check()

    def get_collection_definition(self, collection_id: str):
        """
        Return a collection definition by collection ID
        Args:
            collection_id (string) = Name of the collection to search e.g. wv01
        Returns:
            JSON response
        """

        return self.collections.get_collection_definition(collection_id=collection_id)

    def get_all_collections(self, **kwargs):
        """
        Return definitions for all collections
        Kwargs:
            orderby (string) = SQL-style ORDER BY clause. Only for id and datetime e.g. 'orderby=id ASC' default
            'datetime DESC, id ASC'
            limit (int) = Maximum number of items to return
        Returns:
            JSON response
        """

        return self.collections.get_collection_definition(**kwargs)

    def get_top_level_sub_catalog(self, **kwargs):
        """
        View the available Maxar Sub-Catalogs that can be navigated as a self-contained STAC catalog
        Keyword Args:
            orderby (string) = SQL-style ORDER BY clause. Only for id and datetime e.g. 'orderby=id ASC' default
            'datetime DESC, id ASC'
            limit (int) = Maximum number of items to return
        Returns:
            JSON response
        """

        return self.catalogs.get_top_level_sub_catalog(**kwargs)

    def get_sub_catalog(self, sub_catalog_id: str):
        """
        View the definition of a Maxar Sub-Catalog
        Args:
            sub_catalog_id (string) = Identifier of the sub catalog to view
        Returns:
            JSON response
        """

        return self.catalogs.get_sub_catalog_definition(sub_catalog_id)

    def get_all_sub_catalog_collections(self, sub_catalog_id: str, **kwargs):
        """
        List the collections that belong to a Sub-Catalog
        Args:
            sub_catalog_id string) = Identifier of the sub catalog to view
        Kwargs:
            orderby (string) = SQL-style ORDER BY clause. Only for id and datetime e.g. 'orderby=id ASC' default
            'datetime DESC, id ASC'
            limit (int) = Maximum number of items to return
        Returns:
            JSON response
        """

        return self.catalogs.get_sub_catalog_collections(sub_catalog_id, **kwargs)

    def get_sub_catalog_collection_definition(self, sub_catalog_id: str, sub_catalog_collection_id: str):
        """
        View the definition of a collection that belongs to a Sub-Catalog
        Args:
            sub_catalog_id (string) = Identifier of the sub catalog to view
            sub_catalog_collection_id (string) = Identifier of the sub catalog collection to view
        Returns:
            JSON response
        """

        return self.catalogs.get_collection_in_sub_catalog(sub_catalog_id, sub_catalog_collection_id)

    def get_specifications(self):
        """
        Returns information about specifications that this API conforms to
        Returns:
            JSON response
        """

        return self.server_checks.send_check(endpoint='conformance')

    def healthcheck(self):
        """
        Return the service's health and the health of each of its dependent services
        Returns:
            JSON response
        """

        return self.server_checks.send_check(endpoint='healthcheck')

    def get_status(self):
        """
        Return the service's status
        Returns:
            JSON response
        """

        return self.server_checks.send_check(endpoint='status')
