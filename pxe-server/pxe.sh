#!/bin/bash

declare -A debian
debian[name]="debian"
debian[install]="https://deb.debian.org/debian/dists/stable/main/installer-amd64/current/images/netboot/netboot.tar.gz"
debian[live]="https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/$(curl -s \
				https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/ | grep -Eo '(debian-live).*xfce.*iso' | sed -r 's/(.iso).+/\1/')"
debian[preseed]="https://www.debian.org/releases/buster/example-preseed.txt"
debian[scripts]="https://www.debian.org/releases/buster/example-preseed.txt"

#debian=(
#	"debian" \
#	"https://deb.debian.org/debian/dists/stable/main/installer-amd64/current/images/netboot/netboot.tar.gz" \
#	"https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/$(curl -s \
#	https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/ | grep -Eo '(debian-live).*xfce.*iso' | sed -r 's/(.iso).+/\1/')" \
#	"https://www.debian.org/releases/buster/example-preseed.txt"
#)

kali=(
	"kali" \
	"http://http.kali.org/kali/dists/kali-rolling/main/installer-amd64/current/images/netboot/netboot.tar.gz" \
	"https://cdimage.kali.org/current/$(curl -s https://cdimage.kali.org/current/ | grep -Eo '(kali-linux).*live.*amd64.iso' \
	| sed -r 's/(.iso).+/\1/' | sed -n 1p)"
	"https://gitlab.com/kalilinux/recipes/kali-preseed-examples/-/raw/master/kali-linux-rolling-preseed.cfg"
)

grub_source_url="https://ftp.gnu.org/gnu/grub/$(curl -s https://ftp.gnu.org/gnu/grub/ | grep -Eo '(grub).*tar.gz' | sed -r 's/(.gz).+/\1/' \
				| sed '$!d')"

os=(${debian[@]})

options=(install live preseed scripts)

ftp_adress="$server/ssd1"
ftp_login="ftp"
ftp_pass="pa$$w0rd"

tftp_address="$server"

user_name="flypatriot"
user_pass="pa$$w0rd"

root_pass="pa$$0rd"

dest="tftp/files"

function md5_hash () {
	printf $1 | mkpasswd -s -m md5
}

function make_bootloader {
	grub-mkimage -O x86_64-efi -o ./bootx64.efi -p '(tftp,'$tftp_address')/boot' efinet file \
	gfxmenu gfxterm hdparm linuxefi linux lsefi lsmmap ls lvm memdisk multiboot2 net shim_lock \
	signature_test 	squash4 syslinuxcfg tar terminal tftp time usb video chain configfile disk \
	gptsync iso9660 lsefisystab lspci parttool procfs scsi
}

function create_dirs {
	for dir in ${options[@]}
	do
		if [ ! -d $dest/$dir ]; then
			mkdir $dest/$dir
		fi
	done
}

function download_files () {
	list=${@}
	for opt in ${options[@]}
	do
		if [ -d $dest/$opt ]; then
			echo $opt
			echo ${list[preseed]}
		fi
	done
}

#create_dirs

download_files ${debian[@]}

#md5_hash $user_pass
