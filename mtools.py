#!/usr/bin/env python3

import argparse
# from colorama import init, Fore, Back, Style
from datetime import datetime
import locale
import os
import sys
from modules.core import repair, stats

PATH_LIBRARY_DB = "/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db"

class application:
    name = "Media Server Toolbox"
    description = "{self.name} provides a set of utilities that are useful for maintaining your media server."
    verbose = False
    def __init__(self):
        locale.setlocale(locale.LC_ALL, '')
        # init() # Initializes colorama
        for v in sys.argv:
            if(v == "--verbose" or v == "-v"): self.verbose = True

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
            stats().get_stats(PATH_LIBRARY_DB, self.verbose)
            sys.exit(0)
        
        elif(sys.argv[1] == "repair"):
            if(len(sys.argv) <= 2):
                print("You need to pass an argument to use the repair module.")

            elif(sys.argv[2] == "--repair-file-permissions"):
                repair().file_permissions()

            else:
                print(sys.argv[2] + " is not a valid argument for the repair module.")

        elif(len(sys.argv) <= 1 or sys.argv[1] == "--help" or sys.argv[1] == "-h"):
            print(f"""
{self.name}: {self.description}

usage: {os.path.basename(sys.argv[0])} <service> <--argument, -a>

{os.path.basename(sys.argv[0])} stats --application, -a plex,emby,jellyfin    Output statistics about your media library
{os.path.basename(sys.argv[0])} repair --repair-file-permissions              Repair file permissions for your media library
{os.path.basename(sys.argv[0])} --version, -V                                 Output the {self.name} version number.
{os.path.basename(sys.argv[0])} --help, -h                                    Output this help message.
""")
            sys.exit(1)

application().main()