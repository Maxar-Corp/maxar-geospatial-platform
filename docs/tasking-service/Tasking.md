# Tasking
<hr>

The Tasking portion of the MGP_SDK provides customers the ability to submit tasking requests for new imagery collection within a specified
date range and area of interest. A tasking request will automatically trigger a monitor that will look for matching 
imagery as it collects according to the tasking request. Upon a match, the user will be notified of the acquisition and 
an order will be automatically placed to the pipeline the user selected as part of the tasking request, which includes 
ARD and Core Imagery.

### Getting Started: 
```python
from MGP_SDK.interface import Interface

tasking = Interface().tasking_service
```

### Package methods:

- [New Tasking](#new-tasking--new_tasking)
- [Cancel a Tasking Request](#cancel-a-tasking--cancel_tasking)
- [Get a Tasking Request](#get-tasking-request--get_tasking_request)
- [Tasking List](#tasking-list--tasking_list)


### New Tasking / new_tasking()
Initiates the creating of a tasking request (async) using one of the preconfigured recipes: 50cm_Color, 30cm_Color. If a kwarg
is null or not provided, default recipe value will be used.<br>
Args:<br>
**start_datetime**: ISO-8601 formatted date when the tasking request should start<br>
**end_datetime**: ISO-8601 formatted date when the tasking request should end<br>
**aoi_geojson**: Geojson polygon of area to cover with the tasking request<br>
**recipe**: the name of one of the configured recipes for the tasking request, e.g. "50cm_Color" or "30cm_Color"<br>
**order_templates**: Template for order to be placed. See ordering_service for examples<br> 
Keyword Arguments:<br>
**max_cloud_cover**: double, Maximum cloud cover.<br>
**max_off_nadir_angle**: double, Maximum off nadir angle.<br>
**max_sun_elevation_angle**: double, Maximum sun elevation angle.<br>
```python
start_datetime = "2023-05-01 18:34:57Z"
end_datetime = "2024-04-30 18:34:57Z"
geo_json = {"coordinates": [
    [
        [-106.8, 35.1],
        [-106.4, 35.1],
        [-106.4, 35.4],
        [-106.8, 35.4],
        [-106.8, 35.1]
    ]
],
    "type": "Polygon"
}
recipe = "50cm_Color"
order_templates = "order:template"
max_cloud_cover = 0.02
max_off_nadir_angle = 30.0
min_sun_elevation_angle = 45.0


tasking.new_tasking(start_datetime, end_datetime, geo_json, recipe, order_templates, max_cloud_cover, 
                    max_off_nadir_angle, min_sun_elevation_angle)
```

### Cancel a Tasking / cancel_tasking()
Initiates the canceling of a tasking request (async) <br>
Args:<br>
**tasking_id**: ID of the requested tasking request<br>
**reason**: Reason for canceling the tasking request<br>
```python
tasking.cancel_tasking('131173789789914064', 'test')
```

### Get Tasking Request / get_tasking_request()
Retrieves a tasking request<br>
Args:<br>
**tasking_id**: ID of the requested tasking request<br>
```python
details = tasking.get_tasking_request('131173789789914064')
```

### Tasking List / tasking_list()
Retrieves a page listing of all tasking request based upon query parameters. Limited to the authenticated user's group<br>
Keyword Arguments:<br>
**limit**: how many items to return in the response list. Default 10<br>
**filter**: filter results that match values contained in the given key separated by a colon.<br>
Ex. recipe:50cm_Color. These are not exact matches, so filtering on a value of string:bla will return
all string:bla along with string:blah. Note: filter field may be repeated if multiple filters are desired. If so, supply
as a list.<br>
**sort**: indicates sort order, asc (default) and desc for reverse alphabetical by name<br>
```python
taskings = tasking.tasking_list(limit=5, filter=['recipe:50cm_Color, tasking_status:Accepted'], sort='desc')
```