"""
Python Image Watermarker + Facebook uploader
This module takes a folder of image files, watermarks them and uploads them to a Facebook page
"""
__author__ = "Steve Gilissen"
__copyright__ = "Copyright 2018, Steve Gilissen"
__credits__ = ["Steve Gilissen"]
__version__ = "0.0.2"
__maintainer__ = "Steve Gilissen"
__status__ = "Development"

# ---------------------------------------------------------
#                       MODULE IMPORTS
# ---------------------------------------------------------
from PIL import Image
import argparse
from datetime import datetime
import os
import facebook as fb
import json
import os.path
from os import path
import random

# ---------------------------------------------------------
#                       GLOBAL VARIABLES
# ---------------------------------------------------------
configfile = "config.json"
messagefile = "messages.txt"
page_access_token = ''
page_id = ''

workdir = '_temp'
workfile = ''

# ---------------------------------------------------------
#                       CORE FUNCTIONS
# ---------------------------------------------------------
parser = argparse.ArgumentParser(description='Watermark an image.')
parser.add_argument('inputfile', help='Input file')
parser.add_argument('outputfile', help='Output file')
parser.add_argument('-w', '--watermark', action='store', dest='watermarkfile', help='Watermark file')
args = parser.parse_args()


def main():
    log_to_console("Checking config...")
    if args.watermarkfile is not None:
        log_to_console("Watermarking...")
        watermark_photo(args.inputfile, args.outputfile, args.watermarkfile, (0, 0))
    else:
        log_to_console("No watermark requested.")
        workfile = args.inputfile


    if check_config():
        if path.exists(messagefile):
            log_to_console("Message file {0} found! Choosing random line...".format(messagefile))
            randomline = random.choice(list(open(messagefile)))
        else:
            log_to_console("Message file {0} not found. Proceeding without message...".format(messagefile))
            randomline = ''
        post_to_fb(randomline, workfile)
    else:
        log_to_console("Please check your config.")

def log_to_console(message):
    print("[" + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "] " + message)


def watermark_photo(input_path, output_path, watermark_path, position):
    base_image = Image.open(input_path)
    watermark = Image.open(watermark_path)

    width, height = base_image.size

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    fill_color = (255, 255, 255)
    if transparent.mode in ('RGBA', 'LA'):
        log_to_console("Image is in RGBA (possibly a PNG). Adding white background to replace transparency.")
        background = Image.new(transparent.mode[:-1], transparent.size, fill_color)
        background.paste(transparent, transparent.split()[-1])
        transparent = background
    log_to_console("Saving as jpg.")
    transparent.save(output_path)
    global workfile
    workfile = output_path
    print(workfile)


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        # raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")
        log_to_console("Folder: " + args.inputfile + " is not a valid path")


def check_config():
    if path.exists(configfile):
        with open(configfile) as json_data_file:
            config = json.load(json_data_file)
            try:
                if config['page_id'] == "change me" or config['access_token'] == "change me":
                    log_to_console("The config.json file is incorrect. Please modify the file to reflect your page.")
                    return False
                else:
                    log_to_console("Config file found. Proceeding...")
                    global page_access_token
                    page_access_token = config['access_token']
                    global page_id
                    page_id = config['page_id']
                    return True
            except KeyError:
                log_to_console("The config.json file is invalid.")
                return False
    else:
        defaultconfig = {"page_id": "change me", "access_token": "change me"}
        log_to_console("Config file not found. A generic config.json has been created. "
                       "Please modify to suit your needs.")
        with open('config.json', 'w') as outfile:
            json.dump(defaultconfig, outfile)


def post_to_fb(message, image):
    log_to_console("Posting to Facebook...")
    graph = fb.GraphAPI(access_token=page_access_token, version='2.8')
    # graph.put_object(page_id, connection_name='feed', message=message)
    photo = open(image, "rb")
    # graph.put_object(page_id, "photos", message="Watermarked doggo sez O HAI!", src=photo.read())
    graph.put_photo(image=photo, message=message, album_path=page_id + "/photos")
    log_to_console("Done!")


if __name__ == "__main__":
    # execute only if run as a script
    main()
