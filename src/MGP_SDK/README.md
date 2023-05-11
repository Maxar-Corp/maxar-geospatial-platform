# Maxar Geospatial Platform SDK
<hr>

# Installation Instructions
1. Install python 3.7
2. pip install MGP_SDK
3. Create a credentials file in your home directory called`.mgp-config` 
   * The file should look like:
   ```
   [mgp]
   user_name=<your-user-name>
   user_password=<your-password>
   client_id=<your-client-id>
   ```
### Included Packages:<br>
- [Streaming](#streaming) 
- [Account Service](#account-service)
- [Basemap Service](#basemap-service)
- [Discovery Service](#discovery-service)
- [Monitor Service](#monitor-service)
- [Ordering Service](#ordering-service)
- [Tasking Service](#tasking-service)
- [Usage Service](#usage-service)

## Streaming
The Streaming Imagery SDK service makes Maxar content immediately available via HTTPs and OGC WMS, WMTS, and WFS 
standards. [README](../../docs/streaming/Streaming.md)

Set-up:
```python
from MGP_SDK.interface import Interface

streaming = Interface().streaming
```

## Account Service
SDK for performing administrative tasks such as searching users or setting up accounts

Set-up:
```python
from MGP_SDK.interface import Interface

account = Interface().account_service
```

## Basemap Service
The Streaming Basemaps SDK enables of the Vivid imagery basemaps and associated product and source image metadata using
OGC services. [README](../../docs/basemap-service/Basemap.md)

Set-up:
```python
from MGP_SDK.interface import Interface

basemaps = Interface().basemap_service
```

## Discovery Service
The Discovery service enables customers to discover products that are available to order or stream. 
[README](../../docs/discovery-service/Discovery.md)
Set-up:
```python
from MGP_SDK.interface import Interface

discovery = Interface().discovery_service
```

## Monitor Service
The Monitoring SDK enables customers to be alerted when new data is available in their registered AOI and provides the
capability of ordering that data automatically for delivery to a cloud storage location. 
[README](../../docs/monitor-service/Monitor.md)

Set-up:
```python
from MGP_SDK.interface import Interface

monitor = Interface().monitoring_service
```

## Ordering Service
The Ordering SDK enables customers to acquire Maxar content for offline use. [README](../../docs/ordering-service/Ordering.md)

Set-up:
```python
from MGP_SDK.interface import Interface

ordering = Interface().order_service
```

## Tasking Service
The Tasking SDK provides customers the ability to submit tasking requests for new imagery collection within a specified
date range and area of interest. [README](../../docs/tasking-service/Tasking.md)

Set-up:
```python
from MGP_SDK.interface import Interface

tasking = Interface().tasking_service
```

## Usage Service
The Usage SDK allows account administrators to systematically generate reports for usage analysis. 
[README](../../docs/usage-service/Usage.md)


Set-up:
```python
from MGP_SDK.interface import Interface

usage = Interface().usage_service
```

