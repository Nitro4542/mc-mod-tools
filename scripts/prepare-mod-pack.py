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
            print("The cache path in the configuration isn't given.")
            quit()
    elif config.get('Paths','cache-folder') == "NOT_SET":
        print("The cache path in the configuration isn't given.")
        quit()

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

# Run function
cache_mod_pack(None)