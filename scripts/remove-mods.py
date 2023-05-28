import argparse
import os
import shutil
from configparser import ConfigParser

# Load configuration
config = ConfigParser()
config.read('config.ini')

# Arguments
parser = argparse.ArgumentParser(prog='nitro-mc-mod-remover',description='Instantly remove all of your Minecraft mods')
parser.add_argument("-md", dest = "mc_directory", help="minecraft directory (will use path from config.ini if not given)", required=False, default=None)
parser.add_argument("-s", dest = "silent", help = "use to skip confirmation & backup prompt", required=False, default=False, action='store_true')
args = parser.parse_args()

# Check configuration
if args.mc_directory != None:
    if os.path.isdir(args.mc_directory) != True:
            print("The source path isn't valid or doesn't exist.")
            quit()
elif args.mc_directory == None:
    if config.get('Paths','minecraft-mod-folder') != "default":
        if os.path.isdir(config.get('Paths','minecraft-mod-folder')) != True:
            print("The minecraft mod folder path in the configuration isn't valid or doesn't exist.")
            quit()

# Set mod folder path
if args.mc_directory != None:
    folder = args.mc_directory
elif config.get('Paths','minecraft-mod-folder') != "default":
    folder = config.get('Paths','minecraft-mod-folder')
else:
    if config.get('General','operating-system') == "Windows":
        folder = os.getenv('APPDATA')+"\\.minecraft\\mods"
    elif config.get('General','operating-system') == "Linux":
        folder = os.getenv('HOME')+"/.minecraft/mods"
    else:
        print('Please check your configuration at operating-system.')
        quit()

# Deletes all mods in mods folder
def delete_mods():
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# Define confirmation prompt
def confirm_prompt():
    answer0 = input("Do you want to create a backup of your existing mods? [Y|N]")
    if answer0.lower() in ["y","yes"]:
        os.system("python backup-mods.py")
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

# Run confirmation if -s isn't used
if args.silent == False:
    confirm_prompt()
elif args.silent == True:
    delete_mods()