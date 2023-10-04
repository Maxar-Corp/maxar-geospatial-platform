# Analytics Service CLI

### Raster URL Formation
Options:

	--script_id, -s, Desired raster script name. Required
	--function, -f, Desired raster function
	--collect_id, -cid, Desired collect ID for the raster object
	
	--api_token, -a, Your maxar API token
	
	--crs, -c, Desired projection for the raster object. Defaults to UTM
	--bands, -b, Comma separated string of desired bands for the raster object. Defaults to None
	
	--dra, -d, Binary of whether or not to apply dra to the raster. String of bool (true, false). Defaults to None
	--interpolation, -i, Desired resizing or (re)projection from one pixel grid to another. Defaults to None
Return a vsicurl formatted raster URL

- In the terminal, enter `mgp raster-url` and pass the required flags

Example:

	mgp raster-url -s "ortho-image" -f "pansharp-ortho" -cid <collectID> -a <apiToken> -b "red,green,blue"

### Get Raster Array
Options:

	--raster_url, -r, vsicurl formatted URL of a raster object. Required

	--x_off, -x, Number of pixels to offset on the x axis. Required
	--y_off, -y, Number of pixels to offset on the y axis. Required
	--width, -w, Number of pixels for the returned raster on the x axis. Required
	--height, -h, Number of pixels for the returned raster on the y axis. Required
	
	--download, -d, Flag dictating the download of a raster object. Defaults to False
	--outputpath, -o, Desired output path location for the rasterized object including filename and extension
Create a raster array from a rasterized (vsicurl) URL and download the raster locally if specified

- In the terminal, enter `mgp get-raster-array` and pass the required flags

Example:

	mgp get-raster-array -r "<raster URL from raster-url function>" -x 3067 -y 2045 -w 2045 -h 2045
To return a raster array

Or

	mgp get-raster-array -r "<raster URL from raster-url function>" -x 3067 -y 2045 -w 2045 -h 2045 -d -o "<your\output\path\raster_image.format>"
To download an image of the rasterized object

### Vector Search
Options:

	--layers, -l, Desired vector layer. Required
	
	--bbox, -b, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
	--srsname, -srs, Desired projection NOTE:(WFS for vector data currently only supports EPSG:3857). Defaults to EPSG:3857
	
	--filter, -f, CQL filter used to refine data of search. Defaults to None
	
	--shapefile, -s, Binary of whether to return as shapefile format. Defaults to False
	--csv, -c, Binary of whether to return as a csv format, Defaults to False
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Search vector layers

- In the terminal, enter `mgp vector-search` and pass the required flags

Example:

	mgp vector-search -l "VIVID_BASIC" -b -y

### Vector Image Download
Options:

	--layers, -l, Desired vector layer. Required
	
	--bbox, -b, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
	--srsname, -srs, Desired projection. Defaults to EPSG:4326
	--height, -h, The vertical number of pixels to return. Defaults to 512
	--width, -w, The horizontal number of pixels to return. Defaults to 512
	
	--img_format, -i, The format of the response image either jpeg, png or geotiff
	--outputpath, -o, Output path must include output format. Downloaded path default is user home path
	--filter, -f, CQL filter used to refine data of search. Defaults to None
	
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Download a vector image

- In the terminal, enter `mgp vector-image-download` and pass the required flags

Example:

	mgp vector-image-download -l "VIVID_BASIC" -b -h 256 -w 256 -i jpeg -o "<your\output\path\raster_image.format>" -y

### Vector Tile Download
Options:

	--layers, -l, Desired vector layer. Required
	
	--zoom, -z, Desired zoom level between 1 and 20. Required
	--bbox, -b, Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
	--srsname, -s, Desired projection NOTE:(WFS for vector data currently only supports EPSG:4326). Defaults to EPSG:4326
	
	--outputpath, -o, Output path must include output format. Downloaded path default is user home path
	
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Download vector tiles

- In the terminal, enter `mgp vector-tile-download` and pass the required flags

Example:

	mgp vector-tile-download -l "VIVID_BASIC" -z 15 -b -o "<your\output\path\raster_image.format>" -y
