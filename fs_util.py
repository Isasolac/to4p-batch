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
        capture_output=True)
    return ifind.stdout

def parse_istat_metadata(fs_type: str, filesystem: str, inode: int):
    """ Retrieves the metadata about a given inode in the given filesystem

    Params:
    fs_type: str: The type of filesystem (NTFS, FAT, etc.)
    filesystem: str: The path to the filesystem image file
    inode: int: The inode to retrieve the metadata about

    Returns:

    """
    istat = subprocess.run("istat -f %s %s %d" % (fs_type, filesystem, inode),
                           capture_output=True)
    if fs_type == "ntfs":
        pass
    elif fs_type == "fat":
        pass
    return

def get_filepath(fs_type: str, filesystem: str, inode: int):
    """ Retrieves the file path of the given inode in the given filesystem

    Params:
    fs_type: str: The type of the filesystem (NTFS, FAT, etc.)
    filesystem: str: The path to the filesystem image file
    inode: int: The inode to retrieve the metadata about

    Returns: 
    The file path of the given inode in the given filesystem
    """
    ffind = subprocess.run("ffind -f %s %s %d" % (fs_type, filesystem, inode),
                           capture_output=True)
    return ffind.stdout