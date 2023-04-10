import os
import argparse

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
    

def ntfs_parse(ntfs):
    # TODO: parse NTFS filesystem! Argument will be passed in as a string

    # PERSON 2
    pass

def fat_parse(fat):
    # TODO: parse FAT filesystem! Argument will be passed in as a string
    
    # PERSON 2
    pass


def wordlist_search(wordlist, image):
    # TODO: Use wordlist to search images. Both will be passed in as strings
    # Consider what reports can be generated from this
    # More parameters may be necessary

    # PERSON 3
    pass

def generate_report(data):
    # TODO: what form should our data be stored in?
    # TODO: how can we generate a report?

    # PERSON 4
    pass

if __name__ == '__main__':
    main()
