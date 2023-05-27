# About this project

This is an installer for my Minecraft mod format.  
I created this project for people who don't know how to install mods, and for those who don't want to use a third party launcher and want a safe, ad-free and crap-free tool.  
Please note that this tool is currently only available for Windows and Linux. I'll probably release it for MacOS later.

## How does it work?

For now, you'll need to use the scripts in your terminal.

### backup-mods.py

Use this to backup your existing mods.  
Syntax:  

```bash
\$ python backup-mods.py <arguments>
```

The following arguments are allowed:  
`-h` for help.  
`-d <DESTINATION>` for the backup destination. If not specified, the path from the configuration will be used.  
`-md <MC_DIRECTORY>` for the mods folder inside .minecraft. If not specified, it will use the path given in the configuration.  

### install-mods.py

Use this to install mods.  
Syntax:  

```bash
\$ python install-mods.py <arguments>
```

The following arguments are allowed:  
`-h` for help.  
`-s <SOURCE>` for the source folder. Everything in it will be copied. This is needed to run this command.  
`-md <MC_DIRECTORY>` for the mods folder inside .minecraft. If not specified, it will use the path given in the configuration.  

### prepare-mod-pack.py

Use this to extract a mod pack.  
Syntax:  

```bash
\$ python prepare-mod-pack.py <arguments>
```

The following arguments are allowed:  
`-h` for help.  
`-p <PACK>` for the zip file. If not specified, the path from the configuration will be used.  
`-c <CACHE_FOLDER>` for the cache folder. If not specified, it will use the path given in the configuration.  

### remove-mods.py

Use this to remove all existing mods.  
Syntax:  

```bash
\$ python remove-mods.py <arguments>
```

The following arguments are allowed:  
`-h` for help.  
`-s` for silent mode. All prompts will be skipped and you won't be able to make a backup.
`-md <MC_DIRECTORY>` for the mods folder inside .minecraft. If not specified, it will use the path specified in the configuration.  

## How do I create mod packs for it?

I'm going to make a tool for that. For now, you'll have to do it manually.

## Configuration

Inside the config.ini file in the scripts folder you'll find the default configuration:  

```ini
[Paths]
default-backup-path = NOT_SET
minecraft-mod-folder = default
cache-folder = NOT_SET
```

All explained:  
`default-backup-path` is the path where all your backups will be stored.  
`minecraft-mod-folder` is the mods folder inside your .minecraft folder. Defaults to %appdata%\\.minecraft\mods.  
`cache-folder` is the folder where all your mod packs will be cached.  
  
I would recommend that you configure everything to your needs.

## File structure explained

Just put your mods inside the zip file.
For now, please only include .jar files inside the zip file.
