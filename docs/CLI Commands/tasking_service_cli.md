# Tasking Service CLI

### Submit tasking
Options:

	--pipeline, -p, Desired pipeline namespace and name separated by a forward slash. Required
	--recipe, -r, Desired image recipe. Required
	--start_datetime, -sd, ISO-8601 formatted date when the tasking should start. Required
	--end_datetime, -ed, ISO-8601 formatted date when the tasking should end. Required
	
	--settings, -s, Tasking settings including inventory ids placeholder list and customer description. Required
	--aoi, -a, GeoJSON of AOI
	--output_config, -o, Output configuration template. Required
	--notifications, -n, Notifications template. Required
	
	--metadata, -m, Project metadata. Required
	--validate, -v, Flag to valide tasking request. Defaults to False
	--yes, -y, help='Flag to bypass one or more variable checks. Defaults to False
Submits or validates a tasking request

- In the terminal, enter `mgp submit-tasking` and pass the required flags

Example:

	mgp submit-tasking -p imagery/map-ready -r 50cm_Color -s "2023-01-01T00:00:00Z" -e "2023-02-01T00:00:00Z" -s -a -o -n -m "My tasking order" -v -y

### Cancel tasking
Options:

	--tasking_id, -t, Desired tasking ID. Required
	--reason, -r, Reason for tasking cancellation. Required
Cancels a desired tasking request

- In the terminal, enter `mgp cancel-tasking` and pass the required flags

Example:

	mgp cancel-tasking -t taskingID -r "Changing AOI to new area"
