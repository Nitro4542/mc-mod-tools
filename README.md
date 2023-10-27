<div align="center">
  <img width="192" height="192" alt="logo" src="assets/mc-mod-tools.png">
  <h1>mc-mod-tools</h1>
  <p>A tool to manage your Minecraft mods</p>
</div>

## About

I created this project for people who don't know how to install mods, and for those who don't want to use a third party launcher or those who want a safe, ad-free and crap-free tool.  
Please note that this tool is currently only available for Windows and Linux. I will release it for macOS later.

## Installation

Download the mc-mod-tools.zip file from the [latest release](https://github.com/Nitro4542/mc-mod-tools/releases) and run the GUI version or use the terminal version.

For the GUI to work, you need to install the requirements from the [requirements.txt](requirements.txt) file:
```bash
pip install -r requirements.txt
```

## How does it work?

For now, you need to use the script in your terminal or the GUI.  

### mc_mod_tools.py

This script contains everything you need to run it inside a terminal. The GUI is based on this script.  
Syntax:  

```bash
python mc_mod_tools.py <COMMAND> -d DESTINATION -md MC_DIRECTORY -p PACK -c CACHE_FOLDER -s SOURCE -q -h
```

The following arguments can be used:  
`-h` for help.  
`-d DESTINATION` for the backup destination. If not specified, the path from the configuration will be used.  
`-md MC_DIRECTORY` for the mods folder inside .minecraft. If not specified, the path from the configuration will be used.  
`-p PACK` for the zip file.  
`-c <CACHE_FOLDER>` for the cache folder. If not specified, it will use the path given in the configuration.  
`-s <SOURCE>` for the source folder. Everything in it will be copied. This is needed to run the install-command.  
`-q` for silent mode. All prompts will be skipped, but you won't be able to make a backup.

### mc_mod_gui.py

The GUI should be easy to understand for everyone.

### Configuration

Inside the config.ini file in the scripts folder you will find the default configuration:  

```ini
[Paths]
default-backup-path = default
minecraft-mod-folder = default
cache-folder = default

[General]
operating-system = Windows

[DONT-TOUCH]
version = <VERSION>
```

Options explained:  
`default-backup-path` is the path where all your backups will be stored. By default, it creates a folder inside the folder, where the script is placed, called "Backups".  
`minecraft-mod-folder` is the mods folder inside your .minecraft folder. Defaults to .minecraft/mods.  
`cache-folder` is the folder where all your unzipped mod packs will be placed and cached. By default, it creates a folder inside the folder, where the script is placed, called "Cache".  
`operating-system` is your operating system. Set it either to "Windows" or "Linux" (without the quotes).  
`version` tells the program the version number. It is recommended to not mess with it.
  
If you want to, you can change everything to your needs.

## How do I create mod packs for it?

I'm going to make a tool for that. For now, you have to do it manually.

### What does a mod pack consist of?

Put your mods **and nothing else** inside the zip file.  
This means no extra files or folders.  

## Contributing

When it comes to contributing to the project, the two main things you can do are reporting bugs and submitting pull requests.  

I'm new to Python programming, so any kind of help is appreciated.  
I'd also love to hear every single one of your ideas for this project.  
