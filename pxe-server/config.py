#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import os
import subprocess
from pathlib import Path

# Variables
# Building dependencies
dependencies        = [ "build-essential", "curl", "wget", "make", "autoconf", "tar", "gzip", "gawk", "pkg-config", "bison", "flex", "python3", \
                        "libdevmapper-dev", "libfcft-dev", "libfreetype-dev", "libfuse-dev", "libzfslinux-dev", "liblzma-dev", "libzmat1-dev", \
                        "net-tools" ]
# PXE options
options             = [ "install", "live", "preseed", "scripts" ]
# FTP server options
ftp_adress          = "$server/ssd1"
ftp_login           = "ftp"
ftp_pass            = "pa$$w0rd"
# TFTP server options
tftp_address        = "$server"
tftp_boot_folder    = "boot"
tftp_files_folder   = "files"
# USER account options
user_name           = "flypatriot"
user_pass           = "pa$$w0rd"
# ROOT account options
root_pass           = "pa$$w0rd"
# List of OS
os_list             = [ "debian", "kali" ]

# Debian URLs
debian = {}
debian["name"]      = "debian"
debian["install"]   = "https://deb.debian.org/debian/dists/stable/main/installer-amd64/current/images/netboot/netboot.tar.gz"
debian["live"]      = "https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/$(curl -s \
                    https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/ | grep -Eo '(debian-live).*xfce.*iso' | sed -r 's/(.iso).+/\1/')"
debian["preseed"]   = "https://www.debian.org/releases/buster/example-preseed.txt"
debian["scripts"]   = "https://www.debian.org/releases/buster/example-preseed.txt"

# Kali URLs
kali = {}
kali["name"]        = "kali"
kali["install"]     = "http://http.kali.org/kali/dists/kali-rolling/main/installer-amd64/current/images/netboot/netboot.tar.gz"
kali["live"]        = "https://cdimage.kali.org/current/$(curl -s https://cdimage.kali.org/current/ | grep -Eo '(kali-linux).*live.*amd64.iso' | \
	                sed -r 's/(.iso).+/\1/' | sed -n 1p)"
kali["preseed"]     = "https://gitlab.com/kalilinux/recipes/kali-preseed-examples/-/raw/master/kali-linux-rolling-preseed.cfg"
kali["scripts"]     = "https://gitlab.com/kalilinux/recipes/kali-preseed-examples/-/raw/master/kali-linux-rolling-preseed.cfg"

# GRUB URLs
grub = {}
grub["name"]        = "bootx64.efi"
grub["source"]      = "https://ftp.gnu.org/gnu/grub/$(curl -s https://ftp.gnu.org/gnu/grub/ | grep -Eo '(grub).*tar.gz' | sed -r 's/(.gz).+/\1/' | \
				    sed '$!d')"
grub["arch"]        = "x86_64-efi"
grub["path"]        = "'(tftp,", tftp_address, ")/", tftp_boot_folder, "'"
grub["modules"]     = "efinet file gfxmenu gfxterm hdparm linuxefi linux lsefi lsmmap ls lvm memdisk multiboot2 net shim_lock signature_test squash4 \
                    syslinuxcfg tar terminal tftp time usb video chain configfile disk gptsync iso9660 lsefisystab lspci parttool procfs scsi"
