# Discovery
The Discovery portion of the MGP_SDK enables customers to discover products that are available to order or stream.

The Maxar Geospatial Platform (MGP) uses the SpatioTemporal Asset Catalog (STAC) specification. A STAC catalog stores 
geospatial features that are queryable by location and time, as well as by custom properties stored in each feature. A 
single geospatial feature is represented in the Maxar catalog by a GeoJSON feature.

All of the data served and managed by the Maxar Discovery API follow the STAC specification and implements a STAC API.

### Getting Started
```python
from MGP_SDK.interface import Interface

discovery = Interface().discovery_service
```

### Package methods

- [Stac Search](#stac-search--stac_search)
- [Audit Search](#audit-search--search_by_audit_fields)
- [Get Root Catalog](#get-root-catalog--get_root_catalog)
- [Get All Collections](#get-all-collections--get_call_collections)
- [Get Collection Definition](#get-collection-definition--get_collection_definition)
- [Get Top Level Sub Catalog](#get-top-level-sub-catalog--get_top_level_sub_catalog)
- [Get A Sub Catalog](#get-a-sub-catalog--get_sub_catalog)
- [Get All Sub Catalog Collections](#get-all-sub-catalog-collections--get_all_sub_catalog_collections)
- [Get A Sub Catalog Collection Definition](#get-a-sub-catalog-collection-definition--get_sub_catalog_collection_definition)
- [Get Specifications](#get-specifications--get_specifications)
- [Get Healthcheck](#get-healthcheck--get_healthcheck)
- [Get Status](#get-status--get_status)

## Discovery

### STAC Search / stac_search()
STAC search searches through the Maxar catalog and returns a Feature Collection of STAC items based on the filters 
provided<br>
Keyword Arguments:<br>
**collections**: str, Comma-separated list of collections to search in. Use str format not a Python list<br>
**sub_catalog_id**: str, name of the subCatalogId to search in<br>
**sub_catalog_collection**: str, used to denote collections inside of sub catalogs<br>
**bbox**: str, Bounding box in format "west,south,east,north" in WGS84 decimal degrees<br>
**datetime**: str, Date range filter in ISO 8601 format "start-date/end-date" or exact datetime<br>
**stac_id**: str, Comma-separated list of STAC item IDs to return. Use str format not a Python list<br>
**intersects**: str, GeoJSON geometry to search by<br>
**where**: str, SQL-style WHERE clause for filtering STAC items by properties<br>
**orderby**: SQL-style ORDER BY clause. Only for id and datetime e.g. 'orderby=id'<br>
**limit**: int, Maximum number of items to return<br>

```python
from MGP_SDK.interface import Interface

discovery = Interface().discovery_service

# Get all STAC items in a given location
stac = discovery.stac_search(bbox='-105,40,-104,41')

# Filter by collection
stac = discovery.stac_search(bbox='-105,40,-104,41', collections='wv01, wv04')

# Filter by sub catalog
stac = discovery.stac_search(bbox='-105,40,-104,41', sub_catalog_id='dg-archive')

# Filter by sub catalog collection
stac = discovery.stac_search(bbox='-105,40,-104,41', sub_catalog_id='dg-archive', sub_catalog_collection='wv04')

# Provide conditional filtering
stac = discovery.stac_search(bbox='-105,40,-104,41', where='eo:cloud_cover < 10')

# Filter by date
stac = discovery.stac_search(bbox='-105,40,-104,41', collections='wv01, wv04', 
                             datetime='2022-01-01T00:00:00Z/2022-05-023T00:00:00Z')

# Manipulate the output
stac = discovery.stac_search(bbox='-105,40,-104,41', where='eo:cloud_cover < 10', orderby='datetime asc', limit=15)

# Get a specific STAC by ID
stac = discovery.stac_search(stac_id='160623e2-69dd-4aba-9354-a6d685d28190-inv')

# Get a list by STAC IDs
stac = discovery.stac_search(stac_id='0d1e2b78-aeb0-493e-b046-561265c6735b-inv, 385c2a01-d880-4662-9bef-adde996cf810-inv')
```

### Example Response
<details><summary>Click Me</summary>

```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "id": "10200100D8CB1D00",
            "bbox": [
                -104.901204,
                39.686511,
                -104.664848,
                40.011546
            ],
            "type": "Feature",
            "links": [
                {
                    "rel": "collection",
                    "href": "https://api.maxar.com/discovery/v1/collections/wv01",
                    "type": "application/json"
                },
                {
                    "rel": "root",
                    "href": "https://api.maxar.com/discovery/v1/collections/dg-archive",
                    "type": "application/json"
                },
                {
                    "rel": "self",
                    "href": "https://api.maxar.com/discovery/v1/collections/wv01/items/10200100D8CB1D00",
                    "type": "application/geo+json"
                },
                {
                    "rel": "order-map-ready",
                    "href": "https://api.maxar.com/ordering/v1/pipelines/imagery/map-ready/order",
                    "type": "application/json"
                }
            ],
            "assets": {
                "browse": {
                    "href": "https://api.maxar.com/discovery/v1/collections/wv01/items/10200100D8CB1D00/assets/collections/dg-archive/assets/browse/10200100D8CB1D00.browse.tif",
                    "type": "image/tiff; application=geotiff",
                    "title": "Browse Image"
                },
                "cloud-cover": {
                    "href": "https://api.maxar.com/discovery/v1/collections/wv01/items/10200100D8CB1D00/assets/collections/wv01/assets/cloud-cover/10200100D8CB1D00.cloud.json",
                    "type": "application/geo+json",
                    "title": "Cloud Cover"
                },
                "sample-point-set": {
                    "href": "https://api.maxar.com/discovery/v1/collections/wv01/items/10200100D8CB1D00/assets/collections/wv01/assets/sample-point-sets/10200100D8CB1D00.sample-points.json",
                    "type": "application/geo+json",
                    "title": "Sample Point Set"
                },
                "wms": {
                    "href": "https://api.maxar.com/wms/v1/ogc/ows?cql_filter=legacyIdentifier=%2710200100D8CB1D00%27&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/jpeg&TRANSPARENT=true&LAYERS=Maxar:Imagery&TILED=true&WIDTH=2500&HEIGHT=2500&CRS=EPSG%3A4326&STYLES=raster&BBOX=-104.901204,39.686511,-104.664848,40.011546",
                    "type": "image/jpeg",
                    "title": "WMS"
                }
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [...]
            },
            "collection": "wv01",
            "properties": {
                "gsd": 0.570604214,
                "title": "Maxar WV01 Image 10200100D8CB1D00",
                "datetime": "2023-05-03T21:01:37.154212Z",
                "eo:bands": [
                    {
                        "name": "pan",
                        "center_wavelength": 650
                    }
                ],
                "platform": "worldview-01",
                "instruments": [
                    "VNIR"
                ],
                "associations": [],
                "view:azimuth": 134.029484,
                "constellation": "maxar",
                "off_nadir_avg": 22.2942504,
                "off_nadir_end": 20.915253,
                "off_nadir_max": 24.240393,
                ...
            },
            "stac_version": "1.0.0",
            "stac_extensions": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
                "https://stac-extensions.github.io/view/v1.0.0/schema.json"
            ]
        }
    ],
    "numberReturned": 1,
    "timestamp": "2023-05-04T15:28:06.925108Z",
    "links": [
        {
            "rel": "next",
            "href": "https://api.maxar.com/discovery/v1/search?bbox=-105%2C40%2C-104%2C41&collections=wv01%2C+wv04&limit=1&page=2"
        }
    ]
}
```
</details>

### Audit Search / search_by_audit_fields()
Retrieve items for a given collectionId by audit fields. Only update date or insert date may be provided, not both<br>
Keyword Arguments:<br>
**collection_id**: str, name of the collection to search e.g. wv01<br>
**audit_insert_date**: str, Date range filter in ISO 8601 format "start-date/end-date" or exact datetime<br>
**audit_update_date**: str, Date range filter in ISO 8601 format "start-date/end-date" or exact datetime<br>
**limit**: int, Maximum number of items to return<br>
Returns: List of STAC IDs matching the provided filters <br>
```python
stac_results = discovery.stac_search(collection_id='wv04', audit_insert_date='2023-03-12T00:00:00Z/2023-03-15T12:31:12Z')

stac_results_2 = discovery.stac_search(collection_id='ge01', audit_update_date='2023-03-12T00:00:00Z/2023-03-15T12:31:12Z', 
                                       limit=15)
```

### Get Root Catalog / get_root_catalog()
Returns the root STAC Catalog or STAC Collection that is the entry point for users to browse<br>
```python
root = discovery.get_root_catalog()
```

### Get All Collections / get_call_collections()
Return definitions for all collections<br>
Keyword Arguments:<br>
**orderby**: str, SQL-style ORDER BY clause. Only for id and datetime e.g. 'orderby=id ASC' default 'datetime DESC, id ASC'<br>
**limit**: int, Maximum number of items to return<br>
Returns: JSON response
```python
collections = discovery.get_all_collections(limit=7, orderby='id')
```

### Get Collection Definition / get_collection_definition()
Return a collection definition by collection ID
Arguments:<br>
**collection_id**: str, name of the collection to search e.g. wv01<br>
Returns: JSON response
```python
collection = discovery.get_collection_definition('wv01')
```

### Get Top Level Sub Catalog / get_top_level_sub_catalog()
View the available Maxar Sub-Catalogs that can be navigated as a self-contained STAC catalog<br>
Keyword Arguments:<br>
**orderby**: str, SQL-style ORDER BY clause. Only for id and datetime e.g. 'orderby=id ASC' default 'datetime DESC, id ASC'<br>
**limit**: int, Maximum number of items to return<br>
Returns: JSON response
```python
collections = discovery.get_top_level_sub_catalog(limit=5)
```

### Get a Sub Catalog / get_sub_catalog()
View the definition of a Maxar Sub-Catalog<br>
Arguments:<br>
**sub_catalog_id**: str, ID of the sub catalog to view<br>
Returns: JSON response
```python
sub_catalog = discovery.get_sub_catalog('dg-archive')
```

### Get All Sub Catalog Collections / get_all_sub_catalog_collections()
List the collections that belong to a Sub-Catalog<br>
Keyword Arguments:
**sub_catalog_id**: str, ID of the sub catalog to view<br>
**orderby**: SQL-style ORDER BY clause. Only for id and datetime e.g. 'orderby=id ASC' default 'datetime DESC, id ASC'<br>
**limit**: int, Maximum number of items to return<br>
Returns: JSON response<br>
```python
sub_collections = discovery.get_all_sub_catalog_collections(sub_catalog_id='dg-archive', orderby='datetime asc')
```

### Get a Sub Catalog Collection Definition / get_sub_catalog_collection_definition()
View the definition of a collection that belongs to a Sub-Catalog<br>
Keyword Arguments:<br>
**sub_catalog_id**: str, ID of the sub catalog to view<br>
**sub_catalog_collection_id**: str, ID of the sub catalog collection to view<br>
Returns: JSON response
```python
sub_catalog = discovery.get_sub_catalog_collection_definition(sub_catalog_id='dg-archive', 
                                                              sub_catalog_collection_id='wv04')
```

### Get Specifications / get_specifications()
Returns information about specifications that this API conforms to<br>
Returns: JSON response
```python
spec = discovery.get_specifications()
```

### Get Healthcheck / get_healthcheck()
Return the service's health and the health of each of its dependent services<br>
Returns: JSON response
```python
spec = discovery.get_healthcheck()
```

### Get Status / get_status()
Return the service's status<br>
Returns: JSON response
```python
spec = discovery.get_status()
```




