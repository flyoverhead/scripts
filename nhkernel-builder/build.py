#!/usr/bin/python3
# -*- coding: utf-8 -*-

from config import *

import os.path
import glob
import shutil
import requests


def abort(err):
    print('Error: ' + err)
    exit(1)


# Send messages to Telegram
def tg_send_msg(msg):
    data = {
        'chat_id': vlist['CHAT_ID'],
        'text': ':'.join([vlist['TIME'], msg])
    }
    r = requests.post('https://api.telegram.org/bot' + vlist['BOT_TOKEN'] +
                      '/sendMessage', data=data)
    if r.status_code != 200:
        raise Exception('Send error')


# Send file to Telegram
def tg_send_file(file):
    files = {'document': open(file, 'rb')}
    data = {'chat_id': vlist['CHAT_ID']}
    r = requests.post('https://api.telegram.org/bot' + vlist['BOT_TOKEN'] +
                      '/sendDocument', data=data, files=files)
    if r.status_code != 200:
        raise Exception('Send error')


# Set export's variables to build environment
def set_environment():
    enable_ccache()
    os.environ.update(elist)


# Check if variables are successfully exported to environment
def check_environment():
    for name in elist:
        try:
            print(name, '=', os.environ[name])
        except KeyError:
            pass


# Check if all global variables are correct
def check_list(dict):
    for name, value in dict.items():
        print('{} = {}'.format(name, value))


# Install toolchains
def install_toolchains(td, toolchains):
    for name, url in toolchains.items():
        d = Path(td, name)
        if not d.exists() or not any(os.scandir(d)):
            get_toolchains(name, url)
            shutil.copytree(name, d, dirs_exist_ok=True)


# Download toolchains
def get_toolchains(name, url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        abort(str(e))
    download_ok = False
    filename = os.path.basename(url)
    f = open(filename, 'wb')
    try:
        for chunk in response.iter_content(chunk_size=8192):
            if not chunk:
                continue  # Ignore empty chunks
            f.write(chunk)
        download_ok = True
    except requests.exceptions.RequestException as e:
        print('Error: ' + str(e))
    f.flush()
    os.fsync(f.fileno())
    f.close()
    if download_ok:
        print('Download OK: ' + name)
        shutil.unpack_archive(filename, name, 'gztar')
        os.remove(filename)
    else:
        if filename.exists():
            os.remove(filename)
        abort('There was a problem downloading the file "' + filename + '"')


# Clean nhkernel directory
def make_nhclean(nhunter_dir):
    print('Cleaning up NetHunter kernel zip directory')
    if nhunter_dir.exists():
        try:
            shutil.rmtree(nhunter_dir, ignore_errors=True)
        except OSError as e:
            print('%s : %s' % (nhunter_dir, e.strerror))
    print('NetHunter kernel zip directory cleaned')


# Clean anykernel directory
def make_aclean(anykernel_dir):
    files = ['Image*', '*dtb', flist['CHANGELOG'], 'modules']
    print('Cleaning up anykernel zip directory')
    for file in files:
        for f in glob.glob(os.path.join(anykernel_dir, file)):
            if os.path.isfile(f):
                try:
                    os.remove(f)
                except OSError as e:
                    print('%s : %s' % (f, e.strerror))
            elif os.path.isdir(f):
                try:
                    shutil.rmtree(f)
                except OSError as e:
                    print('%s : %s' % (f, e.strerror))
    print('Anykernel directory cleaned')


# Clean "out" folders
def make_oclean(kernel_dir, kernel_out, modules_out):
    print('Cleaning up kernel-out & modules-out directories')
    # Let's make sure we don't delete the kernel source if we compile in the source tree
    if kernel_dir == kernel_out:
        commands = ['clean', 'mrproper']
        # Clean the source tree as well if we use it to build the kernel, i.e. we have no OUT directory
        for command in commands:
            subprocess.run(['make', '-C', kernel_dir, command])
    else:
        shutil.rmtree(kernel_out, ignore_errors=True)
    shutil.rmtree(modules_out, ignore_errors=True)
    print('Out directories removed!')


# Clean source tree
def make_sclean(config_dir):
    print('Cleaning source directory')
    extensions = ['.old', '.new']
    for ext in extensions:
        for f in glob.glob(os.path.join(config_dir, ext)):
            if os.path.isfile(f):
                try:
                    os.remove(f)
                except OSError as e:
                    print('%s : %s' % (f, e.strerror))
    print('Source directory cleaned')


# Full clean
def make_fclean(kernel_out, modules_out, kernel_dir):
    make_nhclean(plist['NHUNTER_DIR'])
    make_aclean(plist['ANYKERNEL_DIR'])
    make_oclean(kernel_dir, kernel_out,
                modules_out)


# Check if $NH_CONFIG exists and create it if not
def get_defconfig(nh_config, config):
    if not nh_config.exists():
        print(nh_config, 'not found, creating.')
        select_defconfig(nh_config, config)


# Select defconfig file
def select_defconfig(nh_config, config):
    if nh_config.exists():
        print('Found', os.path.basename(nh_config))
    elif config.exists():
        print('Using', os.path.basename(config), 'as new',
              os.path.basename(nh_config))
        shutil.copyfile(config, nh_config)


# Create kernel compilation working directories
def setup_dirs(*dirs):
    for d in dirs:
        name = os.path.basename(d)
        Path(name).mkdir(parents=True, exist_ok=True)
        print('Created new', name, 'directory')


# Enable ccache to speed up compilation
def enable_ccache():
    cc = vlist['CC']
    cross_compiler = elist['CROSS_COMPILE']
    if vlist['CCACHE']:
        if cc and cc.find('ccache'):
            vlist['CC'] = '\"ccache ' + cc + '\"'
        if cross_compiler and cross_compiler.find('ccache'):
            elist['CROSS_COMPILE'] = '\"ccache ' + cross_compiler + '\"'
        print('ccache enabled')


# Compile the kernel
def make_kernel(kernel_out, modules_out, kernel_dir):
    make_fclean(kernel_out, modules_out, kernel_dir)
    setup_dirs(kernel_out, modules_out)
    set_environment()
    if vlist['CC'] == 'clang':
        vlist['CC'] = 'CC=clang'
    get_defconfig(flist['NH_CONFIG'], flist['CONFIG'])
    print('Building kernel')
    tg_send_msg('Start building kernel')
    arguments = {
        'NETHUNTER_CONFIG': flist['NH_CONFIG'],
        'CONFIG': os.path.join(kernel_out, '.config'),
        'MAKE': 'make', 'C': '-C', 'KDIR': kernel_dir,
        'O': kernel_out,
        'CC': vlist['CC'], 'J': '-j', 'THREADS': vlist['THREADS'],
        'INSTALL_MOD_PATH': modules_out,
        'MOD_INSTALL': 'modules_install'
    }
    command_line = []
    for item, value in arguments.items():
        if item == 'O':
            value = '{}={}'.format(item, value)
        elif item == 'INSTALL_MOD_PATH':
            value = '{}={}'.format(item, value)
        command_line.append(value)
    config = command_line[0:2]
    kernel = command_line[2:9]
    modules = command_line[2:]
    if kernel_dir == kernel_out:
        kernel.pop(3)
        modules.pop(3)
    else:
        pass
    shutil.copyfile(*config)
    log = 'build_log.txt'
    with open(log, 'w') as f:
        subprocess.run(kernel, stdout=f)
        subprocess.run(modules, stdout=f)
    tg_send_file(log)
    if flist['KERNEL_IMAGE'].exists():
        files = ['source', 'build']
        for file in files:
            for f in Path(modules_out, 'lib', 'modules').rglob(file):
                try:
                    f.unlink()
                except OSError as e:
                    print('%s : %s' % (f, e.strerror))
        print('Kernel build completed successfully')
        tg_send_msg('Kernel build completed successfully')
    else:
        print('Kernel build failed. Watch ', log, 'for details.')


# Prepare file for zip archive
def make_zip(folder, file):
    Path(plist['UPLOAD_DIR']).mkdir(parents=True, exist_ok=True)
    print('Copying kernel to', file, 'zip directory')
    shutil.copy(flist['KERNEL_IMAGE'], folder)
    if Path(vlist['DO_DTBO']).exists():
        print('Copying dtbo to zip directory...')
        shutil.copyfile(flist['DTBO_IMAGE'], folder)
    if Path(vlist['DO_DTB']).exists():
        print(['Generating dtb in zip directory...'])
        subprocess.run(['make_dtb', folder])
    if Path(plist['MODULES_OUT'], 'lib').exists():
        print('Copying modules to', file, 'zip directory...')
        Path(folder,
             vlist['MODULE_DIRTREE']).mkdir(parents=True, exist_ok=True)
        shutil.copytree(plist['MODULES_IN'],
                        Path(folder,
                             vlist['MODULE_DIRTREE']), dirs_exist_ok=True)
        print('Done')
        print('Creating', file, 'zip file')
        shutil.make_archive(file, 'zip', folder)
        print('Moving', file, 'zip to output directory')
        file += '.zip'
        tg_send_file(file)
        shutil.move(Path(file),
                    Path(plist['UPLOAD_DIR'], file))
        print(file, 'is now available in:', plist['UPLOAD_DIR'])


# Generate the NetHunter kernel zip - to be extracted in the devices folder of the nethunter-installer
def make_nhkernel_zip(nhunter_dir, nh_archive):
    Path(nhunter_dir).mkdir(parents=True, exist_ok=True)
    print('Making NetHunter kernel zip file')
    make_zip(nhunter_dir, nh_archive)
    print('NetHunter kernel zip file build successfully')
    make_nhclean(nhunter_dir)


# Generate the anykernel zip
def make_anykernel_zip(anykernel_dir, any_archive):
    print('Making Test kernel zip file')
    make_zip(anykernel_dir, any_archive)
    print('Test kernel zip file build successfully')
    make_aclean(anykernel_dir)


# Main function
def main():
    make_kernel(plist['KERNEL_OUT'], plist['MODULES_OUT'], plist['KDIR'])
    make_nhkernel_zip(plist['NHUNTER_DIR'], flist['NH_ARCHIVE'])
    make_anykernel_zip(plist['ANYKERNEL_DIR'], flist['ANY_ARCHIVE'])
#    install_toolchains(plist['TD'], toolchains)
#    setup_dirs(plist['KERNEL_OUT'], plist['MODULES_OUT'])
#    check_list(plist)


# Run programm
if __name__ == '__main__':
    main()
