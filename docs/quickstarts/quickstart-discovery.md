# Quick Start for Discovery

## Initializing

After setting up the `.MGP-config` file from the [Getting Started](../index.md) section, run the following code to create an instance of the Interface class. This class will be used to access the functionality of the MGP-SDK.

	from MGP_SDK.interface import Interface
	interface = Interface()
	
	
## STAC

### Searching STAC items

STAC ids are used for further search refining

	stac = interface.discovery_service.stac_search(bbox='-105,40,-104,41', datetime='2015-01-01T00:00:00Z/2016-01-01T00:00:00Z', collections='wv02', where='eo:cloud_cover<20', orderby='id', limt=1)
	stac_id = stac['features']['id']
	
### Get Supported Pipelines

Pipelines are used for ordering archive features

	desired_feature = interface.discovery.get_stac_item(collection_id='wv02', item_id=stac_id)
	for i in desired_feature['links']:
		print(i['rel'])
		print(i['href'])