# Monitor Service CLI

### Create monitor
Options:

	--start_datetime, -sd, ISO-8601 formatted date when the monitoring should start. Required
	--end_datetime, -ed, ISO-8601 formatted date when the monitoring should end. Required  
	--description, -d, Description of the monitor being created. Required
	--aoi, -a, GeoJSON of AOI. Required
	
	--match_criteria, -m, Dictionary of desired matching criteria. Required
	--notifications, -n, Monitor notifications template. Required
	--order_templates, -o, Flag to dictate whether or not to auto-order when monitor is triggered. Defaults to False
	--pipeline, -p, Desired ordering pipeline
	
	--validate, -v, Flag to validate monitor request. Defaults to False
	--yes, -y, Flag to bypass one or more variable checks. Defaults to False
Validate or create a monitor

- In the terminal, enter `mgp create-monitor` and pass the required flags. If `order_templates` is passed, `pipeline` is required and an order settings dictionary will need to be entered into the prompt when the command is run. The `yes` flag will not work if the `order_templates` flag is passed

Examples:

	mgp create-monitor -sd "2024-01-01T00:00:00Z" -ed "2024-02-01T00:00:00Z" -d "Monitor over my AOI" -a -m -v -y

### Get monitor
Options:

	--monitor_id, -id, Desired monitor id 
	--limit, -l, Amount of monitors to return. Defaults to 10
	--filter, -f, Desired filter for returning monitors. Defaults to None
	--sort, -s, Desired sorting option. Defaults to None
List one or more monitor's information

- In the terminal, enter `mgp get-monitor` and pass optional flags if desired

Example:

	mgp get-monitor -id monitorID -l 5 -s asc

### Monitor events
Options:

	--monitor_id, -id, Desired monitor id. Required
	--limit, -l, Amount of monitors to return. Defaults to 10
	--filter, -f, Desired filter for returning monitors. Defaults to None 
	--sort, -s, Desired sorting option. Defaults to None
List the events for a monitor

- In the terminal, enter `mgp monitor-events` and pass the required flag

Example:

	mgp monitor-events -id monitorID

### Toggle monitor
Options:

	--monitor_id, -id, Desired monitor ID. Required
	--enable, -e, Flag to enable a monitor. Defaults to False
	--disable, -d, Flag to disable a monitor. Defaults to False
Toggle the status of a monitor between enabled/disabled

- In the terminal, enter `mgp toggle-monitor` and pass the required flag as well as on of the action flags

Example:

	mgp toggle-monitor -id monitorID -d
