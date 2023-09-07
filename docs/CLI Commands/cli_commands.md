# Setup CLI
After downloading the MGP_SDK library, open a terminal session and activate the python environment the library exists in

### Create a config file
Options:

	--username, -u, Your username
	--password, -p, Your password
	--client_id, -c, Your client ID
Creates a configuration file for authentication use for Maxar Geospatial Platform APIs

- In the terminal, enter `mgp config-file` to begin the setup of a configuration file
- The terminal will prompt you for a username, password, and client_id
- Enter in desired information
- The desired username, password, and client id can be passed into the console directly to bypass prompts

Example:

	mgp config-file
Then enter in the information as the prompts appear

Or

	mgp config-file -u <user.name@email.com> -p <yourPassword> -c <userClientId>
The file will be stored in a user's home directory

### Check home directory
Prints out the location of your machine's home directory where the .MGP-config file will live

Example:

	mgp home-dir

### Reset password in config file
Options:

	--password, -p, Your new password
Updates the password in the .MGP-configuration file

- In the terminal, enter `mgp reset-password` to reset a password in the configuration file
- The terminal will prompt you for a new password
- Enter in desired password
- Confirm the new password

Example:

	mgp reset-password
Then enter in the information as the prompts appear

Or

	mgp reset-password -p <yourNewPassword>

### Store variables in config file
Options:
	
	--variables, -v, Variables for storage in config file. 
	
Choices are:
	
	order_settings (string(dict)) = Settings for an order. Ex: {"settings": {"inventory_ids": ["item_id"], "customer_description": "descripiton"}}
	bbox (string) = Comma separated integers in miny,minx,maxy,maxx format. Ex: 39.911942,-105.006058,39.913793,-104.996789 
	output_config (string(dict)) = Settings for an output configuration. Ex: {"output_config": {"amazon_s3": {"bucket": "bucket-name", "prefix": "prefix/name"}}}  
	
	notifications_settings (string(list(dict))) = Settings for a notification output. Ex: [{"type": "email", "target": "your.email@address.com", "level": "FINAL_ONLY"}] **Note: For use with ordering and tasking only**  
	geojson (string(dict)) = AOI in geoJSON format. Ex: {"type": "Polygon", "coordinates": [[[-103.991089, 39.546412], [-103.900452, 39.546412], [-103.900452, 39.474365], [-103.991089, 39.474365], [-103.991089, 39.546412]]]}  
	monitor_notifications (string(list(dict))) = Settings for a notification output for a monitor. Ex: [{"type": "email", "target": "your.email@address.com"}]  
	
	tasking_template (string(dict)) = Template for a tasking request. Ex: {"settings": {"inventory_ids": ["$.id"], "customer_description": "description"}}  
	match_criteria (string(dict)) = Template for match criteria for monitoring. Ex: {"platform": {"in": ["worldview-03", "worldview-02"]}, "eo:cloud_cover": {"lt": 75}, "aoi:coverage_sqkm": {"gte": 1}}
Creates a variable and stores it in the .MGP-config file stored on your machine. These variables can be utilized with other CLI commands without the need to enter in the entire variable in the command prompt.

- In the command prompt, enter `mgp store-variables -v` followed by the desired variable to store

Example:

	mgp store-variables -v bbox 39.911942,-105.006058,39.913793,-104.996789
Follow the prompts to store the variable
