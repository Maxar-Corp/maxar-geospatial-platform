# Basemaps CLI

### Search available basemaps imagery
Options:

	--bbox, -b, String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
	--srsname, -srs, Desired projection. Defaults to EPSG:4326
	--filter, -f, CQL filter used to refine data of search
	--layer, -l, Desired basemap layer. Defaults to VIVID_BASIC
	
	--shapefile, -s, Binary of whether or not to return as a shapefile format
	--csv, -c, Binary of whether to return as a csv format, Defaults to False
	
	--seamlines, -s, Binary to search seamlines data. Defaults to False
	--featureprofile, -fp, String of the desired stacking profile. Defaults to account Default
	--typename, -t, String of the typename. Defaults to FinishedFeature. Example input MaxarCatalogMosaicProducts
	
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Searches an AOI using the WFS method and returns a list of basemap features and their metadata that intersect with the AOI

- In the terminal, enter `mgp basemaps-search` followed by the desired flags to refine your search

Example:

	mgp basemaps-search -b "39.911942,-105.006058,39.913793,-104.996789" -l "VIVID_PREMIUM" -f "cloudCover<.15"

### Download available basemaps imagery
Options:

	--bbox, -b, String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
	--srsname, -srs, Desired projection. Defaults to EPSG:4326
	--layer, -l, Desired basemap layer. Defaults to VIVID_BASIC
	--height, -h, Integer value representing the vertical number of pixels to return
	--width, -w, Integer value representing the horizontal number of pixels to return
	--img_format, -img, String of the format of the resonse image (jpeg, png, or geotiff)
	--zoom_level, -z Integer value of the zoom level. Used for WMTS
	
	--filter, -f, CQL filter used to refine data of search. Defaults to None
	--download, -dl, Boolean of user option to download file locally
	--outputpath, -o, Path to desired download location
	
	--seamlines, -s, Binary to search seamlines data. Defaults to False
	--yes, -y, Binary of whether or not to default yes over bbox prompt
Downloads a basemap image or a list of basemap image calls and returns the file location of the download.

- In the terminal, enter `mgp basemaps-download` followed by the desired flags to refine your download

Example:

	mgp basemaps-download -b "39.911942,-105.006058,39.913793,-104.996789" -l "VIVID_STANDARD" -z 15 -img jpeg -dl -o "C:\Users\your\output\path\image.format" -s -y
  
**NOTE: Structure of calls should be structured with one of the following examples:**
  
	- bbox, zoom_level, img_format
	- bbox, height, width, img_format

### Get tile list for bounding box
Options:

	--bbox, -b, String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
	--zoom, -z, Desired zoom level between 1 and 20
	--srsname, -s, Desired projection. Defaults to EPSG:4326
	--seamlines, -s, Binary to search seamlines data. Defaults to False
	--filter, -f, CQL filter used to refine data of search. Defaults to None
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Acquires a list of tile calls dependent on the desired bbox and zoom level

- In the terminal, enter `mgp basemapstile-list` followed by the desired flags

Example:

	mgp basemaps-tile-list -b "39.911942,-105.006058,39.913793,-104.996789" -z 15 -y

### Download basemap image tiles
Options:

	--bbox, -b, String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx). Required
	--zoom, -z, Desired zoom level between 1 and 20. Required
	--srsname, -s, Desired projection. Defaults to EPSG:4326
	--layer, -l, Desired basemap layer. Defaults to VIVID_BASIC
	
	--img_format, -img, Desired output image format. Defaults to jpeg
	--filter, -f, CQL filter used to refine data of search. Defaults to None
	
	--outputpath, -o, Desired output path for download. Defaults to None
	--seamlines, -s, Binary to search seamlines data. Defaults to False
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Downloads basemap tiles over a given AOI

- In the terminal, enter `mgp basemaps-download-tiles` followed by the required flags

Example:

	mgp basemaps-download-tiles -b "39.911942,-105.006058,39.913793,-104.996789" -z 15 -img png -o "C:\Users\your\output\path\images.format" -f ona<20 -s -y
	
### Download basemap image by pixel count
Options:

	--bbox, -b, String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
	--height, -h, Desired height of image in pixels
	--width, -w, Desired width of image in pixels
	
	--srsname, -s, Desired projection. Defaults to EPSG:4326
	--layer, -l, Desired basemap layer. Defaults to VIVID_BASIC
	--img_format, -img, Desired output image format. Defaults to jpeg
	--filter, -f, CQL filter used to refine data of search. Defaults to None
	
	--outputpath, -o, Desired output path for download. Defaults to None
	--seamlines, -s, Binary to search seamlines data. Defaults to False
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Downloads the basemap image of the desired bounding box dependent on pixel height and width

- In the terminal, enter `mgp basemaps-image-by-pixel-count` and pass in the required flags

Example:

	mgp basemaps-image-by-pixel-count -b "39.911942,-105.006058,39.913793,-104.996789" -h 512 -w 512 -l "VIVID_PREMIUM" -img png -f "cloudCover<.15" -o "C:\Users\your\output\path\image.format" -y
