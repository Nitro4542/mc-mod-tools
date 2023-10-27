"""A module for managing Minecraft mods"""
import argparse
import os
import random
import shutil
import string
import sys
from configparser import ConfigParser
from datetime import datetime
from zipfile import ZipFile


def randomword(length):
    """Generates a random string"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


class ModTools:
    """Tools for managing Minecraft mods"""
    def __init__(self):
        # Load configuration
        self.config = ConfigParser()
        self.config.read('config.ini')

        # Parse command line arguments
        self.parse_arguments()

    def parse_arguments(self):
        """Set arguments when the file runs as a script, but not when it's imported as a module"""
        if __name__ == "__main__":
            parser = argparse.ArgumentParser(prog='nitro_mc_mod_tools',
                                             description='Toolbox for Nitro\'s Minecraft mod pack format')
            parser.add_argument('command',
                                help="Select which command is going to be run", default=None)
            parser.add_argument("-d", dest="destination",
                                help="backup destination (will use path from config.ini if not given)",
                                required=False, default=None)
            parser.add_argument("-md", dest="mc_directory",
                                help="minecraft directory (will use path from config.ini if not given)",
                                required=False, default=None)
            parser.add_argument("-p", dest="pack",
                                help="path to mod pack",
                                required=False, default=None)
            parser.add_argument("-c", dest="cache_folder",
                                help="cache folder",
                                required=False, default=None)
            parser.add_argument("-s", dest="source",
                                help="source folder path",
                                required=False, default=None)
            parser.add_argument("-q", dest="quiet",
                                help="use to skip confirmation & backup prompt",
                                required=False, default=False, action='store_true')
            self.args = parser.parse_args()
            # Check arguments if set
            if self.args.destination is not None:
                if not os.path.isdir(self.args.destination):
                    print("The backup path given isn't valid or doesn't exist.")
                    sys.exit(1)
            if self.args.mc_directory is not None:
                if not os.path.isdir(self.args.mc_directory):
                    print("The backup path given isn't valid or doesn't exist.")
                    sys.exit(1)
            if self.args.cache_folder is not None:
                if not os.path.isdir(self.args.cache_folder):
                    print("The backup path given isn't valid or doesn't exist.")
                    sys.exit(1)
            if self.args.source is not None:
                if not os.path.isdir(self.args.source):
                    print("The backup path given isn't valid or doesn't exist.")
                    sys.exit(1)

    def get_mod_folder(self, modfolder_input):
        """Sets the mod folder path"""
        if modfolder_input is not None:
            mod_folder = modfolder_input
        elif __name__ == "__main__" and self.args.mc_directory is not None:
            mod_folder = self.args.mc_directory
        elif self.config.get('Paths', 'minecraft-mod-folder') != "default":
            mod_folder = self.config.get('Paths', 'minecraft-mod-folder')
        else:
            if self.config.get('General', 'operating-system') == "Windows":
                mod_folder = os.getenv('APPDATA') + "\\.minecraft\\mods"
            elif self.config.get('General', 'operating-system') == "Linux":
                mod_folder = os.getenv('HOME') + "/.minecraft/mods"
        return mod_folder

    def get_backup_folder(self, backupfolder_input):
        """Sets the backup folder path"""
        if self.config.get('Paths', 'default-backup-path') == "default":
            backup_path = "Backups"
            # Creates folder if it doesn't exist
            if not os.path.isdir(backup_path):
                os.mkdir(backup_path)
        else:
            if backupfolder_input is not None:
                backup_path = backupfolder_input
            elif __name__ == "__main__" and self.args.destination is not None:
                backup_path = self.args.destination
            elif self.config.get('Paths', 'default-backup-path') != "default":
                backup_path = self.config.get('Paths', 'default-backup-path')
        return backup_path

    def get_cache_folder(self, cachefolder_input):
        """Sets the cache folder path"""
        if self.config.get('Paths', 'cache-folder') == "default":
            cache_path = "Cache"
            # Creates folder if it doesn't exist
            if not os.path.isdir(cache_path):
                os.mkdir(cache_path)
        else:
            if cachefolder_input is not None:
                cache_path = cachefolder_input
            elif __name__ == "__main__" and self.args.cache_folder is not None:
                cache_path = self.args.cache_folder
            elif self.config.get('Paths', 'cache_folder') != "default":
                cache_path = self.config.get('Paths', 'cache_folder')
        return cache_path

    def unzip_mod_pack(self, cache_dest, zipfile_path):
        """Function to unzip a mod pack"""
        # Create folder for zip file + Check configuration
        if cache_dest is not None:
            if os.path.isdir(cache_dest):
                final_destination = (cache_dest + "\\" + datetime.today().strftime('%Y-%m-%d') + "_" +
                                     randomword(5))
        else:
            final_destination = (self.get_cache_folder(None) + "\\" + datetime.today().strftime('%Y-%m-%d')
                                 + "_" + randomword(5))
        if not os.path.isdir(final_destination):
            os.mkdir(final_destination)
        # Extract zip file
        if cache_dest is not None:
            with ZipFile(zipfile_path, 'r') as zipobject:
                zipobject.extractall(
                    path=final_destination)
            zipobject.close()
        elif self.args.cache_folder is not None:
            with ZipFile(self.args.pack, 'r') as zipobject:
                zipobject.extractall(
                    path=final_destination)
            zipobject.close()
        return final_destination

    def create_backup(self, backup_dest):
        """Creates a backup of mods folder"""
        mc_mod_folder = self.get_mod_folder(None)
        # Create folder for backup
        if backup_dest is not None:
            if os.path.isdir(backup_dest):
                final_destination = (backup_dest + "\\" + datetime.today().strftime('%Y-%m-%d') + "_" +
                                     randomword(5))
            else:
                print("The backup path given isn't valid or doesn't exist.")
                sys.exit(1)
        # Get and add backup name to destination and create folder if necessary
        else:
            final_destination = (self.get_backup_folder(None) + "\\" + "mod-backup-" +
                                 datetime.today().strftime('%Y-%m-%d') + "_" + randomword(5))
        if not os.path.isdir(final_destination):
            os.mkdir(final_destination)
        # Create backup
        src_files = os.listdir(mc_mod_folder)
        for file_name in src_files:
            full_file_name = os.path.join(mc_mod_folder, file_name)
            if os.path.isfile(full_file_name) and file_name.endswith('.jar'):
                shutil.copy2(full_file_name, final_destination)

    def delete_mods(self):
        """Deletes all mods in mods folder"""
        mc_mod_folder = self.get_mod_folder(None)
        for filename in os.listdir(mc_mod_folder):
            file_path = os.path.join(mc_mod_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except OSError:
                print("An exception occurred")

    def confirmation_prompt(self):
        """Confirmation prompt for delete_mods()"""
        answer0 = input("Do you want to create a backup of your existing mods? [Y|N]")
        if answer0.lower() in ["y", "yes"]:
            self.create_backup(None)
        elif answer0.lower() in ["n", "no"]:
            print('Won\'t create backup')
        else:
            print('Only \"y\" or \"n\" are allowed. Try again.')
            self.confirmation_prompt()
        answer = input("Continue? - All of your mods are being erased! [Y|N]: ")
        if answer.lower() in ["y", "yes"]:
            self.delete_mods()
        elif answer.lower() in ["n", "no"]:
            sys.exit(0)
        else:
            print('Only \"y\" or \"n\" are allowed. Try again.')
            self.confirmation_prompt()

    def install_mods(self, src):
        """Copies mods to your mods folder"""
        mc_mod_folder = self.get_mod_folder(None)
        # Set + check the source folder path
        if src is None:
            src = self.args.source
        if not os.path.isdir(src):
            print("The source path isn't valid or doesn't exist.")
            sys.exit(1)
        # Copies all contents of selected folder in mods folder
        src_files = os.listdir(src)
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if os.path.isfile(full_file_name) and file_name.endswith('.jar'):
                shutil.copy2(full_file_name, mc_mod_folder)

    def install_mods_zip(self, zipfile_path):
        """Extracts a zip file containing mods to the mods folder"""
        mc_mod_folder = self.get_mod_folder(None)
        # Extract zip file
        with ZipFile(zipfile_path, 'r') as zipobject:
            for file_info in zipobject.infolist():
                if file_info.filename.endswith('.jar'):
                    zipobject.extract(file_info, path=mc_mod_folder)
        zipobject.close()

    def check_config(self):
        """Checks config.ini for any errors"""
        if self.config.get('Paths', 'default-backup-path') != "default":
            if not os.path.isdir(self.config.get('Paths', 'default-backup-path')):
                print("The backup path in the configuration isn't valid or doesn't exist.")
                sys.exit(1)
        if self.config.get('Paths', 'minecraft-mod-folder') != "default":
            if not os.path.isdir(self.config.get('Paths', 'minecraft-mod-folder')):
                print(
                    "The minecraft mod folder path in the configuration isn't valid or doesn't exist.")
                sys.exit(1)
        if self.config.get('Paths', 'cache-folder') != "default":
            if not os.path.isdir(self.config.get('Paths', 'cache-folder')):
                print("The cache path in the configuration isn't given.")
                sys.exit(1)
        if (self.config.get('General', 'operating-system') != "Windows" and
                self.config.get('General', 'operating-system') != "Linux"):
            print('Please check your configuration at operating-system.')
            sys.exit(1)

    def main(self):
        """Main function when the file runs as a script,
        but not when it's imported as a module"""
        if __name__ == "__main__":
            if self.args.command == "prepare":
                self.unzip_mod_pack(None, None)
            elif self.args.command == "backup":
                self.create_backup(None)
            elif self.args.command == "remove":
                if self.args.quiet:
                    self.delete_mods()
                elif not self.args.quiet:
                    self.confirmation_prompt()
            elif self.args.command == "install":
                self.install_mods(None)
            else:
                print('Please provide a valid command.')
                sys.exit(2)


# Create an instance of the ModTools class and run the main function
if __name__ == "__main__":
    tools = ModTools()
    tools.main()
