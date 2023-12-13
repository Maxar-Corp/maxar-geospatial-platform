# Release Notes

## Version 1.3.1 (Dec 13, 2023)
* Updated various functions to better handle auth and refresh tokens
* Updated response handler to return better status messaging
* Updated documentation

## Version 1.3.0 (Nov 7, 2023)
* Added CQL check function
* Added acomp and hd options for RasterAnalytics class
* Updated wording of Jupyter notebooks 
* Updated minimum supported version to 3.8

## Version 1.2.3 (Oct 12, 2023)
* Added password parsing to allow special characters

## Version 1.2.2 (Oct 5, 2023)
* No changes, updating documentation and github

## Version 1.2.1 (Oct 4, 2023)
* Added CLI commands for basemaps
* Added additional Jupyter notebook examples for basemaps
* Fixed bug with discovery service stac search

## Version 1.2.0 (Sep 7, 2023)
* Added functionality to download_image() that will download wmts tiles instead of returning a list of WMTS calls to make
* Added CLI commands for variable storage, admin, streaming, usage, ordering, discovery, analytics and monitoring
* Additional Jupyter notebook examples for discovery and ordering, raster analytics, vector analytics and tasking
* Minor bug fixes

## Version 1.1.1 (May 23, 2023)

* Added Jupyter notebook example for monitoring-service
* Bug fix for monitoring service

## Version 1.1.0 (May 18, 2023)

* CLI updates for token-service
* CLI updates for streaming-service
* Validation added for tasking requests
* Updated documentation for CLI commands, discovery-service, monitoring-service, ordering-service, and tasking-service
* Added Jupyter notebook examples for discovery-service, ordering-service, and tasking-service
* Added get_stac_item functionality to discovery-service
* Added get_all_pipelines functionality to ordering-service
* Removed GDAL and rasterio as dependencies for package
* Minor bug fixes

## Version 1.0.0 (May 10, 2022)

* Initial release
