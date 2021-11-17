import cv2
import os
import random
import argparse
import re
import numpy
import math
import xml.etree.ElementTree as ET
import uuid
from . segmentation.segmentation import *




def get_images_and_annotation(images_path, xml_path):
    xmls = [xml_file for xml_file in os.listdir(xml_path) if xml_file.endswith('xml')]
    xmls.sort()
    images = [image_file for image_file in os.listdir(images_path) if image_file.endswith('jpg') or image_file.endswith('JPG')]
    images.sort()
    if len(xmls) != len(images):
        raise ValueError("The count does not match")
    return [images, xmls]


def generate_stains(images_path, xml_path, classes, result_path, max_height=100, max_width=100, min_height = 30, min_width = 30):
    images, xmls =  get_images_and_annotation(images_path=images_path, xml_path=xml_path)
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    for index, image in enumerate(images):
        tree = ET.parse(os.path.join(xml_path, xmls[index]))
        root = tree.getroot()
        for object in root.iter('object'):
            children = list(object)
            name = children[0].text
            if name in classes:
                print('Class to process: {0}'.format(name))
                for coordinate in object.iter('bndbox'):
                    children_coordinates = list(coordinate)
                    xmin = int(children_coordinates[0].text)
                    ymin = int(children_coordinates[1].text)
                    xmax = int(children_coordinates[2].text)
                    ymax = int(children_coordinates[3].text)
                    print("Original coordinates {0} {1} {2} {3}".format(xmin, ymin, xmax, ymax))
                    height = xmax - xmin
                    width = ymax - ymin
                    print("Height is {0}".format(height))
                    print("Weight is {0}".format(width))
                    if height <= max_height and width <= max_width \
                            and height >= min_height and width >= min_width:
                        prefix = name
                        file_name = prefix + "_" + str(uuid.uuid4().hex) + ".png"
                        source_img = cv2.imread(os.path.join(images_path, image))
                        result_file_name = grabcut(
                            source_img,
                            [xmin, ymin, width, height],
                            os.path.join(result_path, file_name), crop_image = True)
                        print(result_file_name)

def test_inside():
    test()


test_inside()
