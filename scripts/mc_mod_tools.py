import argparse
import os
import random
import shutil
import string
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
    parser.add_argument('command', help="Select which command is going to be run", default=None)
parser.add_argument("-d", dest="destination", help="backup destination (will use path from config.ini if not given)",
                    required=False, default=None)
parser.add_argument("-md", dest="mc_directory", help="minecraft directory (will use path from config.ini if not given)",
                    required=False, default=None)
parser.add_argument("-p", dest="pack", help="path to mod pack", required=False, default=None)
parser.add_argument("-c", dest="cache_folder", help="cache folder", required=False, default=None)
parser.add_argument("-s", dest="source", help="source folder path", required=False, default=None)
parser.add_argument("-q", dest="quiet", help="use to skip confirmation & backup prompt", required=False, default=False,
                    action='store_true')
args = parser.parse_args()

# Check arguments
if __name__ == "__main__":
    if args.destination is not None:
        if not os.path.isdir(args.destination):
            print("The backup path given isn't valid or doesn't exist.")
            quit()
    if args.mc_directory is not None:
        if not os.path.isdir(args.mc_directory):
            print("The backup path given isn't valid or doesn't exist.")
            quit()
    if args.cache_folder is not None:
        if not os.path.isdir(args.cache_folder):
            print("The backup path given isn't valid or doesn't exist.")
            quit()
    if args.source is not None:
        if not os.path.isdir(args.source):
            print("The backup path given isn't valid or doesn't exist.")
            quit()

# Check configuration
if args.destination is None:
    if config.get('Paths', 'default-backup-path') != "NOT_SET":
        if not os.path.isdir(config.get('Paths', 'default-backup-path')):
            print("The backup path in the configuration isn't valid or doesn't exist.")
            quit()
    elif config.get('Paths', 'default-backup-path') == "NOT_SET":
        print("The backup path in the configuration isn't given.")
        quit()
if args.mc_directory is None:
    if config.get('Paths', 'minecraft-mod-folder') != "default":
        if not os.path.isdir(config.get('Paths', 'minecraft-mod-folder')):
            print("The minecraft mod folder path in the configuration isn't valid or doesn't exist.")
            quit()
if args.cache_folder is None:
    if config.get('Paths', 'cache-folder') != "NOT_SET":
        if not os.path.isdir(config.get('Paths', 'cache-folder')):
            print("The cache path in the configuration isn't given.")
            quit()
    elif config.get('Paths', 'cache-folder') == "NOT_SET":
        print("The cache path in the configuration isn't given.")
        quit()


# @Nitro4542 pls fix
# if config.get('General','operating-system') != "Windows":
#    print('Please check your configuration at operating-system.')
#    quit()
# elif config.get('General','operating-system') != "Linux":
#    print('Please check your configuration at operating-system.')
#    quit()

# Set mod folder path
def set_mod_folder():
    if args.mc_directory is not None:
        mod_folder = args.mc_directory
    elif config.get('Paths', 'minecraft-mod-folder') != "default":
        mod_folder = config.get('Paths', 'minecraft-mod-folder')
    else:
        if config.get('General', 'operating-system') == "Windows":
            mod_folder = os.getenv('APPDATA') + "\\.minecraft\\mods"
        elif config.get('General', 'operating-system') == "Linux":
            mc_mod_folder = os.getenv('HOME') + "/.minecraft/mods"
    return mod_folder


# Generates a random string
# Needed for some functions to work properly
def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


# Function to cache your mod pack
def cache_mod_pack(cache_dest):
    mc_mod_folder = set_mod_folder()
    # Create folder for zip file + Check configuration
    if cache_dest is not None:
        if os.path.isdir(cache_dest):
            final_destination = cache_dest + "\\" + datetime.today().strftime('%Y-%m-%d') + "_" + randomword(5)
        else:
            print("The cache path given isn't valid or doesn't exist.")
            quit()
    elif args.cache_folder is None:
        if config.get('Paths', 'cache-folder') != "NOT_SET":
            if os.path.isdir(config.get('Paths', 'cache-folder')):
                final_destination = config.get('Paths', 'cache-folder') + "\\" + datetime.today().strftime(
                    '%Y-%m-%d') + "_" + randomword(5)
            else:
                print("The cache path in the configuration isn't valid or doesn't exist.")
                quit()
    elif args.cache_folder is not None:
        if os.path.isdir(args.cache_folder):
            final_destination = args.cache_folder + "\\" + datetime.today().strftime('%Y-%m-%d') + "_" + randomword(5)
        else:
            print("The cache path isn't valid or doesn't exist.")
            quit()
    else:
        print('Error: Please provide a valid cache folder path.')
        quit()
    # Extract zip file
    with ZipFile(args.pack, 'r') as zipobject:
        zipobject.extractall(
            path=final_destination)
    zipobject.close()


# Creates backup of your mods folder
def create_backup(backup_dest):
    mc_mod_folder = set_mod_folder()
    # Create folder for zip file + Check configuration
    if backup_dest is not None:
        if os.path.isdir(backup_dest):
            final_destination = backup_dest + "\\" + datetime.today().strftime('%Y-%m-%d') + "_" + randomword(5)
        else:
            print("The backup path given isn't valid or doesn't exist.")
            quit()
    # Get and add backup name to destination and create folder if necessary
    elif config.get('Paths', 'default-backup-path') == "NOT_SET":
        final_destination = args.destination + "\\" + "mod-backup-" + datetime.today().strftime(
            '%Y-%m-%d') + "_" + randomword(5)
    else:
        final_destination = config.get('Paths',
                                       'default-backup-path') + "\\" + "mod-backup-" + datetime.today().strftime(
            '%Y-%m-%d') + "_" + randomword(5)
    if not os.path.isdir(final_destination):
        os.mkdir(final_destination)
    # Create backup
    src_files = os.listdir(mc_mod_folder)
    for file_name in src_files:
        full_file_name = os.path.join(mc_mod_folder, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy2(full_file_name, final_destination)


# Deletes all mods in mods folder
def delete_mods():
    mc_mod_folder = set_mod_folder()
    for filename in os.listdir(mc_mod_folder):
        file_path = os.path.join(mc_mod_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# Confirmation prompt for delete_mods()
def confirm_prompt():
    answer0 = input("Do you want to create a backup of your existing mods? [Y|N]")
    if answer0.lower() in ["y", "yes"]:
        create_backup(None)
    elif answer0.lower() in ["n", "no"]:
        print('Won\'t create backup')
    else:
        print('Only \"y\" or \"n\" are allowed. Try again.')
        confirm_prompt()
    answer = input("Continue? - All of your mods are being erased! [Y|N]: ")
    if answer.lower() in ["y", "yes"]:
        delete_mods()
    elif answer.lower() in ["n", "no"]:
        quit()
    else:
        print('Only \"y\" or \"n\" are allowed. Try again.')
        confirm_prompt()


# Copies mods in your mods folder
def install_mods(src):
    mc_mod_folder = set_mod_folder()
    # Set + check source folder path
    if src is None:
        src = args.source
    if not os.path.isdir(src):
        print("The source path isn't valid or doesn't exist.")
        quit()
    # Copies all contents of selected folder in mods folder
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy2(full_file_name, mc_mod_folder)


# Run selected command
if __name__ == "__main__":
    if args.command == "prepare":
        cache_mod_pack(None)
    elif args.command == "backup":
        create_backup(None)
    elif args.command == "remove":
        if args.silent:
            delete_mods()
        elif not args.silent:
            confirm_prompt()
    elif args.command == "install":
        install_mods(None)
