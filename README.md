# About this project

This is a toolbox for my Minecraft mod format.  
I created this project for people who don't know how to install mods, and for those who don't want to use a third party launcher and want a safe, ad-free and crap-free tool.  
Please note that this tool is currently only available for Windows and Linux. I'll probably release it for MacOS later.

## How does it work?

For now, you'll need to use the script in your terminal.

### mc-mod-tools.py

This script contains everything you need in a single script.  
Syntax:  

```bash
python mc-mod-tools.py <COMMAND> -d DESTINATION -md MC_DIRECTORY -p PACK -c CACHE_FOLDER -s SOURCE -q -h
```

The following arguments are allowed:  
`-h` for help.  
`-d DESTINATION` for the backup destination. If not specified, the path from the configuration will be used.  
`-md MC_DIRECTORY` for the mods folder inside .minecraft. If not specified, the path from the configuration will be used.  
`-p PACK` for the zip file.  
`-c <CACHE_FOLDER>` for the cache folder. If not specified, it will use the path given in the configuration.  
`-s <SOURCE>` for the source folder. Everything in it will be copied. This is needed to run the install command.  
`-q` for silent mode. All prompts will be skipped and you won't be able to make a backup.

### Configuration

Inside the config.ini file in the scripts folder you'll find the default configuration:  

```ini
[Paths]
default-backup-path = NOT_SET
minecraft-mod-folder = default
cache-folder = NOT_SET

[General]
operating-system = Windows
```

Options explained:  
`default-backup-path` is the path where all your backups will be stored.  
`minecraft-mod-folder` is the mods folder inside your .minecraft folder. Defaults to .minecraft/mods.  
`cache-folder` is the folder where all your mod packs will be cached.  
`operating-system` is your operating system. Set it either to "Windows" or "Linux" (without the quotes).  
  
I would recommend that you configure everything to suit your needs.  

## How do I create mod packs for it?

I'm going to make a tool for that. For now, you'll have to do it manually.

## What does a mod pack consist of?

Just put your mods inside the zip file.
For now, please only include .jar files inside the zip file.
