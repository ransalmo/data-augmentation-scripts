import random

import cv2
import numpy
import os

import shutil
import xml.etree.ElementTree as ET

def copy_and_rename_xml(original_path, new_path, reference_image_name):
    original_directory, original_image_file_name = os.path.split(original_path)
    shutil.copy(original_path, new_path)
    #change xml metadata
    tree = ET.parse(new_path)
    root = tree.getroot()
    for fileNameXML in root.iter('filename'):
        fileNameXML.text = reference_image_name
    tree.write(new_path)

def generate_horizontal_kernel(size):
    kernel = numpy.zeros((size, size))
    kernel[int((size - 1) / 2), :] = numpy.ones(size)
    kernel = kernel / size
    return kernel


def generate_vertical_kernel(size):
    kernel = numpy.zeros((size, size))
    kernel[:, int((size - 1) / 2)] = numpy.ones(size)
    kernel = kernel / size
    return kernel


def generate_motion_blur_pictures(source_path, destiny_path, horizontal=True):
    post_fix = "_blur" if horizontal else "_blur_vertical"
    files = [file for file in os.listdir(source_path) if file.endswith(".jpg") or file.endswith(".jpeg")]
    for file in files:
        filter_size = random.randrange(25,40)
        original_img = cv2.imread(os.path.join(source_path, file))
        if horizontal:
            kernel = generate_horizontal_kernel(filter_size)
        else:
            kernel = generate_vertical_kernel(filter_size)
        output = cv2.filter2D(original_img, -1, kernel)

        im_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

        filename, file_extension = os.path.splitext(file)
        new_image_name = filename + post_fix + file_extension
        cv2.imwrite(os.path.join(destiny_path, new_image_name), output)

        xml_file_name = file.replace(".jpeg", ".xml").replace(".jpg", ".xml")
        new_xml_file_name = new_image_name.replace(".jpeg", ".xml").replace(".jpg", ".xml")

        # write XML
        xml_path = os.path.join(source_path, "annotations", xml_file_name)

        if not os.path.exists(os.path.join(destiny_path, "annotations")):
            os.makedirs(os.path.join(destiny_path, "annotations"))

        new_xml_path = os.path.join(os.path.join(destiny_path, "annotations"), new_xml_file_name)

        copy_and_rename_xml(xml_path, new_xml_path,
                            new_image_name)