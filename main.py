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

    for image in args.images:
        print(image)

        # Step 1: use mmls to find filesystems
        stream = os.popen('mmls ./'+image)
        output = stream.read()
        print(output)

        filesystem_lines = []
        fs_data = False

        # Parse the output of mmls into information about the allocation of each partition
        # As well as reporting metadata
        for line in output.splitlines():
            if fs_data:
                pass
                #parse_mmls_line(line)
            elif "Units" in line:
                tokens = line.split()

                # Sector size is in bytes
                # TODO: store this info in data structure
                sector_size = int((tokens[3].partition("-"))[0])
                print("sector size is: "+str(sector_size))

            elif "Slot" in line:
                fs_data = True

'''
count: the number ID of the resulting carved filesystem ex "1_1"
'''
def cat_slot(slot_num, image_name, count):
    pass

'''
Returns a tuple with: (slot number, is_partition, start, end, length, description)
'''
def parse_mmls_line(line):

    slot_partition = line.partition(":")
    # WARNING = could split at more than one area

    slot_num = slot_partition[0]

    # split the rest into tokens using split
    tokens = line.split()

    description = tokens[5]
    
    if tokens[1] != "-----":
        is_partition = True

    



    return(slot_num, is_partition,)
    




if __name__ == '__main__':
    main()
