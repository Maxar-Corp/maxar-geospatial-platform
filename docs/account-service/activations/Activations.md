# Activation

----

## Get Activations

### **Args:**

#### activationId (*int*):

  The identifier of the desired activation (defaults to None).
  
  *Example:*
  
	interface.account_service.activations.GetActivations(activationId=1)
	
#### activation_number (*str*):

  The number of the desired activation (Defaults to None).
  
  *Example:*
  
	interface.account_service.activations.GetActivations(activation_number="ACT-123456")

----

## Get Activation Types

  *Example:*
  
	interface.account_service.activations.GetActivationTypes()

----

## Get Activations For Account

### **Args:**

#### accountId (*int*):

  The identifier for the desired account
  
  *Example:*
  
	interface.account_service.activations.GetActivationsForAccount(accountId=1)

----

## Get Activation Credit Limit

### **Args:**

#### activation_number (*str*):

  The number of the desired activation.
  
  *Example:*
  
	interface.account_service.activations.get_activation_credit_limit(activation_number="ACT-123456")
