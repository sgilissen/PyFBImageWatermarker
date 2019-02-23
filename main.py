"""
Python Image Watermarker + Facebook uploader
This module takes a folder of image files, watermarks them and uploads them to a Facebook page
"""
__author__ = "Steve Gilissen"
__copyright__ = "Copyright 2018, Steve Gilissen"
__credits__ = ["Steve Gilissen"]
__version__ = "0.0.1"
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

# ---------------------------------------------------------
#                       GLOBAL VARIABLES
# ---------------------------------------------------------
configfile = "config.json"
config = ""
cfg = {
    "page_id"      : "my_page_id",
    "access_token" : "my_access_token"
    }

api = get_api(cfg)

# ---------------------------------------------------------
#                       CORE FUNCTIONS
# ---------------------------------------------------------
parser = argparse.ArgumentParser(description='Watermark an image.')
parser.add_argument('-i', '--input', action='store', dest='inputfile', help='Input file')
parser.add_argument('-o', '--output', action='store', dest='outputfile', help='Output file')
parser.add_argument('-w', '--watermark', action='store', dest='watermarkfile', help='Watermark file')
args = parser.parse_args()

def LogToConsole(message):
    print("[" + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "] " + message)

def WatermarkPhoto(input_path, output_path, watermark_path, position):
    base_image = Image.open(input_path)
    watermark = Image.open(watermark_path)

    width, height = base_image.size

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    transparent.show()
    transparent.save(output_image_path)

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        #raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")
        LogToConsole("Folder: " + args.inputfile + " is not a valid path")

def CheckConfig():
    if path.exists(configfile):
        with open(configfile) as json_data_file:
            config = json.load(json_data_file)
    else:
        defaultconfig = '{"page_id": "not_set", "access_token":"not_set"}'


LogToConsole("Input: " + args.inputfile)
dir_path(args.inputfile)
