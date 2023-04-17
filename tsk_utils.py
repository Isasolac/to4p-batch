import os 
import shlex
import subprocess

from fs import SupportedTypes

def check_if_file_exists(path):
    if not os.path.isfile(path):
        raise FileNotFoundError("Could not find disk image!")

def run_command(command):
    process = subprocess.run(shlex.split(command), shell=True, capture_output=True)
    return process.returncode, process.stdout.decode(), process.stderr.decode()

def mmls(dd_image_path):
    check_if_file_exists(dd_image_path)
    

def fsstat(dd_image_path):
    check_if_file_exists(dd_image_path)
    returncode, stdout, stderr = run_command('fsstat ' + dd_image_path)
    return returncode, stdout, stderr

def get_fs_type(dd_image_path):
    returncode, stdout, _ = fsstat(dd_image_path)
    lines = [line.strip() for line in stdout.split("\n")]
    if returncode == 0:
        for line in lines:
            if line.startswith("File System Type: "):
                if line.endswith("FAT16"):
                    return (SupportedTypes.FAT16, lines)
                elif line.endswith("FAT32"):
                    return (SupportedTypes.FAT32, lines)
                elif line.endswith("NTFS"):
                    return (SupportedTypes.NTFS, lines)
                
    return (SupportedTypes.UNSUPPORTED, None)
