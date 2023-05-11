# Roles

----

## Get User Roles

### **Args:**

#### userId (*str*):

  The identifier of the desired user
  
  *Example:*
  
	interface.account_service.users.GetUserRoles(userId="f:3a34d893-5d36-4cb8-9cfc-6b2a6678de3b:1")

----

## Get User Available Roles

### **Args:**

#### userId (*str*):

  The identifier of the desired user
  
  *Example:*
  
	interface.account_service.users.GetUserAvailableRoles(userId="f:3a34d893-5d36-4cb8-9cfc-6b2a6678de3b:1")

----

## Update User Roles

### **Args:**

#### userId (*str*):

  The identifier of the desired user
  
  *Example:*
  
	interface.account_service.users.UpdateUserRoles(userId="f:3a34d893-5d36-4cb8-9cfc-6b2a6678de3b:1")

#### rolesToUpdate (lst(*str*)):

  The desired roles to update for the user
  
  *Example:*
  
	interface.account_service.user.UpdateUserRoles(["AERIAL_CELLS"])

#### delete (*bool*):

  Flag to dictate whether or not to delete a role from the desired user (defaults to False).
  
  *Example:*
  
	interface.account_service.user.UpdateUserRoles(delete=True)
