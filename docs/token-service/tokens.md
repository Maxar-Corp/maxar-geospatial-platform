# Tokens

----

## Create User Token
Creates a new token to utilize in place of an OAuth token. A dictionary is returned with the id, name,
        description, createDate, and secret fields. NOTE: Make sure to save the secret key as this will be the only time
        it is visible. If a secret key is lost, a new one must be created.
        
  
  *Example:*
  
	interface.tokens.create_token_record()

## Get User Token
Gets a list of all tokens associated with your user
  
*Example:*
  
	interface.tokens.get_user_token()

## Delete User Token(s)
 Deletes one or more tokens for one or more ids. Pass either a string of a token id to delete a single token or
        pass a list of strings of token ids to delete multiple tokens at once
 ### **Args:**

#### token (*str* or *list*):
*Single Delete Example:*

    interface.tokens.delete_tokens(token='string of tokenId')

*Multiple Delete Example*

    interface.tokens.delete_tokens(token=['string of tokenId', 'string of tokenId', 'string of tokenId'])
