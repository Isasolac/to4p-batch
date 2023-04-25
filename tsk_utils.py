import os 
import subprocess
from xml.etree import ElementTree
from fs import SupportedTypes
import datetime
import hashlib

FIWALK_DEFAULT_NS = "{http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML}"


def hash(file_path):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
    return md5.hexdigest(), sha1.hexdigest()

def check_if_file_exists(path):
    if not os.path.isfile(path):
        raise FileNotFoundError("Could not find disk image!")

def run_command(command, input = None):
    with open("audit-log.txt", 'a') as f:
        now = datetime.datetime.now().strftime("%B %d %Y %H:%M:%S")
        f.write(f"{now}, {command.strip()} , Piped: {True if input is not None else False}\n")
    process = subprocess.run(command, shell=True, capture_output=True, input = input)
    return process.returncode, process.stdout, process.stderr

def mmls(dd_image_path):
    check_if_file_exists(dd_image_path)
    

def fsstat(dd_image_path):
    check_if_file_exists(dd_image_path)
    returncode, stdout, stderr = run_command('fsstat ' + dd_image_path)
    return returncode, stdout.decode(), stderr.decode()

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

def fiwalk(dd_image_path):
    files = []
    try:
        _, output, _ = run_command("fiwalk -x -I -f " + dd_image_path)
        root = ElementTree.fromstring(output.decode())
        # Since we will run fiwalk on a single FS partition, 
        # we should only have one volume 
        volume = root.find(FIWALK_DEFAULT_NS + "volume")
        for fileobject in volume.findall(FIWALK_DEFAULT_NS + "fileobject"):
            name_type = fileobject.find(FIWALK_DEFAULT_NS + "name_type")
            inode = fileobject.find(FIWALK_DEFAULT_NS + "inode")
            
            # Let's analyse only regular files
            if name_type == None or name_type.text != "r" or inode == None:
                continue
            file = {}
            filename = fileobject.find(FIWALK_DEFAULT_NS + "filename")
            libmagic = fileobject.find(FIWALK_DEFAULT_NS + "libmagic")
            mtime = fileobject.find(FIWALK_DEFAULT_NS + "mtime")
            ctime = fileobject.find(FIWALK_DEFAULT_NS + "ctime")
            atime = fileobject.find(FIWALK_DEFAULT_NS + "atime")
            crtime = fileobject.find(FIWALK_DEFAULT_NS + "crtime")

            file["inode"] = inode.text if inode != None else None
            file["filename"] = filename.text if filename != None else None
            file["type"] = libmagic.text if libmagic != None else None
            file["mtime"] = mtime.text if mtime != None else None
            file["ctime"] = ctime.text if ctime != None else None
            file["atime"] = atime.text if atime != None else None
            file["crtime"] = crtime.text if crtime != None else None
            file["md5"] =  None
            file["sha1"] = None
            for hashdigest in fileobject.findall(FIWALK_DEFAULT_NS + "hashdigest"):
                if hashdigest.get("type") == "md5":
                    file["md5"] = hashdigest.text
                if hashdigest.get("type") == "sha1":
                    file["sha1"] = hashdigest.text

            files.append(file)
    except:
        print("Failed to execute fiwalk")
    return files
