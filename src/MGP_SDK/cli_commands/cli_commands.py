import json
import click
import os
from MGP_SDK.interface import Interface


@click.group()
def cli():
    pass


def _check_for_config():
    home_dir = os.path.expanduser("~")
    if os.path.exists(os.path.join(home_dir, '.MGP-config')):
        pass
    else:
        raise Exception(
            "MGP config file not found. Please ensure that your config file is located in your home directory"
        )


def _streaming():
    _check_for_config()
    streaming_interface = Interface().streaming
    return streaming_interface


def _token():
    _check_for_config()
    token_interface = Interface().token
    return token_interface


def _admin():
    _check_for_config()
    admin_interface = Interface().account_service
    return admin_interface


def _usage():
    _check_for_config()
    usage_interface = Interface().usage_service
    return usage_interface


def _discovery():
    _check_for_config()
    discovery_interface = Interface().discovery_service
    return discovery_interface


def _ordering():
    _check_for_config()
    ordering_interface = Interface().order_service
    return ordering_interface


def _tasking():
    _check_for_config()
    tasking_interface = Interface().tasking_service
    return tasking_interface


def _monitoring():
    _check_for_config()
    monitoring_interface = Interface().monitoring_service
    return monitoring_interface


def _analytics():
    _check_for_config()
    analytics_interface = Interface().analytics
    return analytics_interface


def _basemaps():
    _check_for_config()
    basemaps_interface = Interface().basemap_service
    return basemaps_interface

  
@click.command()
def home_dir():
    """
    Prints out the location of your machine's home directory
    """

    click.echo("The home directory is: {}".format(os.path.expanduser("~")))


@click.command()
@click.option('--name', '-n', help='Token name', type=str)
@click.option('--description', '-d', help='Token description', type=str)
def create_token(name, description):
    """
    Creates a new API token
    """

    token_interface = _token()
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
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        lines_to_write = []
        token_overwrite = False
        last = lines[-1]
        if "\n" in last:
            token_format = "api_token={}\n"
        else:
            token_format = "\napi_token={}\n"
        for line in lines:
            if "api_token" in line:
                lines_to_write.append(token_format.format(desired))
                token_overwrite = True
            else:
                lines_to_write.append(line)
        if not token_overwrite:
            lines_to_write.append(token_format.format(desired))
    with open(os.path.join(home_dir, ".MGP-config"), 'w') as f:
        f.writelines(lines_to_write)
    click.echo('Token created. apiToken is {}'.format(desired))


@click.command()
def get_tokens():
    """
    Lists all tokens a user has previously created
    """

    token_interface = _token()
    return click.echo(token_interface.get_user_tokens())


@click.command()
@click.option('--token_id', '-id', help='Token ID')
def delete_tokens(token_id):
    """
    Deletes an API token
    """

    token_interface = _token()
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
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
    with open(os.path.join(home_dir, ".MGP-config"), 'w') as w:
        for line in lines:
            if "api_token" not in line:
                w.write(line)
    if len(token_record) > 0:
        for i in token_record:
            if token_id not in i['id']:
                click.echo("Token successfully deleted")
    else:
        click.echo("Token successfully deleted")


@click.command()
@click.option('--username', '-u', help='Your username', type=str)
@click.option('--password', '-p', help='Your password', type=str)
@click.option('--client_id', '-c', help='Your client id', type=str)
def config_file(username, password, client_id):
    """
    Creates a configuration file for authentication use for Maxar tenants
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
    Updates the password in the configuration file
    """

    home_dir = os.path.expanduser("~")
    if os.path.exists(os.path.join(home_dir, '.MGP-config')):
        pass
    else:
        return click.echo("No .MGP-config file found. Please create file")
    password = click.prompt('Enter new password', hide_input=True, confirmation_prompt=True)
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        text = [i.replace('\n','') for i in f.readlines()]
        text[2] = f'user_password={password}'
        with open(os.path.join(home_dir, ".MGP-config"), 'w') as w:
            w.write('\n'.join([i.replace('\n','\\n') for i in text]))
    return click.echo("Password updated")


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)', type=str)
@click.option('--srsname', '-srs', help='String of the desired projection. Defaults to EPSG:4326', default='EPSG:4326')
@click.option('--filter', '-f', help='CQL filter used to refine data of search', type=str, default=None)
@click.option('--shapefile', '-s', help='Binary of whether or not to return as shapefile format', is_flag=True,
              default=False)
@click.option('--featureprofile', '-fp', help='String of the desired stacking profile. Defaults to account Default',
              type=str, default="Default")
@click.option('--typename', '-t',
              help='String of the typename. Defaults to FinishedFeature. Example input MaxarCatalogMosaicProducts',
              type=str, default="FinishedFeature")
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def search(bbox, srsname, filter, shapefile, featureprofile, typename, yes):
    """
    Searches an AOI using the WFS method and returns a list of features and their metadata that intersect with
    the AOI
    """

    streaming_interface = _streaming()
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "bbox" in line:
                if not yes:
                    bbox_check = click.prompt(
                        "A bbox has been found in the .MGP-config file. Would you like to use this "
                        "bbox?[y/n]")
                    if bbox_check.lower() == "n":
                        if bbox:
                            bbox = bbox
                        else:
                            return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                    elif bbox_check.lower() == "y":
                        bbox = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not bbox:
                    bbox = line.split("=")[1]
                elif yes and bbox:
                    bbox = bbox
            else:
                bbox = bbox
    if not typename:
        wfs = streaming_interface.search(
            bbox, srsname=srsname, filter=filter, shapefile=shapefile, featureprofile=featureprofile
        )
    else:
        wfs = streaming_interface.search(
            bbox, srsname=srsname, filter=filter, shapefile=shapefile, featureprofile=featureprofile, typename=typename
        )
    click.echo(wfs)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)', type=str)
@click.option('--srsname', '-srs', help='String of the desired projection. Defaults to EPSG:4326', default='EPSG:4326')
@click.option('--height', '-h', help='Integer value representing the vertical number of pixels to return. Defaults to '
                                     'None', type=int, default=None)
@click.option('--width', '-w', help='Integer value representing the horizontal number of pixels to return. Defaults to '
                                    'None', type=int, default=None)
@click.option('--img_format', '-img', help='String of the format of the response image either jpeg, png or geotiff. '
                                           'Defaults to jpeg', type=str, default='jpeg')
@click.option('--zoom_level', '-z', help='Integer value of the zoom level. Used for WMTS. Defaults to None', type=int,
              default=None)
@click.option('--outputpath', '-o', help='Path to desired download location. Defaults to home directory')
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def download(bbox, srsname, height, width, img_format, zoom_level, outputpath, yes):
    """
    Downloads an image or a list of image calls and returns the file location of the download. NOTE: Structure
    of call should be structured with one of the following: 1) bbox, zoom_level, img_format; 2) bbox, img_format, height, width
    """

    streaming_interface = _streaming()
    if not outputpath:
        home_dir = os.path.expanduser("~")
        outputpath = os.path.join(home_dir, "CLI_download.{}".format(img_format))
    if zoom_level:
        home_dir = os.path.expanduser("~")
        with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
            lines = f.readlines()
            for line in lines:
                if "bbox" in line:
                    if not yes:
                        bbox_check = click.prompt(
                            "A bbox has been found in the .MGP-config file. Would you like to use this "
                            "bbox?[y/n]")
                        if bbox_check.lower() == "n":
                            if bbox:
                                bbox = bbox
                            else:
                                return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                        elif bbox_check.lower() == "y":
                            bbox = line.split("=")[1]
                        else:
                            return click.echo("Invalid input. Please run command again and enter either y or n")
                    elif yes and not bbox:
                        bbox = line.split("=")[1]
                    elif yes and bbox:
                        bbox = bbox
                else:
                    bbox = bbox
            wmts = streaming_interface.download_image(
                zoom_level=zoom_level, bbox=bbox, img_format=img_format, srsname=srsname, download=True,
                outputpath=outputpath
            )
        click.echo(wmts)
    else:
        if not img_format or not width or not height:
            raise Exception('height/width must have an img_format')
        else:
            home_dir = os.path.expanduser("~")
            with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if "bbox" in line:
                        if not yes:
                            bbox_check = click.prompt(
                                "A bbox has been found in the .MGP-config file. Would you like to use this "
                                "bbox?[y/n]")
                            if bbox_check.lower() == "n":
                                if bbox:
                                    bbox = bbox
                                else:
                                    return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                            elif bbox_check.lower() == "y":
                                bbox = line.split("=")[1]
                            else:
                                return click.echo("Invalid input. Please run command again and enter either y or n")
                        elif yes and not bbox:
                            bbox = line.split("=")[1]
                        elif yes and bbox:
                            bbox = bbox
                    else:
                        bbox = bbox
            wms = streaming_interface.download_image(
                bbox=bbox, img_format=img_format, height=height, width=width, srsname=srsname, display=False,
                download=True, outputpath=outputpath
            )
        click.echo(wms)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)', type=str)
@click.option('--zoom', '-z', help='Desired zoom level between 1 and 20', type=int, required=True)
@click.option('--srsname', '-s', help='Desired projection. Defaults to EPSG:4326', type=str, default='EPSG:4326')
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def get_tile_list(bbox, zoom, srsname, yes):
    """
    Acquires a list of tile calls dependent on the desired bbox and zoom level
    """

    streaming_interface = _streaming()
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "bbox" in line:
                if not yes:
                    bbox_check = click.prompt(
                        "A bbox has been found in the .MGP-config file. Would you like to use this "
                        "bbox?[y/n]")
                    if bbox_check.lower() == "n":
                        if bbox:
                            bbox = bbox
                        else:
                            return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                    elif bbox_check.lower() == "y":
                        bbox = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not bbox:
                    bbox = line.split("=")[1]
                elif yes and bbox:
                    bbox = bbox
            else:
                bbox = bbox
    if zoom > 20 or zoom < 1:
        raise Exception("Zoom level must be an integer between 1 and 20")
    tile_list = streaming_interface.get_tile_list_with_zoom(bbox=bbox, zoom_level=zoom, srsname=srsname)
    click.echo(tile_list)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)', type=str)
@click.option('--zoom', '-z', help='Desired zoom level between 1 and 20', type=int, required=True)
@click.option('--srsname', '-s', help='Desired projection. Defaults to EPSG:4326', type=str, default='EPSG:4326')
@click.option('--img_format', '-i', help='Desired output image format. Defaults to jpeg', type=str, default='jpeg')
@click.option('--outputpath', '-o', help='Desired output path for download. Defaults to home directory', type=str)
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def download_tiles(bbox, zoom, srsname, img_format, outputpath, yes):
    """
    Downloads all tiles within a bbox dependent on zoom level
    """

    streaming_interface = _streaming()
    if not outputpath:
        home_dir = os.path.expanduser("~")
        outputpath = os.path.join(home_dir, "CLI_download.{}".format(img_format))
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "bbox" in line:
                if not yes:
                    bbox_check = click.prompt(
                        "A bbox has been found in the .MGP-config file. Would you like to use this "
                        "bbox?[y/n]")
                    if bbox_check.lower() == "n":
                        if bbox:
                            bbox = bbox
                        else:
                            return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                    elif bbox_check.lower() == "y":
                        bbox = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not bbox:
                    bbox = line.split("=")[1]
                elif yes and bbox:
                    bbox = bbox
            else:
                bbox = bbox
    if zoom > 20 or zoom < 1:
        raise Exception("Zoom level must be an integer between 1 and 20")
    tiles = streaming_interface.download_tiles(
        bbox=bbox, zoom_level=zoom, srsname=srsname, img_format=img_format, outputpath=outputpath
    )
    click.echo(tiles)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)', type=str)
@click.option('--height', '-h', help='Desired height of image in pixels. Defaults to 512', type=int, default=512,
              required=True)
@click.option('--width', '-w', help='Desired width of image in pixels. Defaults to 512', type=int, default=512,
              required=True)
@click.option('--srsname', '-s', help='Desired projection. Defaults to EPSG:4326', type=str, default='EPSG:4326')
@click.option('--img_format', '-i', help='Desired output image format. Defaults to jpeg', type=str, default='jpeg')
@click.option('--outputpath', '-o', help='Desired output path for download. Defaults to home directory', type=str)
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def download_by_pixel_count(bbox, height, width, srsname, img_format, outputpath, yes):
    """
    Downloads the image of desired bbox dependent on pixel height and width
    """

    streaming_interface = _streaming()
    if not outputpath:
        home_dir = os.path.expanduser("~")
        outputpath = os.path.join(home_dir, "CLI_download.{}".format(img_format))
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "bbox" in line:
                if not yes:
                    bbox_check = click.prompt(
                        "A bbox has been found in the .MGP-config file. Would you like to use this "
                        "bbox?[y/n]")
                    if bbox_check.lower() == "n":
                        if bbox:
                            bbox = bbox
                        else:
                            return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                    elif bbox_check.lower() == "y":
                        bbox = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not bbox:
                    bbox = line.split("=")[1]
                elif yes and bbox:
                    bbox = bbox
            else:
                bbox = bbox
    if height > 8000 or height < 1:
        raise Exception("Height must be an integer between 1 and 8000")
    if width > 8000 or width < 1:
        raise Exception("Width must be an integer between 1 and 8000")
    image_by_pixel = streaming_interface.download_image_by_pixel_count(
        bbox=bbox, height=height, width=width, srsname=srsname, img_format=img_format, outputpath=outputpath
    )
    click.echo(image_by_pixel)


@click.command()
@click.option('--featureid', '-f', help='Desired feature ID', type=str, required=True)
@click.option('--thread_number', '-t', help='Desired thread number for multithreading. Defaults to 100', type=int,
              default=100)
@click.option('--bbox', '-b', help='String bounding box of AOI. Comma delimited set of coordinates. '
                                   '(miny,minx,maxy,maxx). Deafults to None', type=str, default=None)
@click.option('--mosaic', '-m', help='Flag to determine whether or not to mosaic images together. Defaults to False',
              is_flag=True, default=False)
@click.option('--srsname', '-s', help='Desired projection. Defaults to EPSG:4326', type=str, default='EPSG:4326')
@click.option('--outputdirectory', '-o', help='Desired output directory for download. Defaults to None', type=str,
              default=None)
@click.option('--image_format', '-i', help='Desired output image format. Defaults to jpeg', type=str, default='jpeg')
@click.option('--filename', '-fn', help='Desired filename for mosaiced image. Defaults to Maxar_Image', type=str,
              default='Maxar_Image')
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def full_res_image(featureid, thread_number, bbox, mosaic, srsname, outputdirectory, image_format, filename, yes):
    """
    Takes in a feature id and breaks the image up into 1024x1024 tiles, then places a number of calls based on
    multithreading percentages to return a full image strip in multiple tiles
    """

    streaming_interface = _streaming()
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "bbox" in line:
                if not yes:
                    bbox_check = click.prompt(
                        "A bbox has been found in the .MGP-config file. Would you like to use this "
                        "bbox?[y/n]")
                    if bbox_check.lower() == "n":
                        if bbox:
                            bbox = bbox
                        else:
                            return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                    elif bbox_check.lower() == "y":
                        bbox = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not bbox:
                    bbox = line.split("=")[1]
                elif yes and bbox:
                    bbox = bbox
            else:
                bbox = bbox
    full_resolution_image = streaming_interface.get_full_res_image(
        featureid=featureid, thread_number=thread_number, bbox=bbox, mosaic=mosaic, srsname=srsname,
        outputdirectory=outputdirectory, image_format=image_format, filename=filename
    )
    click.echo(full_resolution_image)


@click.command()
@click.option('--base_dir', '-b', help='Root directory containing image files to be mosaiced', type=str, required=True)
@click.option('--img_format', '-if', help='Image format of files', type=str, required=True)
@click.option('--img_size', '-is', help='Size of individual image files. Defaults to 1024', type=int, default=1024)
@click.option('--outputdirectory', '-o', help='Desired output directory for download. Defaults to home directory',
              type=str)
@click.option('--filename', '-fn', help='Desired filename for mosaiced image. Defaults to merged_image', type=str,
              default='merged_image')
def mosaic(base_dir, img_format, img_size, outputdirectory, filename):
    """
    Creates a mosaic of downloaded image tiles from full_res_dowload function
    """

    streaming_interface = _streaming()
    if not outputdirectory:
        outputdirectory = base_dir
    mosaiced_image = streaming_interface.create_mosaic(
        base_dir=base_dir, img_format=img_format, img_size=img_size, outputdirectory=outputdirectory, filename=filename
    )
    click.echo(mosaiced_image)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)', type=str)
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def calculate_bbox_sqkm(bbox, yes):
    """
    Calculates the area in square kilometers of the bbox
    """

    streaming_interface = _streaming()
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "bbox" in line:
                if not yes:
                    bbox_check = click.prompt(
                        "A bbox has been found in the .MGP-config file. Would you like to use this "
                        "bbox?[y/n]")
                    if bbox_check.lower() == "n":
                        if bbox:
                            bbox = bbox
                        else:
                            return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                    elif bbox_check.lower() == "y":
                        bbox = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not bbox:
                    bbox = line.split("=")[1]
                elif yes and bbox:
                    bbox = bbox
            else:
                bbox = bbox
    sqkm = streaming_interface.calculate_sqkm(bbox=bbox)
    click.echo("Square kilometers of bbox is: {}".format(sqkm))


@click.command()
@click.option('--account_id', '-ai', help='Desired account ID')
@click.option('--account_name', '-an', help='Desired account Name')
@click.option('--id_name', '-idn', is_flag=True, help='Binary for short list of accounts and names. Defaults to False',
              default=False)
@click.option('--types', '-t', is_flag=True, help='Binary for list of all account types. Defaults to False',
              default=False)
def get_accounts(account_id, account_name, id_name, types):
    """
    Lists all accounts if no parameters are passed, or lists a desired account based on parameters passed
    """

    admin_interface = _admin()
    accounts = admin_interface.account_info.get_accounts(account_id=account_id, account_name=account_name,
                                                         id_names=id_name, types=types)
    click.echo(accounts)


@click.command()
def account_roles():
    """
    Lists all account roles for the account the user is tied to
    """

    admin_interface = _admin()
    roles = admin_interface.account_info.get_roles()
    click.echo(roles)


@click.command()
@click.option('--account_id', '-ai', help='Desired account ID', required=True)
def account_comments(account_id):
    """
    Lists all comments for a desired account
    """

    admin_interface = _admin()
    comments = admin_interface.account_info.get_comment(account_id)
    click.echo(comments)


@click.command()
@click.option('--activation_id', '-ai', help='Desired activation ID. Defaults to None', default=None)
@click.option('--activation_number', '-an', help='Desired activation number. Defaults to None', default=None)
def get_activations(activation_id, activation_number):
    """
    Lists all activations if no parameters are passed, or lists a desired activation based on parameters passed
    """

    admin_interface = _admin()
    activations = admin_interface.activations.get_activations(
        activation_id=activation_id, activation_number=activation_number
    )
    click.echo(activations)


@click.command()
@click.option('--account_id', '-ai', help='Desired account ID', required=True)
def activations_for_account(account_id):
    """
    Lists all activations tied to the desired account
    """

    admin_interface = _admin()
    activations = admin_interface.activations.get_activations_for_account(account_id)
    click.echo(activations)


@click.command()
@click.option('--activation_number', '-an', help='Desired activation number', required=True)
def activation_credit_limit(activation_number):
    """
    Gets the credit limit for the desired activation
    """

    admin_interface = _admin()
    act_credit_limit = admin_interface.activations.get_activation_credit_limit(activation_number=activation_number)
    click.echo(act_credit_limit)


@click.command()
def activation_types():
    """
    Lists all activation types
    """

    admin_interface = _admin()
    act_types = admin_interface.activations.get_activation_types()
    click.echo(act_types)


@click.command()
def get_products():
    """
    Lists all products
    """

    admin_interface = _admin()
    products = admin_interface.products.get_products()
    click.echo(products)


@click.command()
@click.option('--product_category', '-pc', help='Desired product category. Defaults to None', default=None)
@click.option('--usage_type', '-ut', help='Desired usage type. Defaults to None', default=None)
@click.option('--age', '-a', help='Desired age range. Defaults to None', default=None)
@click.option('--catalog_type', '-ct', help='Desired catalog type. Defaults to None', default=None)
def product_filter(product_category, usage_type, age, catalog_type):
    """
    Lists all products based on filter parameters passed in
    """

    admin_interface = _admin()
    if not product_category and not usage_type and not age and not catalog_type:
        raise Exception('Please enter a filter option')
    prod_filter = admin_interface.products.filter_products(
        product_category=product_category, usage_type=usage_type, age=age, catalog_type=catalog_type
    )
    click.echo(prod_filter)


@click.command()
@click.option('--table_id', '-t', help='Desired rate table ID. Defaults to None', default=None)
def get_rate_table(table_id):
    """
    Lists all rate tables if no parameters are passed, or lists a desired rate table based on parameters passed
    """

    admin_interface = _admin()
    rate_tables = admin_interface.rate_table_info.get_table(table_id=table_id)
    click.echo(rate_tables)


@click.command()
@click.option('--table_id', '-t', help='Desired rate table ID', required=True)
def get_activation_for_table(table_id):
    """
    Lists all activations associated with the desired rate table
    """

    admin_interface = _admin()
    rate_table_activations = admin_interface.rate_table_info.get_activations_for_table(table_id=table_id)
    click.echo(rate_table_activations)


@click.command()
def get_credit_types():
    """
    Lists all available credit types
    """

    admin_interface = _admin()
    rate_table_credit_types = admin_interface.rate_table_info.get_credit_types()
    click.echo(rate_table_credit_types)


@click.command()
@click.option('--table_id', '-t', help='Desired rate table ID', required=True)
def get_rate_amounts(table_id):
    """
    Lists all rate amounts for the desired rate table
    """

    admin_interface = _admin()
    rate_table_product_credits = admin_interface.rate_table_info.get_rate_amounts(table_id=table_id)
    click.echo(rate_table_product_credits)


@click.command()
def get_table_and_activations():
    """
    Lists all rate tables and their products and the activations that have access to the tables
    """

    admin_interface = _admin()
    table_activations = admin_interface.rate_table_info.get_rate_tables_and_associated_activations()
    click.echo(table_activations)


@click.command()
def get_roles():
    """
    Lists all roles
    """

    admin_interface = _admin()
    roles = admin_interface.roles.get_roles()
    click.echo(roles)


@click.command()
def user_types():
    """
    Lists all available user types
    """

    admin_interface = _admin()
    user_type = admin_interface.roles.get_user_types()
    click.echo(user_type)


@click.command()
@click.option('--user_id', '-id', help='Desired user ID. Defaults to None', default=None)
@click.option('--username', '-u', help='Desired username. Defaults to None', default=None)
@click.option('--page_size', '-ps', help='Desire page size. Defaults to None', default=None)
@click.option('--page', '-p', help='Desired starting page number. Defaults to None', default=None)
def get_users(user_id, username, page_size, page):
    """
    Lists all users if no parameters are passed, or lists a desired user based on parameters passed
    """

    admin_interface = _admin()
    user_list = admin_interface.users.get_users(user_id=user_id, username=username, pageSize=page_size, page=page)
    click.echo(user_list)


@click.command()
@click.option('--user_id', '-id', help='Desired user ID', required=True)
@click.option('--username', '-u', help='Desired username. Defaults to None', default=None)
@click.option('--first_name', '-f', help='Desired first name. Defaults to None', default=None)
@click.option('--last_name', '-l', help='Desired last name. Defaults to None', default=None)
@click.option('--phone', '-p', help='Desired phone number. Defaults to None', default=None)
@click.option('--yes', '-y', help='Flag to bypass one or more update options. Defaults to False', is_flag=True,
              default=False)
def update_user(user_id, username, first_name, last_name, phone, yes):
    """
    Updates desired user based on parameters passed
    """

    admin_interface = _admin()
    if username:
        var_username = username
        update = admin_interface.users.update_user(user_id, username=var_username)
    elif not username:
        if yes:
            pass
        else:
            var_username = click.prompt("Enter new username")
            update = admin_interface.users.update_user(user_id, username=var_username)
    if first_name:
        var_first_name = first_name
        update = admin_interface.users.update_user(user_id, firstName=var_first_name)
    elif not first_name:
        if yes:
            pass
        else:
            var_first_name = click.prompt("Enter new first name")
            update = admin_interface.users.update_user(user_id, firstName=var_first_name)
    if last_name:
        var_last_name = last_name
        update = admin_interface.users.update_user(user_id, lastName=var_last_name)
    elif not last_name:
        if yes:
            pass
        else:
            var_last_name = click.prompt("Enter new last name")
            update = admin_interface.users.update_user(user_id, lastName=var_last_name)
    if phone:
        var_phone = phone
        update = admin_interface.users.update_user(user_id, phone=var_phone)
    elif not phone:
        if yes:
            pass
        else:
            var_phone = click.prompt("Enter new phone number")
            update = admin_interface.users.update_user(user_id, phone=var_phone)
    click.echo(update)


@click.command()
@click.option('--user_type', '-ut', help='Desired user type', required=True)
@click.option('--account_id', '-acc_id', help='Desired account ID', required=True)
@click.option('--activation_id', '-act_id', help='Desired activation ID', required=True)
@click.option('--email', '-e', help='Desired email Address', required=True)
@click.option('--first_name', '-f', help='Desired first name', required=True)
@click.option('--last_name', '-l', help='Desired last name', required=True)
@click.option('--country', '-c', help='Desired country of origin', required=True)
@click.option('--client_id', '-cid', help='Desired client ID. Defaults to mgp', default='mgp')
def create_user(user_type, account_id, activation_id, email, first_name, last_name, country, client_id):
    """
    Creates a new user based on parameters passed
    """

    admin_interface = _admin()
    if user_type:
        user_type = user_type
    else:
        user_type = click.prompt("Enter user type")
    if account_id:
        account_id = account_id
    else:
        account_id = click.prompt("Enter desired account ID")
    if activation_id:
        activation_id = activation_id
    else:
        activation_id = click.prompt("Enter desired activation ID")
    if email:
        email = email
    else:
        email = click.prompt("Enter email address")
    if first_name:
        first_name = first_name
    else:
        first_name = click.prompt("Enter first name")
    if last_name:
        last_name = last_name
    else:
        last_name = click.prompt("Enter last name")
    if country:
        country = country
    else:
        country = click.prompt("Enter country of origin")
    create_new_user = admin_interface.users.create_user(
        user_type=user_type, account_id=account_id, activation_id=activation_id, email_address=email,
        first_name=first_name, last_name=last_name, country=country, client_id=client_id
    )
    click.echo(create_new_user)


@click.command()
@click.option('--user_id', '-u', help='Desired user ID', required=True)
@click.option('--roles', '-r', help='Name of role(s) to add. If multiple roles, separate roles by comma', type=str,
              required=True)
@click.option('--client_id', '-c', help='Desired client ID. Defaults to mgp client ID',
              default='b4e8d573-56ee-4e79-abcd-7b161f93ea17')
@click.option('--delete', '-d', help='Flag for deleting roles. Defaults to False', is_flag=True, default=False)
def update_user_roles(user_id, roles, client_id, delete):
    """
    Adds or removes roles to the desired user based on parameters passed
    """

    admin_interface = _admin()
    if ", " in roles:
        roles_list = roles.split(", ")
    elif "," in roles:
        roles_list = roles.split(",")
    else:
        roles_list = [roles]
    update_roles = admin_interface.users.update_user_roles(
        user_id=user_id, roles_to_update=roles_list, client_id=client_id, delete=delete
    )
    click.echo(update_roles)


@click.command()
@click.option('--user_id', '-u', help='Desired user ID', required=True)
def get_user_roles(user_id):
    """
    Lists all roles tied to the desired user
    """

    admin_interface = _admin()
    user_roles = admin_interface.users.get_user_roles(user_id=user_id)
    click.echo(user_roles)


@click.command()
@click.option('--user_id', '-u', help='Desired user ID', required=True)
@click.option('--client_id', '-c', help='Desired client ID. Defaults to mgp client ID',
              default="b4e8d573-56ee-4e79-abcd-7b161f93ea17")
def get_user_available_roles(user_id, client_id):
    """
    Lists all roles that can be tied to the desired user
    """

    admin_interface = _admin()
    user_available_roles = admin_interface.users.get_user_available_roles(user_id=user_id, client_id=client_id)
    click.echo(user_available_roles)


@click.command()
@click.option('--user_id', '-u', help='Desired user ID', required=True)
@click.option(
    '--yes', '-y', help='Flag to bypass deletion confirmation. Defaults to False', is_flag=True, default=False
)
def delete_user(user_id, yes):
    """
    Deletes a user
    """

    admin_interface = _admin()
    if not yes:
        check = click.prompt("Are you sure you wish to delete this user? [y/n]")
        if check.lower() == "n":
            return click.echo("Deletion aborted")
        elif check.lower() == "y":
            pass
        else:
            return click.echo("Invalid input. Please run command again and enter y or n")
    delete = admin_interface.users.delete_user(user_id=user_id)
    click.echo(delete)


@click.command()
@click.option('--page', '-p', help='Desired starting page. Defaults to 0 (first page)', type=int, default=0)
@click.option('--page_size', '-ps', help='Desired number of returned objects. Defaults to 10', type=int, default=10)
@click.option('--sort', '-s', help='Desired variable to sort by. Defaults to id', type=str, default='id')
def account_usage(page, page_size, sort):
    """
    \b
    Lists one or more account's usage. Sort options are:
    id, accountNumber, sapLicenseId, licensee, soldTo, totalCreditsUsed, numberOfActivations, numberOfUsers
    """
    admin_interface = _admin()
    acc_usage = admin_interface.usage.get_account_usage(page=page, pageSize=page_size, sortBy=sort)
    click.echo(acc_usage)


@click.command()
@click.option('--page', '-p', help='Desired starting page. Defaults to 0 (first page)', type=int, default=0)
@click.option('--page_size', '-ps', help='Desired number of returned objects. Defaults to 10', type=int, default=10)
@click.option('--sort', '-s', help='Desired variable to sort by. Defaults to id', type=str, default='id')
@click.option('--client_id', '-c', help='Desired client ID', type=str, default='b4e8d573-56ee-4e79-abcd-7b161f93ea17')
def activation_usage(page, page_size, sort, client_id):
    """
    \b
    Lists one or more activation's usage. Sort options are:
    id, activationNumber, sapContractIdentifier, sapLineItem, startDate, endDate, creditLimit, totalCreditsUsed,
    creditsUsedPercentage, numberOfUsers, totalUsers, accountTotalUsers, accountName, accountNumber,
    accountSapLicenseId, accountLicensee, accountSoldTo, userLimit, dailyCreditLimitTotal, dailyCreditLimitUsed,
    clientContextId
    """
    admin_interface = _admin()
    act_usage = admin_interface.usage.get_activation_usage(
        page=page, pageSize=page_size, sortBy=sort, clientContextId=client_id
    )
    click.echo(act_usage)


@click.command()
@click.option('--page', '-p', help='Desired starting page. Defaults to 0 (first page)', type=int, default=0)
@click.option('--page_size', '-ps', help='Desired number of returned objects. Defaults to 10', type=int, default=10)
@click.option('--sort', '-s', help='Desired variable to sort by. Defaults to id', type=str, default='id')
@click.option('--client_id', '-c', help='Desired client ID', type=str, default='b4e8d573-56ee-4e79-abcd-7b161f93ea17')
def user_usage(page, page_size, sort, client_id):
    """
    \b
    Lists one or more user's usage. Sort options are:
    id, username, accountId, activationNumber, accountNumber, accountSapLicenseId, accountLicensee, accountSoldTo,
    totalCreditsUsed, dailyCreditLimitTotal, dailyCreditLimitUsed, userType, clientContextId
    """
    admin_interface = _admin()
    us_usage = admin_interface.usage.get_user_usage(
        page=page, pageSize=page_size, sortBy=sort, clientContextId=client_id
    )
    click.echo(us_usage)


@click.command()
def usage_is_allowed():
    """
    Checks if usage credit limit has been reached
    """
    usage_interface = _usage()
    allowed = usage_interface.check_usage_is_allowed()
    click.echo(allowed)


@click.command()
def usage_overview():
    """
    Shows the overview of usage used for the account the user is tied to
    """
    usage_interface = _usage()
    overview = usage_interface.get_usage_overview()
    click.echo(overview)


@click.command()
@click.option('--collections', '-c',
              help='Comma-separated list of collections to search in. Use str format not a Python list', default=None)
@click.option('--sub_catalog_id', '-scid', help='Name of the subCatalogId to search in', default=None)
@click.option(
    '--sub_catalog_collection', '-scc', help='Used to denote collections inside of sub catalogs', default=None
)
@click.option(
    '--bbox', '-b', help='Bounding box in format "west,south,east,north" in WGS84 decimal degrees', default=None
)
@click.option('--datetime', '-d', help='Date range filter in ISO 8601 format "start-date/end-date" or exact datetime',
              default=None)
@click.option('--stac_id', '-sid',
              help='Comma-separated list of STAC item IDs to return. Use str format not a Python list', default=None)
@click.option('--intersects', '-i', help='GeoJSON geometry to search by', default=None)
@click.option('--where', '-w', help='SQL-style WHERE clause for filtering STAC items by properties', default=None)
@click.option('--orderby', '-oby', help='SQL-style ORDER BY clause. Only for id and datetime')
@click.option('--limit', '-l', help='Maximum number of items to return. Defaults to 10', default=10)
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def stac_search(collections, sub_catalog_id, sub_catalog_collection, bbox, datetime, stac_id, intersects, where,
                orderby, limit, yes):
    """
    Returns a list of STAC items
    """

    discovery_interface = _discovery()
    aoi_dict = {"bbox": locals()['bbox'], "intersects": locals()['intersects']}
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "bbox" in line:
                if not yes:
                    bbox_check = click.prompt(
                        "A bbox has been found in the .MGP-config file. Would you like to use this "
                        "bbox?[y/n]")
                    if bbox_check.lower() == "n":
                        if bbox:
                            bbox = bbox
                        else:
                            return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                    elif bbox_check.lower() == "y":
                        bbox = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not bbox:
                    bbox = line.split("=")[1]
                elif yes and bbox:
                    bbox = bbox
            else:
                bbox = bbox
        for line in lines:
            if "geojson" in line:
                if not yes:
                    geojson_check = click.prompt(
                        "A geojson has been found in the .MGP-config file. Would you like to use this geojson?[y/n]"
                    )
                    if geojson_check.lower() == "n":
                        if intersects:
                            intersects = intersects
                        else:
                            intersects = None
                    elif geojson_check.lower() == "y":
                        intersects = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not intersects:
                    intersects = line.split("=")[1]
                elif yes and intersects:
                    # intersects = line[8:].strip()
                    intersects = intersects
            else:
                intersects = intersects
    if aoi_dict['bbox'] != None:
        intersects = None
    if aoi_dict['intersects'] != None:
        bbox = None
    params = {"collections": collections, "sub_catalog_id": sub_catalog_id,
              "sub_catalog_collection": sub_catalog_collection, "bbox": bbox, "datetime": datetime, "stac_id": stac_id,
              "intersects": intersects, "where": where, "orderby": orderby, "limit": limit}
    not_none_params = {k: v for k, v in params.items() if v is not None}
    stac = discovery_interface.stac_search(**not_none_params)
    click.echo(stac)


@click.command()
@click.option('--collection_id', '-cid', help='Identifier of the desired collection', required=True)
@click.option('--audit_insert_date', '-aid',
              help='Desired insert date in ISO-8601 format. Mutually exclusive with auditUpdateDate. Defaults to None',
              default=None)
@click.option('--audit_update_date', '-aud',
              help='Desired update date in ISO-8601 format. Mutually exclusive with auditInsertDate. Defaults to None',
              default=None)
@click.option('--limit', '-l', help='Maximum number of items to return. Defaults to 10', default=10)
def search_audit_fields(collection_id, audit_insert_date, audit_update_date, limit):
    """
    Retrieve items for a given collectionId by audit fields
    """

    discovery_interface = _discovery()
    if audit_update_date and audit_insert_date:
        raise Exception("audit insert date and audit update date are mutually exclusive from each other")
    audit = discovery_interface.search_by_audit_fields(
        collection_id=collection_id, audit_insert_date=audit_insert_date, audit_update_date=audit_update_date,
        limit=limit
    )
    click.echo(audit)


@click.command()
def root_catalog():
    """
    Returns the root STAC Catalog or STAC Collection that is the entry point for users to browse
    """

    discovery_interface = _discovery()
    root = discovery_interface.get_root_catalog()
    click.echo(root)


@click.command()
@click.option('--collection_id', '-c', help='Identifier of the desired collection', required=True)
def collection_definition(collection_id):
    """
    Return a collection definition by collection ID
    """

    discovery_interface = _discovery()
    definition = discovery_interface.get_collection_definition(collection_id=collection_id)
    click.echo(definition)


@click.command()
@click.option('--orderby', '-o', help="SQL-style ORDER BY clause. Only for id and datetime e.g. 'orderby=id ASC'. "
                                      "Defaults to 'datetime DESC, id ASC'", default='datetime DESC, id ASC')
@click.option('--limit', '-l', help='Maximum number of items to return. Defaults to 10', default=10)
def all_collections(orderby, limit):
    """
    Return definitions for all collections
    """

    discovery_interface = _discovery()
    collects = discovery_interface.get_all_collections(orderby=orderby, limit=limit)
    click.echo(collects)


@click.command()
@click.option('--collection_id', '-c', help='Identifier of the desired collection', required=True)
@click.option('--item_id', '-i', help='Identifier of the desired item', required=True)
def get_stac_item(collection_id, item_id):
    """
    View details about a specific STAC item
    """

    discovery_interface = _discovery()
    stac = discovery_interface.get_stac_item(collection_id=collection_id, item_id=item_id)
    click.echo(stac)


@click.command()
@click.option('--orderby', '-o', help="SQL-style ORDER BY clause. Only for id and datetime e.g. 'id asc'. "
                                      "Defaults to 'id asc'", default='id asc')
@click.option('--limit', '-l', help='Maximum number of items to return. Defaults to 10', default=10)
def top_level_sub_catalog(orderby, limit):
    """
    View the available Maxar Sub-Catalogs that can be navigated as a self-contained STAC catalog
    """

    discovery_interface = _discovery()
    top_level = discovery_interface.get_top_level_sub_catalog(orderby=orderby, limit=limit)
    click.echo(top_level)


@click.command()
@click.option('--sub_catalog_id', '-s', help='Identifier of the sub catalog to view', required=True)
def sub_catalog_definition(sub_catalog_id):
    """
    View the definition of a Maxar Sub-Catalog
    """

    discovery_interface = _discovery()
    sub_def = discovery_interface.get_sub_catalog(sub_catalog_id=sub_catalog_id)
    click.echo(sub_def)


@click.command()
@click.option('--sub_catalog_id', '-s', help='Identifier of the sub catalog to view', required=True)
@click.option('--orderby', '-o', help="SQL-style ORDER BY clause. Only for id and datetime e.g. 'id asc'. "
                                      "Defaults to 'id asc'", default='id asc')
@click.option('--limit', '-l', help='Maximum number of items to return. Defaults to 10', default=10)
def all_sub_catalog_definitions(sub_catalog_id, orderby, limit):
    """
    List the collections that belong to a Sub-Catalog
    """

    discovery_interface = _discovery()
    all_sub_defs = discovery_interface.get_all_sub_catalog_collections(sub_catalog_id=sub_catalog_id, orderby=orderby,
                                                                       limit=limit)
    click.echo(all_sub_defs)


@click.command()
@click.option('--sub_catalog_id', '-s', help='Identifier of the sub catalog to view', required=True)
@click.option('--sub_catalog_collection_id', '-sc', help='Identifier of the sub catalog collection to view',
              required=True)
def sub_catalog_collection_definition(sub_catalog_id, sub_catalog_collection_id):
    """
    View the definition of a collection that belongs to a Sub-Catalog
    """

    discovery_interface = _discovery()
    sub_def = discovery_interface.get_sub_catalog_collection_definition(
        sub_catalog_id=sub_catalog_id, sub_catalog_collection_id=sub_catalog_collection_id
    )
    click.echo(sub_def)


@click.command()
def all_pipelines():
    """
    List all pipelines and their information
    """

    ordering_interface = _ordering()
    pipelines = ordering_interface.get_all_pipelines()
    click.echo(pipelines)


@click.command()
@click.option('--namespace', '-ns', help='Desired pipeline namespace', required=True)
@click.option('--name', '-n', help='Desired pipeline name', required=True)
def get_pipeline(namespace, name):
    """
    List the information for a desired pipeline
    """

    ordering_interface = _ordering()
    pipeline = ordering_interface.get_pipeline_details(namespace=namespace, name=name)
    click.echo(pipeline)


@click.command()
@click.option('--namespace', '-ns', help='Desired pipeline namespace', required=True)
@click.option('--name', '-n', help='Desired pipeline name', required=True)
@click.option('--settings', '-s', help='Ordering settings including inventory ids and customer description')
@click.option('--aoi', '-a', help='GeoJSON of AOI')
@click.option('--output_config', '-o', help='Output configuration template')
@click.option('--notifications', '-nt', help='Notifications template')
@click.option('--metadata', '-m', help='Project metadata', required=True)
@click.option('--validate', '-v', help='Flag to validate order. Defaults to False', is_flag=True, default=False)
@click.option('--estimate', '-e', help='Flag to estimate order usage. Defaults to False', is_flag=True, default=False)
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def order(namespace, name, settings, aoi, output_config, notifications, metadata, validate, estimate, yes):
    """
    Validate, estimate, or submit an order
    """

    ordering_interface = _ordering()
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "geojson" in line:
                if not yes:
                    geojson_check = click.prompt(
                        "A geojson has been found in the .MGP-config file. Would you like to use this geojson?[y/n]"
                    )
                    if geojson_check.lower() == "n":
                        if aoi:
                            aoi = aoi
                        else:
                            aoi = None
                    elif geojson_check.lower() == "y":
                        aoi = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not aoi:
                    aoi = line.split("=")[1]
                elif yes and aoi:
                    aoi = aoi
            else:
                aoi = aoi
            if "order_settings" in line:
                if not yes:
                    settings_check = click.prompt(
                        "An order settings template has been found in the .MGP-config file. Would you like to use this "
                        "template?[y/n]"
                    )
                    if settings_check.lower() == "n":
                        if settings:
                            settings = settings
                        else:
                            settings = None
                    elif settings_check.lower() == "y":
                        settings = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not settings:
                    settings = line.split("=")[1]
                elif yes and settings:
                    settings = settings
            else:
                settings = settings
            if "output_settings" in line:
                if not yes:
                    output_config_check = click.prompt(
                        "An output config template has been found in the .MGP-config file. Would you like to use this "
                        "template?[y/n]"
                    )
                    if output_config_check.lower() == "n":
                        if output_config:
                            output_config = output_config
                        else:
                            output_config = None
                    elif output_config_check.lower() == "y":
                        output_config = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not output_config:
                    output_config = line.split("=")[1]
                elif yes and output_config:
                    output_config = output_config
            else:
                output_config = output_config
            if "notifications_settings" in line:
                if not yes:
                    notifications_check = click.prompt(
                        "A notifications template has been found in the .MGP-config file. Would you like to use this "
                        "template?[y/n]"
                    )
                    if notifications_check.lower() == "n":
                        if notifications:
                            notifications = notifications
                        else:
                            notifications = None
                    elif notifications_check.lower() == "y":
                        notifications = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not notifications:
                    notifications = line.split("=")[1]
                elif yes and notifications:
                    notifications = notifications
            else:
                notifications = notifications
    if aoi:
        dict_settings = json.loads(settings)
        dict_settings['settings'].update({"aoi": json.loads(aoi)})
    else:
        dict_settings = json.loads(settings)
    meta = {
        "metadata": {
            "project_id": metadata
        }
    }
    config = json.loads(output_config)
    notifications_dict = json.loads(notifications)
    if estimate:
        order_request = ordering_interface.place_order(
            namespace=namespace, name=name, settings=dict_settings, output_config=config, metadata=meta,
            notifications=notifications_dict)
    else:
        order_request = ordering_interface.place_order(
            namespace=namespace, name=name, settings=dict_settings, output_config=config, metadata=meta,
            notifications=notifications_dict, validate=validate)
    click.echo(order_request)


@click.command()
@click.option('--order_id', '-o', help='Desired order ID', required=True)
def order_details(order_id):
    """
    List the details for an order
    """

    ordering_interface = _ordering()
    details = ordering_interface.get_order_details(order_id=order_id)
    click.echo(details)


@click.command()
@click.option('--order_id', '-o', help='Desired order ID', required=True)
@click.option('--limit', '-l', help='Maximum number of items to return', type=int)
@click.option('--starting_after', '-sa', help='Token (base-64-encoded-key) after which further responses will be '
                                              'returned, paging forward.', default=None)
@click.option('--ending_before', '-eb', help='Token (base-64-encoded key) after which further responses will be '
                                             'returned, paging backward.', default=None)
@click.option('--filter', '-f', help=' Filter results that match values contained in the given key separated by a '
                                     'colon.', default=None)
def order_events(order_id, limit, starting_after, ending_before, filter):
    """
    List the order events for an order
    """

    ordering_interface = _ordering()
    params = {"order_id": order_id, "limit": limit, "starting_after": starting_after, "ending_before": ending_before,
              "filter": filter}
    not_none_params = {k: v for k, v in params.items() if v is not None}
    events = ordering_interface.get_order_events(**not_none_params)
    click.echo(events)


@click.command()
@click.option('--user_id', '-u', help='Desired user ID. Do not pass option if orders for self are desired')
def list_users_orders(user_id):
    """
    List the orders for a user or for your own user if no flag is passed
    """

    ordering_interface = _ordering()
    if user_id:
        user_orders = ordering_interface.get_user_orders(user_id=user_id)
        click.echo(user_orders)
    else:
        user_orders = ordering_interface.get_user_orders()
        click.echo(user_orders)


@click.command()
@click.option('--order_id', '-o', help='Desired order ID', required=True)
def cancel_order(order_id):
    """
    Cancel an order
    """

    ordering_interface = _ordering()
    cancel = ordering_interface.cancel_order(order_id=order_id)
    click.echo(cancel)


@click.command()
@click.option('--pipeline', '-p', help='Desired pipeline namespace and name separated by a forward slash',
              required=True)
@click.option('--recipe', '-r', help='Desired image recipe', required=True)
@click.option('--start_datetime', '-sd', help='ISO-8601 formatted date when the tasking should start', required=True)
@click.option('--end_datetime', '-ed', help='ISO-8601 formatted date when the tasking should end', required=True)
@click.option('--settings', '-s', help='Tasking settings including inventory ids placeholder list and customer '
                                       'description')
@click.option('--aoi', '-a', help='GeoJSON of AOI')
@click.option('--output_config', '-o', help='Output configuration template')
@click.option('--notifications', '-n', help='Notifications template')
@click.option('--metadata', '-m', help='Project metadata', required=True)
@click.option('--validate', '-v', help='Flag to validate tasking request. Defaults to False', is_flag=True,
              default=False)
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def submit_tasking(pipeline, recipe, start_datetime, end_datetime, settings, aoi, output_config, notifications,
                   metadata, validate, yes):
    """
    Submits or validates a tasking request
    """

    tasking_interface = _tasking()
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "geojson" in line:
                if not yes:
                    geojson_check = click.prompt(
                        "A geojson has been found in the .MGP-config file. Would you like to use this geojson?[y/n]"
                    )
                    if geojson_check.lower() == "n":
                        if aoi:
                            aoi = aoi
                        else:
                            aoi = None
                    elif geojson_check.lower() == "y":
                        aoi = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not aoi:
                    aoi = line.split("=")[1]
                elif yes and aoi:
                    aoi = aoi
            else:
                aoi = aoi
            if "tasking_template" in line:
                if not yes:
                    tasking_template_check = click.prompt(
                        "A tasking template has been found in the .MGP-config file. Would you like to use this "
                        "template?[y/n]"
                    )
                    if tasking_template_check.lower() == "n":
                        if settings:
                            settings = settings
                        else:
                            settings = None
                    elif tasking_template_check.lower() == "y":
                        settings = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not settings:
                    settings = line.split("=")[1]
                elif yes and settings:
                    settings = settings
            else:
                settings = settings
            if "output_settings" in line:
                if not yes:
                    output_config_check = click.prompt(
                        "An output config template has been found in the .MGP-config file. Would you like to use this "
                        "template?[y/n]"
                    )
                    if output_config_check.lower() == "n":
                        if output_config:
                            output_config = output_config
                        else:
                            output_config = None
                    elif output_config_check.lower() == "y":
                        output_config = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not output_config:
                    output_config = line.split("=")[1]
                elif yes and output_config:
                    output_config = output_config
            else:
                output_config = output_config
            if "notifications_settings" in line:
                if not yes:
                    notifications_check = click.prompt(
                        "A notifications template has been found in the .MGP-config file. Would you like to use this "
                        "template?[y/n]"
                    )
                    if notifications_check.lower() == "n":
                        if notifications:
                            notifications = notifications
                        else:
                            notifications = None
                    elif notifications_check.lower() == "y":
                        notifications = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not notifications:
                    notifications = line.split("=")[1]
                elif yes and notifications:
                    notifications = notifications
            else:
                notifications = notifications
    tasking_data = [{
        "pipeline": pipeline,
        "template": json.loads(settings)
    }]
    for i in tasking_data:
        i['template'].update(json.loads(output_config))
        i['template'].update({"notifications": json.loads(notifications)})
        i['template'].update({"metadata": {"project_id": metadata}})
    if validate:
        validate = True
    else:
        validate = False
    tasking = tasking_interface.new_tasking(
        start_datetime=start_datetime, end_datetime=end_datetime, aoi_geojson=json.loads(aoi), recipe=recipe,
        order_templates=tasking_data, validate=validate
    )
    click.echo(tasking)


@click.command()
@click.option('--tasking_id', '-t', help='Desired tasking ID', required=True)
def get_tasking_request(tasking_id):
    """
    Get a desired tasking request's information
    """

    tasking_interface = _tasking()
    tasking = tasking_interface.get_tasking_request(tasking_id=tasking_id)
    click.echo(tasking)


@click.command()
@click.option('--tasking_id', '-t', help='Desired tasking ID', required=True)
@click.option('--reason', '-r', help='Reason for tasking cancellation', required=True)
def cancel_tasking(tasking_id, reason):
    """
    Cancels a desired tasking request
    """

    tasking_interface = _tasking()
    cancel = tasking_interface.cancel_tasking(tasking_id=tasking_id, reason=reason)
    click.echo(cancel)


@click.command()
@click.option('--start_datetime', '-sd', help='ISO-8601 formatted date when the monitoring should start', required=True)
@click.option('--end_datetime', '-ed', help='ISO-8601 formatted date when the monitoring should end', required=True)
@click.option('--description', '-d', help='Description of the monitor being created', required=True)
@click.option('--aoi', '-a', help='GeoJSON of AOI')
@click.option('--match_criteria', '-m', help='Dictionary of desired matching criteria')
@click.option('--notifications', '-n', help='Monitor notifications template')
@click.option('--order_templates', '-o', help='Flag to dictate whether or not to auto-order when monitor is triggered. '
                                              'Defaults to False', is_flag=True, default=False)
@click.option('--pipeline', '-p', help='Desired ordering pipeline')
@click.option('--validate', '-v', help='Flag to validate monitor request. Defaults to False', is_flag=True,
              default=False)
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def create_monitor(start_datetime, end_datetime, description, aoi, match_criteria, notifications, order_templates,
                   pipeline, validate, yes):
    """
    Validate or create a monitor
    """

    monitoring_interface = _monitoring()
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "geojson" in line:
                if not yes:
                    geojson_check = click.prompt(
                        "A geojson has been found in the .MGP-config file. Would you like to use this geojson?[y/n]"
                    )
                    if geojson_check.lower() == "n":
                        if aoi:
                            aoi = aoi
                        else:
                            aoi = None
                    elif geojson_check.lower() == "y":
                        aoi = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not aoi:
                    aoi = line.split("=")[1]
                elif yes and aoi:
                    aoi = aoi
            else:
                aoi = aoi
            if "monitor_notifications" in line:
                if not yes:
                    notifications_check = click.prompt(
                        "A notifications template has been found in the .MGP-config file. Would you like to use this "
                        "template?[y/n]"
                    )
                    if notifications_check.lower() == "n":
                        if notifications:
                            notifications = notifications
                        else:
                            notifications = None
                    elif notifications_check.lower() == "y":
                        notifications = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not notifications:
                    notifications = line.split("=")[1]
                elif yes and notifications:
                    notifications = notifications
            else:
                notifications = notifications
            if "match_criteria" in line:
                if not yes:
                    criteria_check = click.prompt(
                        "A match criteria has been found in the .MGP-config file. Would you like to use this "
                        "template?[y/n]"
                    )
                    if criteria_check.lower() == "n":
                        if match_criteria:
                            match_criteria = match_criteria
                        else:
                            match_criteria = None
                    elif criteria_check.lower() == "y":
                        match_criteria = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not match_criteria:
                    match_criteria = line.split("=")[1]
                elif yes and match_criteria:
                    match_criteria = match_criteria
            else:
                match_criteria = match_criteria
    if order_templates:
        order_template_list = [{}]
        if not pipeline:
            pipeline = click.prompt("Please enter desired pipeline and namespace separated by a forward slash")
        else:
            pipeline = pipeline
        for order_dict in order_template_list:
            order_dict.update({"pipeline": pipeline})
        with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
            lines = f.readlines()
            config_array = [i.strip("\n") for i in lines if "[mgp]" not in i]
            config_dict = {}
            for item in config_array:
                key, value = item.split("=")
                config_dict[key] = value
            if "order_settings" in config_dict.keys():
                if not yes:
                    settings_check = click.prompt(
                        "An order settings template has been found in the .MGP-config file. Would you like to use this "
                        "template?[y/n]"
                    )
                    if settings_check.lower() == "n":
                        settings = click.prompt("Enter monitor order settings")
                        try:
                            settings_validation = json.loads(settings)
                            if "settings" not in settings_validation.keys():
                                raise Exception("Settings parameter not found")
                        except:
                            raise Exception("Improperly formatted settings dictionary")
                        for order_template in order_template_list:
                            order_template.update({"template": settings_validation})
                    elif settings_check.lower() == "y":
                        settings = json.loads(config_dict['order_settings'])
                        for order_template in order_template_list:
                            order_template.update({"template": settings})
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes:
                    settings = json.loads(config_dict['order_settings'])
                    for order_template in order_template_list:
                        order_template.update({"template": settings})
            if "output_settings" in config_dict.keys():
                if not yes:
                    output_config_check = click.prompt(
                        "An output config template has been found in the .MGP-config file. Would you like to use this "
                        "template?[y/n]"
                    )
                    if output_config_check.lower() == "n":
                        output_config = click.prompt("Enter output config")
                        try:
                            output_config_validation = json.loads(output_config)
                            if "output_config" not in output_config_validation:
                                raise Exception("output_config parameter not found")
                        except:
                            raise Exception("Improperly formatted output config dictionary")
                        for output_template in order_template_list:
                            output_template['template'].update(output_config_validation)
                    elif output_config_check.lower() == "y":
                        output_config = json.loads(config_dict['output_settings'])
                        for output_template in order_template_list:
                            output_template['template'].update(output_config)
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes:
                    output_config = json.loads(config_dict['output_settings'])
                    for output_template in order_template_list:
                        output_template['template'].update(output_config)
        monitoring = monitoring_interface.new_monitor(
            source='discovery/catalog', start_datetime=start_datetime, end_datetime=end_datetime,
            description=description, aoi_geojson=json.loads(aoi), match_criteria=json.loads(match_criteria),
            monitor_notifications=json.loads(notifications), order_templates=order_template_list, validate=validate
        )
    else:
        monitoring = monitoring_interface.new_monitor(
            source='discovery/catalog', start_datetime=start_datetime, end_datetime=end_datetime,
            description=description, aoi_geojson=json.loads(aoi), match_criteria=json.loads(match_criteria),
            monitor_notifications=json.loads(notifications), validate=validate
        )
    click.echo(monitoring)


@click.command()
@click.option('--monitor_id', '-id', help='Desired monitor id')
@click.option('--limit', '-l', help='Amount of monitors to return. Defaults to 10', default=10)
@click.option('--filter', '-f', help='Desired filter for returning monitors. Defaults to None', default=None)
@click.option('--sort', '-s', help='Desired sorting option. Defaults to None', default=None)
def get_monitor(monitor_id, limit, filter, sort):
    """
    List one or more monitor's information
    """

    monitoring_interface = _monitoring()
    if monitor_id:
        monitor = monitoring_interface.get_monitor(monitor_id=monitor_id)
    else:
        params = {"limit": limit, "filter": filter, "sort": sort}
        not_none_params = {k: v for k, v in params.items() if v is not None}
        monitor = monitoring_interface.get_monitor_list(**not_none_params)
    click.echo(monitor)


@click.command()
@click.option('--monitor_id', '-id', help='Desired monitor id', required=True)
@click.option('--limit', '-l', help='Amount of monitors to return. Defaults to 10', default=10)
@click.option('--filter', '-f', help='Desired filter for returning monitors. Defaults to None', default=None)
@click.option('--sort', '-s', help='Desired sorting option. Defaults to None', default=None)
def monitor_events(monitor_id, limit, filter, sort):
    """
    List the events for a monitor
    """

    monitoring_interface = _monitoring()
    params = {"limit": limit, "filter": filter, "sort": sort}
    not_none_params = {k: v for k, v in params.items() if v is not None}
    events = monitoring_interface.get_monitor_events(monitor_id=monitor_id, **not_none_params)
    click.echo(events)


@click.command()
@click.option('--monitor_id', '-id', help='Desired monitor id', required=True)
@click.option('--enable', '-e', help='Flag to enable a monitor. Defaults to False', is_flag=True, default=False)
@click.option('--disable', '-d', help='Flag to disable a monitor. Defaults to False', is_flag=True, default=False)
def toggle_monitor(monitor_id, enable, disable):
    """
    Toggle the status of a monitor between enabled/disabled
    """

    monitoring_interface = _monitoring()
    if enable and disable:
        raise Exception("Either enable or disable must be called, not both")
    elif enable:
        toggle = monitoring_interface.toggle_monitor_status(monitor_id=monitor_id, status='enable')
    elif disable:
        toggle = monitoring_interface.toggle_monitor_status(monitor_id=monitor_id, status='disable')
    else:
        raise Exception("Either enable or disable must be called, not both or neither")
    click.echo(toggle)


@click.command()
@click.option('--script_id', '-s', help='Desired raster script name', required=True)
@click.option('--function', '-f', help='Desired raster function', required=True)
@click.option('--collect_id', '-cid', help='Desired collect ID for the raster object', required=True)
@click.option('--api_token', '-a', help='Your maxar API token', required=True)
@click.option('--crs', '-c', help='Desired projection for the raster object. Defaults to UTM', default='UTM')
@click.option('--bands', '-b', help='Comma separated string of desired bands for the raster object. Defaults to None',
              default=None)
@click.option('--dra', '-d', help='Binary of whether or not to apply dra to the raster. String of bool (true, false). '
                                  'Defaults to None', default=None)
@click.option('--interpolation', '-i', help='Desired resizing or (re)projection from one pixel grid to another. '
                                            'Defaults to None', default=None)
@click.option('--acomp', '-ac', help='Binary of whether or not to apply atmospheric compensation to the output after'
                                     'hd (if applied) and before dra. String of bool (true, false). Defaults to None',
              default=None)
@click.option('--hd', '-h', help='Binary of whether or not to apply higher resolution to the output. String of bool ('
                                 'true, false). Defaults to None', default=None)
def raster_url(script_id, function, collect_id, api_token, crs, bands, dra, interpolation, acomp, hd):
    """
    Return a vsicurl formatted raster URL
    """

    analytics_interface = _analytics()
    params = {"script_id": script_id, "function": function, "collect_id": collect_id, "api_token": api_token,
              "crs": crs, "bands": bands, "dra": dra, "interpolation": interpolation, "acomp": acomp, "hd": hd}
    not_none_params = {k: v for k, v in params.items() if v is not None}
    create_url = analytics_interface.raster_url(**not_none_params)
    click.echo(create_url)


@click.command()
@click.option('--raster_url', '-r', help='vsicurl formatted URL of a raster object', required=True)
def get_raster_metadata(raster_url):
    """
    Obtain metadata information for a rasterized object
    """
    analytics_interface = _analytics()
    metadata = analytics_interface.raster_metadata(raster_url)
    click.echo(metadata)


@click.command()
@click.option('--raster_url', '-r', help='vsicurl formatted URL of a raster object', required=True)
@click.option('--x_off', '-x', help='Number of pixels to offset on the x axis', type=int, required=True)
@click.option('--y_off', '-y', help='Number of pixels to offset on the y axis', type=int, required=True)
@click.option('--width', '-w', help='Number of pixels for the returned raster on the x axis', type=int, required=True)
@click.option('--height', '-h', help='Number of pixels for the returned raster on the y axis', type=int, required=True)
@click.option('--download', '-d', help='Flag dictating the download of a raster object. Defaults to False',
              is_flag=True, default=False)
@click.option('--outputpath', '-o', help='Desired output path location for the rasterized object including filename '
                                         'and extension')
def get_raster_array(raster_url, x_off, y_off, width, height, download, outputpath):
    """
    Create a raster array from a rasterized (vsicurl) URL and download the raster locally if specified
    """

    analytics_interface = _analytics()
    ras_array = analytics_interface.get_arrays(
        raster_url=raster_url, xoff=x_off, yoff=y_off, width=width, height=height
    )
    if not download:
        click.echo(ras_array)
    else:
        ras_download = analytics_interface.download_raster(raster_array=ras_array, outputpath=outputpath)
        click.echo(ras_download)


@click.command()
@click.option('--layers', '-l', help='Desired vector layer', required=True)
@click.option('--bbox', '-b', help='Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)')
@click.option('--srsname', '-srs', help='Desired projection NOTE:(WFS for vector data currently only supports '
                                        'EPSG:3857). Defaults to EPSG:3857', default='EPSG:3857')
@click.option('--filter', '-f', help='CQL filter used to refine data of search. Defaults to None', default=None)
@click.option('--shapefile', '-s', help='Binary of whether to return as shapefile format. Defaults to False',
              is_flag=True, default=False)
@click.option('--csv', '-c', help='Binary of whether to return as a csv format, Defaults to False', is_flag=True,
              default=False)
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def vector_search(layers, bbox, srsname, filter, shapefile, csv, yes):
    """
    Search vector layers
    """

    analytics_interface = _analytics()
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "bbox" in line:
                if not yes:
                    bbox_check = click.prompt(
                        "A bbox has been found in the .MGP-config file. Would you like to use this "
                        "bbox?[y/n]")
                    if bbox_check.lower() == "n":
                        if bbox:
                            bbox = bbox
                        else:
                            return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                    elif bbox_check.lower() == "y":
                        bbox = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not bbox:
                    bbox = line.split("=")[1]
                elif yes and bbox:
                    bbox = bbox
            else:
                bbox = bbox
    if filter:
        vec_search = analytics_interface.search_vector_layer(
            layers=layers, bbox=bbox, srsname=srsname, filter=filter, shapefile=shapefile, csv=csv
        )
    else:
        vec_search = analytics_interface.search_vector_layer(
            layers=layers, bbox=bbox, srsname=srsname, shapefile=shapefile, csv=csv
        )
    click.echo(vec_search)


@click.command()
@click.option('--layers', '-l', help='Desired vector layer', required=True)
@click.option('--bbox', '-b', help='Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)')
@click.option('--srsname', '-srs', help='Desired projection. Defaults to EPSG:4326', default='EPSG:4326')
@click.option('--height', '-h', help='The vertical number of pixels to return. Defaults to 512', default=512)
@click.option('--width', '-w', help='The horizontal number of pixels to return. Defaults to 512', default=512)
@click.option('--img_format', '-i', help='The format of the response image either jpeg, png or geotiff. Defaults to '
                                         'jpeg', default='jpeg')
@click.option('--outputpath', '-o', help='Output path must include output format. Downloaded path default is '
                                         'user home path', default=None)
@click.option('--filter', '-f', help='CQL filter used to refine data of search. Defaults to None', default=None)
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def vector_image_download(layers, bbox, srsname, height, width, img_format, outputpath, filter, yes):
    """
     Download a vector image
    """

    analytics_interface = _analytics()
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "bbox" in line:
                if not yes:
                    bbox_check = click.prompt(
                        "A bbox has been found in the .MGP-config file. Would you like to use this "
                        "bbox?[y/n]")
                    if bbox_check.lower() == "n":
                        if bbox:
                            bbox = bbox
                        else:
                            return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                    elif bbox_check.lower() == "y":
                        bbox = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not bbox:
                    bbox = line.split("=")[1]
                elif yes and bbox:
                    bbox = bbox
            else:
                bbox = bbox
    if filter:
        vec_download = analytics_interface.download_vector_analytics(
            layers=layers, bbox=bbox, srsname=srsname, height=height, width=width, format=img_format,
            outputpath=outputpath, filter=filter
        )
    else:
        vec_download = analytics_interface.download_vector_analytics(
            layers=layers, bbox=bbox, srsname=srsname, height=height, width=width, format=img_format,
            outputpath=outputpath
        )
    click.echo(vec_download)


@click.command()
@click.option('--layers', '-l', help='Desired vector layer', required=True)
@click.option('--zoom', '-z', help='Desired zoom level between 1 and 20', type=int, required=True)
@click.option('--bbox', '-b', help='Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)')
@click.option('--srsname', '-srs', help='Desired projection NOTE:(WMTS for vector data currently only supports '
                                        'EPSG:4326). Defaults to EPSG:4326', default='EPSG:4326')
@click.option('--outputpath', '-o', help='Output path must include output format. Downloaded path default is '
                                         'user home path', default=None)
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def vector_tile_download(layers, zoom, bbox, srsname, outputpath, yes):
    """
    Download vector tiles
    """

    analytics_interface = _analytics()
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "bbox" in line:
                if not yes:
                    bbox_check = click.prompt(
                        "A bbox has been found in the .MGP-config file. Would you like to use this "
                        "bbox?[y/n]")
                    if bbox_check.lower() == "n":
                        if bbox:
                            bbox = bbox
                        else:
                            return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                    elif bbox_check.lower() == "y":
                        bbox = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not bbox:
                    bbox = line.split("=")[1]
                elif yes and bbox:
                    bbox = bbox
            else:
                bbox = bbox
    vec_tile = analytics_interface.download_vector_tiles(
        layers=layers, zoom_level=zoom, bbox=bbox, srsname=srsname, outputpath=outputpath
    )
    click.echo(vec_tile)


@click.command()
@click.option('--bbox', '-b', help='Bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)')
@click.option('--srsname', '-srs', help='Desired projection. Defaults to EPSG:4326', default='EPSG:4326')
@click.option('--filter', '-f', help='CQL filter used to refine data of search. Defaults to None', default=None)
@click.option('--layer', '-l', help='Desired basemap layer. Defaults to VIVID_BASIC', default='VIVID_BASIC')
@click.option('--shapefile', '-shp', help='Binary of whether or not to return as shapefile format', type=bool)
@click.option('--csv', '-c', help='Binary of whether to return as a csv format, Defaults to False', is_flag=True,
              default=False)
@click.option('--seamlines', '-s', help='Binary to search seamlines data. Defaults to False', is_flag=True,
              default=False)
@click.option('--featureprofile', '-fp', help='String of the desired stacking profile')
@click.option('--typename', '-t', help='String of the desired type name')
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def basemaps_search(bbox, srsname, filter, layer, shapefile, csv, seamlines, featureprofile, typename, yes):
    """
    Searches an AOI using the WFS method and returns a list of basemap features and their metadata that intersect with
    the AOI
    """

    basemaps_interface = _basemaps()
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "bbox" in line:
                if not yes:
                    bbox_check = click.prompt(
                        "A bbox has been found in the .MGP-config file. Would you like to use this "
                        "bbox?[y/n]")
                    if bbox_check.lower() == "n":
                        if bbox:
                            bbox = bbox
                        else:
                            return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                    elif bbox_check.lower() == "y":
                        bbox = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not bbox:
                    bbox = line.split("=")[1]
                elif yes and bbox:
                    bbox = bbox
            else:
                bbox = bbox
    layer_options = ['VIVID_BASIC', 'VIVID_ADVANCED', 'VIVID_STANDARD', 'VIVID_STANDARD_30', 'VIVID_PREMIUM']
    if layer not in layer_options:
        raise Exception("{} is not a valid basemap layer option".format(layer))
    if seamlines:
        product_name = "product_name='{}'".format(layer)
    else:
        product_name = "productName='{}'".format(layer)
    if filter:
        combined_filter = "({})AND({})".format(product_name, filter)
        params = {
            "bbox": bbox, "srsname": srsname, "filter": combined_filter, "shapefile": shapefile, "csv": csv,
            "seamlines": seamlines, "featureprofile": featureprofile, "typename": typename
        }
    else:
        params = {
            "bbox": bbox, "srsname": srsname, "filter": product_name, "shapefile": shapefile, "csv": csv,
            "seamlines": seamlines, "featureprofile": featureprofile, "typename": typename
        }
    not_none_params = {k: v for k, v in params.items() if v is not None}
    search = basemaps_interface.search(**not_none_params)
    click.echo(search)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)', type=str)
@click.option('--srsname', '-srs', help='Desired projection. Defaults to EPSG:4326', default='EPSG:4326')
@click.option('--layer', '-l', help='Desired basemap layer. Defaults to VIVID_BASIC', default='VIVID_BASIC')
@click.option('--height', '-h', help='Integer value representing the vertical number of pixels to return', type=int)
@click.option('--width', '-w', help='Integer value representing the horizontal number of pixels to return', type=int)
@click.option('--img_format', '-img', help='String of the format of the response image either jpeg, png or geotiff. '
                                           'Defaults to jpeg', type=str, default='jpeg')
@click.option('--zoom_level', '-z', help='Integer value of the zoom level. Used for WMTS', type=int)
@click.option('--filter', '-f', help='CQL filter used to refine data of search. Defaults to None', default=None)
@click.option('--outputpath', '-o', help='Path to desired download location')
@click.option('--seamlines', '-s', help='Binary to search seamlines data. Defaults to False', is_flag=True,
              default=False)
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def basemaps_download(bbox, srsname, layer, height, width, img_format, zoom_level, filter, outputpath, seamlines, yes):
    """
    Downloads an image or a list of image calls and returns the file location of the download. NOTE: Structure
    of call should be structured with one of the following: 1) bbox, zoom_level, img_format; 2) bbox, img_format, height, width
    """

    basemaps_interface = _basemaps()
    if not outputpath:
        home_dir = os.path.expanduser("~")
        outputpath = os.path.join(home_dir, "CLI_download.{}".format(img_format))
    layer_options = ['VIVID_BASIC', 'VIVID_ADVANCED', 'VIVID_STANDARD', 'VIVID_STANDARD_30', 'VIVID_PREMIUM']
    if layer not in layer_options:
        raise Exception("{} is not a valid basemap layer option".format(layer))
    if seamlines:
        product_name = "product_name='{}'".format(layer)
    else:
        product_name = "productName='{}'".format(layer)
    if zoom_level:
        home_dir = os.path.expanduser("~")
        with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
            lines = f.readlines()
            for line in lines:
                if "bbox" in line:
                    if not yes:
                        bbox_check = click.prompt(
                            "A bbox has been found in the .MGP-config file. Would you like to use this "
                            "bbox?[y/n]")
                        if bbox_check.lower() == "n":
                            if bbox:
                                bbox = bbox
                            else:
                                return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                        elif bbox_check.lower() == "y":
                            bbox = line.split("=")[1]
                        else:
                            return click.echo("Invalid input. Please run command again and enter either y or n")
                    elif yes and not bbox:
                        bbox = line.split("=")[1]
                    elif yes and bbox:
                        bbox = bbox
                else:
                    bbox = bbox
            if filter:
                combined_filter = "({})AND({})".format(product_name, filter)
                wmts = basemaps_interface.download_image(zoom_level=zoom_level, bbox=bbox, img_format=img_format,
                                                         srsname=srsname, download=True, outputpath=outputpath,
                                                         seamlines=seamlines, filter=combined_filter)
            else:
                wmts = basemaps_interface.download_image(zoom_level=zoom_level, bbox=bbox, img_format=img_format,
                                                         srsname=srsname, download=True, outputpath=outputpath,
                                                         seamlines=seamlines, filter=product_name)
        click.echo(wmts)
    else:
        if not img_format or not width or not height:
            raise Exception('height/width must have an img_format')
        else:
            home_dir = os.path.expanduser("~")
            with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if "bbox" in line:
                        if not yes:
                            bbox_check = click.prompt(
                                "A bbox has been found in the .MGP-config file. Would you like to use this "
                                "bbox?[y/n]")
                            if bbox_check.lower() == "n":
                                if bbox:
                                    bbox = bbox
                                else:
                                    return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                            elif bbox_check.lower() == "y":
                                bbox = line.split("=")[1]
                            else:
                                return click.echo("Invalid input. Please run command again and enter either y or n")
                        elif yes and not bbox:
                            bbox = line.split("=")[1]
                        elif yes and bbox:
                            bbox = bbox
                    else:
                        bbox = bbox
            if filter:
                combined_filter = "({})AND({})".format(product_name, filter)
                wms = basemaps_interface.download_image(bbox=bbox, img_format=img_format, height=height, width=width,
                                                        srsname=srsname, display=False, download=True,
                                                        outputpath=outputpath, seamlines=seamlines,
                                                        filter=combined_filter)
            else:
                wms = basemaps_interface.download_image(bbox=bbox, img_format=img_format, height=height, width=width,
                                                        srsname=srsname, display=False, download=True,
                                                        outputpath=outputpath, seamlines=seamlines,
                                                        filter=product_name)
        click.echo(wms)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)')
@click.option('--zoom_level', '-z', help='Integer value of the zoom level. Used for WMTS', type=int)
@click.option('--srsname', '-srs', help='Desired projection. Defaults to EPSG:4326', default='EPSG:4326')
@click.option('--seamlines', '-s', help='Binary to search seamlines data. Defaults to False', is_flag=True,
              default=False)
@click.option('--filter', '-f', help='CQL filter used to refine data of search. Defaults to None', default=None)
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def basemaps_tile_list(bbox, zoom_level, srsname, seamlines, filter, yes):
    """
    Return a list of tiles and their associated requests
    """

    basemaps_interface = _basemaps()
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "bbox" in line:
                if not yes:
                    bbox_check = click.prompt(
                        "A bbox has been found in the .MGP-config file. Would you like to use this "
                        "bbox?[y/n]")
                    if bbox_check.lower() == "n":
                        if bbox:
                            bbox = bbox
                        else:
                            return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                    elif bbox_check.lower() == "y":
                        bbox = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not bbox:
                    bbox = line.split("=")[1]
                elif yes and bbox:
                    bbox = bbox
            else:
                bbox = bbox
    params = {
        "bbox": bbox, "zoom_level": zoom_level, "srsname": srsname, "filter": filter, "seamlines": seamlines
    }
    not_none_params = {k: v for k, v in params.items() if v is not None}
    tile_list = basemaps_interface.get_tile_list_with_zoom(**not_none_params)
    click.echo(tile_list)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)')
@click.option('--zoom_level', '-z', help='Integer value of the zoom level. Used for WMTS', type=int, required=True)
@click.option('--srsname', '-srs', help='Desired projection. Defaults to EPSG:4326', default='EPSG:4326')
@click.option('--layer', '-l', help='Desired basemap layer. Defaults to VIVID_BASIC', default='VIVID_BASIC')
@click.option('--img_format', '-img', help='String of the format of the response image either jpeg, png or geotiff. '
                                           'Defaults to jpeg', default='jpeg')
@click.option('--filter', '-f', help='CQL filter used to refine data of search. Defaults to None', default=None)
@click.option('--outputpath', '-o', help='Output path must include output format. Downloaded path default is user home '
                                         'path', default=None)
@click.option('--seamlines', '-s', help='Binary to search seamlines data. Defaults to False', is_flag=True,
              default=False)
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def basemaps_download_tiles(bbox, zoom_level, srsname, layer, img_format, filter, outputpath, seamlines, yes):
    """
    Download basemap tiles over a given AOI
    """

    basemaps_interface = _basemaps()
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "bbox" in line:
                if not yes:
                    bbox_check = click.prompt(
                        "A bbox has been found in the .MGP-config file. Would you like to use this "
                        "bbox?[y/n]")
                    if bbox_check.lower() == "n":
                        if bbox:
                            bbox = bbox
                        else:
                            return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                    elif bbox_check.lower() == "y":
                        bbox = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not bbox:
                    bbox = line.split("=")[1]
                elif yes and bbox:
                    bbox = bbox
            else:
                bbox = bbox
    layer_options = ['VIVID_BASIC', 'VIVID_ADVANCED', 'VIVID_STANDARD', 'VIVID_STANDARD_30', 'VIVID_PREMIUM']
    if layer not in layer_options:
        raise Exception("{} is not a valid basemap layer option".format(layer))
    if seamlines:
        product_name = "product_name='{}'".format(layer)
    else:
        product_name = "productName='{}'".format(layer)
    if filter:
        combined_filter = "({})AND({})".format(product_name, filter)
        tiles = basemaps_interface.download_tiles(
            bbox=bbox, zoom_level=zoom_level, srsname=srsname, img_format=img_format, filter=combined_filter,
            outputpath=outputpath, seamlines=seamlines
        )
    else:
        tiles = basemaps_interface.download_tiles(
            bbox=bbox, zoom_level=zoom_level, srsname=srsname, img_format=img_format, filter=product_name,
            outputpath=outputpath, seamlines=seamlines
        )
    click.echo(tiles)


@click.command()
@click.option('--bbox', '-b',
              help='String bounding box of AOI. Comma delimited set of coordinates. (miny,minx,maxy,maxx)')
@click.option('--height', '-h', help='Integer value representing the vertical number of pixels to return', type=int,
              required=True)
@click.option('--width', '-w', help='Integer value representing the horizontal number of pixels to return', type=int,
              required=True)
@click.option('--srsname', '-srs', help='Desired projection. Defaults to EPSG:4326', default='EPSG:4326')
@click.option('--layer', '-l', help='Desired basemap layer. Defaults to VIVID_BASIC', default='VIVID_BASIC')
@click.option('--img_format', '-img', help='String of the format of the response image either jpeg, png or geotiff. '
                                           'Defaults to jpeg', default='jpeg')
@click.option('--filter', '-f', help='CQL filter used to refine data of search. Defaults to None', default=None)
@click.option('--outputpath', '-o', help='Output path must include output format. Downloaded path default is user home '
                                         'path', default=None)
@click.option('--seamlines', '-s', help='Binary to search seamlines data. Defaults to False', is_flag=True,
              default=False)
@click.option('--yes', '-y', help='Flag to bypass one or more variable checks. Defaults to False', is_flag=True,
              default=False)
def basemaps_image_by_pixel_count(bbox, height, width, srsname, layer, img_format, filter, outputpath, seamlines, yes):
    """
    Download a basemap image over a given AOI
    """

    basemaps_interface = _basemaps()
    home_dir = os.path.expanduser("~")
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "bbox" in line:
                if not yes:
                    bbox_check = click.prompt(
                        "A bbox has been found in the .MGP-config file. Would you like to use this "
                        "bbox?[y/n]")
                    if bbox_check.lower() == "n":
                        if bbox:
                            bbox = bbox
                        else:
                            return click.echo("No bbox entered and no bbox passed from .MGP-config file")
                    elif bbox_check.lower() == "y":
                        bbox = line.split("=")[1]
                    else:
                        return click.echo("Invalid input. Please run command again and enter either y or n")
                elif yes and not bbox:
                    bbox = line.split("=")[1]
                elif yes and bbox:
                    bbox = bbox
            else:
                bbox = bbox
    layer_options = ['VIVID_BASIC', 'VIVID_ADVANCED', 'VIVID_STANDARD', 'VIVID_STANDARD_30', 'VIVID_PREMIUM']
    if layer not in layer_options:
        raise Exception("{} is not a valid basemap layer option".format(layer))
    if seamlines:
        product_name = "product_name='{}'".format(layer)
    else:
        product_name = "productName='{}'".format(layer)
    if filter:
        combined_filter = "({})AND({})".format(product_name, filter)
        wms = basemaps_interface.download_image_by_pixel_count(
            bbox=bbox, height=height, width=width, srsname=srsname, img_format=img_format, outputpath=outputpath,
            seamlines=seamlines, filter=combined_filter
        )
    else:
        wms = basemaps_interface.download_image_by_pixel_count(
            bbox=bbox, height=height, width=width, srsname=srsname, img_format=img_format, outputpath=outputpath,
            seamlines=seamlines, filter=product_name
        )
    click.echo(wms)


@click.command()
@click.option('--variables', '-v', type=click.Choice(
    ['order_settings', 'bbox', 'output_config', 'notifications_settings', 'geojson', 'monitor_notifications',
     'tasking_template', 'match_criteria']
), multiple=True, help="Variables for storage")
def store_variables(variables):
    """
    \b
    Creates variables to be stored in the .MGP-config file for future use. Available options are:
        order_settings (string(dict)) = Settings for an order. Ex: {"settings": {"inventory_ids": ["item_id"], "customer_description": "descripiton"}}
        bbox (int) = Comma separated integers in miny,minx,maxy,maxx format. Ex: 39.743,-104.959,39.754,-104.940
        output_config (string(dict)) = Settings for an output configuration. Ex: {"output_config": {"amazon_s3": {"bucket": "bucket-name", "prefix": "prefix/name"}}}
        notifications_settings (string(list(dict))) = Settings for a notification output. Ex: [{"type": "email", "target": "your.email@address.com", "level": "FINAL_ONLY"}] **Note: For use with ordering and tasking only**
        geojson (string(dict)) = AOI in geoJSON format. Ex: {"type": "Polygon", "coordinates": [[[-103.991089, 39.546412], [-103.900452, 39.546412], [-103.900452, 39.474365], [-103.991089, 39.474365], [-103.991089, 39.546412]]]}
        monitor_notifications (string(list(dict))) = Settings for a notification output for a monitor. Ex: [{"type": "email", "target": "your.email@address.com"}]
        tasking_template (string(dict)) = Template for a tasking request. Ex: {"settings": {"inventory_ids": ["$.id"], "customer_description": "description"}}
        match_criteria (string(dict)) = Template for match criteria for monitoring. Ex: {"platform": {"in": ["worldview-03", "worldview-02"]}, "eo:cloud_cover": {"lt": 75}, "aoi:coverage_sqkm": {"gte": 1}}
    """

    home_dir = os.path.expanduser("~")
    for item in variables:
        if item == "bbox":
            var_box = click.prompt('Enter bbox in miny,minx,maxy,maxx format')
        elif item == "order_settings":
            var_order_settings = click.prompt('Enter order settings')
        elif item == "output_config":
            var_output_config = click.prompt('Enter output config')
        elif item == "notifications_settings":
            var_notifications_settings = click.prompt('Enter notifications settings')
        elif item == "geojson":
            var_geojson = click.prompt('Enter geoJSON')
        elif item == "monitor_notifications":
            var_monitor_notifications = click.prompt('Enter monitor notifications')
        elif item == "tasking_template":
            var_tasking_template = click.prompt('Enter tasking template')
        elif item == "match_criteria":
            var_match_criteria = click.prompt('Enter match criteria')
        else:
            return click.echo('{} is not a recognized variable for storage. Please enter a valid variable'.format(item))
    with open(os.path.join(home_dir, ".MGP-config"), 'r') as f:
        lines = f.readlines()
        lines_to_write = []
        bbox_overwrite = False
        order_overwrite = False
        config_overwrite = False
        notifications_overwrite = False
        geojson_overwrite = False
        monitor_notifications_overwrite = False
        tasking_template_overwrite = False
        match_criteria_overwrite = False
        last = lines[-1]
        for item in variables:
            if item == "bbox":
                for line in lines:
                    if "bbox" in line:
                        bbox_check = input("A bbox is already stored. Would you like to overwrite?[y/n]: ")
                        if bbox_check.lower() == "n":
                            return click.echo("Variable storage aborted")
                        elif bbox_check.lower() == "y":
                            pass
                        else:
                            return click.echo("Invalid input. Please run command again and enter either y or n")
                if "\n" in last:
                    bbox_format = 'bbox={}\n'
                else:
                    bbox_format = '\nbbox={}\n'
                for line in lines:
                    if "bbox" in line:
                        lines_to_write.append(bbox_format.format(var_box))
                        bbox_overwrite = True
                    else:
                        lines_to_write.append(line)
                if not bbox_overwrite:
                    lines_to_write.append(bbox_format.format(var_box))
            elif item == "order_settings":
                for line in lines:
                    if "order_settings" in line:
                        order_settings_check = input("Order settings are already stored. Overwrite?[y/n]: ")
                        if order_settings_check.lower() == "n":
                            return click.echo("Variable storage aborted")
                        elif order_settings_check.lower() == "y":
                            pass
                        else:
                            return click.echo("Invalid input. Please run command again and enter either y or n")
                if "\n" in last:
                    order_format = 'order_settings={}'
                else:
                    order_format = '\norder_settings={}'
                for line in lines:
                    if "order_settings" in line:
                        lines_to_write.append(
                            "{}{}{}{}{}".format(
                                order_format, "{", '"settings":{}'.format(var_order_settings), "}", '\n'
                            )
                        )
                        order_overwrite = True
                    else:
                        lines_to_write.append(line)
                if not order_overwrite:
                    lines_to_write.append(order_format.format(var_order_settings))
            elif item == "output_config":
                for line in lines:
                    if "output_settings" in line:
                        output_config_check = input("Output config is already stored. Overwrite?[y/n]: ")
                        if output_config_check.lower() == "n":
                            return click.echo("Variable storage aborted")
                        elif output_config_check.lower() == "y":
                            pass
                        else:
                            return click.echo("Invalid input. Please run command again and enter either y or n")
                if "\n" in last:
                    config_format = 'output_settings={}'
                else:
                    config_format = '\noutput_settings={}'
                for line in lines:
                    if "output_settings" in line:
                        lines_to_write.append(
                            "{}{}{}{}{}".format(
                                config_format, "{", '"output_config":{}'.format(var_output_config), "}", '\n'
                            )
                        )
                        config_overwrite = True
                    else:
                        lines_to_write.append(line)
                if not config_overwrite:
                    lines_to_write.append(config_format.format(var_output_config))
            elif item == "notifications_settings":
                for line in lines:
                    if "notifications_settings" in line:
                        notifications_check = input("Notifications settings are already stored. Overwrite?[y/n]: ")
                        if notifications_check.lower() == "n":
                            return click.echo("Variable storage aborted")
                        elif notifications_check.lower() == "y":
                            pass
                        else:
                            return click.echo("Invalid input. Please run command again and enter either y or n")
                if "\n" in last:
                    notifications_format = 'notifications_settings=[{}]'
                else:
                    notifications_format = '\nnotifications_settings=[{}]'
                for line in lines:
                    if "notifications_settings" in line:
                        lines_to_write.append(
                            "{}{}{}".format(notifications_format, ' [{}]'.format(var_notifications_settings), '\n')
                        )
                        notifications_overwrite = True
                    else:
                        lines_to_write.append(line)
                if not notifications_overwrite:
                    lines_to_write.append(notifications_format.format(var_notifications_settings))
            elif item == "geojson":
                for line in lines:
                    if "geojson" in line:
                        geojson_check = input("A geoJSON is already stored. Overwrite?[y/n]: ")
                        if geojson_check.lower() == "n":
                            return click.echo("Variable storage aborted")
                        elif geojson_check.lower() == "y":
                            pass
                        else:
                            return click.echo("Invalid input. Please run command again and enter either y or n")
                if "\n" in last:
                    geojson_format = 'geojson={}\n'
                else:
                    geojson_format = '\ngeojson={}\n'
                for line in lines:
                    if "geojson" in line:
                        lines_to_write.append(geojson_format.format(var_geojson))
                        geojson_overwrite = True
                    else:
                        lines_to_write.append(line)
                if not geojson_overwrite:
                    lines_to_write.append(geojson_format.format(var_geojson))
            elif item == "monitor_notifications":
                for line in lines:
                    if "monitor_notifications" in line:
                        monitor_notification_check = input(
                            "A monitor notification is already stored. Overwrite?[y/n]: "
                        )
                        if monitor_notification_check.lower() == "n":
                            return click.echo("Variable storage aborted")
                        elif monitor_notification_check.lower() == "y":
                            pass
                        else:
                            return click.echo("Invalid input. Please run command again and enter either y or n")
                if "\n" in last:
                    monitor_notification_format = 'monitor_notifications={}\n'
                else:
                    monitor_notification_format = '\nmonitor_notifications={}\n'
                for line in lines:
                    if "monitor_notifications" in line:
                        lines_to_write.append(
                            "{}{}{}".format(monitor_notification_format, '[{}]'.format(var_monitor_notifications), '\n')
                        )
                        monitor_notifications_overwrite = True
                    else:
                        lines_to_write.append(line)
                if not monitor_notifications_overwrite:
                    lines_to_write.append(monitor_notification_format.format(var_monitor_notifications))
            elif item == "tasking_template":
                for line in lines:
                    if "tasking_template" in line:
                        tasking_template_check = input("A tasking template is already stored. Overwrite?[y/n]: ")
                        if tasking_template_check.lower() == "n":
                            return click.echo("Variable storage aborted")
                        elif tasking_template_check.lower() == "y":
                            pass
                        else:
                            return click.echo("Invalid input. Please run command again and enter either y or n")
                if "\n" in last:
                    tasking_template_format = 'tasking_template={}'
                else:
                    tasking_template_format = '\ntasking_template={}'
                for line in lines:
                    if "tasking_template" in line:
                        lines_to_write.append(
                            "{}{}{}".format(tasking_template_format, '{}'.format(var_tasking_template), '\n')
                        )
                        tasking_template_overwrite = True
                    else:
                        lines_to_write.append(line)
                if not tasking_template_overwrite:
                    lines_to_write.append(tasking_template_format.format(var_tasking_template))
            elif item == "match_criteria":
                for line in lines:
                    if "match_criteria" in line:
                        match_criteria_check = input("A match criteria is already stored. Overwrite?[y/n]: ")
                        if match_criteria_check.lower() == "n":
                            return click.echo("Variable storage aborted")
                        elif match_criteria_check.lower() == "y":
                            pass
                        else:
                            return click.echo("Invalid input. Please run command again and enter either y or n")
                if "\n" in last:
                    match_criteria_format = 'match_criteria={}\n'
                else:
                    match_criteria_format = '\nmatch_criteria={}\n'
                for line in lines:
                    if "match_criteria" in line:
                        lines_to_write.append(match_criteria_format.format(var_match_criteria))
                        match_criteria_overwrite = True
                    else:
                        lines_to_write.append(line)
                if not match_criteria_overwrite:
                    lines_to_write.append(match_criteria_format.format(var_match_criteria))
    with open(os.path.join(home_dir, ".MGP-config"), 'w') as f:
        f.writelines(lines_to_write)
    return click.echo("Variable stored in .MGP-config file")


cli.add_command(home_dir)
cli.add_command(create_token)
cli.add_command(get_tokens)
cli.add_command(delete_tokens)
cli.add_command(config_file)
cli.add_command(reset_password)
cli.add_command(search)
cli.add_command(download)
cli.add_command(get_tile_list)
cli.add_command(download_tiles)
cli.add_command(download_by_pixel_count)
cli.add_command(full_res_image)
cli.add_command(mosaic)
cli.add_command(calculate_bbox_sqkm)
cli.add_command(get_accounts)
cli.add_command(account_roles)
cli.add_command(account_comments)
cli.add_command(get_activations)
cli.add_command(activations_for_account)
cli.add_command(activation_credit_limit)
cli.add_command(activation_types)
cli.add_command(get_products)
cli.add_command(product_filter)
cli.add_command(get_rate_table)
cli.add_command(get_activation_for_table)
cli.add_command(get_credit_types)
cli.add_command(get_rate_amounts)
cli.add_command(get_table_and_activations)
cli.add_command(get_roles)
cli.add_command(user_types)
cli.add_command(get_users)
cli.add_command(update_user)
cli.add_command(create_user)
cli.add_command(update_user_roles)
cli.add_command(get_user_roles)
cli.add_command(get_user_available_roles)
cli.add_command(delete_user)
cli.add_command(account_usage)
cli.add_command(activation_usage)
cli.add_command(user_usage)
cli.add_command(usage_is_allowed)
cli.add_command(usage_overview)
cli.add_command(stac_search)
cli.add_command(search_audit_fields)
cli.add_command(root_catalog)
cli.add_command(collection_definition)
cli.add_command(all_collections)
cli.add_command(get_stac_item)
cli.add_command(top_level_sub_catalog)
cli.add_command(sub_catalog_definition)
cli.add_command(all_sub_catalog_definitions)
cli.add_command(sub_catalog_collection_definition)
cli.add_command(all_pipelines)
cli.add_command(get_pipeline)
cli.add_command(order)
cli.add_command(order_details)
cli.add_command(order_events)
cli.add_command(list_users_orders)
cli.add_command(cancel_order)
cli.add_command(submit_tasking)
cli.add_command(get_tasking_request)
cli.add_command(cancel_tasking)
cli.add_command(create_monitor)
cli.add_command(get_monitor)
cli.add_command(monitor_events)
cli.add_command(toggle_monitor)
cli.add_command(raster_url)
cli.add_command(get_raster_metadata)
cli.add_command(get_raster_array)
cli.add_command(vector_search)
cli.add_command(vector_image_download)
cli.add_command(vector_tile_download)
cli.add_command(basemaps_search)
cli.add_command(basemaps_download)
cli.add_command(basemaps_tile_list)
cli.add_command(basemaps_download_tiles)
cli.add_command(basemaps_image_by_pixel_count)
cli.add_command(store_variables)
