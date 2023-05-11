# Analytics
<hr>

The Analytics portion of the MGP_SDK provides an interface for Raster and Vector Analytics operations in the Maxar Geospatial Platform.

### Getting Started: 
```python
from MGP_SDK.interface import Interface

analytics = Interface(auth)
```

### Package methods:

- [Get Image Metadata Raster](#get-image-metadata-raster--get_image_metadata_raster)
- [Get Byte Range Raster](#get-byte-range-raster--get_byte_range_raster)
- [Search Vector Layer](#search-vector-layer--search_vector_layer)
- [Download Vector Analytics](#download-vector-analytics--download_vector_analytics)

### Get Image Metadata Raster / get_image_metadata_raster()
Function gets metadata about an image given an IPE resource ID, function name, and parameters<br>
**Returns**: Response JSON object containing the metadata about an image.<br>
Args:<br>
**function**: (string) The function to process (e.g. "pansharp")<br>
**script_id**: (string) Desired script ID<br>
Keyword Arguments:<br>
**function_parameters**: (string) The function parameters if required<br>

```python
response = analytics.get_image_metadata_raster(function="pansharp", script_id="your_script_id")
print(response)
```

### Get Byte Range Raster / get_byte_range_raster()
Function returns a virtual image as GeoTIFF given a script ID, function name, function parameters, and a valid byte range.<br>
**Returns**: Response JSON object containing the byte range information.<br>
Args:<br>
**function**: (string) The function to process (e.g. "pansharp")<br>
**script_id**: (string) Desired script ID<br>
**prefetch**: (bool) Default=True, Prefetching true or false<br>
**head_request**: (bool) Default=False, Boolean indicating if it should be a HEAD HTTP request instead of a GET to return only response headers<br>
Keyword Arguments:<br>
**function_parameters**: (string) The function parameters if required<br>

```python
response = analytics.get_byte_range_raster(function="pansharp", script_id="your_script_id")
print(response)
```

### Search Vector Layer / search_vector_layer()
Function searches using the WFS method<br>
**Returns**: Response is either a list of features or a shapefile of all features and associated metadata.<br>
Args:<br>
**layers**: (string) String specifying the layers to search<br>
**bbox**: (string) Default=None, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
**srsname**: (string) Default="EPSG:4326", Desired projection<br>
**filter**: (string) Default=None, CQL filter used to refine data of search.<br>
**shapefile**: (bool) Default=False, Binary of whether to return as shapefile format<br>
**csv**: (bool) Default=False, Binary of whether to return as a CSV format<br>
Keyword Arguments:<br>
**featureprofile**: (string) The desired stacking profile. Defaults to account Default<br>
**typename**: (string) The typename of the desired feature type. Defaults to FinishedFeature<br>

```python
response = analytics.search_vector_layer(layers="your_layers", bbox="miny,minx,maxy,maxx")
print(response)
```

### Download Vector Analytics / download_vector_analytics()
Function downloads the image using the WMS method<br>
**Returns**: requests response object or downloaded file path<br>
Args:<br>
**layers**: (string) String specifying the layers to download<br>
**bbox**: (string) Default=None, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
**srsname**: (string) Default="EPSG:4326", Desired projection<br>
**height**: (int) Default=512, The vertical number of pixels to return<br>
**width**: (int) Default=512, The horizontal number of pixels to return<br>
**format**: (string)

