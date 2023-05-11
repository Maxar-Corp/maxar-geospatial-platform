# Account 

----

## Get Accounts

### **Args:**

#### accountId (*int*):

  The identifier of the desired account (defaults to None).
  
  *Example:*
  
    interface.account_service.account_info.GetAccounts(accountId=1)

#### accountName (*str*):

  The name of the desired account (defaults to None).
  
  *Example:*
  
    interface.account_service.account_info.GetAccounts(accountName="My Account")

#### id_names (*bool*):

  Flag that dictates whether or not to return a condensed list of account ids and account names (defaults to False).
  
  *Example:*
  
    interface.account_service.account_info.GetAccounts(id_names=True)

#### types (*bool*):

  Flag that dictates whether or not to return a list of all account types (defaults to False).
  
  *Example:*
  
    interface.account_service.account_info.GetAccounts(types=True)
