import sys, click, os
from MGP_SDK.interface import Interface
interface = Interface()
token_interface = interface.token


def check_for_config():
    home_dir = os.path.expanduser("~")
    if os.path.exists(os.path.join(home_dir, '.MGP-config')):
        token_interface = interface.token
    else:
        raise Exception(
            "MGP config file not found. Please ensure that your config file is located in your home directory"
        )
    return token_interface


@click.command()
@click.option('--name', '-n', help='Token name', type=str)
@click.option('--description', '-d', help='Token description', type=str)
def create_token(name, description):
    """
    Function creates a new API token
    Args:
        name (string) = Desired token name
        description (string) = Desired token description
    Returns:
        API token to be used for alternative authentication
    """

    check = check_for_config()
    token_record = token_interface.get_user_tokens()
    if len(token_record) > 0:
        proceed = click.prompt('Token already exists would you like to create another? y/n')
        if proceed.lower() == 'n':
            return click.echo('Token creation aborted')
        elif proceed.lower() == 'y':
            pass
        else:
            return click.echo("Invalid input. Please run command again and enter y or n")
    if name:
        name = name
    else:
        name = click.prompt('Token name')
    if description:
        description = description
    else:
        description = click.prompt('Token description')
    token = token_interface.create_token_record(name, description)
    token_record_2 = token_interface.get_user_tokens()
    desired = [i['api_token'] for i in token_record_2 if i['name'] == name][0]
    click.echo('Token created. apiToken is {}'.format(desired))


@click.command()
def get_tokens():
    """
    Function lists all tokens a user has previously created
    Returns:
         List of all user API tokens
    """

    check = check_for_config()
    return click.echo(token_interface.get_user_tokens())


@click.command()
@click.option('--id', '-i', help='Token ID')
def delete_tokens(token_id):
    """
    Function deletes an API token
    Args:
        token_id (string) = Desired API token ID to delete
    Returns:
        Confirmation message of deletion
    """

    check = check_for_config()
    if token_id:
        token_id = token_id
    else:
        token_id = click.prompt('Token ID to delete')
    proceed = click.prompt("Are you sure you want to delete this token? y/n")
    if proceed.lower() == 'n':
        return click.echo('Token deletion aborted')
    elif proceed.lower() == 'y':
        pass
    else:
        return click.echo("Invalid input. Please run command again and enter y or n")
    delete = token_interface.delete_tokens(token=token_id)
    token_record = token_interface.get_user_tokens()
    if len(token_record) > 0:
        for i in token_record:
            if token_id not in i['id']:
                click.echo("Token successfully deleted")
    else:
        click.echo("Token successfully deleted")
