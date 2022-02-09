#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import os
import subprocess
from pathlib import Path


# Toolchains URLs
toolchains = {
              'aarch64': 'https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/'
                         'aarch64/aarch64-linux-android-4.9/+archive/refs/heads/master.tar.gz',
              'clang': 'https://android.googlesource.com/platform/prebuilts/clang/host/linux-x86/'
                       '+archive/refs/heads/master/clang-r433403.tar.gz'
             }


# GIT variables
glist = {}
glist['REMOTE_NAME'] = '0ctobot'
glist['REMOTE_URL'] = 'https://github.com/0ctobot/neutrino_kernel_oneplus_sm8250.git'
glist['LOCAL_BRANCH'] = 'neutrino-msm-kebab-4.19'
glist['REMOTE_GIT'] = ' '.join([glist['REMOTE_NAME'], glist['LOCAL_BRANCH']])
glist['REMOTE_BRANCH'] = '/'.join([glist['REMOTE_NAME'], glist['LOCAL_BRANCH']])
glist['NETHUNTER_BRANCH'] = 'neutrino-nethunter'


# Global variables
vlist = {
           'CCACHE': False, 'CC': 'clang', 'MODULE_DIRTREE': 'modules/system_root/',
           'THREADS': str(os.cpu_count()), 'DO_DTBO': 'false', 'DO_DTB': 'false',
           'DTB_VER': '2', 'CONFIG_TOOL': 'menuconfig', 'MAKE_ARGS': '',
           'CONFIG': 'neutrino_defconfig', 'TIME': datetime.now().strftime('%H:%M:%S'),
           'DEBIAN_DEPEND': ['axel', 'bc', 'build-essential', 'ccache', 'curl',
                             'device-tree-compiler', 'pandoc', 'libncurses5-dev',
                             'lynx', 'lz4', 'fakeroot', 'xz-utils', 'whiptail'],
           'BOT_TOKEN': os.environ.get('bot_token'), 'CHAT_ID': os.environ.get('chat_id')
           }


# Global directories
plist = {}
plist['TD'] = Path(Path.home(), '.android')
plist['CCD64'] = Path(plist['TD'], 'aarch64')
plist['BDIR'] = Path(__file__).resolve().parent
plist['KDIR'] = Path(plist['BDIR']).parent
plist['CONFIG_DIR'] = Path(plist['KDIR'], 'arch', 'arm64', 'configs')
plist['BOOT_DIR'] = Path(plist['BDIR'], 'out', 'arch', 'arm64', 'boot')
plist['NHUNTER_DIR'] = Path(plist['BDIR'], 'nethunter')
plist['ANYKERNEL_DIR'] = Path(plist['BDIR'], 'anykernel3')
plist['KERNEL_OUT'] = Path(plist['BDIR'], 'out')
plist['MODULES_OUT'] = Path(plist['BDIR'], 'modules_out')
plist['MODULES_IN'] = Path(plist['MODULES_OUT'], 'lib')
plist['UPLOAD_DIR'] = Path(plist['BDIR'], 'output')
plist['PATCH_DIR'] = Path(plist['BDIR'], 'patches')


# Variables for export to environment
elist = {}
elist['ARCH'] = 'arm64'
elist['SUBARCH'] = 'arm64'
elist['CLANG_ROOT'] = str(Path(plist['TD'], 'clang'))
elist['CLANG_PATH'] = str(Path(elist['CLANG_ROOT'], 'bin'))
elist['PATH'] = str(elist['CLANG_PATH'] + ':' + os.environ['PATH'])
elist['LD_LIBRARY_PATH'] = str(Path(elist['CLANG_ROOT'], 'lib64'))
elist['CLANG_TRIPLE'] = 'aarch64-linux-gnu-'
elist['CROSS_COMPILE'] = str(Path(plist['CCD64'], 'bin', 'aarch64-linux-android-'))
elist['LOCALVERSION'] = '-NetHunter'


# Files
flist = {
            'NH_ARCHIVE': 'kernel' + elist['LOCALVERSION'],
            'ANY_ARCHIVE': 'anykernel' + elist['LOCALVERSION'],
            'KERNEL_IMAGE': Path(plist['BOOT_DIR'], 'Image.gz-dtb'),
            'DTBTOOL': Path(plist['BDIR'], 'tools', 'dtbToolCM'), 'DTB_IMG': 'dtb.img',
            'DTB_IN': Path(plist['BOOT_DIR'], 'dts'),
            'DTBO_IMAGE': Path(plist['BOOT_DIR'], 'dtbo.img'),
            'CHANGELOG': Path(plist['ANYKERNEL_DIR'], 'Changelog.txt'),
            'NH_CONFIG': Path(plist['CONFIG_DIR'], 'nethunter_defconfig'),
            'CONFIG': Path(plist['CONFIG_DIR'], 'neutrino_defconfig')
            }
