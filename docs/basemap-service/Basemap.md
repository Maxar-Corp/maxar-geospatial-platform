# Basemaps
<hr>

The Streaming Basemaps API enables streaming of the Vivid imagery basemaps and associated product and source image metadata using OGC services, including WMS, WMTS, and WFS. Maxar hosts the suite of Vivid basemaps and makes available the most recent version of each basemap as updates are available. For more information on the Vivid imagery basemap products (Vivid Basic, Vivid Standard, Vivid Advanced, and Vivid Premium) refer to the applicable product specification.

Streaming basemaps is done for areas of interest by specifying the location parameters for the desired image tiles. 
Streaming is available for a single tile or the entire product coverage area. For more information on [OGC](https://www.ogc.org/standards/)

### Getting Started: 
```python
from MGP_SDK.interface import Interface

basemaps = Interface().basemap_service
```

### Package methods:

- [Get Available Basemaps](#get-available-basemaps)
- [Get Basemap Details](#get-basemap-details)
- [Search](#search)
- [Download Image](#download-image)
- [Get Tile List With Zoom](#get-tile-list-with-zoom)
- [Download Tiles](#download-tiles)
- [Download Image By Pixel Count](#download-image-by-pixel-count)


## Basemaps

### Get Available Basemaps 
**get_available_basemaps()**

Get a list of all available basemaps and their information<br>

**Returns**: JSON response of basemaps<br>
```python
available_basemaps = basemaps.get_available_basemaps()
print(available_basemaps)
```

### Get Basemap Details 
**get_basemap_details()**

Get the information of a desired basemap by utilizing the basemap's ID<br>

**Returns**: JSON response of basemap details<br>

Args:<br>
**basemap_id**: string, identifier of the desired basemap. Comma separated for multiple IDs
```python
basemap_details = basemaps.get_basemap_details('92079771-d0b8-4b5c-aecd-1853a6d5589c')
print(basemap_details)
```

## Streaming Basemaps

### Search 
**search()**

Function searches using the wfs method<br>

**Returns**: Response is either a list of features or a shapefile of all features and associated metadata.<br>

**Args:<br>**

* srsname: (*str*) Default=EPSG:4326, Desired projection<br>
* bbox: (*str*) Default=None, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
* filter: (*str*) Default=None, CQL filter used to refine data of search<br>
* shapefile: (*bool*) Default=False, Binary of whether or not to return as shapefile format<br>
* csv: (*bool*) Default=False, Binary of whether or not to return as a csv format<br>
* seamlines**: Default=False, Binary of whether to return the information utilizing the seamlines layer<br>

**Kwargs:<br>**
* request: (*str*) Defaults to `GetFeature`. options: `DescribeFeatureType`, `GetCapabilities`<br>
* featureprofile: (*str*) The desired stacking profile. Defaults to account Default<br>
* typename: (*str*) Defaults to FinishedFeature. The typename of the desired feature type<br>
* Any additional API parameters can be passed as a keyword argument<br>

### Get Feature:
```python
features = basemaps.search(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', srsname='EPSG:3857', 
                            filter="productName='VIVID_STANDARD_30'")
print(features)
```

### Get Capabilities:
```python
capabilities = basemaps.search(request='getCapabilities')
print(capabilities)
```

### Describe Feature Type:
```python
featureType = basemaps.search(request='DescribeFeatureType')
print(features)
```

### Download Image 
**download_image()**

Function downloads the image using an ogc method based on the parameters passed in<br>

**Returns**:requests response object or downloaded file path<br>

**Args:<br>**

* bbox: (*str*) Default=None, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
* srsname: (*str*) Default=EPSG:4326, Desired projection<br>
* height: (*int*) Default=512, The vertical number of pixels to return<br>
* width: (*int*) Default=512, The horizontal number of pixels to return<br>
* img_format: (*str*) Default=jpeg, The format of the response image either jpeg, png or geotiff<br>
* zoom_level: (*int*) Default=None, The zoom level. Used for WMTS<br>
* download: (*bool*) Default=True, User option to download image file locally. Default True<br>
* outputpath: (*str*) Default=None, Output path must include output format. Downloaded path default is user home path.<br>
* display: (*bool*) Default=False, Display image in IDE (Jupyter Notebooks only). Default False<br>
* seamlines: (*bool*) Default=False, Binary of whether to return the information utilizing the seamlines layer<br>

**Kwargs:<br>**

* legacyid**: (*str*) The duc id to download the browse image<br>
* layers: (*str*) Options: `Maxar:Imagery`, `seamline`<br>
* request: (*str*) Defaults to GetMap. options: GetCapabilities<br>

### Get a basemap:
```python
image = basemaps.download_image(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', srsname='EPSG:3857',
                                filter="productName='VIVID_STANDARD_30'", height=1024, width=1024, img_format='png')
```

### Get a vivid map:
```python
image = basemaps.download_image(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', srsname='EPSG:3857',
                                filter="productName='VIVID_STANDARD_30'", layers='Maxar:Imagery', height=1024, 
                                width=1024, img_format='vnd.jpeg-png')
```

### Get Capabilities
```python
capabilities = basemaps.download_image(request='GetCapabilities')
```


### Get Tile List With Zoom 
**get_tile_list_with_zoom()**

Function acquires a list of tile calls dependent on the desired bbox and zoom level<br>

**Returns**: List of individual tile calls for desired bbox and zoom level<br>

**Args:<br>**

* bbox: (*str*) Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
* zoom_level: (*int*) The zoom level<br>
* srsname: (*str*) Default=EPSG:4326, Desired projection<br>
* seamlines: (*bool*) Default=False, Binary of whether to return the information utilizing the seamlines layer<br>
```python
tile_list = basemaps.get_tile_list_with_zoom(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', 
                                              srsname='EPSG:3857', zoom_level=8, 
                                              filter="productName='VIVD_STANDARD_30'")
print(tile_list)
```

### Download Tiles 
**download_tiles()**

Function downloads all tiles within a bbox dependent on zoom level<br>

**Returns**: Message displaying success and location of downloaded tiles<br>

**Args:<br>**

* bbox: (*str*) Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
* zoom_level: (*int*) The zoom level<br>
* srsname: (*str*) Default=EPSG:4326, Desired projection<br>
* img_format: (*str*) Default=jpeg, The format of the response image either jpeg, png or geotiff<br>
* outputpath: (*str*) Default=None, Output path must include output format. Downloaded path default is user home path.<br>
* display: (*bool*) Default=`False`, Display image in IDE (Jupyter Notebooks only)<br>
* seamlines: (*bool*) Default=`False`, Binary of whether to return the information utilizing the seamlines layer<br>
```python
basemaps.download_tiles(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', srsname='EPSG:3857', 
                         zoom_level=8, img_format='geotiff', filter="productName='VIVD_STANDARD_30'")
```

### Download Image By Pixel Count 
**download_image_by_pixel_count()**

Function downloads an image within a given AOI<br>

**Returns**: Message displaying success and location of downloaded tiles<br>

**Args:<br>**

* bbox: (*str*) Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
* height: (*int*) Default=512, The vertical number of pixels to return<br>
* width: (*int*) Default=512, The horizontal number of pixels to return<br>
* srsname: (*str*) Default=EPSG:4326, Desired projection<br>
* img_format: (*str*) Default=jpeg, The format of the response image either jpeg, png or geotiff<br>
* outputpath: (*str*) Default=None, Output path must include output format. Downloaded path default is user home path.<br>
* display: (*bool*) Default=`False`, Display image in IDE (Jupyter Notebooks only)<br>
* seamlines: (*bool*) Default=`False`, Binary of whether to return the information utilizing the seamlines layer<br>
```python
basemaps.download_image_by_pixel_count(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', srsname='EPSG:3857', height=256, width=256, filter="productName='VIVID_STANDARD_30'")
```
