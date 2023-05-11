# Product

----

## Get Products

  *Example:*
  
	interface.account_service.products.get_products()

----

## Filter Products

### **Args:**

#### productCategory (*str*):

  The desired product category to filter by (defaults to None).
  
  *Example:*
  
	interface.account_service.products.filter_products(productCategory="Vivid Standard")

#### usageType (*str*):

  The desired usage type to filter by. Options are Download or Streaming (defaults to None).
  
  *Example:*
  
	interface.account_service.products.filter_products(usageType="Streaming")

#### age (*str*):

  The desired age to filter by (defaults to None).
  
  *Example:*
  
	interface.account_service.products.filter_products(age="5")

#### catalogType (*str*):

  The desired catalog type to filter by. Options are Archive or Online (defaults to None).
   
  *Example:*
   
	interface.account_service.products.filter_products(catalogType="Online")
