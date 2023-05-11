# Usage

----

## Get Account Usage

### **Kwargs:**

#### page (*int*):

  The desired starting page for pagination. First page is page 0.
  
  *Example:*
  
	interface.account_service.usage.get_account_usage(page=0)
	
#### pageSize (*int*):

  The desired amount of returned objects.
  
  *Example*:
  
	interface.account_service.usage.get_account_usage(pageSize=10)
	
#### sortBy (*str*):

  The desired sorting arrangment. Available options are:
	id
	accountNumber
	sapLicenseId
	licensee
	soldTo
	totalCreditsUsed
	numberOfActivations
	numberOfUsers
	
  *Example*:
  
	interface.account_service.usage.get_account_usage(sortBy='id')
	
----

## Get Activation Usage

### **Kwargs:**

#### page (*int*):

  The desired starting page for pagination. First page is page 0.
  
  *Example:*
  
	interface.account_service.usage.get_activation_usage(page=0)
	
#### pageSize (*int*):

  The desired amount of returned objects.
  
  *Example*:
  
	interface.account_service.usage.get_activation_usage(pageSize=10)
	
#### sortBy (*str*):

  The desired sorting arrangment. Available options are:
	id
	activationNumber
	sapContractIdentifier
	sapLineItem
	startDate
	endDate
	creditLimit
	totalCreditsUsed
	creditsUsedPercentage
	numberOfUsers
	totalUsers
	accountTotalUsers
	accountName
	accountNumber
	accountSapLicenseId
	accountLicensee
	accountSoldTo
	userLimit
	dailyCreditLimitTotal
	dailyCreditLimitUsed
	clientContextId
	
  *Example*:
  
	interface.account_service.usage.get_activation_usage(sortBy='id')
	
#### clientContextId (*str*):

  The desired Client ID
  
  *Example:*
  
	interface.account_service.usage.get_activation_usage(clientContextId='123abc45-12ab-1a23-abcd-123abc456def')
	
----

## Get User Usage

### **Kwargs:**

#### page (*int*):

  The desired starting page for pagination. First page is page 0.
  
  *Example:*
  
	interface.account_service.usage.get_user_usage(page=0)
	
#### pageSize (*int*):

  The desired amount of returned objects.
  
  *Example*:
  
	interface.account_service.usage.get_user_usage(pageSize=10)
	
#### sortBy (*str*):

  The desired sorting arrangment. Available options are:
	id
	username
	accountId
	activationNumber
	accountNumber
	accountSapLicenseId
	accountLicensee
	accountSoldTo
	totalCreditsUsed
	dailyCreditLimitTotal
	dailyCreditLimitUsed
	userType
	clientContextId
	
  *Example*:
  
	interface.account_service.usage.get_user_usage(sortBy='id')
	
#### clientContextId (*str*):

  The desired Client ID
  
  *Example:*
  
	interface.account_service.usage.get_user_usage(clientContextId='123abc45-12ab-1a23-abcd-123abc456def')
