#!/usr/bin/env python3

import argparse
# from colorama import init, Fore, Back, Style
from datetime import datetime
import locale
import sys
from modules.core import repair, stats

PATH_LIBRARY_DB = "/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db"

class application:
    name = "Media Server Toolbox"
    description = "{self.name} provides a set of utilities that are useful for maintaining your media server."
    def __init__(self):
        locale.setlocale(locale.LC_ALL, '')
        # init() # Initializes colorama

    def main(self):
        print(r"""
__  __        _ _        ___                        _____         _ _             
|  \/  |___ __| (_)__ _  / __| ___ _ ___ _____ _ _  |_   _|__  ___| | |__  _____ __
| |\/| / -_) _` | / _` | \__ \/ -_) '_\ V / -_) '_|   | |/ _ \/ _ \ | '_ \/ _ \ \ /
|_|  |_\___\__,_|_\__,_| |___/\___|_|  \_/\___|_|     |_|\___/\___/_|_.__/\___/_\_\
                                                                                    
""")
        print("Media Server Toolbox")
        print("""Copyright 2020-""" + str(datetime.now().year) + """, Douglas Parker
https://www.douglas-parker.com, https://git.douglas-parker.com/douglasparker\n""")
        
        if(sys.argv[1] == "stats"):
            if(stats().get_stats(args, PATH_LIBRARY_DB)):
                sys.exit(0)
            else:
                print("There was an error when using this module.")
                sys.exit(1)
        
        elif(sys.argv[1] == "repair"):
            repair().file_permissions()

        elif(len(sys.argv) < 2 or sys.argv[1] == "--help" or sys.argv[1] == "-h"):
            print(f"""
{self.name}: {self.description}

usage: {sys.argv[0]} <service> <--argument, -a>

{sys.argv[0]} stats --application, -a plex,emby,jellyfin    Output statistics about your media library
{sys.argv[0]} repair --repair-file-permissions              Repair file permissions for your media library
{sys.argv[0]} --version, -V                                 Output the {self.name} version number.
{sys.argv[0]} --help, -h                                    Output this help message.
""")
            sys.exit(1)

application().main()