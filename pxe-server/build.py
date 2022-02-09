#!/usr/bin/python3
# -*- coding: utf-8 -*-

from config import *

import os.path
import glob
import shutil
import requests
import apt
import sys

# Error check
def abort(err):
    print('Error: ' + err)
    exit(1)

# Check requiered dependencies
def check_deps(dependencies):
    for name in dependencies:        
        cache = apt.Cache()
        cache.update()
        cache.open()
        if cache[name].is_installed:
            print ("[+] Found installed package: " + name)
        else:
            print ("[-] Missing dependency: " + name)
            print ("[+] Attempting to install...")
            name.mark_install()
            try:
                cache.commit()
            except Exception as arg:
                print >> sys.stderr, "Sorry, package installation failed [{err}]".format(err=str(arg))

# Main function
def main():
    check_deps(dependencies)


# Run programm
if __name__ == '__main__':
    main()
