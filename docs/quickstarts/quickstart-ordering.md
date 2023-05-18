# Quick Start for Ordering

## Initializing

After setting up the `.MGP-config` file from the [Getting Started](../index.md) section, run the following code to create an instance of the Interface class. This class will be used to access the functionality of the MGP-SDK.

	from MGP_SDK.interface import Interface
	interface = Interface()
	
After gathering STAC information from the [Discovery](quickstart-discovery.md) section, continue utlizing the information gathered from that section.

## Pipelines

### Get pipeline details

After determining the namespace and name of the desired pipeline, the get_pipeline_details function can determine what information needs to be acquired to successfully place an ordering

	pipeline = interface.ordering_service.get_pipeline_details(namespace='imagery', name='map-ready')
	required_info = pipeline['data']['settings_schema']['required']
	for info in required_info:
		type_info = pipeline['data']['settings_schema']['properties'][info]
		print("The type of data for {} is: {}".format(info, type_info))
		
## Orders

### Place an Order

An order can be validated before submission with the use of the `validate` argument if desired

	order = interface.ordering_service.place_order(namespace='imagery', name='map-ready', output_config={"output_config": {"amazon_s3": {"bucket": "your-s3-bucket", "prefix": "your-bucket-prefix"}}}, settings={"settings": {"inventory_ids": ["<STAC-feature-id>"], "customer_description": "your-order-name"}}, notifactions=[{"type": "email", "target": "your-email-address", "level": "FINAL_ONLY"}], metadata={"metadata": {"project_id": "your-order-name"}}, validate=False)
	order_id = order['data']['id']
	
### Get Order Details

After an order has been placed, the details of that order can be fetched at any time

	check_order = interface.ordering_service.get_order_details(order_id=order_id)
	
### Get Order Events

Some orders may take time to fully process and may go through a number of event changes. These can be visualized with the get_order_events function

	check_order_events = interface.ordering_service.get_order_events(order_id=order_id)
	
### Cancel an Order

In some cases, the cancellation of an order may be required. This can be done with the cancel_order function **NOTE: Not all pipelines allow cancellation. Check the information of the pipeline before preceding**

	cancel_order = interface.ordering_service.cancel_order(order_id=order_id)
