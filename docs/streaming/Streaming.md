# Maxar Geospatial Platform Streaming SDK
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

- [Search](#search--search)
- [Download Image](#download-image--download_image)
- [Get Tile List With Zoom](#get-tile-list-with-zoom--get_tile_list_with_zoom)
- [Download Browse Image](#download-browse-image--download_browse_image)
- [Get Full Resolution Image](#get-full-resolution-image--get_full_res_image)
- [Get Image From CSV](#get-image-from-csv--get_image_from_csv)

### Search / search()
Function searches using the wfs method<br>
**Returns**: Response is either a list of features or a shapefile of all features and associated metadata.<br>
Args:<br>
**srsname**: (string) Default=EPSG:4326, Desired projection<br>
**bbox**: (string) Default=None, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
**filter**: (string) Default=None, CQL filter used to refine data of search.<br>
**shapefile**: (bool) Default=False, Binary of whether or not to return as shapefile format<br>
**csv**: (bool) Default=False, Binary of whether or not to return as a csv format<br>
Keyword Arguments:<br>
**featureprofile**: (string) The desired stacking profile. Defaults to account Default<br>
**typename**: (string) The typename of the desired feature type. Defaults to FinishedFeature. Example input
MaxarCatalogMosaicProducts<br>
```python
from MGP_SDK.interface import Interface

streaming = Interface().streaming

features = streaming.search(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', srsname='EPSG:3857', 
                            filter="(acquisitionDate>='2022-01-01')AND(cloudCover<0.20)")
print(features)
```

### Download Image / download_image()
Function downloads the image using an ogc method depending on the parameters passing in<br>
**Returns**: requests response object or downloaded file path<br>
Args:<br>
**bbox**: Default=None, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
**srsname**: Default=EPSG:4326, Desired projection<br>
**height**: Default=512, The vertical number of pixels to return<br>
**width**: Default=512, The horizontal number of pixels to return<br>
**img_format**: Default=jpeg, The format of the response image either jpeg, png or geotiff<br>
**zoom_level**: Default=None, The zoom level. Used for WMTS<br>
**download**: Default=True, User option to download image file locally <br>
**outputpath**: Default=None, Output path must include output format. Downloaded path default is user home path.<br>
**display**: Default=False, Display image in IDE (Jupyter Notebooks only)<br>
Keyword Arguments:<br>
**legacyid**: (string) The duc id to download the browse image<br>
```python
image = streaming.download_image(bbox='4828743.9944,-11689315.9992,4831803.1702,-11685446.3746', srsname='EPSG:3857',
                                 height=1024, width=1024, img_format='png', display=True)
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
                                              srsname='EPSG:3857', zoom_level=8)
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
                         zoom_level=8, img_format='geotiff')
```

### Download Browse Image / download_browse_image()
Function downloads the browse image for the desired legacy id<br>
**Returns**: Downloaded image location of desired legacy id in desired format<br>
Args:<br>
**input_id**: The desired input id (Can be feature id or catalog id)<br>
**img_format**: Default=jpeg, The format of the response image either jpeg, png or geotiff<br>
**outputpath**: Default=None, Output path must include output format. Downloaded path default is user home path.<br>
**display**: Default=False,  Display image in IDE (Jupyter Notebooks only). Default False<br>
```python
streaming.download_browse_image(input_id='7327845623467', img_format='png', outputpath=r'C:/myUser/Downloads/Test')
```

### Get Full Resolution Image / get_full_res_image()
Function takes in a feature id and breaks the image up into 1024x1024 tiles, then places a number of calls based on 
multithreading percentages to return a full image strip in multiple tiles<br>
**Returns**: None<br>
**featureid**: Feature id of the image<br>
**thread_number**: Default=100, Number of threads given to multithread functionality. Default 100<br>
**bbox**: Default=None, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)<br>
**mosaic**: Default=False, Flag if image files are mosaiced. Default False<br>
**srsname**: Desired projection. Defaults to EPSG:4326<br>
Keyword Arguments:<br>
**outputdirectory**: string, Desired output location for tiles<br>
**image_format**: string, Desired image format (png or jpeg)<br>
**filename**: string, filename for output mosaiced image
```python
streaming.get_full_res_image(featureid='345757345634', thread_number=125, 
                             bbox='39.906477,-105.010843,39.918031,-104.991939', mosaic=True, image_format='geotiff')
```

### Get Image From CSV / get_image_from_csv()
Function reruns requests for images that previously failed. User will get a message in the event that images have failed
and a csv file will be placed in the users home directory. At that point this method can be called<br>
**Returns**: None<br>
Args:<br>
**featureid**: Feature id of the image<br>
**img_size**: Desired pixel resolution (size x size). Defaults to 1024<br>
Keyword Arguments:<br>
**outputdirectory**: string, Desired output location for tiles<br>
```python
streaming.get_image_from_csv(featureid='3836234573456', img_size='1024x1024')
```




 


