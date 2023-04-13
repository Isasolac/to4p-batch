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
        useful_data = False

        for line in output.splitlines():
            if useful_data:
                parse_mmls_line(line)
            else:
                #TODO: parse header for info
                pass
            if "Slot" in line:
                useful_data = True

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
