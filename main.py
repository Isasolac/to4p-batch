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
    


if __name__ == '__main__':
    main()
