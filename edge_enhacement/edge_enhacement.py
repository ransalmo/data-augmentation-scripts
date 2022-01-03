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

def generate_kernel():
    kernel_sharpen = numpy.array([[-1, -1, -1, -1, -1],
                                 [-1, 2, 2, 2, -1],
                                 [-1, 2, 8, 2, -1],
                                 [-1, 2, 2, 2, -1],
                                 [-1, -1, -1, -1, -1]]) / 8.0
    return kernel_sharpen


def generate_edge_enhacement_pictures(source_path, destiny_path):
    files = [file for file in os.listdir(source_path) if file.endswith(".jpg") or file.endswith(".jpeg")]
    for file in files:
        original_img = cv2.imread(os.path.join(source_path, file))
        kernel = generate_kernel()
        output = cv2.filter2D(original_img, -1, kernel)
        filename, file_extension = os.path.splitext(file)
        new_filename = filename + "_enha" + file_extension
        cv2.imwrite(os.path.join(destiny_path, new_filename), output)
        xml_file_name = file.replace(".jpeg", ".xml").replace(".jpg", ".xml")
        new_xml_file_name = new_filename.replace(".jpeg", ".xml").replace(".jpg", ".xml")
        # write XML
        xml_path = os.path.join(source_path, "annotations", xml_file_name)

        if not os.path.exists(os.path.join(destiny_path, "annotations")):
            os.makedirs(os.path.join(destiny_path, "annotations"))

        new_xml_path = os.path.join(os.path.join(destiny_path, "annotations"), new_xml_file_name)

        copy_and_rename_xml(xml_path, new_xml_path,
                            new_filename)


