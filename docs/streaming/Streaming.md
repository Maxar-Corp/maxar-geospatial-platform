# Imagery
<hr>

The Streaming Imagery API service makes Maxar content immediately available via HTTPs
and OGC WMS, WMTS, and WFS standards. The customer provides required parameters for
each respective implementations via the API, whereby the respective file format and tiles are
returned for streaming integrations across a range of applications and industries. For more information on 
[OGC](https://www.ogc.org/standards/)

### Getting Started: 
```python
from MGP_SDK.interface import Interface

streaming = Interface().streaming
```

### Package methods:

- [Search](#Search)
- [Download Image](#download-image)
- [Get Tile List With Zoom](#get-tile-list-with-zoom)
- [Download Browse Image](#download-browse-image)
- [Get Full Resolution Image](#get-full-resolution-image)
- [Download Image by Pixel Count](#download-image-by-pixel-count)

### Search
**search()**

Function searches using the wfs method<br>
**Returns**: Response is either a list of features or a shapefile of all features and associated metadata.<br>
**Args:**<br>

* srsname: (*str*) Default=EPSG:4326, Desired projection<br>
* bbox: (*str*) Default=None, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
* filter: (*str*) Default=None, CQL filter used to refine data of search.<br>
* shapefile: (*bool*) Default=False, Binary of whether or not to return as shapefile format<br>
* csv: (*bool*) Default=False, Binary of whether or not to return as a csv format<br>

**Keyword Arguments**:<br>

* featureprofile: (*str*) The desired stacking profile. Defaults to account Default<br>
* typename: (*str*) The typename of the desired feature type. Defaults to FinishedFeature. Example input
MaxarCatalogMosaicProducts<br>

```python
from MGP_SDK.interface import Interface

streaming = Interface().streaming

features = streaming.search(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', srsname='EPSG:3857', 
                            filter="(acquisitionDate>='2022-01-01')AND(cloudCover<0.20)")
print(features)
```

### Download Image
**download_image()**

Function downloads the image using an ogc method depending on the parameters passing in<br>
**Returns**: requests response object or downloaded file path<br>
**Args:**<br>

* bbox (*str*): Default=None, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
* srsname (*str*): Default=EPSG:4326, Desired projection<br>
* height (*int*): Default=512, The vertical number of pixels to return<br>
* width (*int*): Default=512, The horizontal number of pixels to return<br>
* img_format (*str*): Default=jpeg, The format of the response image either jpeg, png or geotiff<br>
* zoom_level (*int*): Default=None, The zoom level. Used for WMTS<br>
* download (*bool*): Default=True, User option to download image file locally <br>
* outputpath (*str*): Default=None, Output path must include output format. Downloaded path default is user home path.<br>
* display (*bool*): Default=False, Display image in IDE (Jupyter Notebooks only)<br>

**Keyword Arguments:**<br>
* legacyid: (*str*) The duc id to download the browse image<br>

```python
from MGP_SDK.interface import Interface

streaming = Interface().streaming

image = streaming.download_image(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', srsname='EPSG:3857',
                                 height=1024, width=1024, img_format='png', display=True)
```

### Get Tile List With Zoom 

**get_tile_list_with_zoom()**

Function acquires a list of tile calls dependent on the desired bbox and zoom level<br>

**Returns**: List of individual tile calls for desired bbox and zoom level<br>

**Args:**<br>

* bbox (*str*): Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
* zoom_level (*int*): The zoom level<br>
* srsname (*str*): Default=EPSG:4326, Desired projection<br>

```python
from MGP_SDK.interface import Interface

streaming = Interface().streaming

tile_list = streaming.get_tile_list_with_zoom(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', 
                                              srsname='EPSG:3857', zoom_level=8)
print(tile_list)
```

### Download Tiles 

**download_tiles()**

Function downloads all tiles within a bbox dependent on zoom level<br>

**Returns**: Message displaying success and location of downloaded tiles<br>

**Args:<br>**
* bbox (*str*): Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
* zoom_level (*int*): The zoom level<br>
* srsname (*str*): Default=EPSG:4326, Desired projection<br>
* img_format (*str*): Default=jpeg, The format of the response image either jpeg, png or geotiff<br>
* outputpath (*str*): Default=None, Output path must include output format. Downloaded path default is user home path.<br>
* display (*bool*): Default=False, Display image in IDE (Jupyter Notebooks only)<br>

```python
from MGP_SDK.interface import Interface

streaming = Interface().streaming

streaming.download_tiles(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', srsname='EPSG:3857', 
                         zoom_level=8, img_format='geotiff')
```

### Download Browse Image 

**download_browse_image()**

Function downloads the browse image for the desired legacy id<br>

**Returns**: Downloaded image location of desired legacy id in desired format<br>

**Args:**<br>

* input_id (*str*): The desired input id (Can be feature id or catalog id)<br>
* img_format (*str*): Default=jpeg, The format of the response image either jpeg, png or geotiff<br>
* outputpath (*str*): Default=None, Output path must include output format. Downloaded path default is user home path.<br>
* display (*bool*): Default=False,  Display image in IDE (Jupyter Notebooks only). Default False<br>

```python
from MGP_SDK.interface import Interface

streaming = Interface().streaming

streaming.download_browse_image(input_id='7327845623467', img_format='png', outputpath=r'C:/myUser/Downloads/Test')
```

### Get Full Resolution Image 
**get_full_res_image()**

Function takes in a feature id and breaks the image up into 1024x1024 tiles, then places a number of calls based on 
multithreading percentages to return a full image strip in multiple tiles<br>

**Returns**: None<br>

**Args:**

* featureid (*str*): Feature id of the image<br>
* thread_number (*int*): Default=25, Number of threads given to multithread functionality.<br>
* bbox (*str*): Default=None, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
* mosaic (*bool*): Default=False, Flag if image files are mosaiced.<br>
* srsname (*str*): Desired projection. Defaults to EPSG:4326<br>

**Keyword Arguments:**<br>

* outputdirectory (*str*): Output location for tiles<br>
* image_format (*str*): Image format (png or jpeg)<br>
* filename (*str*): Filename for output mosaiced image

```python
from MGP_SDK.interface import Interface

streaming = Interface().streaming

streaming.get_full_res_image(featureid='345757345634', thread_number=125, 
                             bbox='39.906477,-105.010843,39.918031,-104.991939', mosaic=True, image_format='geotiff')
```

### Download Image by Pixel Count 
**download_image_by_pixel_count()**

Function downloads the image of desired bbox dependent on pixel height and width

**Returns:** Message indicating the location of the downloaded file. 
        
**Args:**

* bbox (*str*): Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
* height (*int*): The vertical number of pixels to return
* width (*int*): The horizontal number of pixels to return
* srsname (*str*): Desired projection. Defaults to EPSG:4326
* img_format (*str*): Default=jpeg, The format of the response image either jpeg, png or geotiff
* outputpath (*str*): Output path must include output format. Downloaded path default is user home path.
* display (*bool*): Display image in IDE (Jupyter Notebooks only). Defaults to `False`

**Kwargs:**
* filter: CQL filter used to refine data of search.
* featureprofile: The desired stacking profile. Defaults to account Default

```python
from MGP_SDK.interface import Interface
streaming = Interface().streaming

feature_id = '932f7992a4d86a9ca412c024c22792ce'
aoi = '39.906477,-105.010843,39.918031,-104.991939'
cql_filter = "featureId='{}'".format(feature_id)
download = streaming.download_image_by_pixel_count(bbox=aoi, height=512, width=512, img_format='jpeg', filter=cql_filter)
print(download)
```
