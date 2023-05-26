import argparse
import os
import shutil
import random, string
from datetime import datetime
from configparser import ConfigParser

# Load configuration
config = ConfigParser()
config.read('config.ini')

# Prepare random function
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

# Arguments
parser = argparse.ArgumentParser(prog='nitro-mc-mod-backup',description='Backup current Minecraft mods')
parser.add_argument("-d", dest = "destination", help="backup destination (will use path from config.ini if not given)", required=False, default=None)
parser.add_argument("-md", dest = "mc_directory", help="minecraft directory (will use path from config.ini if not given)", required=False, default=None)
args = parser.parse_args()

# Check configuration if -d or -md aren't used
if args.destination == None:
    if config.get('Paths','default-backup-path') != "NOT_SET":
        if os.path.isdir(config.get('Paths','default-backup-path')) != True:
            print("The backup path in the configuration isn't valid or doesn't exist.")
            quit()
if args.mc_directory == None:
    if config.get('Paths','minecraft-mod-folder') != "default":
        if os.path.isdir(config.get('Paths','minecraft-mod-folder')) != True:
            print("The minecraft mod folder path in the configuration isn't valid or doesn't exist.")
            quit()

# Get and add backup name to destination and create folder if neccessary
if config.get('Paths','default-backup-path') == "NOT_SET":
    final_destination = args.destination+"\\"+"mod-backup-"+datetime.today().strftime('%Y-%m-%d')+ "_" +randomword(5)
else:
    final_destination = config.get('Paths','default-backup-path')+"\\"+"mod-backup-"+datetime.today().strftime('%Y-%m-%d')+ "_" +randomword(5)
if os.path.isdir(final_destination) != True:
    os.mkdir(final_destination)

# Set mod folder path
if args.mc_directory != None:
    src1 = args.mc_directory
elif config.get('Paths','minecraft-mod-folder') != "default":
    src1 = config.get('Paths','minecraft-mod-folder')
else:
    src1 = os.getenv('APPDATA')+"\\.minecraft\\mods"

# Copy all content of mods folder into backup destination
def create_backup(src):
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy2(full_file_name, final_destination)

# Run backup
create_backup(src1)