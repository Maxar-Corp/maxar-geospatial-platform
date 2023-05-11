# Maxar Geospatial Platform Usage SDK
<hr>

The Usage API allows account administrators to systematically generate reports for usage analysis. Reported usage is 
measured as customers engage with Maxar APIs or Applications

### Getting Started:

```python
from MGP_SDK.interface import Interface

usage = Interface().usage_service
```

### Package methods:

- [Check Usage is Allowed](#check-usage-is-allowed--check_usage_is_allowed)
- [Get Usage Overview](#get-usage-overview--get_usage_overview)


### Check Usage is Allowed / check_usage_is_allowed()
Checks whether usage is allowed for a user<br>
**returns**: A blank 200 response denotes that usage is allowed.<br>

### Checking for authenticated user:
```python
usage_allowed = usage.check_usage_is_allowed()
print(usage_allowed)
```

### Get Usage Overview / get_usage_overview()
Shows the overview of usage used for the account the authenticated user is tied to<br>
**Returns**: Dictionary of available products and their usage<br>
```python
overview = usage.get_usage_overview()
print(overview)
```


