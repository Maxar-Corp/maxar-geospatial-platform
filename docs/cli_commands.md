# Command Line Interface
After downloading the MGP_SDK library, open a terminal session and activate the python environment the library exists in

### Create a config file
- In the terminal, enter `config` to begin the setup of a configuration file
- The terminal will prompt you for a username, password, and client_id
- Enter in desired information

### Reset password in config file
- In the terminal, enter `password` to reset a password in the configuration file
- The terminal will prompt you for a new password
- Enter in desired password
- Confirm the new password

### Create a User Token (Optional)
- In the terminal, enter `token` to create an api token to authenticate into the platform.
- If a token has already been created enter `get_token` into the terminal to show the existing tokens

### Delete a User Token (Optional)
- In the terminal, enter `delete_token` to delete an api token.
- Enter in the desired token_id
- Confirm deletion of api token

### Search available imagery
- In the terminal, enter `search` followed by the desired flags to refine your search. Available flags can be found by running `search --help`
- Available flags are:
  - `--bbox`, `-b`: Bounding box. A string of the bounding box of the desired AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
  - `--filter`, `-f`: Filter. A string of a CQL filter used to refine data of search
  - `--shapefile`, `-s`: Shapefile. A boolean operator to return found data as a shapefile format
  - `--featureprofile`, `-fp`: Feature profile. A string of the desired stacking profile. Defaults to account Default
  - `--typename`, `-t`: Typename. A string of the typename. Defaults to FinishedFeature. Example input: MaxarCatalogMosaicProducts


For further information on search functionality, see [Search](ogc/image_search.md)

### Download available imagery
- In the terminal, enter `download` followed by the desired flags to refine your download. Available flags can be found by running `download --help`
- Available flags are:
  - `--bbox`, `-b`: Bounding box. A string of the bounding box of the desired AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
  - `--height`, `-h`: Height. An integer value representing the vertical number of pixels to return
  - `--width`, `-w`: Width. An integer value representing the horizontal number of pixels to return
  - `--img_format`, `-img`: Image format. A string of the format of the response image in jpeg, png, or geotiff
  - `--zoom_level`, `-z`: Zoom level. An integer value of the zoom level. Used for WMTS
  - `--download`, `-d`: Download. A boolean operator for user option to download file locally
  
**NOTE: Structure of calls should be structured with one of the following examples:**
  
	- bbox, zoom_level, img_format
	- bbox, identifier, gridoffsets, img_format
	- bbox, img_format, height, width

For further information on download functionality, see one of the following:

- [Download](ogc/download_image.md)
- [Download with Feature Id](ogc/download_image_featureid.md)
- [Download by Pixel Count](ogc/download_image_pixel_count.md)
- [Download Tiles](ogc/download_tiles.md)

### Calculate bbox area in SQKM
- In the terminal, enter `area` to determine the size of the desired AOI in SQKM
- The terminal will prompt you for a bounding box
- Enter in desired bounding box
- Alternatively, enter `area` followed by the desired flag to determine the size of the desired AOI in SQKM. Available flag can be found by running `area --help`
- Available flag is:
  - `--bbox`, `-b`: Bounding box. A string of the bounding box of the desired AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)
