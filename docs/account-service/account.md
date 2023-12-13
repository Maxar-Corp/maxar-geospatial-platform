# Account/Activation
<hr>

The Account and Activation portion of the MGP_SDK provides an interface for account/activation administration methods.

___

### Getting Started: 
```python
from MGP_SDK.interface import Interface

interface = Interface()
```

### Package methods
- [Search](#search)
- [Get Self](#get-self)
- [Get Accounts](#get-accounts)
- [Toggle Role](#toggle-role)
- [Get Activations](#get-activations)
- [Get Activation Credit Limit](#get-activation-credit-limit)

## Search 
**search()**

Searches through specified admin area using a target string

**Returns:** A dictionary of information about the found subject 

**Args:**

* search_type (*str*): The desired search area. `account`, `activation`, `user` are acceptable arguments
  
* search_term (*str*): Desired string to be searched for.
    * For `account`, the function will search through account numbers, account names, SAP license ids, sold to, and licensees.
    * For `activations`,  the function will search through activation numbers, SAP contract identifiers, SAP line items, start dates, end dates, activation numbers, and activation ids. 
    * For `user`, the function will search through usernames, roles, activation numbers, and account numbers.


## Get Self 
**get_self()**

Retrieve information about session user

**Returns:** Dictionary of information about session user

## Toggle Role 
**toggle_role()**

Toggles a given permission for all users under an activation 

**Returns:** A dictionary of all affected users and permission/role status

**Args:**

* client_id (*str*): String of client_id
* role (*str*): Role/Permission name to be toggled
* action (*str*): `enable` or `disable`
  
## Get Activations 
**get_activations()**

Retrieve information about activations

**Note:** With no args passed in, will return all available activations.

**Returns:** A dictionary of activations and information.

**Args:**

* activation_id (*int*): ID of an activation. Defaults to `NONE`
* activation_number (*str*): Activation number. Defaults to `NONE`


## Get Activation Credit Limit 
**get_activation_credit_limit()**

Retrieve the credit limit for an activation

**Returns:** Dictionary of a given activation's credit limit and usage

**Args:** 

* activation_number (*str*): Activation number of interest