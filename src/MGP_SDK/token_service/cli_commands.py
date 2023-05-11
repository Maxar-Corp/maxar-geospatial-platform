import sys, click, os
from MGP_SDK.interface import Interface
interface = Interface()
@click.command()
def create_token():
    home_dir = os.path.expanduser("~")
    if os.path.exists(os.path.join(home_dir, '.MGP-config')):
        config_file = os.path.join(home_dir, '.MGP-config')
        with open(config_file, 'r') as config:
            for line in config:
                if "secret:" in line:
                    proceed = click.prompt('Token already exists would you like to create another? y/n')
                    if proceed.lower() == 'n':
                        return click.echo('Token creation aborted')
                    elif proceed.lower() == 'y':
                        pass
                    else:
                        return click.echo("Invalid input. Please run command again and enter y or n")
        token = interface.token.create_token_record()
        with open(config_file, 'a') as config:
            config.write('tokenId:{} secret:{}'.format(token['id'],token['secret']))
        click.echo('Token and Secret stored in config file. {}'.format(config_file))
    else:
        return click.echo("Config file not found. Please run 'config' command to create a config file")
    click.echo("Token ID: {} \nSecret: {} ".format(token['id'], token['secret']))

@click.command()
def get_tokens():
    return click.echo(interface.token.get_user_tokens())
@click.command()
def delete_tokens():
    home_dir = os.path.expanduser("~")
    token_id = click.prompt('Token ID to delete')
    if os.path.exists(os.path.join(home_dir, '.MGP-config')):
        config_file = os.path.join(home_dir, '.MGP-config')
        with open(config_file, "r+") as f:
            before_config = f.readlines()
            f.seek(0)
            for line in before_config:
                if token_id not in line:
                    f.write(line)
            f.truncate()
    response = interface.token.delete_tokens(token=token_id)
    return click.echo(response)

@click.command()
def show_secret():
    home_dir = os.path.expanduser("~")
    token_present = False
    if os.path.exists(os.path.join(home_dir, '.MGP-config')):
        config_file = os.path.join(home_dir, '.MGP-config')
        with open(config_file, 'r') as file:
            for line in file:
                if 'secret:' in line:
                   token_present = True
                   secret = line.split('secret:')[1]
                   return click.echo("Secret Token: {}".format(secret))
        if not token_present:
            click.echo("No Token found. Please run the 'createToken' command to create a token")
    else:
        return click.echo("Config file not found. Please run 'config' command to create a config file")


