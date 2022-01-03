import cv2
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


def generate_contrtast_pictures(source_path, destiny_path):
    files = [file for file in os.listdir(source_path) if file.endswith(".jpg") or file.endswith(".jpeg")]
    for file in files:
        original_img = cv2.imread(os.path.join(source_path, file))
        img_yuv = cv2.cvtColor(original_img, cv2.COLOR_BGR2YUV)
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        filename, file_extension = os.path.splitext(file)
        cv2.imwrite(os.path.join(destiny_path, filename + "_contrast" + file_extension), output)
        xml_file_name = file.replace(".jpeg", ".xml").replace(".jpg", ".xml")
        # write XML
        xml_path = os.path.join(source_path, "annotations", xml_file_name)

        if not os.path.exists(os.path.join(destiny_path, "annotations")):
            os.makedirs(os.path.join(destiny_path, "annotations"))

        copy_and_rename_xml(xml_path, os.path.join(destiny_path, "annotations", filename + "_contrast" + ".xml"), filename + "_contrast" + file_extension)

