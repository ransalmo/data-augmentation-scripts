import os
import shutil
import xml.etree.ElementTree as ET


def copy_and_rename_xml(original_path, new_path, reference_image_name):
    original_directory, original_image_file_name = os.path.split(original_path)
    try:
        shutil.copy(original_path, new_path)
        #change xml metadata
        tree = ET.parse(new_path)
        root = tree.getroot()
        for fileNameXML in root.iter('filename'):
            fileNameXML.text = reference_image_name
        tree.write(new_path)
    except:
        print("Problemas procesando el archivo {0}".format(original_path))