# Analytics
<hr>

The Analytics portion of the MGP_SDK provides an interface for Raster and Vector Analytics operations in the Maxar Geospatial Platform.

### Getting Started: 
```python
from MGP_SDK.interface import Interface

analytics = Interface().analytics
```

### Package methods:

- [Create Raster URL](#raster-url)
- [Raster Metadata](#raster-metadata)
- [Get Raster Arrays](#get-arrays)
- [Download Raster](#download-raster)
- [Search Vector Layer](#search-vector-layer)
- [Download Vector Analytics](#download-vector-analytics)
- [Download Vector Tiles](#download-vector-tiles)

### Create Raster URL / raster_url()
Formats a vsicurl URL to be utilized with further raster functions<br>

**Returns**: URL formatted with desired parameters and /vsicurl/ prefix<br>

**Args:<br>**

* script_id: (*str*) Desired IPEScript (e.g. "ortho-image")<br>
* function: (*str*) Desired function of the IPEScript (e.g. "ortho")<br>
* collect_id: (*str*) Desired raster image ID<br>
* api_token: (*str*) User's maxar_api_token<br>
* crs: (*str*) Default="UTM". Desired projection<br>

**Kwargs:<br>**
* bands: (*str*) Comma separated string of desired bands (e.g. "red,green.blue")<br>
* dra: (*str*) Binary of whether or not to apply dra to the raster. String of bool ("true", "false"). Defaults to false<br>
* interpolation: (*str*) Desired resizing or (re)projection from one pixel grid to another<br>
* acomp: (*str*) Binary of whether or not to apply atmospheric compensation to the output after hd (if applied) and before dra. String of bool ("true", "false"). Defaults to false<br>
* hd: (*str*) Binary of whether or not to apply higher resolution to the output. String of bool ("true", "false"). Defaults to false<br>

```python
response = analytics.raster_url(script_id="ortho-image", function="ortho", collect_id="<collectID>", api_token="<yourAPIToken>", bands="red,green,blue", dra="true")
print(response)
```
___

### Raster Metadata 

**raster_metadata()**

Lists out various metadata information of a desired raster<br>

**Returns**: Dictionary of various raster metadata information<br>

**Args:<br>**

* raster_url: (*str*) Vsicurl formatted URL of a raster object<br>

```python
response = analytics.raster_metadata(raster_url="<vsicurl-formatted-URL>")
print(response)
```
___

### Get Raster Arrays 
**get_arrays()**

Lists out the arrays of a raster<br>

**Returns**: List of arrays of the raster's pixels<br>

**Args:<br>**
* raster_url: (*str*) Vsicurl formatted URL of a raster object<br>
* xoff: (*int*) Number of pixels to offset on the x axis<br>
* yoff: (*int*) Number of pixels to offset on the y axis<br>
* width: (*int*) Number of pixels for the returned raster on the x axis<br>
* height: (*int*) Number of pixels for the returned raster on the y axis<br>

```python
response = analytics.get_arrays(raster_url="<vsicurl-formatted-URL>", xoff=3067, yoff=2045, width=2045, height=2045)
print(response)
```
___

### Download Raster 
**download_raster()**

Download a rasterized image from a raster array<br>

**Returns**: Success message of download location<br>

**Args:<br>**
* raster_array: (*list(list)*) Generated raster array<br>
* outputpath: (*str*) Desired outputpath for the rasterized image including file extension<br>

```python
response = analytics.download_raster(raster_array=[<raster-array>], outputpath=r"your\output\path\image.extension")
print(response)
```
___

### Search Vector Layer 
**search_vector_layer()**

Function searches using the WFS method<br>

**Returns**: Response is either a list of features or a shapefile of all features and associated metadata.<br>

**Args:<br>**

* layers: (*str*) String specifying the layers to search<br>
* bbox: (*str*) Default=`None`, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
* srsname: (*str*) Default="EPSG:4326", Desired projection<br>
* filter: (*str*) Default=`None`, CQL filter used to refine data of search.<br>
* shapefile: (*bool*) Default=`False`, Binary of whether to return as shapefile format<br>
* csv: (*bool*) Default=`False`, Binary of whether to return as a CSV format<br>

**Kwargs:<br>**

* featureprofile: (*str*) The desired stacking profile. Defaults to account Default<br>
* typename: (*str*) The typename of the desired feature type. Defaults to FinishedFeature<br>

```python
response = analytics.search_vector_layer(layers="your_layers", bbox="miny,minx,maxy,maxx")
print(response)
```
___

### Download Vector Analytics 
**download_vector_analytics()**

Function downloads the image using the WMS method<br>

**Returns**: requests response object or downloaded file path<br>

**Args:<br>**
* layers: (*str*) String specifying the layers to download<br>
* bbox: (*str*) Default=`None`, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
* srsname: (*str*) Default="EPSG:4326", Desired projection<br>
* height: (*int*) Default=512, The vertical number of pixels to return<br>
* width: (*int*) Default=512, The horizontal number of pixels to return<br>
* format: (*str*) The format of the response image either `jpeg`, `png` or `geotiff`<br>
* outputpath: (*str*) Output path must include output format. Downloaded path default is user home path<br>
* display: (*bool*) Default=`False`, Display image in IDE (Jupyter Notebooks only)<br>

```python
response = analytics.download_vector_analytics(layers="VIVID_BASIC", bbox="miny,minx,maxy,maxx", height=256, width=256, format="jpeg", outputpath=r"your\output\path\image.extension")
print(response)
```
___

### Download Vector Tiles 
**download_vector_tiles()**

Function downloads vector imagery using the wmts method<br>

**Returns**: Downloaded file path<br>

**Args:<br>**

* layers: (*str*) String specifying the layers to download<br>
* zoom_level: (*int*) The desired zoom level<br>
* bbox: (*str*) Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
* srsname: (*str*) Default="EPSG:4326", Desired projection<br>
* outputpath: (*str*) Output path must include output format. Downloaded path default is user home path<br>
* display: (*bool*) Default=`False`, Display image in IDE (Jupyter Notebooks only)<br>

```python
response = analytics.download_vector_tiles(layers="VIVID_BASIC", zoom_level=15, bbox="miny,minx,maxy,maxx", outputpath=r"your\output\path\image.extension")
print(response)
```
