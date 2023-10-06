# Maxar Geospatial Platform - Python SDK

## Getting started

**MGP SDK** is a Python library for accessing Maxar's Geospatial Platform API endpoints to 
retrieve and manipulate services including account, activation and user access as well as OGC services
The connection is established using login credentials stored in a local config file.


Installation:

There are two options recommended for environment set up to utilize the **MGP SDK**.

1. Installation of rasterio package for georeferencing geotiff files.
	* First install the [Microsoft C++ Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
	* Create a conda environment with the `gdal`, `rasterio`, and `shapely` packages:
		
		Example: ``conda create -n <environment_name> python=3.7 gdal rasterio shapely``
		
	* Proceed with standard pip installation below
		
2. Standard pip installation without the `gdal`, `rasterio`, and `shapely` packages.

	Example: ``pip install MGP-SDK``
	
	*Note: Mosaicing images is still available with this installation option but geotiff files will NOT be georeferenced. See [Download Full Resolution](ogc/get_full_res_image) and [Create Mosaic](ogc/create_mosaic)*

Config File

We recommend creating a credentials file to store your login information for future sessions in one of two ways. 

* Use the command line interface command ``config`` from the command prompt and follow the prompts. See [Command Line Interface](CLI Commands/cli_commands.md)
* Create a credentials file called ``.MGP-config`` in your home directory with the following format:

			[mgp] 
			user_name=<your-user-name>
			user_password=<your-password>
			client_id=<your-client-name>

After creating your config file, you are now ready to start with the following guides:

  * [Quickstart Guide for Admin](quickstarts/quickstart-admin.md)
  * [Quickstart Guide for Streaming](quickstarts/quickstart-streaming.md) 
  * [Quickstart Guide for Discovery](quickstarts/quickstart-discovery.md)
  * [Quickstart Guide for Ordering](quickstarts/quickstart-ordering.md)
  * [Quickstart Guide for Monitoring](quickstarts/quickstart-monitoring.md)