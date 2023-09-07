# Discovery Service CLI

### STAC search
Options:

	--collections, -c, Comma-separated list of collections to search in. Use str format not a Python list
	--sub_catalog_id, -scid, Name of the subCatalogId to search in
	--sub_catalog_collection, -scc, Used to denote collections inside of sub catalogs
	--bbox, -b, Bounding box in format "west,south,east,north" in WGS84 decimal degrees
	
	--datetime, -d, Date range filter in ISO 8601 format "start-date/end-date" or exact datetime 
	--stac_id, -sid, Comma-separated list of STAC item IDs to return. Use str format not a Python list 
	--intersects, -i, GeoJSON geometry to search by
	--where, -w, SQL-style WHERE clause for filtering STAC items by properties 
	
	--orderby, -oby, SQL-style ORDER BY clause. Only for id and datetime 
	--limit, -l, Maximum number of items to return. Defaults to 10 
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Returns a list of STAC items

- In the terminal, enter `mgp stac-search` and pass desired flags

Example:

	mgp stac-search -c wv02 -b -d "2015-01-01T00:00:00Z/2016-01-01T00:00:00Z" -oby id -y

### Search audit fields
Options:

	--collection_id, -cid, Identifier of the desired collection. Required
	--audit_insert_date, -aid, Desired insert date in ISO-8601 format. Mutually exclusive with auditUpdateDate. Defaults to None
	--audit_update_date, -aud, Desired update date in ISO-8601 format. Mutually exclusive with auditInsertDate. Defaults to None 
	--limit, -l, Maximum number of items to return. Defaults to 10
Retrieve items for a given collection ID by audit fields

- In the terminal, enter `mgp search-audit-fields` and pass the required flag

Example:

	mgp search-audit-fields -cid wv01 -aud "2023-03-12T00:00:00Z/2023-03-18T12:31:12Z"

### Root catalog
Returns the root STAC Catalog or STAC Collection that is the entry point for users to browse

- In the terminal, enter `mgp root-catalog`

Example:

	mgp root-catalg

### Collection definition
Options:

	--collection_id, -c, Identifier of the desired collection. Required
Return a collection definition by collection ID

- In the terminal, enter `mgp colleciton-definition` and pass the required flag

Example:

	mgp collection-definition wv01

### All collections
Options:

	--orderby, -o, SQL-style ORDER BY clause. Only for id and datetime Ex: 'orderby=id ASC'. Defaults to 'datetime DESC, id ASC'
	--limit, -l, Maximum number of items to return. Defaults to 10
Return definitions for all collections

- In the terminal, enter `mgp all-collections` and pass optional flags if desired

Example:

	mgp all-collections -o "orderby=datetime ASC"

### Get STAC item
Options:

	--colection_id, -c, Identifier of the desired collection. Required
	--item_id, -i, Identifier of the desired item. Required
View details about a specific STAC item

- In the terminal, enter `mgp get-stac-item` and pass the required flags

Example:

	mgp get-stac-item -c wv01 -i STACID

### Top level sub catalog
Options:

	--orderby, -o, SQL-style ORDER BY clause. Only for id and datetime e.g. 'id asc'. Defaults to 'id asc'
	--limit, -l, Maximum number of items to return. Defaults to 10
View the available Maxar Sub-Catalogs that can be navigated as a self-contained STAC catalog

- In the terminal, enter `mgp top-level-sub-catalog` and pass optional flags if desired

Example:

	mgp top-level-sub-catalog -o "orderby=datetime ASC"

### Sub catalog definition
Options:

	--sub_catalog_id, -s, Identifier of the sub catalog to view. Required
View the definition of a Maxar Sub-Catalog

- In the terminal, enter `mgp sub-catalog-defnition` and pass the required flag

Example:

	mgp sub-catalog-definition -s dg-archive

### All sub catalog definitions
Options:

	--sub_catalog_id, -s, Identifier of the sub catalog to view. Required
	--orderby, -o, SQL-style ORDER BY clause. Only for id and datetime e.g. 'id asc'. Defaults to 'id asc'"
	--limit, -l, Maximum number of items to return. Defaults to 10
List the collections that belong to a Sub-Catalog

- In the terminal, enter `mgp all-sub-catalog-definitions` and pass the required flag

Example:

	mgp all-sub-catalog-definitions -s dg-archive -o "datetime desc"

### Sub catalog collection definitions
Options:

	--sub_catalog_id, -s, Identifier of the sub catalog to view. Required
	--sub_catalog_collection_id, -sc, Identifier of the sub catalog collection to view. Required
View the definition of a collection that belongs to a Sub-Catalog

- In the terminal, enter `mgp sub-catalog-collection-definition` and pass the required flags

Example:

	mgp sub-catalog-collection-definition -s dg-archive -sc wv04
