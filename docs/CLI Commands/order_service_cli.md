# Order Service CLI

### All pipelines
List all pipelines and their information

- In the terminal, enter `mgp all-pipelines`

Example:

	mgp all-pipelines

### Get pipeline
Options:

	--namespace, -ns, Desired pipeline namespace. Required
	--name, -n, Desired pipeline name. Required
List the information for a desired pipeline

- In the terminal, enter `mgp get-pipeline` and pass the required flags

Example:

	mgp get-pipeline -ns imagery -n map-ready

### Order
Options:

	--namespace, -ns, Desired pipeline namespace. Required 
	--name, -n, Desired pipeline name, Required 
	--settings, -s, Ordering settings including inventory ids and customer description
	
	--aoi, -a, GeoJSON of AOI
	--output_config, -o, Output configuration template
	--notifications, -nt, Notifications template 
	
	--metadata, -m, Project metadata. Required  
	--validate, -v, Flag to validate order. Defaults to False  
	--estimate, -e, Flag to estimate order usage. Defaults to False
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Validate, estimate, or submit an order

- In the terminal, enter `mgp order` and pass the required flags

Example:

	mgp order -ns imagery -n map-ready -m "My order details" -s -a -o -nt -v -y

### Order details
Options:

	--order_id, -o, Desired order ID. Required
List the details for an order

- In the terminal, enter `mgp order-details` and pass the required flag

Example:

	mgp order-details -o orderID

### Order events
Options:

	--order_id, -o, Desired order ID. Required
	--limit, -l, Maximum number of items to return
	--starting_after, -sa, Token (base-64-encoded-key) after which further responses will be returned, paging forward
	--ending_before, -eb, Token (base-64-encoded key) after which further responses will be returned, paging backward
	--filter, -f, Filter results that match values contained in the given key separated by a colon
List the order events for an order

- In the terminal, enter `mgp order-events` and pass the required flag

Example:

	mgp order-events -o orderID -l 5

### List users' orders
Options:

	--user_id,-u, Desired user ID. Do not pass option if order for self are desired
List the order for a user or for your own user if no flag is passed

- In the terminal, enter `mgp list-users-orders` and pass optional flag if desired

Example:

	mgp list-users-orders -u userID

### Cancel order
Options:

	--order_id, -o, Desired order ID. Required
Cancel an order

- In the terminal, enter `mgp cancel-order` and pass the required flag.

Example:

	mgp cancel-order -o orderID
