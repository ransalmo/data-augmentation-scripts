import os
import xml.etree.ElementTree as ET
import shutil


def copy_clean_images(source_images_path, destiny_path):
    if not os.path.exists(source_images_path):
        raise ValueError('Source directory does not exist')

    if not os.path.exists(os.path.join(source_images_path, "annotations")):
        raise ValueError('Source directory does not exist')

    annotations_path = os.path.join(source_images_path, "annotations")

    files = os.listdir(annotations_path)
    files = [file for file in files if file.endswith('.XML') or file.endswith('.xml')]

    for file in files:
        objects_detected = 0
        discard = False
        file_path = os.path.join(annotations_path, file)
        tree = ET.parse(file_path)
        root = tree.getroot()
        for member in root.findall('object'):
            label = member[0].text
            if label != 'hoja' and label != 'dano':
                discard = True
                break
        if not discard:
            image_file = file.replace(".xml", ".jpg")
            shutil.copy(os.path.join(source_images_path, image_file), destiny_path)

