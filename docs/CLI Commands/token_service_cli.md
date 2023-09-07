# Token Service CLI

### Create a User Token
Options:

	--name, -d, The desired name for the token
	--description, -d, The description for the newly created token
Create a new Maxar API token for authentication without a JWT

- In the terminal, enter `mgp create-token` to create an api token to authenticate into the platform
- If a token has already been created enter `mgp get-tokens` into the terminal to show the existing tokens

Example:

	mgp create-token
Then enter in the information as the prompts appear
Or

	mgp create-token -n <tokenName> -d <tokenDescription>

### List a user's token(s)
Lists out all tokens that have been created by a user

Example:

	mgp get-tokens

### Delete a User Token
Options:

	--token_id, -id, The ID for the desired token. Note: the ID is not the same as the API token
Deletes an existing API token for a user

- In the terminal, enter `delete_token` to delete an api token.
- Enter in the desired token_id
- Confirm deletion of api token

Example:

	mgp delete-tokens
Then enter in the information as the prompts appear
Or

	mgp delete-tokens -id <tokenId>
