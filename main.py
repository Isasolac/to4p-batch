import os
import argparse # Could also look at getopt?
import parse_fs
import wordlist
import report

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
    args = parser.parse_args()

    # Collects the dictionary information about each image
    image_data_list = []

    if args.wordlist:
        words = parse_wordlist(args.wordlist)

        print(words)

    for image in args.images:
        print(image)

        # Step 1: use mmls to find filesystems
        stream = os.popen('mmls ./'+image)
        output = stream.read()
        #print(output)

        volume_data = {"Volume": "", "Sector_Size": -1}
        fs_data = dict()
        fs_data_start = False

        fs_id = 0

        # Parse the output of mmls into information about the allocation of each partition
        # As well as reporting metadata
        for line in output.splitlines():

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
                    print(data["Description"])
                    # Find the type of file system
                    '''
                    if "FAT32" in data["Description"]:
                        fs_type = "fat32"
                    elif "FAT16" in data["Description"]:
                        fs_type = "fat16"
                    elif "NTFS" in data["Description"]:
                        fs_type = "ntfs"
                    else:
                        fs_type = "unknown"
                    '''
                    fs_type = 'unknown'

                    # Create the name
                    name = fs_type + "_" + str(fs_id) + ".dd"

                    # Store the name in the data structure
                    data["Name"] = name

                    # mmcat out the file system
                    command = 'mmcat ./'+image+' '+fs_key+' > '+name
                    print(command)
                    stream = os.popen(command)
                    output = stream.read()

                    # use fsstat to get the file system type
                    fs_type = get_fs_type(name)
                    #print(fs_type+fs_key)

                    data["Type"] = fs_type

                    fs_data[fs_key] = data

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

            elif "Units" in line:
                tokens = line.split()

                # Sector size is in bytes
                sector_size = int((tokens[3].partition("-"))[0])
                print("sector size is: "+str(sector_size))
                volume_data["Sector_Size"] = sector_size

            elif "Slot" in line:
                fs_data_start = True
        
        # Add this to the collection
        image_data_list.append(volume_data)
    
    # TODO: Add calls to lines that parse the filesystem data

    # TODO: Add calls to lines that parse the wordlist

    # TODO: Generate the report

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


if __name__ == '__main__':
    main()
