import subprocess
import re

def get_sector_or_cluster(match: str, sector_or_cluster_size: int):
    """ Calculates the sector or cluster based on the given the offset of the 
    matched string and the given sector/cluster size

    Params:
    match: str: A single match from the output of the search (one line)
    sector_or_cluster_size: int: The sector or cluster size to use to compute
        the associated sector or cluster

    Returns:
    The associated sector or cluster of the match based on its byte offset
    """
    byte_offset = int(re.search("[0-9]+", match).group())
    return byte_offset // sector_or_cluster_size

def get_inode(fs_type: str, filesystem: str, cluster: int):
    """ Retrieves the inode of a given cluster

    Params:
    fs_type: str: The type of the filesystem (NTFS, FAT, etc.)
    filesystem: str: The path to the filesystem image file
    cluster: int: The cluster to find the inode of

    Returns:
    The inode associated with the given cluster in the given filesystem
    """
    ifind = subprocess.run(
        "ifind -f %s %s -d %d" % (fs_type, filesystem, cluster), 
        capture_output=True, shell=True)
    return ifind.stdout

def parse_istat_metadata(fs_type: str, filesystem: str, inode: str):
    """ Retrieves the metadata about a given inode in the given filesystem

    Params:
    fs_type: str: The type of filesystem (NTFS, FAT, etc.)
    filesystem: str: The path to the filesystem image file
    inode: str: The inode to retrieve the metadata about

    Returns:
        The File created, modified, and accessed times, including the MFT 
        modified time for NTFS, and a check for whether the 
        $STANDARD_INFORMATION times match the $FILE_NAME times.
    """
    istat = subprocess.run("istat -f %s %s %s" % (fs_type, filesystem, inode),
                           capture_output=True, shell=True)
    istat_out = istat.stdout.decode()
    if fs_type == "ntfs":
        # TODO: parse istat NTFS output
        chunks = istat_out.split("Attribute Values:\n")
        std_info_times = chunks[1].split("\n\n")[0]
        std_info_times = std_info_times.split("\n")[-4:]
        file_name_times = chunks[2].split("\n\n")[0]
        file_name_times = file_name_times.split("\n")[-4:]
        matching = True
        for i in range(4):
            if std_info_times[i] != file_name_times[i]:
                # Modified Standard Info times!
                matching = False
        return std_info_times, file_name_times, matching
    elif fs_type == "fat":
        # TODO: parse istat FAT output
        times = istat_out.split("Directory Entry Times:\n")[1]
        times = times.split("\n")[:3]
        return times

def get_filepath(fs_type: str, filesystem: str, inode: str):
    """ Retrieves the file path of the given inode in the given filesystem

    Params:
    fs_type: str: The type of the filesystem (NTFS, FAT, etc.)
    filesystem: str: The path to the filesystem image file
    inode: str: The inode to retrieve the metadata about

    Returns: 
    The file path of the given inode in the given filesystem
    """
    ffind = subprocess.run("ffind -f %s %s %s" % (fs_type, filesystem, inode),
                           capture_output=True, shell=True)
    return ffind.stdout