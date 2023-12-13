# Imagery CLI

### Search available imagery
Options:

	--bbox, -b, String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
	--filter, -f, CQL filter used to refine data of search
	--shapefile, -s, Binary of whether or not to return as a shapefile format
	
	--featureprofile, -fp, String of the desired stacking profile. Defaults to account Default
	--typename, -t, String of the typename. Defaults to FinishedFeature. Example input MaxarCatalogMosaicProducts
	--default, -d, Binary of whether or not to default yes over bbox prompt
Searches an AOI using the WFS method and returns a list of features and their metadata that intersect with the AOI

- In the terminal, enter `mgp search` followed by the desired flags to refine your search

Example:

	mgp search -b "39.911942,-105.006058,39.913793,-104.996789" -d
For further information on search functionality, see [Search](../streaming/Streaming.md)

### Download available imagery
Options:

	--bbox, -b, String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
	--height, -h, Integer value representing the vertical number of pixels to return
	--width, -w, Integer value representing the horizontal number of pixels to return
	--img_format, -img, String of the format of the resonse image (jpeg, png, or geotiff)
	
	--zoom_level, -z Integer value of the zoom level. Used for WMTS
	--download, -dl, Boolean of user option to download file locally
	--outputpath, -o, Path to desired download location
	--default, -d Binary of whether or not to default yes over bbox prompt
Downloads an image or a list of image calls and returns the file location of the download.

- In the terminal, enter `mgp download` followed by the desired flags to refine your download

Example:

	mgp download -b 39.911942,-105.006058,39.913793,-104.996789 -h 512 -w 512 -img jpeg -dl True -o C:\Users -d
  
**NOTE: Structure of calls should be structured with one of the following examples:**
  
	- bbox, zoom_level, img_format
	- bbox, height, width, img_format

For further information on download functionality, see the following:

- [Download](../streaming/Streaming.md)

### Get tile list for bounding box
Options:

	--bbox, -b, String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
	--zoom, -z, Desired zoom level between 1 and 20
	--srsname, -s, Desired projection. Defaults to EPSG:4326
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Acquires a list of tile calls dependent on the desired bbox and zoom level

- In the terminal, enter `mgp get-tile-list` followed by the desired flags

Example:

	mgp get-tile-list -b 39.911942,-105.006058,39.913793,-104.996789 -z 15 -y

### Download image tiles
Options:

	--bbox, -b, String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
	--zoom, -z, Desired zoom level between 1 and 20
	--srsname, -s, Desired projection. Defaults to EPSG:4326
	
	--img_format, -i, Desired output image format. Defaults to jpeg
	--outputpath, -o, Desired output path for download. Defaults to None
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Downloads all tiles within a bbox dependent on zoom level

- In the terminal, enter `mgp download-tiles` followed by the required flags

Example:

	mgp download-tiles -b -z 15 -i png -o C:\Users\tiles.png -y
	
### Download image by pixel count
Options:

	--bbox, -b, String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
	--height, -h, Desired height of image in pixels
	--width, -w, Desired width of image in pixels
	
	--srsname, -s, Desired projection. Defaults to EPSG:4326
	--img_format, -i, Desired output image format. Defaults to jpeg
	--outputpath, -o, Desired output path for download. Defaults to None
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Downloads the image of the desired bounding box dependent on pixel height and width

- In the terminal, enter `mgp download-by-pixel-count` and pass in the required flags

Example:

	mgp download-by-pixel-count -b -h 512 -w 512 -i png -o C:\Users -y

### Download full resolution image
Options:

	--featureid, -f, Desired feature ID
	--thread_number, -t, Desired thread number for multithreading. Defaults to 100
	--bbox, -b, String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
	
	--mosaic, -m, Flag to determine whether or not to mosaic images together
	--srsname, -s, Desired projection. Defaults to EPSG:4326
	--outputdirectory, -o, Desired output directory for download. Defaults to None
	
	--image_format, -i, Desired output image format. Defaults to jpeg
	--filename, -fn, Desired filename for mosaiced image. Defaults to Maxar_Image
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Takes in a feature id and breaks the image up into 1024x1024 tiles and then paces a number of calls based on multithreading percentages to return a full image strip in multiple tiles

- In the terminal, enter `mgp full-res-image` and pass the required flags

Example:

	mgp full-res-image -f <featureId> -b 39.911942,-105.006058,39.913793,-104.996789 -m -o C:\Users -i png -fn full_res.png -y

### Mosaic tiles
Options:

	--base_dir, -b, Root directory containing image files to be mosaiced
	--img_format, -if, Image format of files
	--img_size, -is, Size of individual image files. Defaults to 1024
	--outputdirectory, -o, Desired output directory for download
	--filename, -f, Desired filename for mosaiced image. Default to merged_image
Creates a mosaic of downloaded image tiles from full_res_download function

- In the terminal, enter `mgp mosaic` and pass the required flags

Example:

	mgp mosaic -b C:\Users -if png -o C:\Users\tiles -fn tile_mosaic

### Calculate bbox area in SQKM
Options:

	--bbox, -b, String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Calculates the area in square kilometers of the bounding box

- In the terminal, enter `mgp calculate-bbox-sqkm` and pass the required flags

Example:

	mgp calculate-bbox-sqkm -b 39.911942,-105.006058,39.913793,-104.996789 -y
