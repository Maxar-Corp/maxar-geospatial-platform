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
- [Create Raster URL](#raster-url--raster_url)
- [Get Raster Arrays](#get-arrays--get_arrays)
- [Download Raster](#download-raster--download_raster)
- [Search Vector Layer](#search-vector-layer--search_vector_layer)
- [Download Vector Analytics](#download-vector-analytics--download_vector_analytics)
- [Download Vector Tiles](#download-vector-tiles--download_vector_tiles)

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

### Create Raster URL / raster_url()
Formats a vsicurl URL to be utilized with further raster functions<br>
**Returns**: URL formatted with desired parameters and /vsicurl/ prefix<br>
Args:<br>
**script_id**: (string) Desired IPEScript (e.g. "ortho-image")<br>
**function**: (string) Desired function of the IPEScript (e.g. "ortho")<br>
**collect_id**: (string) Desired raster image ID<br>
**api_token**: (string) User's maxar_api_token<br>
**crs**: (string) Default="UTM". Desired projection<br>
Keyword Arguments:<br>
**bands**: (string) Comma separated string of desired bands (e.g. "red,green.blue")<br>
**dra**: (string) Binary of whether or not to apply dra to the raster. String of bool ("true", "false")<br>
**interpolation**: (string) Desired resizing or (re)projection from one pixel grid to another<br>

```python
response = analytics.raster_url(script_id="ortho-image", function="ortho", collect_id="<collectID>", api_token="<yourAPIToken>", bands="red,green,blue", dra="true")
print(response)
```

### Get Raster Arrays / get_arrays()
Lists out the arrays of a raster<br>
**Returns**: List of arrays of the raster's pixels<br>
Args:<br>
**raster_url**: (string) Vsicurl formatted URL of a raster object<br>
**xoff**: (int) Number of pixels to offset on the x axis<br>
**yoff**: (int) Number of pixels to offset on the y axis<br>
**width**: (int) Number of pixels for the returned raster on the x axis<br>
**height**: (int) Number of pixels for the returned raster on the y axis<br>

```python
response = analytics.get_arrays(raster_url="<vsicurl-formatted-URL>", xoff=3067, yoff=2045, width=2045, height=2045)
print(response)
```

### Download Raster / download_raster()
Download a rasterized image from a raster array<br>
**Returns**: Success message of download location<br>
Args:<br>
**raster_array**: (list(list)) Generated raster array<br>
**outputpath**: (string) Desired outputpath for the rasterized image including file extension<br>

```python
response = analytics.download_raster(raster_array=[<raster-array>], outputpath=r"your\output\path\image.extension")
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
**format**: (string) The format of the response image either jpeg, png or geotiff<br>
**outputpath**: (string) Output path must include output format. Downloaded path default is user home path<br>
**display**: (bool) Default=False, Display image in IDE (Jupyter Notebooks only)<br>

```python
response = analytics.download_vector_analytics(layers="VIVID_BASIC", bbox="miny,minx,maxy,maxx", height=256, width=256, format="jpeg", outputpath=r"your\output\path\image.extension")
print(response)
```

### Download Vector Tiles / download_vector_tiles()
Function downloads vector imagery using the wmts method<br>
**Returns**: Downloaded file path<br>
Args:<br>
**layers**: (string) String specifying the layers to download<br>
**zoom_level**: (int) The desired zoom level<br>
**bbox**: (string) Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
**srsname**: (string) Default="EPSG:4326", Desired projection<br>
**outputpath**: (string) Output path must include output format. Downloaded path default is user home path<br>
**display**: (bool) Default=False, Display image in IDE (Jupyter Notebooks only)<br>

```python
response = analytics.download_vector_tiles(layers="VIVID_BASIC", zoom_level=15, bbox="miny,minx,maxy,maxx", outputpath=r"your\output\path\image.extension")
print(response)
```
