import click
import sys
import os
from MGP_SDK.interface import Interface


def check_for_config():
    home_dir = os.path.expanduser("~")
    if os.path.exists(os.path.join(home_dir, '.MGP-config')):
        cli_interface = Interface().streaming
    else:
        raise Exception(
            "MGP config file not found. Please ensure that your config file is located in your home directory"
        )
    return cli_interface


@click.command()
@click.option('--username', '-u', help='Your username', type=str)
@click.option('--password', '-p', help='Your password', type=str)
@click.option('--client_id', '-c', help='Your client id', type=str)
def config_file(username=None, password=None, client_id=None):
    """
    Function creates a configuration file for authentication use for Maxar tenants
    """

    home_dir = os.path.expanduser("~")
    if os.path.exists(os.path.join(home_dir, '.MGP-config')):
        check = input("An MGP-config file already exists. Overwrite?[y/n]: ")
        if check.lower() == 'n':
            return click.echo("Config file setup aborted")
        elif check.lower() == 'y':
            pass
        else:
            return click.echo("Invalid input. Please run command again and enter either y or n")

    if username:
        username = username
    else:
        username = click.prompt('Your username')
    if password:
        password = password
    else:
        password = click.prompt('Your password', hide_input=True, confirmation_prompt=True)
    if client_id:
        client_id = client_id
    else:
        client_id = click.prompt('Your client id')

    config = ['[mgp]', 'user_name={}'.format(username), 'user_password={}'.format(password),
              'client_id={}'.format(client_id)]
    with open(os.path.join(home_dir, ".MGP-config"), "w") as f:
        for line in config:
            f.write(line)
            f.write('\n')

    return click.echo("MGP-config file created. File is located in {}".format(home_dir))


@click.command()
@click.option('--password', '-p', help="New password", type=str)
def reset_password(password):
    """
    Function updates the password in the configuration file
    """

    home_dir = os.path.expanduser("~")
    if os.path.exists(os.path.join(home_dir, '.MGP-config')):
        pass
    else:
        return click.echo("No .MGP-config file found. Please create file")
    password = click.prompt('Enter new password', hide_input=True, confirmation_prompt=True)
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        text = f.readlines()
        text[2] = 'user_password={}\n'.format(password)
        with open(os.path.join(home_dir, ".MGP-config"), 'w') as f:
            f.writelines(text)
    return click.echo("Password updated")


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)', type=str)
@click.option('--filter', '-f', help='CQL filter used to refine data of search', type=str)
@click.option('--shapefile', '-s', help='Binary of whether or not to return as shapefile format', type=bool)
@click.option('--featureprofile', '-fp', help='String of the desired stacking profile. Defaults to account Default',
              type=str)
@click.option('--typename', '-t',
              help='String of the typename. Defaults to FinishedFeature. Example input MaxarCatalogMosaicProducts',
              type=str)
def search(bbox=None, srsname="EPSG:4326", filter=None, shapefile=False, featureprofile=None, typename=None):
    """
    Function searches an AOI using the WFS method and returns a list of features and their metadata that intersect with
    the AOI
    """

    check = check_for_config()
    if not typename:
        wfs = check.search(bbox, srsname=srsname, filter=filter, shapefile=shapefile, featureprofile=featureprofile)
    else:
        wfs = check.search(bbox, srsname=srsname, filter=filter, shapefile=shapefile, featureprofile=featureprofile,
                           typename=typename)
    click.echo(wfs)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)', type=str)
@click.option('--height', '-h', help='Integer value representing the vertical number of pixels to return', type=int)
@click.option('--width', '-w', help='Integer value representing the horizontal number of pixels to return', type=int)
@click.option('--img_format', '-img', help='String of the format of the response image either jpeg, png or geotiff',
              type=str)
@click.option('--zoom_level', '-z', help='Integer value of the zoom level. Used for WMTS', type=int)
@click.option('--download', '-d', help='Boolean of user option to download file locally', type=bool)
def download(bbox=None, height=None, width=None, img_format=None, zoom_level=None, download=True):
    """
    Function downloads an image or a list of image calls and returns the file location of the download. NOTE: Structure
    of call should be structured with one of the following:
    1) bbox, zoom_level, img_format
    2) bbox, identifier, gridoffsets, img_format
    3) bbox, img_format, height, width
    """

    check = check_for_config()
    if zoom_level:
        if not bbox:
            raise Exception('zoom_level must have a bbox')
        else:
            wmts = check.download_image(zoom_level=zoom_level, bbox=bbox, img_format=img_format,
                                                download=download)
        click.echo(wmts)
    else:
        if not bbox or not img_format or not width or not height:
            raise Exception('height/width must have a bbox and an img_format')
        else:
            wms = check.download_image(bbox=bbox, img_format=img_format, height=height, width=width,
                                               display=False, download=download)
        click.echo(wms)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)', type=str,
              prompt='Enter bbox in miny,minx,maxy,maxx format')
def calculate_bbox_sqkm(bbox=None):
    """
    Function calculates the area in square kilometers of the bbox
    """

    check = check_for_config()
    sqkm = check.calculate_sqkm(bbox=bbox)
    click.echo("Square kilometers of bbox is: {}".format(sqkm))
