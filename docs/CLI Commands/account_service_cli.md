# Account Service CLI

### Get user account
*Note: Only account admins will be able to run this command*

Options:

	--account_id, -ai, Desired account ID
	--account_name, -an, Desired account name
	--id_name, -idn, Binary for short list of accounts and names. Defaults to False
	--types, -t, Binary for list of all account types. Defaults to False
Lists all accounts the user is a part of if not parameters are passed, or lists a desired account based on parameters passed

- In the terminal, enter `mgp get-accounts` and pass optional flags if desired

Example:

	mgp get-accounts -an myAccountName

### Account roles
*Note: Only account admins will be able to run this command*

Lists all account roles for the account the user is tied to

- In the terminal, enter `mgp account-roles`

Example:

	mgp account-roles

### Account comments
*Note: Only account admins will be able to run this command*

Options:

	--account_id, -ai, Desired account ID

Lists all comments for a desired account

- In the terminal, enter `mgp account-comments` and pass the required flag

Example:

	mgp account-comments -ai <ID>

### Get activations
*Note: Only account admins will be able to run this command*

Options:

	--activations_id, -ai, Desired activation ID. Defaults to None
	--activation_number, -an, Desired activation number. Defaults to None
Lists all activations a user is a part of if no parameters are passed, or lists a desired activation based on parameters passed

- In the terminal, enter `mgp get-activations` and pass optional flags if desired

Example:

	mgp get-activations -an myActivationName

### Activations for an account
*Note: Only account admins will be able to run this command*

Options:

	--account_id, -ai, Desired account ID

- In the terminal, enter `mgp activations-for-account` and pass the required flag

Example:

	mgp activations-for-account -ai <ID>

### Activation credit limit
*Note: Only account admins will be able to run this command*

Options:

	--activation_number, -an, Desired activation number

- In the terminal, enter `mgp activation-credit-limit` and pass the required flag

Example:

	mgp activation-credit-limit -an myActivationNumber

### Activation types
*Note: Only account admins will be able to run this command*

Lists the activation types

- In the terminal, enter `mgp activation-types`

Example:

	mgp activation-types

### Get products
*Note: Only account admins will be able to run this command*

Lists available products for the user

- In the terminal, enter `mgp get-products`

Example:

	mgp get-products

### Product filter
*Note: Only account admins will be able to run this command*

Options:

	--product_category, -pc, Desired product category. Defaults to None
	--usage_type, -ut, Desired usage type. Defaults to None
	--age, -a, Desired age range. Defaults to None
	--catalog_type, -ct, Desired catalog type. Defaults to None
Lists all products based on filter parameters passed in

- In the terminal, enter `mgp product-filter` and pass one or more of the flags

Example:

	mgp product-filter -ut Streaming

### Get rate table
*Note: Only account admins will be able to run this command*

Options:

	--table_id, -t, Desired rate table ID. Defaults to None
Lists all rate tables for a user if no parameters are passed, or lists a desired rate table based on parameters passed

- In the terminal, enter `mgp get-rate-table` and pass the optional flag if desired

Example:

	mgp get-rate-table -t <ID>

### Get activation for rate table
*Note: Only account admins will be able to run this command*

Options:

	--table_id, -t, Desired rate table ID
Lists all activations associated with the desired rate table

- In the terminal, enter `mgp get-activation-for-table` and pass the required flag

Example:

	mgp get-activation-for-table -t <ID>

### Get credit types
*Note: Only account admins will be able to run this command*

Lists all available credit types

- In the terminal, enter `mgp get-credit-types`

Example:

	mgp get-credit-types

### Get rate amounts
*Note: Only account admins will be able to run this command*

Options:

	--table_id, -t, Desired rate table ID
Lists all rate amounts for the desired rate table

- In the terminal, enter `mgp get-rate-amounts` and pass the required flag

Example:

	mgp get-rate-amounts -t <ID>

### Get table and activations
*Note: Only account admins will be able to run this command*

Lists all rate tables a user has access to and their products and the activations that have access to the tables

- In the terminal, enter `mgp get-table-and-activations`

Example:

	mgp get-table-and-activations

### Get roles
*Note: Only account admins will be able to run this command*

Lists all roles

- In the terminal, enter `mgp get-roles`

Example:

	mgp get-roles

### User types
*Note: Only account admins will be able to run this command*

Lists all available user types

- In the terminal, enter `mgp user-types`

Example:

	mgp user-types

### Get users
*Note: Only account admins will be able to run this command*

Options:

	--user_id, -id, Desired user ID. Defaults to None
	--username, -u, Desired username. Defaults to None
	--page_size, -ps, Desired page size. Defaults to None
	--page, -p, Desired starting page number. Defaults to None
Lists all users on the same account if no parameters are passed, or lists a desired user based on parameters passed

- In the terminal, enter `mgp get-users` and pass optional flags if desired

Example:

	mgp get-users -u employee@company.com

### Create user
*Note: Only account admins will be able to run this command*

Options:

	--user_type, -ut, Desired user type
	--account_id, -acc_id, Desired account ID
	--activation_id, -act_id, Desired activaiton ID
	--email, -e, Desired email address
	--first_name, -f, Desired first name
	--last_name, -l, Desired last name
	--country, -c, Desired country of origin
	--client_id, -cid, Desired client ID. Defaults to mgp
Creates a new user based on parameters passed

- In the terminal, enter `mgp create-user` and pass all required flags. If a required flag is not passed, a prompt will appear for the missed parameter(s)

Example:

	mgp create-user -ut BASE_USER -acc_id <ID> -act_id <ID> -e user@company.com -f first -l last -c United States of America -c client

### Update user
*Note: Only account admins will be able to run this command*

Options:

	--user_id, -id, Desired user ID. Required
	--username, -u, Desired username. Defaults to None
	--first_name, -f, Desired first name. Defaults to None
	--last_name, -l, Desired last name. Defaults to None
	--phone, -p, Desired phone number. Defaults to None
	--yes, -y, Flag to bypass one or more update options. Defaults to False
Updates desired user based on parameters passed

- In the terminal, enter `mgp update-user` and pass in the required flag

Example:

	mgp update-user -id desiredUserId -u new.username@company.com -y

### Update user roles
*Note: Only account admins will be able to run this command*

Options:

	--user_id, -u, Desired user ID
	--roles, -r, Name of role(s) to add. If multiple roles, separate roles by comma
	--client_id, -c, Desired client ID. Defaults to mgp client ID
	--delete, -d, Flag to delete roles. Defaults to False
Adds or removes roles to the desired user based on parameters passed

- In the terminal, enter `mgp update-user-roles` and pass in the required flags

Example:

	mgp update-user-roles -u userID -r "DAILY_TAKE,PCM" -c clientID

### Get user roles
*Note: Only account admins will be able to run this command*

Options:

	--user_id, -u, Desired user ID
Lists all roles tied to the desired user

- In the terminal, enter `mgp get-user-roles` and pass the required flag

Example:

	mgp get-user-roles userID

### Get user available roles
*Note: Only account admins will be able to run this command*

Options:

	--user_id, -u, Desired user ID
	--client_id, -c, Desired client ID, Defaults to mgp client ID
Lists all roles that can be tied to the desired user

- In the terminal, enter `mgp get-user-available-roles` and pass the required flags

Example:

	mgp get-user-available-roles -u userID -c clientID

### Delete user
*Note: Only account admins will be able to run this command*

Options:

	--user_id, -u, Desired user ID
	--yes, -y, Flag to bypass deletion confirmation. Defaults to False
Deletes a user

- In the terminal, enter `mgp delete-user` and pass the required flag

Example:

	mgp delete-user -u userID -y
