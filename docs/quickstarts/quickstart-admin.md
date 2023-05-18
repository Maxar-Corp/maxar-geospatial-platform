# Quick Start for Admin

## Initializing

After setting up the `.MGP-config` file from the [Getting Started](../index.md) section, run the following code to create an instance of the Interface class. This class will be used to access the functionality of the MGP-SDK.

	from MGP_SDK.interface import Interface
	interface = Interface()
	
	
## Accounts

### Getting the account id

The account ID is used for making updates 

	account = interface.account_service.account_info.GetAccounts()
	accountId = account['accounts'][0]
	
	
## User functions

### Search for an existing activation or user

The Search functionality can search through activations or users within the user's account. The search term can be a partial word and will filter all results that fit that search term.

	interface.account_service.search(search_type="activation", search_term="my_activation")
	interface.account_service.search(search_type="user", search_term="my_user")

### Creating a new user

In order to create a new user, the function requires a user type, account Id, activation Id, email address, first name, and last name

	interface.account_service.Users.CreateUser(user_type="BASE_USER", accountId=<accountId>, activationId=<activationId>, emailAddress="email@address.com", firstName="John", lastName="Smith")

### Searching for an existing user

Alongside the Search functionality described above, there is a more precise way to search for existing users. This is done with the GetUsers function, and can return details for one user or all users within an account.

	interface.account_service.Users.GetUsers()
	interface.account_service.Users.GetUsers(userId=<user's Id>)
	interface.account_service.Users.GetUsers(username="email@address.com")
	
### Updating an existing user

If certain adjustments need to be made to an existing user, the UpdateUser function can make those changes. The user's Id is required to utilize the call. NOTE: User type and the account the user is tied to cannot be changed.

	interface.account_service.Users.UpdateUser(userId=<user's Id>, firstName="Bob", phone="1234567890", emailAddress="new@email.com")
	
### Deleting an existing user

	interface.account_service.Users.DeleteUser(userId=<user's Id>)


## Activations 

### Searching for an existing activation

Alongside the Search functionality described above, there is a more precise way to search for existing activations. This is done with the GetActivations function, and can return details for an activation within an account

	interface.account_service.activations.GetActivations()
	interface.account_service.activations.GetActivations(activationId=<activation's Id>)
