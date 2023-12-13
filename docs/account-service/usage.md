# Usage
<hr>

The Usage portion of the MGP_SDK provides an interface for usage methods.

___

### Getting Started: 
```python
from MGP_SDK.interface import Interface

interface = Interface()
```

### Package methods
* [Account Usage](#get-account-usage)
* [Activation Usage](#get-activation-usage)
* [User Usage](#get-user-usage)

## Get Account Usage 
**get_account_usage()**

Retrieves the usage on an account

**Returns:** Dictionary of usage on an account

**Kwargs:**

* page (*int*): Starting page. First page is page 0
* pageSize (*int*): Number of items returned per page
* sortBy (*string*): Sorting arrangement. Available options are:
    * `id`
    * `accountNumber`
    * `sapLicenseId`
    * `licensee`
    * `soldTo`
    * `totalCreditsUsed`
    * `numberOfActivations`
    * `numberOfUsers`
---

## Get Activation Usage 
**get_activation_usage()**

Retrieves the usage on an activation

**Returns:** Dictionary of usage on an activation

**Kwargs:**

* page (*int*): Starting page. First page is page 0
* pageSize (*int*): Number of items returned per page
* sortBy (*string*): Sorting arrangement. Available options are:
    * `id`
    * `activationNumber`
    * `sapContractIdentifier`
    * `sapLineItem`
    * `startDate`
    * `endDate`
    * `creditLimit`
    * `totalCreditsUsed`
    * `creditsUsedPercentage`
    * `numberOfUsers`
    * `totalUsers`
    * `accountTotalUsers`
    * `accountName`
    * `accountNumber`
    * `accountSapLicenseId`
    * `accountLicensee`
    * `accountSoldTo`
    * `userLimit`
    * `dailyCreditLimitTotal`
    * `dailyCreditLimitUsed`

---

## Get User Usage 
**get_user_usage()**

Retrieves the usage for a user

**Returns:** 

**Kwargs:**

* page (*int*): Starting page. First page is page 0
* pageSize (*int*): Number of items returned per page
* sortBy (*string*): Sorting arrangement. Available options are:
    * `id`
    * `username`
    * `accountId`
    * `activationNumber`
    * `accountNumber`
    * `accountSapLicenseId`
    * `accountLicensee`
    * `accountSoldTo`
    * `totalCreditsUsed`
    * `dailyCreditLimitTotal`
    * `dailyCreditLimitUsed`
    * `userType`