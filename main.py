import os
import argparse # Could also look at getopt?
import parse_fs
import wordlist
import report
import tsk_utils
import shutil
import hashlib

'''
    Command line input: python ./main.py image1.dd image2.dd [...]
'''

# top level function that runs batch loop
def main():
    
    # TODO: parse each file
    # Set up argument parsing
    # Reference: https://docs.python.org/3/library/argparse.html 
    parser = argparse.ArgumentParser(description="Process images")
    parser.add_argument('images', metavar='image.dd', nargs='+',
                        type=str)
    parser.add_argument('-w', '--wordlist', metavar='wordlist.txt',
                        type=str, required=False)
    parser.add_argument('-s', '--hashlist', metavar='hashlist.txt',
                        type=str, required=False)
    args = parser.parse_args()

    # Collects the dictionary information about each image
    image_data_list = []
    image_name_list = []

    if args.wordlist:
        words = parse_wordlist(args.wordlist)

        print(words)
    

    image_id = 0

    for image in args.images:

        image_dir_name = "image"+"_"+str(image_id)
        if os.path.exists(image_dir_name):
            shutil.rmtree(image_dir_name)
        
        stream = os.popen('mkdir '+image_dir_name)

        # Step 1: use mmls to find filesystems
        stream = os.popen('mmls ./'+image)
        output = stream.read()
        #print(output)
        md5, sha1 = hash(image)
        print(f"{image}: {md5}, {sha1}")

        volume_data = {"Volume": "", "Sector_Size": -1, "Name": image, "Offset_Sector": -1, "MD5": md5, "SHA1": sha1}

        fs_data = dict()
        fs_data_start = False

        fs_id = 0

        # Parse the output of mmls into information about the allocation of each partition
        # As well as reporting metadata
        for line in output.splitlines():

            # Make a directory for the image files

            # Parses the main filesystem data
            if fs_data_start:
                tokens = line.split()

                # Builds 2 layer dictionary: main key is partition ID
                data = parse_mmls_line(line)
                fs_key = str(int(tokens[0].partition(":")[0]))
                #print(fs_key)
                fs_data[fs_key] = data

                # If is_partition, parse out the file system and store the name
                if data["Partition"]:
                    #print(data["Description"])
                    # Find the type of file system
                    fs_type = 'partition'

                    # Create the name
                    name = image_dir_name+"/"+fs_type + "_" + str(fs_id) + ".dd"

                    # Store the name in the data structure
                    data["Name"] = name

                    # mmcat out the file system
                    command = 'mmcat ./'+image+' '+fs_key+' > '+name
                    #print(command)
                    stream = os.popen(command)
                    output = stream.read()

                    # use fsstat to get the file system type
                    fs_type = get_fs_type(name)
                    #print(fs_type+fs_key)

                    data["Type"] = fs_type

                    fs_data[fs_key] = data

                    md5, sha1 = hash(name)
                    print(f"{name}: {md5}, {sha1}")
                    data["MD5"] = md5
                    data["SHA1"] = sha1

                    # increment the fs_id so names don't overlap
                    fs_id = fs_id+1

                
                

            elif "Partition Table" in line:
                tokens = line.split()
                if "DOS" in line:
                    volume="MBR"
                elif "GUID" in line:
                    volume="GPT"
                print("Volume is: "+volume)
                volume_data["Volume"] = volume

            elif "Offset Sector" in line:
                tokens = line.split()

                offset_sec = int(tokens[2])
                volume_data["Offset_Sector"] = offset_sec

            elif "Units" in line:
                tokens = line.split()

                # Sector size is in bytes
                sector_size = int((tokens[3].partition("-"))[0])
                print("sector size is: "+str(sector_size))
                volume_data["Sector_Size"] = sector_size

            elif "Slot" in line:
                fs_data_start = True
        
        # Add this to the collection
        image_data_list.append((volume_data,fs_data))
        

        # Print out filesystem report
        # Create filesystem object here and add it to the data
        for key in fs_data:
            data = fs_data[key]

            # if data["Partition"] is true, then there is a filesystem 
            # associated with this partition ID
            if data["Partition"]:
                # Create the fs object
                data["HashList"] = None
                data["WordList"] = None
                if data["Type"] == "NTFS":
                    data["Object"] = parse_fs.NTFS(data["Name"])
                    data["HashList"] = None if not args.hashlist else parse_hashlist(args.hashlist,data["Name"])
                    data["WordList"] = None if not args.wordlist else wordlist.wordlist_search_filesystem(words, data["Name"], data)
                elif data["Type"] == "FAT16":
                    data["Object"] = parse_fs.FAT16(data["Name"])
                    data["HashList"] = None if not args.hashlist else parse_hashlist(args.hashlist,data["Name"])
                    data["WordList"] = None if not args.wordlist else wordlist.wordlist_search_filesystem(words, data["Name"], data)
                elif data["Type"] == "FAT32":
                    data["Object"] = parse_fs.FAT32(data["Name"])
                    data["HashList"] = None if not args.hashlist else parse_hashlist(args.hashlist,data["Name"])
                    data["WordList"] = None if not args.wordlist else wordlist.wordlist_search_filesystem(words, data["Name"], data)
                else:
                    data["Object"] = parse_fs.Unsupported(data["Name"])
                    print("FS Type Unknown for key "+key)
                
                print("Slot "+key+" is a partition,")
                print("File system type: "+data["Type"])
                print("Carved name = "+data["Name"])
                    
        image_id += 1
    
    for data in image_data_list:
        # volume_data, fs_data
        # wordlist_data = None if not args.wordlist else wordlist.wordlist_search_image(words,data[0]["Name"],data)
        report.generate_report(data[0], data[1])

'''
count: the number ID of the resulting carved filesystem ex "1_1"
'''
def cat_slot(slot_num, image_name, count):
    pass

'''
Returns a dictionary with slot information
'''
def parse_mmls_line(line):
    tokens = line.split()

    # Reconstruct description
    description = ""
    for i in range(5,len(tokens)):
        description += tokens[i]+ " "

    data = {"Slot": tokens[1],
    "Start": tokens[2],
    "End": tokens[3],
    "Size": tokens[4],
    "Description": description}

    #slot_partition = line.partition(":")

    if tokens[1] != "-------" and tokens[1] != "Meta":
        data["Partition"] = True
    else:
        data["Partition"] = False

    return data

    
def get_fs_type(carve_name):

    # Run fsstat on carved image
    stream = os.popen('fsstat ./'+carve_name)
    output = stream.read()

    fs_type = "unknown"
    
    if "File System Type: NTFS" in output:
        # get fs type
        fs_type = "NTFS"

    elif "File System Type: FAT16" in output:
        fs_type = "FAT16"
    elif "File System Type: FAT32" in output:
        fs_type = "FAT32"
    
    return fs_type


def parse_wordlist(wordlist_file):
    words = []

    with open(wordlist_file, 'r') as file:
        
        for word in file.readlines():
            words.append(word.strip('\n'))

    return words

def parse_hashlist(hashlist_file, fs_name):
    matches = []

    file_list = tsk_utils.fiwalk(fs_name)

    with open(hashlist_file, 'r') as file:
        
        for hashsum in file.readlines():
            hashsum = hashsum.strip('\n')

            # Use word to search filesystem
            for file in file_list:
                if  (file["md5"] == hashsum) or (file["sha1"] == hashsum):
                    file["matching_hash"] = "md5" if (file["md5"] == hashsum) else "sha1"
                    matches.append(file)

    return matches

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
 
if __name__ == '__main__':
    main()
