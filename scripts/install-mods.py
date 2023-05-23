import argparse
import os
import shutil

# Arguments
parser = argparse.ArgumentParser(prog='nitro-mc-mod-installer',description='Instantly install a whole Minecraft mod pack')
parser.add_argument("-d", dest = "destination", help="source folder destination",required=True)
args = parser.parse_args()

# Copy all content of selected folder into mods folder
src = args.destination
final_destination = os.getenv('APPDATA')+"\\.minecraft\\mods"
src_files = os.listdir(src)
for file_name in src_files:
    full_file_name = os.path.join(src, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy2(full_file_name, final_destination)