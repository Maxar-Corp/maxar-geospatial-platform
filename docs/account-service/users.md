# Users
<hr>
The users portion of the MGP_SDK provides an interface for user administration methods.

---

### Getting Started:
```python
from MGP_SDK.interface import Interface

interface = Interface()
```

### Package methods

* [Get User](#get-users)
* [Create User](#create-user)
* [Update User](#update-user)
* [Delete User](#delete-user)
* [Get User Roles](#get-user-roles)
* [Update User Roles](#update-user-roles)


### Get User 
**get_users()**

Retrieves information about a user

**Returns:** Dictionary of a user's information

**Args:**
* user_id (*str*): User's id number. Defaults to `None`
* username (*str*): User's username. Defaults to `None`

**Kwargs:**
* pageSize (*int*): Number of results to be returned.
* page (*int*): Page number to be returned.

### Create User 

**create_user()**

Creates a user 

**Returns:** Dictionary of created user's information

**Args:**

* user_type (*str*): User type for the new user. `BASE_USER` or `ACCOUNT_ADMIN`
* account_id (*str*): Account for the new user.
* activation_id (*str*): Activation for the new user.
* emailAddress (*str*): Email address for the new user
* firstName (*str*): First name of the new user
* lastName (*str*): Last name of the new user
* client_id (*str*): Client for new user. Defaults to `mgp`

**Kwargs:**

* comments (*str*): Comments for the user's account.

___

### Update User 
**update_user()**

Updates and existing user's information

**Args:**

* userId (*str*): The user's id
   
**Kwargs:**

* emailAddress (*str*): The new email address for the user
* firstName (*str*): The new first name of the user
* lastName (*str*): The new last name of the user
* comments (*str*): Additional comments for the user

___

## Get Users 
**get_users()**

Get information about a user

**Returns:** Dictionary of the user's information

**Args:**

* userId (*str*): The identifier for the desired user (defaults to None).
* username (*str*): The username of the desired user (defaults to None).
	
**Kwargs:**

* pageSize (*int*): The desired number of objects returned
* page (*int*): The desired starting page for pagination (0 is the first page)

----

## Delete User 
**delete_user()**

Delete a user

**Returns:** Message indicating successful deletion of a user

**Args:**

* userId (*str*): The id of the user to be deleted

___

## Get User Roles 
**get_user_roles()**

Retrieves roles associated with a user.

**Returns:** Dictionary of currently assigned user roles.

**Args:**

* user_id (*str*): ID of user

---

## Get User Available Roles 
**get_user_available_roles()**

Retrieves roles available to be assigned to a user.

**Returns:** Dictionary of available roles 

**Args:**

* user_id (*str*): ID of user
* client_id (*str*): ID of user's client. Defaults to id associated with `mgp` client.

---

## Update User Roles 
**update_user_roles()**

Adds or deletes roles from a user

**Returns:** Dictionary of updated roles

**Args:**

* user_id (*str*): ID of user to be updated
* roles_to_update (*list(str)*): List of roles to be updated.
* client_id (*str*): Client id user is associated with. Defaults to id for `mgp` client.
* delete (*bool*): Determines if role is added or delete. Defaults to `False`, indicating role addition.

---

