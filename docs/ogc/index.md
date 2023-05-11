## Getting started

**MPS Portal SDK** is a Python library for accessing Maxar's Portal Services API endpoints to 
retrieve and manipulate services including account, activation and user access as well as OGC services.
The connection is established using login credentials stored in a local config file.


Installation:

1. Installation via pip is recommened: ``pip install Maxar-MPS`` in your environment.
2. We recommend creating a credentials file to store your login information for future sessions in one of two ways. 
	* Use the command line interface command ``config`` from the command prompt and follow the prompts. See [Command Line Interface](cli_commands)
	* Create a credentials file called ``.mgp-config`` in your home directory with the following format

			[mps] 
			user_name=<your-user-name>
			user_password=<your-password>
			user_tenant=<your-base-url> i.e. https://marianas-test.dev.mdsdev.com

After creating your config file, you are now ready to start with the [Quickstart Guide](quickstart)