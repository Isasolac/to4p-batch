import subprocess
import fs_util

def wordlist_search_image(wordlist: list, image: str, image_data, 
                          exclude_list: list = [], verbose: bool = False):
    """ Searches through a disk image for the words contained in the word list

    Params:
    wordlist: [str, ...]: A list of string words to search for
    image: str: a string path to the image file to search in
    image_data: ?: contains information on the image, including sector size, 
        partition information, etc.
    exclude_list: [str, ...] = []: (Optional) A list of strings to exclude from
        the search
    verbose: bool = False: (Optional) Whether or not to print out extra
        information while running

    Returns:

    """
    # First, find matches in the image as a whole, then narrow down to specific
    # filesystems 
    matches_str = get_matches(wordlist, image, exclude_list, verbose)
    occurrences = count_occurrences(wordlist, matches_str, verbose)
    relevant_partitions = set()
    for match in matches_str.split("\n"):
        # get sector offset
        match_sector = fs_util.get_sector_or_cluster(match, image.sector_size, verbose)
        # use sector offset to find partition
        # partition = # TODO: get partition number/offset from the sector
        # relevant_partitions.add(partition)
        pass
    for part in relevant_partitions:
        # 
        pass

def wordlist_search_filesystem(wordlist: list, filesystem: str, fs_data, 
                               exclude_list: list = [], verbose: bool = False):
    """ Searches through a disk image for the words contained in the word list

    Params:
    wordlist: [str, ...]: A list of string words to search for
    filesystem: str: a string path to the filesystem image file to search in
    fs_data: ?: contains information on the filesystem, including its type, 
        cluster size, etc.
    exclude_list: [str, ...] = []: (Optional) A list of strings to exclude from
        the search
    verbose: bool = False: (Optional) Whether or not to print out extra
        information while running

    Returns:
    found_files: dict: A mapping of the matching strings from the word list to
        their associated files and inodes
    occurrences: dict: A mapping of each word in the word list to the number of
        times it was found in the filesystem.
    """
    matches_str = get_matches(wordlist, filesystem, exclude_list, verbose)
    occurrences = count_occurrences(wordlist, matches_str, verbose)
    found_files = {}
    for match in matches_str.split("\n"):
        match_cluster = fs_util.get_sector_or_cluster(match, fs_data.cluster_size, verbose)
        match_inode = fs_util.get_inode(fs_data.fs_type, filesystem, match_cluster)
        match_filepath = fs_util.get_filepath(fs_data.fs_type, filesystem, match_inode)
        found_files[match] = match_filepath + " (Inode: " + str(match_inode) + ")"
    return found_files, occurrences


def get_matches(wordlist: list, image: str, exclude_list: list = [], 
                verbose: bool = False):
    """ Searches through a given image file for all words in the word list

    Params:
    wordlist: [str, ...]: A list of string words to search for
    image: str: a string path to the image file to search in
        This could be either a full disk image or a filesystem carved out from
        a full disk image. 
    exclude_list: [str, ...] = []: (Optional) A list of strings to exclude from
        the search
    verbose: bool = False: (Optional) Whether or not to print out extra 
        information while running.

    Returns:
    A string containing all of the occurrences of words in the word list, 
        in addition to their byte offsets, separated by newline characters.
    """
    # Take in image file path, create strings and grep
    # TODO: Use wordlist to search images. Both will be passed in as strings
    # Consider what reports can be generated from this
    # More parameters may be necessary

    # PERSON 3
    if verbose:
        print("Extracting strings from %s" % image)
    stringsproc = subprocess.run("strings -eS -td " + image, 
                                 capture_output=True)
    strings = stringsproc.stdout
    if verbose: 
        print("Searching for strings in wordlist")
    grepproc = subprocess.run("grep -i -w -E '" + "|".join(wordlist) + "'", 
                              input=strings, capture_output=True)
    foundstrings = grepproc.stdout
    if len(exclude_list) > 0:
        if verbose:
            print("Removing strings in exclude list")
        invgrepproc = subprocess.run(
            "grep -i -v -E '" + "|".join(exclude_list) + "'", 
            input=foundstrings, capture_output=True)
        foundstrings = invgrepproc.stdout
    return foundstrings.decode() # .split("\n")


def count_occurrences(wordlist: list, matches: str):
    """ Counts the number of occurrences of each word in the word list in the
    output from the found strings

    Params:
    wordlist: [str, ...]: A list of string words to count the occurrences of
    matches: str: The output from get_matches, containing all of the instances
        where words from the word list were found
    
    Returns:
    A dictionary mapping of each word in the wordlist to the number of 
        occurrences in the matches string
    """
    return {word: matches.count(word) for word in wordlist}