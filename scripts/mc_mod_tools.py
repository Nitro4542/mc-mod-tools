import argparse
import os
import shutil
import random, string
from datetime import datetime
from configparser import ConfigParser
from zipfile import ZipFile

# Load configuration
config = ConfigParser()
config.read('config.ini')

# Arguments
parser = argparse.ArgumentParser(prog='nitro-mc-mod-tools',description='Toolbox for Nitro\'s Minecraft mod pack format')
parser.add_argument('command', help="Select which command is going to be run", default=None)
parser.add_argument("-d", dest = "destination", help="backup destination (will use path from config.ini if not given)", required=False, default=None)
parser.add_argument("-md", dest = "mc_directory", help="minecraft directory (will use path from config.ini if not given)", required=False, default=None)
parser.add_argument("-p", dest = "pack", help="path to mod pack", required=False, default=None)
parser.add_argument("-c", dest = "cache_folder", help="cache folder", required=False, default=None)
parser.add_argument("-s", dest = "source", help="source folder path",required=False, default=None)
parser.add_argument("-q", dest = "quiet", help = "use to skip confirmation & backup prompt", required=False, default=False, action='store_true')
args = parser.parse_args()

# Check arguments
if args.destination != None:
    if os.path.isdir(args.destination) != True:
        print("The backup path given isn't valid or doesn't exist.")
        quit()
if args.mc_directory != None:
    if os.path.isdir(args.mc_directory) != True:
        print("The backup path given isn't valid or doesn't exist.")
        quit()
if args.cache_folder != None:
    if os.path.isdir(args.cache_folder) != True:
        print("The backup path given isn't valid or doesn't exist.")
        quit()
if args.source != None:
    if os.path.isdir(args.source) != True:
        print("The backup path given isn't valid or doesn't exist.")
        quit()

# Check configuration
if args.destination == None:
    if config.get('Paths','default-backup-path') != "NOT_SET":
        if os.path.isdir(config.get('Paths','default-backup-path')) != True:
            print("The backup path in the configuration isn't valid or doesn't exist.")
            quit()
    elif config.get('Paths','default-backup-path') == "NOT_SET":
        print("The backup path in the configuration isn't given.")
        quit()
if args.mc_directory == None:
    if config.get('Paths','minecraft-mod-folder') != "default":
        if os.path.isdir(config.get('Paths','minecraft-mod-folder')) != True:
            print("The minecraft mod folder path in the configuration isn't valid or doesn't exist.")
            quit()
if args.cache_folder == None:
    if config.get('Paths','cache-folder') != "NOT_SET":
        if os.path.isdir(config.get('Paths','cache-folder')) != True:
            print("The cache path in the configuration isn't given.")
            quit()
    elif config.get('Paths','cache-folder') == "NOT_SET":
        print("The cache path in the configuration isn't given.")
        quit()
# @Nitro4542 pls fix
#if config.get('General','operating-system') != "Windows":
#    print('Please check your configuration at operating-system.')
#    quit()
#elif config.get('General','operating-system') != "Linux":
#    print('Please check your configuration at operating-system.')
#    quit()

# Set mod folder path
if args.mc_directory != None:
    mc_mod_folder = args.mc_directory
elif config.get('Paths','minecraft-mod-folder') != "default":
    mc_mod_folder = config.get('Paths','minecraft-mod-folder')
else:
    if config.get('General','operating-system') == "Windows":
        mc_mod_folder = os.getenv('APPDATA')+"\\.minecraft\\mods"
    elif config.get('General','operating-system') == "Linux":
        mc_mod_folder = os.getenv('HOME')+"/.minecraft/mods"

# Generates a random string
# Needed for some functions to work properly
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

# Function to cache your mod pack
def cache_mod_pack(cache_dest):
# Create folder for zip file + Check configuration
    if cache_dest != None:
        if os.path.isdir(cache_dest) == True:
            final_destination = cache_dest + "\\" + datetime.today().strftime('%Y-%m-%d') + "_" +randomword(5)
        else:
            print("The cache path given isn't valid or doesn't exist.")
            quit()
    elif args.cache_folder == None:
        if config.get('Paths','cache-folder') != "NOT_SET":
            if os.path.isdir(config.get('Paths','cache-folder')) == True:
                final_destination = config.get('Paths','cache-folder') + "\\" + datetime.today().strftime('%Y-%m-%d') + "_" +randomword(5)
            else:
                print("The cache path in the configuration isn't valid or doesn't exist.")
                quit()
    elif args.cache_folder != None:
        if os.path.isdir(args.cache_folder) == True:
            final_destination = args.cache_folder + "\\" + datetime.today().strftime('%Y-%m-%d') + "_" +randomword(5)
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
def create_backup():
    # Get and add backup name to destination and create folder if neccessary
    if config.get('Paths','default-backup-path') == "NOT_SET":
        final_destination = args.destination+"\\"+"mod-backup-"+datetime.today().strftime('%Y-%m-%d')+ "_" +randomword(5)
    else:
        final_destination = config.get('Paths','default-backup-path')+"\\"+"mod-backup-"+datetime.today().strftime('%Y-%m-%d')+ "_" +randomword(5)
    if os.path.isdir(final_destination) != True:
        os.mkdir(final_destination)
    # Create backup
    src_files = os.listdir(mc_mod_folder)
    for file_name in src_files:
        full_file_name = os.path.join(mc_mod_folder, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy2(full_file_name, final_destination)

# Deletes all mods in mods folder
def delete_mods():
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
    if answer0.lower() in ["y","yes"]:
        create_backup()
    elif answer0.lower() in ["n","no"]:
        print('Won\'t create backup')
    else:
        print('Only \"y\" or \"n\" are allowed. Try again.')
        confirm_prompt()
    answer = input("Continue? - All of your mods are beeing erased! [Y|N]: ")
    if answer.lower() in ["y","yes"]:
        delete_mods()
    elif answer.lower() in ["n","no"]:
        quit()
    else:
        print('Only \"y\" or \"n\" are allowed. Try again.')
        confirm_prompt()

# Copies mods in your mods folder
def install_mods(src):
# Set + check source folder path
    if src == None:
        src = args.source
    if os.path.isdir(src) != True:
        print("The source path isn't valid or doesn't exist.")
        quit()
# Copies all contents of selected folder in mods folder
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy2(full_file_name, mc_mod_folder)

# Run selected command
if args.command == "prepare":
    cache_mod_pack(None)
elif args.command == "backup":
    create_backup()
elif args.command == "remove":
    if args.silent == True:
        delete_mods()
    elif args.silent != True:
        confirm_prompt()
elif args.command == "install":
    install_mods(None)