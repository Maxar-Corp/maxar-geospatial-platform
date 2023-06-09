# Basemaps
<hr>

The Streaming Basemaps API enables streaming of the Vivid imagery basemaps and associated product and source image metadata using 
OGC services, including WMS, WMTS, and WFS. Maxar hosts the suite of Vivid basemaps and makes available the most recent 
version of each basemap as updates are available. For more information on the Vivid imagery basemap products (Vivid 
Basic, Vivid Standard, Vivid Advanced, and Vivid Premium) refer to the applicable product specification.

Streaming basemaps is done for areas of interest by specifying the location parameters for the desired image tiles. 
Streaming is available for a single tile or the entire product coverage area. For more information on 
[OGC](https://www.ogc.org/standards/)

### Getting Started: 
```python
from MGP_SDK.interface import Interface

basemaps = Interface().basemap_service
```

### Package methods:

- [Get Available Basemaps](#get-available-basemaps--get_available_basemaps)
- [Get Basemap Details](#get-basemap-details--get_basemap_details)
- [Search](#search--search)
- [Download Image](#download-image--download_image)
- [Get Tile List With Zoom](#get-tile-list-with-zoom--get_tile_list_with_zoom)


## Basemaps

### Get Available Basemaps / get_available_basemaps()
Get a list of all available basemaps and their information<br>
**Returns**: JSON response of basemaps<br>
```python
available_basemaps = basemaps.get_available_basemaps()
print(available_basemaps)
```

### Get Basemap Details / get_basemap_details()
Get the information of a desired basemap by utilizing the basemap's ID<br>
**Returns**: JSON response of basemap details<br>
Args:<br>
**basemap_id**: string, identifier of the desired basemap. Comma separated for multiple IDs
```python
basemap_details = basemaps.get_basemap_details('92079771-d0b8-4b5c-aecd-1853a6d5589c')
print(basemap_details)
```

## Streaming Seamlines

### Search / search()
Function searches using the wfs method<br>
**Returns**: Response is either a list of features or a shapefile of all features and associated metadata.<br>
Args:<br>
**srsname**: (string) Default=EPSG:4326, Desired projection<br>
**bbox**: (string) Default=None, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
**filter**: (string) Default=None, CQL filter used to refine data of search<br>
**shapefile**: (bool) Default=False, Binary of whether or not to return as shapefile format<br>
**csv**: (bool) Default=False, Binary of whether or not to return as a csv format<br>
Keyword Arguments:<br>
**request**: Defaults to GetFeature. options: DescribeFeatureType, GetCapabilities<br>
**featureprofile**: (string) The desired stacking profile. Defaults to account Default<br>
**typename**: (string) The typename of the desired feature type. Defaults to seamline<br>
Any additional API parameters can be passed as a keyword argument<br>
### Get Feature:
```python
features = seamline.search(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', srsname='EPSG:3857', 
                            filter="product_name='VIVID_STANDARD_30'")
print(features)
```
### Get Capabilities:
```python
capabilities = seamline.search(request='getCapabilities')
print(capabilities)
```

### Describe Feature Type:
```python
featureType = seamline.search(request='DescribeFeatureType')
print(features)
```
### Download Image / download_image()
Function downloads the image using an ogc method based on the parameters passed in<br>
**Returns**:requests response object or downloaded file path<br>
Args:<br>
**bbox**: Default=None, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
**srsname**: Default=EPSG:4326, Desired projection<br>
**height**: Default=512, The vertical number of pixels to return<br>
**width**: Default=512, The horizontal number of pixels to return<br>
**img_format**: Default=jpeg, The format of the response image either jpeg, png or geotiff<br>
**zoom_level**: Default=None, The zoom level. Used for WMTS<br>
**download**: Default=True, User option to download image file locally. Default True<br>
**outputpath**: Default=None, Output path must include output format. Downloaded path default is user home path.<br>
**display**: Default=False, Display image in IDE (Jupyter Notebooks only). Default False<br>
Keyword Arguments:<br>
**legacyid**: (string) The duc id to download the browse image<br>
**layers**: Defaults to Maxar:seamline. Options: Maxar:Imagery<br>
**request**: Defaults to GetMap. options: GetCapabilities<br>

### Get a seamline map:
```python
image = seamline.download_image(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', srsname='EPSG:3857',
                                filter="productName='VIVID_STANDARD_30'", height=1024, width=1024, img_format='png')
```

### Get a vivid map:
```python
image = seamline.download_image(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', srsname='EPSG:3857',
                                filter="productName='VIVID_STANDARD_30'", layers='Maxar:Imagery', height=1024, 
                                width=1024, img_format='vnd.jpeg-png')
```

### Get Capabilities
```python
capabilities = seamline.download_image(request='GetCapabilities')
```


### Get Tile List With Zoom / get_tile_list_with_zoom()
Function acquires a list of tile calls dependent on the desired bbox and zoom level<br>
**Returns**: List of individual tile calls for desired bbox and zoom level<br>
Args:<br>
**bbox**: Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
**zoom_level**: The zoom level<br>
**srsname**: Default=EPSG:4326, Desired projection<br>
```python
tile_list = streaming.get_tile_list_with_zoom(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', 
                                              srsname='EPSG:3857', zoom_level=8, 
                                              filter="product_name='VIVD_STANDARD_30'")
print(tile_list)
```

### Download Tiles / download_tiles()
Function downloads all tiles within a bbox dependent on zoom level<br>
**Returns**: Message displaying success and location of downloaded tiles<br>
Args:<br>
**bbox**: Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
**zoom_level**: The zoom level<br>
**srsname**: Default=EPSG:4326, Desired projection<br>
**img_format**: Default=jpeg, The format of the response image either jpeg, png or geotiff<br>
**outputpath**: Default=None, Output path must include output format. Downloaded path default is user home path.<br>
**display**: Default=False, Display image in IDE (Jupyter Notebooks only)<br>
```python
streaming.download_tiles(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', srsname='EPSG:3857', 
                         zoom_level=8, img_format='geotiff', filter="product_name='VIVD_STANDARD_30'")
```


