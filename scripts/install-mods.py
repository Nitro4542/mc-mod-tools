import argparse
import os
import shutil
from configparser import ConfigParser

# Load configuration
config = ConfigParser()
config.read('config.ini')

# Arguments
parser = argparse.ArgumentParser(prog='nitro-mc-mod-installer',description='Instantly install a whole Minecraft mod pack')
parser.add_argument("-d", dest = "destination", help="source folder destination",required=True, default=None)
parser.add_argument("-md", dest = "mc_directory", help="minecraft directory (will use path from config.ini if not given)", required=False, default=None)
args = parser.parse_args()

# Check configuration if -d or -md aren't used
if args.destination != None:
    if config.get('Paths','default-backup-path') != "NOT_SET":
        if os.path.isdir(config.get('Paths','default-backup-path')) != True:
            print("The backup path in the configuration isn't valid or doesn't exist.")
            quit()
if args.mc_directory != None:
    if config.get('Paths','minecraft-mod-folder') != "default":
        if os.path.isdir(config.get('Paths','minecraft-mod-folder')) != True:
            print("The minecraft mod folder path in the configuration isn't valid or doesn't exist.")
            quit()

# Set mod and source mod pack folder path
src = args.destination
if config.get('Paths','minecraft-mod-folder') != "default":
    final_destination = config.get('Paths','minecraft-mod-folder')
else:
    final_destination = os.getenv('APPDATA')+"\\.minecraft\\mods"

# Copy all content of selected folder into mods folder
src_files = os.listdir(src)
for file_name in src_files:
    full_file_name = os.path.join(src, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy2(full_file_name, final_destination)