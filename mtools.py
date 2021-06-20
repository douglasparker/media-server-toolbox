#!/usr/bin/env python3

import argparse
# from colorama import init, Fore, Back, Style
from datetime import datetime
import locale
import sys
from modules.core import repair, stats

PATH_LIBRARY_DB = "/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db"

class application:
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

        parser = argparse.ArgumentParser(description="Media Server Toolbox provides a set of utilities that are useful for maintaining your media server.", formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("module", type=str, help="""The module that you'd like to run from the toolbox.

stats - Output statistics about your media library
repair - Repair file permissions for your media library""")
        parser.add_argument("-a", "--application", metavar="{PLEX,EMBY,JELLYFIN}", type=str, default="plex", choices=["plex", "emby", "jellyfin"], help="Choose the media server you want to pull data from.")
        parser.add_argument("-t", "--test", metavar="BOOL", type=bool, default=True, help="This is just a argument for debugging purposes.")
        parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output for more technical information.")
        parser.add_argument("-V", "--version", metavar="", type=bool, help="")
        args = parser.parse_args()

        if(args.module == "stats"):
            if(stats().get_stats(args, PATH_LIBRARY_DB)):
                sys.exit(0)
            else:
                print("There was an error when using this module.")
                sys.exit(1)
        
        elif(args.module == "repair"):
            repair().file_permissions()

        else:
            print(args.module + " is not a valid module.")
            sys.exit(1)

application().main()