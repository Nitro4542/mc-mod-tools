"""A module for managing your Minecraft mods"""
# Import needed libraries
import argparse
import os
import random
import shutil
import string
import sys
from configparser import ConfigParser
from datetime import datetime
from zipfile import ZipFile

# Load configuration
config = ConfigParser()
config.read('config.ini')

# Arguments
parser = argparse.ArgumentParser(prog='nitro_mc_mod_tools',
                                 description='Toolbox for Nitro\'s Minecraft mod pack format')
if __name__ == "__main__":
    parser.add_argument('command',
                        help="Select which command is going to be run", default=None)
parser.add_argument("-d", dest="destination",
                    help="backup destination (will use path from config.ini if not given)",
                    required=False, default=None)
parser.add_argument("-md", dest="mc_directory",
                    help="minecraft directory (will use path from config.ini if not given)",
                    required=False, default=None)
parser.add_argument("-p", dest="pack",
                    help="path to mod pack",
                    required=False, default=None)
parser.add_argument("-c", dest="cache_folder",
                    help="cache folder",
                    required=False, default=None)
parser.add_argument("-s", dest="source",
                    help="source folder path",
                    required=False, default=None)
parser.add_argument("-q", dest="quiet",
                    help="use to skip confirmation & backup prompt",
                    required=False, default=False, action='store_true')
args = parser.parse_args()

# Check arguments
if __name__ == "__main__":
    if args.destination is not None:
        if not os.path.isdir(args.destination):
            print("The backup path given isn't valid or doesn't exist.")
            sys.exit(1)
    if args.mc_directory is not None:
        if not os.path.isdir(args.mc_directory):
            print("The backup path given isn't valid or doesn't exist.")
            sys.exit(1)
    if args.cache_folder is not None:
        if not os.path.isdir(args.cache_folder):
            print("The backup path given isn't valid or doesn't exist.")
            sys.exit(1)
    if args.source is not None:
        if not os.path.isdir(args.source):
            print("The backup path given isn't valid or doesn't exist.")
            sys.exit(1)


def randomword(length):
    """Generates a random string
    Needed for some functions to work properly"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def get_mod_folder(modfolder_input):
    """Sets mod folder path"""
    if modfolder_input is not None:
        mod_folder = modfolder_input
    elif args.mc_directory is not None:
        mod_folder = args.mc_directory
    elif config.get('Paths', 'minecraft-mod-folder') != "default":
        mod_folder = config.get('Paths', 'minecraft-mod-folder')
    else:
        if config.get('General', 'operating-system') == "Windows":
            mod_folder = os.getenv('APPDATA') + "\\.minecraft\\mods"
        elif config.get('General', 'operating-system') == "Linux":
            mod_folder = os.getenv('HOME') + "/.minecraft/mods"
    return mod_folder


def get_backup_folder(backupfolder_input):
    """Sets backup folder"""
    if config.get('Paths', 'default-backup-path') == "default":
        backup_path = "Backups"
    else:
        if backupfolder_input is not None:
            backup_path = backupfolder_input
        elif args.destination is not None:
            backup_path = args.destination
        elif config.get('Paths', 'default-backup-path') != "default":
            backup_path = config.get('Paths', 'default-backup-path')
    return backup_path


def get_cache_folder(cachefolder_input):
    """Sets cache folder"""
    if config.get('Paths', 'cache-folder') == "default":
        cache_path = "Cache"
    else:
        if cachefolder_input is not None:
            cache_path = cachefolder_input
        elif args.cache_folder is not None:
            cache_path = args.cache_folder
        elif config.get('Paths', 'cache_folder') != "default":
            cache_path = config.get('Paths', 'cache_folder')
    return cache_path


def unzip_mod_pack(cache_dest, zipfile_path):
    """Function to unzip your mod pack"""
    # Create folder for zip file + Check configuration
    if cache_dest is not None:
        if os.path.isdir(cache_dest):
            final_destination = (cache_dest + "\\" + datetime.today().strftime('%Y-%m-%d') + "_" +
                                 randomword(5))
    else:
        final_destination = (get_cache_folder(None) + "\\" + datetime.today().strftime('%Y-%m-%d')
                             + "_" + randomword(5))
    if not os.path.isdir(final_destination):
        os.mkdir(final_destination)
    # Extract zip file
    if cache_dest is not None:
        with ZipFile(zipfile_path, 'r') as zipobject:
            zipobject.extractall(
                path=final_destination)
        zipobject.close()
    elif args.cache_folder is not None:
        with ZipFile(args.pack, 'r') as zipobject:
            zipobject.extractall(
                path=final_destination)
        zipobject.close()
    return final_destination


def create_backup(backup_dest):
    """Creates a backup of your mods folder"""
    mc_mod_folder = get_mod_folder(None)
    # Create folder for backup
    if backup_dest is not None:
        if os.path.isdir(backup_dest):
            final_destination = (backup_dest + "\\" + datetime.today().strftime('%Y-%m-%d') + "_" +
                                 randomword(5))
        else:
            print("The backup path given isn't valid or doesn't exist.")
            sys.exit(1)
    # Get and add backup name to destination and create folder if necessary
    else:
        final_destination = (get_backup_folder(None) + "\\" + "mod-backup-" +
                             datetime.today().strftime('%Y-%m-%d') + "_" + randomword(5))
    if not os.path.isdir(final_destination):
        os.mkdir(final_destination)
    # Create backup
    src_files = os.listdir(mc_mod_folder)
    for file_name in src_files:
        full_file_name = os.path.join(mc_mod_folder, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy2(full_file_name, final_destination)


def delete_mods():
    """Deletes all mods in mods folder"""
    mc_mod_folder = get_mod_folder(None)
    for filename in os.listdir(mc_mod_folder):
        file_path = os.path.join(mc_mod_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except OSError:
            print("An exception occurred")


def confirmation_prompt():
    """Confirmation prompt for delete_mods()"""
    answer0 = input("Do you want to create a backup of your existing mods? [Y|N]")
    if answer0.lower() in ["y", "yes"]:
        create_backup(None)
    elif answer0.lower() in ["n", "no"]:
        print('Won\'t create backup')
    else:
        print('Only \"y\" or \"n\" are allowed. Try again.')
        confirmation_prompt()
    answer = input("Continue? - All of your mods are being erased! [Y|N]: ")
    if answer.lower() in ["y", "yes"]:
        delete_mods()
    elif answer.lower() in ["n", "no"]:
        sys.exit(0)
    else:
        print('Only \"y\" or \"n\" are allowed. Try again.')
        confirmation_prompt()


def install_mods(src):
    """Copies mods in your mods folder"""
    mc_mod_folder = get_mod_folder(None)
    # Set + check source folder path
    if src is None:
        src = args.source
    if not os.path.isdir(src):
        print("The source path isn't valid or doesn't exist.")
        sys.exit(1)
    # Copies all contents of selected folder in mods folder
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy2(full_file_name, mc_mod_folder)


def install_mods_zip(zipfile_path):
    """Extracts a zip file containing mods to the mods folder"""
    mc_mod_folder = get_mod_folder(None)
    # Extract zip file
    with ZipFile(zipfile_path, 'r') as zipobject:
        zipobject.extractall(
            path=mc_mod_folder)
    zipobject.close()


# Check config.ini
if args.destination is None:
    if config.get('Paths', 'default-backup-path') != "default":
        if not os.path.isdir(config.get('Paths', 'default-backup-path')):
            print("The backup path in the configuration isn't valid or doesn't exist.")
            sys.exit(1)
if args.mc_directory is None:
    if config.get('Paths', 'minecraft-mod-folder') != "default":
        if not os.path.isdir(config.get('Paths', 'minecraft-mod-folder')):
            print(
                "The minecraft mod folder path in the configuration isn't valid or doesn't exist.")
            sys.exit(1)
if args.cache_folder is None:
    if config.get('Paths', 'cache-folder') != "default":
        if not os.path.isdir(config.get('Paths', 'cache-folder')):
            print("The cache path in the configuration isn't given.")
            sys.exit(1)
if (config.get('General', 'operating-system') != "Windows" and
        config.get('General', 'operating-system') != "Linux"):
    print('Please check your configuration at operating-system.')
    sys.exit(1)

# Run selected commands
if __name__ == "__main__":
    if args.command == "prepare":
        unzip_mod_pack(None, None)
    elif args.command == "backup":
        create_backup(None)
    elif args.command == "remove":
        if args.silent:
            delete_mods()
        elif not args.silent:
            confirmation_prompt()
    elif args.command == "install":
        install_mods(None)
    else:
        print('Please provide a valid command.')
        sys.exit(2)
