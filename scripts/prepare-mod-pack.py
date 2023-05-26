import argparse
import os
import shutil
import random, string
from configparser import ConfigParser
from zipfile import ZipFile
from datetime import datetime

# Prepare random function
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

# Load configuration
config = ConfigParser()
config.read('config.ini')

# Arguments
parser = argparse.ArgumentParser(prog='nitro-mc-mod-prepare',description='Prepare a mod pack')
parser.add_argument("-p", dest = "pack", help="path to mod pack", required=True, default=None)
parser.add_argument("-c", dest = "cache_folder", help="cache folder", required=False, default=None)
args = parser.parse_args()

# Check configuration
if args.cache_folder == None:
    if config.get('Paths','cache-folder') != "NOT_SET":
        if os.path.isdir(config.get('Paths','cache-folder')) != True:
            print("The cache path in the configuration isn't valid or doesn't exist.")
            quit()
    if config.get('Paths','cache-folder') == "NOT_SET":
        print("The cache path in the configuration isn't given.")
        quit()

# Create folder for zip file
if args.cache_folder == None:
    if config.get('Paths','cache-folder') != "NOT_SET":
        if os.path.isdir(config.get('Paths','cache-folder')) == True:
            final_destination = config.get('Paths','cache-folder') + "\\" + datetime.today().strftime('%Y-%m-%d') + "-" +randomword(5)
else:
    final_destination = args.cache_folder + "\\" + datetime.today().strftime('%Y-%m-%d') + randomword(5)

# Extract zip file
with ZipFile(args.pack, 'r') as zipobject: 
    zipobject.extractall(
        path=final_destination)
zipobject.close()