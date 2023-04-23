import subprocess
import re
import fs_util

def wordlist_search_image(wordlist: list, image: str, image_data_tuple: tuple, 
                          exclude_list: list = [], 
                          search_partitions: bool = True, 
                          verbose: bool = False):
    """ Searches through a disk image for the words contained in the word list

    Params:
    wordlist: [str, ...]: A list of string words to search for
    image: str: a string path to the image file to search in
    image_data_tuple: tuple: contains the volume_data and fs_data dictionaries
    exclude_list: [str, ...] = []: (Optional) A list of strings to exclude from
        the search
    search_partitions: bool = True: (Optional) Whether to search through all 
        relevant partitions as well, or simply return the list of relevant  
        partitions
    verbose: bool = False: (Optional) Whether or not to print out extra
        information while running

    Returns:
    A dictionary containing the total number of occurrences on the disk and
        either the filesystem search results for each partition or the set
        of all relevant partitions in which matches were found

        "Total_Occurrences": dict: A mapping of each word in the word list to 
            the number of times it was found in the filesystem.
        "Relevant_Partitions": set: A set of the partition IDs associated with
            the file systems that contain matches
        A mapping of each relevant filesystem image name to its results from 
            wordlist_search_filesystem
        
    """
    # First, find matches in the image as a whole, then narrow down to specific
    # filesystems 
    volume_data, fs_data = image_data_tuple
    if verbose:
        print("Finding matching strings in image %s:" % image)
    matches_str = get_matches(wordlist, image, exclude_list, verbose)
    occurrences = count_occurrences(wordlist, matches_str)
    relevant_partitions = {}
    if verbose:
        print("Searching through matches for relevant partitions:")
    for match in matches_str.split("\n"):
        if re.search("[0-9]+", match) is None:
            continue
        # get sector offset
        match_sector = fs_util.get_sector_or_cluster(
            match, volume_data["Sector_Size"])
        if verbose:
            byte_offset = int(re.search("[0-9]+", match).group())
            print("Match %s in sector %d ( = %d / %d)" % 
                  (match, match_sector, byte_offset, 
                   volume_data["Sector_Size"]))
            print("Checking through paritions for matching sector")
        # use sector offset to find partition based on the filesystems in the image
        for fs_key, part in fs_data.items():
            if int(part["Start"]) <= match_sector <= int(part["End"]):
                if verbose:
                    print("Found sector %d in %s (between %d and %d)" % 
                          (match_sector, part["Name"], part["Start"], 
                           part["End"]))
                # store the names of the relevant partitions along with their data
                relevant_partitions[fs_key] = part
                break
    results = {"Total_Occurrences": occurrences, 
               "Relevant_Partitions": set(relevant_partitions.keys())}
    if search_partitions:
        # aggregate results from all relevant filesystems, as well as a total occurrences count
        if verbose:
            print("Searching through all relevant partitions:")
        for fs_key, fs_data in relevant_partitions.items():
            # run wordlist search on file
            results[fs_key] = wordlist_search_filesystem(
                wordlist, fs_data["Name"], fs_data, exclude_list, verbose)
    else:
        if verbose:
            print("Skipped searching through relevant partitions.")
        # return only the occurrences count and the set of relevant partitions
    return results

def wordlist_search_filesystem(wordlist: list, filesystem: str, fs_data, 
                               exclude_list: list = [], verbose: bool = False):
    """ Searches through a disk image for the words contained in the word list

    Params:
    wordlist: [str, ...]: A list of string words to search for
    filesystem: str: a string path to the filesystem image file to search in
    fs_data: dict: contains information on the filesystem, as well as an object
        containing its data (parse_fs.py)
    exclude_list: [str, ...] = []: (Optional) A list of strings to exclude from
        the search
    verbose: bool = False: (Optional) Whether or not to print out extra
        information while running

    Returns:
    A dictionary containing the number of occurrences and the files associated 
        with those matches.

        "Occurrences": dict: A mapping of each word in the word list to the 
            number of times it was found in the filesystem.
        "Found_Files": dict: A mapping of the matching strings from the word 
            list to their associated files and inodes
    """
    if verbose:
        print("Finding matching strings in filesystem %s:" % filesystem)
    matches_str = get_matches(wordlist, filesystem, exclude_list, verbose)
    occurrences = count_occurrences(wordlist, matches_str)
    found_files = {}
    fs_type = ""
    if "NTFS" in fs_data["Type"]:
        fs_type = "ntfs"
    elif "FAT" in fs_data["Type"]:
        fs_type = "fat"
    # else:
    #     raise
    if verbose:
        print("Searching through matches to find associated files:")
    for match in matches_str.split("\n"):
        if re.search("[0-9]+", match) is None:
            continue
        match_cluster = fs_util.get_sector_or_cluster(match, fs_data["Object"].cluster_size)
        if verbose:
            byte_offset = int(re.search("[0-9]+", match).group())
            print("Match %s in cluster %d ( = %d / %d)" % 
                  (match, match_cluster, byte_offset, fs_data["Object"].cluster_size))
        match_inode = fs_util.get_inode(fs_type, filesystem, match_cluster).decode()
        if verbose:
            ifindcmd = "ifind -f %s %s -d %d" % (fs_type, filesystem, match_cluster)
            print("Find the inode for cluster %d (%s)" % 
                  (match_cluster, ifindcmd))
        match_info = {}
        match_info["Match_Line"] = match
        match_info["Cluster"] = match_cluster
        match_info["Inode"] = match_inode
        if match_inode.startswith("Inode not found"):
            if verbose:
                print("Couldn't find a matching inode for cluster %d" % 
                      match_cluster)
            # found_files[match] = "Cluster: %d (Inode not found)" % match_cluster
            match_info["Filepath"] = None
            match_info["Filename"] = None
            match_info["Metadata"] = None
        else:
            if verbose:
                print("Found inode %d for cluster %d" % (match_inode, 
                                                         match_cluster))
                ffindcmd = "ffind -f %s %s %s" % (fs_type, filesystem, 
                                                  match_inode)
                print("Find the filepath for inode %d (%s)" % 
                      (match_inode, ffindcmd))
            match_filepath = fs_util.get_filepath(fs_type, filesystem, 
                                                  match_inode)
            if verbose:
                print("Found filepath %s" % match_filepath)
                istatcmd = "istat -f %s %s %s" % (fs_type, filesystem, match_inode)
                print("Collecting file metadata (%s)" % istatcmd)
            # found_files[match] = match_filepath + " (Inode: " + str(match_inode) + ")"
            match_info["Filepath"] = match_filepath
            match_info["Filename"] = match_filepath.split("/")[-1]
            match_info["Metadata"] = fs_util.parse_istat_metadata(fs_type, filesystem, match_inode)
        found_files[", ".join([i for i in wordlist if i in match])] = match_info
    return {"Occurrences": occurrences, "Found_Files": found_files}


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
    stringscmd = "strings -eS -td " + image
    if verbose:
        print("Extracting strings from %s (%s)" % (image, stringscmd))
    stringsproc = subprocess.run(stringscmd, capture_output=True, shell=True)
    strings = stringsproc.stdout
    grepcmd = "grep -i -w -E '" + "|".join(wordlist) + "'"
    if verbose: 
        print("Searching for strings in wordlist (%s)" % grepcmd)
    grepproc = subprocess.run(grepcmd, input=strings, capture_output=True, 
                              shell=True)
    foundstrings = grepproc.stdout
    if len(exclude_list) > 0:
        invgrepcmd = "grep -i -v -E '" + "|".join(exclude_list) + "'"
        if verbose:
            print("Removing strings in exclude list (%s)" % invgrepcmd)
        invgrepproc = subprocess.run(invgrepcmd, input=foundstrings, 
                                     capture_output=True, shell=True)
        foundstrings = invgrepproc.stdout
    if verbose:
        print("Finished finding matching strings.")
    return foundstrings.decode() 


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
