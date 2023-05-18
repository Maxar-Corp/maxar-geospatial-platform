# Ordering
<hr>

The Ordering portion of the MGP_SDK enables customers to acquire Maxar content for offline use. Customers can create orders via API request
using the results of their Discovery request by submitting a set of delivery type and content-specific parameters to the
Ordering API. Submission to the Ordering API asynchronously triggers the content production pipeline to deliver the 
requested data. The Order is delivered to the location set by the customer in their Order request. The Ordering service 
has built-in order tracking, notifications, and error management for every request. These validation mechanisms will 
prevent users from exceeding their allowed usage.<br>

### Getting Started: 
```python
from MGP_SDK.interface import Interface

ordering = Interface().order_service
```

### Package methods:

- [Place a New Order](#place-a-new-order--place_order)
- [Estimate Order Usage](#estimate-order-usage--get_usage_estimate)
- [Cancel an Order](#cancel-an-order--cancel_order)
- [Cancel Multiple Orders](#cancel-multiple-orders--cancel__multiple_orders)
- [Get Order Details](#get-order-details--get_order_details)
- [Get My Orders](#get-my-orders--get_my_orders)
- [Get User Orders](#get-user-orders--get_user_orders)
- [Get Order Events](#get-order-events--get_order_events)
- [Get All Pipelines](#get-all-pipelines--get_all_pipelines)
- [Get Pipeline Details](#get-pipeline-details--get_pipeline_details)

### Place a New Order / place_order()
Places an order for the given group of pipelines and pipeline name<br>
Args:<br>
**namespace**: string, a group of pipelines (e.g. 'imagery') <br>
**name**: string, name of the pipeline to order from (e.g. 'analysis-ready')<br>
**output_config**: (optional) dictionary, delivery configuration. Amazon S3, Google Cloud Storage, Azure Blob storage are 
supported.<br>
**settings**: dictionary, settings specific to this pipeline. (required if the requested pipeline requires
user-provided input parameters and has a json_schema attribute)<br>
Keyword Arguments:<br>
**notifications**: list, (optional) destination(s) where notifications should be sent. Multiple notifications of
the same type can be created, each having its own notification level.<br>
**metadata**: dictionary, (optional) supplemental information to attach to this order<br>
**validate**: boolean, (optional, default = False) True if user requests to validate order before sending<br>
```python
settings = {"acquisitions": [{"id": "10403C0001FD6000"}],
            "bbox": [-106.8, 35.1, -106.4, 35.4],
            "ard_settings": {
                "bundle_adjust": True,
                "healthy_vegetation_mask": True,
                "water_mask": False}
            }

output_config = {
    "amazon_s3": {
        "bucket": "user-docs-demo",
        "prefix": "albuquerque"}
	}
notifications = [
    {
        "type": "email",
        "target": "username@myemail.com",
        "level": "INITIAL_FINAL"
    }
]
metadata = {"project_id": "albuquerque-cars"}

ordering.place_order('imagery', 'analysis-ready', settings, output_config, 
                     notifications=notifications, metadata=metadata, validate=True)
```

### Estimate Order Usage / get_usage_estimate()
 Get a usage estimate for the order<br>
 Args: <br>
**namespace**: string, a group of pipelines (e.g. 'imagery') <br>
**name**: string, name of the pipeline to order from (e.g. 'analysis-ready')<br>
**output_config**: (optional) dictionary, delivery configuration. Amazon S3, Google Cloud Storage, Azure Blob storage are 
supported.<br>
**settings**: dictionary, settings specific to this pipeline. (required if the requested pipeline requires
user-provided input parameters and has a json_schema attribute)<br>
Keyword Arguments:
**notifications**: list, (optional) destination(s) where notifications should be sent. Multiple notifications of
the same type can be created, each having its own notification level.<br>
**metadata**: dictionary, (optional) supplemental information to attach to this order<br>

 ```python
settings = {'settings'}
output_config = {'output config'}
notifications = {'notifications'}
metadata = {'metadata'}
order_usage = ordering.get_usage_estimate('imagery', 'analysis-ready', settings, output_config, 
                                          notifications=notifications, metadata=metadata)
print(order_detials)
```

### Cancel an Order / cancel_order()
Cancels an order is pipeline supports canceling<br>
Args:<br>
**order_id**: The ID of the Order to cancel<br>
```python
ordering.cancel_order('99926034175760632')
```

### Cancel Multiple Orders / cancel__multiple_orders()
Cancels orders based on a list containing order IDs<br>
Args:<br>
**order_id**: list, list containing the IDs of the Orders to cancel<br>
```python
order_list = ['99926034175760632', '99926034175760631', '99926034175760630']
ordering.cancel__multiple_order(order_list)
```

### Get Order Details / get_order_details()
Gets the IDs of all Orders that match the search criteria and the user can access.<br>
Args:<br>
**order_id**: string, the ID of the order<br>
```python
order_detials = ordering.get_order_details('99926034175760632')
print(order_detials)
```

### Get User Orders / get_user_orders()
Returns a list of a users order by user ID. If no ID is provided, returns a list of the authenticated user's orders.<br>
Args:<br>
**user_id**: str, the ID of the desired user<br>
Keyword Arguments:<br>
**limit**: int, (optional) limits the number of responses returned<br>
**filter**: list, Filter results that match values contained in the given key separated by a colon<br>
**sort**: str, Indicates sort order, desc (default) for descending order (newest first) and asc for ascending order (oldest firts)<br>
**start_date**: str, ISO-8601 formatted date after which to query orders (inclusive)<br>
**end_date**: str, ISO-8601 formatted date before which to query orders (inclusive)<br>
```python
user_orders = ordering.get_user_orders(user_id='f:123456789:1')
```

### Get Order Events / get_order_events()
Gets events for an order by order ID<br>
Args:<br>
**order_id**: int, ID of the requested order<br>
Keyword Arguments:<br>
**limit**: int, (optional) limits the number of responses returned<br>
**filter**: list, Filter results that match values contained in the given key separated by a colon<br>
```python
events = ordering.get_order_events('99926034175760632', limit=5, filter="pipeline_id:imagery/analysis-ready")
```

### Get All Pipelines / get_all_pipelines()
Returns a list of all available pipelines<br>
```python
all_pipelines = ordering.get_all_pipelines()
```

### Get Pipeline Details / get_pipeline_details()
Gets the details for a pipeline by namespace and name<br>
Args:<br>
**namespace**: str, a group of pipelines (e.g. 'imagery')<br>
**name**: str, name of the pipeline to order from (e.g. 'analysis-ready')<br>
```python
details = ordering.get_pipeline_details('imagery', 'analysis-ready')
```


