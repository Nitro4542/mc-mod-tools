import argparse
import os
from zipfile import ZipFile

# Arguments
parser = argparse.ArgumentParser(prog='nitro-mc-mod-info',description='Get mod pack info from mods.zip format')
parser.add_argument("-f", dest = "file", help="location of mods.zip")
args = parser.parse_args()

# Create folders
if os.path.isdir("%temp%\\nitro-mc-mod-installer") != True:
    os.mkdir("%temp%\\nitro-mc-mod-installer")
if os.path.isdir("%temp%\\nitro-mc-mod-installer\\info") != True:
    os.mkdir("%temp%\\nitro-mc-mod-installer\\info")

# Check if zip file is specified
if args.file is not None:
# Extract info.txt from zip file
    with ZipFile(args.file, 'r') as zipobject: 
        zipobject.extract(
            "info.txt", path="%temp%\\nitro-mc-mod-installer\\info")
    zipobject.close()
    open("%temp%\\nitro-mc-mod-installer\\info\\info.txt")