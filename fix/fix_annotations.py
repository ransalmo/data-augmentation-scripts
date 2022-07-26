import cv2
import argparse
import os
import shutil
import xml.etree.ElementTree as ET


def get_image_size(imagePath):
    print("Reading file: {0}".format(imagePath))
    img = cv2.imread(imagePath)
    height, width, channels = img.shape
    return (height, width)


def fix_annotations_xml(imagePath, xmlPath):
    height, width = get_image_size(imagePath)
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    print(xmlPath)
    has_changes = False
    matches = root.findall('.//bndbox')
    for bndBoxXML in matches:
        item = bndBoxXML
        has_issues = False
        children = bndBoxXML.getchildren()
        xmin = int(children[0].text)
        ymin = int(children[1].text)
        xmax = int(children[2].text)
        ymax = int(children[3].text)
        print("Coordenadas originales {0} {1} {2} {3}".format(xmin, ymin, xmax, ymax))

        if xmin >= width:
            has_issues = True
        if ymin >= height:
            has_issues = True
        if xmax > width:
            has_issues = True
        if ymax > height:
            has_issues = True
        if has_issues:
            #root.remove(item)
            has_changes = True
        else:
            print("No hay cambios")
    if has_changes:
        shutil.copy(imagePath, "/Volumes/Randy/Fallout")
        shutil.copy(xmlPath, os.path.join("/Volumes/Randy/Fallout", "annotations"))
        #tree.write(xmlPath)

    return has_changes


def main(path):
    if not os.path.exists(path):
        raise ValueError("The source folder doesn't exist, please check the path")
    print("Path to process {0}".format(path))
    files = [file for file in os.listdir(path) if (file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".jpeg")) and not file.startswith(".")]
    filesToProcess = len(files)
    print("Files to process: {0}".format(filesToProcess))
    fixed = 0
    for index, file in enumerate(files):
        print("Processing file {0}".format(file))
        image_path = os.path.join(path, file)
        xml_file = file.replace(".jpg", ".xml").replace(".JPG",".xml").replace(".jpeg",".xml")
        xml_path = os.path.join(path,"annotations", xml_file)
        fix_done = fix_annotations_xml(image_path, xml_path)
        if fix_done:
            fixed = fixed + 1
            print("File {0} fixed, recommend review", xml_path)

    print("Images fixed {0}".format(fixed))


if __name__ == "__main__":
    path = "/Volumes/Randy/data/synteticv2"
    main(path)



# def main(args):
#     if not os.path.exists(args.path):
#         raise ValueError("The source folder doesn't exist, please check the path")
#     files = [file for file in os.listdir(args.path) if file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".jpeg")]
#     filesToProcess = len(files)
#     print("Files to process: {0}".format(filesToProcess))
#     for index, file in enumerate(files):
#         filePath = os.path.join(args.path, file)
#         print("Processing image {0}".format(index + 1))
#         fix_annotations_xml(filePath)
#
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--path", help="folder path were images are located",
#                         default=os.path.join(os.getcwd(), "images", "annotations"))
#     args = parser.parse_args()
#     main(args)


