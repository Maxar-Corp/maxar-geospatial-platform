# API Keys
<hr>
The API key portion of the `MGP_SDK` provides an interface for working with API keys for the platform.  

----

### Getting Started:
```python
from MGP_SDK.interface import Interface

interface = Interface()
```

### Package methods

* [Get User API keys](#get-user-api-keys)
* [Create API key](#create-api-key)
* [Delete API Keys](#delete-api-keys)

## Get User API Keys 
**get_user_tokens()**

Retrieves a list of all API keys associated with a user.

**Returns:** Dictionary of all API keys associated with a user.

## Create API Key 
**create_token_record()**

Creates a new API key to utilize in calls with no authentication headers instead of an OAuth2 bearer token. 

- *NOTE:* Make sure to save the API key as this will be the only time
        it is visible. If a API key is lost, a new one must be created.
        
**Returns:** Dictionary of information about the newly created API key.  

**Args:**

* name (*str*): Name for the API key.
* description (*str*): Description for the API key.
* expiration_date (*str*): UTC expiration date of the API key in `yyyy-mm-dd hh:mm:ss`. Defaults to 180 days. Cannot exceed 180 days.


## Delete API Keys 
**delete_tokens()**

 Deletes one or more API keys. Pass either a string of a token id to delete a single token or
        pass a list of strings of token ids to delete multiple tokens at once

**Args:**

 * token (*str* or *list(str)*): ID(s) of API key(s) to be deleted.
