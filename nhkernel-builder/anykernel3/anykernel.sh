# AnyKernel3 Ramdisk Mod Script
# osm0sis @ xda-developers
# Changes for SkyDragon by HolyAngel @ xda-developers
# Changes for NetHunter by Re4son

## AnyKernel setup
# begin properties
properties() { '
kernel.string=NetHunter Kernel for the OnePlus 8 / T / Pro
do.devicecheck=1
do.modules=1
do.systemless=0 #Never use this for NetHunter kernels as it prevents us from writing to /lib/modules
do.cleanup=1
do.cleanuponabort=0
device.name1=OnePlus8
device.name2=oneplus8
device.name3=OnePlus8T
device.name4=oneplus8t
device.name5=OnePlus8Pro
device.name6=oneplus8pro
device.name7=instantnoodle
device.name8=instantnoodlep
device.name9=instantnoodlev
device.name10=Kebab
device.name11=kebab
device.name12=Kebabt
device.name13=kebabt
device.name14=Kona
device.name15=kona
supported.versions=
supported.patchlevels=
'; } # end properties

# shell variables
block=/dev/block/bootdevice/by-name/boot;
is_slot_device=1;
ramdisk_compression=auto;

## AnyKernel methods (DO NOT CHANGE)
# import patching functions/variables - see for reference
. tools/ak3-core.sh;

## Trim partitions
fstrim -v /cache;
fstrim -v /data;

## AnyKernel file attributes
# set permissions/ownership for included ramdisk files
chmod -R 750 $ramdisk/*;
chown -R root:root $ramdisk/*;

## AnyKernel install
dump_boot;

# begin ramdisk changes

# init.rc
backup_file init.rc;
replace_string init.rc "cpuctl cpu,timer_slack" "mount cgroup none /dev/cpuctl cpu" "mount cgroup none /dev/cpuctl cpu,timer_slack";

# init.tuna.rc
backup_file init.tuna.rc;
insert_line init.tuna.rc "nodiratime barrier=0" after "mount_all /fstab.tuna" "\tmount ext4 /dev/block/platform/omap/omap_hsmmc.0/by-name/userdata /data remount nosuid nodev noatime nodiratime barrier=0";
append_file init.tuna.rc "bootscript" init.tuna;

# fstab.tuna
backup_file fstab.tuna;
patch_fstab fstab.tuna /system ext4 options "noatime,barrier=1" "noatime,nodiratime,barrier=0";
patch_fstab fstab.tuna /cache ext4 options "barrier=1" "barrier=0,nomblk_io_submit";
patch_fstab fstab.tuna /data ext4 options "data=ordered" "nomblk_io_submit,data=writeback";
append_file fstab.tuna "usbdisk" fstab;

# end ramdisk changes

write_boot;
## end install

