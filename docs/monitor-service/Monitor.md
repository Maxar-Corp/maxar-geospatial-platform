# Monitoring
<hr>

The Monitoring portion of the MGP_SDK enables customers to be alerted when new data is available in their registered AOI and provides the 
capability of ordering that data automatically for delivery to a cloud storage location. Customers can define specific 
collection parameters that trigger delivery such as cloud cover, off-nadir angle, look angle, time of day, and others 
when submitting a monitoring request.

### Getting Started: 
```python
from MGP_SDK.interface import Interface

monitoring = Interface().monitoring_service
```

### Package methods:

- [Create a New Monitor](#create-a-new-monitor--new_monitor)
- [Toggle Monitor Status](#toggle-a-monitors-status--toggle_monitor_status)
- [Get a Monitor](#get-a-monitor--get_monitor)
- [Get a List of Monitors](#get-a-list-of-monitors--get_monitor_list)
- [Get Monitor Events](#get-monitor-events--get_monitor_events)

### Create a new monitor / new_monitor():
Initiates the creation of a new monitor<br>
Args:<br>
**source**: string, the ID of the event source to listen to. e.g 'discovery/catalog'<br>
**validate**: bool, binary of only validating, not submitting the monitor. Defaults to False
Keyword Arguments:<br>
**start_datetime**: string, ISO-8601-formatted datetime string indicating when the monitor should start<br>
**end_datetime**: string, ISO-8601-formatted datetime string indicating when the monitor should end<br>
**description**: string, a human-friendly description of the monitor<br>
**intersects**: dict, a GeoJSON geometry indicating the area of interest for the monitor<br>
**match_criteria**: dict, the fields and values to match against; criteria are specified using a JSON object<br>
**monitor_notifications**: list, destination(s) where notifications should be sent<br>
**order_templates**: list,  orders to be placed automatically when an event matches the monitor's criteria<br>
```python
new_monitor = monitoring.new_monitor('discover/catalog', start_datetime='2023-05-08T12:00:00.000000+00:00', end_datetime='2023-05-10T12:0:00.000000+00:00', description='test_monitor')
print(new_monitor)
```

### Toggle a monitor's status / toggle_monitor_status()
Enables or disables a monitor<br>
Args:<br>
**monitor_id**: string, the ID of the monitor<br>
**status**: string, 'enable' or 'disable'<br>
```python
monitoring.toggle_monitor_status('6130456176116070854', 'disable')
```

### Get a Monitor / get_monitor()
Retrieves a monitor configuration<br>
Args:<br>
**monitor_id**: string, the ID of the monitor<br>
```python
status = monitoring.get_monitor('6130456176116070854')
print(status)
```
<details>
<summary>Example Response:</summary>

```javascript
{
    "data": {
        "id": "1234123412341234",
        "date_created": "2023-02-16T18:22:25Z",
        "date_modified": "2023-02-16T18:22:25Z",
        "creator_id": "id",
        "creator_group_id": "NO_GROUP",
        "source": "discovery/catalog",
        "description": "monitor for new imagery in albuquerque",
        "start_datetime": "2023-06-18T00:00:00Z",
        "end_datetime": "2023-09-18T00:00:00Z",
        "aoi_geojson": {
            "type": "Polygon",
            "coordinates": [
                [-106.8, 35.1],
				[-106.4, 35.1],
				[-106.4, 35.4],
				[-106.8, 35.4],
				[-106.8, 35.1]
            ]
          ]                
        },
        "match_criteria": {
            "platform": {
                "in": [
                    "worldview-03",
                    "worldview-02"
                ]
            },
            "eo:cloud_cover": {
                "lt": 75
            }
        },
        "erode_area": false,
        "order_templates": [
            {pipeline": "imagery/analysis-ready",
                "template": {
                "settings": {
				"acquisitions": [{
					"id": "$.id"
                    }],
                "intersects": "$._aoi_geojson",
				"ard_settings": {
					"bundle_adjust": true,
					"healthy_vegetation_mask": false,
					"water_mask": false
				}
			},
                    "output_config": {
                        "amazon_s3": {
                            "bucket": "your-bucket",
                            "prefix": "your-prefix"
                        }
                    }
                }
            }
        ],
        "monitor_notifications": [
            {
                "type": "email",
                "target": "myemail.email.com"
            }
        ],
        "state": {},
        "enabled": false,
        "monitor_links": {
            "self": "https://api.maxar.com/v1/monitoring/v1monitors/612258447717453999",
            "events": "https://api.maxar.com/monitoring/monitors/6122584477174534999/events"
        }
    },
    "links": {
        "request": "https://api.maxar.com/monitoring/v1/monitors"
    },
    "request_timestamp": "2023-02-16T18:22:25Z",
    "response_timestamp": "2023-02-16T18:22:26Z",
    "request_duration": 1
}
```
</details>

### Get a List of Monitors / get_monitor_list()
Retrieves a list of monitor configurations<br>
Keyword Arguments:<br>
**limit**: int, number of monitors to return, defaults to 10<br>
**filter**: string | list[string], filter results that match values contained in the given key separated by a colon. If
multiple filters are needed, provide as a list of filters<br>
**sort**: string, asc (default) or desc
```python
monitor_list = monitoring.get_monitor_list(limit=5, filter='enabled=false', sort='desc')
print(monitor_list)
```

### Get Monitor Events / get_monitor_events()
Retrieves a list of events for a monitor<br>
Args:<br>
**monitor_id**: string, the ID of the monitor<br>
Keyword Arguments:<br>
**limit**: int, number of monitors to return, defaults to 10<br>
**filter**: string | list[string], filter results that match values contained in the given key separated by a colon. If
multiple filters are needed, provide as a list of filters<br>
**sort**: string, asc (default) or desc
```python
monitor_events = monitoring.get_monitor_events('6130456176116070854', limit=7)
print(monitor_events)
```

