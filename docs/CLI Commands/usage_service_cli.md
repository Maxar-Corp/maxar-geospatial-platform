# Usage Service CLI

### Account usage
*Note: Only account admins will be able to run this command*

Options:

	--page, -p, Desired starting page. Defaults to 0 (first page)
	--page_size, -ps, Desired number of returned objects. Defaults to 10
	--sort, -s, Desired variable to sort by. Defaults to id
Lists one or more account's usage. Sort options are: `id`, `accountNumber`, `sapLicenseId`, `licensee`, `soldTo`, `totalCreditsUsed`, `numberOfActivations`, and `numberOfUsers`

- In the terminal, enter `mgp account-usage` and pass optional parameters if desired

Example:

	mgp account-usage -s accountNumber

### Activation usage
*Note: Only account admins will be able to run this command*

Options:

	--page, -p, Desired starting page. Defaults to 0 (first page)
	--page_size, -ps, Desired number of returned objects. Defaults to 10
	--sort, -s, Desired variable to sort by. Defaults to id
	--client_id, -c, Desired client ID. Defaults to mgp client ID
Lists one or more activation's usage. Sort options are: `id`, `activationNumber`, `sapContractIdentifier`, `sapLineItem`, `startDate`, `endDate`, `creditLimit`, `totalCreditsUsed`, `creditsUsedPercentage`, `numberOfUsers`, `totalUsers`, `accounTotalUsers`, `accountName`, `accountNumber`, `accountSapLicenseId`, `accountLicensee`, `accountSoldTo`, `userLimit`, `dailyCreditLimitTotal`, `dailyCreditLimitUsed`, and `clientContextId`

- In the terminal, enter `mgp activation-usage` and pass optional parameters if desired

Example:

	mgp activation-usage -s creditLimit

### User usage
*Note: Only account admins will be able to run this command*

Options:

	--page, -p, Desired starting page. Defaults to 0 (first page)
	--page_size, -ps, Desired number of returned objects. Defaults to 10
	--sort, -s, Desired variable to sort by. Defaults to id
	--client_id, -c, Desired client ID. Defaults to mgp client ID
Lists one or more user's usage. Sort options are: `id`, `username`, `accountId`, `activationNumber`, `accountNumber`, `accountSapLicenseId`, `accountLicensee`, `accountSoldTo`, `totalCreditsUsed`, `dailyCreditLimitTotal`, `dailyCreditLimitUsed`, `userType`, and `clientContextId`

- In the terminal, enter `mgp user-usage` and pass optional parameters if desired

Example:

	mgp user-usage -s username

### Usage is allowed
*Note: Only account admins will be able to run this command*

Checks if usage credit limit has been reached

- In the terminal, enter `mgp usage-is-allowed`

Example:

	mgp usage-is-allowed

### Usage overview
*Note: Only account admins will be able to run this command*

Shows the overview of usage used for the account the user is tied to

- In the terminal, enter `mgp usage-overview`

Example:

	mgp usage-overview
