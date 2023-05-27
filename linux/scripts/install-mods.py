import argparse
import os
import shutil
from configparser import ConfigParser

# Load configuration
config = ConfigParser()
config.read('config.ini')

# Arguments
parser = argparse.ArgumentParser(prog='nitro-mc-mod-installer',description='Instantly install a whole Minecraft mod pack')
parser.add_argument("-s", dest = "source", help="source folder path",required=True, default=None)
parser.add_argument("-md", dest = "mc_directory", help="minecraft directory (will use path from config.ini if not given)", required=False, default=None)
args = parser.parse_args()

# Check configuration if -md isn't used
if os.path.isdir(args.source) != True:
        print("The source path isn't valid or doesn't exist.")
        quit()
if args.mc_directory == None:
    if config.get('Paths','minecraft-mod-folder') != "default":
        if os.path.isdir(config.get('Paths','minecraft-mod-folder')) != True:
            print("The minecraft mod folder path in the configuration isn't valid or doesn't exist.")
            quit()

def install_mods(src):
# Set mod and source mod pack folder path
    if src == None:
        if args.source != None:
            src = args.source
        else:
            print('Error: Please provide a valid mod pack source.')
            quit()
    if os.path.isdir(src) != True:
        print("The source path isn't valid or doesn't exist.")
        quit()
    if config.get('Paths','minecraft-mod-folder') != "default":
        final_destination = config.get('Paths','minecraft-mod-folder')
    else:
        final_destination = os.getenv('HOME')+"/.minecraft/mods"

# Copy all contents of selected folder into mods folder
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy2(full_file_name, final_destination)

# Run install process
install_mods(None)