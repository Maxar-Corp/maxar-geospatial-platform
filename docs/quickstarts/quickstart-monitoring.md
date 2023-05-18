# Quick Start for Monitoring

## Initializing

After setting up the `.MGP-config` file from the [Getting Started](../index.md) section, run the following code to create an instance of the Interface class. This class will be used to access the functionality of the MGP-SDK.

	from MGP_SDK.interface import Interface
	interface = Interface()
	
## Monitors

### Creating a new Monitoring

A monitor will create an alert over a desired location and will notify a user when new imagery is available over their desired AOI. The monitor must be set at least 15 minutes into the future and must be in ISO-8601 format. The monitor also uses a geoJSON to determine the AOI

	monitor = interface.monitoring_service.new_monitor(source="discovery/catalog", start_datetime="2023-05-18T16:57:44+00:00", end_datetime="2023-05-19T16:47:44+00:00", description="My-monitor", intersects={"type": "Polygon", "coordinates": [[[-106.8, 35.1], [-106.4, 35.1], [-106.4, 35.4], [-106.8, 35.4], [-106.8, 35.1]]]}, match_criteria={"platform": {"in": ["worldview-03", "worldview-02"]}, "eo:cloud_cover": {"lt": 75}, "aoi:coverage_sqkm": {"gte": 1}}, monitor_notifications=[{"type": "email", "target": "your-email-address"}])
	
### Toggle Monitor status

After a monitor has passed its start date but before it has reached its end date, a user can toggle a monitor to `enable` (on) or `disable` (off)

	toggle_monitor = interface.monitoring_service.toggle_monitor_status(monitor_id="desired-monitor-id", status="disable")
	
### Get Monitor events

After a monitor has been created, a user can check the events of a monitor. The results can be sorted or filtered with the `filter` and `sort` keyword arguments respectively

	monitor_events = interface.monitoring_service.get_monitor_events(monitor_id="desired-monitor-id")
