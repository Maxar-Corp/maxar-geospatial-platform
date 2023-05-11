# Rate Table

----

## Get Table

### **Args:**

#### table_id (*int*):

  The identifier of the desired rate table (defaults to None).
  
  *Example:*
  
	interface.account_service.rate_table_info.GetTable(table_id=1)
	
----

## Get Activations For Table

### **Args:**

#### table_id (*int*):

  The identifier for the desired rate table
  
  *Example:*
  
	interface.account_service.rate_table_info.GetActivationsForTable(table_id=1)

----

## Get Rate Amounts

### **Args:**

#### table_id

  The identifier for the desired rate table
  
  *Example:*
  
	interface.account_service.rate_table_info.GetRateAmounts(table_id=1)

----

## Get Credit Types

  *Example:*
  
	interface.account_service.rate_table_info.GetCreditTypes()
	
----

## Get Rate Tables and Associated Activations

  *Example:*
  
	interface.account_service.rate_table_info.get_rate_tables_and_associated_activations()
