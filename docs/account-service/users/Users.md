#User

----

## Create User

### **Args:**

#### user_type (*str*):

  The desired user type for the newly created user. Options are BASE_USER, ACCOUNT_ADMIN, GLOBAL_ADMIN, SYSTEM_ADMIN
  
  *Example:*
  
	interface.account_service.users.CreateUser(user_type="BASE_USER")

#### accountId (*int*):

  The identifier for the desired account to tie the user to
  
  *Example:*
  
	interface.account_service.users.CreateUser(accountId=1)

#### activationId (*int*):

  The identifier for the desired activation to tie the user to
  
  *Example:*
  
	interface.account_service.users.CreateUser(activationId=1)

#### emailAddress (*str*):

  The desired email address for the newly created user
  
  *Example:*
  
	interface.account_service.users.CreateUser(emailAddress="my_user@mail.com")

#### firstName (*str*):

  The desired first name of the newly created user
  
  *Example:*
  
	interface.account_service.users.CreateUser(firstName="Han")

#### lastName (*str*):

  The desired last name of the newly created user
  
  *Example:*
  
	interface.account_service.users.CreateUser(lastName="Solo")

#### client_id (*str*):

  The desired client id for the newly created user (defaults to mds-account-ui).
  
  **Exmaple:**
  
	interface.account_service.users.CreateUser(client_id="mgp")

### **Kwargs:**

#### comments (*str*):

  The desired comments for the user
  
  *Example:*
  
	interface.account_service.users.CreateUser(comments="Never tell me the odds")

----

## Update User

### **Args:**

#### userId (*str*):

  The identifier of the desired user
  
  *Example:*
  
	interface.account_service.users.UpdateUser(userId="f:3a34d893-5d36-4cb8-9cfc-6b2a6678de3b:1")
   
### **Kwargs:**

#### emailAddress (*str*):

  The email address for the desired user
  
  *Example:*
  
	interface.account_service.users.UpdateUser(emailAddress="my_user@mail.com")

#### firstName (*str*):

  The first name of the desired user
  
  *Example:*
  
	interface.account_service.users.UpdateUser(firstName="Han")

#### lastName (*str*):

  The last name of the desired user
  
  *Example:*
  
	interface.account_service.users.UpdateUser(lastName="Solo")

#### comments (*str*):

  The desired comments for the user
  
  *Example:*
  
	interface.account_service.users.UpdateUser(comments="Never tell me the odds")

----

## Get Users

### **Args:**

#### userId (*str*):

  The identifier for the desired user (defaults to None).
  
  *Example:*
  
	interface.account_service.users.GetUsers(userId="f:3a34d893-5d36-4cb8-9cfc-6b2a6678de3b:1")

#### username (*str*):

  The username of the desired user (defaults to None).
  
  **Exmaple:**
  
	interface.account_service.users.GetUsers(username="my_user@mail.com")
	
### **Kwargs:**

#### pageSize (*int*):

  The desired number of objects returned
  
  *Example:*
  
	interface.account_service.users.GetUsers(pageSize=100)
	
#### page (*int*):

  The desired starting page for pagination (0 is the first page)
  
  *Example:*
  
	interface.account_service.users.GetUsers(page=0)

----

## Delete User

### **Args:**

#### userId (*str*):

  The identifier of the desired user
  
  *Example:*
  
	interface.account_service.users.DeleteUser(userId="f:3a34d893-5d36-4cb8-9cfc-6b2a6678de3b:1")
