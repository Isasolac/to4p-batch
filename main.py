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
    args = parser.parse_args()

    # Collects the dictionary information about each image
    image_data_list = []

    for image in args.images:
        print(image)

        # Step 1: use mmls to find filesystems
        stream = os.popen('mmls ./'+image)
        output = stream.read()
        print(output)

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
                fs_data[tokens[0]] = data

                # If is_partition, parse out the file system and store the name
                if data["Partition"]:
                    # Find the type of file system
                    if "FAT32" in data["Description"]:
                        fs_type = "fat32"
                    elif "FAT16" in data["Description"]:
                        fs_type = "fat16"
                    elif "NTFS" in data["Description"]:
                        fs_type = "ntfs"
                    else:
                        fs_type = "unknown"

                    data["Type"] = fs_type

                    # Create the name
                    name = fs_type + "_" + str(fs_id) + ".dd"

                    # Store the name in the data structure
                    data["Name"] = name

                    # TODO: mmcat out the file system
                    command = 'mmcat ./'+image+' '+tokens[0]+' > '+name
                    print(command)
                    stream = os.popen(command)

                    fs_data[tokens[0]] = data

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
Returns a tuple with: (slot number, is_partition, start, end, length, description)
'''
def parse_mmls_line(line):
    tokens = line.split()



    data = {"Slot": tokens[1],
    "Start": tokens[2],
    "End": tokens[3],
    "Size": tokens[4],
    "Description": tokens[5]}

    #slot_partition = line.partition(":")

    if tokens[1] != "-----" and tokens[1] != "Meta":
        data["Partition"] = True

    return data

    
    




if __name__ == '__main__':
    main()
