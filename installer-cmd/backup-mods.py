import argparse
import os
import shutil
from datetime import datetime

# Arguments
parser = argparse.ArgumentParser(prog='nitro-mc-mod-backup',description='Backup current Minecraft mods')
parser.add_argument("-d", dest = "destination", help="backup destination",required=True)
args = parser.parse_args()

# Add backup name to destination and create folder
final_destination = args.destination+"\\"+"mod-backup-"+datetime.today().strftime('%Y-%m-%d')
if os.path.isdir(final_destination) != True:
    os.mkdir(final_destination)

# Copy all content of mods folder into backup destination
src = os.getenv('APPDATA')+"\\.minecraft\\mods"
src_files = os.listdir(src)
for file_name in src_files:
    full_file_name = os.path.join(src, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy2(full_file_name, final_destination)